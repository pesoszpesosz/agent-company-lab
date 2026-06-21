"""Write per-owner continuity handoff packets from open owner-response tasks."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_watchdog_owner_handoff_packets.v1"
DEFAULT_JSON = REPORTS_DIR / "continuity-watchdog-owner-handoff-packets-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "continuity-watchdog-owner-handoff-packets-v1-20260621.md"
DEFAULT_PACKET_DIR = REPORTS_DIR / "continuity-owner-handoffs-v1-20260621"
TASK_ID = "task-continuity-watchdog-owner-handoff-packets-v1-20260621"
TRACE_ID = "trace-continuity-watchdog-owner-handoff-packets-v1-20260621"
AI_RESOURCES_LANE = "ai_resources_lab"
WATCHDOG_AGENT = "continuity-watchdog-worker-20260621"
TERMINAL_STATUSES = {"complete", "completed", "cancelled", "parked", "retired"}
UUID_LIKE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)


def _load_open_tasks(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT
          t.task_id,
          t.lane_id,
          t.title,
          t.status,
          t.priority,
          t.owner_agent_id,
          t.duplicate_key,
          t.evidence_required,
          t.next_action,
          t.created_at,
          t.updated_at,
          a.role_id,
          a.department_id AS owner_department_id,
          a.status AS owner_status,
          a.thread_id AS agent_thread_id,
          l.owner_thread_id AS lane_owner_thread_id,
          l.department AS lane_department,
          l.status AS lane_status
        FROM tasks t
        LEFT JOIN agents a ON a.agent_id = t.owner_agent_id
        LEFT JOIN lanes l ON l.lane_id = t.lane_id
        WHERE t.duplicate_key LIKE 'continuity-owner-response-task:%'
          AND t.status NOT IN ({})
        ORDER BY t.priority DESC, t.owner_agent_id, t.lane_id, t.task_id
        """.format(",".join("?" for _ in TERMINAL_STATUSES)),
        tuple(sorted(TERMINAL_STATUSES)),
    ).fetchall()
    return [dict(row) for row in rows]


def _response_type(task: dict[str, Any]) -> str:
    duplicate_key = str(task.get("duplicate_key") or "")
    prefix = "continuity-owner-response-task:"
    if not duplicate_key.startswith(prefix):
        return "unknown"
    remainder = duplicate_key[len(prefix) :]
    return remainder.split(":", 1)[0] if ":" in remainder else remainder


def _target_id(task: dict[str, Any]) -> str:
    duplicate_key = str(task.get("duplicate_key") or "")
    prefix = "continuity-owner-response-task:"
    if not duplicate_key.startswith(prefix):
        return str(task.get("task_id") or "")
    remainder = duplicate_key[len(prefix) :]
    return remainder.split(":", 1)[1] if ":" in remainder else str(task.get("task_id") or "")


def _owner_thread_id(tasks: list[dict[str, Any]]) -> str | None:
    for key in ("agent_thread_id", "lane_owner_thread_id"):
        for task in tasks:
            value = task.get(key)
            if value and str(value).startswith("codex-thread:"):
                return str(value)
    for key in ("agent_thread_id", "lane_owner_thread_id"):
        for task in tasks:
            value = task.get(key)
            if value:
                return str(value)
    return None


def _dispatch_mode(thread_id: str | None) -> str:
    if not thread_id:
        return "missing_thread_escalate_to_ai_resources"
    if thread_id.startswith("codex-thread:"):
        return "send_to_live_codex_thread"
    if UUID_LIKE.match(thread_id):
        return "send_to_existing_codex_thread"
    if thread_id.startswith("codex-current-ceo-thread"):
        return "route_through_ceo_or_premium_router_placeholder"
    return "manual_thread_resolution_required"


def _acceptance_criteria(task: dict[str, Any]) -> list[str]:
    response_type = _response_type(task)
    lane_id = str(task.get("lane_id") or "")
    criteria = [
        f"Name source task `{task['task_id']}` and lane `{lane_id}`.",
        "Cite the provided evidence path or state why it is stale or missing.",
        "Write one local report/artifact and register it in the control plane.",
        "Do not create a duplicate worker; evolve, park, merge, or escalate with evidence.",
    ]
    if response_type == "owner_selection_or_park_required":
        criteria.extend(
            [
                "Choose existing owner, park with revisit condition, or retire with rationale.",
                "Do not mutate lane ownership from the handoff packet.",
            ]
        )
    elif response_type == "acknowledgement_response_required":
        criteria.append("Acknowledge the customer objective in a compact owner response artifact.")
    elif response_type == "lane_goal_response_required":
        criteria.append("Submit the current lane goal, nearest money proof, and next local evidence step.")
    return criteria


