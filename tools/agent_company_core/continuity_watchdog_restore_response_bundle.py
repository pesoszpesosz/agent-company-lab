"""Owner-facing response contracts for continuity restore packets."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .continuity_watchdog_restore_plan import DEFAULT_JSON as DEFAULT_RESTORE_PLAN_JSON
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_watchdog_restore_response_bundle.v1"
DEFAULT_JSON = REPORTS_DIR / "continuity-watchdog-restore-response-bundle-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "continuity-watchdog-restore-response-bundle-v1-20260621.md"
DEFAULT_RESPONSE_DIR = REPORTS_DIR / "continuity-restore-responses-v1-20260621"
AI_RESOURCES_LANE = "ai_resources_lab"
WATCHDOG_AGENT = "continuity-watchdog-worker-20260621"
TASK_ID = "task-continuity-watchdog-restore-response-bundle-v1-20260621"
RESPONSE_TYPES = [
    "owner_selection_or_park_required",
    "acknowledgement_response_required",
    "lane_goal_response_required",
    "manual_review_required",
]
COMMON_PROHIBITED_ACTIONS = [
    "mutate_source_restore_packet",
    "mutate_source_task_or_lane",
    "create_duplicate_agent_without_overlap_review",
    "start_worker_or_thread_without_explicit_ceo_scope",
    "publish_submit_trade_spend_or_call_external_api",
]


def _response_type(kind: str) -> str:
    if kind == "repair_ownerless_lane":
        return "owner_selection_or_park_required"
    if kind == "dispatch_stale_owner_acknowledgement":
        return "acknowledgement_response_required"
    if kind == "request_lane_goal":
        return "lane_goal_response_required"
    return "manual_review_required"


def _response_contract(response_type: str) -> dict[str, Any]:
    if response_type == "owner_selection_or_park_required":
        allowed = [
            "assign_existing_owner_after_overlap_review",
            "park_lane_with_revisit_condition",
            "retire_lane_with_rationale",
            "request_ceo_decision_batch_item",
        ]
        required = [
            "selected_response_option",
            "lane_id",
            "restore_packet_id",
            "owner_agent_id_or_decision_owner",
            "evidence_artifact_path",
            "overlap_review_or_revisit_condition",
        ]
    elif response_type == "acknowledgement_response_required":
        allowed = [
            "acknowledge_and_start_local_work",
            "park_with_revisit_condition",
            "request_ceo_decision_batch_item",
        ]
        required = [
            "selected_response_option",
            "lane_id",
            "source_task_id",
            "owner_agent_id",
            "evidence_artifact_path",
            "next_revisit_condition_or_ceo_decision_needed",
        ]
    elif response_type == "lane_goal_response_required":
        allowed = [
            "submit_current_goal_artifact",
            "park_lane_with_revisit_condition",
            "request_owner_repair",
        ]
        required = [
            "selected_response_option",
            "lane_id",
            "restore_packet_id",
            "owner_agent_id",
            "goal_artifact_path_or_revisit_condition",
        ]
    else:
        allowed = ["route_to_ceo_decision_batch", "park_with_revisit_condition"]
        required = [
            "selected_response_option",
            "restore_packet_id",
            "decision_owner",
            "evidence_artifact_path",
            "next_action",
        ]
    return {
        "allowed_responses": allowed,
        "required_fields": required,
        "prohibited_actions": COMMON_PROHIBITED_ACTIONS,
    }


def _response_next_action(response_type: str) -> str:
    if response_type == "owner_selection_or_park_required":
        return "AI Resources must produce an owner-selection, park, retire, or CEO-decision artifact before any lane ownership mutation."
    if response_type == "acknowledgement_response_required":
        return "Existing lane owner must submit exactly one acknowledgement response artifact using the response contract."
    if response_type == "lane_goal_response_required":
        return "Lane owner must submit one current goal artifact, a park/revisit condition, or an owner-repair request."
    return "CEO decision batch must route, park, or retire this unsupported restore action."


def _response_id(packet: dict[str, Any], index: int) -> str:
    packet_id = str(packet.get("restore_packet_id") or packet.get("target_id") or f"packet-{index}")
    return f"continuity-restore-response-v1-{index:03d}-{safe_id_fragment(packet_id, 110)}"


def _response_item(
    packet: dict[str, Any],
    restore_plan_path: Path,
    restore_plan_generated_utc: str | None,
    response_dir: Path,
    index: int,
) -> dict[str, Any]:
    response_type = _response_type(str(packet.get("kind") or "manual_review_required"))
    response_id = _response_id(packet, index)
    response_json_path = response_dir / f"{response_id}.json"
    response_md_path = response_dir / f"{response_id}.md"
    return {
        "response_item_id": response_id,
        "schema_version": "continuity_restore_response.v1",
        "response_type": response_type,
        "restore_packet_id": packet.get("restore_packet_id"),
        "source_restore_plan_path": str(restore_plan_path),
        "source_restore_plan_generated_utc": restore_plan_generated_utc,
        "source_action_kind": packet.get("kind"),
        "target_type": packet.get("target_type"),
        "target_id": packet.get("target_id"),
        "lane_id": packet.get("lane_id"),
        "source_task_id": packet.get("source_task_id"),
        "input_id": packet.get("input_id"),
        "assigned_surface": packet.get("assigned_surface"),
        "recommended_owner_agent_id": packet.get("recommended_owner_agent_id"),
        "required_evidence": packet.get("required_evidence"),
        "source_packet_next_action": packet.get("next_action"),
        "next_action": _response_next_action(response_type),
        "response_contract": _response_contract(response_type),
        "response_json_path": str(response_json_path),
        "response_md_path": str(response_md_path),
    }


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"response_items": len(items)}
    for response_type in RESPONSE_TYPES:
        counts[response_type] = 0
    for item in items:
        counts[item["response_type"]] = counts.get(item["response_type"], 0) + 1
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_response_md(path: Path, item: dict[str, Any]) -> None:
    lines = [
        f"# Continuity Restore Response: {item['response_item_id']}",
        "",
        f"Response type: `{item['response_type']}`",
        f"Restore packet: `{item.get('restore_packet_id') or ''}`",
        f"Target: `{item.get('target_type') or ''}:{item.get('target_id') or ''}`",
        f"Assigned surface: `{item.get('assigned_surface') or ''}`",
        f"Recommended owner: `{item.get('recommended_owner_agent_id') or ''}`",
        "",
        "## Next Action",
        "",
        str(item["next_action"]),
        "",
        "## Response Contract",
        "",
        "Allowed responses:",
    ]
    for option in item["response_contract"]["allowed_responses"]:
        lines.append(f"- `{option}`")
    lines.extend(["", "Required fields:"])
    for field in item["response_contract"]["required_fields"]:
        lines.append(f"- `{field}`")
    lines.extend(["", "Prohibited actions:"])
    for action in item["response_contract"]["prohibited_actions"]:
        lines.append(f"- `{action}`")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Watchdog Restore Response Bundle V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Restore plan: `{payload['source_restore_plan_path']}`",
        f"Response dir: `{payload['response_dir']}`",
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
            "## Response Items",
            "",
            "| Response Type | Target | Assigned Surface | Recommended Owner | Next Action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in payload["response_items"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['response_type']}`",
                    md_cell(f"{item.get('target_type') or ''}:{item.get('target_id') or ''}", 160),
                    f"`{item.get('assigned_surface') or ''}`",
                    md_cell(item.get("recommended_owner_agent_id"), 140),
                    md_cell(item["next_action"], 260),
                ]
            )
            + " |"
        )
    if not payload["response_items"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This bundle writes local response contracts and audit rows only. It does not mutate source restore packets, source tasks, source lanes, owner assignments, service requests, worker queues, browser state, accounts, public surfaces, payments, trades, submissions, APIs, or external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_response_files(items: list[dict[str, Any]]) -> None:
    response_dirs = {Path(item["response_json_path"]).parent for item in items}
    if not response_dirs:
        response_dirs = {DEFAULT_RESPONSE_DIR}
    for response_dir in response_dirs:
        if not response_dir.exists():
            continue
        for path in response_dir.glob("continuity-restore-response-v1-*"):
            if path.is_file() and path.suffix in {".json", ".md"}:
                path.unlink()
    for item in items:
        _write_json(Path(item["response_json_path"]), item)
        _write_response_md(Path(item["response_md_path"]), item)


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write continuity watchdog restore response bundle v1', 'complete', 95, ?, 'continuity-watchdog-restore-response-bundle:v1', ?, ?, ?, ?, ?, ?)
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
            "artifact-continuity-watchdog-restore-response-bundle-v1-json-20260621",
            "continuity_watchdog_restore_response_bundle_json",
            json_path,
            "Machine-readable continuity watchdog restore response bundle.",
        ),
        (
            "artifact-continuity-watchdog-restore-response-bundle-v1-md-20260621",
            "continuity_watchdog_restore_response_bundle_markdown",
            md_path,
            "Human-readable continuity watchdog restore response bundle.",
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
        "response_item_ids": [item["response_item_id"] for item in payload["response_items"]],
        "source_restore_plan_path": payload["source_restore_plan_path"],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_watchdog_restore_response_bundle_written', ?, ?, ?, ?, ?, ?)
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
            "trace-event-continuity-watchdog-restore-response-bundle-v1-20260621",
            "trace-continuity-watchdog-restore-response-bundle-v1-20260621",
            AI_RESOURCES_LANE,
            TASK_ID,
            WATCHDOG_AGENT,
            ts,
            "continuity_watchdog_restore_response_bundle_v1",
            f"Wrote {payload['counts']['response_items']} continuity restore response contracts.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-continuity-watchdog-restore-response-bundle-v1-20260621', ?, ?, 'continuity_watchdog_restore_response_bundle', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, payload["status"], str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_continuity_watchdog_restore_response_bundle(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    restore_plan_path = Path(getattr(args, "restore_plan", None) or DEFAULT_RESTORE_PLAN_JSON)
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    response_dir = Path(getattr(args, "response_dir", None) or DEFAULT_RESPONSE_DIR)
    restore_plan = load_json(restore_plan_path)
    items = [
        _response_item(
            packet,
            restore_plan_path,
            restore_plan.get("generated_utc"),
            response_dir,
            index,
        )
        for index, packet in enumerate(restore_plan.get("restore_packets") or [], start=1)
    ]
    counts = _counts(items)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "responses_ready" if items else "no_responses_needed",
        "source_restore_plan_path": str(restore_plan_path),
        "source_restore_plan_generated_utc": restore_plan.get("generated_utc"),
        "source_restore_plan_status": restore_plan.get("status"),
        "counts": counts,
        "response_items": items,
        "next_action": (
            "Route response contracts to AI Resources or existing lane owners; source restore packets and source tasks remain unchanged."
            if items
            else "No restore responses required; continue continuity watchdog cadence."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "response_dir": str(response_dir),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_response_files(items)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_continuity_watchdog_restore_response_bundle_cli(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = write_continuity_watchdog_restore_response_bundle(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "response_item_ids": [item["response_item_id"] for item in payload["response_items"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "response_dir": payload["response_dir"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
