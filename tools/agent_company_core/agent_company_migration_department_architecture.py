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
from .agent_company_migration_department_architecture_content import (
    build_agent_company_department_architecture_packet_markdown_lines,
    build_agent_company_department_architecture_packet_model,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_department_architecture_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    packet_task_id = "task-agent-company-department-architecture-packet-20260616"
    packet_evidence_id = "agent-company-department-architecture-packet-20260616"
    source_radar_task_id = "task-agent-company-infrastructure-radar-20260616"
    source_radar_evidence_id = "agent-company-infrastructure-radar-20260616"
    duplicate_key = "agent-company-department-architecture-packet-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    radar_validation = load_json(AGENT_COMPANY_INFRASTRUCTURE_RADAR_VALIDATION_JSON)
    radar_payload = load_json(AGENT_COMPANY_INFRASTRUCTURE_RADAR_JSON)
    content_model = build_agent_company_department_architecture_packet_model(radar_payload.get("approval_gates"))
    department_architecture_packet_count = content_model["department_architecture_packet_count"]
    department_count = content_model["department_count"]
    table_blueprint_count = content_model["table_blueprint_count"]
    service_request_type_count = content_model["service_request_type_count"]
    thread_template_count = content_model["thread_template_count"]
    worker_pool_interface_count = content_model["worker_pool_interface_count"]
    approval_gate_count = content_model["approval_gate_count"]
    local_decision = content_model["local_decision"]
    recommended_default = content_model["recommended_default"]
    packet_summary = content_model["summary"]
    packet_next_action = content_model["next_action"]
    runtime_boundary = content_model["runtime_boundary"]
    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_radar_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_radar_task_id,),
    ).fetchone()
    source_radar_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_radar_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    packet_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_radar_task or source_radar_task["status"] != "complete":
        failures.append("source infrastructure radar task is missing or incomplete")
    if not source_radar_evidence or source_radar_evidence["status"] != "local_agent_company_infrastructure_radar_complete":
        failures.append("source infrastructure radar evidence is missing or not complete")
    if not radar_validation.get("all_checks_passed") or radar_validation.get("failure_count") != 0:
        failures.append("source infrastructure radar validation is not clean")
    if department_architecture_packet_count != 1:
        failures.append(f"expected 1 department architecture packet, got {department_architecture_packet_count}")
    if department_count != 7:
        failures.append(f"expected 7 departments, got {department_count}")
    if table_blueprint_count != 10:
        failures.append(f"expected 10 table blueprints, got {table_blueprint_count}")
    if service_request_type_count != 12:
        failures.append(f"expected 12 service request types, got {service_request_type_count}")
    if thread_template_count != 8:
        failures.append(f"expected 8 thread templates, got {thread_template_count}")
    if worker_pool_interface_count != 7:
        failures.append(f"expected 7 worker pool interfaces, got {worker_pool_interface_count}")
    if approval_gate_count != 6:
        failures.append(f"expected 6 approval gates, got {approval_gate_count}")
    if target_task_exists_before:
        failures.append(f"target department architecture packet task already exists: {packet_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if packet_evidence_exists_before:
        failures.append(f"department architecture packet evidence already exists: {packet_evidence_id}")
    if tasks_table_rows_before != 226:
        failures.append(f"expected 226 task rows before department architecture packet, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 134:
        failures.append(f"expected 134 evidence rows before department architecture packet, got {lane_evidence_rows_before}")


    payload = {
        "schema_version": "agent_company.department_architecture_packet.v1",
        "generated_utc": generated_utc,
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "packet_evidence_id": packet_evidence_id,
        "source_radar_task_id": source_radar_task_id,
        "source_radar_evidence_id": source_radar_evidence_id,
        "source_radar_validation_path": str(AGENT_COMPANY_INFRASTRUCTURE_RADAR_VALIDATION_JSON),
        **content_model,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = build_agent_company_department_architecture_packet_markdown_lines(
        model=content_model,
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
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
                packet_task_id,
                lane_id,
                "Create agent company department architecture packet",
                11,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                packet_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": packet_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company department architecture packet",
                "status": "local_agent_company_department_architecture_packet_complete",
                "summary": packet_summary,
                "next_action": packet_next_action,
                "ownership_note": "Generated by platform_engineering from the local infrastructure radar; packet is local-only and performs no external actions.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_packet = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (packet_task_id,)) else 0
    if task_rows_inserted_by_packet != 1:
        failures.append(f"expected 1 task row inserted by department architecture packet, got {task_rows_inserted_by_packet}")
    if tasks_table_rows_after != 227:
        failures.append(f"expected 227 task rows after department architecture packet, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 135:
        failures.append(f"expected 135 evidence rows after department architecture packet, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("department architecture packet evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during department architecture packet")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.department_architecture_packet_validation.v1",
        "generated_utc": generated_utc,
        "packet_path": str(json_output_path),
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "source_radar_task_id": source_radar_task_id,
        "department_architecture_packet_count": department_architecture_packet_count,
        "department_count": department_count,
        "table_blueprint_count": table_blueprint_count,
        "service_request_type_count": service_request_type_count,
        "thread_template_count": thread_template_count,
        "worker_pool_interface_count": worker_pool_interface_count,
        "approval_gate_count": approval_gate_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
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
                "packet_lane_id": lane_id,
                "packet_task_id": packet_task_id,
                "department_count": department_count,
                "table_blueprint_count": table_blueprint_count,
                "service_request_type_count": service_request_type_count,
                "thread_template_count": thread_template_count,
                "worker_pool_interface_count": worker_pool_interface_count,
                "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


