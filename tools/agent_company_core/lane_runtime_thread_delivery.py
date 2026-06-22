"""Prepare and record Codex owner-thread deliveries for runtime dispatch packets."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "lane_runtime_thread_delivery_outbox.v1"
APPROVAL_SCHEMA_VERSION = "lane_runtime_thread_delivery_approval.v1"
APPROVAL_DRAFTS_SCHEMA_VERSION = "lane_runtime_thread_delivery_approval_drafts.v1"
APPROVAL_PROMOTION_SCHEMA_VERSION = "lane_runtime_thread_delivery_approval_promotion.v1"
SEND_PREFLIGHT_SCHEMA_VERSION = "lane_runtime_thread_delivery_send_preflight.v1"
SAFE_LOCAL_AUTO_WAKE_AUTHORITY = "safe_local_continuity_wake"
APPROVED_THREAD_DELIVERY_AUTHORITY = "approved_thread_delivery"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
VALID_RECEIPT_STATUSES = {"delivered", "send_failed"}
VALID_APPROVAL_DECISIONS = {"send_approved", "keep_parked"}
APPROVAL_DECISION_FILE_SUFFIXES = {
    "send_approved": "send-approved",
    "keep_parked": "keep-parked",
}
SECRET_FIELD_FRAGMENTS = {
    "api_key",
    "cookie",
    "credential",
    "password",
    "private_key",
    "refresh_token",
    "secret",
    "seed_phrase",
    "token",
    "otp",
}
SAFE_AUTO_WAKE_PROMPT_MARKERS = (
    "Continue your active lane goal using this CEO control-plane dispatch.",
    "Boundary:",
    "Do not start browsers, create agents, mutate ownership, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone.",
    "Work locally only and write the required evidence artifact or an explicit park/revisit packet.",
)
SECRET_LIKE_TEXT_PATTERNS = (
    re.compile(r"\b(?:api[_-]?key|refresh[_-]?token|private[_-]?key)\b\s*[:=]", re.IGNORECASE),
    re.compile(r"\b(?:password|secret|cookie|otp|token)\b\s*[:=]", re.IGNORECASE),
    re.compile(r"\bseed\s+phrase\b\s*[:=]", re.IGNORECASE),
)


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


def _approval_report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-v1-{day}.md")
    return json_path, md_path


def _approval_drafts_report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-drafts-v1-{day}.json"
    )
    md_path = Path(
        getattr(args, "path", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-drafts-v1-{day}.md"
    )
    draft_dir = Path(
        getattr(args, "draft_dir", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-drafts-v1-{day}"
    )
    return json_path, md_path, draft_dir


def _approval_promotion_report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-promotion-v1-{day}.json"
    )
    md_path = Path(
        getattr(args, "path", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-approval-promotion-v1-{day}.md"
    )
    return json_path, md_path


def _send_preflight_report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(
        getattr(args, "json_path", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-send-preflight-v1-{day}.json"
    )
    md_path = Path(
        getattr(args, "path", None)
        or REPORTS_DIR / f"lane-runtime-thread-delivery-send-preflight-v1-{day}.md"
    )
    return json_path, md_path


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
            "lease_expires_at": dispatch.get("lease_expires_at"),
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
        "lease_expires_at": dispatch.get("lease_expires_at"),
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


def _zero_side_effect_boundary() -> dict[str, Any]:
    return {
        "thread_messages_sent": 0,
        "worker_starts": 0,
        "browser_sessions_started": 0,
        "external_api_calls": 0,
        "service_requests_approved_or_started": 0,
        "public_actions": 0,
        "wallet_payment_trading_actions": 0,
        "external_side_effects": False,
    }


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


def _write_approval_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Thread Delivery Approval v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Delivery: `{payload.get('delivery_id') or ''}`",
        f"Decision: `{payload.get('decision') or ''}`",
        f"Signal: `{payload.get('approval_signal') or ''}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Result",
        "",
        f"- OK: `{payload['ok']}`",
        f"- Reason: {payload.get('reason') or 'accepted'}",
        "",
        "## Boundary",
        "",
        "This approval command writes local approval evidence and delivery ledger status only. It does not send thread messages, start workers, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_approval_drafts_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Thread Delivery Approval Drafts v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Draft dir: `{payload['draft_dir']}`",
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
            "## Drafts",
            "",
            "| Delivery | Decision | Thread | Draft | Active Signal Path |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    if payload["drafts"]:
        for item in payload["drafts"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['delivery_id']}`",
                        f"`{item.get('decision') or ''}`",
                        f"`{item['thread_id_for_tool']}`",
                        md_cell(item.get("draft_path") or "", 120),
                        md_cell(item.get("active_signal_path") or "", 120),
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
            "This command writes local approval draft files only. It does not approve deliveries, send thread messages, start workers, open browsers, call APIs, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_approval_promotion_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Thread Delivery Approval Promotion v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"OK: `{payload['ok']}`",
        f"Draft path: `{payload.get('draft_path') or ''}`",
        f"Active signal path: `{payload.get('active_signal_path') or ''}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Result",
        "",
        f"- Delivery: `{payload.get('delivery_id') or ''}`",
        f"- Reason: {payload.get('reason') or 'accepted'}",
        "",
        "## Next Action",
        "",
        payload["next_action"],
        "",
        "## Boundary",
        "",
        "This command writes one local active approval-signal file only after explicit review confirmation. It does not mutate delivery status, send thread messages, start workers, open browsers, call APIs, publish, submit, spend, trade, or contact anyone.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_send_preflight_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Thread Delivery Send Preflight v1",
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
            "## Send Packets",
            "",
            "| Delivery | Thread | Prompt | Receipt |",
            "| --- | --- | --- | --- |",
        ]
    )
    if payload["send_packets"]:
        for item in payload["send_packets"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['delivery_id']}`",
                        f"`{item['thread_id_for_tool']}`",
                        md_cell(item.get("prompt_path") or "", 120),
                        md_cell(item.get("receipt_command") or "", 120),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| none |  |  |  |")
    if payload["blocked_deliveries"]:
        lines.extend(
            [
                "",
                "## Blocked",
                "",
                "| Delivery | Reason | Prompt |",
                "| --- | --- | --- |",
            ]
        )
        for item in payload["blocked_deliveries"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['delivery_id']}`",
                        f"`{item['reason']}`",
                        md_cell(item.get("prompt_path") or "", 120),
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
            "This preflight writes local send packets only. It does not send thread messages, start workers, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _secret_like_key(payload: Any, prefix: str = "") -> str | None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key).lower()
            key_path = f"{prefix}.{key}" if prefix else str(key)
            if any(fragment in key_text for fragment in SECRET_FIELD_FRAGMENTS):
                return key_path
            nested = _secret_like_key(value, key_path)
            if nested:
                return nested
    elif isinstance(payload, list):
        for index, item in enumerate(payload):
            nested = _secret_like_key(item, f"{prefix}[{index}]")
            if nested:
                return nested
    return None


def _secret_like_text(text: str) -> str | None:
    for pattern in SECRET_LIKE_TEXT_PATTERNS:
        if pattern.search(text):
            return pattern.pattern
    return None


def _safe_local_auto_wake_assessment(row: sqlite3.Row, prompt_text: str) -> dict[str, Any]:
    thread_id = _normalize_thread_id(row["owner_thread_id"])
    if not thread_id:
        return {"safe": False, "reason": "missing_owner_thread_id"}
    missing_markers = [marker for marker in SAFE_AUTO_WAKE_PROMPT_MARKERS if marker not in prompt_text]
    if missing_markers:
        return {
            "safe": False,
            "reason": "prompt_not_generated_by_local_continuity_delivery_contract",
            "missing_markers": missing_markers,
        }
    secret_pattern = _secret_like_text(prompt_text)
    if secret_pattern:
        return {
            "safe": False,
            "reason": "prompt_contains_secret_like_assignment",
            "pattern": secret_pattern,
        }
    return {
        "safe": True,
        "reason": "local_only_continuity_wake",
        "required_prompt_markers": list(SAFE_AUTO_WAKE_PROMPT_MARKERS),
        "external_side_effect_boundary": "thread wake only; worker prompt forbids browser, account, API, public, payment, trade, ownership, and agent-creation actions",
    }


def _active_resume_delivery_rows(conn: sqlite3.Connection, now_value: str, max_deliveries: int) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT d.delivery_id, d.task_id, d.lane_id, d.session_id, d.owner_agent_id, d.owner_thread_id,
               d.packet_path, d.prompt_path, d.status, d.delivery_attempts, d.delivered_at, d.last_error,
               d.created_at, d.updated_at
        FROM lane_runtime_thread_deliveries d
        JOIN tasks t ON t.task_id = d.task_id
        JOIN account_capacity_sessions s ON s.session_id = d.session_id
        WHERE d.status IN ('delivered', 'send_failed')
          AND t.status = 'in_progress'
          AND t.lease_expires_at IS NOT NULL
          AND t.lease_expires_at > ?
          AND s.surface = 'codex'
          AND s.status = 'available'
          AND s.last_refresh_utc IS NOT NULL
          AND COALESCE(d.delivered_at, d.updated_at, d.created_at) < s.last_refresh_utc
          AND d.owner_thread_id LIKE 'codex-thread:%'
        ORDER BY s.last_refresh_utc DESC, d.updated_at ASC, d.delivery_id
        LIMIT ?
        """,
        (now_value, max_deliveries),
    ).fetchall()


