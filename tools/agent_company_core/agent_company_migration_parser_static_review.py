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


def write_agent_company_migration_decision_parser_static_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    review_task_id = "task-agent-company-migration-decision-parser-static-review-20260616"
    review_evidence_id = "agent-company-migration-decision-parser-static-review-20260616"
    source_file_draft_task_id = "task-agent-company-migration-decision-parser-module-file-draft-20260616"
    source_file_draft_evidence_id = "agent-company-migration-decision-parser-module-file-draft-20260616"
    duplicate_key = "agent-company-migration-decision-parser-static-review-20260616"
    local_decision = "agent_company_migration_decision_parser_static_review_ready_for_report_only_install_preflight"
    recommended_default = "draft_report_only_install_preflight_next_without_writing_or_importing_module"
    static_review_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    file_draft_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_VALIDATION_JSON)
    file_draft_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_JSON)
    module_source = str(file_draft_payload.get("module_source", ""))
    module_source_lines = module_source.rstrip("\n").splitlines()
    static_checks = [
        {"check_id": "has_report_only_docstring", "passed": "Report-only parser" in module_source},
        {"check_id": "has_allowed_decision_types", "passed": "ALLOWED_DECISION_TYPES" in module_source},
        {"check_id": "has_required_fields", "passed": "REQUIRED_FIELDS" in module_source},
        {"check_id": "has_json_object_guard", "passed": "def guard_json_object_only" in module_source},
        {"check_id": "has_scope_guard", "passed": "def guard_scope_boundaries" in module_source},
        {"check_id": "has_artifact_guard", "passed": "def guard_artifact_paths" in module_source},
        {"check_id": "has_expiration_signature_guard", "passed": "def guard_expiration_and_signature" in module_source},
        {"check_id": "has_result_builder", "passed": "def build_report_only_result" in module_source},
        {"check_id": "has_parse_entrypoint", "passed": "def parse_report_only_decision" in module_source},
        {"check_id": "result_always_report_only", "passed": "'report_only': True" in module_source},
        {"check_id": "no_apply_or_service_mutation_calls", "passed": all(token not in module_source for token in ["conn.execute", "requests.", "subprocess", "open("])},
    ]
    recommendations = [
        "Keep the first installed version behind a report-only command flag.",
        "Run the saved 12-fixture suite after writing any real module file.",
        "Require static review to pass before importing the parser module.",
        "Keep live operator decision parsing disabled until a signed operator approval exists.",
        "Preserve service request and migration boundaries as hard parser guards.",
    ]
    static_check_count = len(static_checks)
    passed_static_check_count = sum(1 for item in static_checks if item["passed"])
    failed_static_check_count = static_check_count - passed_static_check_count
    issues = [item["check_id"] for item in static_checks if not item["passed"]]
    issue_count = len(issues)
    recommendation_count = len(recommendations)
    module_source_line_count = len(module_source_lines)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_file_draft_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_file_draft_task_id,),
    ).fetchone()
    source_file_draft_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_file_draft_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (review_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (review_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_file_draft_task or source_file_draft_task["status"] != "complete":
        failures.append("source parser module file draft task is missing or incomplete")
    if not source_file_draft_evidence or source_file_draft_evidence["status"] != "local_agent_company_migration_decision_parser_module_file_draft_complete":
        failures.append("source parser module file draft evidence is missing or not complete")
    if not file_draft_validation.get("all_checks_passed") or file_draft_validation.get("failure_count") != 0:
        failures.append("source parser module file draft validation is not clean")
    if static_review_count != 1:
        failures.append(f"expected 1 static review, got {static_review_count}")
    if static_check_count != 11:
        failures.append(f"expected 11 static checks, got {static_check_count}")
    if passed_static_check_count != 11:
        failures.append(f"expected 11 passed static checks, got {passed_static_check_count}")
    if failed_static_check_count != 0:
        failures.append(f"expected 0 failed static checks, got {failed_static_check_count}")
    if issue_count != 0:
        failures.append(f"expected 0 static review issues, got {issue_count}")
    if recommendation_count != 5:
        failures.append(f"expected 5 recommendations, got {recommendation_count}")
    if module_source_line_count != 80:
        failures.append(f"expected 80 module source lines, got {module_source_line_count}")
    if target_task_exists_before:
        failures.append(f"target parser static review task already exists: {review_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"parser static review evidence already exists: {review_evidence_id}")
    if tasks_table_rows_before != 238:
        failures.append(f"expected 238 task rows before parser static review, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 146:
        failures.append(f"expected 146 evidence rows before parser static review, got {lane_evidence_rows_before}")

    summary = "Static-reviewed the report-only parser module file draft; all source checks passed and no issues were found without writing or importing a parser module."
    next_action = "Draft the report-only install preflight next; do not write, install, import, or run the parser module."
    runtime_boundary = {
        "static_review_executed": True,
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
        "schema_version": "agent_company.migration_decision_parser_static_review.v1",
        "generated_utc": generated_utc,
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "review_evidence_id": review_evidence_id,
        "source_file_draft_task_id": source_file_draft_task_id,
        "source_file_draft_evidence_id": source_file_draft_evidence_id,
        "static_review_count": static_review_count,
        "static_check_count": static_check_count,
        "passed_static_check_count": passed_static_check_count,
        "failed_static_check_count": failed_static_check_count,
        "issue_count": issue_count,
        "recommendation_count": recommendation_count,
        "module_source_line_count": module_source_line_count,
        "static_checks": static_checks,
        "issues": issues,
        "recommendations": recommendations,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Parser Static Review",
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
        "## Static Checks",
        "",
        "| Check | Passed |",
        "| --- | --- |",
    ]
    for item in static_checks:
        md_lines.append(f"| `{item['check_id']}` | `{item['passed']}` |")
    md_lines.extend(["", "## Recommendations", ""])
    md_lines.extend(f"- {item}" for item in recommendations)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only static review. It does not write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                review_task_id,
                lane_id,
                "Create agent company migration decision parser static review",
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
                "evidence_id": review_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser static review",
                "status": "local_agent_company_migration_decision_parser_static_review_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the parser module file draft; review is local/report-only and no module was written or imported.",
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
    task_rows_inserted_by_static_review = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (review_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (review_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (review_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_static_review != 1:
        failures.append(f"expected 1 task row inserted by static review, got {task_rows_inserted_by_static_review}")
    if tasks_table_rows_after != 239:
        failures.append(f"expected 239 task rows after static review, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 147:
        failures.append(f"expected 147 evidence rows after static review, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("parser static review evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by static review, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during static review")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_static_review": task_rows_inserted_by_static_review,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_static_review_validation.v1",
        "generated_utc": generated_utc,
        "review_path": str(json_output_path),
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "source_file_draft_task_id": source_file_draft_task_id,
        "static_review_count": static_review_count,
        "static_check_count": static_check_count,
        "passed_static_check_count": passed_static_check_count,
        "failed_static_check_count": failed_static_check_count,
        "issue_count": issue_count,
        "recommendation_count": recommendation_count,
        "module_source_line_count": module_source_line_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_static_review": task_rows_inserted_by_static_review,
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
                "review_lane_id": lane_id,
                "review_task_id": review_task_id,
                "static_check_count": static_check_count,
                "passed_static_check_count": passed_static_check_count,
                "failed_static_check_count": failed_static_check_count,
                "issue_count": issue_count,
                "recommendation_count": recommendation_count,
                "task_rows_inserted_by_static_review": task_rows_inserted_by_static_review,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

