"""Drain lane runtime dispatch recommendations into local leases and packets."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import timedelta
from pathlib import Path
from typing import Any

from .io import load_json, now_utc, parse_utc
from .paths import DB_PATH, REPORTS_DIR
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "lane_runtime_dispatch_drain.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(getattr(args, "json_path", None) or REPORTS_DIR / f"lane-runtime-dispatch-drain-v1-{day}.json")
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"lane-runtime-dispatch-drain-v1-{day}.md")
    packet_dir = Path(getattr(args, "packet_dir", None) or REPORTS_DIR / f"lane-runtime-dispatch-packets-v1-{day}")
    return json_path, md_path, packet_dir


def _as_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(0, parsed)


def _load_recommendations(path: Path, max_dispatches: int) -> list[dict[str, Any]]:
    payload = load_json(path)
    return [dict(item) for item in payload.get("dispatch_recommendations", [])[:max_dispatches]]


def _lease_expiry(generated_utc: str, lease_minutes: int) -> str:
    generated_dt = parse_utc(generated_utc)
    if generated_dt is None:
        raise SystemExit(f"Invalid --now-utc: {generated_utc}")
    return (generated_dt + timedelta(minutes=lease_minutes)).isoformat(timespec="seconds").replace("+00:00", "Z")


def _task_row(conn: sqlite3.Connection, task_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()


def _session_row(conn: sqlite3.Connection, session_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM account_capacity_sessions WHERE session_id = ?", (session_id,)).fetchone()


def _session_available_slots(session: sqlite3.Row) -> int:
    if session["status"] != "available":
        return 0
    return max(0, int(session["concurrency_limit"]) - int(session["active_lease_count"]))


def _active_lease(task: sqlite3.Row, generated_utc: str) -> bool:
    lease_owner = task["lease_owner_agent_id"]
    expires_at = parse_utc(task["lease_expires_at"])
    generated_dt = parse_utc(generated_utc)
    return bool(lease_owner and expires_at and generated_dt and expires_at > generated_dt)


def _skip(reason: str, recommendation: dict[str, Any]) -> dict[str, Any]:
    return {
        "reason": reason,
        "session_id": recommendation.get("session_id"),
        "task_id": recommendation.get("task_id"),
        "lane_id": recommendation.get("lane_id"),
        "owner_agent_id": recommendation.get("owner_agent_id"),
    }


def _packet_path(packet_dir: Path, task_id: str) -> Path:
    return packet_dir / f"lane-runtime-dispatch-{safe_id_fragment(task_id, 90)}.md"


def _write_packet(path: Path, item: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Dispatch Packet v1",
        "",
        f"Generated UTC: `{item['generated_utc']}`",
        f"Dry run: `{item['dry_run']}`",
        f"Task: `{item['task_id']}`",
        f"Lane: `{item['lane_id']}`",
        f"Runtime mode: `{item.get('runtime_mode') or ''}`",
        f"Session: `{item['session_id']}`",
        f"Lease owner: `{item['lease_owner_agent_id']}`",
        f"Lease expires: `{item['lease_expires_at']}`",
        f"Owner thread: `{item.get('owner_thread_id') or ''}`",
        "",
        "## Evidence",
        "",
        item.get("evidence_required") or "",
        "",
        "## Next Action",
        "",
        item.get("next_action") or "",
        "",
        "## Boundary",
        "",
        "This packet authorizes local task work only. It does not send a thread message, start a worker runtime, open a browser, approve a service request, publish, submit, spend, trade, call APIs, or contact anyone.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _apply_lease(
    conn: sqlite3.Connection,
    recommendation: dict[str, Any],
    lease_owner: str,
    lease_expires_at: str,
    generated_utc: str,
) -> None:
    task_id = str(recommendation["task_id"])
    session_id = str(recommendation["session_id"])
    row = _task_row(conn, task_id)
    if row is None:
        raise SystemExit(f"Task disappeared before lease: {task_id}")
    status = "in_progress" if row["status"] == "new" else row["status"]
    conn.execute(
        """
        UPDATE tasks
        SET status = ?,
            owner_agent_id = COALESCE(owner_agent_id, ?),
            lease_owner_agent_id = ?,
            lease_expires_at = ?,
            started_at = COALESCE(started_at, ?),
            updated_at = ?
        WHERE task_id = ?
        """,
        (status, lease_owner, lease_owner, lease_expires_at, generated_utc, generated_utc, task_id),
    )
    conn.execute(
        """
        UPDATE account_capacity_sessions
        SET active_lease_count = active_lease_count + 1,
            updated_at = ?
        WHERE session_id = ?
        """,
        (generated_utc, session_id),
    )


def _dispatch_item(
    recommendation: dict[str, Any],
    packet_path: Path,
    lease_owner: str,
    lease_expires_at: str,
    generated_utc: str,
    dry_run: bool,
) -> dict[str, Any]:
    return {
        "session_id": recommendation["session_id"],
        "task_id": recommendation["task_id"],
        "lane_id": recommendation["lane_id"],
        "runtime_mode": recommendation.get("runtime_mode"),
        "owner_agent_id": recommendation.get("owner_agent_id"),
        "owner_thread_id": recommendation.get("owner_thread_id"),
        "lease_owner_agent_id": lease_owner,
        "lease_expires_at": lease_expires_at,
        "evidence_required": recommendation.get("evidence_required"),
        "next_action": recommendation.get("next_action"),
        "packet_path": str(packet_path),
        "generated_utc": generated_utc,
        "dry_run": dry_run,
    }


def _drain(
    conn: sqlite3.Connection,
    recommendations: list[dict[str, Any]],
    generated_utc: str,
    lease_minutes: int,
    executor_agent_id: str,
    packet_dir: Path,
    dry_run: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    leased: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    lease_expires_at = _lease_expiry(generated_utc, lease_minutes)
    for recommendation in recommendations:
        task_id = str(recommendation.get("task_id") or "")
        session_id = str(recommendation.get("session_id") or "")
        if not task_id or not session_id:
            skipped.append(_skip("missing_task_or_session_id", recommendation))
            continue
        task = _task_row(conn, task_id)
        if task is None:
            skipped.append(_skip("missing_task", recommendation))
            continue
        if task["status"] in {"complete", "cancelled"}:
            skipped.append(_skip(f"task_{task['status']}", recommendation))
            continue
        if _active_lease(task, generated_utc):
            skipped.append(_skip("task_already_leased", recommendation))
            continue
        session = _session_row(conn, session_id)
        if session is None:
            skipped.append(_skip("missing_session", recommendation))
            continue
        if session["status"] != "available":
            skipped.append(_skip(f"session_{session['status']}", recommendation))
            continue
        if _session_available_slots(session) <= 0:
            skipped.append(_skip("capacity_full", recommendation))
            continue

        lease_owner = str(recommendation.get("owner_agent_id") or executor_agent_id)
        packet_path = _packet_path(packet_dir, task_id)
        item = _dispatch_item(recommendation, packet_path, lease_owner, lease_expires_at, generated_utc, dry_run)
        _write_packet(packet_path, item)
        leased.append(item)
        if not dry_run:
            _apply_lease(conn, recommendation, lease_owner, lease_expires_at, generated_utc)
    if not dry_run:
        conn.commit()
    return leased, skipped


def _status(leased: list[dict[str, Any]], dry_run: bool) -> str:
    if leased and dry_run:
        return "dry_run_dispatch_packets_ready"
    if leased:
        return "dispatch_packets_ready"
    return "no_dispatches_leased"


def _counts(
    recommendations: list[dict[str, Any]],
    leased: list[dict[str, Any]],
    skipped: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "recommendations_seen": len(recommendations),
        "leased_dispatches": len(leased),
        "skipped_dispatches": len(skipped),
        "packets_written": len(leased),
        "sessions_touched": len({item["session_id"] for item in leased}),
    }


def _next_action(status: str, dry_run: bool) -> str:
    if status == "dry_run_dispatch_packets_ready" or dry_run:
        return "Review dry-run packets; rerun without --dry-run to lease tasks when capacity should be consumed."
    if status == "dispatch_packets_ready":
        return "Deliver the dispatch packets to the leased owner threads through the next approved local worker adapter."
    return "No recommendations were leased; rerun the activation planner after capacity refresh or task queue changes."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Dispatch Drain v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Dry run: `{payload['dry_run']}`",
        f"Activation plan: `{payload['activation_plan']}`",
        f"JSON mirror: `{payload['json_path']}`",
        f"Packet dir: `{payload['packet_dir']}`",
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
            "## Leased Dispatches",
            "",
            "| Session | Task | Lane | Lease Owner | Expires | Packet |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    if payload["leased_dispatches"]:
        for item in payload["leased_dispatches"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['session_id']}`",
                        f"`{item['task_id']}`",
                        f"`{item['lane_id']}`",
                        f"`{item['lease_owner_agent_id']}`",
                        f"`{item['lease_expires_at']}`",
                        md_cell(item["packet_path"], 120),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Skipped Dispatches",
            "",
            "| Reason | Session | Task | Lane |",
            "| --- | --- | --- | --- |",
        ]
    )
    if payload["skipped_dispatches"]:
        for item in payload["skipped_dispatches"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['reason']}`",
                        f"`{item.get('session_id') or ''}`",
                        f"`{item.get('task_id') or ''}`",
                        f"`{item.get('lane_id') or ''}`",
                    ]
                )
                + " |"
            )
    else:
        lines.append("| none |  |  |  |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This drain only writes local packets and, when not in dry-run mode, mutates local task leases and account capacity counters. It does not send thread messages, start workers, open browsers, approve service requests, publish, submit, spend, trade, call APIs, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-dispatch-drain-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Drain lane runtime dispatch plan', 'complete', 97, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-dispatch-drain:{day}",
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
            f"artifact-lane-runtime-dispatch-drain-json-{day}",
            "lane_runtime_dispatch_drain_json",
            json_path,
            "Machine-readable local lane runtime dispatch drain.",
        ),
        (
            f"artifact-lane-runtime-dispatch-drain-md-{day}",
            "lane_runtime_dispatch_drain",
            md_path,
            "Human-readable local lane runtime dispatch drain.",
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


def drain_lane_runtime_dispatch_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path, packet_dir = _report_paths(generated, args)
    activation_plan = Path(getattr(args, "activation_plan"))
    max_dispatches = _as_int(getattr(args, "max_dispatches", 10), 10) or 10
    lease_minutes = _as_int(getattr(args, "lease_minutes", 120), 120) or 120
    executor_agent_id = str(getattr(args, "executor_agent_id", None) or "lane-runtime-dispatch-drain-executor")
    dry_run = bool(getattr(args, "dry_run", False))
    recommendations = _load_recommendations(activation_plan, max_dispatches)
    leased, skipped = _drain(
        conn,
        recommendations,
        generated,
        lease_minutes,
        executor_agent_id,
        packet_dir,
        dry_run,
    )
    status = _status(leased, dry_run)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "db": str(DB_PATH),
        "status": status,
        "dry_run": dry_run,
        "activation_plan": str(activation_plan),
        "max_dispatches": max_dispatches,
        "lease_minutes": lease_minutes,
        "executor_agent_id": executor_agent_id,
        "packet_dir": str(packet_dir),
        "leased_dispatches": leased,
        "skipped_dispatches": skipped,
        "counts": _counts(recommendations, leased, skipped),
        "next_action": _next_action(status, dry_run),
        "zero_side_effect_boundary": {
            "task_leases_mutated": 0 if dry_run else len(leased),
            "account_capacity_counters_mutated": 0 if dry_run else len(leased),
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


def write_lane_runtime_dispatch_drain_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = drain_lane_runtime_dispatch_plan(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "packet_dir": payload["packet_dir"],
                "dry_run": payload["dry_run"],
            },
            indent=2,
        )
    )


__all__ = [
    "drain_lane_runtime_dispatch_plan",
    "write_lane_runtime_dispatch_drain_cli",
]
