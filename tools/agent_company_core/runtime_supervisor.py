"""Runtime supervisor for lane threads, capacity, and human gates."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR, ROOT
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import compact_text, md_cell, sha256_file


SCHEMA_VERSION = "worker_runtime_status.v1"
HUMAN_ACTION_SCHEMA_VERSION = "human_action_feed.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"

SURFACE_KEYWORDS = {
    "algora": "Algora",
    "bugcrowd": "Bugcrowd",
    "cantina": "Cantina",
    "drivendata": "DrivenData",
    "dorahacks": "DoraHacks",
    "fiverr": "Fiverr",
    "github": "GitHub",
    "gitcoin": "Gitcoin",
    "gumroad": "Gumroad",
    "hackerone": "HackerOne",
    "kaggle": "Kaggle",
    "kalshi": "Kalshi",
    "lemon squeezy": "Lemon Squeezy",
    "lemonsqueezy": "Lemon Squeezy",
    "opire": "Opire",
    "polar": "Polar",
    "polymarket": "Polymarket",
    "promptbase": "PromptBase",
    "upwork": "Upwork",
    "youtube": "YouTube",
}

HUMAN_GATE_KEYWORDS = (
    "account",
    "approval",
    "approve",
    "browser",
    "checkout",
    "credential",
    "credentials",
    "identity",
    "kyc",
    "listing",
    "log in",
    "login",
    "manual",
    "payout",
    "public",
    "submit",
    "submission",
    "tax",
    "terms",
    "trade",
    "upload",
    "wallet",
)

TASK_BLOCKING_GATE_KEYWORDS = (
    "account access",
    "approval before",
    "before login",
    "billing",
    "checkout",
    "credential",
    "credentials",
    "identity",
    "kyc",
    "legal",
    "log in",
    "login",
    "payment",
    "payout",
    "public action",
    "public listing",
    "submit",
    "submission",
    "tax",
    "terms",
    "trade",
    "upload",
    "wallet",
    "without approval",
)

LOCAL_PREP_ACTION_KEYWORDS = (
    "capture",
    "consume",
    "draft",
    "prepare",
    "review",
    "surface",
    "write",
)

LOCAL_PREP_BOUNDARY_MARKERS = (
    "do not ",
    "keep all work local",
    "keep work local",
    "local only",
    "local-only",
    "no browser side effects",
    "no commitments",
    "without external action",
    "without taking side effects",
)

BLOCKING_SERVICE_GATE_MARKERS = (
    "account_access",
    "billing",
    "credential",
    "identity",
    "kyc",
    "legal",
    "legal_kyc_tax_payment",
    "model_api_call",
    "payment",
    "payout",
    "real_money",
    "requires_user_decision",
    "security_report_submission",
    "signed_in",
    "submission_requires",
    "tax",
    "trade",
    "wallet",
)

STATUS_PRIORITY = [
    "system_error",
    "usage_limited",
    "missing_thread",
    "blocked_by_human_gate",
    "parked_by_capacity",
    "repo_backing_needed",
    "not_loaded",
    "running",
    "idle_ready",
    "external_owned_or_parked",
]


def _date_fragment(generated_utc: str) -> str:
    return generated_utc[:10].replace("-", "")


def _report_paths(generated_utc: str, args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    day = _date_fragment(generated_utc)
    json_path = Path(getattr(args, "json_path", None) or REPORTS_DIR / f"worker-runtime-status-v1-{day}.json")
    md_path = Path(getattr(args, "path", None) or REPORTS_DIR / f"worker-runtime-status-v1-{day}.md")
    human_json_path = Path(
        getattr(args, "human_action_json_path", None) or REPORTS_DIR / f"human-action-feed-runtime-v1-{day}.json"
    )
    human_md_path = Path(
        getattr(args, "human_action_path", None) or REPORTS_DIR / f"human-action-feed-runtime-v1-{day}.md"
    )
    return json_path, md_path, human_json_path, human_md_path


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_thread_snapshot(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [dict(item) for item in payload]
    return [dict(item) for item in payload.get("threads", [])]


def _normalize_thread_id(thread_id: str | None) -> str:
    return str(thread_id or "").removeprefix("codex-thread:")


def _thread_status(thread: dict[str, Any] | None) -> str:
    if not thread:
        return ""
    status = thread.get("status")
    if isinstance(status, dict):
        return str(status.get("type") or "")
    return str(status or "")


def _thread_map(threads: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {_normalize_thread_id(thread.get("id") or thread.get("threadId")): thread for thread in threads}


def _repo_backed(cwd: str | None) -> bool:
    if not cwd:
        return False
    path = Path(cwd)
    if not path.exists():
        return False
    return any((candidate / ".git").exists() for candidate in [path, *path.parents])


def _text_mentions_canonical_root(text: str) -> bool:
    normalized_text = text.replace("\\", "/").lower()
    normalized_root = str(ROOT).replace("\\", "/").lower()
    return normalized_root in normalized_text


def _task_is_canonical_local(task: dict[str, Any]) -> bool:
    text = " ".join(
        str(task.get(key) or "")
        for key in ["task_id", "lane_id", "title", "evidence_required", "next_action", "duplicate_key"]
    )
    return _text_mentions_canonical_root(text)


def _tasks_are_canonical_local(tasks: list[dict[str, Any]]) -> bool:
    return bool(tasks) and all(_task_is_canonical_local(task) for task in tasks)


def _surface_from_text(text: str) -> str:
    lowered = text.lower()
    for keyword, surface in SURFACE_KEYWORDS.items():
        if keyword in lowered:
            return surface
    if any(word in lowered for word in ("marketplace", "platform", "external account", "account access")):
        return "External platform"
    return "External account or platform"


def _has_human_gate_signal(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in HUMAN_GATE_KEYWORDS)


def _is_local_prep_task(text: str) -> bool:
    lowered = text.lower()
    if not any(keyword in lowered for keyword in LOCAL_PREP_ACTION_KEYWORDS):
        return False
    return any(marker in lowered for marker in LOCAL_PREP_BOUNDARY_MARKERS)


def _human_gate_from_task(task: dict[str, Any]) -> dict[str, Any] | None:
    text = " ".join(
        str(task.get(key) or "")
        for key in ["task_id", "lane_id", "title", "evidence_required", "next_action", "duplicate_key"]
    )
    if not _has_human_gate_signal(text):
        return None
    lowered = text.lower()
    external_surface_seen = any(keyword in lowered for keyword in SURFACE_KEYWORDS)
    hard_gate_seen = any(keyword in lowered for keyword in TASK_BLOCKING_GATE_KEYWORDS)
    safety_boundary_only = (
        not external_surface_seen
        and ("do not " in lowered or "no-" in lowered or " no " in lowered)
        and not any(
            phrase in lowered
            for phrase in (
                "account access",
                "approval before",
                "ask the human",
                "explicit approval",
                "human for",
                "provide/confirm",
                "requires user",
                "surface exact",
                "without approval",
            )
        )
    )
    if safety_boundary_only:
        return None
    if not (external_surface_seen or hard_gate_seen):
        return None
    surface = _surface_from_text(text)
    priority = _as_int(task.get("priority"), 50)
    local_prep_only = _is_local_prep_task(text)
    blocking = priority >= 90 and (external_surface_seen or hard_gate_seen) and not local_prep_only
    return {
        "priority": priority,
        "surface": surface,
        "lane_id": task["lane_id"],
        "task_id": task["task_id"],
        "service_request_id": None,
        "blocking": blocking,
        "gate_category": "external_account_or_platform_gate",
        "exact_human_decision": (
            f"Provide/confirm scoped access or approval for {surface}, or keep the task parked with no external action."
        ),
        "why_ai_cannot_safely_do_it": (
            "The task text indicates account access, terms, payout, identity, upload, submission, listing, "
            "checkout, public action, wallet, trade, browser, or credential boundaries."
        ),
        "business_reason": compact_text(task.get("title"), 220) or "Unblock a gated lane task after local prep.",
        "expected_upside": "The lane can resume from local readiness as soon as scoped human approval/access exists.",
        "deadline_or_expiration": "none_detected",
        "source_evidence_path": task.get("evidence_required"),
        "decline_or_ignore_branch": (
            "Keep the lane local/read-only, parked, or queued until an explicit scoped approval exists."
        ),
        "next_action": task.get("next_action"),
    }


def _json_dict(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _surface_from_service_request(row: sqlite3.Row) -> str:
    intake = _json_dict(row["intake_json"])
    surface = str(intake.get("surface") or "").strip()
    if surface:
        return surface
    return _surface_from_text(" ".join(str(row[key] or "") for key in ["request_type", "risk_gate", "requested_action"]))


def _service_request_gates_by_lane(conn: sqlite3.Connection) -> dict[str, list[dict[str, Any]]]:
    rows = conn.execute(
        """
        SELECT request_id, request_type, lane_id, status, risk_gate, requested_action,
               intake_json, artifact_path, created_at
        FROM service_requests
        WHERE status = 'needs_review'
        ORDER BY created_at DESC, request_id
        """
    ).fetchall()
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        lane_id = row["lane_id"]
        if not lane_id:
            continue
        intake = _json_dict(row["intake_json"])
        forbidden = intake.get("forbidden_actions_without_approval")
        if not isinstance(forbidden, list):
            forbidden = []
        request_type = str(row["request_type"] or "").lower()
        risk_gate = str(row["risk_gate"] or "").lower()
        requested_action = str(row["requested_action"] or "").lower()
        control_text = " ".join([request_type, risk_gate, requested_action])
        read_only_catalog_request = risk_gate == "catalog_required_approval_no_external_action"
        blocking = False if read_only_catalog_request else any(
            marker in control_text for marker in BLOCKING_SERVICE_GATE_MARKERS
        )
        priority = 100 if blocking else 60
        gate = {
            "priority": priority,
            "surface": _surface_from_service_request(row),
            "lane_id": lane_id,
            "task_id": None,
            "service_request_id": row["request_id"],
            "blocking": blocking,
            "gate_category": row["risk_gate"] or "external_action_gate",
            "exact_human_decision": f"Approve, reject, or keep parked: {row['requested_action']}",
            "why_ai_cannot_safely_do_it": (
                "The service request is still in needs_review and may cross an account, approval, browser, "
                "public-action, payout, identity, wallet, trade, upload, submission, or terms gate."
            ),
            "business_reason": compact_text(row["requested_action"], 220)
            or "Could unlock gated lane work after local readiness is clear.",
            "expected_upside": "The lane can resume from local readiness as soon as scoped approval/access exists.",
            "deadline_or_expiration": str(intake.get("deadline_or_expiration") or "none_detected"),
            "source_evidence_path": row["artifact_path"],
            "decline_or_ignore_branch": "Keep the work local, parked, or fixture-only until a scoped approval exists.",
            "next_action": row["requested_action"],
            "forbidden_actions_without_approval": [str(item) for item in forbidden],
        }
        grouped.setdefault(lane_id, []).append(gate)
    return grouped


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
        item["available_slots"] = max(0, concurrency_limit - active_lease_count) if item["status"] == "available" else 0
        sessions.append(item)
    return sessions


def _capacity_summary(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    wakeups: list[str] = []
    for session in sessions:
        status_counts[session["status"]] = status_counts.get(session["status"], 0) + 1
        if session.get("status") == "cooling_down" and session.get("resume_after_utc"):
            wakeups.append(str(session["resume_after_utc"]))
    return {
        "sessions_seen": len(sessions),
        "status_counts": status_counts,
        "available_slots": sum(_as_int(session.get("available_slots"), 0) for session in sessions),
        "next_capacity_wakeup_utc": min(wakeups) if wakeups else None,
    }


def _open_tasks_by_lane(conn: sqlite3.Connection, limit: int) -> dict[str, list[dict[str, Any]]]:
    rows = conn.execute(
        """
        SELECT task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
               evidence_required, next_action, created_at, updated_at,
               lease_owner_agent_id, lease_expires_at
        FROM tasks
        WHERE status NOT IN ('complete', 'cancelled')
        ORDER BY priority DESC, updated_at DESC, task_id
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        item = dict(row)
        grouped.setdefault(item["lane_id"], []).append(item)
    return grouped


