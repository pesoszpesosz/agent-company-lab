"""Create safe local keepalive deliveries for always-on governance lanes."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import timedelta
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "lane_runtime_governance_keepalive.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
CRITICAL_GOVERNANCE_AGENT_IDS = {
    "lane-manager-ai_resources_lab-20260620",
    "premium-customer-context-router-20260621",
    "continuity-watchdog-worker-20260621",
}


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"lane-runtime-governance-keepalive-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"lane-runtime-governance-keepalive-v1-{day}.md")
    packet_dir = Path(
        getattr(args, "packet_dir", None) or REPORTS_DIR / f"lane-runtime-governance-keepalive-v1-{day}"
    )
    return json_path, md_path, packet_dir


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_boundary() -> dict[str, Any]:
    return {
        "thread_messages_sent": 0,
        "worker_starts": 0,
        "browser_sessions_started": 0,
        "external_api_calls": 0,
        "service_requests_approved_or_started": 0,
        "public_actions": 0,
        "wallet_payment_trading_actions": 0,
        "external_side_effects": False,
    }


def _lease_expiry(generated_utc: str, lease_minutes: int) -> str:
    generated_dt = parse_utc(generated_utc)
    if generated_dt is None:
        raise SystemExit(f"Invalid --now-utc: {generated_utc}")
    return (generated_dt + timedelta(minutes=lease_minutes)).isoformat(timespec="seconds").replace("+00:00", "Z")


def _available_sessions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT session_id, concurrency_limit, active_lease_count
        FROM account_capacity_sessions
        WHERE surface = 'codex'
          AND status = 'available'
          AND active_lease_count < concurrency_limit
        ORDER BY (concurrency_limit - active_lease_count) DESC, session_id ASC
        """
    ).fetchall()
    sessions: list[dict[str, Any]] = []
    for row in rows:
        slots = max(0, int(row["concurrency_limit"]) - int(row["active_lease_count"]))
        for _ in range(slots):
            sessions.append({"session_id": row["session_id"]})
    return sessions


def _always_on_lane_targets(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT p.lane_id, p.cadence_minutes, p.max_parallel_tasks, l.owner_agent_id, l.owner_thread_id,
               a.status AS agent_status
        FROM lane_runtime_policies p
        JOIN lanes l ON l.lane_id = p.lane_id
        LEFT JOIN agents a ON a.agent_id = l.owner_agent_id
        WHERE p.runtime_mode = 'always_on'
          AND COALESCE(l.status, '') = 'active'
        ORDER BY p.lane_id
        """
    ).fetchall()
    return [
        {
            "target_kind": "always_on_lane",
            "target_id": str(row["lane_id"]),
            "duplicate_scope": str(row["lane_id"]),
            "lane_id": row["lane_id"],
            "cadence_minutes": row["cadence_minutes"],
            "owner_agent_id": row["owner_agent_id"],
            "owner_thread_id": row["owner_thread_id"],
            "agent_status": row["agent_status"],
        }
        for row in rows
    ]


def _critical_governance_agent_targets(
    conn: sqlite3.Connection,
    covered_threads: set[str],
) -> list[dict[str, Any]]:
    if not CRITICAL_GOVERNANCE_AGENT_IDS:
        return []
    placeholders = ",".join("?" for _ in CRITICAL_GOVERNANCE_AGENT_IDS)
    rows = conn.execute(
        f"""
        SELECT agent_id, role_id, thread_id, status
        FROM agents
        WHERE agent_id IN ({placeholders})
        ORDER BY agent_id
        """,
        tuple(sorted(CRITICAL_GOVERNANCE_AGENT_IDS)),
    ).fetchall()
    targets: list[dict[str, Any]] = []
    for row in rows:
        thread_id = str(row["thread_id"] or "")
        if thread_id in covered_threads:
            continue
        targets.append(
            {
                "target_kind": "critical_governance_agent",
                "target_id": str(row["agent_id"]),
                "duplicate_scope": f"agent:{row['agent_id']}",
                "lane_id": AI_RESOURCES_LANE,
                "cadence_minutes": 15,
                "owner_agent_id": row["agent_id"],
                "owner_thread_id": thread_id,
                "agent_status": row["status"],
            }
        )
    return targets


def _governance_targets(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    lane_targets = _always_on_lane_targets(conn)
    covered_threads = {str(item["owner_thread_id"] or "") for item in lane_targets if item.get("owner_thread_id")}
    agent_targets = _critical_governance_agent_targets(conn, covered_threads)
    return lane_targets + agent_targets


def _latest_keepalive_time(conn: sqlite3.Connection, duplicate_scope: str) -> str | None:
    row = conn.execute(
        """
        SELECT MAX(COALESCE(d.delivered_at, d.updated_at, d.created_at)) AS latest_at
        FROM lane_runtime_thread_deliveries d
        JOIN tasks t ON t.task_id = d.task_id
        WHERE t.duplicate_key LIKE ?
        """,
        (f"governance-keepalive:{duplicate_scope}:%",),
    ).fetchone()
    return str(row["latest_at"] or "") or None


def _open_keepalive_exists(conn: sqlite3.Connection, duplicate_scope: str, now_value: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM lane_runtime_thread_deliveries d
        JOIN tasks t ON t.task_id = d.task_id
        WHERE t.duplicate_key LIKE ?
          AND t.status NOT IN ('complete', 'cancelled')
          AND (
            t.lease_expires_at IS NULL
            OR t.lease_expires_at > ?
          )
          AND d.status IN ('ready_to_send', 'send_approved', 'delivered', 'send_failed')
        LIMIT 1
        """,
        (f"governance-keepalive:{duplicate_scope}:%", now_value),
    ).fetchone()
    return row is not None


