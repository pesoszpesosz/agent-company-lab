"""Local lane runtime activation planning."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "lane_runtime_activation_plan.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
VALID_RUNTIME_MODES = {"always_on", "on_demand", "scheduled", "parked"}
DISPATCHABLE_MODES = {"always_on", "on_demand", "scheduled"}
MODE_PRIORITY = {"always_on": 0, "on_demand": 1, "scheduled": 2}


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path]:
    day = generated_utc[:10].replace("-", "")
    json_path = Path(getattr(args, "json_path", None) or REPORTS_DIR / f"lane-runtime-activation-plan-v1-{day}.json")
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"lane-runtime-activation-plan-v1-{day}.md")
    return json_path, md_path


def _as_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(0, parsed)


def _json_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _normalize_policy(policy: dict[str, Any]) -> dict[str, Any]:
    lane_id = str(policy.get("lane_id") or "").strip()
    if not lane_id:
        raise SystemExit("Every lane runtime policy requires lane_id")
    runtime_mode = str(policy.get("runtime_mode") or "on_demand").strip()
    if runtime_mode not in VALID_RUNTIME_MODES:
        raise SystemExit(f"Invalid runtime_mode for {lane_id}: {runtime_mode}")
    cadence = policy.get("cadence_minutes")
    cadence_minutes = _as_int(cadence, 0) or None
    max_parallel_tasks = _as_int(policy.get("max_parallel_tasks"), 1) or 1
    return {
        "lane_id": lane_id,
        "runtime_mode": runtime_mode,
        "cadence_minutes": cadence_minutes,
        "max_parallel_tasks": max_parallel_tasks,
        "capacity_class": policy.get("capacity_class") or "codex",
        "activation_triggers": _json_list(policy.get("activation_triggers")),
        "park_conditions": _json_list(policy.get("park_conditions")),
        "notes": policy.get("notes"),
    }


def _load_policies(path: Path, max_lanes: int) -> list[dict[str, Any]]:
    payload = load_json(path)
    if isinstance(payload, list):
        policies = payload
    else:
        policies = payload.get("policies", [])
    return [_normalize_policy(dict(policy)) for policy in policies[:max_lanes]]


def _upsert_policies(conn: sqlite3.Connection, policies: list[dict[str, Any]], generated_utc: str) -> None:
    for policy in policies:
        conn.execute(
            """
            INSERT INTO lane_runtime_policies(
              lane_id, runtime_mode, cadence_minutes, max_parallel_tasks,
              capacity_class, activation_triggers_json, park_conditions_json,
              notes, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(lane_id) DO UPDATE SET
              runtime_mode=excluded.runtime_mode,
              cadence_minutes=excluded.cadence_minutes,
              max_parallel_tasks=excluded.max_parallel_tasks,
              capacity_class=excluded.capacity_class,
              activation_triggers_json=excluded.activation_triggers_json,
              park_conditions_json=excluded.park_conditions_json,
              notes=excluded.notes,
              updated_at=excluded.updated_at
            """,
            (
                policy["lane_id"],
                policy["runtime_mode"],
                policy["cadence_minutes"],
                policy["max_parallel_tasks"],
                policy["capacity_class"],
                json.dumps(policy["activation_triggers"], sort_keys=True),
                json.dumps(policy["park_conditions"], sort_keys=True),
                policy["notes"],
                generated_utc,
                generated_utc,
            ),
        )
    conn.commit()


def _capacity_sessions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT session_id, surface, account_label, status, concurrency_limit,
               active_lease_count, resume_after_utc, last_refresh_utc, last_error, notes
        FROM account_capacity_sessions
        ORDER BY session_id
        """
    ).fetchall()
    sessions: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        concurrency_limit = _as_int(item.get("concurrency_limit"), 1)
        active_lease_count = _as_int(item.get("active_lease_count"), 0)
        item["concurrency_limit"] = concurrency_limit
        item["active_lease_count"] = active_lease_count
        item["available_slots"] = (
            max(0, concurrency_limit - active_lease_count) if item.get("status") == "available" else 0
        )
        sessions.append(item)
    return sessions


def _slot_sequence(sessions: list[dict[str, Any]]) -> list[str]:
    slots: list[str] = []
    for session in sessions:
        slots.extend([session["session_id"]] * session["available_slots"])
    return slots


def _next_wakeup(sessions: list[dict[str, Any]]) -> str | None:
    wakeups = [
        str(session["resume_after_utc"])
        for session in sessions
        if session.get("status") == "cooling_down" and session.get("resume_after_utc")
    ]
    return min(wakeups) if wakeups else None


