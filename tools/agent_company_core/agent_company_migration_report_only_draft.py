from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Report-only migration draft, apply preflight, and operator review writers."""

from .constants import (
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_JSON,
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_JSON,
    AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_REPORT,
    AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_JSON,
    AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_REPORT,
    AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_VALIDATION_JSON,
)
from .agent_company_migration_report_only_draft_content import build_report_only_migration_draft_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_report_only_migration_draft(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    migration_task_id = "task-agent-company-report-only-migration-draft-20260616"
    migration_evidence_id = "agent-company-report-only-migration-draft-20260616"
    source_schema_plan_task_id = "task-agent-company-department-schema-plan-20260616"
    source_schema_plan_evidence_id = "agent-company-department-schema-plan-20260616"
    duplicate_key = "agent-company-report-only-migration-draft-20260616"
    local_decision = "agent_company_report_only_migration_draft_ready_for_apply_preflight_packet"
    recommended_default = "draft_apply_preflight_next_without_executing_migration_sql"
    migration_draft_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")

    source_schema_validation = load_json(AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_VALIDATION_JSON)
    source_schema_payload = load_json(AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_JSON)
    table_plans = source_schema_payload.get("table_plans", [])
    draft_content = build_report_only_migration_draft_content(table_plans)
    table_migrations = draft_content["table_migrations"]
    create_statements = draft_content["create_statements"]
    index_statements = draft_content["index_statements"]
    validation_queries = draft_content["validation_queries"]
    rollback_statements = draft_content["rollback_statements"]
    apply_gates = draft_content["apply_gates"]
    table_migration_count = draft_content["table_migration_count"]
    create_statement_count = draft_content["create_statement_count"]
    index_statement_count = draft_content["index_statement_count"]
    validation_query_count = draft_content["validation_query_count"]
    rollback_statement_count = draft_content["rollback_statement_count"]
    apply_gate_count = draft_content["apply_gate_count"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_schema_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_schema_plan_task_id,),
    ).fetchone()
    source_schema_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_schema_plan_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (migration_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (migration_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_schema_task or source_schema_task["status"] != "complete":
        failures.append("source department schema plan task is missing or incomplete")
    if not source_schema_evidence or source_schema_evidence["status"] != "local_agent_company_department_schema_plan_complete":
        failures.append("source department schema plan evidence is missing or not complete")
    if not source_schema_validation.get("all_checks_passed") or source_schema_validation.get("failure_count") != 0:
        failures.append("source department schema plan validation is not clean")
    if migration_draft_count != 1:
        failures.append(f"expected 1 migration draft, got {migration_draft_count}")
    if table_migration_count != 10:
        failures.append(f"expected 10 table migrations, got {table_migration_count}")
    if create_statement_count != 10:
        failures.append(f"expected 10 create statements, got {create_statement_count}")
    if index_statement_count != 20:
        failures.append(f"expected 20 index statements, got {index_statement_count}")
    if validation_query_count != 10:
        failures.append(f"expected 10 validation queries, got {validation_query_count}")
    if rollback_statement_count != 30:
        failures.append(f"expected 30 rollback statements, got {rollback_statement_count}")
    if apply_gate_count != 7:
        failures.append(f"expected 7 apply gates, got {apply_gate_count}")
    if target_task_exists_before:
        failures.append(f"target report-only migration task already exists: {migration_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"report-only migration evidence already exists: {migration_evidence_id}")
    if tasks_table_rows_before != 228:
        failures.append(f"expected 228 task rows before report-only migration draft, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 136:
        failures.append(f"expected 136 evidence rows before report-only migration draft, got {lane_evidence_rows_before}")

    summary = "Drafted a report-only migration packet from the department schema plan, including SQL text, validation queries, rollback SQL, and apply gates without executing migration SQL."
    next_action = "Draft the apply-preflight packet next; do not execute migration SQL until the operator explicitly approves an apply step."
    runtime_boundary = {
        "migration_sql_executed": False,
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
        "schema_version": "agent_company.report_only_migration_draft.v1",
        "generated_utc": generated_utc,
        "migration_lane_id": lane_id,
        "migration_task_id": migration_task_id,
        "migration_evidence_id": migration_evidence_id,
        "source_schema_plan_task_id": source_schema_plan_task_id,
        "source_schema_plan_evidence_id": source_schema_plan_evidence_id,
        "migration_draft_count": migration_draft_count,
        "table_migration_count": table_migration_count,
        "create_statement_count": create_statement_count,
        "index_statement_count": index_statement_count,
        "validation_query_count": validation_query_count,
        "rollback_statement_count": rollback_statement_count,
        "apply_gate_count": apply_gate_count,
        "table_migrations": table_migrations,
        "create_statements": create_statements,
        "index_statements": index_statements,
        "validation_queries": validation_queries,
        "rollback_statements": rollback_statements,
        "apply_gates": apply_gates,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Report-Only Migration Draft",
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
        "## Migration Inventory",
        "",
        f"- Tables: {table_migration_count}",
        f"- CREATE TABLE statements: {create_statement_count}",
        f"- CREATE INDEX statements: {index_statement_count}",
        f"- Validation queries: {validation_query_count}",
        f"- Rollback statements: {rollback_statement_count}",
        "",
        "## Apply Gates",
        "",
    ]
    md_lines.extend(f"- `{gate}`" for gate in apply_gates)
    md_lines.extend(["", "## SQL Draft", ""])
    for table_migration in table_migrations:
        md_lines.extend(
            [
                f"### `{table_migration['table']}`",
                "",
                "```sql",
                table_migration["create_statement"],
                *table_migration["index_statements"],
                table_migration["validation_query"],
                "```",
                "",
                "Rollback:",
                "",
                "```sql",
                *table_migration["rollback_statements"],
                "```",
                "",
            ]
        )
    md_lines.extend(
        [
            "## Boundary",
            "",
            "This command writes a migration draft only. It does not execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                migration_task_id,
                lane_id,
                "Create agent company report-only migration draft",
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
                "evidence_id": migration_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company report-only migration draft",
                "status": "local_agent_company_report_only_migration_draft_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the department schema plan; SQL is report-only and was not executed.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    table_count_after = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    tables_created = int(table_count_after) - int(table_count_before)
    task_rows_inserted_by_migration_draft = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (migration_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (migration_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (migration_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_migration_draft != 1:
        failures.append(f"expected 1 task row inserted by migration draft, got {task_rows_inserted_by_migration_draft}")
    if tasks_table_rows_after != 229:
        failures.append(f"expected 229 task rows after migration draft, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 137:
        failures.append(f"expected 137 evidence rows after migration draft, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("report-only migration evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by report-only migration draft, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during report-only migration draft")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_migration_draft": task_rows_inserted_by_migration_draft,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.report_only_migration_draft_validation.v1",
        "generated_utc": generated_utc,
        "migration_draft_path": str(json_output_path),
        "migration_lane_id": lane_id,
        "migration_task_id": migration_task_id,
        "source_schema_plan_task_id": source_schema_plan_task_id,
        "migration_draft_count": migration_draft_count,
        "table_migration_count": table_migration_count,
        "create_statement_count": create_statement_count,
        "index_statement_count": index_statement_count,
        "validation_query_count": validation_query_count,
        "rollback_statement_count": rollback_statement_count,
        "apply_gate_count": apply_gate_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_migration_draft": task_rows_inserted_by_migration_draft,
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
                "migration_lane_id": lane_id,
                "migration_task_id": migration_task_id,
                "table_migration_count": table_migration_count,
                "create_statement_count": create_statement_count,
                "index_statement_count": index_statement_count,
                "validation_query_count": validation_query_count,
                "rollback_statement_count": rollback_statement_count,
                "task_rows_inserted_by_migration_draft": task_rows_inserted_by_migration_draft,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

