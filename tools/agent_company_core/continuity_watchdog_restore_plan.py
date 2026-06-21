"""Continuity watchdog restore packets derived from a snapshot report."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .continuity_watchdog_snapshot import DEFAULT_JSON as DEFAULT_SNAPSHOT_JSON
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_watchdog_restore_plan.v1"
DEFAULT_JSON = REPORTS_DIR / "continuity-watchdog-restore-plan-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "continuity-watchdog-restore-plan-v1-20260621.md"
DEFAULT_PACKET_DIR = REPORTS_DIR / "continuity-restore-packets-v1-20260621"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_OWNER = "lane-manager-ai_resources_lab-20260620"
WATCHDOG_AGENT = "continuity-watchdog-worker-20260621"
TASK_ID = "task-continuity-watchdog-restore-plan-v1-20260621"
KNOWN_COUNTS = [
    "repair_ownerless_lane",
    "dispatch_stale_owner_acknowledgement",
    "request_lane_goal",
    "manual_restore_review",
]
PROHIBITED_ACTIONS = [
    "mutate_source_snapshot",
    "create_duplicate_agent_without_overlap_review",
    "start_worker_or_thread_without_explicit_ceo_scope",
    "publish_submit_trade_spend_or_call_external_api",
]


def _finding_maps(snapshot: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    findings = snapshot.get("findings") or {}
    ownerless_by_lane = {
        str(item.get("lane_id")): item
        for item in findings.get("ownerless_active_lanes", [])
        if item.get("lane_id")
    }
    stale_ack_by_task = {
        str(item.get("task_id")): item
        for item in findings.get("stale_owner_acknowledgements", [])
        if item.get("task_id")
    }
    goal_gap_by_lane = {
        str(item.get("lane_id")): item
        for item in findings.get("lanes_without_open_tasks", [])
        if item.get("lane_id")
    }
    return {
        "ownerless_by_lane": ownerless_by_lane,
        "stale_ack_by_task": stale_ack_by_task,
        "goal_gap_by_lane": goal_gap_by_lane,
    }


def _input_id_from_ack(finding: dict[str, Any] | None) -> str | None:
    duplicate_key = str((finding or {}).get("duplicate_key") or "")
    marker = ":owner-acknowledgement:"
    if marker not in duplicate_key:
        return None
    return duplicate_key.split(marker, 1)[0] or None


def _packet_id(kind: str, target: str, index: int) -> str:
    return f"continuity-restore-v1-{index:03d}-{safe_id_fragment(kind, 60)}-{safe_id_fragment(target, 90)}"


def _packet_for_action(
    action: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
    snapshot: dict[str, Any],
    snapshot_path: Path,
    packet_dir: Path,
    index: int,
) -> dict[str, Any]:
    kind = str(action.get("kind") or "manual_restore_review")
    lane_id = action.get("lane_id")
    task_id = action.get("task_id")
    target = str(task_id or lane_id or action.get("agent_id") or action.get("duplicate_key") or f"action-{index}")
    packet_id = _packet_id(kind, target, index)
    packet_json_path = packet_dir / f"{packet_id}.json"
    packet_md_path = packet_dir / f"{packet_id}.md"

    packet: dict[str, Any] = {
        "restore_packet_id": packet_id,
        "schema_version": "continuity_restore_packet.v1",
        "kind": kind if kind in KNOWN_COUNTS else "manual_restore_review",
        "source_action_kind": kind,
        "source_snapshot_path": str(snapshot_path),
        "source_snapshot_generated_utc": snapshot.get("generated_utc"),
        "target_type": "lane" if lane_id and not task_id else "task" if task_id else "action",
        "target_id": target,
        "lane_id": lane_id,
        "source_task_id": task_id,
        "source_next_action": action.get("next_action"),
        "priority": 80,
        "assigned_surface": "ceo_decision_batch",
        "recommended_owner_agent_id": WATCHDOG_AGENT,
        "required_evidence": "Local restore decision artifact before any state mutation.",
        "next_action": "CEO reviews unsupported restore action and decides whether to route, park, merge, or retire.",
        "prohibited_actions": PROHIBITED_ACTIONS,
        "packet_json_path": str(packet_json_path),
        "packet_md_path": str(packet_md_path),
    }

    if kind == "repair_ownerless_lane":
        finding = maps["ownerless_by_lane"].get(str(lane_id))
        packet.update(
            {
                "target_type": "lane",
                "department": (finding or {}).get("department"),
                "owner_thread_id": (finding or {}).get("owner_thread_id"),
                "priority": 96,
                "assigned_surface": AI_RESOURCES_LANE,
                "recommended_owner_agent_id": AI_RESOURCES_OWNER,
                "required_evidence": "AI Resources owner-selection, park, or retire packet with overlap review evidence.",
                "next_action": (
                    "AI Resources selects an existing non-overlapping owner or writes an explicit park/retire decision; "
                    "new agents require capability-overlap review first."
                ),
            }
        )
    elif kind == "dispatch_stale_owner_acknowledgement":
        finding = maps["stale_ack_by_task"].get(str(task_id))
        packet.update(
            {
                "target_type": "task",
                "input_id": _input_id_from_ack(finding),
                "priority": 92,
                "assigned_surface": "existing_lane_owner",
                "recommended_owner_agent_id": (finding or {}).get("owner_agent_id"),
                "source_duplicate_key": (finding or {}).get("duplicate_key"),
                "source_status": (finding or {}).get("status"),
                "age_minutes": (finding or {}).get("age_minutes"),
                "required_evidence": "Existing lane owner acknowledgement artifact path and selected response option.",
                "next_action": (
                    "Use the owner-acknowledgement dispatch contract with the existing lane owner; "
                    "do not create a duplicate agent."
                ),
            }
        )
    elif kind == "request_lane_goal":
        finding = maps["goal_gap_by_lane"].get(str(lane_id))
        owner = (finding or {}).get("owner_agent_id")
        packet.update(
            {
                "target_type": "lane",
                "priority": 86,
                "assigned_surface": "existing_lane_owner" if owner else AI_RESOURCES_LANE,
                "recommended_owner_agent_id": owner or AI_RESOURCES_OWNER,
                "required_evidence": "One current lane goal artifact, or an explicit park/kill request with rationale.",
                "next_action": (
                    "Ask the lane owner for one current goal artifact; if no owner exists, route to AI Resources "
                    "for owner repair before goal assignment."
                ),
            }
        )
    return packet


def _counts(packets: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"restore_packets": len(packets)}
    for key in KNOWN_COUNTS:
        counts[key] = 0
    for packet in packets:
        counts[packet["kind"]] = counts.get(packet["kind"], 0) + 1
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_packet_md(path: Path, packet: dict[str, Any]) -> None:
    lines = [
        f"# Continuity Restore Packet: {packet['restore_packet_id']}",
        "",
        f"Kind: `{packet['kind']}`",
        f"Target: `{packet['target_type']}:{packet['target_id']}`",
        f"Assigned surface: `{packet['assigned_surface']}`",
        f"Recommended owner: `{packet.get('recommended_owner_agent_id') or ''}`",
        f"Priority: `{packet['priority']}`",
        "",
        "## Required Evidence",
        "",
        str(packet["required_evidence"]),
        "",
        "## Next Action",
        "",
        str(packet["next_action"]),
        "",
        "## Prohibited Actions",
        "",
    ]
    for action in packet["prohibited_actions"]:
        lines.append(f"- `{action}`")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Watchdog Restore Plan V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Source snapshot: `{payload['source_snapshot_path']}`",
        f"Packet dir: `{payload['packet_dir']}`",
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
            "## Restore Packets",
            "",
            "| Kind | Target | Assigned Surface | Recommended Owner | Priority | Next Action |",
            "| --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for packet in payload["restore_packets"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{packet['kind']}`",
                    md_cell(f"{packet['target_type']}:{packet['target_id']}", 160),
                    f"`{packet['assigned_surface']}`",
                    md_cell(packet.get("recommended_owner_agent_id"), 140),
                    str(packet["priority"]),
                    md_cell(packet["next_action"], 260),
                ]
            )
            + " |"
        )
    if not payload["restore_packets"]:
        lines.append("| none |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This restore plan writes local reports, local restore packet files, and audit rows only. It does not mutate source tasks or lanes, assign owners, release leases, send thread messages, start workers, open browsers, create accounts, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_packet_files(packets: list[dict[str, Any]]) -> None:
    packet_dirs = {Path(packet["packet_json_path"]).parent for packet in packets}
    if not packet_dirs:
        packet_dirs = {DEFAULT_PACKET_DIR}
    for packet_dir in packet_dirs:
        if not packet_dir.exists():
            continue
        for path in packet_dir.glob("continuity-restore-v1-*"):
            if path.is_file() and path.suffix in {".json", ".md"}:
                path.unlink()
    for packet in packets:
        json_path = Path(packet["packet_json_path"])
        md_path = Path(packet["packet_md_path"])
        _write_json(json_path, packet)
        _write_packet_md(md_path, packet)


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write continuity watchdog restore plan v1', 'complete', 94, ?, 'continuity-watchdog-restore-plan:v1', ?, ?, ?, ?, ?, ?)
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
            "artifact-continuity-watchdog-restore-plan-v1-json-20260621",
            "continuity_watchdog_restore_plan_json",
            json_path,
            "Machine-readable continuity watchdog restore plan.",
        ),
        (
            "artifact-continuity-watchdog-restore-plan-v1-md-20260621",
            "continuity_watchdog_restore_plan_markdown",
            md_path,
            "Human-readable continuity watchdog restore plan.",
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
              notes=excluded.notes
            """,
            (artifact_id, AI_RESOURCES_LANE, TASK_ID, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "counts": payload["counts"],
        "restore_packet_ids": [packet["restore_packet_id"] for packet in payload["restore_packets"]],
        "source_snapshot_path": payload["source_snapshot_path"],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_watchdog_restore_plan_written', ?, ?, ?, ?, ?, ?)
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
            "trace-event-continuity-watchdog-restore-plan-v1-20260621",
            "trace-continuity-watchdog-restore-plan-v1-20260621",
            AI_RESOURCES_LANE,
            TASK_ID,
            WATCHDOG_AGENT,
            ts,
            "continuity_watchdog_restore_plan_v1",
            f"Wrote {payload['counts']['restore_packets']} continuity restore packets.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-continuity-watchdog-restore-plan-v1-20260621', ?, ?, 'continuity_watchdog_restore_plan', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, payload["status"], str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_continuity_watchdog_restore_plan_bundle(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    snapshot_path = Path(getattr(args, "snapshot_report", None) or DEFAULT_SNAPSHOT_JSON)
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    packet_dir = Path(getattr(args, "packet_dir", None) or DEFAULT_PACKET_DIR)
    snapshot = load_json(snapshot_path)
    maps = _finding_maps(snapshot)
    packets = [
        _packet_for_action(action, maps, snapshot, snapshot_path, packet_dir, index)
        for index, action in enumerate(snapshot.get("restore_actions") or [], start=1)
    ]
    counts = _counts(packets)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "restore_plan_ready" if packets else "no_restore_needed",
        "source_snapshot_path": str(snapshot_path),
        "source_snapshot_generated_utc": snapshot.get("generated_utc"),
        "source_snapshot_status": snapshot.get("status"),
        "counts": counts,
        "restore_packets": packets,
        "next_action": (
            "Route restore packets to AI Resources or existing lane owners; keep all source state unchanged until packet evidence exists."
            if packets
            else "No restore packets required; continue continuity watchdog cadence."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "packet_dir": str(packet_dir),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_packet_files(packets)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_continuity_watchdog_restore_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_continuity_watchdog_restore_plan_bundle(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "restore_packet_ids": [packet["restore_packet_id"] for packet in payload["restore_packets"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "packet_dir": payload["packet_dir"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