def _target_due(conn: sqlite3.Connection, target: dict[str, Any], now_value: str) -> tuple[bool, str]:
    duplicate_scope = str(target["duplicate_scope"])
    if str(target.get("agent_status") or "") != "active":
        return False, "owner_agent_not_active"
    if not str(target.get("owner_thread_id") or "").startswith("codex-thread:"):
        return False, "missing_codex_owner_thread"
    if _open_keepalive_exists(conn, duplicate_scope, now_value):
        return False, "open_keepalive_already_exists"
    latest = _latest_keepalive_time(conn, duplicate_scope)
    if not latest:
        return True, "no_prior_keepalive"
    latest_dt = parse_utc(latest)
    now_dt = parse_utc(now_value)
    cadence = max(1, int(target.get("cadence_minutes") or 15))
    if latest_dt is None or now_dt is None:
        return True, "invalid_latest_keepalive_time"
    if latest_dt + timedelta(minutes=cadence) <= now_dt:
        return True, "cadence_elapsed"
    return False, "cadence_not_elapsed"


def _task_id(target_key: str, generated_utc: str) -> str:
    fragment = generated_utc.replace("-", "").replace(":", "").replace("T", "-").replace("Z", "")
    return f"task-governance-keepalive-{safe_id_fragment(target_key, 64)}-{fragment}"


def _delivery_id(task_id: str) -> str:
    return f"delivery-governance-keepalive-{safe_id_fragment(task_id, 90)}"


