"""Escalate stale premium-customer follow-ups without starting lane work."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import OWNER_AGENT_ID, ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "premium_customer_followup_escalation.v1"
DEFAULT_JSON = REPORTS_DIR / "customer-followup-escalation-v1-20260620.json"
DEFAULT_MD = REPORTS_DIR / "customer-followup-escalation-v1-20260620.md"
LEDGER_JSON = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.json"
LEDGER_MD = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.md"
UPDATE_FEED_JSON = REPORTS_DIR / "customer-update-feed-v3-20260620.json"
UPDATE_FEED_MD = REPORTS_DIR / "customer-update-feed-v3-20260620.md"
DEFAULT_TARGET_SURFACE = "ai_resources_lab"


ESCALATION_ACTIONS = {
    "stale_unacknowledged": "Ask AI Resources to decide whether to reuse the lane manager, evolve one existing agent, or route to CEO decision batch.",
    "stale_active": "Ask AI Resources to inspect whether the task is genuinely progressing or needs manager intervention.",
    "blocked": "Prepare a CEO decision-batch item naming the gate, owner, and requested decision.",
    "ownerless": "Ask AI Resources to repair lane ownership or recommend one explicit owner.",
    "stale_other": "Ask AI Resources to classify the stale state and choose repair, park, or CEO decision batch.",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _attention_items(monitor: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in monitor.get("followup_tasks", []) if item.get("requires_intake_attention")]


def _escalation_item(item: dict[str, Any], target_surface: str) -> dict[str, Any]:
    monitor_status = item.get("monitor_status", "unknown")
    return {
        "task_id": item.get("task_id"),
        "lane_id": item.get("lane_id"),
        "owner_agent_id": item.get("owner_agent_id"),
        "task_status": item.get("status"),
        "monitor_status": monitor_status,
        "age_minutes": item.get("age_minutes"),
        "priority": item.get("priority"),
        "current_next_action": item.get("next_action"),
        "target_surface": "ceo_decision_batch" if monitor_status == "blocked" else target_surface,
        "recommended_action": ESCALATION_ACTIONS.get(
            monitor_status,
            "Ask AI Resources to classify the follow-up and either repair, park with revisit condition, or escalate to CEO decision batch.",
        ),
        "must_not_do": [
            "do_not_claim_or_start_lane_task_from_escalation",
            "do_not_open_browser_or_create_account",
            "do_not_perform_public_or_payment_action",
            "do_not_duplicate_lane_manager_work",
        ],
    }


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Premium Customer Follow-Up Escalation V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Input id: `{payload.get('input_id') or 'all'}`",
        f"Target surface: `{payload['target_surface']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Summary",
        "",
        payload["summary"],
        "",
        "## Escalation Items",
        "",
        "| Lane | Task | Monitor Status | Target | Recommended Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in payload["escalation_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.get('lane_id')}`",
                    f"`{item.get('task_id')}`",
                    md_cell(item.get("monitor_status"), 80),
                    f"`{item.get('target_surface')}`",
                    md_cell(item.get("recommended_action"), 260),
                ]
            )
            + " |"
        )
    if not payload["escalation_items"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Created Local Task",
            "",
            f"`{payload.get('escalation_task_id') or ''}`",
            "",
            "## Boundary",
            "",
            "This packet creates local triage/decision work only. It does not claim lane tasks, start workers, open browsers, create accounts, publish, submit, trade, spend, call APIs, approve service requests, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _load_json_or_default(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _lane_owner(conn: sqlite3.Connection, lane_id: str) -> str | None:
    row = conn.execute("SELECT owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    return row["owner_agent_id"] if row else None


def _upsert_escalation_task(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    md_path: Path,
) -> str:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    target_lane = payload["target_surface"] if payload["target_surface"] != "ceo_decision_batch" else "premium_customer_intake"
    task_id = f"task-{input_fragment}-followup-escalation-{safe_id_fragment(payload['target_surface'], 40)}"
    owner = _lane_owner(conn, target_lane) or OWNER_AGENT_ID
    duplicate_key = f"{payload.get('input_id') or 'all'}:followup-escalation:{payload['target_surface']}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(?, ?, ?, 'new', 93, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          title=excluded.title,
          status=tasks.status,
          priority=excluded.priority,
          owner_agent_id=COALESCE(tasks.owner_agent_id, excluded.owner_agent_id),
          duplicate_key=excluded.duplicate_key,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at
        """,
        (
            task_id,
            target_lane,
            f"Triage stale premium customer follow-ups for {payload.get('input_id') or 'all'}",
            owner,
            duplicate_key,
            str(md_path),
            payload["next_action"],
            ts,
            ts,
        ),
    )
    return task_id


