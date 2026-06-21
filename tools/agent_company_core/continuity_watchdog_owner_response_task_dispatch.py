"""Turn local owner response artifacts into concrete local task dispatches."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .continuity_watchdog_owner_response_artifacts import DEFAULT_JSON as DEFAULT_OWNER_RESPONSE_ARTIFACTS_JSON
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_watchdog_owner_response_task_dispatch.v1"
DEFAULT_JSON = REPORTS_DIR / "continuity-watchdog-owner-response-task-dispatch-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "continuity-watchdog-owner-response-task-dispatch-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
WATCHDOG_AGENT = "continuity-watchdog-worker-20260621"
TASK_ID = "task-continuity-watchdog-owner-response-task-dispatch-v1-20260621"
RESPONSE_TYPES = [
    "owner_selection_or_park_required",
    "acknowledgement_response_required",
    "lane_goal_response_required",
    "manual_review_required",
]
TERMINAL_STATUSES = {"complete", "cancelled"}


def _target_id(artifact: dict[str, Any]) -> str:
    response_type = str(artifact.get("response_type") or "manual_review_required")
    if response_type == "acknowledgement_response_required":
        return str(artifact.get("source_task_id") or artifact.get("target_id") or artifact["owner_response_artifact_id"])
    return str(artifact.get("lane_id") or artifact.get("target_id") or artifact["owner_response_artifact_id"])


def _duplicate_key(artifact: dict[str, Any]) -> str:
    response_type = str(artifact.get("response_type") or "manual_review_required")
    return f"continuity-owner-response-task:{response_type}:{_target_id(artifact)}"


def _task_lane_id(artifact: dict[str, Any]) -> str:
    response_type = str(artifact.get("response_type") or "manual_review_required")
    if response_type in {"owner_selection_or_park_required", "manual_review_required"}:
        return AI_RESOURCES_LANE
    return str(artifact.get("lane_id") or AI_RESOURCES_LANE)


def _task_owner_agent_id(artifact: dict[str, Any]) -> str:
    response_type = str(artifact.get("response_type") or "manual_review_required")
    if response_type in {"owner_selection_or_park_required", "manual_review_required"}:
        return AI_RESOURCES_OWNER
    return str(artifact.get("owner_agent_id") or artifact.get("recommended_owner_agent_id") or WATCHDOG_AGENT)


def _priority(response_type: str) -> int:
    if response_type == "owner_selection_or_park_required":
        return 96
    if response_type == "acknowledgement_response_required":
        return 92
    if response_type == "lane_goal_response_required":
        return 86
    return 80


def _title(artifact: dict[str, Any]) -> str:
    response_type = str(artifact.get("response_type") or "manual_review_required")
    target = _target_id(artifact)
    if response_type == "owner_selection_or_park_required":
        return f"Decide continuity owner response for {target}"
    if response_type == "acknowledgement_response_required":
        return f"Handle continuity owner acknowledgement response for {target}"
    if response_type == "lane_goal_response_required":
        return f"Submit continuity lane goal response for {target}"
    return f"Review continuity owner response for {target}"


def _task_id_for_duplicate_key(duplicate_key: str) -> str:
    return f"task-{safe_id_fragment(duplicate_key, 170)}"


def _dispatch_item(artifact: dict[str, Any]) -> dict[str, Any]:
    response_type = str(artifact.get("response_type") or "manual_review_required")
    if response_type not in RESPONSE_TYPES:
        response_type = "manual_review_required"
    duplicate_key = _duplicate_key({**artifact, "response_type": response_type})
    task_id = _task_id_for_duplicate_key(duplicate_key)
    evidence = artifact.get("artifact_md_path") or artifact.get("evidence_artifact_path") or artifact.get(
        "goal_artifact_path_or_revisit_condition"
    )
    next_action = str(artifact.get("next_action") or "Work this continuity owner response locally and report evidence.")
    return {
        "dispatch_task_id": task_id,
        "response_type": response_type,
        "selected_response_option": artifact.get("selected_response_option"),
        "source_owner_response_artifact_id": artifact.get("owner_response_artifact_id"),
        "target_type": artifact.get("target_type"),
        "target_id": artifact.get("target_id"),
        "source_task_id": artifact.get("source_task_id"),
        "source_lane_id": artifact.get("lane_id"),
        "task_lane_id": _task_lane_id({**artifact, "response_type": response_type}),
        "task_owner_agent_id": _task_owner_agent_id({**artifact, "response_type": response_type}),
        "status": "new",
        "priority": _priority(response_type),
        "title": _title({**artifact, "response_type": response_type}),
        "duplicate_key": duplicate_key,
        "evidence_required": str(evidence or ""),
        "next_action": next_action,
        "source_state_mutated": False,
        "external_side_effects": False,
    }


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"dispatch_tasks": len(items)}
    for response_type in RESPONSE_TYPES:
        counts[response_type] = 0
    for item in items:
        counts[item["response_type"]] = counts.get(item["response_type"], 0) + 1
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Watchdog Owner Response Task Dispatch V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Owner response artifacts: `{payload['source_owner_response_artifacts_path']}`",
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
            "## Dispatch Tasks",
            "",
            "| Response Type | Task Lane | Owner | Duplicate Key | Evidence | Next Action |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["dispatch_tasks"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['response_type']}`",
                    f"`{item['task_lane_id']}`",
                    md_cell(item.get("task_owner_agent_id"), 140),
                    md_cell(item["duplicate_key"], 180),
                    md_cell(item.get("evidence_required"), 160),
                    md_cell(item.get("next_action"), 260),
                ]
            )
            + " |"
        )
    if not payload["dispatch_tasks"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This command writes local task rows, local reports, and audit rows only. It does not mutate source owner response artifacts, source acknowledgement tasks, source lanes, owner assignments, service requests, worker queues, browser state, accounts, public surfaces, payments, trades, submissions, APIs, or external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _existing_task_id(conn: sqlite3.Connection, task_id: str, duplicate_key: str) -> str | None:
    row = conn.execute(
        """
        SELECT task_id
        FROM tasks
        WHERE task_id = ? OR duplicate_key = ?
        ORDER BY CASE WHEN task_id = ? THEN 0 ELSE 1 END
        LIMIT 1
        """,
        (task_id, duplicate_key, task_id),
    ).fetchone()
    return str(row["task_id"]) if row else None


def _upsert_dispatch_task(conn: sqlite3.Connection, item: dict[str, Any], ts: str) -> None:
    existing_task_id = _existing_task_id(conn, item["dispatch_task_id"], item["duplicate_key"])
    if existing_task_id:
        existing = conn.execute("SELECT status FROM tasks WHERE task_id = ?", (existing_task_id,)).fetchone()
        status = existing["status"] if existing and existing["status"] in TERMINAL_STATUSES else item["status"]
        conn.execute(
            """
            UPDATE tasks
            SET lane_id = ?,
                title = ?,
                status = ?,
                priority = ?,
                owner_agent_id = ?,
                duplicate_key = ?,
                evidence_required = ?,
                next_action = ?,
                updated_at = ?
            WHERE task_id = ?
            """,
            (
                item["task_lane_id"],
                item["title"],
                status,
                item["priority"],
                item["task_owner_agent_id"],
                item["duplicate_key"],
                item["evidence_required"],
                item["next_action"],
                ts,
                existing_task_id,
            ),
        )
        item["dispatch_task_id"] = existing_task_id
        item["status"] = status
        return
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item["dispatch_task_id"],
            item["task_lane_id"],
            item["title"],
            item["status"],
            item["priority"],
            item["task_owner_agent_id"],
            item["duplicate_key"],
            item["evidence_required"],
            item["next_action"],
            ts,
            ts,
        ),
    )


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    for item in payload["dispatch_tasks"]:
        _upsert_dispatch_task(conn, item, ts)
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write continuity watchdog owner response task dispatch v1', 'complete', 97, ?, 'continuity-watchdog-owner-response-task-dispatch:v1', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            TASK_ID,
            AI_RESOURCES_LANE,
            WATCHDOG_AGENT,
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
            "artifact-continuity-watchdog-owner-response-task-dispatch-v1-json-20260621",
            "continuity_watchdog_owner_response_task_dispatch_json",
            json_path,
            "Machine-readable continuity owner response task dispatch.",
        ),
        (
            "artifact-continuity-watchdog-owner-response-task-dispatch-v1-md-20260621",
            "continuity_watchdog_owner_response_task_dispatch_markdown",
            md_path,
            "Human-readable continuity owner response task dispatch.",
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
            (artifact_id, AI_RESOURCES_LANE, TASK_ID, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "counts": payload["counts"],
        "dispatch_task_ids": [item["dispatch_task_id"] for item in payload["dispatch_tasks"]],
        "source_owner_response_artifacts_path": payload["source_owner_response_artifacts_path"],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_watchdog_owner_response_task_dispatch_written', ?, ?, ?, ?, ?, ?)
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
            "trace-event-continuity-watchdog-owner-response-task-dispatch-v1-20260621",
            "trace-continuity-watchdog-owner-response-task-dispatch-v1-20260621",
            AI_RESOURCES_LANE,
            TASK_ID,
            WATCHDOG_AGENT,
            ts,
            "continuity_watchdog_owner_response_task_dispatch_v1",
            f"Wrote {payload['counts']['dispatch_tasks']} continuity owner response dispatch tasks.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-continuity-watchdog-owner-response-task-dispatch-v1-20260621', ?, ?, 'continuity_watchdog_owner_response_task_dispatch', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, payload["status"], str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_continuity_watchdog_owner_response_task_dispatch(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    owner_response_artifacts_path = Path(
        getattr(args, "owner_response_artifacts", None) or DEFAULT_OWNER_RESPONSE_ARTIFACTS_JSON
    )
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    owner_response_artifacts = load_json(owner_response_artifacts_path)
    items = [
        _dispatch_item(artifact)
        for artifact in owner_response_artifacts.get("owner_response_artifacts") or []
        if artifact.get("source_state_mutated") is False
    ]
    counts = _counts(items)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "dispatch_tasks_ready" if items else "no_dispatch_tasks_needed",
        "source_owner_response_artifacts_path": str(owner_response_artifacts_path),
        "source_owner_response_artifacts_generated_utc": owner_response_artifacts.get("generated_utc"),
        "source_owner_response_artifacts_status": owner_response_artifacts.get("status"),
        "counts": counts,
        "dispatch_tasks": items,
        "next_action": (
            "Work the created local dispatch tasks through existing owners and CEO/AI Resources review; source tasks and lanes remain unchanged."
            if items
            else "No owner response dispatch tasks required; continue continuity watchdog cadence."
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


def write_continuity_watchdog_owner_response_task_dispatch_cli(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> None:
    payload = write_continuity_watchdog_owner_response_task_dispatch(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "dispatch_task_ids": [item["dispatch_task_id"] for item in payload["dispatch_tasks"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
