from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Infrastructure radar and department architecture/schema planning writers."""

from .constants import (
    AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_JSON,
    AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_REPORT,
    AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_VALIDATION_JSON,
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_JSON,
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_REPORT,
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_VALIDATION_JSON,
    AGENT_COMPANY_INFRASTRUCTURE_RADAR_JSON,
    AGENT_COMPANY_INFRASTRUCTURE_RADAR_REPORT,
    AGENT_COMPANY_INFRASTRUCTURE_RADAR_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .agent_company_migration_infrastructure_radar_content import build_agent_company_infrastructure_radar_model


def write_agent_company_infrastructure_radar(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_INFRASTRUCTURE_RADAR_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_INFRASTRUCTURE_RADAR_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_INFRASTRUCTURE_RADAR_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    radar_task_id = "task-agent-company-infrastructure-radar-20260616"
    radar_evidence_id = "agent-company-infrastructure-radar-20260616"
    duplicate_key = "agent-company-infrastructure-radar-20260616"
    local_decision = "agent_company_infrastructure_radar_ready_for_department_design"
    recommended_default = "use_temporal_or_durable_queue_for_workflow_state_and_agent_frameworks_for_role_level_reasoning"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    radar_model = build_agent_company_infrastructure_radar_model()
    primary_sources = radar_model["primary_sources"]
    candidates = radar_model["candidates"]
    architecture_mappings = radar_model["architecture_mappings"]
    recommended_spine = radar_model["recommended_spine"]
    cashflow_lane_mappings = radar_model["cashflow_lane_mappings"]
    approval_gates = radar_model["approval_gates"]
    primary_source_count = radar_model["primary_source_count"]
    candidate_count = radar_model["candidate_count"]
    architecture_mapping_count = radar_model["architecture_mapping_count"]
    recommended_spine_count = radar_model["recommended_spine_count"]
    cashflow_lane_mapping_count = radar_model["cashflow_lane_mapping_count"]
    approval_gate_count = radar_model["approval_gate_count"]
    infrastructure_radar_count = radar_model["infrastructure_radar_count"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (radar_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    radar_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (radar_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if infrastructure_radar_count != 1:
        failures.append(f"expected 1 infrastructure radar, got {infrastructure_radar_count}")
    if primary_source_count != 5:
        failures.append(f"expected 5 primary sources, got {primary_source_count}")
    if candidate_count != 5:
        failures.append(f"expected 5 candidates, got {candidate_count}")
    if architecture_mapping_count != 7:
        failures.append(f"expected 7 architecture mappings, got {architecture_mapping_count}")
    if recommended_spine_count != 4:
        failures.append(f"expected 4 recommended spine entries, got {recommended_spine_count}")
    if cashflow_lane_mapping_count != 8:
        failures.append(f"expected 8 cashflow lane mappings, got {cashflow_lane_mapping_count}")
    if approval_gate_count != 6:
        failures.append(f"expected 6 approval gates, got {approval_gate_count}")
    if target_task_exists_before:
        failures.append(f"target infrastructure radar task already exists: {radar_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if radar_evidence_exists_before:
        failures.append(f"infrastructure radar evidence already exists: {radar_evidence_id}")
    if tasks_table_rows_before != 225:
        failures.append(f"expected 225 task rows before infrastructure radar, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 133:
        failures.append(f"expected 133 evidence rows before infrastructure radar, got {lane_evidence_rows_before}")

    radar_summary = (
        "Created a primary-source-backed infrastructure radar for the agent company: durable orchestration spine, stateful manager graphs, guarded tool agents, department templates, and approval gates."
    )
    radar_next_action = (
        "Turn this radar into a department architecture packet with concrete tables, service request types, thread templates, and worker pool interfaces."
    )
    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "agent_company.infrastructure_radar.v1",
        "generated_utc": generated_utc,
        "radar_lane_id": lane_id,
        "radar_task_id": radar_task_id,
        "radar_evidence_id": radar_evidence_id,
        "infrastructure_radar_count": infrastructure_radar_count,
        "primary_source_count": primary_source_count,
        "candidate_count": candidate_count,
        "architecture_mapping_count": architecture_mapping_count,
        "recommended_spine_count": recommended_spine_count,
        "cashflow_lane_mapping_count": cashflow_lane_mapping_count,
        "approval_gate_count": approval_gate_count,
        "primary_sources": primary_sources,
        "candidates": candidates,
        "architecture_mappings": architecture_mappings,
        "recommended_spine": recommended_spine,
        "cashflow_lane_mappings": cashflow_lane_mappings,
        "approval_gates": approval_gates,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": radar_summary,
        "next_action": radar_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Infrastructure Radar",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        radar_summary,
        "",
        "## Primary Sources",
        "",
        "| Source | Type | Agent Company Takeaway | URL |",
        "| --- | --- | --- | --- |",
    ]
    for source in primary_sources:
        md_lines.append(f"| {source['name']} | `{source['source_type']}` | {source['agent_company_takeaway']} | {source['url']} |")
    md_lines.extend(["", "## Recommended Spine", ""])
    md_lines.extend(f"- {item}" for item in recommended_spine)
    md_lines.extend(
        [
            "",
            "## Architecture Mapping",
            "",
            "| Layer | Stack | Responsibility |",
            "| --- | --- | --- |",
        ]
    )
    for item in architecture_mappings:
        md_lines.append(f"| {item['layer']} | {', '.join(item['recommended_stack'])} | {item['responsibility']} |")
    md_lines.extend(
        [
            "",
            "## Cashflow Lanes",
            "",
            "| Lane | Agent Type | Gate |",
            "| --- | --- | --- |",
        ]
    )
    for item in cashflow_lane_mappings:
        md_lines.append(f"| `{item['lane']}` | `{item['agent_type']}` | `{item['gate']}` |")
    md_lines.extend(["", "## Approval Gates", ""])
    md_lines.extend(f"- `{gate}`" for gate in approval_gates)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This radar is local research infrastructure. It does not install dependencies, start workers, call APIs, open browsers, register accounts, create wallets, spend money, submit reports, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            radar_next_action,
            "",
        ]
    )
    output_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                radar_task_id,
                lane_id,
                "Create source-backed agent company infrastructure radar",
                12,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                radar_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": radar_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company infrastructure radar",
                "status": "local_agent_company_infrastructure_radar_complete",
                "summary": radar_summary,
                "next_action": radar_next_action,
                "ownership_note": "Generated by platform_engineering from current primary-source research; radar is local-only and performs no external actions.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_radar = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (radar_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (radar_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (radar_task_id,)) else 0
    if task_rows_inserted_by_radar != 1:
        failures.append(f"expected 1 task row inserted by infrastructure radar, got {task_rows_inserted_by_radar}")
    if tasks_table_rows_after != 226:
        failures.append(f"expected 226 task rows after infrastructure radar, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 134:
        failures.append(f"expected 134 evidence rows after infrastructure radar, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("infrastructure radar evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during infrastructure radar")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_radar": task_rows_inserted_by_radar,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.infrastructure_radar_validation.v1",
        "generated_utc": generated_utc,
        "radar_path": str(json_output_path),
        "radar_lane_id": lane_id,
        "radar_task_id": radar_task_id,
        "infrastructure_radar_count": infrastructure_radar_count,
        "primary_source_count": primary_source_count,
        "candidate_count": candidate_count,
        "architecture_mapping_count": architecture_mapping_count,
        "recommended_spine_count": recommended_spine_count,
        "cashflow_lane_mapping_count": cashflow_lane_mapping_count,
        "approval_gate_count": approval_gate_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_radar": task_rows_inserted_by_radar,
        "lane_evidence_rows_before": lane_evidence_rows_before,
        "lane_evidence_rows_after": lane_evidence_rows_after,
        "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "radar_lane_id": lane_id,
                "radar_task_id": radar_task_id,
                "primary_source_count": primary_source_count,
                "candidate_count": candidate_count,
                "cashflow_lane_mapping_count": cashflow_lane_mapping_count,
                "task_rows_inserted_by_radar": task_rows_inserted_by_radar,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