def _active_lane_rows(conn: sqlite3.Connection, limit: int) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT
              l.lane_id, l.department, l.status AS lane_status, l.owner_agent_id, l.owner_thread_id,
              p.runtime_mode, p.cadence_minutes, p.max_parallel_tasks, p.capacity_class
            FROM lanes l
            LEFT JOIN lane_runtime_policies p ON p.lane_id = l.lane_id
            WHERE l.status = 'active'
            ORDER BY l.lane_id
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    ]


def _classification(
    lane: dict[str, Any],
    thread: dict[str, Any] | None,
    tasks: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    capacity_summary: dict[str, Any],
) -> str:
    thread_status = _thread_status(thread)
    owner_thread_id = _normalize_thread_id(lane.get("owner_thread_id"))
    if lane.get("runtime_mode") == "parked" or lane.get("lane_status") not in {"active", "planned"}:
        return "external_owned_or_parked"
    if thread_status == "systemError":
        return "system_error"
    if thread_status in {"usageLimited", "rateLimited", "quotaExceeded"}:
        return "usage_limited"
    if owner_thread_id and thread is None:
        return "missing_thread"
    if not owner_thread_id:
        return "missing_thread"
    if gates:
        return "blocked_by_human_gate"
    capacity_class = lane.get("capacity_class") or "codex"
    if tasks and capacity_class == "codex" and int(capacity_summary["available_slots"]) <= 0:
        return "parked_by_capacity"
    if thread and not _repo_backed(thread.get("cwd")) and tasks and not _tasks_are_canonical_local(tasks):
        return "repo_backing_needed"
    if thread_status == "notLoaded":
        return "not_loaded"
    if thread_status in {"active", "running", "busy"}:
        return "running"
    return "idle_ready"