def _write_packet(path: Path, item: dict[str, Any]) -> None:
    lines = [
        "# Governance Keepalive Packet v1",
        "",
        f"Generated UTC: `{item['generated_utc']}`",
        f"Lane: `{item['lane_id']}`",
        f"Target kind: `{item['target_kind']}`",
        f"Target id: `{item['target_id']}`",
        f"Task: `{item['task_id']}`",
        f"Owner agent: `{item['owner_agent_id']}`",
        f"Owner thread: `{item['owner_thread_id']}`",
        f"Session: `{item['session_id']}`",
        f"Lease expires: `{item['lease_expires_at']}`",
        "",
        "## Mission",
        "",
        item["next_action"],
        "",
        "## Boundary",
        "",
        "This packet authorizes local governance/status work only. It does not start browsers, create agents, mutate ownership, approve service requests, publish, submit, spend, trade, call APIs, contact anyone, or take external side effects.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_prompt(path: Path, item: dict[str, Any]) -> None:
    prompt = "\n".join(
        [
            "Continue your active lane goal using this CEO control-plane dispatch.",
            "",
            f"Task: `{item['task_id']}`",
            f"Lane: `{item['lane_id']}`",
            "Runtime mode: `always_on`",
            f"Lease owner: `{item['owner_agent_id']}`",
            f"Lease expires: `{item['lease_expires_at']}`",
            f"Dispatch packet: `{item['packet_path']}`",
            "",
            "Evidence:",
            item["evidence_required"],
            "",
            "Next action:",
            item["next_action"],
            "",
            "Boundary:",
            "Do not start browsers, create agents, mutate ownership, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone. Work locally only and write the required evidence artifact or an explicit park/revisit packet.",
            "",
            "When finished, leave the task evidence path and a short completion summary in your thread.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")


def _upsert_keepalive(
    conn: sqlite3.Connection,
    target: dict[str, Any],
    session_id: str,
    generated_utc: str,
    lease_expires_at: str,
    packet_dir: Path,
    no_db_record: bool,
) -> dict[str, Any]:
    lane_id = str(target["lane_id"])
    target_id = str(target["target_id"])
    duplicate_scope = str(target["duplicate_scope"])
    task_id = _task_id(duplicate_scope, generated_utc)
    delivery_id = _delivery_id(task_id)
    packet_path = packet_dir / f"{safe_id_fragment(task_id, 90)}.md"
    prompt_path = packet_dir / f"{safe_id_fragment(task_id, 90)}-prompt.md"
    evidence_required = (
        f"reports/{lane_id}/governance-keepalive-{generated_utc[:10]}.md or an equivalent local status artifact"
    )
    next_action = (
        "Run one bounded local governance/status pass for your lane: read the latest CEO restore brief and current "
        "operator inbox, identify whether your lane has actionable safe local work, record any blocker as an exact "
        "gate, and write/register a compact local status artifact. Do not create duplicate workers or broaden scope."
    )
    item = {
        "delivery_id": delivery_id,
        "task_id": task_id,
        "lane_id": lane_id,
        "target_kind": target["target_kind"],
        "target_id": target_id,
        "duplicate_scope": duplicate_scope,
        "session_id": session_id,
        "owner_agent_id": target["owner_agent_id"],
        "owner_thread_id": target["owner_thread_id"],
        "thread_id_for_tool": str(target["owner_thread_id"]).removeprefix("codex-thread:"),
        "lease_expires_at": lease_expires_at,
        "evidence_required": evidence_required,
        "next_action": next_action,
        "packet_path": str(packet_path),
        "prompt_path": str(prompt_path),
        "generated_utc": generated_utc,
    }
    _write_packet(packet_path, item)
    _write_prompt(prompt_path, item)
    if not no_db_record:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at, lease_owner_agent_id,
              lease_expires_at, started_at
            )
            VALUES(?, ?, 'Run always-on governance keepalive', 'in_progress', 99, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
              status='in_progress',
              priority=excluded.priority,
              owner_agent_id=excluded.owner_agent_id,
              evidence_required=excluded.evidence_required,
              next_action=excluded.next_action,
              updated_at=excluded.updated_at,
              lease_owner_agent_id=excluded.lease_owner_agent_id,
              lease_expires_at=excluded.lease_expires_at
            """,
            (
                task_id,
                lane_id,
                target["owner_agent_id"],
                f"governance-keepalive:{duplicate_scope}:{generated_utc[:16]}",
                evidence_required,
                next_action,
                generated_utc,
                generated_utc,
                target["owner_agent_id"],
                lease_expires_at,
                generated_utc,
            ),
        )
        conn.execute(
            """
            INSERT INTO lane_runtime_thread_deliveries(
              delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
              packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
              created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, 'ready_to_send', 0, NULL, NULL, ?, ?)
            ON CONFLICT(delivery_id) DO UPDATE SET
              session_id=excluded.session_id,
              owner_agent_id=excluded.owner_agent_id,
              owner_thread_id=excluded.owner_thread_id,
              packet_path=excluded.packet_path,
              prompt_path=excluded.prompt_path,
              status=CASE
                WHEN lane_runtime_thread_deliveries.delivered_at IS NOT NULL THEN lane_runtime_thread_deliveries.status
                WHEN lane_runtime_thread_deliveries.status IN (
                  'delivered', 'send_approval_parked', 'superseded_parked'
                ) THEN lane_runtime_thread_deliveries.status
                ELSE excluded.status
              END,
              last_error=CASE
                WHEN lane_runtime_thread_deliveries.delivered_at IS NOT NULL THEN lane_runtime_thread_deliveries.last_error
                WHEN lane_runtime_thread_deliveries.status IN (
                  'delivered', 'send_approval_parked', 'superseded_parked'
                ) THEN lane_runtime_thread_deliveries.last_error
                ELSE excluded.last_error
              END,
              updated_at=excluded.updated_at
            """,
            (
                delivery_id,
                task_id,
                lane_id,
                session_id,
                target["owner_agent_id"],
                target["owner_thread_id"],
                str(packet_path),
                str(prompt_path),
                generated_utc,
                generated_utc,
            ),
        )
        conn.execute(
            """
            UPDATE account_capacity_sessions
            SET active_lease_count = active_lease_count + 1,
                updated_at = ?
            WHERE session_id = ?
            """,
            (generated_utc, session_id),
        )
        conn.commit()
    return {**item, "status": "ready_to_send"}


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Governance Keepalive v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
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
            "## Keepalives",
            "",
            "| Lane | Delivery | Thread | Prompt |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in payload["keepalives"]:
        lines.append(
            "| "
            + " | ".join(
                [
            f"`{item['target_kind']}:{item['target_id']}`",
                    f"`{item['delivery_id']}`",
                    f"`{item['thread_id_for_tool']}`",
                    md_cell(item["prompt_path"], 100),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Skipped",
            "",
            "| Lane | Reason |",
            "| --- | --- |",
        ]
    )
    for item in payload["skipped_lanes"]:
        lines.append(f"| `{item['lane_id']}` | `{item['reason']}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This report creates local-only keepalive delivery rows. It does not send thread messages, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-governance-keepalive-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write lane runtime governance keepalive report', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          status=excluded.status,
          priority=excluded.priority,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            AI_RESOURCES_LANE,
            AI_RESOURCES_OWNER,
            f"lane-runtime-governance-keepalive:{day}",
            str(md_path),
            payload.get("next_action") or "",
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path_value, notes in [
        (
            f"artifact-lane-runtime-governance-keepalive-json-{day}",
            "lane_runtime_governance_keepalive_json",
            json_path,
            "Machine-readable always-on governance keepalive report.",
        ),
        (
            f"artifact-lane-runtime-governance-keepalive-md-{day}",
            "lane_runtime_governance_keepalive",
            md_path,
            "Human-readable always-on governance keepalive report.",
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
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path_value), sha256_file(path_value), notes, ts),
        )
    conn.commit()


def _status(counts: dict[str, int]) -> str:
    if counts["keepalives_created"]:
        return "keepalives_ready_to_send"
    if counts["available_capacity_slots"] <= 0 and counts["due_lanes"]:
        return "pending_capacity"
    if counts["due_lanes"]:
        return "blocked"
    return "no_keepalives_due"


def write_lane_runtime_governance_keepalive(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path, packet_dir = _report_paths(generated, args)
    max_keepalives = max(0, int(getattr(args, "max_keepalives", 2)))
    lease_minutes = max(1, int(getattr(args, "lease_minutes", 30)))
    sessions = _available_sessions(conn)
    targets = _governance_targets(conn)
    lease_expires_at = _lease_expiry(generated, lease_minutes)
    keepalives: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    due_targets = 0
    no_db_record = bool(getattr(args, "no_db_record", False))
    for target in targets:
        due, reason = _target_due(conn, target, generated)
        if not due:
            skipped.append(
                {
                    "lane_id": target["lane_id"],
                    "target_kind": target["target_kind"],
                    "target_id": target["target_id"],
                    "reason": reason,
                }
            )
            continue
        due_targets += 1
        if len(keepalives) >= max_keepalives:
            skipped.append(
                {
                    "lane_id": target["lane_id"],
                    "target_kind": target["target_kind"],
                    "target_id": target["target_id"],
                    "reason": "max_keepalives_reached",
                }
            )
            continue
        if not sessions:
            skipped.append(
                {
                    "lane_id": target["lane_id"],
                    "target_kind": target["target_kind"],
                    "target_id": target["target_id"],
                    "reason": "no_available_capacity",
                }
            )
            continue
        session = sessions.pop(0)
        keepalives.append(
            _upsert_keepalive(
                conn,
                target,
                str(session["session_id"]),
                generated,
                lease_expires_at,
                packet_dir,
                no_db_record,
            )
        )
    counts = {
        "always_on_lanes_seen": sum(1 for item in targets if item["target_kind"] == "always_on_lane"),
        "critical_governance_agents_seen": sum(
            1 for item in targets if item["target_kind"] == "critical_governance_agent"
        ),
        "governance_targets_seen": len(targets),
        "due_lanes": due_targets,
        "due_targets": due_targets,
        "available_capacity_slots": len(sessions) + len(keepalives),
        "keepalives_created": len(keepalives),
        "skipped_lanes": len(skipped),
    }
    status = _status(counts)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "counts": counts,
        "keepalives": keepalives,
        "skipped_lanes": skipped,
        "next_action": (
            "Send ready keepalive delivery prompts through the existing thread delivery preflight."
            if keepalives
            else "No governance keepalive delivery is ready."
        ),
        "zero_side_effect_boundary": _safe_boundary(),
        "json_path": str(json_path),
        "md_path": str(md_path),
        "packet_dir": str(packet_dir),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not no_db_record:
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_lane_runtime_governance_keepalive_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_lane_runtime_governance_keepalive(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
            },
            indent=2,
        )
    )


__all__ = [
    "write_lane_runtime_governance_keepalive",
    "write_lane_runtime_governance_keepalive_cli",
]
