"""Write compact CEO state packets and human-action feeds."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc, parse_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "ceo_state_packet.v1"
HUMAN_ACTION_SCHEMA_VERSION = "human_action_feed.v1"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
DEFAULT_JSON = REPORTS_DIR / "ceo-state-packet-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ceo-state-packet-v1-20260621.md"
DEFAULT_HUMAN_JSON = REPORTS_DIR / "human-action-feed-v1-20260621.json"
DEFAULT_HUMAN_MD = REPORTS_DIR / "human-action-feed-v1-20260621.md"
PREVIOUS_PACKET = REPORTS_DIR / "ceo-state-packet-v1-20260620.json"


def _date_fragment(generated_utc: str) -> str:
    return generated_utc[:10].replace("-", "")


def _packet_id(generated_utc: str) -> str:
    return f"ceo-state-packet-v1-{_date_fragment(generated_utc)}"


def _task_id(generated_utc: str) -> str:
    return f"task-{_packet_id(generated_utc)}"


def _table_count(conn: sqlite3.Connection, table: str) -> int:
    return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def _company_counts(conn: sqlite3.Connection) -> dict[str, int]:
    return {
        "lanes": _table_count(conn, "lanes"),
        "departments": _table_count(conn, "departments"),
        "roles": _table_count(conn, "roles"),
        "agents": _table_count(conn, "agents"),
        "tasks": _table_count(conn, "tasks"),
        "artifacts": _table_count(conn, "artifacts"),
        "outcomes": _table_count(conn, "outcomes"),
        "trace_events": _table_count(conn, "trace_events"),
        "service_requests": _table_count(conn, "service_requests"),
    }


def _age_minutes(updated_at: str | None, generated_utc: str) -> int | None:
    if not updated_at:
        return None
    updated = parse_utc(updated_at)
    generated = parse_utc(generated_utc)
    if not updated or not generated:
        return None
    return max(0, int((generated - updated).total_seconds() // 60))


def _stale_owner_acknowledgements(conn: sqlite3.Connection, generated_utc: str, limit: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT task_id, lane_id, status, owner_agent_id, updated_at, next_action
        FROM tasks
        WHERE duplicate_key LIKE '%:owner-acknowledgement:%'
          AND status NOT IN ('complete', 'cancelled')
        ORDER BY updated_at, priority DESC
        """
    ).fetchall()
    stale: list[dict[str, Any]] = []
    for row in rows:
        age = _age_minutes(row["updated_at"], generated_utc)
        if age is not None and age >= 60:
            stale.append(
                {
                    "task_id": row["task_id"],
                    "lane_id": row["lane_id"],
                    "status": row["status"],
                    "owner_agent_id": row["owner_agent_id"],
                    "age_minutes": age,
                    "next_action": row["next_action"],
                }
            )
    return stale[:limit]


def _service_request_counts(conn: sqlite3.Connection) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in conn.execute("SELECT status, COUNT(*) AS n FROM service_requests GROUP BY status"):
        counts[row["status"]] = int(row["n"])
    return counts


def _optional_gate_queue(conn: sqlite3.Connection, limit: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT request_id, request_type, lane_id, risk_gate, requested_action, artifact_path, created_at
        FROM service_requests
        WHERE status = 'needs_review'
        ORDER BY created_at DESC, request_id
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    queue: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        queue.append(
            {
                "priority": index,
                "request_id": row["request_id"],
                "request_type": row["request_type"],
                "lane_id": row["lane_id"],
                "gate_category": row["risk_gate"],
                "exact_human_decision": f"Approve, reject, or keep parked: {row['requested_action']}",
                "why_ai_cannot_safely_do_it": "The service request is still in needs_review and may cross an external-action gate.",
                "business_reason": "Could unlock gated work after local readiness is clear.",
                "expected_upside": "Sharper route proof or faster lane validation if approved.",
                "deadline_or_expiration": "none",
                "source_evidence_path": row["artifact_path"],
                "decline_or_ignore_branch": "Keep the work local, parked, or fixture-only until a scoped approval exists.",
            }
        )
    return queue


def _human_action_feed(
    conn: sqlite3.Connection,
    generated_utc: str,
    human_json_path: Path,
    human_md_path: Path,
    limit: int,
) -> dict[str, Any]:
    queue = _optional_gate_queue(conn, limit)
    feed_status = "optional_gate_review_available" if queue else "no_immediate_human_action_required_for_local_only_work"
    return {
        "schema_version": HUMAN_ACTION_SCHEMA_VERSION,
        "generated_utc": generated_utc,
        "owner_agent_id": "human-action-desk-worker-20260620",
        "feed_status": feed_status,
        "service_request_status_counts": _service_request_counts(conn),
        "required_now": [],
        "optional_gate_queue": queue,
        "human_ask_required_fields": [
            "exact_action_requested",
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


def _open_tasks(conn: sqlite3.Connection, limit: int) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT task_id, lane_id, title, status, priority, owner_agent_id, next_action
            FROM tasks
            WHERE status NOT IN ('complete', 'cancelled')
            ORDER BY priority DESC, updated_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    ]


def _active_lanes(conn: sqlite3.Connection, limit: int = 12) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT lane_id, department, owner_agent_id, status
            FROM lanes
            WHERE status = 'active'
            ORDER BY lane_id
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    ]


def _recent_outcomes(conn: sqlite3.Connection, limit: int = 8) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT outcome_id, lane_id, outcome_type, status, realized_usd, evidence, next_action, created_at
            FROM outcomes
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    ]


