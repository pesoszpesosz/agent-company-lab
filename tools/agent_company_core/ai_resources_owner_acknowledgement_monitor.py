"""Monitor AI Resources owner acknowledgement requests for stalled responses."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "ai_resources_owner_acknowledgement_monitor.v1"
DEFAULT_JSON = REPORTS_DIR / "ai-resources-owner-acknowledgement-monitor-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ai-resources-owner-acknowledgement-monitor-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
TERMINAL_STATUSES = {"complete", "cancelled"}
BLOCKED_STATUSES = {"blocked", "needs_review"}


def _age_minutes(row: sqlite3.Row, now_value: str) -> int | None:
    base = parse_utc(row["updated_at"] or row["created_at"])
    now_dt = parse_utc(now_value)
    if not base or not now_dt:
        return None
    return max(0, int((now_dt - base).total_seconds() // 60))


def _query(input_id: str | None) -> tuple[str, tuple[Any, ...]]:
    if input_id:
        return (
            """
            SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
                   evidence_required, next_action, created_at, updated_at, started_at, completed_at
            FROM tasks
            WHERE duplicate_key LIKE ?
            ORDER BY priority DESC, lane_id, created_at
            """,
            (f"{input_id}:owner-acknowledgement:%",),
        )
    return (
        """
        SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
               evidence_required, next_action, created_at, updated_at, started_at, completed_at
        FROM tasks
        WHERE duplicate_key LIKE ?
        ORDER BY updated_at DESC, priority DESC, lane_id
        """,
        ("%:owner-acknowledgement:%",),
    )


def _classify(row: sqlite3.Row, age_minutes: int | None, stale_after_minutes: int) -> tuple[str, bool]:
    status = row["status"]
    if not row["owner_agent_id"]:
        return "ownerless", True
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


def _collect(
    conn: sqlite3.Connection,
    input_id: str | None,
    now_value: str,
    stale_after_minutes: int,
) -> list[dict[str, Any]]:
    sql, params = _query(input_id)
    rows = conn.execute(sql, params).fetchall()
    items: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row, now_value)
        monitor_status, attention = _classify(row, age, stale_after_minutes)
        items.append(
            {
                "task_id": row["task_id"],
                "lane_id": row["lane_id"],
                "title": row["title"],
                "status": row["status"],
                "monitor_status": monitor_status,
                "requires_ai_resources_attention": attention,
                "priority": row["priority"],
                "owner_agent_id": row["owner_agent_id"],
                "duplicate_key": row["duplicate_key"],
                "evidence_required": row["evidence_required"],
                "next_action": row["next_action"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "age_minutes": age,
            }
        )
    return items


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {"total": len(items)}
    for item in items:
        key = item["monitor_status"]
        counts[key] = counts.get(key, 0) + 1
        if item["requires_ai_resources_attention"]:
            counts["requires_ai_resources_attention"] = counts.get("requires_ai_resources_attention", 0) + 1
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# AI Resources Owner Acknowledgement Monitor V1",
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
            "## Owner Acknowledgement Tasks",
            "",
            "| Lane | Task | Owner | Task Status | Monitor Status | Age Min | Attention | Next Action |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for item in payload["acknowledgement_tasks"]:
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
                    "yes" if item["requires_ai_resources_attention"] else "no",
                    md_cell(item.get("next_action"), 220),
                ]
            )
            + " |"
        )
    if not payload["acknowledgement_tasks"]:
        lines.append("| none |  |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This monitor writes local reports and audit rows only. It does not mutate acknowledgement tasks, mutate source follow-ups, start workers, create agents, open browsers, create accounts, publish, submit, trade, spend, call APIs, or approve service requests.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    task_id = f"task-ai-resources-owner-acknowledgement-monitor-v1-{input_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, ?, 'complete', 89, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"Monitor owner acknowledgements for {payload.get('input_id') or 'all'}",
            AI_RESOURCES_OWNER,
            f"{payload.get('input_id') or 'all'}:owner-acknowledgement-monitor",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (f"artifact-ai-resources-owner-acknowledgement-monitor-json-{input_fragment}", "ai_resources_owner_acknowledgement_monitor_json", json_path, "Machine-readable owner acknowledgement monitor report."),
        (f"artifact-ai-resources-owner-acknowledgement-monitor-md-{input_fragment}", "ai_resources_owner_acknowledgement_monitor", md_path, "Human-readable owner acknowledgement monitor report."),
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
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ai_resources_owner_acknowledgements_monitored', ?, ?, ?, ?, ?, ?)
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
            f"trace-event-ai-resources-owner-acknowledgement-monitor-{input_fragment}",
            f"trace-ai-resources-owner-acknowledgement-monitor-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            AI_RESOURCES_OWNER,
            ts,
            "ai_resources_owner_acknowledgement_monitor_v1",
            f"Checked {payload['counts']['total']} owner acknowledgement tasks; {payload['counts'].get('requires_ai_resources_attention', 0)} need attention.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'ai_resources_owner_acknowledgement_monitor', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-ai-resources-owner-acknowledgement-monitor-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def monitor_ai_resources_owner_acknowledgements(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    input_id = getattr(args, "input_id", None)
    stale_after = int(getattr(args, "stale_after_minutes", 60))
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    items = _collect(conn, input_id, generated, stale_after)
    counts = _counts(items)
    attention = counts.get("requires_ai_resources_attention", 0)
    status = "attention_needed" if attention else "clear"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "input_id": input_id,
        "stale_after_minutes": stale_after,
        "counts": counts,
        "acknowledgement_tasks": items,
        "next_action": (
            "Escalate stale or blocked owner acknowledgements to CEO decision batch, explicit lane parking, or a lane-owner response repair."
            if attention
            else "No acknowledgement escalation required; continue monitoring owner responses."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_ai_resources_owner_acknowledgement_monitor(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = monitor_ai_resources_owner_acknowledgements(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload.get("input_id"),
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
