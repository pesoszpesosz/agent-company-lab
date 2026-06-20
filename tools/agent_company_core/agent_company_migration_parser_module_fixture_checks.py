from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

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
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_module_fixture_checks(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_MODULE_FIXTURE_CHECKS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    checks_task_id = "task-agent-company-migration-decision-module-fixture-checks-20260616"
    checks_evidence_id = "agent-company-migration-decision-module-fixture-checks-20260616"
    source_module_task_id = "task-agent-company-migration-decision-parser-module-draft-20260616"
    source_module_evidence_id = "agent-company-migration-decision-parser-module-draft-20260616"
    duplicate_key = "agent-company-migration-decision-module-fixture-checks-20260616"
    local_decision = "agent_company_migration_decision_module_fixture_checks_ready_for_report_only_parser_module_file_draft"
    recommended_default = "draft_report_only_parser_module_file_next_without_installing_or_live_parsing"
    module_fixture_checks_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    module_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_VALIDATION_JSON)
    module_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_JSON)
    fixture_runner_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_JSON)
    module_sections = module_payload.get("module_sections", [])
    function_blocks = module_payload.get("function_blocks", [])
    guard_functions = module_payload.get("guard_functions", [])
    fixture_coverage = module_payload.get("fixture_coverage", [])
    fixture_results = fixture_runner_payload.get("fixture_results", [])
    check_cases = []
    for result in fixture_results:
        fixture_id = result.get("fixture_id")
        expected = result.get("expected")
        module_has_coverage = fixture_id in fixture_coverage
        module_has_parse_entry = "parse_report_only_decision" in function_blocks
        module_has_scope_guard = "guard_scope_boundaries" in function_blocks or "guard_no_live_apply_scope" in guard_functions
        module_has_result_builder = "build_report_only_result" in function_blocks
        passed = bool(module_has_coverage and module_has_parse_entry and module_has_scope_guard and module_has_result_builder)
        check_cases.append(
            {
                "fixture_id": fixture_id,
                "expected": expected,
                "module_has_coverage": module_has_coverage,
                "module_has_parse_entry": module_has_parse_entry,
                "module_has_scope_guard": module_has_scope_guard,
                "module_has_result_builder": module_has_result_builder,
                "passed": passed,
            }
        )
    check_case_count = len(check_cases)
    passed_check_count = sum(1 for item in check_cases if item["passed"])
    failed_check_count = check_case_count - passed_check_count
    module_section_count = len(module_sections)
    function_block_count = len(function_blocks)
    guard_function_count = len(guard_functions)
    fixture_coverage_count = len(fixture_coverage)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_module_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_module_task_id,),
    ).fetchone()
    source_module_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_module_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (checks_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (checks_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_module_task or source_module_task["status"] != "complete":
        failures.append("source parser module draft task is missing or incomplete")
    if not source_module_evidence or source_module_evidence["status"] != "local_agent_company_migration_decision_parser_module_draft_complete":
        failures.append("source parser module draft evidence is missing or not complete")
    if not module_validation.get("all_checks_passed") or module_validation.get("failure_count") != 0:
        failures.append("source parser module draft validation is not clean")
    if module_fixture_checks_count != 1:
        failures.append(f"expected 1 module fixture checks packet, got {module_fixture_checks_count}")
    if check_case_count != 12:
        failures.append(f"expected 12 check cases, got {check_case_count}")
    if passed_check_count != 12:
        failures.append(f"expected 12 passed checks, got {passed_check_count}")
    if failed_check_count != 0:
        failures.append(f"expected 0 failed checks, got {failed_check_count}")
    if module_section_count != 8:
        failures.append(f"expected 8 module sections, got {module_section_count}")
    if function_block_count != 9:
        failures.append(f"expected 9 function blocks, got {function_block_count}")
    if guard_function_count != 9:
        failures.append(f"expected 9 guard functions, got {guard_function_count}")
    if fixture_coverage_count != 12:
        failures.append(f"expected 12 fixture coverage rows, got {fixture_coverage_count}")
    if target_task_exists_before:
        failures.append(f"target module fixture checks task already exists: {checks_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"module fixture checks evidence already exists: {checks_evidence_id}")
    if tasks_table_rows_before != 236:
        failures.append(f"expected 236 task rows before module fixture checks, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 144:
        failures.append(f"expected 144 evidence rows before module fixture checks, got {lane_evidence_rows_before}")

    summary = "Checked the report-only parser module draft against all 12 migration decision fixtures; every fixture has coverage, parser entry, scope guard, and result builder support."
    next_action = "Draft the report-only parser module file next; do not install it or parse live decisions."
    runtime_boundary = {
        "report_only_module_checks_executed": True,
        "parser_module_file_written": False,
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
        "schema_version": "agent_company.migration_decision_module_fixture_checks.v1",
        "generated_utc": generated_utc,
        "checks_lane_id": lane_id,
        "checks_task_id": checks_task_id,
        "checks_evidence_id": checks_evidence_id,
        "source_module_task_id": source_module_task_id,
        "source_module_evidence_id": source_module_evidence_id,
        "module_fixture_checks_count": module_fixture_checks_count,
        "check_case_count": check_case_count,
        "passed_check_count": passed_check_count,
        "failed_check_count": failed_check_count,
        "module_section_count": module_section_count,
        "function_block_count": function_block_count,
        "guard_function_count": guard_function_count,
        "fixture_coverage_count": fixture_coverage_count,
        "check_cases": check_cases,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Module Fixture Checks",
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
        "## Check Results",
        "",
        f"- Check cases: {check_case_count}",
        f"- Passed: {passed_check_count}",
        f"- Failed: {failed_check_count}",
        "",
        "| Fixture | Expected | Covered | Entry | Scope Guard | Result Builder | Passed |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in check_cases:
        md_lines.append(f"| `{item['fixture_id']}` | `{item['expected']}` | `{item['module_has_coverage']}` | `{item['module_has_parse_entry']}` | `{item['module_has_scope_guard']}` | `{item['module_has_result_builder']}` | `{item['passed']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These are report-only module fixture checks. They do not write an importable parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                checks_task_id,
                lane_id,
                "Create agent company migration decision module fixture checks",
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
                "evidence_id": checks_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision module fixture checks",
                "status": "local_agent_company_migration_decision_module_fixture_checks_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the parser module draft; checks are report-only and no parser module was written.",
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
    task_rows_inserted_by_module_fixture_checks = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (checks_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (checks_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (checks_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_module_fixture_checks != 1:
        failures.append(f"expected 1 task row inserted by module fixture checks, got {task_rows_inserted_by_module_fixture_checks}")
    if tasks_table_rows_after != 237:
        failures.append(f"expected 237 task rows after module fixture checks, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 145:
        failures.append(f"expected 145 evidence rows after module fixture checks, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("module fixture checks evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by module fixture checks, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during module fixture checks")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_module_fixture_checks": task_rows_inserted_by_module_fixture_checks,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_module_fixture_checks_validation.v1",
        "generated_utc": generated_utc,
        "checks_path": str(json_output_path),
        "checks_lane_id": lane_id,
        "checks_task_id": checks_task_id,
        "source_module_task_id": source_module_task_id,
        "module_fixture_checks_count": module_fixture_checks_count,
        "check_case_count": check_case_count,
        "passed_check_count": passed_check_count,
        "failed_check_count": failed_check_count,
        "module_section_count": module_section_count,
        "function_block_count": function_block_count,
        "guard_function_count": guard_function_count,
        "fixture_coverage_count": fixture_coverage_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_module_fixture_checks": task_rows_inserted_by_module_fixture_checks,
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
                "checks_lane_id": lane_id,
                "checks_task_id": checks_task_id,
                "check_case_count": check_case_count,
                "passed_check_count": passed_check_count,
                "failed_check_count": failed_check_count,
                "task_rows_inserted_by_module_fixture_checks": task_rows_inserted_by_module_fixture_checks,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

