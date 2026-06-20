"""AI Resources triage for premium-customer follow-up escalations."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "ai_resources_customer_followup_triage.v1"
DEFAULT_JSON = REPORTS_DIR / "ai-resources-customer-followup-triage-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ai-resources-customer-followup-triage-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"


DECISION_LABELS = {
    "reuse_existing_owner": "Reuse existing owner",
    "evolve_existing_agent": "Evolve existing agent",
    "park_with_revisit_condition": "Park with revisit condition",
    "ceo_decision_batch": "CEO decision batch",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _triage_decision(item: dict[str, Any]) -> tuple[str, str, str]:
    monitor_status = str(item.get("monitor_status") or "unknown")
    target_surface = str(item.get("target_surface") or "")
    if monitor_status == "blocked" or target_surface == "ceo_decision_batch":
        return (
            "ceo_decision_batch",
            "Blocked follow-up needs a compact CEO decision item naming the gate and requested operator choice.",
            "Draft one CEO decision-batch item; do not unblock, approve, or start the lane task.",
        )
    if monitor_status == "stale_unacknowledged":
        return (
            "reuse_existing_owner",
            "The lane already has an owner; the fastest non-overlap repair is an owner acknowledgement packet.",
            "Ask the existing lane owner to acknowledge, park with reason, or produce the first local follow-up artifact.",
        )
    if monitor_status in {"stale_active", "ownerless"}:
        return (
            "evolve_existing_agent",
            "The lane needs a capability or ownership repair, but not a new parallel worker yet.",
            "Evolve or repair one existing manager/agent with a narrow next action and evidence requirement.",
        )
    return (
        "park_with_revisit_condition",
        "The monitor state is not specific enough to justify new work or a new hire.",
        "Park the item with a revisit condition tied to fresh evidence, owner response, or a later CEO packet.",
    )


def _triage_item(item: dict[str, Any]) -> dict[str, Any]:
    decision, rationale, recommended_action = _triage_decision(item)
    return {
        "task_id": item.get("task_id"),
        "lane_id": item.get("lane_id"),
        "owner_agent_id": item.get("owner_agent_id"),
        "task_status": item.get("task_status"),
        "monitor_status": item.get("monitor_status"),
        "source_target_surface": item.get("target_surface"),
        "decision": decision,
        "decision_label": DECISION_LABELS[decision],
        "rationale": rationale,
        "recommended_action": recommended_action,
        "source_next_action": item.get("current_next_action"),
        "must_not_do": [
            "do_not_start_workers_from_triage",
            "do_not_claim_or_mutate_original_lane_followup",
            "do_not_create_overlapping_agents",
            "do_not_open_browser_or_create_account",
            "do_not_perform_public_payment_trading_or_external_action",
        ],
    }


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = {key: 0 for key in DECISION_LABELS}
    counts["total"] = len(items)
    for item in items:
        counts[item["decision"]] += 1
    return counts


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# AI Resources Customer Follow-Up Triage V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Input id: `{payload.get('input_id') or 'all'}`",
        f"Escalation report: `{payload['escalation_report_path']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Summary",
        "",
        payload["summary"],
        "",
        "## Counts",
        "",
        "| Decision | Count |",
        "| --- | ---: |",
    ]
    for key in ["reuse_existing_owner", "evolve_existing_agent", "park_with_revisit_condition", "ceo_decision_batch"]:
        lines.append(f"| {DECISION_LABELS[key]} | {payload['counts'].get(key, 0)} |")
    lines.extend(
        [
            "",
            "## Triage Items",
            "",
            "| Lane | Task | Monitor Status | Decision | Recommended Action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["triage_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.get('lane_id')}`",
                    f"`{item.get('task_id')}`",
                    md_cell(item.get("monitor_status"), 80),
                    md_cell(item.get("decision_label"), 80),
                    md_cell(item.get("recommended_action"), 260),
                ]
            )
            + " |"
        )
    if not payload["triage_items"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This triage packet writes local reports and audit rows only. It does not claim or mutate original lane follow-ups, start workers, create agents, open browsers, create accounts, publish, submit, trade, spend, call APIs, approve service requests, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_triage_run(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    json_path: Path,
    md_path: Path,
) -> None:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    task_id = f"task-ai-resources-customer-followup-triage-v1-{input_fragment}"
    duplicate_key = f"ai-resources-customer-followup-triage:{payload.get('input_id') or 'all'}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, ?, 'complete', 91, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          lane_id=excluded.lane_id,
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
            f"Triage premium customer follow-up escalation for {payload.get('input_id') or 'all'}",
            AI_RESOURCES_OWNER,
            duplicate_key,
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (f"artifact-ai-resources-customer-followup-triage-json-{input_fragment}", "ai_resources_customer_followup_triage_json", json_path, "Machine-readable AI Resources customer follow-up triage packet."),
        (f"artifact-ai-resources-customer-followup-triage-md-{input_fragment}", "ai_resources_customer_followup_triage", md_path, "Human-readable AI Resources customer follow-up triage packet."),
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
              notes=excluded.notes
            """,
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": payload.get("input_id"),
        "counts": payload["counts"],
        "triage_item_count": len(payload["triage_items"]),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ai_resources_customer_followup_triage_written', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            f"trace-event-ai-resources-customer-followup-triage-{input_fragment}",
            f"trace-ai-resources-customer-followup-triage-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            AI_RESOURCES_OWNER,
            ts,
            "ai_resources_customer_followup_triage_v1",
            f"Wrote AI Resources triage packet for {len(payload['triage_items'])} customer follow-up escalation items.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'ai_resources_customer_followup_triage', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-ai-resources-customer-followup-triage-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def triage_ai_resources_customer_followups(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    escalation_path = Path(args.escalation_report)
    escalation = _load_json(escalation_path)
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    triage_items = [_triage_item(item) for item in escalation.get("escalation_items", [])]
    status = "triage_ready" if triage_items else "no_triage_needed"
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "input_id": escalation.get("input_id"),
        "escalation_report_path": str(escalation_path),
        "summary": (
            f"AI Resources classified {len(triage_items)} customer follow-up escalation items into reuse, evolve, park, or CEO-decision paths."
            if triage_items
            else f"Escalation report `{escalation_path}` has no items requiring AI Resources triage."
        ),
        "counts": _counts(triage_items),
        "triage_items": triage_items,
        "next_action": (
            "Use the triage packet to request owner acknowledgement, evolve one existing agent, park ambiguous work, or draft CEO decision-batch items without starting lane work."
            if triage_items
            else "No AI Resources triage action required; continue monitoring customer follow-ups."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_triage_run(conn, payload, json_path, md_path)
    return payload


def write_ai_resources_customer_followup_triage(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = triage_ai_resources_customer_followups(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload.get("input_id"),
                "triage_item_count": len(payload["triage_items"]),
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
