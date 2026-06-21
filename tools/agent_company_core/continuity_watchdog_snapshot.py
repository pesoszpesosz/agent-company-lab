"""Continuity watchdog snapshot and local restore plan."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "continuity_watchdog_snapshot.v1"
DEFAULT_JSON = REPORTS_DIR / "continuity-watchdog-snapshot-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "continuity-watchdog-snapshot-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
WATCHDOG_AGENT = "continuity-watchdog-worker-20260621"
TASK_ID = "task-continuity-watchdog-snapshot-v1-20260621"
TERMINAL_STATUSES = {"complete", "cancelled"}


def _age_minutes(updated_at: str | None, generated_utc: str) -> int | None:
    if not updated_at:
        return None
    updated = parse_utc(updated_at)
    generated = parse_utc(generated_utc)
    if not updated or not generated:
        return None
    return max(0, int((generated - updated).total_seconds() // 60))


def _rows(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def _ownerless_active_lanes(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return _rows(
        conn,
        """
        SELECT lane_id, department, status, owner_agent_id, owner_thread_id, updated_at
        FROM lanes
        WHERE status = 'active' AND (owner_agent_id IS NULL OR owner_agent_id = '')
        ORDER BY lane_id
        """,
    )


def _missing_owner_agent_lanes(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return _rows(
        conn,
        """
        SELECT l.lane_id, l.department, l.owner_agent_id, l.owner_thread_id, l.updated_at
        FROM lanes l
        LEFT JOIN agents a ON a.agent_id = l.owner_agent_id
        WHERE l.status = 'active'
          AND l.owner_agent_id IS NOT NULL
          AND l.owner_agent_id != ''
          AND a.agent_id IS NULL
        ORDER BY l.lane_id
        """,
    )


def _agents_missing_threads(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return _rows(
        conn,
        """
        SELECT agent_id, role_id, department_id, status, updated_at
        FROM agents
        WHERE status = 'active' AND (thread_id IS NULL OR thread_id = '')
        ORDER BY agent_id
        """,
    )


def _stale_open_tasks(conn: sqlite3.Connection, generated_utc: str, stale_after_minutes: int) -> list[dict[str, Any]]:
    rows = _rows(
        conn,
        """
        SELECT task_id, lane_id, status, priority, owner_agent_id, duplicate_key, updated_at, next_action
        FROM tasks
        WHERE status NOT IN ('complete', 'cancelled')
        ORDER BY updated_at ASC, priority DESC, task_id
        """,
    )
    stale: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row.get("updated_at"), generated_utc)
        if age is not None and age >= stale_after_minutes:
            row["age_minutes"] = age
            stale.append(row)
    return stale


def _expired_leases(conn: sqlite3.Connection, generated_utc: str) -> list[dict[str, Any]]:
    return _rows(
        conn,
        """
        SELECT task_id, lane_id, status, owner_agent_id, lease_owner_agent_id, lease_expires_at
        FROM tasks
        WHERE status NOT IN ('complete', 'cancelled')
          AND lease_expires_at IS NOT NULL
          AND lease_expires_at < ?
        ORDER BY lease_expires_at ASC, task_id
        """,
        (generated_utc,),
    )


def _duplicate_active_keys(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return _rows(
        conn,
        """
        SELECT duplicate_key, COUNT(*) AS active_count,
               GROUP_CONCAT(task_id) AS task_ids,
               GROUP_CONCAT(owner_agent_id) AS owner_agent_ids
        FROM tasks
        WHERE status NOT IN ('complete', 'cancelled')
          AND duplicate_key IS NOT NULL
          AND duplicate_key != ''
        GROUP BY duplicate_key
        HAVING COUNT(*) > 1
        ORDER BY active_count DESC, duplicate_key
        """,
    )


def _lanes_without_open_tasks(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return _rows(
        conn,
        """
        SELECT l.lane_id, l.owner_agent_id, l.status
        FROM lanes l
        LEFT JOIN tasks t
          ON t.lane_id = l.lane_id
         AND t.status NOT IN ('complete', 'cancelled')
        WHERE l.status = 'active'
        GROUP BY l.lane_id
        HAVING COUNT(t.task_id) = 0
        ORDER BY l.lane_id
        """,
    )


def _stale_owner_acknowledgements(
    conn: sqlite3.Connection,
    generated_utc: str,
    stale_after_minutes: int,
) -> list[dict[str, Any]]:
    rows = _rows(
        conn,
        """
        SELECT task_id, lane_id, status, priority, owner_agent_id, duplicate_key, updated_at, next_action
        FROM tasks
        WHERE duplicate_key LIKE '%:owner-acknowledgement:%'
          AND status NOT IN ('complete', 'cancelled')
        ORDER BY updated_at ASC, priority DESC, task_id
        """,
    )
    stale: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row.get("updated_at"), generated_utc)
        if age is not None and age >= stale_after_minutes:
            row["age_minutes"] = age
            stale.append(row)
    return stale


def _restore_actions(findings: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for lane in findings["ownerless_active_lanes"]:
        actions.append(
            {
                "kind": "repair_ownerless_lane",
                "lane_id": lane["lane_id"],
                "next_action": "Route to AI Resources for owner selection or explicit park/retire decision.",
            }
        )
    for lane in findings["missing_owner_agent_lanes"]:
        actions.append(
            {
                "kind": "repair_missing_owner_agent",
                "lane_id": lane["lane_id"],
                "owner_agent_id": lane["owner_agent_id"],
                "next_action": "Register the missing owner agent or assign an existing non-overlapping owner.",
            }
        )
    for agent in findings["agents_missing_threads"]:
        actions.append(
            {
                "kind": "attach_agent_thread",
                "agent_id": agent["agent_id"],
                "next_action": "Attach a Codex thread id or mark the agent parked if no live thread exists.",
            }
        )
    for task in findings["expired_leases"]:
        actions.append(
            {
                "kind": "release_or_reclaim_expired_lease",
                "task_id": task["task_id"],
                "lane_id": task["lane_id"],
                "next_action": "Prepare local lease release or reclaim packet; do not mutate lease automatically.",
            }
        )
    for item in findings["duplicate_active_keys"]:
        actions.append(
            {
                "kind": "resolve_duplicate_active_key",
                "duplicate_key": item["duplicate_key"],
                "task_ids": item.get("task_ids"),
                "next_action": "Choose one primary owner and park or merge duplicate active tasks.",
            }
        )
    for task in findings["stale_owner_acknowledgements"]:
        actions.append(
            {
                "kind": "dispatch_stale_owner_acknowledgement",
                "task_id": task["task_id"],
                "lane_id": task["lane_id"],
                "next_action": "Use the owner-acknowledgement dispatch packet; do not create duplicate agents.",
            }
        )
    for lane in findings["lanes_without_open_tasks"]:
        actions.append(
            {
                "kind": "request_lane_goal",
                "lane_id": lane["lane_id"],
                "next_action": "Ask lane owner for one current goal artifact or explicit park/kill state.",
            }
        )
    return actions


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Watchdog Snapshot V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Cadence minutes: `{payload['cadence_minutes']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Counts",
        "",
        "| Finding | Count |",
        "| --- | ---: |",
    ]
    for key, value in payload["counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Restore Actions", "", "| Kind | Target | Next Action |", "| --- | --- | --- |"])
    for action in payload["restore_actions"]:
        target = action.get("task_id") or action.get("lane_id") or action.get("agent_id") or action.get("duplicate_key") or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{action['kind']}`",
                    md_cell(str(target), 120),
                    md_cell(action["next_action"], 240),
                ]
            )
            + " |"
        )
    if not payload["restore_actions"]:
        lines.append("| none |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This snapshot writes local reports and audit rows only. It does not mutate source tasks, assign owners, release leases, start workers, send thread messages, open browsers, create accounts, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write continuity watchdog snapshot v1', 'complete', 93, ?, 'continuity-watchdog-snapshot:v1', ?, ?, ?, ?, ?, ?)
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
        ("artifact-continuity-watchdog-snapshot-v1-json-20260621", "continuity_watchdog_snapshot_json", json_path, "Machine-readable continuity watchdog snapshot."),
        ("artifact-continuity-watchdog-snapshot-v1-md-20260621", "continuity_watchdog_snapshot_markdown", md_path, "Human-readable continuity watchdog snapshot."),
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
        "restore_action_count": len(payload["restore_actions"]),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_watchdog_snapshot_written', ?, ?, ?, ?, ?, ?)
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
            "trace-event-continuity-watchdog-snapshot-v1-20260621",
            "trace-continuity-watchdog-snapshot-v1-20260621",
            AI_RESOURCES_LANE,
            TASK_ID,
            WATCHDOG_AGENT,
            ts,
            "continuity_watchdog_snapshot_v1",
            f"Wrote continuity snapshot with {len(payload['restore_actions'])} restore actions.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-continuity-watchdog-snapshot-v1-20260621', ?, ?, 'continuity_watchdog_snapshot', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, payload["status"], str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_continuity_watchdog_snapshot_bundle(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    stale_after = int(getattr(args, "stale_after_minutes", 60))
    cadence = int(getattr(args, "cadence_minutes", 15))
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    findings = {
        "ownerless_active_lanes": _ownerless_active_lanes(conn),
        "missing_owner_agent_lanes": _missing_owner_agent_lanes(conn),
        "agents_missing_threads": _agents_missing_threads(conn),
        "stale_open_tasks": _stale_open_tasks(conn, generated, stale_after),
        "expired_leases": _expired_leases(conn, generated),
        "duplicate_active_keys": _duplicate_active_keys(conn),
        "lanes_without_open_tasks": _lanes_without_open_tasks(conn),
        "stale_owner_acknowledgements": _stale_owner_acknowledgements(conn, generated, stale_after),
    }
    restore_actions = _restore_actions(findings)
    counts = {key: len(value) for key, value in findings.items()}
    status = "restore_ready" if restore_actions else "clear"
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "cadence_minutes": cadence,
        "stale_after_minutes": stale_after,
        "counts": counts,
        "findings": findings,
        "restore_actions": restore_actions,
        "next_action": (
            "Route restore actions to AI Resources, existing lane owners, or CEO decision batch; do not mutate tasks automatically."
            if restore_actions
            else "No continuity restore action required; continue heartbeat cadence."
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


def write_continuity_watchdog_snapshot(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_continuity_watchdog_snapshot_bundle(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "restore_action_count": len(payload["restore_actions"]),
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