def _metrics_delta(counts: dict[str, int]) -> dict[str, int | None]:
    empty = {
        "tasks_delta": None,
        "artifacts_delta": None,
        "outcomes_delta": None,
        "trace_events_delta": None,
    }
    if not PREVIOUS_PACKET.exists():
        return empty
    previous = json.loads(PREVIOUS_PACKET.read_text(encoding="utf-8")).get("company_counts", {})
    if any(counts[key] < int(previous.get(key, 0)) for key in ["tasks", "artifacts", "outcomes", "trace_events"]):
        return empty
    return {
        "tasks_delta": counts["tasks"] - int(previous.get("tasks", counts["tasks"])),
        "artifacts_delta": counts["artifacts"] - int(previous.get("artifacts", counts["artifacts"])),
        "outcomes_delta": counts["outcomes"] - int(previous.get("outcomes", counts["outcomes"])),
        "trace_events_delta": counts["trace_events"] - int(previous.get("trace_events", counts["trace_events"])),
    }


def _next_dispatch_queue(open_tasks: list[dict[str, Any]], stale_acks: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for item in stale_acks:
        queue.append(
            {
                "kind": "owner_acknowledgement",
                "task_id": item["task_id"],
                "lane_id": item["lane_id"],
                "next_action": item["next_action"],
            }
        )
    for task in open_tasks:
        queue.append(
            {
                "kind": "open_task",
                "task_id": task["task_id"],
                "lane_id": task["lane_id"],
                "next_action": task["next_action"],
            }
        )
    return queue[:limit]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_human_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Human Action Feed V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Owner: `{payload['owner_agent_id']}`",
        f"Status: `{payload['feed_status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Required Now",
        "",
    ]
    if payload["required_now"]:
        lines.extend(f"- {item}" for item in payload["required_now"])
    else:
        lines.append("No immediate human action is required for local-only company work.")
    lines.extend(
        [
            "",
            "## Optional Gate Queue",
            "",
            "| Priority | Request | Gate | Exact Human Decision | Decline Branch |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    for item in payload["optional_gate_queue"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item["priority"]),
                    f"`{item['request_id']}`",
                    md_cell(item["gate_category"], 80),
                    md_cell(item["exact_human_decision"], 220),
                    md_cell(item["decline_or_ignore_branch"], 180),
                ]
            )
            + " |"
        )
    if not payload["optional_gate_queue"]:
        lines.append("| none |  |  |  |  |")
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


