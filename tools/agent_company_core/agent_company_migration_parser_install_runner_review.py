from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Parser install decision runner and review writers."""

from .agent_company_migration_parser_install_runner_review_content import build_install_decision_runner_review_content
from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_install_decision_runner_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    review_task_id = "task-agent-company-migration-decision-parser-install-decision-runner-review-20260616"
    review_evidence_id = "agent-company-migration-decision-parser-install-decision-runner-review-20260616"
    source_runner_task_id = "task-agent-company-migration-decision-parser-install-decision-runner-20260616"
    source_runner_evidence_id = "agent-company-migration-decision-parser-install-decision-runner-20260616"
    duplicate_key = "agent-company-migration-decision-parser-install-decision-runner-review-20260616"
    review_content = build_install_decision_runner_review_content(
        runner_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REPORT),
        runner_validation_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_VALIDATION_JSON),
        fixture_suite_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_REPORT),
        install_preflight_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT),
    )
    local_decision = review_content["local_decision"]
    recommended_default = review_content["recommended_default"]
    install_decision_runner_review_count = review_content["install_decision_runner_review_count"]
    runner_result_checks = review_content["runner_result_checks"]
    approval_conditions = review_content["approval_conditions"]
    hold_conditions = review_content["hold_conditions"]
    evidence_links = review_content["evidence_links"]
    operator_instructions = review_content["operator_instructions"]
    runner_result_check_count = review_content["runner_result_check_count"]
    approval_condition_count = review_content["approval_condition_count"]
    hold_condition_count = review_content["hold_condition_count"]
    evidence_link_count = review_content["evidence_link_count"]
    operator_instruction_count = review_content["operator_instruction_count"]
    summary = review_content["summary"]
    next_action = review_content["next_action"]
    runtime_boundary = review_content["runtime_boundary"].copy()
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    runner_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_VALIDATION_JSON)
    runner_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_JSON)
    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_runner_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_runner_task_id,),
    ).fetchone()
    source_runner_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_runner_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (review_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (review_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_runner_task or source_runner_task["status"] != "complete":
        failures.append("source install decision runner task is missing or incomplete")
    if not source_runner_evidence or source_runner_evidence["status"] != "local_agent_company_migration_decision_parser_install_decision_runner_complete":
        failures.append("source install decision runner evidence is missing or not complete")
    if not runner_validation.get("all_checks_passed") or runner_validation.get("failure_count") != 0:
        failures.append("source install decision runner validation is not clean")
    if runner_payload.get("recommended_default") != "review_report_only_runner_results_next_without_writing_or_importing_parser":
        failures.append("source install decision runner default does not point to review")
    if runner_payload.get("fixtures_evaluated") != 11 or runner_payload.get("passed_fixture_count") != 11:
        failures.append("source install decision runner did not pass all 11 fixtures")
    if runner_payload.get("accepted_result_count") != 4 or runner_payload.get("rejected_result_count") != 7:
        failures.append("source install decision runner accept/reject counts are not 4/7")
    runtime = runner_payload.get("runtime_boundary", {})
    if runtime.get("parser_module_file_written") or runtime.get("parser_module_imported") or runtime.get("live_decisions_parsed"):
        failures.append("source install decision runner crossed parser write/import/live-parse boundary")
    if runtime.get("service_requests_updated") or runtime.get("service_requests_assigned") or runtime.get("external_side_effects"):
        failures.append("source install decision runner mutated service requests or external state")
    if install_decision_runner_review_count != 1:
        failures.append(f"expected 1 install decision runner review, got {install_decision_runner_review_count}")
    if runner_result_check_count != 6:
        failures.append(f"expected 6 runner result checks, got {runner_result_check_count}")
    if approval_condition_count != 6:
        failures.append(f"expected 6 approval conditions, got {approval_condition_count}")
    if hold_condition_count != 6:
        failures.append(f"expected 6 hold conditions, got {hold_condition_count}")
    if evidence_link_count != 4:
        failures.append(f"expected 4 evidence links, got {evidence_link_count}")
    if operator_instruction_count != 6:
        failures.append(f"expected 6 operator instructions, got {operator_instruction_count}")
    if target_task_exists_before:
        failures.append(f"target install decision runner review task already exists: {review_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"install decision runner review evidence already exists: {review_evidence_id}")
    if tasks_table_rows_before != 244:
        failures.append(f"expected 244 task rows before install decision runner review, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 152:
        failures.append(f"expected 152 evidence rows before install decision runner review, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.migration_decision_parser_install_decision_runner_review.v1",
        "generated_utc": generated_utc,
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "review_evidence_id": review_evidence_id,
        "source_runner_task_id": source_runner_task_id,
        "source_runner_evidence_id": source_runner_evidence_id,
        "install_decision_runner_review_count": install_decision_runner_review_count,
        "runner_result_check_count": runner_result_check_count,
        "approval_condition_count": approval_condition_count,
        "hold_condition_count": hold_condition_count,
        "evidence_link_count": evidence_link_count,
        "operator_instruction_count": operator_instruction_count,
        "runner_result_checks": runner_result_checks,
        "approval_conditions": approval_conditions,
        "hold_conditions": hold_conditions,
        "evidence_links": evidence_links,
        "operator_instructions": operator_instructions,
        "runner_result_summary": {
            "fixtures_evaluated": runner_payload.get("fixtures_evaluated"),
            "accepted_result_count": runner_payload.get("accepted_result_count"),
            "rejected_result_count": runner_payload.get("rejected_result_count"),
            "passed_fixture_count": runner_payload.get("passed_fixture_count"),
            "failed_fixture_count": runner_payload.get("failed_fixture_count"),
        },
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Parser Install Decision Runner Review",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        summary,
        "",
        "## Runner Result Checks",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in runner_result_checks)
    md_lines.extend(["", "## Approval Conditions", ""])
    md_lines.extend(f"- {item}" for item in approval_conditions)
    md_lines.extend(["", "## Hold Conditions", ""])
    md_lines.extend(f"- {item}" for item in hold_conditions)
    md_lines.extend(["", "## Operator Instructions", ""])
    md_lines.extend(f"- {item}" for item in operator_instructions)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only runner review packet. It does not apply an install decision, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                "Create agent company migration decision parser install decision runner review",
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
                "title": "Agent company migration decision parser install decision runner review",
                "status": "local_agent_company_migration_decision_parser_install_decision_runner_review_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from install decision runner results; no parser write approval was granted.",
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
    task_rows_inserted_by_install_decision_runner_review = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (review_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (review_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (review_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_install_decision_runner_review != 1:
        failures.append(f"expected 1 task row inserted by install decision runner review, got {task_rows_inserted_by_install_decision_runner_review}")
    if tasks_table_rows_after != 245:
        failures.append(f"expected 245 task rows after install decision runner review, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 153:
        failures.append(f"expected 153 evidence rows after install decision runner review, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("install decision runner review evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by install decision runner review, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during install decision runner review")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_install_decision_runner_review": task_rows_inserted_by_install_decision_runner_review,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_install_decision_runner_review_validation.v1",
        "generated_utc": generated_utc,
        "review_path": str(json_output_path),
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "source_runner_task_id": source_runner_task_id,
        "install_decision_runner_review_count": install_decision_runner_review_count,
        "runner_result_check_count": runner_result_check_count,
        "approval_condition_count": approval_condition_count,
        "hold_condition_count": hold_condition_count,
        "evidence_link_count": evidence_link_count,
        "operator_instruction_count": operator_instruction_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_install_decision_runner_review": task_rows_inserted_by_install_decision_runner_review,
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
                "runner_result_check_count": runner_result_check_count,
                "approval_condition_count": approval_condition_count,
                "hold_condition_count": hold_condition_count,
                "operator_instruction_count": operator_instruction_count,
                "task_rows_inserted_by_install_decision_runner_review": task_rows_inserted_by_install_decision_runner_review,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


