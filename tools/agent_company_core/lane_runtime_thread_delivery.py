"""Prepare and record Codex owner-thread deliveries for runtime dispatch packets."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "lane_runtime_thread_delivery_outbox.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
VALID_RECEIPT_STATUSES = {"delivered", "send_failed"}


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"lane-runtime-thread-delivery-outbox-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"lane-runtime-thread-delivery-outbox-v1-{day}.md")
    outbox_dir = Path(
        getattr(args, "outbox_dir", None) or REPORTS_DIR / f"lane-runtime-thread-delivery-outbox-v1-{day}"
    )
    return json_path, md_path, outbox_dir


def _normalize_thread_id(thread_id: str | None) -> str:
    return str(thread_id or "").removeprefix("codex-thread:")


def _delivery_id(task_id: str) -> str:
    return f"delivery-lane-runtime-{safe_id_fragment(task_id, 90)}"


def _prompt_path(outbox_dir: Path, task_id: str) -> Path:
    return outbox_dir / f"lane-runtime-thread-delivery-{safe_id_fragment(task_id, 90)}.md"


def _load_dispatches(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    return [dict(item) for item in payload.get("leased_dispatches", [])]


def _existing_delivery(conn: sqlite3.Connection, delivery_id: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM lane_runtime_thread_deliveries WHERE delivery_id = ?",
        (delivery_id,),
    ).fetchone()


def _prompt_text(item: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Continue your active lane goal using this CEO control-plane dispatch.",
            "",
            f"Task: `{item['task_id']}`",
            f"Lane: `{item['lane_id']}`",
            f"Runtime mode: `{item.get('runtime_mode') or ''}`",
            f"Lease owner: `{item.get('lease_owner_agent_id') or item.get('owner_agent_id') or ''}`",
            f"Lease expires: `{item.get('lease_expires_at') or ''}`",
            f"Dispatch packet: `{item.get('packet_path') or ''}`",
            "",
            "Evidence:",
            str(item.get("evidence_required") or ""),
            "",
            "Next action:",
            str(item.get("next_action") or ""),
            "",
            "Boundary:",
            "Do not start browsers, create agents, mutate ownership, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone. Work locally only and write the required evidence artifact or an explicit park/revisit packet.",
            "",
            "When finished, leave the task evidence path and a short completion summary in your thread.",
            "",
        ]
    )


def _delivery_from_dispatch(
    conn: sqlite3.Connection,
    dispatch: dict[str, Any],
    outbox_dir: Path,
    generated_utc: str,
) -> dict[str, Any]:
    task_id = str(dispatch.get("task_id") or "")
    owner_thread_id = str(dispatch.get("owner_thread_id") or "")
    delivery_id = _delivery_id(task_id)
    existing = _existing_delivery(conn, delivery_id)
    if existing and existing["status"] == "delivered":
        return {
            "delivery_id": delivery_id,
            "task_id": task_id,
            "lane_id": dispatch.get("lane_id"),
            "session_id": dispatch.get("session_id"),
            "owner_agent_id": dispatch.get("owner_agent_id"),
            "owner_thread_id": owner_thread_id,
            "thread_id_for_tool": _normalize_thread_id(owner_thread_id),
            "packet_path": dispatch.get("packet_path"),
            "prompt_path": existing["prompt_path"],
            "status": "already_delivered",
            "delivered_at": existing["delivered_at"],
        }
    if not owner_thread_id:
        prompt = None
        status = "blocked_no_owner_thread"
    else:
        prompt_path = _prompt_path(outbox_dir, task_id)
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(_prompt_text(dispatch), encoding="utf-8")
        prompt = str(prompt_path)
        status = "ready_to_send"
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, NULL, ?, ?)
        ON CONFLICT(delivery_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          session_id=excluded.session_id,
          owner_agent_id=excluded.owner_agent_id,
          owner_thread_id=excluded.owner_thread_id,
          packet_path=excluded.packet_path,
          prompt_path=excluded.prompt_path,
          status=CASE
            WHEN lane_runtime_thread_deliveries.status = 'delivered' THEN lane_runtime_thread_deliveries.status
            ELSE excluded.status
          END,
          updated_at=excluded.updated_at
        """,
        (
            delivery_id,
            task_id,
            dispatch.get("lane_id"),
            dispatch.get("session_id"),
            dispatch.get("owner_agent_id"),
            owner_thread_id,
            dispatch.get("packet_path") or "",
            prompt,
            status,
            generated_utc,
            generated_utc,
        ),
    )
    return {
        "delivery_id": delivery_id,
        "task_id": task_id,
        "lane_id": dispatch.get("lane_id"),
        "session_id": dispatch.get("session_id"),
        "owner_agent_id": dispatch.get("owner_agent_id"),
        "owner_thread_id": owner_thread_id,
        "thread_id_for_tool": _normalize_thread_id(owner_thread_id),
        "packet_path": dispatch.get("packet_path"),
        "prompt_path": prompt,
        "status": status,
        "delivered_at": None,
    }