def count_active_resume_thread_deliveries(conn: sqlite3.Connection, now_value: str) -> int:
    row = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM lane_runtime_thread_deliveries d
        JOIN tasks t ON t.task_id = d.task_id
        JOIN account_capacity_sessions s ON s.session_id = d.session_id
        WHERE d.status IN ('delivered', 'send_failed')
          AND t.status = 'in_progress'
          AND t.lease_expires_at IS NOT NULL
          AND t.lease_expires_at > ?
          AND s.surface = 'codex'
          AND s.status = 'available'
          AND s.last_refresh_utc IS NOT NULL
          AND COALESCE(d.delivered_at, d.updated_at, d.created_at) < s.last_refresh_utc
          AND d.owner_thread_id LIKE 'codex-thread:%'
        """,
        (now_value,),
    ).fetchone()
    return int(row["count"] if row else 0)


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


def _record_approval_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    delivery_fragment = safe_id_fragment(str(payload.get("delivery_id") or "unknown"), 48)
    task_id = f"task-lane-runtime-thread-delivery-approval-v1-{day}-{delivery_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Apply lane runtime thread delivery approval signal', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-thread-delivery-approval:{delivery_fragment}",
            str(md_path),
            payload.get("next_action") or "",
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (
            f"artifact-lane-runtime-thread-delivery-approval-json-{day}-{delivery_fragment}",
            "lane_runtime_thread_delivery_approval_json",
            json_path,
            "Machine-readable lane runtime thread delivery approval result.",
        ),
        (
            f"artifact-lane-runtime-thread-delivery-approval-md-{day}-{delivery_fragment}",
            "lane_runtime_thread_delivery_approval",
            md_path,
            "Human-readable lane runtime thread delivery approval result.",
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


def _record_approval_drafts_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-thread-delivery-approval-drafts-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write lane runtime thread delivery approval drafts', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-thread-delivery-approval-drafts:{day}",
            str(md_path),
            payload.get("next_action") or "",
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (
            f"artifact-lane-runtime-thread-delivery-approval-drafts-json-{day}",
            "lane_runtime_thread_delivery_approval_drafts_json",
            json_path,
            "Machine-readable lane runtime thread delivery approval drafts.",
        ),
        (
            f"artifact-lane-runtime-thread-delivery-approval-drafts-md-{day}",
            "lane_runtime_thread_delivery_approval_drafts",
            md_path,
            "Human-readable lane runtime thread delivery approval drafts.",
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


def _record_approval_promotion_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    delivery_fragment = safe_id_fragment(str(payload.get("delivery_id") or "unknown"), 48)
    task_id = f"task-lane-runtime-thread-delivery-approval-promotion-v1-{day}-{delivery_fragment}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Promote reviewed thread delivery approval draft', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-thread-delivery-approval-promotion:{delivery_fragment}",
            str(md_path),
            payload.get("next_action") or "",
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (
            f"artifact-lane-runtime-thread-delivery-approval-promotion-json-{day}-{delivery_fragment}",
            "lane_runtime_thread_delivery_approval_promotion_json",
            json_path,
            "Machine-readable lane runtime thread delivery approval promotion result.",
        ),
        (
            f"artifact-lane-runtime-thread-delivery-approval-promotion-md-{day}-{delivery_fragment}",
            "lane_runtime_thread_delivery_approval_promotion",
            md_path,
            "Human-readable lane runtime thread delivery approval promotion result.",
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


def _record_send_preflight_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-thread-delivery-send-preflight-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write lane runtime thread delivery send preflight', 'complete', 98, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-thread-delivery-send-preflight:{day}",
            str(md_path),
            payload.get("next_action") or "",
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        (
            f"artifact-lane-runtime-thread-delivery-send-preflight-json-{day}",
            "lane_runtime_thread_delivery_send_preflight_json",
            json_path,
            "Machine-readable lane runtime thread delivery send preflight.",
        ),
        (
            f"artifact-lane-runtime-thread-delivery-send-preflight-md-{day}",
            "lane_runtime_thread_delivery_send_preflight",
            md_path,
            "Human-readable lane runtime thread delivery send preflight.",
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
            **_zero_side_effect_boundary(),
        },
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def _approval_result(
    *,
    generated: str,
    json_path: Path,
    md_path: Path,
    signal_path: Path,
    ok: bool,
    status: str,
    reason: str | None,
    signal: dict[str, Any] | None,
    row: sqlite3.Row | None,
) -> dict[str, Any]:
    delivery_id = str((signal or {}).get("delivery_id") or (row["delivery_id"] if row else ""))
    decision = str((signal or {}).get("decision") or "")
    payload: dict[str, Any] = {
        "schema_version": APPROVAL_SCHEMA_VERSION,
        "generated_utc": generated,
        "ok": ok,
        "status": status,
        "reason": reason,
        "approval_signal": str(signal_path),
        "approval_id": (signal or {}).get("approval_id"),
        "delivery_id": delivery_id,
        "decision": decision,
        "thread_id_for_tool": (signal or {}).get("thread_id_for_tool"),
        "expected_thread_id_for_tool": _normalize_thread_id(row["owner_thread_id"]) if row else None,
        "prompt_path": row["prompt_path"] if row else None,
        "next_action": (
            "A separate scoped sender may now send this prompt and record a delivery receipt."
            if ok and status == "send_approved"
            else "Keep the delivery local until a valid scoped approval signal is supplied."
        ),
        "zero_side_effect_boundary": _zero_side_effect_boundary(),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    return payload


def _write_approval_result(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    payload: dict[str, Any],
    json_path: Path,
    md_path: Path,
) -> dict[str, Any]:
    _write_json(json_path, payload)
    _write_approval_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_approval_run(conn, payload, json_path, md_path)
    return payload


def _ready_delivery_rows(conn: sqlite3.Connection, max_deliveries: int) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
               packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
               created_at, updated_at
        FROM lane_runtime_thread_deliveries
        WHERE status = 'ready_to_send'
        ORDER BY updated_at ASC, delivery_id
        LIMIT ?
        """,
        (max_deliveries,),
    ).fetchall()


