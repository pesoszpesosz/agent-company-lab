"""Dispatch stale AI Resources owner acknowledgements to existing lane owners."""

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


SCHEMA_VERSION = "ai_resources_owner_acknowledgement_dispatch.v1"
DEFAULT_JSON = REPORTS_DIR / "ai-resources-owner-acknowledgement-dispatch-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ai-resources-owner-acknowledgement-dispatch-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
TERMINAL_STATUSES = {"complete", "cancelled"}
BLOCKED_STATUSES = {"blocked", "needs_review"}
RESPONSE_OPTIONS = [
    "acknowledge_and_start_local_work",
    "park_with_revisit_condition",
    "request_ceo_decision_batch_item",
]


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
            ORDER BY priority DESC, updated_at, lane_id
            """,
            (f"{input_id}:owner-acknowledgement:%",),
        )
    return (
        """
        SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
               evidence_required, next_action, created_at, updated_at, started_at, completed_at
        FROM tasks
        WHERE duplicate_key LIKE ?
        ORDER BY updated_at, priority DESC, lane_id
        """,
        ("%:owner-acknowledgement:%",),
    )


def _dispatch_needed(row: sqlite3.Row, age_minutes: int | None, stale_after_minutes: int) -> bool:
    if row["status"] in TERMINAL_STATUSES:
        return False
    if row["status"] in BLOCKED_STATUSES:
        return True
    return age_minutes is not None and age_minutes >= stale_after_minutes


def _response_contract() -> dict[str, Any]:
    return {
        "allowed_responses": RESPONSE_OPTIONS,
        "required_fields": [
            "selected_response_option",
            "lane_id",
            "source_task_id",
            "owner_agent_id",
            "evidence_artifact_path",
            "next_revisit_condition_or_ceo_decision_needed",
        ],
        "prohibited_actions": [
            "create_duplicate_agent",
            "start_unrequested_worker",
            "mutate_source_acknowledgement_task",
            "publish_submit_trade_spend_or_call_external_api",
        ],
    }


def _dispatch_item(row: sqlite3.Row, age: int | None, stale_after_minutes: int, dispatch_id: str) -> dict[str, Any]:
    lane_fragment = safe_id_fragment(row["lane_id"], 80)
    return {
        "dispatch_item_id": f"{dispatch_id}-{lane_fragment}",
        "lane_id": row["lane_id"],
        "existing_owner_agent_id": row["owner_agent_id"],
        "source_task_id": row["task_id"],
        "source_duplicate_key": row["duplicate_key"],
        "source_title": row["title"],
        "source_status": row["status"],
        "priority": row["priority"],
        "age_minutes": age,
        "stale_after_minutes": stale_after_minutes,
        "response_options": RESPONSE_OPTIONS,
        "response_contract": _response_contract(),
        "next_action": "Send this response contract to the existing lane owner; do not create a duplicate agent.",
    }


def _collect(
    conn: sqlite3.Connection,
    input_id: str | None,
    generated_utc: str,
    stale_after_minutes: int,
    dispatch_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    sql, params = _query(input_id)
    rows = conn.execute(sql, params).fetchall()
    dispatch_items: list[dict[str, Any]] = []
    fresh_open: list[dict[str, Any]] = []
    terminal: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row, generated_utc)
        summary = {
            "lane_id": row["lane_id"],
            "source_task_id": row["task_id"],
            "source_status": row["status"],
            "existing_owner_agent_id": row["owner_agent_id"],
            "source_duplicate_key": row["duplicate_key"],
            "age_minutes": age,
        }
        if row["status"] in TERMINAL_STATUSES:
            terminal.append(summary)
        elif _dispatch_needed(row, age, stale_after_minutes):
            dispatch_items.append(_dispatch_item(row, age, stale_after_minutes, dispatch_id))
        else:
            fresh_open.append(summary)
    return dispatch_items, fresh_open, terminal


def _counts(dispatch_items: list[dict[str, Any]], fresh_open: list[dict[str, Any]], terminal: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "dispatch_items": len(dispatch_items),
        "fresh_open_acknowledgements": len(fresh_open),
        "terminal_acknowledgements": len(terminal),
        "total_owner_acknowledgements": len(dispatch_items) + len(fresh_open) + len(terminal),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# AI Resources Owner Acknowledgement Dispatch V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Dispatch id: `{payload['dispatch_id']}`",
        f"Input filter: `{payload.get('input_id') or 'all'}`",
        f"Stale after minutes: `{payload['stale_after_minutes']}`",
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
            "## Dispatch Items",
            "",
            "| Lane | Existing Owner | Source Task | Status | Age Min | Response Options | Next Action |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for item in payload["dispatch_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    md_cell(item.get("existing_owner_agent_id"), 120),
                    f"`{item['source_task_id']}`",
                    md_cell(item.get("source_status"), 60),
                    str(item["age_minutes"] if item["age_minutes"] is not None else ""),
                    md_cell(", ".join(item["response_options"]), 190),
                    md_cell(item.get("next_action"), 220),
                ]
            )
            + " |"
        )
    if not payload["dispatch_items"]:
        lines.append("| none |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Response Contract",
            "",
            "Lane owners must choose exactly one response option:",
        ]
    )
    for option in RESPONSE_OPTIONS:
        lines.append(f"- `{option}`")
    lines.extend(
        [
            "",
            "Each response must include lane id, source task id, owner id, evidence artifact path, and either a concrete revisit condition or the requested CEO decision-batch item.",
            "",
            "## Boundary",
            "",
            "This dispatch writes local reports and audit rows only. It does not mutate acknowledgement tasks, mutate source follow-ups, start workers, create agents, open browsers, create accounts, publish, submit, trade, spend, call APIs, approve service requests, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    task_id = f"task-ai-resources-owner-acknowledgement-dispatch-v1-{input_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, ?, 'complete', 88, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"Dispatch stale owner acknowledgements for {payload.get('input_id') or 'all'}",
            AI_RESOURCES_OWNER,
            f"{payload.get('input_id') or 'all'}:owner-acknowledgement-dispatch",
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
            f"artifact-ai-resources-owner-acknowledgement-dispatch-json-{input_fragment}",
            "ai_resources_owner_acknowledgement_dispatch_json",
            json_path,
            "Machine-readable owner acknowledgement dispatch packet.",
        ),
        (
            f"artifact-ai-resources-owner-acknowledgement-dispatch-md-{input_fragment}",
            "ai_resources_owner_acknowledgement_dispatch",
            md_path,
            "Human-readable owner acknowledgement dispatch packet.",
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
              notes=excluded.notes
            """,
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": payload.get("input_id"),
        "counts": payload["counts"],
        "dispatch_item_ids": [item["dispatch_item_id"] for item in payload["dispatch_items"]],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ai_resources_owner_acknowledgement_dispatch_written', ?, ?, ?, ?, ?, ?)
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
            f"trace-event-ai-resources-owner-acknowledgement-dispatch-{input_fragment}",
            f"trace-ai-resources-owner-acknowledgement-dispatch-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            AI_RESOURCES_OWNER,
            ts,
            "ai_resources_owner_acknowledgement_dispatch_v1",
            f"Wrote {payload['counts']['dispatch_items']} existing-owner dispatch items for stale acknowledgements.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'ai_resources_owner_acknowledgement_dispatch', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-ai-resources-owner-acknowledgement-dispatch-{input_fragment}",
            AI_RESOURCES_LANE,
            task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def dispatch_ai_resources_owner_acknowledgements(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    input_id = getattr(args, "input_id", None)
    stale_after = int(getattr(args, "stale_after_minutes", 60))
    input_fragment = safe_id_fragment(input_id or "all", 90)
    dispatch_id = f"ai-resources-owner-acknowledgement-dispatch-v1-{input_fragment}"
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    dispatch_items, fresh_open, terminal = _collect(conn, input_id, generated, stale_after, dispatch_id)
    counts = _counts(dispatch_items, fresh_open, terminal)
    status = "dispatch_ready" if dispatch_items else "no_dispatch_needed"
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "dispatch_id": dispatch_id,
        "input_id": input_id,
        "stale_after_minutes": stale_after,
        "counts": counts,
        "dispatch_items": dispatch_items,
        "fresh_open_acknowledgements": fresh_open,
        "terminal_acknowledgements": terminal,
        "next_action": (
            "Route each dispatch item to the existing lane owner with the response contract; consolidate unresolved items into the next CEO decision batch."
            if dispatch_items
            else "No stale owner acknowledgements require dispatch; continue monitoring."
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


def write_ai_resources_owner_acknowledgement_dispatch(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = dispatch_ai_resources_owner_acknowledgements(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload.get("input_id"),
                "counts": payload["counts"],
                "dispatch_item_ids": [item["dispatch_item_id"] for item in payload["dispatch_items"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