def _counts(deliveries: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "deliveries_seen": len(deliveries),
        "ready_to_send": sum(1 for item in deliveries if item["status"] == "ready_to_send"),
        "blocked_no_owner_thread": sum(1 for item in deliveries if item["status"] == "blocked_no_owner_thread"),
        "already_delivered": sum(1 for item in deliveries if item["status"] == "already_delivered"),
    }


def _status(counts: dict[str, int]) -> str:
    if counts["ready_to_send"]:
        return "ready_to_send"
    if counts["blocked_no_owner_thread"]:
        return "blocked"
    return "no_delivery_needed"


def _next_action(status: str) -> str:
    if status == "ready_to_send":
        return "Send each prompt_path to thread_id_for_tool through the Codex app thread tool, then record delivery receipts."
    if status == "blocked":
        return "Resolve missing owner_thread_id before sending; do not create duplicate workers automatically."
    return "No thread delivery is pending."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Thread Delivery Outbox v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Drain report: `{payload['drain_report']}`",
        f"JSON mirror: `{payload['json_path']}`",
        f"Outbox dir: `{payload['outbox_dir']}`",
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
            "## Deliveries",
            "",
            "| Status | Delivery | Thread | Task | Prompt |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    if payload["deliveries"]:
        for item in payload["deliveries"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['status']}`",
                        f"`{item['delivery_id']}`",
                        f"`{item.get('thread_id_for_tool') or ''}`",
                        f"`{item['task_id']}`",
                        md_cell(item.get("prompt_path") or "", 120),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This outbox writes local prompt files and delivery ledger rows only. It does not send thread messages, start workers, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-thread-delivery-outbox-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write lane runtime thread delivery outbox', 'complete', 97, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-thread-delivery-outbox:{day}",
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
            f"artifact-lane-runtime-thread-delivery-outbox-json-{day}",
            "lane_runtime_thread_delivery_outbox_json",
            json_path,
            "Machine-readable lane runtime thread delivery outbox.",
        ),
        (
            f"artifact-lane-runtime-thread-delivery-outbox-md-{day}",
            "lane_runtime_thread_delivery_outbox",
            md_path,
            "Human-readable lane runtime thread delivery outbox.",
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


def write_lane_runtime_thread_delivery_outbox(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path, outbox_dir = _report_paths(generated, args)
    drain_report = Path(getattr(args, "drain_report"))
    deliveries = [_delivery_from_dispatch(conn, item, outbox_dir, generated) for item in _load_dispatches(drain_report)]
    conn.commit()
    counts = _counts(deliveries)
    status = _status(counts)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "drain_report": str(drain_report),
        "outbox_dir": str(outbox_dir),
        "deliveries": deliveries,
        "counts": counts,
        "next_action": _next_action(status),
        "zero_side_effect_boundary": {
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
    return payload


def record_lane_runtime_thread_delivery_receipt(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    status = str(getattr(args, "status"))
    if status not in VALID_RECEIPT_STATUSES:
        raise SystemExit(f"Invalid delivery receipt status: {status}")
    delivery_id = str(getattr(args, "delivery_id"))
    row = _existing_delivery(conn, delivery_id)
    if row is None:
        raise SystemExit(f"Unknown delivery: {delivery_id}")
    ts = getattr(args, "now_utc", None) or now_utc()
    error = getattr(args, "error", None)
    delivered_at = ts if status == "delivered" else None
    conn.execute(
        """
        UPDATE lane_runtime_thread_deliveries
        SET status = ?,
            delivery_attempts = delivery_attempts + 1,
            delivered_at = COALESCE(?, delivered_at),
            last_error = ?,
            updated_at = ?
        WHERE delivery_id = ?
        """,
        (status, delivered_at, error, ts, delivery_id),
    )
    conn.commit()
    return {"ok": True, "delivery_id": delivery_id, "status": status, "delivered_at": delivered_at}


def write_lane_runtime_thread_delivery_outbox_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_lane_runtime_thread_delivery_outbox(conn, args)
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


def record_lane_runtime_thread_delivery_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    print(json.dumps(record_lane_runtime_thread_delivery_receipt(conn, args), indent=2))


__all__ = [
    "record_lane_runtime_thread_delivery_cli",
    "record_lane_runtime_thread_delivery_receipt",
    "write_lane_runtime_thread_delivery_outbox",
    "write_lane_runtime_thread_delivery_outbox_cli",
]
