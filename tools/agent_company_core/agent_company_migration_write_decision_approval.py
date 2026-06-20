from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Write-side decision parser contract, fixture, runner, review, and approval request writers."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_FIXTURE_SUITE_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_FIXTURE_SUITE_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_FIXTURE_SUITE_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_INTAKE_CONTRACT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_INTAKE_CONTRACT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_INTAKE_CONTRACT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_VALIDATION_JSON,
)
from .agent_company_migration_write_decision_approval_content import build_parser_write_approval_request_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_write_approval_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    request_task_id = "task-agent-company-migration-decision-parser-write-approval-request-20260616"
    request_evidence_id = "agent-company-migration-decision-parser-write-approval-request-20260616"
    source_review_task_id = "task-agent-company-migration-decision-parser-write-decision-runner-review-20260616"
    source_review_evidence_id = "agent-company-migration-decision-parser-write-decision-runner-review-20260616"
    duplicate_key = "agent-company-migration-decision-parser-write-approval-request-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_review_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_VALIDATION_JSON)
    source_review_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_JSON)
    preflight_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_JSON)
    target_file = (preflight_payload.get("target_files") or [{}])[0]
    target_path = target_file.get("target_path")
    source_artifact_path = target_file.get("source_artifact")
    request_content = build_parser_write_approval_request_content(
        target_path=target_path,
        source_artifact_path=source_artifact_path,
        source_review_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_JSON),
        source_review_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_REPORT),
        source_review_validation_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_VALIDATION_JSON),
        source_runner_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REPORT),
        source_fixture_suite_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_FIXTURE_SUITE_REPORT),
        install_preflight_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT),
    )
    local_decision = request_content["local_decision"]
    recommended_default = request_content["recommended_default"]
    parser_write_approval_request_count = request_content["parser_write_approval_request_count"]
    approval_fields = request_content["approval_fields"]
    boundary_conditions = request_content["boundary_conditions"]
    refusal_triggers = request_content["refusal_triggers"]
    evidence_links = request_content["evidence_links"]
    operator_instructions = request_content["operator_instructions"]
    approval_field_count = request_content["approval_field_count"]
    boundary_condition_count = request_content["boundary_condition_count"]
    refusal_trigger_count = request_content["refusal_trigger_count"]
    evidence_link_count = request_content["evidence_link_count"]
    operator_instruction_count = request_content["operator_instruction_count"]
    summary = request_content["summary"]
    next_action = request_content["next_action"]
    runtime_boundary = request_content["runtime_boundary"]
    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_review_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_review_task_id,),
    ).fetchone()
    source_review_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_review_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (request_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (request_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_review_task or source_review_task["status"] != "complete":
        failures.append("source parser write runner review task is missing or incomplete")
    if not source_review_evidence or source_review_evidence["status"] != "local_agent_company_migration_decision_parser_write_decision_runner_review_complete":
        failures.append("source parser write runner review evidence is missing or not complete")
    if not source_review_validation.get("all_checks_passed") or source_review_validation.get("failure_count") != 0:
        failures.append("source parser write runner review validation is not clean")
    if source_review_payload.get("recommended_default") != recommended_default:
        failures.append("source parser write runner review default is not hold")
    if not target_path or not source_artifact_path:
        failures.append("parser write target path or source artifact is missing")
    if parser_write_approval_request_count != 1:
        failures.append(f"expected 1 parser write approval request, got {parser_write_approval_request_count}")
    if approval_field_count != 9:
        failures.append(f"expected 9 approval fields, got {approval_field_count}")
    if boundary_condition_count != 8:
        failures.append(f"expected 8 boundary conditions, got {boundary_condition_count}")
    if refusal_trigger_count != 8:
        failures.append(f"expected 8 refusal triggers, got {refusal_trigger_count}")
    if evidence_link_count != 5:
        failures.append(f"expected 5 evidence links, got {evidence_link_count}")
    if operator_instruction_count != 7:
        failures.append(f"expected 7 operator instructions, got {operator_instruction_count}")
    if target_task_exists_before:
        failures.append(f"target parser write approval request task already exists: {request_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"parser write approval request evidence already exists: {request_evidence_id}")
    if tasks_table_rows_before != 249:
        failures.append(f"expected 249 task rows before parser write approval request, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 157:
        failures.append(f"expected 157 evidence rows before parser write approval request, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_request.v1",
        "generated_utc": generated_utc,
        "request_lane_id": lane_id,
        "request_task_id": request_task_id,
        "request_evidence_id": request_evidence_id,
        "source_review_task_id": source_review_task_id,
        "source_review_evidence_id": source_review_evidence_id,
        "target_path": target_path,
        "source_artifact_path": source_artifact_path,
        "source_review_path": str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REVIEW_JSON),
        "parser_write_approval_request_count": parser_write_approval_request_count,
        "approval_field_count": approval_field_count,
        "boundary_condition_count": boundary_condition_count,
        "refusal_trigger_count": refusal_trigger_count,
        "evidence_link_count": evidence_link_count,
        "operator_instruction_count": operator_instruction_count,
        "approval_fields": approval_fields,
        "boundary_conditions": boundary_conditions,
        "refusal_triggers": refusal_triggers,
        "evidence_links": evidence_links,
        "operator_instructions": operator_instructions,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Parser Write Approval Request",
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
        "## Approval Fields",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in approval_fields)
    md_lines.extend(["", "## Boundary Conditions", ""])
    md_lines.extend(f"- {item}" for item in boundary_conditions)
    md_lines.extend(["", "## Refusal Triggers", ""])
    md_lines.extend(f"- {item}" for item in refusal_triggers)
    md_lines.extend(["", "## Operator Instructions", ""])
    md_lines.extend(f"- {item}" for item in operator_instructions)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only approval request packet. It does not grant approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                request_task_id,
                lane_id,
                "Create agent company migration decision parser write approval request",
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
                "evidence_id": request_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser write approval request",
                "status": "local_agent_company_migration_decision_parser_write_approval_request_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from parser write runner review; no parser write approval was granted.",
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
    task_rows_inserted_by_parser_write_approval_request = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (request_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (request_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (request_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_write_approval_request != 1:
        failures.append(f"expected 1 task row inserted by parser write approval request, got {task_rows_inserted_by_parser_write_approval_request}")
    if tasks_table_rows_after != 250:
        failures.append(f"expected 250 task rows after parser write approval request, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 158:
        failures.append(f"expected 158 evidence rows after parser write approval request, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("parser write approval request evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by parser write approval request, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during parser write approval request")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_write_approval_request": task_rows_inserted_by_parser_write_approval_request,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_request_validation.v1",
        "generated_utc": generated_utc,
        "request_path": str(json_output_path),
        "request_lane_id": lane_id,
        "request_task_id": request_task_id,
        "source_review_task_id": source_review_task_id,
        "parser_write_approval_request_count": parser_write_approval_request_count,
        "approval_field_count": approval_field_count,
        "boundary_condition_count": boundary_condition_count,
        "refusal_trigger_count": refusal_trigger_count,
        "evidence_link_count": evidence_link_count,
        "operator_instruction_count": operator_instruction_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_write_approval_request": task_rows_inserted_by_parser_write_approval_request,
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
                "request_lane_id": lane_id,
                "request_task_id": request_task_id,
                "approval_field_count": approval_field_count,
                "boundary_condition_count": boundary_condition_count,
                "refusal_trigger_count": refusal_trigger_count,
                "operator_instruction_count": operator_instruction_count,
                "task_rows_inserted_by_parser_write_approval_request": task_rows_inserted_by_parser_write_approval_request,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

