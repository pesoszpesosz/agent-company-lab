"""Seed bounded local next tasks for active lanes with no open work."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import MANAGER_PACKET_DIR, REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_lane_next_task_seed.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
TERMINAL_STATUSES = {"done", "complete", "completed", "cancelled", "closed"}

LANE_PROFILES: dict[str, dict[str, Any]] = {
    "content_and_social_growth": {
        "priority": 78,
        "title": "Continue local content and social growth proof",
        "expected_artifact": "reports/content-and-social-growth/content-and-social-growth-local-proof-packet-v1-{day}.md",
        "next_action": (
            "Produce one compact local content/social growth proof packet from the current lane goal: pick one "
            "candidate audience angle, draft a no-posting content/reply plan, name the public-action gate, and "
            "record the next evidence step. Do not post, message, follow, open accounts, or operate a browser."
        ),
    },
    "digital_products_templates_plugins": {
        "priority": 78,
        "title": "Continue local digital product readiness proof",
        "expected_artifact": "reports/digital-products/digital-products-local-readiness-packet-v1-{day}.md",
        "next_action": (
            "Produce one local product-readiness packet from the current lane goal: choose one template/plugin "
            "candidate, define packaging scope, acceptance checks, pricing/release assumptions, and service gates. "
            "Do not publish, list, sell, call APIs, or spend."
        ),
    },
    "lead_generation_and_sales": {
        "priority": 77,
        "title": "Continue local lead generation offer proof",
        "expected_artifact": "reports/lead-generation-and-sales/lead-generation-local-offer-proof-v1-{day}.md",
        "next_action": (
            "Produce one local lead-generation proof packet from the current lane goal: define a non-spam offer, "
            "qualification rules, a small local lead worksheet shape, and the outreach approval gate. Do not email, "
            "DM, scrape, enrich, or contact anyone."
        ),
    },
    "local_trading_strategy_research": {
        "priority": 76,
        "title": "Continue local trading paper-research proof",
        "expected_artifact": "reports/local-trading/local-trading-paper-research-proof-v1-{day}.md",
        "next_action": (
            "Produce one paper-only trading research packet from the current lane goal: choose a hypothesis, define "
            "replay data requirements, risk notes, and next local test. Do not place orders, connect brokers, use "
            "paid data, or trade."
        ),
    },
    "premium_customer_intake": {
        "priority": 82,
        "title": "Continue premium customer routing queue proof",
        "expected_artifact": "reports/premium-customer-intake/premium-customer-routing-queue-proof-v1-{day}.md",
        "next_action": (
            "Produce one premium-customer intake queue packet: check preserved raw input, route ledger, update feed, "
            "and pending follow-ups; summarize newest customer-facing state without copying raw material into CEO "
            "context. Do not start workers, approve service requests, open browsers, or take external actions."
        ),
    },
    "security_bounty_private_reports": {
        "priority": 78,
        "title": "Continue local security bounty report-readiness proof",
        "expected_artifact": "reports/security-bounty-private-reports/security-bounty-local-readiness-proof-v1-{day}.md",
        "next_action": (
            "Produce one local security-bounty readiness packet from the current lane goal: identify a safe in-scope "
            "research target class, report template, evidence standard, and private-submission gate. Do not touch live "
            "targets, scan, exploit, submit, or contact programs."
        ),
    },
    "web3_airdrops_grants_hackathons": {
        "priority": 76,
        "title": "Continue local Web3 opportunity proof",
        "expected_artifact": "reports/web3-airdrops-grants-hackathons/web3-local-opportunity-proof-v1-{day}.md",
        "next_action": (
            "Produce one local Web3 grants/airdrops/hackathons opportunity packet from the current lane goal: choose "
            "one opportunity type, map eligibility/evidence requirements, define wallet/account gates, and name the "
            "next local validation step. Do not connect wallets, sign messages, submit forms, or spend gas."
        ),
    },
}

LANE_FOLLOWUP_PROFILES: dict[str, dict[str, Any]] = {
    "content_and_social_growth": {
        "priority": 76,
        "title": "Continue local content reply-target shortlist",
        "expected_artifact": "reports/content-and-social-growth/ai-builder-reply-target-shortlist-v1-{day}.md",
        "next_action": (
            "Create a local-only AI-builder reply-target shortlist shell from the proof packet: 3 to 5 candidate rows "
            "from local artifacts and non-account public sources only, with source family, gate status, topic, "
            "evidence strength, reply-gap signal, content use, risk flags, next allowed action, approval required, "
            "and X/Grok/Radar placeholders marked awaiting service approval. Do not browse, post, reply, message, "
            "follow, call APIs, or take public action."
        ),
    },
    "digital_products_templates_plugins": {
        "priority": 76,
        "title": "Continue local digital product release-review checklist",
        "expected_artifact": "reports/digital-products/agent-skill-starter-kit-release-review-checklist-v1-{day}.md",
        "next_action": (
            "Prepare a local release-review checklist for Agent Skill Starter Kit v0 using existing artifacts only; "
            "compare Lemon Squeezy and Gumroad from local evidence, select one provisional no-publish route, and list "
            "exact human decisions needed before any service request is approved or started. Do not browse, create "
            "accounts, zip, upload, publish, list, sell, call APIs, spend, or mutate ownership."
        ),
    },
    "lead_generation_and_sales": {
        "priority": 76,
        "title": "Continue local lead-generation no-send approval draft",
        "expected_artifact": "reports/lead-generation-and-sales/lead-generation-outreach-approval-request-draft-v1-{day}.md",
        "next_action": (
            "Write a no-send approval request packet for exactly one lead-generation route, or a blocked-route memo if "
            "the route cannot satisfy gates without browsing, enrichment, account action, or real prospect data. Do "
            "not email, DM, scrape, enrich, import CRM data, contact anyone, open browsers, or approve service work."
        ),
    },
    "local_trading_strategy_research": {
        "priority": 74,
        "title": "Continue local trading no-key replay prep",
        "expected_artifact": "reports/local-trading/local-trading-no-key-replay-prep-v1-{day}.md",
        "next_action": (
            "Create a no-key local replay prep artifact: inventory non-sensitive local trading/backtest files, select "
            "one candidate dataset readable without credentials or external calls, define frozen replay columns, and "
            "state paper-only stop conditions. Do not inspect accounts, connect brokers, call APIs, use paid data, "
            "place orders, spend, or trade."
        ),
    },
    "premium_customer_intake": {
        "priority": 80,
        "title": "Continue premium customer intake watch",
        "expected_artifact": "reports/premium-customer-intake/premium-customer-routing-queue-watch-v1-{day}.md",
        "next_action": (
            "Maintain a local premium-customer intake watch: check for new preserved raw material, route ledger changes, "
            "update-feed gaps, and lane follow-up drift; if no new material exists, write a compact no-new-input watch "
            "status and next check condition. Keep raw material out of CEO context and do not start workers, approve "
            "service requests, open browsers, call APIs, or take external actions."
        ),
    },
    "security_bounty_private_reports": {
        "priority": 76,
        "title": "Continue local security evidence source ranking",
        "expected_artifact": "reports/security-bounty-private-reports/security-source-ranking-packet-v1-{day}.md",
        "next_action": (
            "Create a source-ranking packet for the imported security evidence set, then promote exactly one candidate "
            "to local_proof_needed or scope_unverified_blocked. Use local evidence only; do not touch live targets, "
            "scan, exploit, submit reports, contact programs, open browsers, call APIs, or approve route gates."
        ),
    },
    "web3_airdrops_grants_hackathons": {
        "priority": 74,
        "title": "Continue local Gitcoin application readiness checklist",
        "expected_artifact": "reports/web3-airdrops-grants-hackathons/gitcoin-local-application-readiness-checklist-v1-{day}.md",
        "next_action": (
            "Create a local-only Gitcoin application readiness checklist: map each draft field to sanitized public-safe "
            "text, cite exact local evidence, mark fields blocked by browser/account/legal/wallet/public-action gates, "
            "score expected value versus paid code bounties, and recommend read-only refresh, gate packets, or parking. "
            "Do not browse, connect wallets, sign, submit forms, spend gas, call APIs, or take public action."
        ),
    },
}


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(getattr(args, "json_path", None) or REPORTS_DIR / f"continuity-lane-next-task-seed-v1-{day}.json")
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"continuity-lane-next-task-seed-v1-{day}.md")
    return json_path, md_path


def _manager_packet_dir(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "manager_packet_dir", None) or MANAGER_PACKET_DIR)


def _active_owned_lanes_without_open_tasks(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    terminal = tuple(TERMINAL_STATUSES)
    placeholders = ",".join("?" for _ in terminal)
    return conn.execute(
        f"""
        SELECT
          l.lane_id,
          l.department,
          l.status,
          l.owner_agent_id,
          l.owner_thread_id,
          COALESCE(SUM(CASE WHEN t.status NOT IN ({placeholders}) THEN 1 ELSE 0 END), 0) AS open_tasks,
          COUNT(t.task_id) AS total_tasks
        FROM lanes l
        LEFT JOIN tasks t ON t.lane_id = l.lane_id
        WHERE l.status = 'active'
          AND l.owner_agent_id IS NOT NULL
          AND l.owner_agent_id != ''
        GROUP BY l.lane_id, l.department, l.status, l.owner_agent_id, l.owner_thread_id
        HAVING open_tasks = 0
        ORDER BY l.lane_id
        """,
        terminal,
    ).fetchall()


def _latest_completed_lane_next_proof(conn: sqlite3.Connection, lane_id: str) -> dict[str, Any] | None:
    terminal = tuple(TERMINAL_STATUSES)
    placeholders = ",".join("?" for _ in terminal)
    rows = conn.execute(
        f"""
        SELECT
          artifact.artifact_id,
          artifact.kind,
          artifact.path_or_url,
          artifact.task_id,
          artifact.created_at,
          artifact.sha256,
          task.completed_at,
          task.updated_at AS task_updated_at
        FROM artifacts artifact
        JOIN tasks task ON task.task_id = artifact.task_id
        WHERE task.lane_id = ?
          AND task.duplicate_key LIKE 'continuity:lane-next-task:%'
          AND task.status IN ({placeholders})
          AND artifact.kind NOT LIKE '%seed%'
          AND artifact.kind NOT LIKE '%input%'
        ORDER BY COALESCE(task.completed_at, task.updated_at, artifact.created_at) DESC, artifact.created_at DESC
        LIMIT 20
        """,
        (lane_id, *terminal),
    ).fetchall()
    for row in rows:
        item = dict(row)
        if Path(item["path_or_url"]).exists():
            item["source"] = "completed_lane_next_proof_artifact"
            item["path_exists"] = True
            return item
    return None


def _manager_packet_evidence(lane_id: str, manager_packet_dir: Path) -> dict[str, Any]:
    manager_packet = manager_packet_dir / f"{lane_id}-manager-packet.md"
    return {
        "artifact_id": None,
        "kind": "manager_packet",
        "path_or_url": str(manager_packet),
        "task_id": None,
        "created_at": None,
        "sha256": sha256_file(manager_packet) if manager_packet.exists() else None,
        "source": "manager_packet",
        "path_exists": manager_packet.exists(),
    }


def _latest_lane_evidence(conn: sqlite3.Connection, lane_id: str, manager_packet_dir: Path) -> dict[str, Any]:
    lane_next_proof = _latest_completed_lane_next_proof(conn, lane_id)
    if lane_next_proof:
        return lane_next_proof
    rows = conn.execute(
        """
        SELECT artifact_id, kind, path_or_url, task_id, created_at, sha256
        FROM artifacts
        WHERE lane_id = ?
          AND (
            kind LIKE '%lane_goal%'
            OR kind LIKE '%current_lane_goal%'
            OR kind LIKE '%continuity%'
            OR path_or_url LIKE '%lane-goal%'
            OR path_or_url LIKE '%lane_goal%'
            OR path_or_url LIKE '%continuity-owner-responses%'
          )
        ORDER BY created_at DESC, artifact_id DESC
        LIMIT 20
        """,
        (lane_id,),
    ).fetchall()
    candidates = [dict(row) for row in rows]
    for candidate in candidates:
        path = Path(candidate["path_or_url"])
        if path.exists():
            candidate["source"] = "latest_lane_goal_artifact"
            candidate["path_exists"] = True
            return candidate
    manager_packet = _manager_packet_evidence(lane_id, manager_packet_dir)
    if manager_packet["path_exists"]:
        manager_packet["source"] = "manager_packet_after_stale_lane_goal_artifacts"
        manager_packet["stale_lane_goal_artifact_count"] = len(candidates)
        return manager_packet
    if candidates:
        candidate = candidates[0]
        candidate["source"] = "latest_lane_goal_artifact_missing_path"
        candidate["path_exists"] = False
        return candidate

    return manager_packet


def _profile_for_lane(lane_id: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    if evidence and evidence.get("source") == "completed_lane_next_proof_artifact" and lane_id in LANE_FOLLOWUP_PROFILES:
        profile = dict(LANE_FOLLOWUP_PROFILES[lane_id])
        profile["profile_stage"] = "proof_followup"
        return profile
    profile = LANE_PROFILES.get(lane_id)
    if profile:
        profile = dict(profile)
        profile["profile_stage"] = "initial_lane_next"
        return profile
    return {
        "priority": 72,
        "title": f"Continue local lane proof for {lane_id}",
        "expected_artifact": f"reports/{safe_id_fragment(lane_id, 80)}/local-lane-proof-packet-v1-{{day}}.md",
        "profile_stage": "generic_lane_next",
        "next_action": (
            "Produce one bounded local proof packet from the current lane goal or manager packet: state the next "
            "artifact, evidence requirement, owner, gate, and revisit condition. Do not create agents, mutate lane "
            "ownership, start workers, approve service requests, open browsers, publish, submit, trade, spend, call "
            "APIs, or contact anyone."
        ),
    }


def _open_seed_task(conn: sqlite3.Connection, lane_id: str, day: str) -> sqlite3.Row | None:
    base_key = f"continuity:lane-next-task:{lane_id}:{day}:%"
    terminal = tuple(TERMINAL_STATUSES)
    placeholders = ",".join("?" for _ in terminal)
    return conn.execute(
        f"""
        SELECT task_id, status, duplicate_key, evidence_required, next_action
        FROM tasks
        WHERE duplicate_key LIKE ?
          AND status NOT IN ({placeholders})
        ORDER BY created_at DESC, task_id DESC
        LIMIT 1
        """,
        (base_key, *terminal),
    ).fetchone()


def _next_sequence(conn: sqlite3.Connection, lane_id: str, day: str) -> str:
    base_key = f"continuity:lane-next-task:{lane_id}:{day}:%"
    count = conn.execute("SELECT COUNT(*) FROM tasks WHERE duplicate_key LIKE ?", (base_key,)).fetchone()[0]
    return f"{int(count) + 1:03d}"


def _seed_lane_task(
    conn: sqlite3.Connection,
    lane: sqlite3.Row,
    evidence: dict[str, Any],
    generated_utc: str,
    no_db_record: bool,
) -> dict[str, Any]:
    lane_id = lane["lane_id"]
    day = generated_utc[:10].replace("-", "")
    profile = _profile_for_lane(lane_id, evidence)
    expected_artifact = profile["expected_artifact"].format(day=day)
    open_seed = _open_seed_task(conn, lane_id, day)
    item: dict[str, Any] = {
        "lane_id": lane_id,
        "department": lane["department"],
        "owner_agent_id": lane["owner_agent_id"],
        "owner_thread_id": lane["owner_thread_id"],
        "source_open_tasks": lane["open_tasks"],
        "source_total_tasks": lane["total_tasks"],
        "evidence_source": evidence["source"],
        "evidence_artifact_id": evidence.get("artifact_id"),
        "evidence_path": evidence["path_or_url"],
        "evidence_path_exists": evidence["path_exists"],
        "expected_artifact": expected_artifact,
        "profile_stage": profile["profile_stage"],
        "priority": profile["priority"],
        "title": profile["title"],
        "next_action": profile["next_action"],
    }
    if open_seed:
        item.update(
            {
                "seed_status": "skipped_open_seed_exists",
                "task_id": open_seed["task_id"],
                "duplicate_key": open_seed["duplicate_key"],
            }
        )
        return item
    sequence = _next_sequence(conn, lane_id, day)
    lane_fragment = safe_id_fragment(lane_id, 70)
    task_id = f"task-continuity-lane-next-task-{day}-{lane_fragment}-{sequence}"
    duplicate_key = f"continuity:lane-next-task:{lane_id}:{day}:{sequence}"
    item.update({"seed_status": "planned" if no_db_record else "created", "task_id": task_id, "duplicate_key": duplicate_key})
    if no_db_record:
        return item

    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(?, ?, ?, 'new', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            task_id,
            lane_id,
            profile["title"],
            profile["priority"],
            lane["owner_agent_id"],
            duplicate_key,
            evidence["path_or_url"],
            profile["next_action"],
            generated_utc,
            generated_utc,
        ),
    )
    evidence_path = Path(evidence["path_or_url"])
    if evidence_path.exists():
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, 'continuity_lane_next_task_seed_evidence', ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              lane_id=excluded.lane_id,
              task_id=excluded.task_id,
              kind=excluded.kind,
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes,
              created_at=excluded.created_at
            """,
            (
                f"artifact-continuity-lane-next-task-seed-evidence-{lane_fragment}-{sequence}",
                lane_id,
                task_id,
                str(evidence_path),
                sha256_file(evidence_path),
                "Seed evidence for the next bounded local lane task.",
                generated_utc,
            ),
        )
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_lane_next_task_seeded', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path,
          created_at=excluded.created_at
        """,
        (
            f"trace-event-continuity-lane-next-task-seed-{lane_fragment}-{sequence}",
            f"trace-continuity-lane-next-task-seed-{day}",
            lane_id,
            task_id,
            lane["owner_agent_id"],
            generated_utc,
            "continuity_lane_next_task_seed_v1",
            f"Seeded next bounded local task for zero-open active lane `{lane_id}`.",
            json.dumps(
                {
                    "duplicate_key": duplicate_key,
                    "evidence_path": evidence["path_or_url"],
                    "expected_artifact": expected_artifact,
                    "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
                },
                sort_keys=True,
            ),
            evidence["path_or_url"],
            generated_utc,
        ),
    )
    return item


def _open_seed_tasks(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    terminal = tuple(TERMINAL_STATUSES)
    placeholders = ",".join("?" for _ in terminal)
    return conn.execute(
        f"""
        SELECT
          t.task_id,
          t.lane_id,
          t.status,
          t.owner_agent_id,
          t.duplicate_key,
          t.evidence_required,
          l.owner_thread_id
        FROM tasks t
        LEFT JOIN lanes l ON l.lane_id = t.lane_id
        WHERE t.duplicate_key LIKE 'continuity:lane-next-task:%'
          AND t.status NOT IN ({placeholders})
        ORDER BY t.lane_id, t.task_id
        """,
        terminal,
    ).fetchall()


def _repair_open_seed_evidence(
    conn: sqlite3.Connection,
    generated_utc: str,
    manager_packet_dir: Path,
    no_db_record: bool,
) -> list[dict[str, Any]]:
    repairs: list[dict[str, Any]] = []
    for task in _open_seed_tasks(conn):
        current_path = task["evidence_required"] or ""
        if current_path and Path(current_path).exists():
            continue
        fallback = _manager_packet_evidence(task["lane_id"], manager_packet_dir)
        item = {
            "lane_id": task["lane_id"],
            "task_id": task["task_id"],
            "owner_agent_id": task["owner_agent_id"],
            "duplicate_key": task["duplicate_key"],
            "old_evidence_path": current_path,
            "new_evidence_path": fallback["path_or_url"],
            "new_evidence_path_exists": fallback["path_exists"],
            "repair_status": "planned" if no_db_record else "repaired" if fallback["path_exists"] else "missing_fallback",
        }
        repairs.append(item)
        if no_db_record or not fallback["path_exists"]:
            continue
        lane_fragment = safe_id_fragment(task["lane_id"], 70)
        task_fragment = safe_id_fragment(task["task_id"], 90)
        fallback_path = Path(fallback["path_or_url"])
        conn.execute(
            """
            UPDATE tasks
            SET evidence_required = ?, updated_at = ?
            WHERE task_id = ?
            """,
            (str(fallback_path), generated_utc, task["task_id"]),
        )
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, 'continuity_lane_next_task_seed_evidence_repair', ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              lane_id=excluded.lane_id,
              task_id=excluded.task_id,
              kind=excluded.kind,
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes,
              created_at=excluded.created_at
            """,
            (
                f"artifact-continuity-lane-next-task-seed-evidence-repair-{lane_fragment}-{task_fragment}",
                task["lane_id"],
                task["task_id"],
                str(fallback_path),
                sha256_file(fallback_path),
                "Repaired stale seed evidence path by linking the current manager packet.",
                generated_utc,
            ),
        )
    return repairs


