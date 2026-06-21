"""Local account/session capacity dispatch planning."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "account_capacity_dispatch_plan.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
VALID_STATUSES = {"available", "cooling_down", "needs_restore", "retired_or_parked"}


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"account-capacity-dispatch-plan-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"account-capacity-dispatch-plan-v1-{day}.md")
    return json_path, md_path


def _load_sessions(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    if isinstance(payload, list):
        sessions = payload
    else:
        sessions = payload.get("sessions", [])
    return [_normalize_session(dict(session)) for session in sessions]


def _as_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(0, parsed)


def _normalize_session(session: dict[str, Any]) -> dict[str, Any]:
    session_id = str(session.get("session_id") or "").strip()
    if not session_id:
        raise SystemExit("Every capacity session requires session_id")
    status = str(session.get("status") or "needs_restore").strip()
    if status not in VALID_STATUSES:
        raise SystemExit(f"Invalid capacity status for {session_id}: {status}")
    concurrency_limit = _as_int(session.get("concurrency_limit"), 1)
    active_lease_count = _as_int(session.get("active_lease_count"), 0)
    return {
        "session_id": session_id,
        "surface": str(session.get("surface") or "unknown"),
        "account_label": session.get("account_label"),
        "status": status,
        "concurrency_limit": concurrency_limit,
        "active_lease_count": active_lease_count,
        "available_slots": max(0, concurrency_limit - active_lease_count) if status == "available" else 0,
        "resume_after_utc": session.get("resume_after_utc"),
        "last_refresh_utc": session.get("last_refresh_utc"),
        "last_error": session.get("last_error"),
        "notes": session.get("notes"),
    }


def _upsert_capacity_sessions(conn: sqlite3.Connection, sessions: list[dict[str, Any]], generated_utc: str) -> None:
    for session in sessions:
        conn.execute(
            """
            INSERT INTO account_capacity_sessions(
              session_id, surface, account_label, status, concurrency_limit,
              active_lease_count, resume_after_utc, last_refresh_utc, last_error,
              notes, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
              surface=excluded.surface,
              account_label=excluded.account_label,
              status=excluded.status,
              concurrency_limit=excluded.concurrency_limit,
              active_lease_count=excluded.active_lease_count,
              resume_after_utc=excluded.resume_after_utc,
              last_refresh_utc=excluded.last_refresh_utc,
              last_error=excluded.last_error,
              notes=excluded.notes,
              updated_at=excluded.updated_at
            """,
            (
                session["session_id"],
                session["surface"],
                session["account_label"],
                session["status"],
                session["concurrency_limit"],
                session["active_lease_count"],
                session["resume_after_utc"],
                session["last_refresh_utc"],
                session["last_error"],
                session["notes"],
                generated_utc,
                generated_utc,
            ),
        )
    conn.commit()


def _candidate_tasks(conn: sqlite3.Connection, max_tasks: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT
          t.task_id, t.lane_id, t.title, t.priority, t.owner_agent_id,
          t.evidence_required, t.next_action, t.created_at, t.updated_at,
          l.owner_thread_id
        FROM tasks t
        LEFT JOIN lanes l ON l.lane_id = t.lane_id
        WHERE t.status = 'new'
          AND t.lease_owner_agent_id IS NULL
        ORDER BY t.priority DESC, t.created_at ASC, t.task_id ASC
        LIMIT ?
        """,
        (max_tasks,),
    ).fetchall()
    return [dict(row) for row in rows]


def _slot_sequence(sessions: list[dict[str, Any]], max_tasks: int) -> list[str]:
    slots: list[str] = []
    for session in sorted(sessions, key=lambda item: item["session_id"]):
        slots.extend([session["session_id"]] * session["available_slots"])
        if len(slots) >= max_tasks:
            break
    return slots[:max_tasks]


def _next_wakeup(sessions: list[dict[str, Any]]) -> str | None:
    wakeups = [
        str(session["resume_after_utc"])
        for session in sessions
        if session["status"] == "cooling_down" and session.get("resume_after_utc")
    ]
    return min(wakeups) if wakeups else None