def _approval_decision_file_suffix(decision: str) -> str:
    return APPROVAL_DECISION_FILE_SUFFIXES.get(decision, safe_id_fragment(decision or "unknown-decision", 40))


def _approval_signal_path(delivery_id: str, decision: str = "send_approved") -> Path:
    return (
        Path("state")
        / "thread-delivery-approvals"
        / f"{safe_id_fragment(delivery_id, 90)}-{_approval_decision_file_suffix(decision)}.json"
    )


def _approval_draft_payload(
    row: sqlite3.Row,
    generated_utc: str,
    operator: str,
    decision: str = "send_approved",
) -> dict[str, Any]:
    delivery_id = str(row["delivery_id"])
    if decision == "keep_parked":
        scope = "Approve keeping only this delivery parked; do not send the prompt."
        attestation = "No credential or token is included; this keeps only this one local delivery parked."
        approval_id = f"approval-{safe_id_fragment(delivery_id, 72)}-keep-parked"
    else:
        scope = "Approve sending only the exact prompt_path currently recorded for this delivery."
        attestation = "No credential or token is included; this approves only this one local delivery."
        approval_id = f"approval-{safe_id_fragment(delivery_id, 80)}"
    return {
        "approval_id": approval_id,
        "delivery_id": delivery_id,
        "thread_id_for_tool": _normalize_thread_id(row["owner_thread_id"]),
        "decision": decision,
        "approved_utc": generated_utc,
        "operator": operator,
        "scope": scope,
        "attestation": attestation,
    }


