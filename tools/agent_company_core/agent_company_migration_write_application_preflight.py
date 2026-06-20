from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
"""Approval-response application preflight, packet, fixture, runner, and review writers."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_FIXTURE_SUITE_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_FIXTURE_SUITE_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_FIXTURE_SUITE_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_RUNNER_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_VALIDATION_JSON,
)
from .agent_company_migration_write_application_preflight_content import build_application_preflight_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_write_approval_response_application_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    preflight_task_id = "task-agent-company-migration-decision-parser-write-approval-response-application-preflight-20260616"
    preflight_evidence_id = "agent-company-migration-decision-parser-write-approval-response-application-preflight-20260616"
    source_review_task_id = "task-agent-company-migration-decision-parser-write-approval-response-runner-review-20260616"
    source_review_evidence_id = "agent-company-migration-decision-parser-write-approval-response-runner-review-20260616"
    duplicate_key = "agent-company-migration-decision-parser-write-approval-response-application-preflight-20260616"
    preflight_content = build_application_preflight_content(
        runner_review_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_REPORT),
        runner_review_validation_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_VALIDATION_JSON),
        runner_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REPORT),
        approval_request_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_REPORT),
    )
    local_decision = preflight_content["local_decision"]
    recommended_default = preflight_content["recommended_default"]
    parser_write_approval_response_application_preflight_count = preflight_content["parser_write_approval_response_application_preflight_count"]
    signed_response_present = preflight_content["signed_response_present"]
    application_allowed = preflight_content["application_allowed"]
    prerequisite_checks = preflight_content["prerequisite_checks"]
    signed_response_requirements = preflight_content["signed_response_requirements"]
    blocked_actions = preflight_content["blocked_actions"]
    hold_conditions = preflight_content["hold_conditions"]
    evidence_links = preflight_content["evidence_links"]
    prerequisite_check_count = preflight_content["prerequisite_check_count"]
    signed_response_requirement_count = preflight_content["signed_response_requirement_count"]
    blocked_action_count = preflight_content["blocked_action_count"]
    hold_condition_count = preflight_content["hold_condition_count"]
    evidence_link_count = preflight_content["evidence_link_count"]
    summary = preflight_content["summary"]
    next_action = preflight_content["next_action"]
    runtime_boundary = preflight_content["runtime_boundary"]
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_review_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_VALIDATION_JSON)
    source_review_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_JSON)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_review_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_review_task_id,),
    ).fetchone()
    source_review_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_review_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_review_task or source_review_task["status"] != "complete":
        failures.append("source approval response runner review task is missing or incomplete")
    if not source_review_evidence or source_review_evidence["status"] != "local_agent_company_migration_decision_parser_write_approval_response_runner_review_complete":
        failures.append("source approval response runner review evidence is missing or not complete")
    if not source_review_validation.get("all_checks_passed") or source_review_validation.get("failure_count") != 0:
        failures.append("source approval response runner review validation is not clean")
    if source_review_payload.get("recommended_default") != "hold_without_signed_parser_write_approval_response_application":
        failures.append("source approval response runner review default is not hold")
    runner_summary = source_review_payload.get("runner_result_summary", {})
    if runner_summary.get("fixtures_evaluated") != 13 or runner_summary.get("passed_fixture_count") != 13:
        failures.append("source approval response runner review does not show all 13 fixtures passing")
    if runner_summary.get("accepted_result_count") != 4 or runner_summary.get("rejected_result_count") != 9:
        failures.append("source approval response runner review accept/reject counts are not 4/9")
    if parser_write_approval_response_application_preflight_count != 1:
        failures.append(f"expected 1 approval response application preflight, got {parser_write_approval_response_application_preflight_count}")
    if prerequisite_check_count != 7:
        failures.append(f"expected 7 prerequisite checks, got {prerequisite_check_count}")
    if signed_response_requirement_count != 8:
        failures.append(f"expected 8 signed response requirements, got {signed_response_requirement_count}")
    if blocked_action_count != 12:
        failures.append(f"expected 12 blocked actions, got {blocked_action_count}")
    if hold_condition_count != 6:
        failures.append(f"expected 6 hold conditions, got {hold_condition_count}")
    if evidence_link_count != 4:
        failures.append(f"expected 4 evidence links, got {evidence_link_count}")
    if signed_response_present:
        failures.append("signed response unexpectedly present")
    if application_allowed:
        failures.append("application should not be allowed without a signed response")
    if target_task_exists_before:
        failures.append(f"target approval response application preflight task already exists: {preflight_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"approval response application preflight evidence already exists: {preflight_evidence_id}")
    if tasks_table_rows_before != 254:
        failures.append(f"expected 254 task rows before approval response application preflight, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 162:
        failures.append(f"expected 162 evidence rows before approval response application preflight, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_preflight.v1",
        "generated_utc": generated_utc,
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "preflight_evidence_id": preflight_evidence_id,
        "source_review_task_id": source_review_task_id,
        "source_review_evidence_id": source_review_evidence_id,
        "parser_write_approval_response_application_preflight_count": parser_write_approval_response_application_preflight_count,
        "prerequisite_check_count": prerequisite_check_count,
        "signed_response_requirement_count": signed_response_requirement_count,
        "blocked_action_count": blocked_action_count,
        "hold_condition_count": hold_condition_count,
        "evidence_link_count": evidence_link_count,
        "signed_response_present": signed_response_present,
        "application_allowed": application_allowed,
        "prerequisite_checks": prerequisite_checks,
        "signed_response_requirements": signed_response_requirements,
        "blocked_actions": blocked_actions,
        "hold_conditions": hold_conditions,
        "evidence_links": evidence_links,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Parser Write Approval Response Application Preflight",
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
        "## Prerequisite Checks",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in prerequisite_checks)
    md_lines.extend(["", "## Required Signed Response Fields", ""])
    md_lines.extend(f"- `{item}`" for item in signed_response_requirements)
    md_lines.extend(["", "## Blocked Actions", ""])
    md_lines.extend(f"- {item}" for item in blocked_actions)
    md_lines.extend(["", "## Hold Conditions", ""])
    md_lines.extend(f"- {item}" for item in hold_conditions)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only application preflight. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                preflight_task_id,
                lane_id,
                "Create agent company migration decision parser write approval response application preflight",
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
                "evidence_id": preflight_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser write approval response application preflight",
                "status": "local_agent_company_migration_decision_parser_write_approval_response_application_preflight_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from approval response runner review; no signed response was applied.",
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
    task_rows_inserted_by_parser_write_approval_response_application_preflight = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (preflight_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_write_approval_response_application_preflight != 1:
        failures.append(f"expected 1 task row inserted by approval response application preflight, got {task_rows_inserted_by_parser_write_approval_response_application_preflight}")
    if tasks_table_rows_after != 255:
        failures.append(f"expected 255 task rows after approval response application preflight, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 163:
        failures.append(f"expected 163 evidence rows after approval response application preflight, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("approval response application preflight evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by approval response application preflight, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during approval response application preflight")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_write_approval_response_application_preflight": task_rows_inserted_by_parser_write_approval_response_application_preflight,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": str(json_output_path),
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "source_review_task_id": source_review_task_id,
        "parser_write_approval_response_application_preflight_count": parser_write_approval_response_application_preflight_count,
        "prerequisite_check_count": prerequisite_check_count,
        "signed_response_requirement_count": signed_response_requirement_count,
        "blocked_action_count": blocked_action_count,
        "hold_condition_count": hold_condition_count,
        "evidence_link_count": evidence_link_count,
        "signed_response_present": signed_response_present,
        "application_allowed": application_allowed,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_write_approval_response_application_preflight": task_rows_inserted_by_parser_write_approval_response_application_preflight,
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
                "preflight_lane_id": lane_id,
                "preflight_task_id": preflight_task_id,
                "prerequisite_check_count": prerequisite_check_count,
                "signed_response_requirement_count": signed_response_requirement_count,
                "blocked_action_count": blocked_action_count,
                "hold_condition_count": hold_condition_count,
                "task_rows_inserted_by_parser_write_approval_response_application_preflight": task_rows_inserted_by_parser_write_approval_response_application_preflight,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )



