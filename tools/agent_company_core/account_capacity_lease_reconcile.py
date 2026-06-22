"""Reconcile account capacity counters from runtime delivery leases."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "account_capacity_lease_reconcile.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
TERMINAL_TASK_STATUSES = {"cancelled", "closed", "complete", "completed", "done", "killed"}


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"account-capacity-lease-reconcile-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"account-capacity-lease-reconcile-v1-{day}.md")
    return json_path, md_path


def _delivery_sessions(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        """
        SELECT DISTINCT session_id
        FROM lane_runtime_thread_deliveries
        WHERE session_id IS NOT NULL AND session_id != ''
        ORDER BY session_id
        """
    ).fetchall()
    return [row["session_id"] for row in rows]


def _active_counts_by_session(conn: sqlite3.Connection, generated_utc: str) -> dict[str, int]:
    generated_dt = parse_utc(generated_utc)
    if generated_dt is None:
        raise SystemExit(f"Invalid --now-utc: {generated_utc}")
    counts: dict[str, int] = {}
    rows = conn.execute(
        """
        SELECT d.session_id, t.task_id, t.status, t.lease_owner_agent_id, t.lease_expires_at
        FROM lane_runtime_thread_deliveries d
        JOIN tasks t ON t.task_id = d.task_id
        WHERE d.session_id IS NOT NULL AND d.session_id != ''
        """
    ).fetchall()
    for row in rows:
        expires = parse_utc(row["lease_expires_at"])
        active = (
            row["status"] not in {"complete", "cancelled"}
            and row["lease_owner_agent_id"] is not None
            and expires is not None
            and expires > generated_dt
        )
        if active:
            counts[row["session_id"]] = counts.get(row["session_id"], 0) + 1
    return counts


def _session_rows(conn: sqlite3.Connection, session_ids: list[str]) -> list[sqlite3.Row]:
    if not session_ids:
        return []
    placeholders = ",".join("?" for _ in session_ids)
    return conn.execute(
        f"""
        SELECT session_id, status, concurrency_limit, active_lease_count, resume_after_utc
        FROM account_capacity_sessions
        WHERE session_id IN ({placeholders})
        ORDER BY session_id
        """,
        tuple(session_ids),
    ).fetchall()


def _reconcile_rows(
    conn: sqlite3.Connection,
    generated_utc: str,
    no_db_record: bool,
) -> list[dict[str, Any]]:
    session_ids = _delivery_sessions(conn)
    active_counts = _active_counts_by_session(conn, generated_utc)
    rows = _session_rows(conn, session_ids)
    reconciled: list[dict[str, Any]] = []
    for row in rows:
        before = int(row["active_lease_count"])
        after = active_counts.get(row["session_id"], 0)
        item = {
            "session_id": row["session_id"],
            "status": row["status"],
            "concurrency_limit": int(row["concurrency_limit"]),
            "active_lease_count_before": before,
            "active_lease_count_after": after,
            "capacity_released": max(0, before - after),
            "capacity_claimed": max(0, after - before),
        }
        reconciled.append(item)
        if not no_db_record and before != after:
            conn.execute(
                """
                UPDATE account_capacity_sessions
                SET active_lease_count = ?,
                    updated_at = ?
                WHERE session_id = ?
                """,
                (after, generated_utc, row["session_id"]),
            )
    if not no_db_record:
        conn.commit()
    return reconciled


def _clear_terminal_task_leases(
    conn: sqlite3.Connection,
    generated_utc: str,
    no_db_record: bool,
) -> list[dict[str, Any]]:
    placeholders = ",".join("?" for _ in TERMINAL_TASK_STATUSES)
    rows = conn.execute(
        f"""
        SELECT task_id, lane_id, status, lease_owner_agent_id, lease_expires_at
        FROM tasks
        WHERE status IN ({placeholders})
          AND (lease_owner_agent_id IS NOT NULL OR lease_expires_at IS NOT NULL)
        ORDER BY task_id
        """,
        tuple(sorted(TERMINAL_TASK_STATUSES)),
    ).fetchall()
    cleared = [dict(row) for row in rows]
    if not no_db_record and cleared:
        conn.executemany(
            """
            UPDATE tasks
            SET lease_owner_agent_id = NULL,
                lease_expires_at = NULL,
                updated_at = ?
            WHERE task_id = ?
            """,
            [(generated_utc, item["task_id"]) for item in cleared],
        )
        conn.commit()
    return cleared


def _counts(items: list[dict[str, Any]], terminal_task_leases: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "sessions_reconciled": len(items),
        "sessions_changed": sum(1 for item in items if item["active_lease_count_before"] != item["active_lease_count_after"]),
        "capacity_released": sum(item["capacity_released"] for item in items),
        "capacity_claimed": sum(item["capacity_claimed"] for item in items),
        "terminal_task_leases_cleared": len(terminal_task_leases),
    }


def _status(counts: dict[str, int]) -> str:
    if counts["capacity_released"]:
        return "capacity_released"
    if counts["capacity_claimed"]:
        return "capacity_claimed"
    if counts["terminal_task_leases_cleared"]:
        return "terminal_task_leases_cleared"
    return "already_consistent"


def _next_action(status: str) -> str:
    if status == "capacity_released":
        return "Rerun lane runtime activation planning; newly freed capacity may drain the next queued lane."
    if status == "capacity_claimed":
        return "Capacity counters were raised to match active runtime deliveries; avoid extra dispatch until planning is rerun."
    if status == "terminal_task_leases_cleared":
        return "Terminal task lease fields were cleared; continue normal restore monitoring."
    return "Capacity counters already match active runtime deliveries."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Account Capacity Lease Reconcile v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
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
            "## Sessions",
            "",
            "| Session | Status | Before | After | Released | Claimed |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    if payload["sessions"]:
        for item in payload["sessions"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['session_id']}`",
                        md_cell(item["status"], 60),
                        str(item["active_lease_count_before"]),
                        str(item["active_lease_count_after"]),
                        str(item["capacity_released"]),
                        str(item["capacity_claimed"]),
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
            "This reconciler updates local account capacity counters for sessions represented in lane_runtime_thread_deliveries and clears stale lease fields on terminal tasks. It does not mutate task status, send thread messages, start workers, open browsers, approve service requests, call APIs, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-account-capacity-lease-reconcile-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Reconcile account capacity leases', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"account-capacity-lease-reconcile:{day}",
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
            f"artifact-account-capacity-lease-reconcile-json-{day}",
            "account_capacity_lease_reconcile_json",
            json_path,
            "Machine-readable account capacity lease reconciliation.",
        ),
        (
            f"artifact-account-capacity-lease-reconcile-md-{day}",
            "account_capacity_lease_reconcile",
            md_path,
            "Human-readable account capacity lease reconciliation.",
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


def reconcile_account_capacity_leases(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    no_db_record = bool(getattr(args, "no_db_record", False))
    sessions = _reconcile_rows(conn, generated, no_db_record)
    terminal_task_leases = _clear_terminal_task_leases(conn, generated, no_db_record)
    counts = _counts(sessions, terminal_task_leases)
    status = _status(counts)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "sessions": sessions,
        "terminal_task_leases_cleared": terminal_task_leases,
        "counts": counts,
        "next_action": _next_action(status),
        "zero_side_effect_boundary": {
            "task_status_mutations": 0,
            "task_lease_fields_cleared": len(terminal_task_leases) if not no_db_record else 0,
            "thread_messages_sent": 0,
            "worker_starts": 0,
            "browser_sessions_started": 0,
            "external_api_calls": 0,
            "service_requests_approved_or_started": 0,
            "public_actions": 0,
            "wallet_payment_trading_actions": 0,
            "external_side_effects": False,
        },
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not no_db_record:
        _record_run(conn, payload, json_path, md_path)
    return payload


def reconcile_account_capacity_leases_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = reconcile_account_capacity_leases(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
            },
            indent=2,
        )
    )


__all__ = [
    "reconcile_account_capacity_leases",
    "reconcile_account_capacity_leases_cli",
]
