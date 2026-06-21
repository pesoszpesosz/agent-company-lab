"""Concrete local owner responses for continuity restore response contracts."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .continuity_watchdog_restore_response_bundle import DEFAULT_JSON as DEFAULT_RESPONSE_BUNDLE_JSON
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


SCHEMA_VERSION = "continuity_watchdog_owner_response_artifacts.v1"
DEFAULT_JSON = REPORTS_DIR / "continuity-watchdog-owner-response-artifacts-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "continuity-watchdog-owner-response-artifacts-v1-20260621.md"
DEFAULT_ARTIFACT_DIR = REPORTS_DIR / "continuity-owner-responses-v1-20260621"
AI_RESOURCES_LANE = "ai_resources_lab"
WATCHDOG_AGENT = "continuity-watchdog-worker-20260621"
TASK_ID = "task-continuity-watchdog-owner-response-artifacts-v1-20260621"
RESPONSE_TYPES = [
    "owner_selection_or_park_required",
    "acknowledgement_response_required",
    "lane_goal_response_required",
    "manual_review_required",
]


def _selected_response_option(item: dict[str, Any]) -> str:
    response_type = str(item.get("response_type") or "manual_review_required")
    preferred = {
        "owner_selection_or_park_required": "request_ceo_decision_batch_item",
        "acknowledgement_response_required": "acknowledge_and_start_local_work",
        "lane_goal_response_required": "submit_current_goal_artifact",
        "manual_review_required": "route_to_ceo_decision_batch",
    }.get(response_type, "route_to_ceo_decision_batch")
    allowed = (item.get("response_contract") or {}).get("allowed_responses") or []
    if not allowed or preferred in allowed:
        return preferred
    return str(allowed[0])


def _artifact_id(item: dict[str, Any], index: int) -> str:
    source = str(item.get("response_item_id") or item.get("restore_packet_id") or f"response-{index}")
    return f"continuity-owner-response-v1-{index:03d}-{safe_id_fragment(source, 110)}"


def _base_artifact(item: dict[str, Any], artifact_dir: Path, index: int) -> dict[str, Any]:
    artifact_id = _artifact_id(item, index)
    artifact_json_path = artifact_dir / f"{artifact_id}.json"
    artifact_md_path = artifact_dir / f"{artifact_id}.md"
    response_type = str(item.get("response_type") or "manual_review_required")
    selected = _selected_response_option(item)
    return {
        "owner_response_artifact_id": artifact_id,
        "schema_version": "continuity_owner_response_artifact.v1",
        "response_type": response_type if response_type in RESPONSE_TYPES else "manual_review_required",
        "selected_response_option": selected,
        "source_response_item_id": item.get("response_item_id"),
        "restore_packet_id": item.get("restore_packet_id"),
        "target_type": item.get("target_type"),
        "target_id": item.get("target_id"),
        "lane_id": item.get("lane_id"),
        "source_task_id": item.get("source_task_id"),
        "input_id": item.get("input_id"),
        "assigned_surface": item.get("assigned_surface"),
        "recommended_owner_agent_id": item.get("recommended_owner_agent_id"),
        "required_evidence": item.get("required_evidence"),
        "artifact_json_path": str(artifact_json_path),
        "artifact_md_path": str(artifact_md_path),
        "source_state_mutated": False,
        "external_side_effects": False,
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }


def _owner_selection_fields(artifact: dict[str, Any]) -> dict[str, Any]:
    lane_id = artifact.get("lane_id") or artifact.get("target_id") or "unknown_lane"
    return {
        "owner_agent_id_or_decision_owner": "ceo_decision_batch",
        "evidence_artifact_path": artifact["artifact_md_path"],
        "overlap_review_or_revisit_condition": (
            "AI Resources must complete capability-overlap review before changing owner assignment."
        ),
        "next_action": (
            f"Queue `{lane_id}` for CEO decision batch: select an existing non-overlapping owner, park it with a "
            "revisit condition, or retire it with rationale. Do not mutate lane ownership from this artifact."
        ),
    }


def _acknowledgement_fields(artifact: dict[str, Any]) -> dict[str, Any]:
    owner = artifact.get("recommended_owner_agent_id") or "existing_lane_owner"
    lane_id = artifact.get("lane_id") or "unknown_lane"
    return {
        "owner_agent_id": owner,
        "evidence_artifact_path": artifact["artifact_md_path"],
        "next_revisit_condition_or_ceo_decision_needed": (
            "If no owner update lands before the next continuity cadence, keep this acknowledgement in the restore queue."
        ),
        "local_work_scope": "Acknowledge the routed item and start local artifact work only.",
        "next_action": (
            f"Existing owner `{owner}` should handle the acknowledgement for `{lane_id}` locally and report evidence; "
            "no duplicate owner or worker should be created."
        ),
    }


def _lane_goal_fields(artifact: dict[str, Any]) -> dict[str, Any]:
    owner = artifact.get("recommended_owner_agent_id") or "existing_lane_owner"
    lane_id = artifact.get("lane_id") or artifact.get("target_id") or "unknown_lane"
    current_goal = (
        f"Produce one current local proof artifact for `{lane_id}` or submit an explicit park/retire request with rationale."
    )
    return {
        "owner_agent_id": owner,
        "goal_artifact_path_or_revisit_condition": artifact["artifact_md_path"],
        "current_goal_statement": current_goal,
        "first_local_action": (
            "Write a compact lane goal artifact with expected evidence, fast-fail condition, and next CEO-visible status."
        ),
        "fast_fail_rule": "If the lane cannot name a local proof artifact, evidence path, and next owner step, park it.",
        "next_action": f"Owner `{owner}` should submit the lane goal artifact for `{lane_id}`.",
    }


def _manual_review_fields(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_owner": "ceo_decision_batch",
        "evidence_artifact_path": artifact["artifact_md_path"],
        "next_action": "Route this unsupported response type to CEO decision batch or park it with a revisit condition.",
    }


def _owner_response_artifact(item: dict[str, Any], artifact_dir: Path, index: int) -> dict[str, Any]:
    artifact = _base_artifact(item, artifact_dir, index)
    if artifact["response_type"] == "owner_selection_or_park_required":
        artifact.update(_owner_selection_fields(artifact))
    elif artifact["response_type"] == "acknowledgement_response_required":
        artifact.update(_acknowledgement_fields(artifact))
    elif artifact["response_type"] == "lane_goal_response_required":
        artifact.update(_lane_goal_fields(artifact))
    else:
        artifact.update(_manual_review_fields(artifact))
    return artifact


def _counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"owner_response_artifacts": len(items)}
    for response_type in RESPONSE_TYPES:
        counts[response_type] = 0
    for item in items:
        counts[item["response_type"]] = counts.get(item["response_type"], 0) + 1
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_artifact_md(path: Path, artifact: dict[str, Any]) -> None:
    lines = [
        f"# Continuity Owner Response: {artifact['owner_response_artifact_id']}",
        "",
        f"Response type: `{artifact['response_type']}`",
        f"Selected response: `{artifact['selected_response_option']}`",
        f"Target: `{artifact.get('target_type') or ''}:{artifact.get('target_id') or ''}`",
        f"Lane: `{artifact.get('lane_id') or ''}`",
        f"Owner/decision surface: `{artifact.get('owner_agent_id') or artifact.get('owner_agent_id_or_decision_owner') or artifact.get('decision_owner') or ''}`",
        "",
        "## Next Action",
        "",
        str(artifact["next_action"]),
        "",
        "## Evidence",
        "",
        f"Evidence artifact path: `{artifact.get('evidence_artifact_path') or artifact.get('goal_artifact_path_or_revisit_condition') or ''}`",
        f"Source response item: `{artifact.get('source_response_item_id') or ''}`",
        f"Restore packet: `{artifact.get('restore_packet_id') or ''}`",
        "",
    ]
    if artifact.get("current_goal_statement"):
        lines.extend(
            [
                "## Current Lane Goal",
                "",
                str(artifact["current_goal_statement"]),
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "This owner response artifact is local-only. It does not mutate source tasks, source lanes, owner assignments, worker queues, browser state, accounts, public surfaces, payments, trades, submissions, APIs, or external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Continuity Watchdog Owner Response Artifacts V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Response bundle: `{payload['source_response_bundle_path']}`",
        f"Artifact dir: `{payload['artifact_dir']}`",
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
            "## Owner Response Artifacts",
            "",
            "| Response Type | Target | Selected Response | Owner/Decision Surface | Next Action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for artifact in payload["owner_response_artifacts"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{artifact['response_type']}`",
                    md_cell(f"{artifact.get('target_type') or ''}:{artifact.get('target_id') or ''}", 160),
                    f"`{artifact['selected_response_option']}`",
                    md_cell(
                        artifact.get("owner_agent_id")
                        or artifact.get("owner_agent_id_or_decision_owner")
                        or artifact.get("decision_owner"),
                        140,
                    ),
                    md_cell(artifact["next_action"], 260),
                ]
            )
            + " |"
        )
    if not payload["owner_response_artifacts"]:
        lines.append("| none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This command writes local owner response artifacts and audit rows only. It does not mutate source response contracts, source restore packets, source tasks, source lanes, owner assignments, service requests, worker queues, browser state, accounts, public surfaces, payments, trades, submissions, APIs, or external systems.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_artifact_files(items: list[dict[str, Any]]) -> None:
    for item in items:
        _write_json(Path(item["artifact_json_path"]), item)
        _write_artifact_md(Path(item["artifact_md_path"]), item)


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Write continuity watchdog owner response artifacts v1', 'complete', 96, ?, 'continuity-watchdog-owner-response-artifacts:v1', ?, ?, ?, ?, ?, ?)
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
            "artifact-continuity-watchdog-owner-response-artifacts-v1-json-20260621",
            "continuity_watchdog_owner_response_artifacts_json",
            json_path,
            "Machine-readable continuity watchdog owner response artifacts.",
        ),
        (
            "artifact-continuity-watchdog-owner-response-artifacts-v1-md-20260621",
            "continuity_watchdog_owner_response_artifacts_markdown",
            md_path,
            "Human-readable continuity watchdog owner response artifacts.",
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
        "owner_response_artifact_ids": [
            item["owner_response_artifact_id"] for item in payload["owner_response_artifacts"]
        ],
        "source_response_bundle_path": payload["source_response_bundle_path"],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'continuity_watchdog_owner_response_artifacts_written', ?, ?, ?, ?, ?, ?)
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
            "trace-event-continuity-watchdog-owner-response-artifacts-v1-20260621",
            "trace-continuity-watchdog-owner-response-artifacts-v1-20260621",
            AI_RESOURCES_LANE,
            TASK_ID,
            WATCHDOG_AGENT,
            ts,
            "continuity_watchdog_owner_response_artifacts_v1",
            f"Wrote {payload['counts']['owner_response_artifacts']} continuity owner response artifacts.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-continuity-watchdog-owner-response-artifacts-v1-20260621', ?, ?, 'continuity_watchdog_owner_response_artifacts', ?, 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, TASK_ID, payload["status"], str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def write_continuity_watchdog_owner_response_artifacts(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    response_bundle_path = Path(getattr(args, "response_bundle", None) or DEFAULT_RESPONSE_BUNDLE_JSON)
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    artifact_dir = Path(getattr(args, "artifact_dir", None) or DEFAULT_ARTIFACT_DIR)
    response_bundle = load_json(response_bundle_path)
    items = [
        _owner_response_artifact(item, artifact_dir, index)
        for index, item in enumerate(response_bundle.get("response_items") or [], start=1)
    ]
    counts = _counts(items)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "owner_response_artifacts_ready" if items else "no_owner_response_artifacts_needed",
        "source_response_bundle_path": str(response_bundle_path),
        "source_response_bundle_generated_utc": response_bundle.get("generated_utc"),
        "source_response_bundle_status": response_bundle.get("status"),
        "counts": counts,
        "owner_response_artifacts": items,
        "next_action": (
            "Use these local owner response artifacts in the next CEO/AI Resources state packet; source tasks and lanes remain unchanged."
            if items
            else "No owner response artifacts required; continue continuity watchdog cadence."
        ),
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "artifact_dir": str(artifact_dir),
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_artifact_files(items)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_continuity_watchdog_owner_response_artifacts_cli(
    conn: sqlite3.Connection,
    args: argparse.Namespace,
) -> None:
    payload = write_continuity_watchdog_owner_response_artifacts(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "owner_response_artifact_ids": [
                    item["owner_response_artifact_id"] for item in payload["owner_response_artifacts"]
                ],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "artifact_dir": payload["artifact_dir"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