def _stop_gates() -> list[str]:
    return [
        "no external side effects",
        "no browser/session/account action",
        "no public action/submission/message",
        "no payment/wallet/trade/order",
        "no model/API/MCP/tool spend",
        "no service request approval/start",
        "no lane ownership mutation",
        "no duplicate worker creation",
    ]


def _packet_name(owner_agent_id: str) -> str:
    return f"continuity-owner-handoff-{safe_id_fragment(owner_agent_id, 90)}.md"


def _owner_packet(owner_agent_id: str, tasks: list[dict[str, Any]], packet_dir: Path) -> dict[str, Any]:
    thread_id = _owner_thread_id(tasks)
    packet_path = packet_dir / _packet_name(owner_agent_id)
    items = []
    for task in tasks:
        items.append(
            {
                "task_id": task["task_id"],
                "lane_id": task["lane_id"],
                "response_type": _response_type(task),
                "target_id": _target_id(task),
                "priority": task["priority"],
                "status": task["status"],
                "duplicate_key": task.get("duplicate_key"),
                "evidence_required": task.get("evidence_required") or "",
                "next_action": task.get("next_action") or "",
                "acceptance_criteria": _acceptance_criteria(task),
                "stop_gates": _stop_gates(),
            }
        )
    return {
        "owner_agent_id": owner_agent_id,
        "owner_role_id": tasks[0].get("role_id") or "",
        "owner_department_id": tasks[0].get("owner_department_id") or "",
        "owner_status": tasks[0].get("owner_status") or "missing_agent_row",
        "owner_thread_id": thread_id or "",
        "dispatch_mode": _dispatch_mode(thread_id),
        "packet_path": str(packet_path),
        "task_count": len(items),
        "tasks": items,
    }