def _next_action(runtime_status: str, lane: dict[str, Any], gates: list[dict[str, Any]], cap: dict[str, Any]) -> str:
    if runtime_status == "blocked_by_human_gate":
        surface = gates[0]["surface"] if gates else "external platform"
        return f"Put {surface} access/approval in the human-action feed and keep the lane parked until scoped approval exists."
    if runtime_status == "parked_by_capacity":
        wakeup = cap.get("next_capacity_wakeup_utc")
        suffix = f" after {wakeup}" if wakeup else " when capacity refreshes"
        return f"Do not restore as broken; queue this lane for dispatch{suffix}."
    if runtime_status == "system_error":
        return "Route a bounded restore packet to the continuity watchdog and preserve the latest lane goal context."
    if runtime_status == "usage_limited":
        return "Mark the lane cooling_down, avoid repeated prompts, and resume from queue when refreshed capacity appears."
    if runtime_status == "missing_thread":
        return "Register or recreate the Codex goal thread before assigning more lane work."
    if runtime_status == "repo_backing_needed":
        return "Prefer a repo-backed thread or absolute-path recovery executor before dispatching write-heavy work."
    if runtime_status == "not_loaded":
        return "Keep registered; activate only when policy and capacity recommend dispatch."
    if runtime_status == "running":
        return "Monitor for completion packet, fresh artifact, or stale lease."
    if runtime_status == "external_owned_or_parked":
        return "Leave parked until CEO or AR changes the runtime policy."
    return "Ready for dispatch when a queued task and capacity align."


