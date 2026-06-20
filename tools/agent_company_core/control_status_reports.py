from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    CEO_REVIEW_REPORT,
    COMPANY_EXPANSION_GAP_MAP_JSON,
    COMPANY_EXPANSION_GAP_MAP_REPORT,
    COMPANY_EXPANSION_GAP_MAP_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_workers import db_scalar
from .utils import md_cell

def list_status(conn: sqlite3.Connection) -> None:
    lanes = [dict(row) for row in conn.execute("SELECT lane_id, department, owner_agent_id, owner_thread_id, status FROM lanes ORDER BY lane_id")]
    tasks = [dict(row) for row in conn.execute("SELECT task_id, lane_id, status, priority, title, owner_agent_id, lease_owner_agent_id, lease_expires_at FROM tasks ORDER BY priority DESC, created_at DESC LIMIT 25")]
    requests = [dict(row) for row in conn.execute("SELECT request_id, service_id, request_type, lane_id, status, risk_gate, assigned_agent_id, artifact_path, decision_note FROM service_requests ORDER BY created_at DESC LIMIT 25")]
    service_catalog = [dict(row) for row in conn.execute("SELECT service_id, request_type, owner_role_id, default_status, purpose FROM service_catalog ORDER BY request_type, service_id LIMIT 25")]
    artifacts = [dict(row) for row in conn.execute("SELECT artifact_id, lane_id, task_id, kind, path_or_url FROM artifacts ORDER BY created_at DESC LIMIT 25")]
    outcomes = [dict(row) for row in conn.execute("SELECT outcome_id, lane_id, task_id, outcome_type, status FROM outcomes ORDER BY created_at DESC LIMIT 25")]
    evidence = [dict(row) for row in conn.execute("SELECT evidence_id, lane_id, status, title, source_path, source_url FROM lane_evidence ORDER BY updated_at DESC LIMIT 25")]
    source_specs = [dict(row) for row in conn.execute("SELECT spec_id, lane_id, source_type, cadence, risk_gate FROM source_specs ORDER BY lane_id, spec_id LIMIT 25")]
    trace_events = [dict(row) for row in conn.execute("SELECT event_id, trace_id, lane_id, task_id, event_type, event_time, summary, artifact_path FROM trace_events ORDER BY event_time DESC, created_at DESC LIMIT 25")]
    print(json.dumps({"db": str(DB_PATH), "lanes": lanes, "tasks": tasks, "service_requests": requests, "service_catalog": service_catalog, "artifacts": artifacts, "outcomes": outcomes, "evidence": evidence, "source_specs": source_specs, "trace_events": trace_events}, indent=2))


