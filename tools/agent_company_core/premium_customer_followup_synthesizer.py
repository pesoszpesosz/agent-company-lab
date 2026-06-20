"""Synthesize lane-owned follow-up tasks from premium customer route packets."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR, ROOT
from .premium_customer_intake_router import OWNER_AGENT_ID, ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, safe_id_fragment, sha256_file


PROCESSED_DIR = ROOT / "intake" / "customer" / "processed"
LEDGER_JSON = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.json"
LEDGER_MD = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.md"
UPDATE_FEED_JSON = REPORTS_DIR / "customer-update-feed-v3-20260620.json"
UPDATE_FEED_MD = REPORTS_DIR / "customer-update-feed-v3-20260620.md"
SCHEMA_VERSION = "premium_customer_lane_followup_synthesis.v1"


LANE_ACTIONS = {
    "ai_resources_lab": "Evaluate required worker/resource capability and propose one non-overlapping upgrade or reuse path.",
    "youtube_content_channels": "Create a YouTube lane work packet that turns the capsule into one script/storyboard or material-analysis task.",
    "paid_code_bounties": "Create a local no-egress bounty scout packet or decide the existing paid-code lane already covers it.",
    "prediction_market_research": "Create a local market-angle packet with data needs, venue gates, and no-trade boundary.",
    "ai_ml_competitions": "Create a competition feasibility packet with account/dataset/compute gates and local proof path.",
    "money_source_discovery": "Decide whether this implies a new money path, an existing lane update, or a watch-list revisit trigger.",
    "digital_products_templates_plugins": "Create a local product-fit packet or route to an existing product artifact plan.",
    "content_and_social_growth": "Create a distribution/growth packet that stays local unless a later public-action gate is approved.",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(value: str | None, limit: int = 380) -> str:
    if not value:
        return ""
    cleaned = " ".join(str(value).replace("\r", "\n").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit].rstrip() + "..."


def _primary_route(packet: dict[str, Any]) -> str:
    why = packet.get("ceo_context_capsule", {}).get("why_this_route", "")
    match = re.search(r"Primary route `([^`]+)`", why)
    if match:
        return match.group(1)
    target_lanes = packet.get("target_lane_ids") or []
    if target_lanes:
        return str(target_lanes[0])
    for route in packet.get("routes", []):
        if route.get("status") == "routed":
            return str(route.get("lane_or_surface"))
    return "premium_customer_intake"


def _lane_owner(conn: sqlite3.Connection | None, lane_id: str) -> tuple[str | None, bool]:
    if conn is None:
        return None, False
    row = conn.execute("SELECT owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    if not row:
        return None, False
    return row["owner_agent_id"], True


def _task_status_for_duplicate(conn: sqlite3.Connection, task_id: str, duplicate_key: str) -> str | None:
    row = conn.execute(
        "SELECT status FROM tasks WHERE task_id = ? OR duplicate_key = ? ORDER BY created_at DESC LIMIT 1",
        (task_id, duplicate_key),
    ).fetchone()
    return row["status"] if row else None


def _followup_task(packet: dict[str, Any], lane_id: str, primary_lane: str, owner_agent_id: str | None) -> dict[str, Any]:
    input_id = packet["input_id"]
    task_id = f"task-{input_id}-followup-{safe_id_fragment(lane_id, 70)}"
    summary = _compact(packet.get("customer_intent") or packet.get("ceo_context_capsule", {}).get("short_summary"))
    priority = 91 if lane_id == primary_lane else 76
    return {
        "task_id": task_id,
        "lane_id": lane_id,
        "title": f"Follow up customer input for {lane_id}",
        "status": "new",
        "priority": priority,
        "owner_agent_id": owner_agent_id,
        "duplicate_key": f"{input_id}:lane-followup:{lane_id}",
        "evidence_required": f"Route packet for {input_id}",
        "next_action": LANE_ACTIONS.get(
            lane_id,
            "Create a compact lane-owned packet that applies the customer input or parks it with a revisit condition.",
        ),
        "customer_context_capsule": summary,
    }


def _target_lanes(packet: dict[str, Any]) -> list[str]:
    lanes = []
    for lane_id in packet.get("target_lane_ids", []):
        if lane_id and lane_id not in lanes:
            lanes.append(str(lane_id))
    return lanes


def _packet_paths(input_id: str, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{input_id}-lane-followups.json", output_dir / f"{input_id}-lane-followups.md"


def _write_followup_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_followup_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Premium Customer Lane Follow-Up Synthesis",
        "",
        f"Input id: `{payload['input_id']}`",
        f"Generated UTC: {payload['generated_utc']}",
        f"Primary route: `{payload['primary_route']}`",
        f"Status: `{payload['status']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Capsule",
        "",
        payload["context_capsule"],
        "",
        "## Lane Tasks",
        "",
        "| Lane | Task | Owner | Priority | Status | Next Action |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for item in payload["followup_tasks"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    f"`{item['task_id']}`",
                    md_cell(item.get("owner_agent_id"), 100),
                    str(item["priority"]),
                    md_cell(item["status"], 80),
                    md_cell(item["next_action"], 220),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This synthesis creates local lane tasks and local artifacts only. It does not approve gates, start workers, open browsers, create accounts, publish, submit, trade, spend, call APIs, or perform external actions.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _upsert_followup_task(conn: sqlite3.Connection, task: dict[str, Any], route_packet_path: Path) -> str:
    ts = now_utc()
    existing_status = _task_status_for_duplicate(conn, task["task_id"], task["duplicate_key"])
    status = existing_status or task["status"]
    if existing_status:
        conn.execute(
            """
            UPDATE tasks
            SET lane_id = ?,
                title = ?,
                status = ?,
                priority = ?,
                owner_agent_id = COALESCE(owner_agent_id, ?),
                duplicate_key = ?,
                evidence_required = ?,
                next_action = ?,
                updated_at = ?
            WHERE task_id = ? OR duplicate_key = ?
            """,
            (
                task["lane_id"],
                task["title"],
                status,
                task["priority"],
                task.get("owner_agent_id"),
                task["duplicate_key"],
                str(route_packet_path),
                task["next_action"],
                ts,
                task["task_id"],
                task["duplicate_key"],
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task["task_id"],
                task["lane_id"],
                task["title"],
                status,
                task["priority"],
                task.get("owner_agent_id"),
                task["duplicate_key"],
                str(route_packet_path),
                task["next_action"],
                ts,
                ts,
            ),
        )
    return status


def _upsert_artifact(
    conn: sqlite3.Connection,
    artifact_id: str,
    lane_id: str,
    task_id: str,
    kind: str,
    path: Path,
    notes: str,
) -> None:
    ts = now_utc()
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
        (artifact_id, lane_id, task_id, kind, str(path), sha256_file(path), notes, ts),
    )


def _update_ledger_and_feed(
    payload: dict[str, Any],
    packet_md_path: Path,
    ledger_json: Path,
    ledger_md: Path,
    update_feed_json: Path,
    update_feed_md: Path,
) -> None:
    now = now_utc()
    if ledger_json.exists():
        ledger = _load_json(ledger_json)
        entries = []
        for entry in ledger.get("entries", []):
            if entry.get("input_id") == payload["input_id"]:
                updated = dict(entry)
                updated["status"] = "synthesized"
                updated["next_artifact"] = str(packet_md_path)
                updated["followup_task_ids"] = [task["task_id"] for task in payload["followup_tasks"]]
                entries.append(updated)
            else:
                entries.append(entry)
        ledger["entries"] = entries
        ledger["generated_utc"] = now
        ledger_json.write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")
        _write_ledger_md(ledger, packet_md_path, ledger_json, ledger_md)
    if update_feed_json.exists():
        feed = _load_json(update_feed_json)
    else:
        feed = {
            "schema_version": "customer_update_feed.v3",
            "owner_agent_id": OWNER_AGENT_ID,
            "status": "active_local_update_feed",
            "updates": [],
            "zero_side_effect_boundary": {"external_side_effects": False},
        }
    update = {
        "update_id": f"customer-update-{payload['input_id']}-followups",
        "generated_utc": now,
        "summary": f"Lane follow-up tasks synthesized for `{payload['input_id']}`.",
        "applied": [
            "lane_followup_packet_written",
            "lane_owned_tasks_created_or_refreshed",
            "routing_ledger_marked_synthesized",
        ],
        "route_packet_path": str(packet_md_path),
        "human_action_needed": False,
        "next": "Lane managers can claim or work the generated local tasks; no external action is authorized.",
    }
    updates = [item for item in feed.get("updates", []) if item.get("update_id") != update["update_id"]]
    feed["updates"] = [update] + updates
    feed["generated_utc"] = now
    feed["schema_version"] = "customer_update_feed.v3"
    feed["owner_agent_id"] = OWNER_AGENT_ID
    feed["status"] = "active_local_update_feed"
    feed["zero_side_effect_boundary"] = {"external_side_effects": False}
    update_feed_json.write_text(json.dumps(feed, indent=2, sort_keys=True), encoding="utf-8")
    _write_update_feed_md(feed, update_feed_json, update_feed_md)


def _write_ledger_md(ledger: dict[str, Any], packet_md_path: Path, ledger_json: Path, ledger_md: Path) -> None:
    lines = [
        "# Customer Request Routing Ledger V1",
        "",
        f"Generated UTC: {ledger.get('generated_utc')}",
        f"Owner: `{ledger.get('owner_agent_id')}`",
        f"Status: {ledger.get('status')}",
        f"JSON mirror: `{ledger_json}`",
        "",
        "## Ledger Rule",
        "",
        str(ledger.get("ledger_rule", "")),
        "",
        "## Entries",
        "",
        "| Input | Class | Primary Route | Status | Next Artifact |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in ledger.get("entries", []):
        lines.append(
            f"| `{item.get('input_id')}` | `{item.get('input_class')}` | `{item.get('primary_route')}` | {md_cell(item.get('status'), 80)} | `{item.get('next_artifact')}` |"
        )
    lines.extend(
        [
            "",
            "## Current Follow-Up Packet",
            "",
            f"`{packet_md_path}`",
            "",
            "## Boundary",
            "",
            "This ledger is local routing memory only. It does not approve gates, start workers, open browsers, create accounts, publish, upload, trade, spend, call APIs, or perform external actions.",
            "",
        ]
    )
    ledger_md.write_text("\n".join(lines), encoding="utf-8")


def _write_update_feed_md(feed: dict[str, Any], update_feed_json: Path, update_feed_md: Path) -> None:
    lines = [
        "# Customer Update Feed V3",
        "",
        f"Generated UTC: {feed.get('generated_utc')}",
        f"Owner: `{feed.get('owner_agent_id')}`",
        f"Status: {feed.get('status')}",
        f"JSON mirror: `{update_feed_json}`",
        "",
        "## Updates",
        "",
    ]
    for item in feed.get("updates", []):
        lines.extend(
            [
                f"### {item.get('generated_utc')} - {item.get('summary')}",
                "",
                f"Route packet: `{item.get('route_packet_path', '')}`",
                "",
                f"Human action needed: {'yes' if item.get('human_action_needed') else 'none'}.",
                "",
                f"Next: {item.get('next', '')}",
                "",
            ]
        )
    update_feed_md.write_text("\n".join(lines), encoding="utf-8")


def synthesize_premium_customer_followups(
    conn: sqlite3.Connection | None,
    args: argparse.Namespace,
) -> dict[str, Any]:
    route_packet_path = Path(args.route_packet)
    packet = _load_json(route_packet_path)
    input_id = packet["input_id"]
    output_dir = Path(args.output_dir) if getattr(args, "output_dir", None) else PROCESSED_DIR
    ledger_json = Path(args.ledger_json) if getattr(args, "ledger_json", None) else LEDGER_JSON
    ledger_md = Path(args.ledger_md) if getattr(args, "ledger_md", None) else LEDGER_MD
    update_feed_json = Path(args.update_feed_json) if getattr(args, "update_feed_json", None) else UPDATE_FEED_JSON
    update_feed_md = Path(args.update_feed_md) if getattr(args, "update_feed_md", None) else UPDATE_FEED_MD
    json_path, md_path = _packet_paths(input_id, output_dir)
    primary_lane = _primary_route(packet)
    lanes = _target_lanes(packet)
    if not lanes:
        raise SystemExit(f"Route packet has no target lanes: {route_packet_path}")
    followup_tasks: list[dict[str, Any]] = []
    unknown_lanes: list[str] = []
    for lane_id in lanes:
        owner, known = _lane_owner(conn, lane_id)
        if not known:
            unknown_lanes.append(lane_id)
        followup_tasks.append(_followup_task(packet, lane_id, primary_lane, owner))
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": now_utc(),
        "input_id": input_id,
        "status": "synthesized",
        "route_packet_path": str(route_packet_path),
        "primary_route": primary_lane,
        "context_capsule": _compact(packet.get("customer_intent") or packet.get("ceo_context_capsule", {}).get("short_summary"), 700),
        "followup_tasks": followup_tasks,
        "unknown_lanes": unknown_lanes,
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }
    _write_followup_json(json_path, payload)
    _write_followup_md(md_path, payload)
    if not getattr(args, "no_db_record", False) and conn is not None:
        command_task_id = f"task-{input_id}-lane-followup-synthesis"
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at, started_at, completed_at
            )
            VALUES(?, 'premium_customer_intake', ?, 'complete', 89, ?, ?, ?, ?, ?, ?, ?, ?)
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
                command_task_id,
                f"Synthesize lane follow-ups for {input_id}",
                OWNER_AGENT_ID,
                f"{input_id}:lane-followup-synthesis",
                str(md_path),
                "Lane managers own generated local tasks; intake monitors for stale unclaimed follow-ups.",
                ts,
                ts,
                ts,
                ts,
            ),
        )
        created_statuses: list[dict[str, str]] = []
        for task in followup_tasks:
            task_status = _upsert_followup_task(conn, task, route_packet_path)
            task["status"] = task_status
            created_statuses.append({"task_id": task["task_id"], "status": task_status})
        _write_followup_json(json_path, payload)
        _write_followup_md(md_path, payload)
        _upsert_artifact(
            conn,
            f"artifact-{input_id}-lane-followup-json",
            "premium_customer_intake",
            command_task_id,
            "customer_lane_followup_synthesis_json",
            json_path,
            "Machine-readable lane follow-up synthesis packet.",
        )
        _upsert_artifact(
            conn,
            f"artifact-{input_id}-lane-followup-md",
            "premium_customer_intake",
            command_task_id,
            "customer_lane_followup_synthesis",
            md_path,
            "Human-readable lane follow-up synthesis packet.",
        )
        metadata = {
            "input_id": input_id,
            "primary_route": primary_lane,
            "followup_task_ids": [task["task_id"] for task in followup_tasks],
            "unknown_lanes": unknown_lanes,
            "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        }
        conn.execute(
            """
            INSERT INTO trace_events(
              event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
              source, summary, metadata_json, artifact_path, created_at
            )
            VALUES(?, ?, 'premium_customer_intake', ?, ?, 'premium_customer_lane_followups_synthesized', ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
              trace_id=excluded.trace_id,
              task_id=excluded.task_id,
              agent_id=excluded.agent_id,
              event_time=excluded.event_time,
              source=excluded.source,
              summary=excluded.summary,
              metadata_json=excluded.metadata_json,
              artifact_path=excluded.artifact_path
            """,
            (
                f"trace-event-{input_id}-lane-followups",
                f"trace-{input_id}-lane-followups",
                command_task_id,
                OWNER_AGENT_ID,
                ts,
                "premium_customer_followup_synthesizer_v1",
                f"Synthesized {len(followup_tasks)} lane-owned follow-up tasks for {input_id}.",
                json.dumps(metadata, sort_keys=True),
                str(md_path),
                ts,
            ),
        )
        conn.execute(
            """
            INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
            VALUES(?, 'premium_customer_intake', ?, 'customer_lane_followup_synthesis', 'synthesized', 0, ?, ?, ?)
            ON CONFLICT(outcome_id) DO UPDATE SET
              status=excluded.status,
              evidence=excluded.evidence,
              next_action=excluded.next_action
            """,
            (
                f"outcome-{input_id}-lane-followups",
                command_task_id,
                str(md_path),
                "Monitor generated lane tasks; escalate stale or ownerless lanes to AI Resources.",
                ts,
            ),
        )
        conn.commit()
        _update_ledger_and_feed(payload, md_path, ledger_json, ledger_md, update_feed_json, update_feed_md)
    return payload


def write_premium_customer_followup_synthesis(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = synthesize_premium_customer_followups(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "input_id": payload["input_id"],
                "primary_route": payload["primary_route"],
                "followup_task_count": len(payload["followup_tasks"]),
                "followup_task_ids": [task["task_id"] for task in payload["followup_tasks"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
