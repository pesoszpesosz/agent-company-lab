"""Run one local account-capacity continuity cycle."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .account_capacity_lease_reconcile import reconcile_account_capacity_leases
from .account_capacity_refresh_signal import apply_account_capacity_refresh_signal
from .ceo_state_packet import write_ceo_state_packet_bundle
from .continuity_watchdog_snapshot import write_continuity_watchdog_snapshot_bundle
from .io import now_utc
from .lane_runtime_activation_plan import build_lane_runtime_activation_plan
from .lane_runtime_dispatch_drain import drain_lane_runtime_dispatch_plan
from .lane_runtime_thread_delivery import write_lane_runtime_thread_delivery_outbox
from .paths import REPORTS_DIR
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "account_capacity_continuity_cycle.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"


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


def _run_refresh_signal(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
) -> dict[str, Any] | None:
    signal_path = getattr(args, "refresh_signal", None)
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
            max_dispatches=getattr(args, "max_dispatches", 1),
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


def _run_ceo_state(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
    generated_utc: str,
    work_dir: Path,
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
            open_task_limit=getattr(args, "open_task_limit", 10),
            dispatch_limit=getattr(args, "dispatch_limit", 10),
            no_db_record=getattr(args, "no_db_record", False),
        ),
    )


def _counts(
    refresh_payload: dict[str, Any] | None,
    activation_payload: dict[str, Any],
    drain_payload: dict[str, Any] | None,
    delivery_payload: dict[str, Any] | None,
    watchdog_payload: dict[str, Any],
) -> dict[str, int]:
    refresh_counts = refresh_payload.get("counts", {}) if refresh_payload else {}
    activation_counts = activation_payload.get("counts", {})
    drain_counts = drain_payload.get("counts", {}) if drain_payload else {}
    delivery_counts = delivery_payload.get("counts", {}) if delivery_payload else {}
    return {
        "refresh_signals_applied": int(refresh_counts.get("sessions_available", 0)),
        "dispatch_recommendations": int(activation_counts.get("dispatch_recommendations", 0)),
        "eligible_task_candidates": int(activation_counts.get("eligible_task_candidates", 0)),
        "available_capacity": int(activation_counts.get("available_capacity", 0)),
        "leased_dispatches": int(drain_counts.get("leased_dispatches", 0)),
        "ready_thread_deliveries": int(delivery_counts.get("ready_to_send", 0)),
        "blocked_thread_deliveries": int(delivery_counts.get("blocked_no_owner_thread", 0)),
        "watchdog_restore_actions": len(watchdog_payload.get("restore_actions", [])),
        "thread_messages_sent": 0,
    }


def _status(
    activation_payload: dict[str, Any],
    drain_payload: dict[str, Any] | None,
    delivery_payload: dict[str, Any] | None,
    watchdog_payload: dict[str, Any],
) -> str:
    if delivery_payload and delivery_payload.get("status") == "ready_to_send":
        return "delivery_outbox_ready"
    if drain_payload and drain_payload.get("counts", {}).get("leased_dispatches", 0):
        return "dispatch_leased"
    if activation_payload.get("status") == "dispatch_recommended":
        return "dispatch_ready_planning_only"
    if activation_payload.get("status") == "pending_capacity":
        return "pending_capacity"
    if watchdog_payload.get("status") == "restore_ready":
        return "restore_ready"
    return "monitoring"


def _next_action(status: str) -> str:
    if status == "delivery_outbox_ready":
        return "Review the local delivery outbox and send ready prompts only through a separately approved thread-delivery action."
    if status == "dispatch_leased":
        return "Write or inspect the local delivery outbox before contacting owner threads."
    if status == "dispatch_ready_planning_only":
        return "Rerun this cycle with --drain when the recommended local leases should be consumed."
    if status == "pending_capacity":
        return "Wait for a newer usable local refresh signal, then rerun the cycle so capacity can drain queued lane work."
    if status == "restore_ready":
        return "Review watchdog restore actions and route bounded local repair packets."
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
        f"Refresh signal: `{payload.get('refresh_signal') or ''}`",
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

    refresh_payload = _run_refresh_signal(conn, args, generated, work_dir)
    pre_reconcile_payload = _run_lease_reconcile(conn, args, generated, work_dir, "account-capacity-lease-reconcile-pre")
    activation_payload = _run_activation_plan(conn, args, generated, work_dir)
    drain_payload = _run_dispatch_drain(conn, args, generated, work_dir, activation_payload)
    delivery_payload = _run_thread_delivery_outbox(conn, args, generated, work_dir, drain_payload)
    post_reconcile_payload = (
        _run_lease_reconcile(conn, args, generated, work_dir, "account-capacity-lease-reconcile-post")
        if drain_payload
        else None
    )
    watchdog_payload = _run_watchdog(conn, args, generated, work_dir)
    ceo_payload = _run_ceo_state(conn, args, generated, work_dir)

    status = _status(activation_payload, drain_payload, delivery_payload, watchdog_payload)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "policy_snapshot": str(getattr(args, "policy_snapshot")),
        "refresh_signal": getattr(args, "refresh_signal", None),
        "drain_enabled": bool(getattr(args, "drain", False)),
        "max_lanes": int(getattr(args, "max_lanes", 100)),
        "max_dispatches": int(getattr(args, "max_dispatches", 1)),
        "substeps": {
            "refresh_signal": _substep(refresh_payload, reason="no_refresh_signal_provided"),
            "lease_reconcile_pre": _substep(pre_reconcile_payload),
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
            "lease_reconcile_post": _substep(post_reconcile_payload, reason="no_drain_payload"),
            "watchdog_snapshot": _substep(watchdog_payload),
            "ceo_state_packet": {
                "status": ceo_payload.get("status"),
                "json_path": ceo_payload.get("json_path"),
                "md_path": ceo_payload.get("md_path"),
                "counts": ceo_payload.get("company_counts", {}),
            },
        },
        "counts": _counts(refresh_payload, activation_payload, drain_payload, delivery_payload, watchdog_payload),
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