def write_dashboard(conn: sqlite3.Connection, path: str | None) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(path) if path else REPORTS_DIR / "control-plane-status-latest.md"
    lanes = [dict(row) for row in conn.execute("SELECT lane_id, department, owner_agent_id, owner_thread_id, status FROM lanes ORDER BY lane_id")]
    tasks = [dict(row) for row in conn.execute("SELECT task_id, lane_id, status, priority, title, owner_agent_id, lease_owner_agent_id, lease_expires_at, next_action FROM tasks ORDER BY priority DESC, created_at DESC LIMIT 50")]
    requests = [dict(row) for row in conn.execute("SELECT request_id, service_id, request_type, lane_id, status, risk_gate, requested_action, assigned_agent_id, artifact_path, decision_note FROM service_requests ORDER BY created_at DESC LIMIT 50")]
    service_catalog = [dict(row) for row in conn.execute("SELECT service_id, request_type, owner_role_id, default_status, purpose FROM service_catalog ORDER BY request_type, service_id LIMIT 50")]
    artifacts = [dict(row) for row in conn.execute("SELECT artifact_id, lane_id, task_id, kind, path_or_url FROM artifacts ORDER BY created_at DESC LIMIT 50")]
    outcomes = [dict(row) for row in conn.execute("SELECT outcome_id, lane_id, task_id, outcome_type, status, next_action FROM outcomes ORDER BY created_at DESC LIMIT 50")]
    evidence = [dict(row) for row in conn.execute("SELECT evidence_id, lane_id, status, title, source_path, source_url, next_action, ownership_note FROM lane_evidence ORDER BY updated_at DESC LIMIT 50")]
    source_specs = [dict(row) for row in conn.execute("SELECT spec_id, lane_id, source_type, cadence, risk_gate FROM source_specs ORDER BY lane_id, spec_id LIMIT 50")]
    trace_events = [dict(row) for row in conn.execute("SELECT event_id, trace_id, lane_id, task_id, event_type, event_time, summary, artifact_path FROM trace_events ORDER BY event_time DESC, created_at DESC LIMIT 50")]

    lines = [
        "# Agent Company Control Plane Status",
        "",
        f"Generated UTC: {now_utc()}",
        f"Database: `{DB_PATH}`",
        "",
        "## Lane Ownership",
        "",
        "| Lane | Department | Owner Agent | Owner Thread | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for lane in lanes:
        lines.append(
            f"| `{lane['lane_id']}` | {lane['department']} | {lane['owner_agent_id'] or ''} | {lane['owner_thread_id'] or ''} | {lane['status']} |"
        )
    lines.extend(["", "## Active Tasks", "", "| Priority | Status | Lane | Task | Owner | Lease | Next Action |", "| ---: | --- | --- | --- | --- | --- | --- |"])
    for task in tasks:
        lines.append(
            f"| {task['priority']} | {task['status']} | `{task['lane_id']}` | `{task['task_id']}` - {task['title']} | {task['owner_agent_id'] or ''} | {task['lease_owner_agent_id'] or ''} until {task['lease_expires_at'] or ''} | {task['next_action'] or ''} |"
        )
    lines.extend(["", "## Service Requests", "", "| Status | Service | Type | Lane | Assigned | Gate | Requested Action | Artifact | Decision Note |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for req in requests:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(req["status"], 80),
                    md_cell(req["service_id"], 120),
                    md_cell(req["request_type"], 120),
                    f"`{req['lane_id'] or ''}`",
                    md_cell(req["assigned_agent_id"], 120),
                    md_cell(req["risk_gate"], 180),
                    md_cell(req["requested_action"], 260),
                    md_cell(req["artifact_path"], 160),
                    md_cell(req["decision_note"], 180),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Service Worker Catalog", "", "| Status | Type | Service | Owner Role | Purpose |", "| --- | --- | --- | --- | --- |"])
    for service in service_catalog:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(service["default_status"], 80),
                    md_cell(service["request_type"], 120),
                    f"`{service['service_id']}`",
                    f"`{service['owner_role_id']}`",
                    md_cell(service["purpose"], 280),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Recent Artifacts", "", "| Kind | Lane | Artifact | Path/URL |", "| --- | --- | --- | --- |"])
    for artifact in artifacts:
        lines.append(
            f"| {artifact['kind']} | `{artifact['lane_id'] or ''}` | `{artifact['artifact_id']}` | `{artifact['path_or_url']}` |"
        )
    lines.extend(["", "## Recent Outcomes", "", "| Status | Type | Lane | Outcome | Next Action |", "| --- | --- | --- | --- | --- |"])
    for outcome in outcomes:
        lines.append(
            f"| {outcome['status']} | {outcome['outcome_type']} | `{outcome['lane_id']}` | `{outcome['outcome_id']}` | {outcome['next_action'] or ''} |"
        )
    lines.extend(["", "## Recent Lane Evidence", "", "| Status | Lane | Evidence | Source | Ownership Note | Next Action |", "| --- | --- | --- | --- | --- | --- |"])
    for item in evidence:
        source = item["source_url"] or item["source_path"] or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item["status"], 120),
                    f"`{item['lane_id']}`",
                    f"`{item['evidence_id']}` - {md_cell(item['title'], 180)}",
                    md_cell(source, 180),
                    md_cell(item["ownership_note"], 220),
                    md_cell(item["next_action"], 220),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Source Specs", "", "| Lane | Spec | Type | Cadence | Gate |", "| --- | --- | --- | --- | --- |"])
    for spec in source_specs:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{spec['lane_id']}`",
                    f"`{spec['spec_id']}`",
                    md_cell(spec["source_type"], 80),
                    md_cell(spec["cadence"], 120),
                    md_cell(spec["risk_gate"], 180),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Recent Trace Events", "", "| Time | Type | Trace | Lane | Task | Event | Artifact |", "| --- | --- | --- | --- | --- | --- | --- |"])
    for event in trace_events:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(event["event_time"], 80),
                    md_cell(event["event_type"], 100),
                    f"`{event['trace_id']}`",
                    f"`{event['lane_id'] or ''}`",
                    f"`{event['task_id'] or ''}`",
                    f"`{event['event_id']}` - {md_cell(event['summary'], 220)}",
                    md_cell(event["artifact_path"], 160),
                ]
            )
            + " |"
        )
    if not trace_events:
        lines.append("| none |  |  |  |  |  |  |")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path)}, indent=2))

