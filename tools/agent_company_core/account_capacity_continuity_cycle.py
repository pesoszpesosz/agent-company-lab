"""Run one local account-capacity continuity cycle."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .account_capacity_lease_reconcile import reconcile_account_capacity_leases
from .account_capacity_refresh_monitor import DEFAULT_SIGNAL_DIR, write_account_capacity_refresh_monitor
from .account_capacity_refresh_signal import apply_account_capacity_refresh_signal
from .ceo_state_packet import write_ceo_state_packet_bundle
from .continuity_watchdog_snapshot import write_continuity_watchdog_snapshot_bundle
from .io import now_utc, parse_utc
from .lane_runtime_activation_plan import build_lane_runtime_activation_plan
from .lane_runtime_dispatch_drain import drain_lane_runtime_dispatch_plan
from .lane_runtime_expired_delivery_reconcile import reconcile_expired_lane_runtime_deliveries
from .lane_runtime_superseded_delivery_reconcile import reconcile_superseded_lane_runtime_deliveries
from .lane_runtime_governance_keepalive import write_lane_runtime_governance_keepalive
from .lane_runtime_thread_delivery import (
    apply_lane_runtime_thread_delivery_approval_signal,
    count_active_resume_thread_deliveries,
    write_lane_runtime_thread_delivery_outbox,
    write_lane_runtime_thread_delivery_send_preflight,
)
from .paths import REPORTS_DIR
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "account_capacity_continuity_cycle.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
DEFAULT_THREAD_DELIVERY_APPROVAL_DIR = Path("state") / "thread-delivery-approvals"


def _date_fragment(generated_utc: str) -> str:
    return generated_utc[:10].replace("-", "")


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path, Path]:
    day = _date_fragment(generated_utc)
    json_path = Path(
        getattr(args, "json_path", None) or REPORTS_DIR / f"account-capacity-continuity-cycle-v1-{day}.json"
    )
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"account-capacity-continuity-cycle-v1-{day}.md")
    work_dir = Path(getattr(args, "work_dir", None) or REPORTS_DIR / f"account-capacity-continuity-cycle-v1-{day}")
    return json_path, md_path, work_dir


def _ns(**kwargs: Any) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)


def _step_paths(work_dir: Path, step: str) -> tuple[str, str]:
    return str(work_dir / f"{step}.md"), str(work_dir / f"{step}.json")


def _substep(payload: dict[str, Any] | None, status: str = "skipped", reason: str | None = None) -> dict[str, Any]:
    if payload is None:
        item: dict[str, Any] = {"status": status}
        if reason:
            item["reason"] = reason
        return item
    return {
        "status": payload.get("status"),
        "counts": payload.get("counts", {}),
        "json_path": payload.get("json_path"),
        "md_path": payload.get("md_path"),
    }


def _load_candidate_signal(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict):
        return None
    if str(payload.get("status") or "").strip() != "usable":
        return None
    if not str(payload.get("session_id") or "").strip():
        return None
    if not str(payload.get("observed_utc") or "").strip():
        return None
    return payload


def _auto_refresh_signal_path(args: argparse.Namespace) -> str | None:
    if getattr(args, "refresh_signal", None):
        return None
    if not getattr(args, "auto_apply_ready_refresh_signal", False):
        return None
    signal_dir = Path(getattr(args, "refresh_signal_dir", None) or DEFAULT_SIGNAL_DIR)
    if not signal_dir.exists():
        return None
    candidates: list[tuple[str, str]] = []
    for path in signal_dir.glob("*.json"):
        if not path.is_file():
            continue
        payload = _load_candidate_signal(path)
        if not payload:
            continue
        candidates.append((str(payload.get("observed_utc") or ""), str(path)))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def _self_observed_capacity_session(conn: sqlite3.Connection, args: argparse.Namespace) -> sqlite3.Row | None:
    requested_session = str(getattr(args, "self_observed_capacity_session_id", "") or "").strip()
    if requested_session:
        return conn.execute(
            """
            SELECT session_id, surface, status, concurrency_limit, active_lease_count
            FROM account_capacity_sessions
            WHERE session_id = ?
              AND surface = 'codex'
              AND status IN ('cooling_down', 'needs_restore')
              AND active_lease_count < concurrency_limit
            """,
            (requested_session,),
        ).fetchone()
    return conn.execute(
        """
        SELECT session_id, surface, status, concurrency_limit, active_lease_count
        FROM account_capacity_sessions
        WHERE surface = 'codex'
          AND status IN ('cooling_down', 'needs_restore')
          AND active_lease_count < concurrency_limit
        ORDER BY concurrency_limit DESC, session_id ASC
        LIMIT 1
        """
    ).fetchone()


def _write_self_observed_refresh_signal(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
) -> str | None:
    if getattr(args, "refresh_signal", None):
        return None
    if not getattr(args, "auto_apply_ready_refresh_signal", False):
        return None
    if not getattr(args, "self_observed_codex_capacity_refresh", False):
        return None
    row = _self_observed_capacity_session(conn, args)
    if row is None:
        return None
    signal_dir = Path(getattr(args, "refresh_signal_dir", None) or DEFAULT_SIGNAL_DIR)
    signal_dir.mkdir(parents=True, exist_ok=True)
    session_id = str(row["session_id"])
    path = signal_dir / f"{safe_id_fragment(session_id, 90)}-usable.json"
    day = generated_utc[:10].replace("-", "")
    payload = {
        "signal_id": f"self-observed-refresh-signal-{safe_id_fragment(session_id, 80)}-{day}",
        "session_id": session_id,
        "observed_utc": generated_utc,
        "status": "usable",
        "source": "codex_goal_restore_observed",
        "evidence": (
            "CEO goal/heartbeat restore is executing inside Codex after account/session availability returned; "
            "no credential, token, cookie, password, API key, or OTP is stored."
        ),
        "boundary": (
            "Local capacity signal only. This does not store credentials, start browsers, send thread messages, "
            "publish, submit, spend, trade, call external APIs, or contact anyone."
        ),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(path)


def _load_candidate_thread_delivery_approval(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict):
        return None
    if str(payload.get("decision") or "").strip() not in {"send_approved", "keep_parked"}:
        return None
    if not str(payload.get("delivery_id") or "").strip():
        return None
    if not str(payload.get("thread_id_for_tool") or "").strip():
        return None
    if not str(payload.get("operator") or "").strip():
        return None
    return payload


def _auto_thread_delivery_approval_signal_path(args: argparse.Namespace) -> str | None:
    if getattr(args, "thread_delivery_approval_signal", None):
        return None
    if not getattr(args, "auto_apply_ready_thread_delivery_approval", False):
        return None
    approval_dir = Path(getattr(args, "thread_delivery_approval_dir", None) or DEFAULT_THREAD_DELIVERY_APPROVAL_DIR)
    if not approval_dir.exists():
        return None
    candidates: list[tuple[str, str]] = []
    for path in approval_dir.glob("*.json"):
        if not path.is_file():
            continue
        payload = _load_candidate_thread_delivery_approval(path)
        if not payload:
            continue
        candidates.append((str(payload.get("approved_utc") or ""), str(path)))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def _run_refresh_signal(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    signal_path: str | None = None,
) -> dict[str, Any] | None:
    signal_path = signal_path or getattr(args, "refresh_signal", None)
    if not signal_path:
        return None
    md_path, json_path = _step_paths(work_dir, "account-capacity-refresh-signal")
    return apply_account_capacity_refresh_signal(
        conn,
        _ns(
            signal_path=signal_path,
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_thread_delivery_approval_signal(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    signal_path: str | None = None,
) -> dict[str, Any] | None:
    signal_path = signal_path or getattr(args, "thread_delivery_approval_signal", None)
    if not signal_path:
        return None
    md_path, json_path = _step_paths(work_dir, "lane-runtime-thread-delivery-approval")
    return apply_lane_runtime_thread_delivery_approval_signal(
        conn,
        _ns(
            approval_signal=signal_path,
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_lease_reconcile(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    step: str,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, step)
    return reconcile_account_capacity_leases(
        conn,
        _ns(
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_expired_delivery_reconcile(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, "lane-runtime-expired-delivery-reconcile")
    return reconcile_expired_lane_runtime_deliveries(
        conn,
        _ns(
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_superseded_delivery_reconcile(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, "lane-runtime-superseded-delivery-reconcile")
    return reconcile_superseded_lane_runtime_deliveries(
        conn,
        _ns(
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_activation_plan(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, "lane-runtime-activation-plan")
    return build_lane_runtime_activation_plan(
        conn,
        _ns(
            policy_snapshot=getattr(args, "policy_snapshot"),
            runtime_supervisor_status=getattr(args, "runtime_supervisor_status", None),
            now_utc=generated_utc,
            max_lanes=getattr(args, "max_lanes", 100),
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_dispatch_drain(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    activation_plan: dict[str, Any],
) -> dict[str, Any] | None:
    if not getattr(args, "drain", False):
        return None
    if not activation_plan.get("dispatch_recommendations"):
        return None
    md_path, json_path = _step_paths(work_dir, "lane-runtime-dispatch-drain")
    return drain_lane_runtime_dispatch_plan(
        conn,
        _ns(
            activation_plan=activation_plan["json_path"],
            now_utc=generated_utc,
            lease_minutes=getattr(args, "lease_minutes", 120),
            executor_agent_id=getattr(args, "executor_agent_id", "account-capacity-continuity-cycle"),
            max_dispatches=getattr(args, "max_dispatches", 5),
            packet_dir=str(work_dir / "dispatch-packets"),
            path=md_path,
            json_path=json_path,
            dry_run=False,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_thread_delivery_outbox(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    drain_payload: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not drain_payload or not drain_payload.get("leased_dispatches"):
        return None
    md_path, json_path = _step_paths(work_dir, "lane-runtime-thread-delivery-outbox")
    return write_lane_runtime_thread_delivery_outbox(
        conn,
        _ns(
            drain_report=drain_payload["json_path"],
            now_utc=generated_utc,
            outbox_dir=str(work_dir / "thread-delivery-outbox"),
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_governance_keepalive(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any] | None:
    if not getattr(args, "auto_wake_local_only_thread_deliveries", False):
        return None
    md_path, json_path = _step_paths(work_dir, "lane-runtime-governance-keepalive")
    return write_lane_runtime_governance_keepalive(
        conn,
        _ns(
            now_utc=generated_utc,
            max_keepalives=max(2, int(getattr(args, "max_dispatches", 5))),
            lease_minutes=min(max(1, int(getattr(args, "lease_minutes", 120))), 30),
            packet_dir=str(work_dir / "governance-keepalive"),
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_thread_delivery_send_preflight(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    delivery_payload: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not getattr(args, "auto_wake_local_only_thread_deliveries", False):
        return None
    active_resume_count = count_active_resume_thread_deliveries(conn, generated_utc)
    if not delivery_payload and not active_resume_count:
        return None
    counts = delivery_payload.get("counts", {}) if delivery_payload and isinstance(delivery_payload.get("counts"), dict) else {}
    if (
        int(counts.get("ready_to_send", 0) or 0) <= 0
        and int(counts.get("send_approved", 0) or 0) <= 0
        and not active_resume_count
    ):
        return None
    md_path, json_path = _step_paths(work_dir, "lane-runtime-thread-delivery-send-preflight")
    ready_or_approved = int(counts.get("ready_to_send", 0) or 0) + int(counts.get("send_approved", 0) or 0)
    return write_lane_runtime_thread_delivery_send_preflight(
        conn,
        _ns(
            now_utc=generated_utc,
            max_deliveries=max(int(getattr(args, "max_dispatches", 5)), ready_or_approved, active_resume_count),
            include_safe_ready_deliveries=True,
            include_active_resume_deliveries=True,
            auto_authorize_approved_deliveries=True,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _normalize_thread_id(thread_id: str | None) -> str:
    return str(thread_id or "").removeprefix("codex-thread:")


def _existing_ready_thread_delivery_outbox(
    conn: sqlite3.Connection,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any] | None:
    rows = conn.execute(
        """
        SELECT d.delivery_id, d.task_id, d.lane_id, d.session_id, d.owner_agent_id, d.owner_thread_id,
               d.packet_path, d.prompt_path, d.status, d.delivered_at, t.lease_expires_at
        FROM lane_runtime_thread_deliveries d
        LEFT JOIN tasks t ON t.task_id = d.task_id
        WHERE d.status IN ('ready_to_send', 'send_approved')
        ORDER BY d.updated_at DESC, d.delivery_id
        """
    ).fetchall()
    if not rows:
        return None
    deliveries = [
        {
            "delivery_id": row["delivery_id"],
            "task_id": row["task_id"],
            "lane_id": row["lane_id"],
            "session_id": row["session_id"],
            "owner_agent_id": row["owner_agent_id"],
            "owner_thread_id": row["owner_thread_id"],
            "thread_id_for_tool": _normalize_thread_id(row["owner_thread_id"]),
            "packet_path": row["packet_path"],
            "prompt_path": row["prompt_path"],
            "lease_expires_at": row["lease_expires_at"],
            "status": row["status"],
            "delivered_at": row["delivered_at"],
        }
        for row in rows
    ]
    counts = {
        "deliveries_seen": len(deliveries),
        "ready_to_send": sum(1 for item in deliveries if item["status"] == "ready_to_send"),
        "send_approved": sum(1 for item in deliveries if item["status"] == "send_approved"),
        "blocked_no_owner_thread": 0,
        "already_delivered": 0,
    }
    status = "ready_to_send" if counts["ready_to_send"] else "approved_to_send"
    md_path, json_path = _step_paths(work_dir, "lane-runtime-thread-delivery-outbox")
    payload = {
        "schema_version": "lane_runtime_thread_delivery_outbox.v1",
        "generated_utc": generated_utc,
        "status": status,
        "counts": counts,
        "deliveries": deliveries,
        "drain_report": None,
        "json_path": json_path,
        "md_path": md_path,
        "outbox_dir": str(work_dir / "thread-delivery-outbox"),
        "next_action": (
            "Review the human-action feed and create a scoped approval signal for ready deliveries."
            if status == "ready_to_send"
            else "An approved local delivery is pending a separately scoped sender action; after sending, record the delivery receipt."
        ),
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
    }
    _write_json(Path(json_path), payload)
    _write_existing_delivery_outbox_md(Path(md_path), payload)
    return payload


def _auto_wake_delivery_ids(send_preflight_payload: dict[str, Any] | None) -> set[str]:
    if not send_preflight_payload:
        return set()
    ids: set[str] = set()
    for item in send_preflight_payload.get("send_packets", []):
        if not isinstance(item, dict):
            continue
        if item.get("auto_wake_authorized") is True:
            delivery_id = str(item.get("delivery_id") or "").strip()
            if delivery_id:
                ids.add(delivery_id)
    return ids


def _filter_human_gate_delivery_outbox(
    delivery_payload: dict[str, Any] | None,
    send_preflight_payload: dict[str, Any] | None,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any] | None:
    auto_wake_ids = _auto_wake_delivery_ids(send_preflight_payload)
    if not delivery_payload or not auto_wake_ids:
        return delivery_payload
    deliveries = [
        item
        for item in delivery_payload.get("deliveries", [])
        if not isinstance(item, dict) or str(item.get("delivery_id") or "") not in auto_wake_ids
    ]
    if len(deliveries) == len(delivery_payload.get("deliveries", [])):
        return delivery_payload
    counts = {
        "deliveries_seen": len(deliveries),
        "ready_to_send": sum(1 for item in deliveries if item.get("status") == "ready_to_send"),
        "send_approved": sum(1 for item in deliveries if item.get("status") == "send_approved"),
        "blocked_no_owner_thread": sum(1 for item in deliveries if item.get("status") == "blocked_no_owner_thread"),
        "already_delivered": sum(1 for item in deliveries if item.get("status") == "already_delivered"),
    }
    status = "ready_to_send" if counts["ready_to_send"] else "approved_to_send" if counts["send_approved"] else "no_delivery_needed"
    md_path, json_path = _step_paths(work_dir, "lane-runtime-thread-delivery-human-gate-outbox")
    payload = {
        **delivery_payload,
        "generated_utc": generated_utc,
        "status": status,
        "counts": counts,
        "deliveries": deliveries,
        "json_path": json_path,
        "md_path": md_path,
        "filtered_auto_wake_delivery_ids": sorted(auto_wake_ids),
        "next_action": (
            "Review remaining human-gated thread deliveries."
            if deliveries
            else "No human-gated thread deliveries remain after safe local auto-wake classification."
        ),
    }
    _write_json(Path(json_path), payload)
    _write_existing_delivery_outbox_md(Path(md_path), payload)
    return payload


def _write_existing_delivery_outbox_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Thread Delivery Outbox v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "Source: existing open delivery rows",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Deliveries",
        "",
        "| Status | Delivery | Thread | Task | Prompt |",
        "| --- | --- | --- | --- | --- |",
    ]
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
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This report rediscovers existing local delivery rows only. It does not send thread messages, start workers, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _run_watchdog(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, "continuity-watchdog-snapshot")
    return write_continuity_watchdog_snapshot_bundle(
        conn,
        _ns(
            now_utc=generated_utc,
            stale_after_minutes=getattr(args, "stale_after_minutes", 60),
            cadence_minutes=getattr(args, "cadence_minutes", 15),
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_capacity_refresh_monitor(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    cycle_json_path: Path,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, "account-capacity-refresh-monitor")
    return write_account_capacity_refresh_monitor(
        conn,
        _ns(
            continuity_cycle=str(cycle_json_path),
            refresh_signal_dir=getattr(args, "refresh_signal_dir", None),
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _run_ceo_state(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
    capacity_refresh_monitor: dict[str, Any] | None = None,
    delivery_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    md_path, json_path = _step_paths(work_dir, "ceo-state-packet")
    human_md_path = work_dir / "human-action-feed.md"
    human_json_path = work_dir / "human-action-feed.json"
    return write_ceo_state_packet_bundle(
        conn,
        _ns(
            now_utc=generated_utc,
            path=md_path,
            json_path=json_path,
            human_action_path=str(human_md_path),
            human_action_json_path=str(human_json_path),
            capacity_refresh_monitor=(
                capacity_refresh_monitor.get("json_path") if capacity_refresh_monitor else None
            ),
            thread_delivery_outbox=(
                delivery_payload.get("json_path") if delivery_payload else None
            ),
            open_task_limit=getattr(args, "open_task_limit", 10),
            dispatch_limit=getattr(args, "dispatch_limit", 10),
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _safe_parse_utc(value: str | None):
    try:
        return parse_utc(value)
    except ValueError:
        return None


def _thread_delivery_lease_counts(delivery_payload: dict[str, Any] | None) -> dict[str, int]:
    counts = {"active": 0, "expired": 0, "unknown": 0}
    if not delivery_payload:
        return counts
    generated = _safe_parse_utc(str(delivery_payload.get("generated_utc") or ""))
    for item in delivery_payload.get("deliveries", []):
        if item.get("status") not in {"ready_to_send", "send_approved"}:
            continue
        expires = _safe_parse_utc(str(item.get("lease_expires_at") or ""))
        if not generated or not expires:
            counts["unknown"] += 1
        elif expires <= generated:
            counts["expired"] += 1
        else:
            counts["active"] += 1
    return counts


def _counts(
    refresh_payload: dict[str, Any] | None,
    thread_delivery_approval_payload: dict[str, Any] | None,
    expired_delivery_reconcile_payload: dict[str, Any] | None,
    superseded_delivery_reconcile_payload: dict[str, Any] | None,
    governance_keepalive_payload: dict[str, Any] | None,
    activation_payload: dict[str, Any],
    drain_payload: dict[str, Any] | None,
    delivery_payload: dict[str, Any] | None,
    thread_delivery_send_preflight_payload: dict[str, Any] | None,
    watchdog_payload: dict[str, Any],
    capacity_refresh_monitor: dict[str, Any] | None = None,
) -> dict[str, int]:
    refresh_counts = refresh_payload.get("counts", {}) if refresh_payload else {}
    thread_delivery_approval_applied = (
        1
        if thread_delivery_approval_payload
        and thread_delivery_approval_payload.get("ok") is True
        and thread_delivery_approval_payload.get("status") in {"send_approved", "send_approval_parked"}
        else 0
    )
    activation_counts = activation_payload.get("counts", {})
    expired_delivery_counts = (
        expired_delivery_reconcile_payload.get("counts", {}) if expired_delivery_reconcile_payload else {}
    )
    superseded_delivery_counts = (
        superseded_delivery_reconcile_payload.get("counts", {}) if superseded_delivery_reconcile_payload else {}
    )
    governance_keepalive_counts = governance_keepalive_payload.get("counts", {}) if governance_keepalive_payload else {}
    drain_counts = drain_payload.get("counts", {}) if drain_payload else {}
    delivery_counts = delivery_payload.get("counts", {}) if delivery_payload else {}
    send_preflight_counts = (
        thread_delivery_send_preflight_payload.get("counts", {}) if thread_delivery_send_preflight_payload else {}
    )
    monitor_counts = capacity_refresh_monitor.get("counts", {}) if capacity_refresh_monitor else {}
    delivery_lease_counts = _thread_delivery_lease_counts(delivery_payload)
    return {
        "refresh_signals_applied": int(refresh_counts.get("sessions_available", 0)),
        "thread_delivery_approvals_applied": thread_delivery_approval_applied,
        "dispatch_recommendations": int(activation_counts.get("dispatch_recommendations", 0)),
        "eligible_task_candidates": int(activation_counts.get("eligible_task_candidates", 0)),
        "available_capacity": int(activation_counts.get("available_capacity", 0)),
        "overdue_capacity_sessions": int(activation_counts.get("overdue_capacity_sessions", 0)),
        "runtime_blocked_lanes": int(activation_counts.get("runtime_blocked_lanes", 0)),
        "lanes_pending_capacity": int(activation_counts.get("lanes_pending_capacity", 0)),
        "ready_refresh_signals": int(monitor_counts.get("ready_refresh_signals", 0)),
        "required_capacity_refresh_actions": int(monitor_counts.get("required_human_actions", 0)),
        "expired_ready_deliveries_parked": int(expired_delivery_counts.get("deliveries_parked", 0)),
        "expired_delivery_task_leases_released": int(expired_delivery_counts.get("task_leases_released", 0)),
        "expired_delivery_tasks_requeued": int(expired_delivery_counts.get("tasks_requeued", 0)),
        "superseded_deliveries_parked": int(superseded_delivery_counts.get("deliveries_parked", 0)),
        "superseded_delivery_task_leases_released": int(
            superseded_delivery_counts.get("task_leases_released", 0)
        ),
        "superseded_delivery_tasks_requeued": int(superseded_delivery_counts.get("tasks_requeued", 0)),
        "superseded_delivery_tasks_closed_as_superseded": int(
            superseded_delivery_counts.get("tasks_closed_as_superseded", 0)
        ),
        "governance_keepalives_created": int(governance_keepalive_counts.get("keepalives_created", 0)),
        "governance_keepalive_due_lanes": int(governance_keepalive_counts.get("due_lanes", 0)),
        "leased_dispatches": int(drain_counts.get("leased_dispatches", 0)),
        "ready_thread_deliveries": int(delivery_counts.get("ready_to_send", 0)),
        "approved_thread_deliveries": int(delivery_counts.get("send_approved", 0)),
        "blocked_thread_deliveries": int(delivery_counts.get("blocked_no_owner_thread", 0)),
        "thread_delivery_send_packets_ready": int(send_preflight_counts.get("send_packets_ready", 0)),
        "safe_auto_wake_thread_deliveries": int(send_preflight_counts.get("auto_wake_packets_ready", 0)),
        "active_resume_thread_deliveries": int(send_preflight_counts.get("active_resume_deliveries_seen", 0)),
        "blocked_thread_delivery_send_preflight": int(send_preflight_counts.get("blocked_missing_prompt", 0))
        + int(send_preflight_counts.get("blocked_auto_wake_safety", 0)),
        "active_thread_delivery_leases": delivery_lease_counts["active"],
        "expired_thread_delivery_leases": delivery_lease_counts["expired"],
        "unknown_thread_delivery_leases": delivery_lease_counts["unknown"],
        "watchdog_restore_actions": len(watchdog_payload.get("restore_actions", [])),
        "thread_messages_sent": 0,
    }


def _status(
    activation_payload: dict[str, Any],
    governance_keepalive_payload: dict[str, Any] | None,
    drain_payload: dict[str, Any] | None,
    delivery_payload: dict[str, Any] | None,
    thread_delivery_send_preflight_payload: dict[str, Any] | None,
    watchdog_payload: dict[str, Any],
    capacity_refresh_monitor: dict[str, Any] | None = None,
) -> str:
    if (
        thread_delivery_send_preflight_payload
        and thread_delivery_send_preflight_payload.get("status") == "auto_wake_sends_ready"
    ):
        return "auto_wake_thread_delivery_ready"
    if governance_keepalive_payload and governance_keepalive_payload.get("status") == "keepalives_ready_to_send":
        return "governance_keepalive_ready"
    if delivery_payload and delivery_payload.get("status") == "ready_to_send":
        return "delivery_outbox_ready"
    if delivery_payload and delivery_payload.get("status") == "approved_to_send":
        return "approved_thread_delivery_pending"
    if drain_payload and drain_payload.get("counts", {}).get("leased_dispatches", 0):
        return "dispatch_leased"
    if capacity_refresh_monitor and capacity_refresh_monitor.get("status") == "refresh_signal_ready":
        return "refresh_signal_ready"
    if activation_payload.get("status") == "dispatch_recommended":
        return "dispatch_ready_planning_only"
    if activation_payload.get("status") == "pending_capacity":
        return "pending_capacity"
    if int(activation_payload.get("counts", {}).get("runtime_blocked_lanes", 0)):
        if activation_payload.get("status") == "runtime_blocked":
            return "runtime_blocked"
        return "monitoring_gated_lanes"
    if watchdog_payload.get("status") == "restore_ready":
        return "restore_ready"
    return "monitoring"


def _next_action(
    status: str,
    activation_payload: dict[str, Any],
    capacity_refresh_monitor: dict[str, Any] | None = None,
) -> str:
    if status == "auto_wake_thread_delivery_ready":
        return "Send the safe local auto-wake packets with codex_app.send_message_to_thread, then record delivery receipts."
    if status == "governance_keepalive_ready":
        return "Send the safe always-on governance keepalive packets, then record delivery receipts."
    if status == "delivery_outbox_ready":
        return "Review the human-action feed and create a scoped approval signal for ready thread-delivery prompts."
    if status == "approved_thread_delivery_pending":
        return "Run a separately scoped sender for the approved delivery, then record its delivery receipt."
    if status == "dispatch_leased":
        return "Write or inspect the local delivery outbox before contacting owner threads."
    if status == "refresh_signal_ready":
        return (
            capacity_refresh_monitor or {}
        ).get(
            "next_action",
            "Apply the scoped refresh signal through the continuity cycle, then drain only capacity-eligible work.",
        )
    if status == "dispatch_ready_planning_only":
        return "Rerun this cycle with --drain when the recommended local leases should be consumed."
    if status == "pending_capacity":
        if capacity_refresh_monitor and capacity_refresh_monitor.get("status") == "refresh_signal_needed":
            return capacity_refresh_monitor.get("next_action", activation_payload.get("next_action", ""))
        return activation_payload.get(
            "next_action",
            "Wait for a newer usable local refresh signal, then rerun the cycle so capacity can drain queued lane work.",
        )
    if status == "runtime_blocked":
        return "Review the runtime supervisor and human-action feed for blocked lanes; keep them out of dispatch until their gate clears."
    if status == "monitoring_gated_lanes":
        return "Continue restore monitoring; gated lanes stay parked until scoped approval or a safe local trigger appears."
    if status == "restore_ready":
        return "Review watchdog restore actions and route bounded local repair packets."
    if int(activation_payload.get("counts", {}).get("runtime_blocked_lanes", 0)):
        return "Review the runtime supervisor and human-action feed for blocked lanes; keep them out of dispatch until their gate clears."
    return "Continue heartbeat cadence; no local dispatch or restore action is required."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Account Capacity Continuity Cycle v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Policy snapshot: `{payload['policy_snapshot']}`",
        f"Runtime supervisor status: `{payload.get('runtime_supervisor_status') or ''}`",
        f"Refresh signal: `{payload.get('refresh_signal') or ''}`",
        f"Refresh signal dir: `{payload.get('refresh_signal_dir') or ''}`",
        f"Drain enabled: `{payload['drain_enabled']}`",
        f"JSON mirror: `{payload['json_path']}`",
        f"Work dir: `{payload['work_dir']}`",
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
            "## Substeps",
            "",
            "| Step | Status | JSON |",
            "| --- | --- | --- |",
        ]
    )
    for key, item in payload["substeps"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{key}`",
                    f"`{item.get('status')}`",
                    md_cell(item.get("json_path") or "", 120),
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
            "This cycle applies local refresh signals, reconciles local capacity counters, writes local plans, optionally leases local tasks, and writes local delivery outbox files. It does not send thread messages, start workers, open browsers, approve service requests, call APIs, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = _date_fragment(ts)
    task_id = f"task-account-capacity-continuity-cycle-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Run account capacity continuity cycle', 'complete', 99, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"account-capacity-continuity-cycle:{day}",
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
            f"artifact-account-capacity-continuity-cycle-json-{day}",
            "account_capacity_continuity_cycle_json",
            json_path,
            "Machine-readable account capacity continuity cycle result.",
        ),
        (
            f"artifact-account-capacity-continuity-cycle-md-{day}",
            "account_capacity_continuity_cycle",
            md_path,
            "Human-readable account capacity continuity cycle result.",
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


def run_account_capacity_continuity_cycle(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path, work_dir = _report_paths(generated, args)
    work_dir.mkdir(parents=True, exist_ok=True)

    self_observed_signal_path = _write_self_observed_refresh_signal(conn, args, generated)
    auto_signal_path = _auto_refresh_signal_path(args)
    effective_refresh_signal = getattr(args, "refresh_signal", None) or self_observed_signal_path or auto_signal_path
    refresh_payload = _run_refresh_signal(conn, args, generated, work_dir, effective_refresh_signal)
    pre_reconcile_payload = _run_lease_reconcile(conn, args, generated, work_dir, "account-capacity-lease-reconcile-pre")
    expired_delivery_reconcile_payload = _run_expired_delivery_reconcile(conn, args, generated, work_dir)
    superseded_delivery_reconcile_payload = _run_superseded_delivery_reconcile(conn, args, generated, work_dir)
    delivery_cleanup_reconcile_payload = _run_lease_reconcile(
        conn,
        args,
        generated,
        work_dir,
        "account-capacity-lease-reconcile-after-delivery-cleanup",
    )
    activation_payload = _run_activation_plan(conn, args, generated, work_dir)
    drain_payload = _run_dispatch_drain(conn, args, generated, work_dir, activation_payload)
    delivery_payload = _run_thread_delivery_outbox(conn, args, generated, work_dir, drain_payload)
    governance_keepalive_payload = _run_governance_keepalive(conn, args, generated, work_dir)
    if delivery_payload is None:
        delivery_payload = _existing_ready_thread_delivery_outbox(conn, generated, work_dir)
    post_reconcile_payload = (
        _run_lease_reconcile(conn, args, generated, work_dir, "account-capacity-lease-reconcile-post")
        if drain_payload
        else None
    )
    watchdog_payload = _run_watchdog(conn, args, generated, work_dir)
    auto_thread_delivery_approval_path = _auto_thread_delivery_approval_signal_path(args)
    effective_thread_delivery_approval_signal = (
        getattr(args, "thread_delivery_approval_signal", None) or auto_thread_delivery_approval_path
    )
    thread_delivery_approval_payload = _run_thread_delivery_approval_signal(
        conn,
        args,
        generated,
        work_dir,
        effective_thread_delivery_approval_signal,
    )
    if thread_delivery_approval_payload and thread_delivery_approval_payload.get("ok"):
        delivery_payload = _existing_ready_thread_delivery_outbox(conn, generated, work_dir)
    if governance_keepalive_payload and int(
        governance_keepalive_payload.get("counts", {}).get("keepalives_created", 0) or 0
    ):
        delivery_payload = _existing_ready_thread_delivery_outbox(conn, generated, work_dir)
    thread_delivery_send_preflight_payload = _run_thread_delivery_send_preflight(
        conn,
        args,
        generated,
        work_dir,
        delivery_payload,
    )
    preview_counts = _counts(
        refresh_payload,
        thread_delivery_approval_payload,
        expired_delivery_reconcile_payload,
        superseded_delivery_reconcile_payload,
        governance_keepalive_payload,
        activation_payload,
        drain_payload,
        delivery_payload,
        thread_delivery_send_preflight_payload,
        watchdog_payload,
    )
    preview_status = _status(
        activation_payload,
        governance_keepalive_payload,
        drain_payload,
        delivery_payload,
        thread_delivery_send_preflight_payload,
        watchdog_payload,
    )
    preview_payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": preview_status,
        "policy_snapshot": str(getattr(args, "policy_snapshot")),
        "runtime_supervisor_status": getattr(args, "runtime_supervisor_status", None),
        "refresh_signal": effective_refresh_signal,
        "refresh_signal_dir": getattr(args, "refresh_signal_dir", None),
        "self_observed_refresh_signal": self_observed_signal_path,
        "thread_delivery_approval_signal": effective_thread_delivery_approval_signal,
        "thread_delivery_approval_dir": getattr(args, "thread_delivery_approval_dir", None),
        "auto_applied_refresh_signal": (
            self_observed_signal_path or auto_signal_path
            if refresh_payload and int(refresh_payload.get("counts", {}).get("sessions_available", 0))
            else None
        ),
        "auto_applied_thread_delivery_approval": (
            auto_thread_delivery_approval_path
            if thread_delivery_approval_payload and thread_delivery_approval_payload.get("ok")
            else None
        ),
        "counts": preview_counts,
        "json_path": str(json_path),
        "md_path": str(md_path),
        "work_dir": str(work_dir),
    }
    _write_json(json_path, preview_payload)
    capacity_refresh_monitor = _run_capacity_refresh_monitor(conn, args, generated, work_dir, json_path)
    human_gate_delivery_payload = _filter_human_gate_delivery_outbox(
        delivery_payload,
        thread_delivery_send_preflight_payload,
        generated,
        work_dir,
    )
    ceo_payload = _run_ceo_state(
        conn,
        args,
        generated,
        work_dir,
        capacity_refresh_monitor,
        human_gate_delivery_payload,
    )

    status = _status(
        activation_payload,
        governance_keepalive_payload,
        drain_payload,
        delivery_payload,
        thread_delivery_send_preflight_payload,
        watchdog_payload,
        capacity_refresh_monitor,
    )
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "policy_snapshot": str(getattr(args, "policy_snapshot")),
        "runtime_supervisor_status": getattr(args, "runtime_supervisor_status", None),
        "refresh_signal": effective_refresh_signal,
        "refresh_signal_dir": getattr(args, "refresh_signal_dir", None),
        "self_observed_refresh_signal": self_observed_signal_path,
        "thread_delivery_approval_signal": effective_thread_delivery_approval_signal,
        "thread_delivery_approval_dir": getattr(args, "thread_delivery_approval_dir", None),
        "thread_delivery_send_preflight": (
            thread_delivery_send_preflight_payload.get("json_path")
            if thread_delivery_send_preflight_payload
            else None
        ),
        "auto_applied_refresh_signal": (
            self_observed_signal_path or auto_signal_path
            if refresh_payload and int(refresh_payload.get("counts", {}).get("sessions_available", 0))
            else None
        ),
        "auto_applied_thread_delivery_approval": (
            auto_thread_delivery_approval_path
            if thread_delivery_approval_payload and thread_delivery_approval_payload.get("ok")
            else None
        ),
        "drain_enabled": bool(getattr(args, "drain", False)),
        "max_lanes": int(getattr(args, "max_lanes", 100)),
        "max_dispatches": int(getattr(args, "max_dispatches", 5)),
        "substeps": {
            "refresh_signal": _substep(refresh_payload, reason="no_refresh_signal_provided"),
            "thread_delivery_approval": _substep(
                thread_delivery_approval_payload,
                reason="no_thread_delivery_approval_signal_provided",
            ),
            "lease_reconcile_pre": _substep(pre_reconcile_payload),
            "expired_delivery_reconcile": _substep(expired_delivery_reconcile_payload),
            "superseded_delivery_reconcile": _substep(superseded_delivery_reconcile_payload),
            "lease_reconcile_after_delivery_cleanup": _substep(delivery_cleanup_reconcile_payload),
            "governance_keepalive": _substep(
                governance_keepalive_payload,
                reason="auto_wake_local_only_thread_deliveries_not_enabled",
            ),
            "activation_plan": _substep(activation_payload),
            "dispatch_drain": _substep(
                drain_payload,
                reason=(
                    "drain_flag_not_set"
                    if not getattr(args, "drain", False)
                    else "no_dispatch_recommendations"
                ),
            ),
            "thread_delivery_outbox": _substep(delivery_payload, reason="no_leased_dispatches"),
            "thread_delivery_send_preflight": _substep(
                thread_delivery_send_preflight_payload,
                reason="auto_wake_local_only_thread_deliveries_not_enabled_or_no_delivery",
            ),
            "thread_delivery_human_gate_outbox": _substep(
                human_gate_delivery_payload if human_gate_delivery_payload is not delivery_payload else None,
                reason="no_auto_wake_filter_applied",
            ),
            "lease_reconcile_post": _substep(post_reconcile_payload, reason="no_drain_payload"),
            "watchdog_snapshot": _substep(watchdog_payload),
            "capacity_refresh_monitor": _substep(capacity_refresh_monitor),
            "ceo_state_packet": {
                "status": ceo_payload.get("status"),
                "json_path": ceo_payload.get("json_path"),
                "md_path": ceo_payload.get("md_path"),
                "counts": ceo_payload.get("company_counts", {}),
            },
        },
        "counts": _counts(
            refresh_payload,
            thread_delivery_approval_payload,
            expired_delivery_reconcile_payload,
            superseded_delivery_reconcile_payload,
            governance_keepalive_payload,
            activation_payload,
            drain_payload,
            delivery_payload,
            thread_delivery_send_preflight_payload,
            watchdog_payload,
            capacity_refresh_monitor,
        ),
        "next_action": _next_action(status, activation_payload, capacity_refresh_monitor),
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
        "work_dir": str(work_dir),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def run_account_capacity_continuity_cycle_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = run_account_capacity_continuity_cycle(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "next_action": payload["next_action"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "work_dir": payload["work_dir"],
            },
            indent=2,
        )
    )


__all__ = [
    "run_account_capacity_continuity_cycle",
    "run_account_capacity_continuity_cycle_cli",
]
