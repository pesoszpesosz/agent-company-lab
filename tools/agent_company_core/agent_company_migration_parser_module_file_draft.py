from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Migration decision parser fixture-check, module-file draft, and static review writers."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_VALIDATION_JSON,
)
from .agent_company_migration_parser_module_file_draft_content import build_parser_module_file_draft_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_module_file_draft(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    file_draft_task_id = "task-agent-company-migration-decision-parser-module-file-draft-20260616"
    file_draft_evidence_id = "agent-company-migration-decision-parser-module-file-draft-20260616"
    source_checks_task_id = "task-agent-company-migration-decision-module-fixture-checks-20260616"
    source_checks_evidence_id = "agent-company-migration-decision-module-fixture-checks-20260616"
    duplicate_key = "agent-company-migration-decision-parser-module-file-draft-20260616"
    local_decision = "agent_company_migration_decision_parser_module_file_draft_ready_for_report_only_static_review"
    recommended_default = "static_review_module_file_draft_next_without_writing_or_importing_module"
    parser_module_file_draft_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    checks_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_VALIDATION_JSON)
    module_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_JSON)
    draft_content = build_parser_module_file_draft_content(module_payload)
    parser_module_file_draft_count = draft_content["parser_module_file_draft_count"]
    guard_functions = draft_content["guard_functions"]
    accepted_decision_types = draft_content["accepted_decision_types"]
    result_fields = draft_content["result_fields"]
    refusal_reasons = draft_content["refusal_reasons"]
    fixture_coverage = draft_content["fixture_coverage"]
    module_source = draft_content["module_source"]
    module_source_line_count = draft_content["module_source_line_count"]
    guard_function_count = draft_content["guard_function_count"]
    accepted_decision_type_count = draft_content["accepted_decision_type_count"]
    result_field_count = draft_content["result_field_count"]
    refusal_reason_count = draft_content["refusal_reason_count"]
    fixture_coverage_count = draft_content["fixture_coverage_count"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_checks_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_checks_task_id,),
    ).fetchone()
    source_checks_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_checks_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (file_draft_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (file_draft_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_checks_task or source_checks_task["status"] != "complete":
        failures.append("source module fixture checks task is missing or incomplete")
    if not source_checks_evidence or source_checks_evidence["status"] != "local_agent_company_migration_decision_module_fixture_checks_complete":
        failures.append("source module fixture checks evidence is missing or not complete")
    if not checks_validation.get("all_checks_passed") or checks_validation.get("failure_count") != 0:
        failures.append("source module fixture checks validation is not clean")
    if parser_module_file_draft_count != 1:
        failures.append(f"expected 1 parser module file draft, got {parser_module_file_draft_count}")
    if module_source_line_count != 80:
        failures.append(f"expected 80 module source lines, got {module_source_line_count}")
    if guard_function_count != 9:
        failures.append(f"expected 9 guard functions, got {guard_function_count}")
    if accepted_decision_type_count != 4:
        failures.append(f"expected 4 accepted decision types, got {accepted_decision_type_count}")
    if result_field_count != 8:
        failures.append(f"expected 8 result fields, got {result_field_count}")
    if refusal_reason_count != 8:
        failures.append(f"expected 8 refusal reasons, got {refusal_reason_count}")
    if fixture_coverage_count != 12:
        failures.append(f"expected 12 fixture coverage rows, got {fixture_coverage_count}")
    if target_task_exists_before:
        failures.append(f"target parser module file draft task already exists: {file_draft_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"parser module file draft evidence already exists: {file_draft_evidence_id}")
    if tasks_table_rows_before != 237:
        failures.append(f"expected 237 task rows before parser module file draft, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 145:
        failures.append(f"expected 145 evidence rows before parser module file draft, got {lane_evidence_rows_before}")

    summary = "Drafted the parser module file contents as a report-only artifact, including allowed decisions, guards, result builder, and parse entrypoint without writing an importable file."
    next_action = "Static-review the parser module file draft next; do not write, install, import, or run it."
    runtime_boundary = {
        "parser_module_file_written": False,
        "parser_module_imported": False,
        "live_decisions_parsed": False,
        "operator_decision_applied": False,
        "migration_sql_executed": False,
        "apply_command_enabled": False,
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
        "schema_version": "agent_company.migration_decision_parser_module_file_draft.v1",
        "generated_utc": generated_utc,
        "file_draft_lane_id": lane_id,
        "file_draft_task_id": file_draft_task_id,
        "file_draft_evidence_id": file_draft_evidence_id,
        "source_checks_task_id": source_checks_task_id,
        "source_checks_evidence_id": source_checks_evidence_id,
        "parser_module_file_draft_count": parser_module_file_draft_count,
        "module_source_line_count": module_source_line_count,
        "guard_function_count": guard_function_count,
        "accepted_decision_type_count": accepted_decision_type_count,
        "result_field_count": result_field_count,
        "refusal_reason_count": refusal_reason_count,
        "fixture_coverage_count": fixture_coverage_count,
        "module_source": module_source,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Parser Module File Draft",
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
        "## Module Source Draft",
        "",
        "```python",
        module_source.rstrip(),
        "```",
        "",
        "## Boundary",
        "",
        "This is a report-only module file draft. It does not write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
        "",
        "## Next Action",
        "",
        next_action,
        "",
    ]
    output_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                file_draft_task_id,
                lane_id,
                "Create agent company migration decision parser module file draft",
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
                "evidence_id": file_draft_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser module file draft",
                "status": "local_agent_company_migration_decision_parser_module_file_draft_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from report-only module fixture checks; module source was drafted inside reports only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_after = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    tables_created = int(table_count_after) - int(table_count_before)
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_parser_module_file_draft = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (file_draft_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (file_draft_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (file_draft_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_module_file_draft != 1:
        failures.append(f"expected 1 task row inserted by parser module file draft, got {task_rows_inserted_by_parser_module_file_draft}")
    if tasks_table_rows_after != 238:
        failures.append(f"expected 238 task rows after parser module file draft, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 146:
        failures.append(f"expected 146 evidence rows after parser module file draft, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("parser module file draft evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by parser module file draft, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during parser module file draft")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_module_file_draft": task_rows_inserted_by_parser_module_file_draft,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_module_file_draft_validation.v1",
        "generated_utc": generated_utc,
        "file_draft_path": str(json_output_path),
        "file_draft_lane_id": lane_id,
        "file_draft_task_id": file_draft_task_id,
        "source_checks_task_id": source_checks_task_id,
        "parser_module_file_draft_count": parser_module_file_draft_count,
        "module_source_line_count": module_source_line_count,
        "guard_function_count": guard_function_count,
        "accepted_decision_type_count": accepted_decision_type_count,
        "result_field_count": result_field_count,
        "refusal_reason_count": refusal_reason_count,
        "fixture_coverage_count": fixture_coverage_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_module_file_draft": task_rows_inserted_by_parser_module_file_draft,
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
                "file_draft_lane_id": lane_id,
                "file_draft_task_id": file_draft_task_id,
                "module_source_line_count": module_source_line_count,
                "guard_function_count": guard_function_count,
                "accepted_decision_type_count": accepted_decision_type_count,
                "result_field_count": result_field_count,
                "refusal_reason_count": refusal_reason_count,
                "fixture_coverage_count": fixture_coverage_count,
                "task_rows_inserted_by_parser_module_file_draft": task_rows_inserted_by_parser_module_file_draft,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


