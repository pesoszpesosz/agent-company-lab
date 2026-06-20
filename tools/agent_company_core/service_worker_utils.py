from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Shared DB and report helpers for service-worker workflows."""



def load_report_json_or_error(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON in {path}: {exc}"]
    if not isinstance(payload, dict):
        return None, [f"JSON root is not an object in {path}"]
    return payload, []


def check_expected_values(
    payload: dict[str, Any] | None,
    expected: dict[str, Any],
    prefix: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    failures: list[str] = []
    if payload is None:
        for key, expected_value in expected.items():
            failure = f"{prefix}.{key} unavailable because validation file could not be loaded"
            failures.append(failure)
            checks.append(
                {
                    "key": key,
                    "expected": expected_value,
                    "actual": None,
                    "passed": False,
                    "failure": failure,
                }
            )
        return checks, failures
    for key, expected_value in expected.items():
        actual = payload.get(key)
        passed = actual == expected_value
        failure = None if passed else f"{prefix}.{key} expected {expected_value!r}, got {actual!r}"
        if failure:
            failures.append(failure)
        checks.append(
            {
                "key": key,
                "expected": expected_value,
                "actual": actual,
                "passed": passed,
                "failure": failure,
            }
        )
    return checks, failures


def db_scalar(conn: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> Any:
    row = conn.execute(query, params).fetchone()
    return row[0] if row else None



def service_worker_chain_db_snapshot(conn: sqlite3.Connection) -> dict[str, Any]:
    service_status_counts = {
        row["status"]: row["count"]
        for row in conn.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM service_requests
            GROUP BY status
            ORDER BY status
            """
        )
    }
    assigned_rows = [
        {
            "request_id": row["request_id"],
            "status": row["status"],
            "assigned_agent_id": row["assigned_agent_id"],
            "updated_at": row["updated_at"],
        }
        for row in conn.execute(
            """
            SELECT request_id, status, assigned_agent_id, updated_at
            FROM service_requests
            WHERE assigned_agent_id IS NOT NULL
            ORDER BY request_id
            """
        )
    ]
    tasks_total = int(db_scalar(conn, "SELECT COUNT(*) FROM tasks") or 0)
    tasks_complete = int(db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE status = 'complete'") or 0)
    open_task_rows = [
        {
            "task_id": row["task_id"],
            "lane_id": row["lane_id"],
            "status": row["status"],
            "priority": row["priority"],
            "evidence_required": row["evidence_required"],
        }
        for row in conn.execute(
            """
            SELECT task_id, lane_id, status, priority, evidence_required
            FROM tasks
            WHERE status != 'complete'
            ORDER BY priority DESC, created_at DESC, task_id
            """
        )
    ]
    open_tasks_started_or_leased = int(
        db_scalar(
            conn,
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE status != 'complete'
              AND (lease_owner_agent_id IS NOT NULL OR started_at IS NOT NULL)
            """,
        )
        or 0
    )
    open_tasks_missing_evidence_required = int(
        db_scalar(
            conn,
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE status != 'complete'
              AND (evidence_required IS NULL OR TRIM(evidence_required) = '')
            """,
        )
        or 0
    )
    return {
        "tasks_total": tasks_total,
        "tasks_complete": tasks_complete,
        "tasks_open": tasks_total - tasks_complete,
        "open_tasks": open_task_rows,
        "open_tasks_started_or_leased": open_tasks_started_or_leased,
        "open_tasks_missing_evidence_required": open_tasks_missing_evidence_required,
        "artifacts_total": int(db_scalar(conn, "SELECT COUNT(*) FROM artifacts") or 0),
        "trace_events_total": int(db_scalar(conn, "SELECT COUNT(*) FROM trace_events") or 0),
        "agents_total": int(db_scalar(conn, "SELECT COUNT(*) FROM agents") or 0),
        "service_requests_total": int(db_scalar(conn, "SELECT COUNT(*) FROM service_requests") or 0),
        "service_status_counts": dict(sorted(service_status_counts.items())),
        "assigned_service_requests": assigned_rows,
    }