def _record_escalation_run(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    json_path: Path,
    md_path: Path,
) -> None:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    run_task_id = f"task-premium-customer-followup-escalation-v1-{input_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, 'premium_customer_intake', ?, 'complete', 88, ?, ?, ?, ?, ?, ?, ?, ?)
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
            run_task_id,
            f"Escalate stale premium customer follow-ups for {payload.get('input_id') or 'all'}",
            OWNER_AGENT_ID,
            f"premium-customer-followup-escalation:{payload.get('input_id') or 'all'}",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (f"artifact-premium-customer-followup-escalation-json-{input_fragment}", "customer_followup_escalation_json", json_path, "Machine-readable premium customer follow-up escalation packet."),
        (f"artifact-premium-customer-followup-escalation-md-{input_fragment}", "customer_followup_escalation", md_path, "Human-readable premium customer follow-up escalation packet."),
    ]:
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, 'premium_customer_intake', ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              lane_id=excluded.lane_id,
              task_id=excluded.task_id,
              kind=excluded.kind,
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes
            """,
            (artifact_id, run_task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": payload.get("input_id"),
        "target_surface": payload["target_surface"],
        "escalation_task_id": payload.get("escalation_task_id"),
        "escalation_item_count": len(payload["escalation_items"]),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, 'premium_customer_intake', ?, ?, 'premium_customer_followup_escalation_written', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            f"trace-event-premium-customer-followup-escalation-{input_fragment}",
            f"trace-premium-customer-followup-escalation-{input_fragment}",
            run_task_id,
            OWNER_AGENT_ID,
            ts,
            "premium_customer_followup_escalation_v1",
            f"Wrote escalation packet for {len(payload['escalation_items'])} premium customer follow-up tasks.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, 'premium_customer_intake', ?, 'customer_followup_escalation', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-premium-customer-followup-escalation-{input_fragment}",
            run_task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def _update_ledger(payload: dict[str, Any], ledger_json: Path, ledger_md: Path) -> None:
    ledger = _load_json_or_default(ledger_json, {})
    if not ledger:
        return
    entries = []
    for entry in ledger.get("entries", []):
        if payload.get("input_id") and entry.get("input_id") != payload["input_id"]:
            entries.append(entry)
            continue
        updated = dict(entry)
        updated["followup_escalation"] = {
            "status": payload["status"],
            "target_surface": payload["target_surface"],
            "report_path": payload["md_path"],
            "escalation_task_id": payload.get("escalation_task_id"),
            "generated_utc": payload["generated_utc"],
        }
        entries.append(updated)
    ledger["entries"] = entries
    ledger["generated_utc"] = payload["generated_utc"]
    _write_json(ledger_json, ledger)
    lines = [
        "# Customer Request Routing Ledger V1",
        "",
        f"Generated UTC: {ledger.get('generated_utc')}",
        f"Owner: `{ledger.get('owner_agent_id')}`",
        f"Status: {ledger.get('status')}",
        f"JSON mirror: `{ledger_json}`",
        "",
        "## Entries",
        "",
        "| Input | Class | Primary Route | Status | Follow-Up Monitor | Follow-Up Escalation | Next Artifact |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in ledger.get("entries", []):
        monitor_status = item.get("followup_monitor", {}).get("status", "")
        escalation_status = item.get("followup_escalation", {}).get("status", "")
        lines.append(
            f"| `{item.get('input_id')}` | `{item.get('input_class')}` | `{item.get('primary_route')}` | {md_cell(item.get('status'), 80)} | `{monitor_status}` | `{escalation_status}` | `{item.get('next_artifact')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This ledger is local routing memory only. It does not approve gates, start workers, open browsers, create accounts, publish, upload, trade, spend, call APIs, or perform external actions.",
            "",
        ]
    )
    ledger_md.write_text("\n".join(lines), encoding="utf-8")


def _update_feed(payload: dict[str, Any], feed_json: Path, feed_md: Path) -> None:
    feed = _load_json_or_default(
        feed_json,
        {
            "schema_version": "customer_update_feed.v3",
            "owner_agent_id": OWNER_AGENT_ID,
            "status": "active_local_update_feed",
            "updates": [],
            "zero_side_effect_boundary": {"external_side_effects": False},
        },
    )
    update = {
        "update_id": f"customer-update-followup-escalation-{payload.get('input_id') or 'all'}",
        "generated_utc": payload["generated_utc"],
        "summary": f"Follow-up escalation packet written for {len(payload['escalation_items'])} stale customer lane tasks.",
        "applied": [
            "followup_escalation_packet_written",
            "ai_resources_or_ceo_triage_task_created",
            "routing_ledger_escalation_status_updated",
        ],
        "route_packet_path": payload["md_path"],
        "human_action_needed": False,
        "next": payload["next_action"],
    }
    updates = [item for item in feed.get("updates", []) if item.get("update_id") != update["update_id"]]
    feed["updates"] = [update] + updates
    feed["generated_utc"] = payload["generated_utc"]
    feed["schema_version"] = "customer_update_feed.v3"
    feed["owner_agent_id"] = OWNER_AGENT_ID
    feed["status"] = "active_local_update_feed"
    feed["zero_side_effect_boundary"] = {"external_side_effects": False}
    _write_json(feed_json, feed)
    lines = [
        "# Customer Update Feed V3",
        "",
        f"Generated UTC: {feed.get('generated_utc')}",
        f"Owner: `{feed.get('owner_agent_id')}`",
        f"Status: {feed.get('status')}",
        f"JSON mirror: `{feed_json}`",
        "",
        "## Updates",
        "",
    ]
    for item in feed.get("updates", []):
        lines.extend(
            [
                f"### {item.get('generated_utc')} - {item.get('summary')}",
                "",
                f"Route packet: `{item.get('route_packet_path', '')}`",
                "",
                f"Human action needed: {'yes' if item.get('human_action_needed') else 'none'}.",
                "",
                f"Next: {item.get('next', '')}",
                "",
            ]
        )
    feed_md.write_text("\n".join(lines), encoding="utf-8")


def escalate_premium_customer_followups(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    monitor_path = Path(args.monitor_report)
    monitor = _load_json(monitor_path)
    generated = getattr(args, "now_utc", None) or now_utc()
    target_surface = getattr(args, "target_surface", None) or DEFAULT_TARGET_SURFACE
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    ledger_json = Path(getattr(args, "ledger_json", None) or LEDGER_JSON)
    ledger_md = Path(getattr(args, "ledger_md", None) or LEDGER_MD)
    update_feed_json = Path(getattr(args, "update_feed_json", None) or UPDATE_FEED_JSON)
    update_feed_md = Path(getattr(args, "update_feed_md", None) or UPDATE_FEED_MD)
    attention_items = _attention_items(monitor)
    escalation_items = [_escalation_item(item, target_surface) for item in attention_items]
    status = "escalation_needed" if escalation_items else "no_escalation_needed"
    summary = (
        f"{len(escalation_items)} follow-up tasks from monitor `{monitor_path}` require controlled triage."
        if escalation_items
        else f"Monitor `{monitor_path}` has no follow-up tasks requiring escalation."
    )
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "input_id": monitor.get("input_id"),
        "monitor_report_path": str(monitor_path),
        "target_surface": target_surface,
        "summary": summary,
        "escalation_items": escalation_items,
        "next_action": (
            "AI Resources should triage stale customer follow-ups and either evolve/reuse one existing worker, park with revisit condition, or draft a CEO decision-batch item."
            if escalation_items
            else "No escalation task needed; continue follow-up monitoring."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "escalation_task_id": None,
    }
    if escalation_items and not getattr(args, "no_db_record", False):
        payload["escalation_task_id"] = _upsert_escalation_task(conn, payload, md_path)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_escalation_run(conn, payload, json_path, md_path)
        _update_ledger(payload, ledger_json, ledger_md)
        _update_feed(payload, update_feed_json, update_feed_md)
    return payload


def write_premium_customer_followup_escalation(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = escalate_premium_customer_followups(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload.get("input_id"),
                "target_surface": payload["target_surface"],
                "escalation_item_count": len(payload["escalation_items"]),
                "escalation_task_id": payload.get("escalation_task_id"),
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
