"""Monitor premium-customer lane follow-up tasks for stalled work."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import OWNER_AGENT_ID, ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "premium_customer_followup_monitor.v1"
DEFAULT_JSON = REPORTS_DIR / "customer-followup-monitor-v1-20260620.json"
DEFAULT_MD = REPORTS_DIR / "customer-followup-monitor-v1-20260620.md"
LEDGER_JSON = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.json"
LEDGER_MD = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.md"
UPDATE_FEED_JSON = REPORTS_DIR / "customer-update-feed-v3-20260620.json"
UPDATE_FEED_MD = REPORTS_DIR / "customer-update-feed-v3-20260620.md"


TERMINAL_STATUSES = {"complete", "cancelled"}
BLOCKED_STATUSES = {"blocked", "needs_review"}


def _load_json_or_default(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _age_minutes(row: sqlite3.Row, now_value: str) -> int | None:
    base = parse_utc(row["updated_at"] or row["created_at"])
    now_dt = parse_utc(now_value)
    if not base or not now_dt:
        return None
    return max(0, int((now_dt - base).total_seconds() // 60))


def _followup_query(input_id: str | None) -> tuple[str, tuple[Any, ...]]:
    if input_id:
        return (
            """
            SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
                   evidence_required, next_action, created_at, updated_at, started_at, completed_at,
                   lease_owner_agent_id, lease_expires_at
            FROM tasks
            WHERE duplicate_key LIKE ?
            ORDER BY priority DESC, lane_id, created_at
            """,
            (f"{input_id}:lane-followup:%",),
        )
    return (
        """
        SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
               evidence_required, next_action, created_at, updated_at, started_at, completed_at,
               lease_owner_agent_id, lease_expires_at
        FROM tasks
        WHERE duplicate_key LIKE ?
        ORDER BY updated_at DESC, priority DESC, lane_id
        """,
        ("%:lane-followup:%",),
    )


def _lane_known(conn: sqlite3.Connection, lane_id: str) -> bool:
    return bool(conn.execute("SELECT 1 FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone())


def _followup_input_id(duplicate_key: str | None) -> str | None:
    marker = ":lane-followup:"
    text = str(duplicate_key or "")
    if marker not in text:
        return None
    return text.split(marker, 1)[0] or None


def _completed_owner_acknowledgement(conn: sqlite3.Connection, row: sqlite3.Row) -> sqlite3.Row | None:
    lane_id = str(row["lane_id"] or "")
    input_id = _followup_input_id(row["duplicate_key"])
    duplicate_keys = [f"all:owner-acknowledgement:{lane_id}"]
    if input_id:
        duplicate_keys.insert(0, f"{input_id}:owner-acknowledgement:{lane_id}")
    placeholders = ",".join("?" for _ in duplicate_keys)
    return conn.execute(
        f"""
        SELECT task_id, duplicate_key, evidence_required, next_action, updated_at
        FROM tasks
        WHERE duplicate_key IN ({placeholders})
          AND status IN ('complete', 'cancelled')
        ORDER BY updated_at DESC, task_id
        LIMIT 1
        """,
        tuple(duplicate_keys),
    ).fetchone()


def _classify(row: sqlite3.Row, lane_known: bool, age_minutes: int | None, stale_after_minutes: int) -> tuple[str, bool]:
    if not lane_known or not row["owner_agent_id"]:
        return "ownerless", True
    status = row["status"]
    if status in TERMINAL_STATUSES:
        return "complete", False
    if status in BLOCKED_STATUSES:
        return "blocked", True
    is_stale = age_minutes is not None and age_minutes >= stale_after_minutes
    if status == "new":
        return ("stale_unacknowledged" if is_stale else "unacknowledged"), is_stale
    if status == "in_progress":
        return ("stale_active" if is_stale else "active"), is_stale
        return ("stale_other" if is_stale else "open_other"), is_stale


def _collect_followups(
    conn: sqlite3.Connection,
    input_id: str | None,
    now_value: str,
    stale_after_minutes: int,
) -> list[dict[str, Any]]:
    sql, params = _followup_query(input_id)
    rows = conn.execute(sql, params).fetchall()
    items: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row, now_value)
        known = _lane_known(conn, row["lane_id"])
        monitor_status, attention = _classify(row, known, age, stale_after_minutes)
        acknowledgement = _completed_owner_acknowledgement(conn, row) if monitor_status == "stale_unacknowledged" else None
        if acknowledgement:
            monitor_status = "owner_acknowledged_open"
            attention = False
        items.append(
            {
                "task_id": row["task_id"],
                "lane_id": row["lane_id"],
                "title": row["title"],
                "status": row["status"],
                "monitor_status": monitor_status,
                "requires_intake_attention": attention,
                "priority": row["priority"],
                "owner_agent_id": row["owner_agent_id"],
                "lane_known": known,
                "duplicate_key": row["duplicate_key"],
                "evidence_required": row["evidence_required"],
                "next_action": row["next_action"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "age_minutes": age,
                "lease_owner_agent_id": row["lease_owner_agent_id"],
                "lease_expires_at": row["lease_expires_at"],
                "owner_acknowledgement_task_id": acknowledgement["task_id"] if acknowledgement else None,
                "owner_acknowledgement_evidence": acknowledgement["evidence_required"] if acknowledgement else None,
            }
        )
    return items


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {"total": len(items)}
    for item in items:
        key = item["monitor_status"]
        counts[key] = counts.get(key, 0) + 1
        if item["requires_intake_attention"]:
            counts["requires_intake_attention"] = counts.get("requires_intake_attention", 0) + 1
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Premium Customer Follow-Up Monitor V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Input filter: `{payload.get('input_id') or 'all'}`",
        f"Stale after minutes: `{payload['stale_after_minutes']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for key, count in sorted(payload["counts"].items()):
        lines.append(f"| `{key}` | {count} |")
    lines.extend(
        [
            "",
            "## Follow-Up Tasks",
            "",
            "| Lane | Task | Owner | Task Status | Monitor Status | Age Min | Attention | Next Action |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for item in payload["followup_tasks"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['task_id']}`",
                    md_cell(item.get("owner_agent_id"), 100),
                    md_cell(item["status"], 60),
                    md_cell(item["monitor_status"], 80),
                    str(item["age_minutes"] if item["age_minutes"] is not None else ""),
                    "yes" if item["requires_intake_attention"] else "no",
                    md_cell(item.get("next_action"), 220),
                ]
            )
            + " |"
        )
    if not payload["followup_tasks"]:
        lines.append("| none |  |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This monitor writes local reports and audit rows only. It does not claim tasks, start workers, open browsers, create accounts, publish, submit, trade, spend, call APIs, or approve service requests.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


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
        updated["followup_monitor"] = {
            "status": payload["status"],
            "report_path": payload["md_path"],
            "counts": payload["counts"],
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
        "| Input | Class | Primary Route | Status | Follow-Up Monitor | Next Artifact |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in ledger.get("entries", []):
        monitor = item.get("followup_monitor", {})
        monitor_status = monitor.get("status", "")
        lines.append(
            f"| `{item.get('input_id')}` | `{item.get('input_class')}` | `{item.get('primary_route')}` | {md_cell(item.get('status'), 80)} | `{monitor_status}` | `{item.get('next_artifact')}` |"
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
        "update_id": f"customer-update-followup-monitor-{payload.get('input_id') or 'all'}",
        "generated_utc": payload["generated_utc"],
        "summary": f"Follow-up monitor checked {payload['counts']['total']} lane tasks; {payload['counts'].get('requires_intake_attention', 0)} need intake attention.",
        "applied": [
            "followup_monitor_report_written",
            "routing_ledger_monitor_status_updated",
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


def _record_monitor_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    suffix = payload.get("input_id") or "all"
    task_id = f"task-premium-customer-followup-monitor-v1-{suffix}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, 'premium_customer_intake', ?, 'complete', 87, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"Monitor premium customer follow-ups for {suffix}",
            OWNER_AGENT_ID,
            f"premium-customer-followup-monitor:{suffix}",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (f"artifact-premium-customer-followup-monitor-json-{suffix}", "customer_followup_monitor_json", json_path, "Machine-readable premium customer follow-up monitor report."),
        (f"artifact-premium-customer-followup-monitor-md-{suffix}", "customer_followup_monitor", md_path, "Human-readable premium customer follow-up monitor report."),
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
            (artifact_id, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": payload.get("input_id"),
        "counts": payload["counts"],
        "report_path": str(md_path),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, 'premium_customer_intake', ?, ?, 'premium_customer_followup_monitor_checked', ?, ?, ?, ?, ?, ?)
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
            f"trace-event-premium-customer-followup-monitor-{suffix}",
            f"trace-premium-customer-followup-monitor-{suffix}",
            task_id,
            OWNER_AGENT_ID,
            ts,
            "premium_customer_followup_monitor_v1",
            f"Checked {payload['counts']['total']} premium customer follow-up tasks; {payload['counts'].get('requires_intake_attention', 0)} need intake attention.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, 'premium_customer_intake', ?, 'customer_followup_monitor', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-premium-customer-followup-monitor-{suffix}",
            task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def monitor_premium_customer_followups(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    stale_after = int(getattr(args, "stale_after_minutes", 60))
    input_id = getattr(args, "input_id", None)
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    ledger_json = Path(getattr(args, "ledger_json", None) or LEDGER_JSON)
    ledger_md = Path(getattr(args, "ledger_md", None) or LEDGER_MD)
    update_feed_json = Path(getattr(args, "update_feed_json", None) or UPDATE_FEED_JSON)
    update_feed_md = Path(getattr(args, "update_feed_md", None) or UPDATE_FEED_MD)
    items = _collect_followups(conn, input_id, generated, stale_after)
    counts = _counts(items)
    attention = counts.get("requires_intake_attention", 0)
    status = "attention_needed" if attention else "clear"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "input_id": input_id,
        "stale_after_minutes": stale_after,
        "counts": counts,
        "followup_tasks": items,
        "next_action": (
            "Escalate ownerless, blocked, or stale follow-ups to AI Resources or the CEO decision batch."
            if attention
            else "No intake escalation required; continue monitoring generated follow-up tasks."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_monitor_run(conn, payload, json_path, md_path)
        _update_ledger(payload, ledger_json, ledger_md)
        _update_feed(payload, update_feed_json, update_feed_md)
    return payload


def write_premium_customer_followup_monitor(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = monitor_premium_customer_followups(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload["input_id"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