def _status(recommendations: list[dict[str, Any]], candidates: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> str:
    if recommendations:
        return "ready_to_dispatch"
    if not candidates:
        return "no_queued_tasks"
    if any(session["status"] == "cooling_down" for session in sessions):
        return "waiting_for_capacity"
    return "no_available_capacity"


def _next_action(status: str, next_wakeup_utc: str | None) -> str:
    if status == "ready_to_dispatch":
        return "Lease recommended tasks through a scoped local command, then dispatch only up to available session capacity."
    if status == "waiting_for_capacity":
        suffix = f" at {next_wakeup_utc}" if next_wakeup_utc else ""
        return f"Wait for session refresh{suffix}; rerun this planner when capacity becomes available."
    if status == "no_queued_tasks":
        return "No queued local tasks currently require capacity."
    return "Register or refresh a capacity session before dispatching queued work."


def _build_recommendations(tasks: list[dict[str, Any]], slots: list[str]) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []
    for task, session_id in zip(tasks, slots):
        recommendations.append(
            {
                "session_id": session_id,
                "task_id": task["task_id"],
                "lane_id": task["lane_id"],
                "priority": task["priority"],
                "owner_agent_id": task["owner_agent_id"],
                "owner_thread_id": task["owner_thread_id"],
                "evidence_required": task["evidence_required"],
                "next_action": task["next_action"],
                "recommended_action": "lease_then_dispatch_with_capacity_guard",
            }
        )
    return recommendations


def _counts(
    sessions: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "sessions_seen": len(sessions),
        "available_sessions": sum(1 for session in sessions if session["status"] == "available"),
        "cooling_down_sessions": sum(1 for session in sessions if session["status"] == "cooling_down"),
        "needs_restore_sessions": sum(1 for session in sessions if session["status"] == "needs_restore"),
        "retired_or_parked_sessions": sum(1 for session in sessions if session["status"] == "retired_or_parked"),
        "available_capacity": sum(session["available_slots"] for session in sessions),
        "queued_task_candidates": len(tasks),
        "dispatch_recommendations": len(recommendations),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Account Capacity Dispatch Plan v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        f"Capacity snapshot: `{payload['capacity_snapshot']}`",
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
            "## Sessions",
            "",
            "| Session | Surface | Status | Capacity | Resume | Last Refresh |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for session in payload["sessions"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{session['session_id']}`",
                    md_cell(session["surface"], 80),
                    f"`{session['status']}`",
                    str(session["available_slots"]),
                    md_cell(session.get("resume_after_utc") or "", 80),
                    md_cell(session.get("last_refresh_utc") or "", 80),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Dispatch Recommendations",
            "",
            "| Session | Task | Lane | Priority | Owner Thread | Action |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    if payload["dispatch_recommendations"]:
        for item in payload["dispatch_recommendations"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['session_id']}`",
                        f"`{item['task_id']}`",
                        f"`{item['lane_id']}`",
                        str(item["priority"]),
                        md_cell(item.get("owner_thread_id") or "", 120),
                        f"`{item['recommended_action']}`",
                    ]
                )
                + " |"
            )
    else:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This planner records local capacity state and writes dispatch recommendations only. It does not store credentials or refresh tokens, mutate task leases, send thread messages, start workers, approve service requests, open browsers, call APIs, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-account-capacity-dispatch-plan-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write account capacity dispatch plan', 'complete', 95, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          status=excluded.status,
          priority=excluded.priority,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            AI_RESOURCES_LANE,
            AI_RESOURCES_OWNER,
            f"account-capacity-dispatch-plan:{day}",
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
            f"artifact-account-capacity-dispatch-plan-json-{day}",
            "account_capacity_dispatch_plan_json",
            json_path,
            "Machine-readable local account capacity dispatch plan.",
        ),
        (
            f"artifact-account-capacity-dispatch-plan-md-{day}",
            "account_capacity_dispatch_plan",
            md_path,
            "Human-readable local account capacity dispatch plan.",
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
              notes=excluded.notes,
              created_at=excluded.created_at
            """,
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    conn.commit()


def build_account_capacity_dispatch_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    snapshot_path = Path(getattr(args, "capacity_snapshot"))
    max_tasks = _as_int(getattr(args, "max_tasks", 10), 10)
    sessions = _load_sessions(snapshot_path)
    _upsert_capacity_sessions(conn, sessions, generated)
    tasks = _candidate_tasks(conn, max_tasks)
    slots = _slot_sequence(sessions, max_tasks)
    recommendations = _build_recommendations(tasks, slots)
    next_wakeup_utc = _next_wakeup(sessions)
    status = _status(recommendations, tasks, sessions)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "db": str(DB_PATH),
        "status": status,
        "capacity_snapshot": str(snapshot_path),
        "max_tasks": max_tasks,
        "sessions": sessions,
        "queued_task_candidates": tasks,
        "dispatch_recommendations": recommendations,
        "next_wakeup_utc": next_wakeup_utc,
        "counts": _counts(sessions, tasks, recommendations),
        "next_action": _next_action(status, next_wakeup_utc),
        "zero_side_effect_boundary": {
            "credentials_or_tokens_stored": 0,
            "task_leases_mutated": 0,
            "thread_messages_sent": 0,
            "worker_starts": 0,
            "service_requests_approved_or_started": 0,
            "browser_sessions_started": 0,
            "external_api_calls": 0,
            "public_actions": 0,
            "wallet_payment_trading_actions": 0,
            "external_side_effects": False,
        },
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_account_capacity_dispatch_plan_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = build_account_capacity_dispatch_plan(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "next_wakeup_utc": payload["next_wakeup_utc"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
            },
            indent=2,
        )
    )


__all__ = [
    "build_account_capacity_dispatch_plan",
    "write_account_capacity_dispatch_plan_cli",
]