def _counts(items: list[dict[str, Any]], repairs: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "lanes_without_open_tasks": len(items),
        "seed_tasks_created": sum(1 for item in items if item["seed_status"] == "created"),
        "seed_tasks_planned": sum(1 for item in items if item["seed_status"] == "planned"),
        "open_seed_tasks_reused": sum(1 for item in items if item["seed_status"] == "skipped_open_seed_exists"),
        "missing_evidence_paths": sum(1 for item in items if not item["evidence_path_exists"]),
        "open_seed_evidence_repaired": sum(1 for item in repairs if item["repair_status"] == "repaired"),
        "open_seed_evidence_repair_planned": sum(1 for item in repairs if item["repair_status"] == "planned"),
        "open_seed_missing_evidence_unrepaired": sum(1 for item in repairs if item["repair_status"] == "missing_fallback"),
    }


def _status_from_counts(counts: dict[str, int]) -> str:
    if counts["seed_tasks_created"]:
        return "seeded"
    if counts["seed_tasks_planned"]:
        return "planned_report_only"
    if counts["open_seed_evidence_repaired"]:
        return "repaired_existing_seed_evidence"
    if counts["open_seed_tasks_reused"]:
        return "already_seeded"
    return "no_zero_open_lanes"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Lane Next Task Seed V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Counts",
        "",
        "| Count | Value |",
        "| --- | ---: |",
    ]
    for key, value in payload["counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Seed Decisions",
            "",
            "| Lane | Owner | Status | Task | Evidence | Expected Artifact |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["seed_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['owner_agent_id']}`",
                    f"`{item['seed_status']}`",
                    f"`{item['task_id']}`",
                    md_cell(item.get("evidence_path"), 180),
                    md_cell(item.get("expected_artifact"), 120),
                ]
            )
            + " |"
        )
    if not payload["seed_items"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Evidence Repairs",
            "",
            "| Lane | Task | Status | Old Evidence | New Evidence |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["repair_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['task_id']}`",
                    f"`{item['repair_status']}`",
                    md_cell(item.get("old_evidence_path"), 150),
                    md_cell(item.get("new_evidence_path"), 150),
                ]
            )
            + " |"
        )
    if not payload["repair_items"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This command creates bounded local lane tasks only. It does not create agents, mutate lane ownership, start workers, approve service requests, open browsers, create accounts, publish, submit, trade, spend, call external APIs, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-continuity-lane-next-task-seed-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Seed next local tasks for zero-open active lanes', 'complete', 91, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          title=excluded.title,
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          duplicate_key=excluded.duplicate_key,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            AI_RESOURCES_LANE,
            AI_RESOURCES_OWNER,
            f"continuity:lane-next-task-seed:{day}",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (
            f"artifact-continuity-lane-next-task-seed-json-{day}",
            "continuity_lane_next_task_seed_json",
            json_path,
            "Machine-readable continuity lane next-task seed report.",
        ),
        (
            f"artifact-continuity-lane-next-task-seed-md-{day}",
            "continuity_lane_next_task_seed",
            md_path,
            "Human-readable continuity lane next-task seed report.",
        ),
    ]:
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              lane_id=excluded.lane_id,
              task_id=excluded.task_id,
              kind=excluded.kind,
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes,
              created_at=excluded.created_at
            """,
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'continuity_lane_next_task_seed', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-continuity-lane-next-task-seed-{day}",
            AI_RESOURCES_LANE,
            task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )


def seed_continuity_lane_next_tasks(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    manager_packet_dir = _manager_packet_dir(args)
    no_db_record = bool(getattr(args, "no_db_record", False))
    repair_items = _repair_open_seed_evidence(conn, generated, manager_packet_dir, no_db_record)
    lanes = _active_owned_lanes_without_open_tasks(conn)
    seed_items = []
    for lane in lanes:
        evidence = _latest_lane_evidence(conn, lane["lane_id"], manager_packet_dir)
        seed_items.append(_seed_lane_task(conn, lane, evidence, generated, no_db_record))
    counts = _counts(seed_items, repair_items)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": _status_from_counts(counts),
        "counts": counts,
        "seed_items": seed_items,
        "repair_items": repair_items,
        "next_action": (
            "Regenerate continuity watchdog, manager packets, CEO state, and lane thread manifest."
            if counts["seed_tasks_created"] or counts["open_seed_evidence_repaired"]
            else "No lane next-task seed creation is currently needed."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not no_db_record:
        _record_run(conn, payload, json_path, md_path)
        conn.commit()
    return payload


def write_continuity_lane_next_task_seed_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = seed_continuity_lane_next_tasks(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