def _tasks_by_lane(conn: sqlite3.Connection, lane_ids: list[str]) -> dict[str, list[dict[str, Any]]]:
    if not lane_ids:
        return {}
    placeholders = ",".join("?" for _ in lane_ids)
    rows = conn.execute(
        f"""
        SELECT
          t.task_id, t.lane_id, t.title, t.priority, t.owner_agent_id,
          t.evidence_required, t.next_action, t.created_at, t.updated_at,
          l.owner_thread_id, l.status AS lane_status
        FROM tasks t
        LEFT JOIN lanes l ON l.lane_id = t.lane_id
        WHERE t.status = 'new'
          AND t.lease_owner_agent_id IS NULL
          AND t.lane_id IN ({placeholders})
        ORDER BY t.lane_id ASC, t.priority DESC, t.created_at ASC, t.task_id ASC
        """,
        tuple(lane_ids),
    ).fetchall()
    grouped: dict[str, list[dict[str, Any]]] = {lane_id: [] for lane_id in lane_ids}
    for row in rows:
        grouped.setdefault(row["lane_id"], []).append(dict(row))
    return grouped


def _lane_exists(conn: sqlite3.Connection, lane_ids: list[str]) -> set[str]:
    if not lane_ids:
        return set()
    placeholders = ",".join("?" for _ in lane_ids)
    rows = conn.execute(f"SELECT lane_id FROM lanes WHERE lane_id IN ({placeholders})", tuple(lane_ids)).fetchall()
    return {row["lane_id"] for row in rows}


def _idle_action(policy: dict[str, Any], exists: bool) -> str:
    if not exists:
        return "missing_lane_policy"
    mode = policy["runtime_mode"]
    if mode == "parked":
        return "parked_no_dispatch"
    if mode == "always_on":
        return "ensure_seed_or_monitor"
    if mode == "scheduled":
        return "monitor_cadence"
    return "monitor_for_trigger"