def write_lane_runtime_thread_delivery_approval_drafts(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path, draft_dir = _approval_drafts_report_paths(generated, args)
    max_deliveries = max(1, int(getattr(args, "max_deliveries", 10)))
    operator = str(getattr(args, "operator", "matth") or "matth")
    rows = _ready_delivery_rows(conn, max_deliveries)
    draft_dir.mkdir(parents=True, exist_ok=True)
    drafts: list[dict[str, Any]] = []
    for row in rows:
        delivery_id = str(row["delivery_id"])
        for decision in ["send_approved", "keep_parked"]:
            draft_path = draft_dir / (
                f"{safe_id_fragment(delivery_id, 90)}-{_approval_decision_file_suffix(decision)}.json"
            )
            draft_payload = _approval_draft_payload(row, generated, operator, decision)
            draft_path.write_text(json.dumps(draft_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            drafts.append(
                {
                    "delivery_id": delivery_id,
                    "task_id": row["task_id"],
                    "lane_id": row["lane_id"],
                    "thread_id_for_tool": _normalize_thread_id(row["owner_thread_id"]),
                    "prompt_path": row["prompt_path"],
                    "decision": decision,
                    "draft_path": str(draft_path),
                    "active_signal_path": _approval_signal_path(delivery_id, decision).as_posix(),
                }
            )
    counts = {
        "ready_deliveries_seen": len(rows),
        "drafts_written": len(drafts),
        "send_approved_drafts": sum(1 for item in drafts if item.get("decision") == "send_approved"),
        "keep_parked_drafts": sum(1 for item in drafts if item.get("decision") == "keep_parked"),
    }
    status = "approval_drafts_ready" if drafts else "no_ready_deliveries"
    payload = {
        "schema_version": APPROVAL_DRAFTS_SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "draft_dir": str(draft_dir),
        "counts": counts,
        "drafts": drafts,
        "next_action": (
            "Review each draft and, only after explicit approval, place the chosen JSON in its active_signal_path."
            if drafts
            else "No ready thread deliveries need approval drafts."
        ),
        "zero_side_effect_boundary": _zero_side_effect_boundary(),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_approval_drafts_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_approval_drafts_run(conn, payload, json_path, md_path)
    return payload


def _promotion_result(
    *,
    generated: str,
    json_path: Path,
    md_path: Path,
    draft_path: Path,
    active_signal_path: Path | None,
    ok: bool,
    status: str,
    reason: str | None,
    draft: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "schema_version": APPROVAL_PROMOTION_SCHEMA_VERSION,
        "generated_utc": generated,
        "ok": ok,
        "status": status,
        "reason": reason,
        "draft_path": str(draft_path),
        "active_signal_path": str(active_signal_path) if active_signal_path else None,
        "approval_id": (draft or {}).get("approval_id"),
        "delivery_id": (draft or {}).get("delivery_id"),
        "thread_id_for_tool": (draft or {}).get("thread_id_for_tool"),
        "decision": (draft or {}).get("decision"),
        "next_action": (
            "Run the restore cycle with --auto-apply-ready-thread-delivery-approval to apply this local signal."
            if ok
            else "Review the rejection reason and regenerate or correct the approval draft before promotion."
        ),
        "zero_side_effect_boundary": {
            **_zero_side_effect_boundary(),
            "delivery_status_mutations": 0,
            "delivery_attempts_incremented": 0,
        },
        "json_path": str(json_path),
        "md_path": str(md_path),
    }


def _write_promotion_result(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    payload: dict[str, Any],
    json_path: Path,
    md_path: Path,
) -> dict[str, Any]:
    _write_json(json_path, payload)
    _write_approval_promotion_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_approval_promotion_run(conn, payload, json_path, md_path)
    return payload


def promote_lane_runtime_thread_delivery_approval_draft(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _approval_promotion_report_paths(generated, args)
    draft_path = Path(getattr(args, "draft_path"))
    active_dir = Path(getattr(args, "active_signal_dir", None) or Path("state") / "thread-delivery-approvals")

    try:
        draft = load_json(draft_path)
    except (json.JSONDecodeError, OSError) as exc:
        draft = None
        return _write_promotion_result(
            conn,
            args,
            _promotion_result(
                generated=generated,
                json_path=json_path,
                md_path=md_path,
                draft_path=draft_path,
                active_signal_path=None,
                ok=False,
                status="rejected",
                reason=f"unreadable_draft:{exc.__class__.__name__}",
                draft=None,
            ),
            json_path,
            md_path,
        )
    if not isinstance(draft, dict):
        draft = {}

    delivery_id = str(draft.get("delivery_id") or "").strip()
    decision = str(draft.get("decision") or "").strip()
    active_path = active_dir / (
        f"{safe_id_fragment(delivery_id or 'unknown', 90)}-{_approval_decision_file_suffix(decision)}.json"
    )

    def reject(reason: str) -> dict[str, Any]:
        payload = _promotion_result(
            generated=generated,
            json_path=json_path,
            md_path=md_path,
            draft_path=draft_path,
            active_signal_path=active_path,
            ok=False,
            status="rejected",
            reason=reason,
            draft=draft,
        )
        return _write_promotion_result(conn, args, payload, json_path, md_path)

    if not getattr(args, "confirm_reviewed", False):
        return reject("missing_confirm_reviewed")
    secret_key = _secret_like_key(draft)
    if secret_key:
        return reject(f"approval draft contains credential-like key: {secret_key}")
    if not delivery_id:
        return reject("missing_delivery_id")
    row = _existing_delivery(conn, delivery_id)
    if row is None:
        return reject(f"unknown delivery_id: {delivery_id}")
    if row["status"] != "ready_to_send":
        return reject(f"delivery is not ready_to_send: {row['status']}")
    if decision not in VALID_APPROVAL_DECISIONS:
        return reject(f"invalid draft decision: {decision}")
    expected_thread_id = _normalize_thread_id(row["owner_thread_id"])
    if str(draft.get("thread_id_for_tool") or "") != expected_thread_id:
        return reject("thread_id_for_tool mismatch")
    if "only" not in str(draft.get("attestation") or "").lower():
        return reject("attestation must scope approval to only this delivery")

    active_path.parent.mkdir(parents=True, exist_ok=True)
    active_path.write_text(json.dumps(draft, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload = _promotion_result(
        generated=generated,
        json_path=json_path,
        md_path=md_path,
        draft_path=draft_path,
        active_signal_path=active_path,
        ok=True,
        status="approval_signal_ready",
        reason=None,
        draft=draft,
    )
    return _write_promotion_result(conn, args, payload, json_path, md_path)


def apply_lane_runtime_thread_delivery_approval_signal(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _approval_report_paths(generated, args)
    signal_path = Path(getattr(args, "approval_signal"))
    signal = load_json(signal_path)
    secret_key = _secret_like_key(signal)
    delivery_id = str(signal.get("delivery_id") or "")
    row = _existing_delivery(conn, delivery_id) if delivery_id else None

    def reject(reason: str) -> dict[str, Any]:
        payload = _approval_result(
            generated=generated,
            json_path=json_path,
            md_path=md_path,
            signal_path=signal_path,
            ok=False,
            status="rejected",
            reason=reason,
            signal=signal,
            row=row,
        )
        return _write_approval_result(conn, args, payload, json_path, md_path)

    if secret_key:
        return reject(f"approval signal contains credential-like key: {secret_key}")
    if not delivery_id:
        return reject("missing delivery_id")
    if row is None:
        return reject(f"unknown delivery_id: {delivery_id}")
    decision = str(signal.get("decision") or "")
    if decision not in VALID_APPROVAL_DECISIONS:
        return reject(f"invalid decision: {decision}")
    if row["status"] != "ready_to_send":
        return reject(f"delivery is not ready_to_send: {row['status']}")
    expected_thread_id = _normalize_thread_id(row["owner_thread_id"])
    if str(signal.get("thread_id_for_tool") or "") != expected_thread_id:
        return reject("thread_id_for_tool mismatch")
    if not str(row["prompt_path"] or "").strip():
        return reject("delivery has no prompt_path")
    if not str(signal.get("operator") or "").strip():
        return reject("missing operator")
    if "only" not in str(signal.get("attestation") or "").lower():
        return reject("attestation must scope approval to only this delivery")

    new_status = "send_approved" if decision == "send_approved" else "send_approval_parked"
    last_error = None if new_status == "send_approved" else "human kept parked through approval signal"
    conn.execute(
        """
        UPDATE lane_runtime_thread_deliveries
        SET status = ?,
            last_error = ?,
            updated_at = ?
        WHERE delivery_id = ?
        """,
        (new_status, last_error, generated, delivery_id),
    )
    conn.commit()
    refreshed = _existing_delivery(conn, delivery_id)
    payload = _approval_result(
        generated=generated,
        json_path=json_path,
        md_path=md_path,
        signal_path=signal_path,
        ok=True,
        status=new_status,
        reason=None,
        signal=signal,
        row=refreshed,
    )
    return _write_approval_result(conn, args, payload, json_path, md_path)


def _approved_delivery_rows(conn: sqlite3.Connection, max_deliveries: int) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
               packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
               created_at, updated_at
        FROM lane_runtime_thread_deliveries
        WHERE status = 'send_approved'
        ORDER BY updated_at ASC, delivery_id
        LIMIT ?
        """,
        (max_deliveries,),
    ).fetchall()


def _delivery_receipt_command(delivery_id: str, status: str, error_placeholder: bool = False) -> str:
    command = (
        "python tools\\agent_company.py record-lane-runtime-thread-delivery "
        f"--delivery-id {delivery_id} --status {status}"
    )
    if error_placeholder:
        command += " --error <reason>"
    return command


def _send_preflight_packet(
    row: sqlite3.Row,
    *,
    send_authority: str,
    auto_wake_authorized: bool,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    delivery_id = str(row["delivery_id"])
    prompt_path = Path(str(row["prompt_path"] or ""))
    blocked_base = {
        "delivery_id": delivery_id,
        "task_id": row["task_id"],
        "lane_id": row["lane_id"],
        "thread_id_for_tool": _normalize_thread_id(row["owner_thread_id"]),
        "prompt_path": str(row["prompt_path"] or ""),
        "source_delivery_status": row["status"],
        "send_authority": send_authority,
    }
    if not str(row["prompt_path"] or "").strip():
        return None, {**blocked_base, "reason": "missing_prompt_path"}
    if not prompt_path.exists() or not prompt_path.is_file():
        return None, {**blocked_base, "reason": "prompt_file_not_found"}
    prompt_text = prompt_path.read_text(encoding="utf-8")
    safety_assessment = (
        _safe_local_auto_wake_assessment(row, prompt_text)
        if send_authority == SAFE_LOCAL_AUTO_WAKE_AUTHORITY
        else {
            "safe": True,
            "reason": "delivery_already_has_scoped_send_approval",
        }
    )
    if not safety_assessment["safe"]:
        return None, {
            **blocked_base,
            "reason": safety_assessment["reason"],
            "safety_assessment": safety_assessment,
        }
    packet = {
        "delivery_id": delivery_id,
        "task_id": row["task_id"],
        "lane_id": row["lane_id"],
        "session_id": row["session_id"],
        "owner_agent_id": row["owner_agent_id"],
        "owner_thread_id": row["owner_thread_id"],
        "thread_id_for_tool": _normalize_thread_id(row["owner_thread_id"]),
        "packet_path": row["packet_path"],
        "prompt_path": str(prompt_path),
        "prompt_sha256": sha256_file(prompt_path),
        "prompt_text": prompt_text,
        "source_delivery_status": row["status"],
        "send_authority": send_authority,
        "auto_wake_authorized": auto_wake_authorized,
        "safety_assessment": safety_assessment,
        "send_tool_intent": "codex_app.send_message_to_thread",
        "receipt_command": _delivery_receipt_command(delivery_id, "delivered"),
        "failure_receipt_command": _delivery_receipt_command(delivery_id, "send_failed", error_placeholder=True),
    }
    return packet, None


def _send_preflight_status(counts: dict[str, int]) -> str:
    if counts.get("auto_wake_packets_ready", 0):
        return "auto_wake_sends_ready"
    if counts["send_packets_ready"]:
        return "approved_sends_ready"
    if counts.get("blocked_missing_prompt", 0) or counts.get("blocked_auto_wake_safety", 0):
        return "blocked"
    return "no_approved_sends"


def _send_preflight_next_action(status: str) -> str:
    if status == "auto_wake_sends_ready":
        return "Send each auto_wake_authorized prompt_text to thread_id_for_tool with codex_app.send_message_to_thread, then run the receipt command."
    if status == "approved_sends_ready":
        return "Use a separately approved thread sender to send each prompt_text to thread_id_for_tool, then run the receipt command."
    if status == "blocked":
        return "Repair missing prompt files or auto-wake safety failures before attempting a thread send."
    return "No approved thread deliveries are waiting to be sent."


def write_lane_runtime_thread_delivery_send_preflight(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _send_preflight_report_paths(generated, args)
    max_deliveries = max(1, int(getattr(args, "max_deliveries", 10)))
    include_safe_ready = bool(getattr(args, "include_safe_ready_deliveries", False))
    include_active_resume = bool(getattr(args, "include_active_resume_deliveries", False))
    auto_authorize_approved = bool(getattr(args, "auto_authorize_approved_deliveries", False))
    approved_rows = _approved_delivery_rows(conn, max_deliveries)
    remaining = max(0, max_deliveries - len(approved_rows))
    safe_ready_rows = _ready_delivery_rows(conn, remaining or max_deliveries) if include_safe_ready else []
    remaining = max(0, max_deliveries - len(approved_rows) - len(safe_ready_rows))
    active_resume_rows = (
        _active_resume_delivery_rows(conn, generated, remaining or max_deliveries) if include_active_resume else []
    )
    send_packets: list[dict[str, Any]] = []
    blocked_deliveries: list[dict[str, Any]] = []
    for row in approved_rows:
        packet, blocked = _send_preflight_packet(
            row,
            send_authority=APPROVED_THREAD_DELIVERY_AUTHORITY,
            auto_wake_authorized=auto_authorize_approved,
        )
        if packet:
            send_packets.append(packet)
        if blocked:
            blocked_deliveries.append(blocked)
    for row in safe_ready_rows:
        packet, blocked = _send_preflight_packet(
            row,
            send_authority=SAFE_LOCAL_AUTO_WAKE_AUTHORITY,
            auto_wake_authorized=True,
        )
        if packet:
            send_packets.append(packet)
        if blocked:
            blocked_deliveries.append(blocked)
    for row in active_resume_rows:
        packet, blocked = _send_preflight_packet(
            row,
            send_authority=SAFE_LOCAL_AUTO_WAKE_AUTHORITY,
            auto_wake_authorized=True,
        )
        if packet:
            send_packets.append(packet)
        if blocked:
            blocked_deliveries.append(blocked)
    counts = {
        "approved_deliveries_seen": len(approved_rows),
        "send_packets_ready": len(send_packets),
        "blocked_missing_prompt": sum(
            1 for item in blocked_deliveries if item.get("reason") in {"missing_prompt_path", "prompt_file_not_found"}
        ),
    }
    if include_safe_ready:
        counts.update(
            {
                "safe_ready_deliveries_seen": len(safe_ready_rows),
                "active_resume_deliveries_seen": len(active_resume_rows),
                "auto_wake_packets_ready": sum(
                    1 for item in send_packets if item.get("auto_wake_authorized") is True
                ),
                "blocked_auto_wake_safety": sum(
                    1
                    for item in blocked_deliveries
                    if item.get("reason")
                    not in {"missing_prompt_path", "prompt_file_not_found"}
                ),
            }
        )
    status = _send_preflight_status(counts)
    payload = {
        "schema_version": SEND_PREFLIGHT_SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "counts": counts,
        "send_packets": send_packets,
        "blocked_deliveries": blocked_deliveries,
        "next_action": _send_preflight_next_action(status),
        "zero_side_effect_boundary": _zero_side_effect_boundary(),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_send_preflight_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_send_preflight_run(conn, payload, json_path, md_path)
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


def apply_lane_runtime_thread_delivery_approval_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = apply_lane_runtime_thread_delivery_approval_signal(conn, args)
    print(
        json.dumps(
            {
                "ok": payload["ok"],
                "status": payload["status"],
                "reason": payload.get("reason"),
                "delivery_id": payload.get("delivery_id"),
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
            },
            indent=2,
        )
    )


def write_lane_runtime_thread_delivery_send_preflight_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_lane_runtime_thread_delivery_send_preflight(conn, args)
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


def write_lane_runtime_thread_delivery_approval_drafts_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_lane_runtime_thread_delivery_approval_drafts(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "draft_dir": payload["draft_dir"],
            },
            indent=2,
        )
    )


def promote_lane_runtime_thread_delivery_approval_draft_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = promote_lane_runtime_thread_delivery_approval_draft(conn, args)
    print(
        json.dumps(
            {
                "ok": payload["ok"],
                "status": payload["status"],
                "reason": payload.get("reason"),
                "delivery_id": payload.get("delivery_id"),
                "active_signal_path": payload.get("active_signal_path"),
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
            },
            indent=2,
        )
    )


__all__ = [
    "apply_lane_runtime_thread_delivery_approval_cli",
    "apply_lane_runtime_thread_delivery_approval_signal",
    "count_active_resume_thread_deliveries",
    "promote_lane_runtime_thread_delivery_approval_draft",
    "promote_lane_runtime_thread_delivery_approval_draft_cli",
    "record_lane_runtime_thread_delivery_cli",
    "record_lane_runtime_thread_delivery_receipt",
    "write_lane_runtime_thread_delivery_approval_drafts",
    "write_lane_runtime_thread_delivery_approval_drafts_cli",
    "write_lane_runtime_thread_delivery_outbox",
    "write_lane_runtime_thread_delivery_outbox_cli",
    "write_lane_runtime_thread_delivery_send_preflight",
    "write_lane_runtime_thread_delivery_send_preflight_cli",
]