def _write_state_md(path: Path, payload: dict[str, Any]) -> None:
    counts = payload["company_counts"]
    gates = payload["active_blockers_and_gates"]
    lines = [
        "# CEO State Packet V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Packet id: `{payload['packet_id']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Company Counts",
        "",
        "| Table | Count |",
        "| --- | ---: |",
    ]
    for key, value in counts.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Active Blockers And Gates",
            "",
            f"- Service requests needing review: `{gates['service_requests_needing_review']}`",
            f"- Blocked tasks: `{gates['blocked_task_count']}`",
            f"- Stale owner acknowledgements: `{gates['stale_owner_acknowledgement_count']}`",
            "",
            "## Current Decision Batch",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in payload["current_decision_batch"])
    lines.extend(["", "## Next Dispatch Queue", "", "| Kind | Task | Lane | Next Action |", "| --- | --- | --- | --- |"])
    for item in payload["next_dispatch_queue"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item["kind"], 80),
                    f"`{item['task_id']}`",
                    f"`{item['lane_id']}`",
                    md_cell(item.get("next_action"), 220),
                ]
            )
            + " |"
        )
    if not payload["next_dispatch_queue"]:
        lines.append("| none |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is a compact local state summary only. It does not approve service requests, start workers, call models/APIs, open browsers, create accounts, publish, submit, trade, spend, or perform security testing.",
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
    fragment = _date_fragment(ts)
    task_id = _task_id(ts)
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Refresh CEO state packet v1', 'complete', 94, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          title=excluded.title,
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          duplicate_key=excluded.duplicate_key,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            AI_RESOURCES_LANE,
            AI_RESOURCES_OWNER,
            payload["packet_id"],
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    artifact_rows = [
        (f"artifact-ceo-state-packet-v1-json-{fragment}", "ceo_state_packet_json", json_path, "Machine-readable CEO state packet."),
        (f"artifact-ceo-state-packet-v1-md-{fragment}", "ceo_state_packet_markdown", md_path, "Human-readable CEO state packet."),
        (f"artifact-human-action-feed-v1-json-{fragment}", "human_action_feed_json", human_json_path, "Machine-readable human-action feed."),
        (f"artifact-human-action-feed-v1-md-{fragment}", "human_action_feed_markdown", human_md_path, "Human-readable human-action feed."),
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
              notes=excluded.notes
            """,
            (artifact_id, AI_RESOURCES_LANE, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ceo_state_packet_refreshed', ?, 'ceo_state_packet_v1', ?, ?, ?, ?)
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
            f"trace-event-ceo-state-packet-v1-{fragment}",
            f"trace-ceo-state-packet-v1-{fragment}",
            AI_RESOURCES_LANE,
            task_id,
            AI_RESOURCES_OWNER,
            ts,
            f"Refreshed CEO state packet with {len(payload['next_dispatch_queue'])} dispatch candidates and {len(human_feed['optional_gate_queue'])} optional human gate decisions.",
            json.dumps(
                {
                    "company_counts": payload["company_counts"],
                    "active_blockers_and_gates": payload["active_blockers_and_gates"],
                    "human_action_feed_status": human_feed["feed_status"],
                    "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
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
        VALUES(?, ?, ?, 'ceo_state_packet', 'current', 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-ceo-state-packet-v1-{fragment}",
            AI_RESOURCES_LANE,
            task_id,
            str(md_path),
            payload["next_action"],
            ts,
        ),
    )
    conn.commit()


def write_ceo_state_packet_bundle(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    open_task_limit = int(getattr(args, "open_task_limit", 10))
    dispatch_limit = int(getattr(args, "dispatch_limit", 10))
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    human_json_path = Path(getattr(args, "human_action_json_path", None) or DEFAULT_HUMAN_JSON)
    human_md_path = Path(getattr(args, "human_action_path", None) or DEFAULT_HUMAN_MD)

    counts = _company_counts(conn)
    open_tasks = _open_tasks(conn, open_task_limit)
    stale_acks = _stale_owner_acknowledgements(conn, generated, dispatch_limit)
    service_counts = _service_request_counts(conn)
    human_feed = _human_action_feed(conn, generated, human_json_path, human_md_path, dispatch_limit)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "packet_id": _packet_id(generated),
        "generated_utc": generated,
        "status": "current_local_state_packet",
        "company_counts": counts,
        "current_decision_batch": [
            "owner_acknowledgement_pressure",
            "goal_evolver_review",
            "ceo_state_packet",
            "human_action_feed",
            "manager_dispatch_queue",
        ],
        "active_blockers_and_gates": {
            "service_requests_needing_review": service_counts.get("needs_review", 0),
            "blocked_task_count": int(
                conn.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('blocked', 'needs_review')").fetchone()[0]
            ),
            "stale_owner_acknowledgement_count": len(stale_acks),
            "required_human_action_count": len(human_feed["required_now"]),
            "optional_gate_queue_count": len(human_feed["optional_gate_queue"]),
        },
        "top_promoted_lanes": _active_lanes(conn),
        "killed_lanes_and_reasons": [],
        "human_action_feed": human_feed,
        "ai_resources_candidate_shortlist": [
            "ceo_state_packet_v1",
            "human_action_feed_v1",
            "goal_evolver_review_v1",
        ],
        "open_tasks": open_tasks,
        "recent_outcomes": _recent_outcomes(conn),
        "next_dispatch_queue": _next_dispatch_queue(open_tasks, stale_acks, dispatch_limit),
        "metrics_since_last_packet": _metrics_delta(counts),
        "next_action": "Use this compact packet as the CEO context capsule; dispatch only the listed local next actions or route exact human gates through the human-action feed.",
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_state_md(md_path, payload)
    _write_json(human_json_path, human_feed)
    _write_human_md(human_md_path, human_feed)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, human_feed, json_path, md_path, human_json_path, human_md_path)
    return payload


def write_ceo_state_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_ceo_state_packet_bundle(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "packet_id": payload["packet_id"],
                "status": payload["status"],
                "company_counts": payload["company_counts"],
                "active_blockers_and_gates": payload["active_blockers_and_gates"],
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