def _build_lane_states_and_candidates(
    conn: sqlite3.Connection,
    policies: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    lane_ids = [policy["lane_id"] for policy in policies]
    existing_lanes = _lane_exists(conn, lane_ids)
    grouped_tasks = _tasks_by_lane(conn, lane_ids)
    lane_states: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for policy_index, policy in enumerate(policies):
        lane_id = policy["lane_id"]
        tasks = grouped_tasks.get(lane_id, [])
        exists = lane_id in existing_lanes
        selected_tasks = tasks[: policy["max_parallel_tasks"]]
        if exists and policy["runtime_mode"] in DISPATCHABLE_MODES and selected_tasks:
            action = "eligible_for_dispatch"
            for task in selected_tasks:
                candidates.append(
                    {
                        "policy_index": policy_index,
                        "runtime_mode": policy["runtime_mode"],
                        "mode_priority": MODE_PRIORITY[policy["runtime_mode"]],
                        "task": task,
                        "policy": policy,
                    }
                )
        else:
            action = _idle_action(policy, exists)
        lane_states.append(
            {
                "lane_id": lane_id,
                "runtime_mode": policy["runtime_mode"],
                "cadence_minutes": policy["cadence_minutes"],
                "max_parallel_tasks": policy["max_parallel_tasks"],
                "capacity_class": policy["capacity_class"],
                "activation_triggers": policy["activation_triggers"],
                "park_conditions": policy["park_conditions"],
                "open_task_count": len(tasks),
                "selected_task_count": len(selected_tasks),
                "recommended_action": action,
            }
        )
    candidates.sort(
        key=lambda item: (
            item["mode_priority"],
            item["policy_index"],
            -int(item["task"]["priority"]),
            item["task"]["created_at"],
            item["task"]["task_id"],
        )
    )
    return lane_states, candidates


def _build_recommendations(
    lane_states: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    slots: list[str],
) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []
    recommended_lanes: set[str] = set()
    for candidate, session_id in zip(candidates, slots):
        task = candidate["task"]
        policy = candidate["policy"]
        recommended_lanes.add(policy["lane_id"])
        recommendations.append(
            {
                "session_id": session_id,
                "lane_id": policy["lane_id"],
                "runtime_mode": policy["runtime_mode"],
                "task_id": task["task_id"],
                "priority": task["priority"],
                "owner_agent_id": task["owner_agent_id"],
                "owner_thread_id": task["owner_thread_id"],
                "evidence_required": task["evidence_required"],
                "next_action": task["next_action"],
                "recommended_action": "lease_then_dispatch_with_runtime_and_capacity_guard",
            }
        )
    for state in lane_states:
        if state["recommended_action"] != "eligible_for_dispatch":
            continue
        state["recommended_action"] = "dispatch_recommended" if state["lane_id"] in recommended_lanes else "pending_capacity"
    return recommendations


def _status(recommendations: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> str:
    if recommendations:
        return "dispatch_recommended"
    if candidates:
        return "pending_capacity"
    return "monitoring"


def _next_action(status: str, next_wakeup_utc: str | None) -> str:
    if status == "dispatch_recommended":
        return "Lease recommended tasks through a scoped local command, then dispatch only within account capacity."
    if status == "pending_capacity":
        suffix = f" at {next_wakeup_utc}" if next_wakeup_utc else ""
        return f"Wait for account/session capacity{suffix}; keep lanes marked pending instead of restoring them as broken."
    return "Continue monitoring always-on lanes for seed gaps and on-demand lanes for activation triggers."


def _counts(
    policies: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    lane_states: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "policies_seen": len(policies),
        "always_on_lanes": sum(1 for policy in policies if policy["runtime_mode"] == "always_on"),
        "on_demand_lanes": sum(1 for policy in policies if policy["runtime_mode"] == "on_demand"),
        "scheduled_lanes": sum(1 for policy in policies if policy["runtime_mode"] == "scheduled"),
        "parked_lanes": sum(1 for policy in policies if policy["runtime_mode"] == "parked"),
        "available_capacity": sum(session["available_slots"] for session in sessions),
        "eligible_task_candidates": len(candidates),
        "dispatch_recommendations": len(recommendations),
        "lanes_pending_capacity": sum(1 for state in lane_states if state["recommended_action"] == "pending_capacity"),
        "lanes_monitoring": sum(1 for state in lane_states if state["recommended_action"].startswith("monitor")),
        "lanes_parked": sum(1 for state in lane_states if state["recommended_action"] == "parked_no_dispatch"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Lane Runtime Activation Plan v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        f"Policy snapshot: `{payload['policy_snapshot']}`",
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
            "## Lane Activation States",
            "",
            "| Lane | Mode | Open Tasks | Max Parallel | Action |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for state in payload["lane_activation_states"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{state['lane_id']}`",
                    f"`{state['runtime_mode']}`",
                    str(state["open_task_count"]),
                    str(state["max_parallel_tasks"]),
                    f"`{state['recommended_action']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Dispatch Recommendations",
            "",
            "| Session | Lane | Mode | Task | Priority | Owner Thread | Action |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    if payload["dispatch_recommendations"]:
        for item in payload["dispatch_recommendations"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['session_id']}`",
                        f"`{item['lane_id']}`",
                        f"`{item['runtime_mode']}`",
                        f"`{item['task_id']}`",
                        str(item["priority"]),
                        md_cell(item.get("owner_thread_id") or "", 120),
                        f"`{item['recommended_action']}`",
                    ]
                )
                + " |"
            )
    else:
        lines.append("| none |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
            "## Boundary",
            "",
            "This planner writes local runtime policy state and activation recommendations only. It does not mutate task leases, send thread messages, start workers, approve service requests, open browsers, call APIs, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    day = ts[:10].replace("-", "")
    task_id = f"task-lane-runtime-activation-plan-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write lane runtime activation plan', 'complete', 96, ?, ?, ?, ?, ?, ?, ?, ?)
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
            f"lane-runtime-activation-plan:{day}",
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
            f"artifact-lane-runtime-activation-plan-json-{day}",
            "lane_runtime_activation_plan_json",
            json_path,
            "Machine-readable local lane runtime activation plan.",
        ),
        (
            f"artifact-lane-runtime-activation-plan-md-{day}",
            "lane_runtime_activation_plan",
            md_path,
            "Human-readable local lane runtime activation plan.",
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


def build_lane_runtime_activation_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path, md_path = _report_paths(generated, args)
    snapshot_path = Path(getattr(args, "policy_snapshot"))
    max_lanes = _as_int(getattr(args, "max_lanes", 100), 100) or 100
    policies = _load_policies(snapshot_path, max_lanes)
    _upsert_policies(conn, policies, generated)
    sessions = _capacity_sessions(conn)
    slots = _slot_sequence(sessions)
    lane_states, candidates = _build_lane_states_and_candidates(conn, policies)
    recommendations = _build_recommendations(lane_states, candidates, slots)
    next_wakeup_utc = _next_wakeup(sessions)
    status = _status(recommendations, candidates)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "db": str(DB_PATH),
        "status": status,
        "policy_snapshot": str(snapshot_path),
        "max_lanes": max_lanes,
        "capacity_sessions": sessions,
        "lane_activation_states": lane_states,
        "dispatch_recommendations": recommendations,
        "next_wakeup_utc": next_wakeup_utc,
        "counts": _counts(policies, sessions, lane_states, candidates, recommendations),
        "next_action": _next_action(status, next_wakeup_utc),
        "zero_side_effect_boundary": {
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


def write_lane_runtime_activation_plan_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = build_lane_runtime_activation_plan(conn, args)
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
    "build_lane_runtime_activation_plan",
    "write_lane_runtime_activation_plan_cli",
]
