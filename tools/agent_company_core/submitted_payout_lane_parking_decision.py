"""Park the submitted payout lane as external-owned/read-only."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "submitted_payout_lane_parking_decision.v1"
LANE_ID = "submitted_bounty_payouts"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
TASK_ID = "task-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621"
TRACE_ID = "trace-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621"
DEFAULT_JSON = REPORTS_DIR / "submitted-bounty-payouts-external-owned-parking-decision-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "submitted-bounty-payouts-external-owned-parking-decision-v1-20260621.md"
PARKED_STATUS = "external_owned_readonly"
EXTERNAL_OWNER_REF = "external:parallel-payout-worker"
REVISIT_CONDITION = (
    "Reopen only if the user explicitly reassigns payout monitoring into this lab, supplies the live parallel "
    "worker thread id, or asks AR to replace the external payout worker."
)
SOURCE_TASK_IDS = [
    "task-continuity-owner-response-task-owner_selection_or_park_required-submitted_bounty_payouts",
    "task-continuity-owner-response-task-lane_goal_response_required-submitted_bounty_payouts",
]


def _row(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
    row = conn.execute(sql, params).fetchone()
    return dict(row) if row else None


def _load_lane(conn: sqlite3.Connection) -> dict[str, Any]:
    lane = _row(conn, "SELECT * FROM lanes WHERE lane_id = ?", (LANE_ID,))
    if not lane:
        raise RuntimeError(f"Lane not found: {LANE_ID}")
    return lane


def _continuity_tasks(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT task_id, status, owner_agent_id, duplicate_key, evidence_required, next_action
        FROM tasks
        WHERE task_id IN ({})
        ORDER BY task_id
        """.format(",".join("?" for _ in SOURCE_TASK_IDS)),
        tuple(SOURCE_TASK_IDS),
    ).fetchall()
    return [dict(row) for row in rows]


def _payload(conn: sqlite3.Connection, generated_utc: str, json_path: Path, md_path: Path) -> dict[str, Any]:
    lane_before = _load_lane(conn)
    tasks_before = _continuity_tasks(conn)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated_utc,
        "status": "parking_decision_ready",
        "lane_id": LANE_ID,
        "decision": "park_as_external_owned_readonly",
        "previous_lane_state": {
            "status": lane_before.get("status"),
            "owner_agent_id": lane_before.get("owner_agent_id"),
            "owner_thread_id": lane_before.get("owner_thread_id"),
            "notes": lane_before.get("notes"),
        },
        "new_lane_state": {
            "status": PARKED_STATUS,
            "owner_agent_id": None,
            "owner_thread_id": EXTERNAL_OWNER_REF,
            "notes": (
                "External-owned/read-only in this lab. Parallel Find profitable edge worker owns "
                "GitHub/RustChain/Charles payout monitoring; do not duplicate monitoring or public follow-up here."
            ),
        },
        "completed_continuity_tasks": [task["task_id"] for task in tasks_before],
        "revisit_condition": REVISIT_CONDITION,
        "rationale": [
            "README and manager packets repeatedly state that submitted_bounty_payouts is imported for visibility only.",
            "No live Codex thread was found for a local submitted-payout worker in this lab.",
            "Creating a new payout owner would duplicate the external payout worker and violate the overlap boundary.",
            "Parking removes a false ownerless-active-lane alarm while preserving local evidence visibility.",
        ],
        "next_action": REVISIT_CONDITION,
        "source_state_mutation": {
            "lane_status_updated": True,
            "lane_owner_assigned": False,
            "continuity_tasks_completed": len(tasks_before),
            "duplicate_worker_created": False,
        },
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Submitted Bounty Payouts External-Owned Parking Decision V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Lane: `{payload['lane_id']}`",
        f"Decision: `{payload['decision']}`",
        f"New status: `{payload['new_lane_state']['status']}`",
        f"External owner reference: `{payload['new_lane_state']['owner_thread_id']}`",
        "",
        "## Rationale",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["rationale"])
    lines.extend(
        [
            "",
            "## Completed Continuity Tasks",
            "",
            "| Task |",
            "| --- |",
        ]
    )
    for task_id in payload["completed_continuity_tasks"]:
        lines.append(f"| {md_cell(task_id, 180)} |")
    if not payload["completed_continuity_tasks"]:
        lines.append("| none found |")
    lines.extend(
        [
            "",
            "## Revisit Condition",
            "",
            payload["revisit_condition"],
            "",
            "## Boundary",
            "",
            "This decision mutates only local control-plane lane/task status. It does not create a worker, start a thread, monitor GitHub/RustChain/Charles, post public messages, submit claims, create accounts, route payments, trade, spend, call APIs, or contact external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _apply_decision(conn: sqlite3.Connection, payload: dict[str, Any], md_path: Path, ts: str) -> None:
    lane_state = payload["new_lane_state"]
    conn.execute(
        """
        UPDATE lanes
        SET status = ?,
            owner_agent_id = NULL,
            owner_thread_id = ?,
            notes = ?,
            updated_at = ?
        WHERE lane_id = ?
        """,
        (lane_state["status"], lane_state["owner_thread_id"], lane_state["notes"], ts, LANE_ID),
    )
    for task_id in SOURCE_TASK_IDS:
        conn.execute(
            """
            UPDATE tasks
            SET status = 'complete',
                owner_agent_id = ?,
                evidence_required = ?,
                next_action = ?,
                updated_at = ?,
                completed_at = ?
            WHERE task_id = ?
            """,
            (AI_RESOURCES_OWNER, str(md_path), payload["next_action"], ts, ts, task_id),
        )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Park submitted payout lane as external-owned read-only', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            AI_RESOURCES_OWNER,
            "submitted-bounty-payouts-external-owned-parking-decision:v1",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )


def _record_audit(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    for artifact_id, kind, path, notes in [
        (
            "artifact-submitted-bounty-payouts-external-owned-parking-decision-v1-json-20260621",
            "submitted_payout_parking_decision_json",
            json_path,
            "Machine-readable submitted payout external-owned parking decision.",
        ),
        (
            "artifact-submitted-bounty-payouts-external-owned-parking-decision-v1-md-20260621",
            "submitted_payout_parking_decision_markdown",
            md_path,
            "Human-readable submitted payout external-owned parking decision.",
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
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'submitted_payout_lane_parked_external_readonly', ?, ?, ?, ?, ?, ?)
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
            "trace-event-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621",
            TRACE_ID,
            AI_RESOURCES_LANE,
            TASK_ID,
            AI_RESOURCES_OWNER,
            ts,
            "submitted_payout_lane_parking_decision_v1",
            "Parked submitted_bounty_payouts as external-owned/read-only to avoid duplicating the parallel payout worker.",
            json.dumps(
                {
                    "lane_id": LANE_ID,
                    "new_status": PARKED_STATUS,
                    "external_owner_ref": EXTERNAL_OWNER_REF,
                    "source_state_mutation": payload["source_state_mutation"],
                    "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
                },
                sort_keys=True,
            ),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621', ?, ?, 'lane_parking_decision', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, PARKED_STATUS, str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_submitted_payout_lane_parking_decision(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    payload = _payload(conn, generated, json_path, md_path)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _apply_decision(conn, payload, md_path, generated)
        _record_audit(conn, payload, json_path, md_path)
    return payload


def write_submitted_payout_lane_parking_decision_cli(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> None:
    payload = write_submitted_payout_lane_parking_decision(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "lane_id": payload["lane_id"],
                "decision": payload["decision"],
                "new_lane_state": payload["new_lane_state"],
                "completed_continuity_tasks": payload["completed_continuity_tasks"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