def _status_rows(
    lanes: list[dict[str, Any]],
    threads_by_id: dict[str, dict[str, Any]],
    tasks_by_lane: dict[str, list[dict[str, Any]]],
    service_gates_by_lane: dict[str, list[dict[str, Any]]],
    capacity_summary: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    all_gates: list[dict[str, Any]] = []
    for lane in lanes:
        lane_id = lane["lane_id"]
        thread_id = _normalize_thread_id(lane.get("owner_thread_id"))
        thread = threads_by_id.get(thread_id)
        tasks = tasks_by_lane.get(lane_id, [])
        gates = [*service_gates_by_lane.get(lane_id, []), *[gate for task in tasks if (gate := _human_gate_from_task(task))]]
        gates.sort(key=lambda item: (-item["priority"], item.get("task_id") or item.get("service_request_id") or ""))
        blocking_gates = [gate for gate in gates if gate.get("blocking")]
        runtime_status = _classification(lane, thread, tasks, blocking_gates, capacity_summary)
        leased_tasks = [task for task in tasks if task.get("lease_owner_agent_id")]
        rows.append(
            {
                "lane_id": lane_id,
                "department": lane["department"],
                "lane_status": lane["lane_status"],
                "runtime_mode": lane.get("runtime_mode") or "unclassified",
                "capacity_class": lane.get("capacity_class") or "codex",
                "owner_agent_id": lane.get("owner_agent_id"),
                "owner_thread_id": lane.get("owner_thread_id"),
                "thread_status": _thread_status(thread) or "missing",
                "repo_backed": _repo_backed(thread.get("cwd")) if thread else False,
                "open_task_count": len(tasks),
                "leased_task_count": len(leased_tasks),
                "human_gate_count": len(blocking_gates),
                "top_task_id": tasks[0]["task_id"] if tasks else None,
                "runtime_status": runtime_status,
                "next_action": _next_action(runtime_status, lane, blocking_gates, capacity_summary),
            }
        )
        all_gates.extend(gates)
    all_gates.sort(key=lambda item: (-item["priority"], item["lane_id"], item["task_id"]))
    return rows, all_gates


def _counts(rows: list[dict[str, Any]], gates: list[dict[str, Any]]) -> dict[str, int]:
    counts = {status: 0 for status in STATUS_PRIORITY}
    for row in rows:
        counts[row["runtime_status"]] = counts.get(row["runtime_status"], 0) + 1
    counts["lanes_seen"] = len(rows)
    counts["human_gate_items"] = len(gates)
    counts["open_tasks_seen"] = sum(int(row["open_task_count"]) for row in rows)
    counts["leased_tasks_seen"] = sum(int(row["leased_task_count"]) for row in rows)
    return counts


def _overall_status(counts: dict[str, int]) -> str:
    attention = [
        "system_error",
        "usage_limited",
        "missing_thread",
        "blocked_by_human_gate",
        "parked_by_capacity",
        "repo_backing_needed",
    ]
    return "attention_required" if any(counts.get(status, 0) for status in attention) else "clear"


def _human_action_feed(
    generated_utc: str,
    gates: list[dict[str, Any]],
    human_json_path: Path,
    human_md_path: Path,
) -> dict[str, Any]:
    required = [gate for gate in gates if gate.get("blocking") and gate["priority"] >= 90]
    optional = [gate for gate in gates if not gate.get("blocking")]
    return {
        "schema_version": HUMAN_ACTION_SCHEMA_VERSION,
        "generated_utc": generated_utc,
        "owner_agent_id": "human-action-desk-worker-20260620",
        "feed_status": "human_gate_action_required" if required else "account_gate_review_available" if gates else "no_immediate_human_action_required_for_local_only_work",
        "required_now": required,
        "account_gate_queue": required,
        "optional_gate_queue": optional,
        "human_ask_required_fields": [
            "surface",
            "exact_human_decision",
            "why_ai_cannot_safely_do_it",
            "business_reason",
            "expected_upside",
            "deadline_or_expiration",
            "gate_category",
            "source_evidence_path",
            "decline_or_ignore_branch",
        ],
        "zero_side_effect_boundary": {
            "user_credentials_requested_in_chat": 0,
            "accounts_created": 0,
            "browser_sessions_started": 0,
            "public_actions_taken": 0,
            "payments_trades_wallets_kyc_actions": 0,
            "service_requests_approved_rejected_assigned_or_started_by_feed": 0,
            "external_side_effects": False,
        },
        "json_path": str(human_json_path),
        "md_path": str(human_md_path),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_human_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Human Action Feed Runtime v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['feed_status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Required Now",
        "",
        "| Surface | Lane | Task | Exact Human Decision | Decline Branch |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in payload["required_now"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item["surface"], 80),
                    f"`{item['lane_id']}`",
                    f"`{item.get('task_id') or item.get('service_request_id') or ''}`",
                    md_cell(item["exact_human_decision"], 220),
                    md_cell(item["decline_or_ignore_branch"], 180),
                ]
            )
            + " |"
        )
    if not payload["required_now"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Account Gate Queue",
            "",
            "| Priority | Surface | Lane | Task | Gate | Next Action |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["account_gate_queue"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item["priority"]),
                    md_cell(item["surface"], 80),
                    f"`{item['lane_id']}`",
                    f"`{item.get('task_id') or item.get('service_request_id') or ''}`",
                    md_cell(item["gate_category"], 90),
                    md_cell(item.get("next_action"), 240),
                ]
            )
            + " |"
        )
    if not payload["account_gate_queue"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Optional Gate Queue",
            "",
            "| Priority | Surface | Lane | Task | Gate | Next Action |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["optional_gate_queue"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item["priority"]),
                    md_cell(item["surface"], 80),
                    f"`{item['lane_id']}`",
                    f"`{item.get('task_id') or item.get('service_request_id') or ''}`",
                    md_cell(item["gate_category"], 90),
                    md_cell(item.get("next_action"), 240),
                ]
            )
            + " |"
        )
    if not payload["optional_gate_queue"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This feed does not request credentials, create accounts, open browsers, take public actions, spend, trade, approve service requests, or start workers.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_status_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Worker Runtime Status v1",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        f"Thread snapshot: `{payload['thread_snapshot']}`",
        "",
        "## Capacity",
        "",
        f"- Available slots: `{payload['capacity_summary']['available_slots']}`",
        f"- Next capacity wakeup: `{payload['capacity_summary']['next_capacity_wakeup_utc'] or 'none'}`",
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
            "## Lane Runtime Statuses",
            "",
            "| Lane | Mode | Thread | Open | Gates | Status | Next Action |",
            "| --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for item in payload["lane_runtime_statuses"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['runtime_mode']}`",
                    f"`{item['thread_status']}`",
                    str(item["open_task_count"]),
                    str(item["human_gate_count"]),
                    f"`{item['runtime_status']}`",
                    md_cell(item["next_action"], 240),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This supervisor reads a supplied Codex thread snapshot and local SQLite state. It writes local reports only; it does not start workers, send thread messages, approve gates, open browsers, create accounts, publish, submit, spend, trade, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _record_run(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    human_feed: dict[str, Any],
    json_path: Path,
    md_path: Path,
    human_json_path: Path,
    human_md_path: Path,
) -> None:
    ts = payload["generated_utc"]
    day = _date_fragment(ts)
    task_id = f"task-worker-runtime-status-v1-{day}"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Refresh worker runtime supervisor status', 'complete', 99, ?, ?, ?, ?, ?, ?, ?, ?)
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
            task_id,
            AI_RESOURCES_LANE,
            AI_RESOURCES_OWNER,
            f"worker-runtime-status:{day}",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    artifact_rows = [
        (f"artifact-worker-runtime-status-json-{day}", "worker_runtime_status_json", json_path, "Machine-readable worker runtime supervisor status."),
        (f"artifact-worker-runtime-status-md-{day}", "worker_runtime_status_markdown", md_path, "Human-readable worker runtime supervisor status."),
        (f"artifact-human-action-feed-runtime-json-{day}", "human_action_feed_runtime_json", human_json_path, "Machine-readable runtime human-action feed."),
        (f"artifact-human-action-feed-runtime-md-{day}", "human_action_feed_runtime_markdown", human_md_path, "Human-readable runtime human-action feed."),
    ]
    for artifact_id, kind, path, notes in artifact_rows:
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
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'worker_runtime_status_refreshed', ?, 'worker_runtime_status_v1', ?, ?, ?, ?)
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
            f"trace-event-worker-runtime-status-v1-{day}",
            f"trace-worker-runtime-status-v1-{day}",
            AI_RESOURCES_LANE,
            task_id,
            AI_RESOURCES_OWNER,
            ts,
            (
                f"Refreshed runtime supervisor with {payload['counts']['lanes_seen']} lanes, "
                f"{payload['counts']['human_gate_items']} human gates, and "
                f"{payload['capacity_summary']['available_slots']} available capacity slots."
            ),
            json.dumps(
                {
                    "status": payload["status"],
                    "counts": payload["counts"],
                    "capacity_summary": payload["capacity_summary"],
                    "human_action_feed_status": human_feed["feed_status"],
                },
                sort_keys=True,
            ),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, 'worker_runtime_status', 'current', 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-worker-runtime-status-v1-{day}",
            AI_RESOURCES_LANE,
            task_id,
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def write_runtime_supervisor_status_bundle(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    lane_limit = _as_int(getattr(args, "lane_limit", 100), 100) or 100
    open_task_limit = _as_int(getattr(args, "open_task_limit", 250), 250) or 250
    thread_snapshot = Path(getattr(args, "thread_snapshot"))
    json_path, md_path, human_json_path, human_md_path = _report_paths(generated, args)

    threads = _load_thread_snapshot(thread_snapshot)
    threads_by_id = _thread_map(threads)
    sessions = _capacity_sessions(conn)
    cap = _capacity_summary(sessions)
    tasks_by_lane = _open_tasks_by_lane(conn, open_task_limit)
    service_gates_by_lane = _service_request_gates_by_lane(conn)
    lane_rows = _active_lane_rows(conn, lane_limit)
    runtime_rows, gates = _status_rows(lane_rows, threads_by_id, tasks_by_lane, service_gates_by_lane, cap)
    counts = _counts(runtime_rows, gates)
    status = _overall_status(counts)
    human_feed = _human_action_feed(generated, gates, human_json_path, human_md_path)
    next_action = (
        "Route required human/account gates to the human desk, recover systemError threads through watchdog, "
        "and keep capacity-blocked lanes queued instead of treating them as broken."
        if status == "attention_required"
        else "Continue normal runtime monitoring and dispatch only through lane policy plus capacity."
    )
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": status,
        "thread_snapshot": str(thread_snapshot),
        "threads_seen": len(threads),
        "capacity_sessions": sessions,
        "capacity_summary": cap,
        "lane_runtime_statuses": runtime_rows,
        "counts": counts,
        "human_action_feed": human_feed,
        "next_action": next_action,
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_status_md(md_path, payload)
    _write_json(human_json_path, human_feed)
    _write_human_md(human_md_path, human_feed)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, human_feed, json_path, md_path, human_json_path, human_md_path)
    return payload


def write_runtime_supervisor_status_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_runtime_supervisor_status_bundle(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "capacity_summary": payload["capacity_summary"],
                "human_action_feed_status": payload["human_action_feed"]["feed_status"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "human_action_json_path": payload["human_action_feed"]["json_path"],
                "human_action_md_path": payload["human_action_feed"]["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
