"""Request existing lane-owner acknowledgement for AI Resources triage items."""

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


SCHEMA_VERSION = "ai_resources_owner_acknowledgement_requests.v1"
DEFAULT_JSON = REPORTS_DIR / "ai-resources-owner-acknowledgement-requests-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ai-resources-owner-acknowledgement-requests-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _acknowledgement_requests(triage: dict[str, Any]) -> list[dict[str, Any]]:
    input_id = triage.get("input_id") or "all"
    requests = []
    for item in triage.get("triage_items", []):
        lane_id = item.get("lane_id")
        if item.get("decision") != "reuse_existing_owner" or not lane_id:
            continue
        lane_fragment = safe_id_fragment(str(lane_id), 70)
        requests.append(
            {
                "task_id": f"task-{input_id}-owner-acknowledgement-{lane_fragment}",
                "lane_id": lane_id,
                "owner_agent_id": item.get("owner_agent_id"),
                "status": "new",
                "priority": 90,
                "duplicate_key": f"{input_id}:owner-acknowledgement:{lane_id}",
                "source_followup_task_id": item.get("task_id"),
                "source_followup_status": item.get("task_status"),
                "triage_decision": item.get("decision"),
                "recommended_action": "Acknowledge the customer follow-up locally: accept the existing task, park it with a revisit condition, or request a CEO decision-batch item.",
                "next_action": "Write one local acknowledgement artifact before starting workers or creating overlapping agents.",
            }
        )
    return requests


def _counts(triage_items: list[dict[str, Any]], requests: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "owner_acknowledgement_requested": len(requests),
        "skipped": max(0, len(triage_items) - len(requests)),
        "total": len(triage_items),
    }


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# AI Resources Owner Acknowledgement Requests V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Input id: `{payload.get('input_id') or 'all'}`",
        f"Triage report: `{payload['triage_report_path']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Summary",
        "",
        payload["summary"],
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
            "## Acknowledgement Requests",
            "",
            "| Lane | Owner | Ack Task | Source Follow-Up | Next Action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["acknowledgement_requests"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.get('lane_id')}`",
                    md_cell(item.get("owner_agent_id"), 110),
                    f"`{item.get('task_id')}`",
                    f"`{item.get('source_followup_task_id')}`",
                    md_cell(item.get("next_action"), 260),
                ]
            )
            + " |"
        )
    if not payload["acknowledgement_requests"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet creates local acknowledgement requests only. It does not mutate source follow-up tasks, start workers, create agents, open browsers, create accounts, publish, submit, trade, spend, call APIs, approve service requests, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _existing_status(conn: sqlite3.Connection, task_id: str, duplicate_key: str) -> str | None:
    row = conn.execute(
        "SELECT status FROM tasks WHERE task_id = ? OR duplicate_key = ? ORDER BY created_at DESC LIMIT 1",
        (task_id, duplicate_key),
    ).fetchone()
    return row["status"] if row else None


def _upsert_ack_task(conn: sqlite3.Connection, request: dict[str, Any], md_path: Path, ts: str) -> str:
    status = _existing_status(conn, request["task_id"], request["duplicate_key"]) or request["status"]
    existing = conn.execute(
        "SELECT task_id FROM tasks WHERE task_id = ? OR duplicate_key = ? ORDER BY created_at DESC LIMIT 1",
        (request["task_id"], request["duplicate_key"]),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE tasks
            SET lane_id = ?,
                title = ?,
                status = ?,
                priority = ?,
                owner_agent_id = COALESCE(owner_agent_id, ?),
                duplicate_key = ?,
                evidence_required = ?,
                next_action = ?,
                updated_at = ?
            WHERE task_id = ? OR duplicate_key = ?
            """,
            (
                request["lane_id"],
                f"Acknowledge customer follow-up triage for {request['lane_id']}",
                status,
                request["priority"],
                request.get("owner_agent_id"),
                request["duplicate_key"],
                str(md_path),
                request["next_action"],
                ts,
                request["task_id"],
                request["duplicate_key"],
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request["task_id"],
                request["lane_id"],
                f"Acknowledge customer follow-up triage for {request['lane_id']}",
                status,
                request["priority"],
                request.get("owner_agent_id"),
                request["duplicate_key"],
                str(md_path),
                request["next_action"],
                ts,
                ts,
            ),
        )
    return status


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    input_fragment = safe_id_fragment(payload.get("input_id") or "all", 90)
    command_task_id = f"task-ai-resources-owner-acknowledgement-requests-v1-{input_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, ?, 'complete', 90, ?, ?, ?, ?, ?, ?, ?, ?)
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
            command_task_id,
            AI_RESOURCES_LANE,
            f"Request lane-owner acknowledgements for {payload.get('input_id') or 'all'}",
            AI_RESOURCES_OWNER,
            f"{payload.get('input_id') or 'all'}:owner-acknowledgement-requests",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for request in payload["acknowledgement_requests"]:
        request["status"] = _upsert_ack_task(conn, request, md_path, ts)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    for artifact_id, kind, path, notes in [
        (f"artifact-ai-resources-owner-acknowledgement-requests-json-{input_fragment}", "ai_resources_owner_acknowledgement_requests_json", json_path, "Machine-readable AI Resources owner acknowledgement request packet."),
        (f"artifact-ai-resources-owner-acknowledgement-requests-md-{input_fragment}", "ai_resources_owner_acknowledgement_requests", md_path, "Human-readable AI Resources owner acknowledgement request packet."),
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
            (artifact_id, AI_RESOURCES_LANE, command_task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": payload.get("input_id"),
        "counts": payload["counts"],
        "acknowledgement_task_ids": [item["task_id"] for item in payload["acknowledgement_requests"]],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ai_resources_owner_acknowledgement_requests_written', ?, ?, ?, ?, ?, ?)
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
            f"trace-event-ai-resources-owner-acknowledgement-requests-{input_fragment}",
            f"trace-ai-resources-owner-acknowledgement-requests-{input_fragment}",
            AI_RESOURCES_LANE,
            command_task_id,
            AI_RESOURCES_OWNER,
            ts,
            "ai_resources_owner_acknowledgement_requests_v1",
            f"Wrote {len(payload['acknowledgement_requests'])} owner acknowledgement requests for customer follow-up triage.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'ai_resources_owner_acknowledgement_requests', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-ai-resources-owner-acknowledgement-requests-{input_fragment}",
            AI_RESOURCES_LANE,
            command_task_id,
            payload["status"],
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def request_ai_resources_owner_acknowledgements(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    triage_path = Path(args.triage_report)
    triage = _load_json(triage_path)
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    triage_items = triage.get("triage_items", [])
    requests = _acknowledgement_requests(triage)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "acknowledgement_requests_ready" if requests else "no_acknowledgement_requests_needed",
        "input_id": triage.get("input_id"),
        "triage_report_path": str(triage_path),
        "summary": (
            f"Prepared {len(requests)} lane-owner acknowledgement requests from AI Resources triage."
            if requests
            else f"Triage report `{triage_path}` has no reuse-existing-owner items."
        ),
        "counts": _counts(triage_items, requests),
        "acknowledgement_requests": requests,
        "next_action": (
            "Lane owners should acknowledge each request with one local artifact or park/escalate with a concrete revisit condition."
            if requests
            else "No owner acknowledgement requests needed; continue monitoring triage outcomes."
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


def write_ai_resources_owner_acknowledgement_requests(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = request_ai_resources_owner_acknowledgements(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "input_id": payload.get("input_id"),
                "counts": payload["counts"],
                "acknowledgement_task_ids": [item["task_id"] for item in payload["acknowledgement_requests"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