def _counts(packets: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {
        "owner_packets": len(packets),
        "open_dispatch_tasks": sum(packet["task_count"] for packet in packets),
    }
    for packet in packets:
        counts[packet["dispatch_mode"]] = counts.get(packet["dispatch_mode"], 0) + 1
        for task in packet["tasks"]:
            key = str(task["response_type"])
            counts[key] = counts.get(key, 0) + 1
    return counts


def _write_owner_packet(path: Path, packet: dict[str, Any], generated_utc: str) -> None:
    lines = [
        f"# Continuity Owner Handoff - {packet['owner_agent_id']}",
        "",
        f"Generated UTC: {generated_utc}",
        f"Owner: `{packet['owner_agent_id']}`",
        f"Role: `{packet['owner_role_id']}`",
        f"Department: `{packet['owner_department_id']}`",
        f"Owner status: `{packet['owner_status']}`",
        f"Thread: `{packet['owner_thread_id'] or 'missing'}`",
        f"Dispatch mode: `{packet['dispatch_mode']}`",
        "",
        "## Tasks",
        "",
    ]
    for task in packet["tasks"]:
        lines.extend(
            [
                f"### {task['task_id']}",
                "",
                f"- Lane: `{task['lane_id']}`",
                f"- Response type: `{task['response_type']}`",
                f"- Target: `{task['target_id']}`",
                f"- Priority: `{task['priority']}`",
                f"- Status: `{task['status']}`",
                f"- Evidence: `{task['evidence_required']}`",
                f"- Next action: {task['next_action']}",
                "",
                "Acceptance criteria:",
            ]
        )
        lines.extend(f"- {item}" for item in task["acceptance_criteria"])
        lines.extend(["", "Stop gates:"])
        lines.extend(f"- {item}" for item in task["stop_gates"])
        lines.append("")
    lines.extend(
        [
            "## Boundary",
            "",
            "This handoff is local and report-only. It does not mutate source tasks, lane ownership, service requests, browser/account state, public surfaces, wallets, payments, trades, submissions, APIs, model spend, or external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Watchdog Owner Handoff Packets V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Packet directory: `{payload['packet_dir']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Counts",
        "",
        "| Count | Value |",
        "| --- | ---: |",
    ]
    for key, value in sorted(payload["counts"].items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Owner Packets",
            "",
            "| Owner | Thread | Dispatch Mode | Tasks | Packet |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for packet in payload["owner_packets"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(packet["owner_agent_id"], 120),
                    md_cell(packet.get("owner_thread_id") or "missing", 100),
                    f"`{packet['dispatch_mode']}`",
                    str(packet["task_count"]),
                    md_cell(packet["packet_path"], 160),
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
            "This command writes local packet files, reports, and audit rows only. It does not send thread messages, start workers, mutate source continuity tasks, assign lane ownership, approve service requests, open browsers, create accounts, publish, submit, trade, spend, call APIs, or contact external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _clear_generated_owner_packets(packet_dir: Path) -> None:
    if not packet_dir.exists():
        return
    for path in packet_dir.glob("continuity-owner-handoff-*.md"):
        if path.is_file():
            path.unlink()


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write continuity owner handoff packets v1', 'complete', 95, ?, ?, ?, ?, ?, ?, ?, ?)
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
            TASK_ID,
            AI_RESOURCES_LANE,
            WATCHDOG_AGENT,
            "continuity-watchdog-owner-handoff-packets:v1",
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    artifacts = [
        (
            "artifact-continuity-watchdog-owner-handoff-packets-v1-json-20260621",
            "continuity_owner_handoff_packets_json",
            json_path,
            "Machine-readable continuity owner handoff packet index.",
        ),
        (
            "artifact-continuity-watchdog-owner-handoff-packets-v1-md-20260621",
            "continuity_owner_handoff_packets_markdown",
            md_path,
            "Human-readable continuity owner handoff packet index.",
        ),
    ]
    for packet in payload["owner_packets"]:
        artifacts.append(
            (
                f"artifact-continuity-owner-handoff-{safe_id_fragment(packet['owner_agent_id'], 120)}-20260621",
                "continuity_owner_handoff_packet",
                Path(packet["packet_path"]),
                f"Owner handoff packet for {packet['owner_agent_id']}.",
            )
        )
    for artifact_id, kind, path, notes in artifacts:
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
            (artifact_id, AI_RESOURCES_LANE, TASK_ID, kind, str(path), sha256_file(path), notes, ts),
        )
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_owner_handoff_packets_written', ?, ?, ?, ?, ?, ?)
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
            "trace-event-continuity-watchdog-owner-handoff-packets-v1-20260621",
            TRACE_ID,
            AI_RESOURCES_LANE,
            TASK_ID,
            WATCHDOG_AGENT,
            ts,
            "continuity_watchdog_owner_handoff_packets_v1",
            f"Wrote {payload['counts']['owner_packets']} owner handoff packets for {payload['counts']['open_dispatch_tasks']} open continuity dispatch tasks.",
            json.dumps({"counts": payload["counts"], "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY}, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-continuity-watchdog-owner-handoff-packets-v1-20260621', ?, ?, 'continuity_owner_handoff_packets', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, payload["status"], str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_continuity_watchdog_owner_handoff_packets(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    packet_dir = Path(getattr(args, "packet_dir", None) or DEFAULT_PACKET_DIR)
    tasks = _load_open_tasks(conn)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in tasks:
        grouped[str(task.get("owner_agent_id") or "missing_owner_agent")].append(task)
    packets = [_owner_packet(owner, grouped[owner], packet_dir) for owner in sorted(grouped)]
    _clear_generated_owner_packets(packet_dir)
    for packet in packets:
        _write_owner_packet(Path(packet["packet_path"]), packet, generated)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "owner_handoff_packets_ready" if packets else "no_open_owner_handoffs",
        "packet_dir": str(packet_dir),
        "counts": _counts(packets),
        "owner_packets": packets,
        "next_action": (
            "Send the owner packets to existing Codex owner threads where dispatch_mode allows; route placeholder or missing-thread cases through AI Resources/premium router without creating duplicate workers."
            if packets
            else "No open continuity owner handoffs remain; continue watchdog cadence."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_continuity_watchdog_owner_handoff_packets_cli(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> None:
    payload = write_continuity_watchdog_owner_handoff_packets(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "packet_dir": payload["packet_dir"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
