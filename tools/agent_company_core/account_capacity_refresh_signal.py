"""Apply explicit local refresh signals to account capacity sessions."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import load_json, now_utc, parse_utc
from .paths import REPORTS_DIR
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "account_capacity_refresh_signal.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"account-capacity-refresh-signal-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"account-capacity-refresh-signal-v1-{day}.md")
    return json_path, md_path


def _load_signal(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise SystemExit("--signal-path must contain one JSON object")
    return payload


def _session(conn: sqlite3.Connection, session_id: str) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT session_id, status, concurrency_limit, active_lease_count,
               resume_after_utc, last_refresh_utc, last_error, updated_at
        FROM account_capacity_sessions
        WHERE session_id = ?
        """,
        (session_id,),
    ).fetchone()


def _decision(signal: dict[str, Any], row: sqlite3.Row | None) -> dict[str, Any]:
    session_id = str(signal.get("session_id") or "").strip()
    status = str(signal.get("status") or "").strip()
    observed_utc = str(signal.get("observed_utc") or "").strip()
    item: dict[str, Any] = {
        "session_id": session_id,
        "signal_id": signal.get("signal_id"),
        "signal_status": status,
        "observed_utc": observed_utc,
        "source": signal.get("source"),
        "evidence": signal.get("evidence"),
        "decision": "ignored",
        "reason": None,
    }
    if not session_id:
        item["reason"] = "missing_session_id"
        return item
    if row is None:
        item["reason"] = "missing_session"
        return item
    observed = parse_utc(observed_utc)
    updated = parse_utc(row["updated_at"])
    if observed is None:
        item["reason"] = "invalid_observed_utc"
        return item
    if updated is not None and observed <= updated:
        item["reason"] = "stale_signal"
        return item
    if status != "usable":
        item["reason"] = "signal_not_usable"
        return item
    if row["status"] == "retired_or_parked":
        item["reason"] = "session_retired_or_parked"
        return item
    item.update(
        {
            "decision": "mark_available",
            "reason": "usable_refresh_signal",
            "status_before": row["status"],
            "status_after": "available",
            "active_lease_count": int(row["active_lease_count"]),
        }
    )
    return item


def _apply_decision(
    conn: sqlite3.Connection,
    decision: dict[str, Any],
    generated_utc: str,
) -> None:
    if decision["decision"] != "mark_available":
        return
    conn.execute(
        """
        UPDATE account_capacity_sessions
        SET status = 'available',
            resume_after_utc = NULL,
            last_refresh_utc = ?,
            last_error = NULL,
            updated_at = ?
        WHERE session_id = ?
        """,
        (decision["observed_utc"], generated_utc, decision["session_id"]),
    )


def _counts(decisions: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "signals_seen": len(decisions),
        "sessions_available": sum(1 for item in decisions if item["decision"] == "mark_available"),
        "stale_signals": sum(1 for item in decisions if item.get("reason") == "stale_signal"),
        "missing_sessions": sum(1 for item in decisions if item.get("reason") == "missing_session"),
        "unusable_signals": sum(1 for item in decisions if item.get("reason") == "signal_not_usable"),
        "ignored_signals": sum(1 for item in decisions if item["decision"] == "ignored"),
    }


def _status(counts: dict[str, int]) -> str:
    if counts["sessions_available"]:
        return "capacity_available"
    return "ignored"


def _next_action(status: str) -> str:
    if status == "capacity_available":
        return "Rerun lane runtime activation planning and drain only the newly capacity-eligible recommendations."
    return "Keep sessions parked or cooling down until a newer usable refresh signal is observed."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Account Capacity Refresh Signal v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Signal path: `{payload['signal_path']}`",
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
            "## Decisions",
            "",
            "| Session | Signal | Decision | Reason | Observed |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["decisions"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.get('session_id') or ''}`",
                    md_cell(item.get("signal_id") or "", 80),
                    f"`{item['decision']}`",
                    f"`{item.get('reason') or ''}`",
                    f"`{item.get('observed_utc') or ''}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This command applies explicit local capacity refresh signals only. It does not store refresh tokens or credentials, start browsers, send thread messages, approve service requests, call APIs, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-account-capacity-refresh-signal-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Apply account capacity refresh signal', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"account-capacity-refresh-signal:{day}",
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
            f"artifact-account-capacity-refresh-signal-json-{day}",
            "account_capacity_refresh_signal_json",
            json_path,
            "Machine-readable account capacity refresh signal result.",
        ),
        (
            f"artifact-account-capacity-refresh-signal-md-{day}",
            "account_capacity_refresh_signal",
            md_path,
            "Human-readable account capacity refresh signal result.",
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


def apply_account_capacity_refresh_signal(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    signal_path = Path(getattr(args, "signal_path"))
    signal = _load_signal(signal_path)
    row = _session(conn, str(signal.get("session_id") or ""))
    decisions = [_decision(signal, row)]
    for decision in decisions:
        _apply_decision(conn, decision, generated)
    counts = _counts(decisions)
    status = _status(counts)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "signal_path": str(signal_path),
        "decisions": decisions,
        "counts": counts,
        "next_action": _next_action(status),
        "zero_side_effect_boundary": {
            "refresh_tokens_or_credentials_stored": 0,
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
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    conn.commit()
    return payload


def apply_account_capacity_refresh_signal_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = apply_account_capacity_refresh_signal(conn, args)
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
    "apply_account_capacity_refresh_signal",
    "apply_account_capacity_refresh_signal_cli",
]
