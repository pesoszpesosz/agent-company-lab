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


def write_agent_company_department_schema_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    schema_plan_task_id = "task-agent-company-department-schema-plan-20260616"
    schema_plan_evidence_id = "agent-company-department-schema-plan-20260616"
    source_packet_task_id = "task-agent-company-department-architecture-packet-20260616"
    source_packet_evidence_id = "agent-company-department-architecture-packet-20260616"
    duplicate_key = "agent-company-department-schema-plan-20260616"
    local_decision = "agent_company_department_schema_plan_ready_for_report_only_migration_draft"
    recommended_default = "draft_report_only_migration_next_without_creating_tables_or_workers"
    schema_plan_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")

    source_packet_validation = load_json(AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_VALIDATION_JSON)
    source_packet_payload = load_json(AGENT_COMPANY_DEPARTMENT_ARCHITECTURE_PACKET_JSON)
    table_plans = [
        {"table": "agent_threads", "columns": ["thread_id", "department_id", "lane_id", "role_id", "owner_agent_id", "state", "current_task_id", "service_request_id", "handoff_status", "last_report_path", "created_at", "updated_at"], "indexes": ["department_state", "owner_state"]},
        {"table": "departments", "columns": ["department_id", "manager_role_id", "purpose", "status", "default_lane_id", "approval_policy_id", "queue_limit", "created_at", "updated_at", "last_reviewed_at"], "indexes": ["status_manager", "default_lane"]},
        {"table": "money_paths", "columns": ["money_path_id", "department_id", "name", "category", "payout_model", "expected_value_score", "legality_status", "capital_required", "proofability_score", "gate_level", "status", "created_at", "updated_at"], "indexes": ["department_status", "category_score"]},
        {"table": "opportunity_leads", "columns": ["lead_id", "money_path_id", "source_url", "source_name", "payout_min", "payout_max", "currency", "account_required", "risk_score", "competition_score", "proof_artifact_path", "next_action", "status", "created_at", "updated_at"], "indexes": ["money_path_status", "risk_payout"]},
        {"table": "worker_pool_interfaces", "columns": ["pool_id", "department_id", "worker_role_id", "allowed_actions", "forbidden_actions", "input_schema", "output_schema", "approval_required", "max_parallel_threads", "status", "created_at", "updated_at"], "indexes": ["department_status", "approval_status"]},
        {"table": "approval_gates", "columns": ["gate_id", "gate_type", "department_id", "requested_by_thread_id", "service_request_id", "scope", "risk_summary", "approval_state", "approved_by", "expires_at", "rollback_plan", "decision_note", "created_at", "updated_at"], "indexes": ["state_type", "service_request_state"]},
        {"table": "evidence_packets", "columns": ["packet_id", "lane_id", "department_id", "source_task_id", "source_path", "source_url", "confidence", "status", "summary", "next_action", "reviewer_note", "created_at", "updated_at"], "indexes": ["department_status", "source_task"]},
        {"table": "task_handoffs", "columns": ["handoff_id", "from_thread_id", "to_thread_id", "task_id", "service_request_id", "handoff_type", "payload_path", "status", "response_path", "created_at", "updated_at", "completed_at"], "indexes": ["to_thread_status", "task_status"]},
        {"table": "experiment_runs", "columns": ["run_id", "money_path_id", "department_id", "experiment_type", "hypothesis", "input_path", "output_path", "metric_json", "result_state", "kill_reason", "started_at", "completed_at", "created_at"], "indexes": ["money_path_result", "department_started"]},
        {"table": "roi_ledger", "columns": ["roi_entry_id", "money_path_id", "lead_id", "task_id", "expected_value_usd", "realized_value_usd", "cost_usd", "minutes_spent", "payout_probability", "status", "decision_reason", "created_at", "updated_at"], "indexes": ["money_path_status", "value_probability"]},
    ]
    service_request_contracts = [
        {"request_type": item, "required_fields": ["request_id", "department_id", "source_path", "risk_summary", "approval_scope"], "default_status": "needs_review"}
        for item in source_packet_payload.get("service_request_types", [])
    ]
    migration_steps = [
        "create_departments_and_money_paths_plan",
        "create_agent_threads_and_worker_pool_interfaces_plan",
        "create_approval_gates_plan",
        "create_opportunity_leads_plan",
        "create_evidence_packets_and_task_handoffs_plan",
        "create_experiment_runs_and_roi_ledger_plan",
        "backfill_department_mappings_plan",
        "run_report_only_integrity_validation_plan",
    ]
    guardrails = [
        "report_only_until_operator_approval",
        "no_table_creation_in_this_command",
        "no_worker_start_or_assignment",
        "no_browser_or_account_action",
        "no_wallet_payment_or_real_money_action",
        "no_security_testing_beyond_read_only",
        "no_public_submission_or_marketplace_post",
        "preserve_existing_service_request_states",
    ]
    table_plan_count = len(table_plans)
    column_plan_count = sum(len(item["columns"]) for item in table_plans)
    index_plan_count = sum(len(item["indexes"]) for item in table_plans)
    service_request_contract_count = len(service_request_contracts)
    migration_step_count = len(migration_steps)
    guardrail_count = len(guardrails)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_packet_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_packet_task_id,),
    ).fetchone()
    source_packet_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_packet_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (schema_plan_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (schema_plan_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_packet_task or source_packet_task["status"] != "complete":
        failures.append("source department architecture packet task is missing or incomplete")
    if not source_packet_evidence or source_packet_evidence["status"] != "local_agent_company_department_architecture_packet_complete":
        failures.append("source department architecture packet evidence is missing or not complete")
    if not source_packet_validation.get("all_checks_passed") or source_packet_validation.get("failure_count") != 0:
        failures.append("source department architecture packet validation is not clean")
    if schema_plan_count != 1:
        failures.append(f"expected 1 schema plan, got {schema_plan_count}")
    if table_plan_count != 10:
        failures.append(f"expected 10 table plans, got {table_plan_count}")
    if column_plan_count != 127:
        failures.append(f"expected 127 column plans, got {column_plan_count}")
    if index_plan_count != 20:
        failures.append(f"expected 20 index plans, got {index_plan_count}")
    if service_request_contract_count != 12:
        failures.append(f"expected 12 service request contracts, got {service_request_contract_count}")
    if migration_step_count != 8:
        failures.append(f"expected 8 migration steps, got {migration_step_count}")
    if guardrail_count != 8:
        failures.append(f"expected 8 guardrails, got {guardrail_count}")
    if target_task_exists_before:
        failures.append(f"target schema plan task already exists: {schema_plan_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"schema plan evidence already exists: {schema_plan_evidence_id}")
    if tasks_table_rows_before != 227:
        failures.append(f"expected 227 task rows before department schema plan, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 135:
        failures.append(f"expected 135 evidence rows before department schema plan, got {lane_evidence_rows_before}")

    summary = "Converted the department architecture packet into a report-only schema plan for tables, columns, indexes, service request contracts, migration order, and guardrails."
    next_action = "Draft the report-only migration packet next; do not create tables or start any workers until explicitly approved."
    runtime_boundary = {
        "tables_created": 0,
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
        "schema_version": "agent_company.department_schema_plan.v1",
        "generated_utc": generated_utc,
        "schema_plan_lane_id": lane_id,
        "schema_plan_task_id": schema_plan_task_id,
        "schema_plan_evidence_id": schema_plan_evidence_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "schema_plan_count": schema_plan_count,
        "table_plan_count": table_plan_count,
        "column_plan_count": column_plan_count,
        "index_plan_count": index_plan_count,
        "service_request_contract_count": service_request_contract_count,
        "migration_step_count": migration_step_count,
        "guardrail_count": guardrail_count,
        "table_plans": table_plans,
        "service_request_contracts": service_request_contracts,
        "migration_steps": migration_steps,
        "guardrails": guardrails,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Department Schema Plan",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        summary,
        "",
        "## Table Plans",
        "",
        "| Table | Columns | Indexes |",
        "| --- | ---: | --- |",
    ]
    for item in table_plans:
        md_lines.append(f"| `{item['table']}` | {len(item['columns'])} | {', '.join(item['indexes'])} |")
    md_lines.extend(["", "## Service Request Contracts", ""])
    md_lines.extend(f"- `{item['request_type']}`: status starts as `{item['default_status']}`; required fields: {', '.join(item['required_fields'])}" for item in service_request_contracts)
    md_lines.extend(["", "## Migration Order", ""])
    md_lines.extend(f"{idx}. `{step}`" for idx, step in enumerate(migration_steps, start=1))
    md_lines.extend(["", "## Guardrails", ""])
    md_lines.extend(f"- `{item}`" for item in guardrails)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This schema plan is report-only. It creates no database tables, starts no workers, assigns no service requests, calls no APIs, opens no browsers, registers no accounts, touches no wallets or payments, spends no money, posts nowhere, and performs no security testing.",
            "",
            "## Next Action",
            "",
            next_action,
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
                schema_plan_task_id,
                lane_id,
                "Create agent company department schema plan",
                11,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": schema_plan_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company department schema plan",
                "status": "local_agent_company_department_schema_plan_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the local department architecture packet; report-only and no external actions.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_after = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_schema_plan = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (schema_plan_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (schema_plan_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (schema_plan_task_id,)) else 0
    tables_created = int(table_count_after) - int(table_count_before)
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_schema_plan != 1:
        failures.append(f"expected 1 task row inserted by schema plan, got {task_rows_inserted_by_schema_plan}")
    if tasks_table_rows_after != 228:
        failures.append(f"expected 228 task rows after schema plan, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 136:
        failures.append(f"expected 136 evidence rows after schema plan, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("schema plan evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by report-only schema plan, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during department schema plan")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_schema_plan": task_rows_inserted_by_schema_plan,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.department_schema_plan_validation.v1",
        "generated_utc": generated_utc,
        "schema_plan_path": str(json_output_path),
        "schema_plan_lane_id": lane_id,
        "schema_plan_task_id": schema_plan_task_id,
        "source_packet_task_id": source_packet_task_id,
        "schema_plan_count": schema_plan_count,
        "table_plan_count": table_plan_count,
        "column_plan_count": column_plan_count,
        "index_plan_count": index_plan_count,
        "service_request_contract_count": service_request_contract_count,
        "migration_step_count": migration_step_count,
        "guardrail_count": guardrail_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_schema_plan": task_rows_inserted_by_schema_plan,
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
                "schema_plan_lane_id": lane_id,
                "schema_plan_task_id": schema_plan_task_id,
                "table_plan_count": table_plan_count,
                "column_plan_count": column_plan_count,
                "index_plan_count": index_plan_count,
                "service_request_contract_count": service_request_contract_count,
                "task_rows_inserted_by_schema_plan": task_rows_inserted_by_schema_plan,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

