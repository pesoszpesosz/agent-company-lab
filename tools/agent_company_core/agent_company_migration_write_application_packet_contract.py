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
from .agent_company_migration_write_application_packet_contract_content import build_application_packet_contract_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    contract_task_id = "task-agent-company-migration-decision-parser-write-approval-response-application-packet-contract-20260616"
    contract_evidence_id = "agent-company-migration-decision-parser-write-approval-response-application-packet-contract-20260616"
    source_preflight_task_id = "task-agent-company-migration-decision-parser-write-approval-response-application-preflight-20260616"
    source_preflight_evidence_id = "agent-company-migration-decision-parser-write-approval-response-application-preflight-20260616"
    duplicate_key = "agent-company-migration-decision-parser-write-approval-response-application-packet-contract-20260616"
    contract_content = build_application_packet_contract_content(
        application_preflight_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_REPORT),
        application_preflight_validation_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_VALIDATION_JSON),
        runner_review_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_REPORT),
        intake_contract_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_REPORT),
        approval_request_report_path=str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_REPORT),
    )
    local_decision = contract_content["local_decision"]
    recommended_default = contract_content["recommended_default"]
    parser_write_approval_response_application_packet_contract_count = contract_content["parser_write_approval_response_application_packet_contract_count"]
    application_allowed = contract_content["application_allowed"]
    application_fields = contract_content["application_fields"]
    eligibility_rules = contract_content["eligibility_rules"]
    blocked_actions = contract_content["blocked_actions"]
    hold_conditions = contract_content["hold_conditions"]
    evidence_links = contract_content["evidence_links"]
    application_field_count = contract_content["application_field_count"]
    eligibility_rule_count = contract_content["eligibility_rule_count"]
    blocked_action_count = contract_content["blocked_action_count"]
    hold_condition_count = contract_content["hold_condition_count"]
    evidence_link_count = contract_content["evidence_link_count"]
    summary = contract_content["summary"]
    next_action = contract_content["next_action"]
    runtime_boundary = contract_content["runtime_boundary"]
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_preflight_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_VALIDATION_JSON)
    source_preflight_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_JSON)


    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_preflight_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_preflight_task_id,),
    ).fetchone()
    source_preflight_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_preflight_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (contract_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (contract_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_preflight_task or source_preflight_task["status"] != "complete":
        failures.append("source approval response application preflight task is missing or incomplete")
    if not source_preflight_evidence or source_preflight_evidence["status"] != "local_agent_company_migration_decision_parser_write_approval_response_application_preflight_complete":
        failures.append("source approval response application preflight evidence is missing or not complete")
    if not source_preflight_validation.get("all_checks_passed") or source_preflight_validation.get("failure_count") != 0:
        failures.append("source approval response application preflight validation is not clean")
    if source_preflight_payload.get("recommended_default") != "keep_hold_until_signed_approval_response_application_packet_exists":
        failures.append("source approval response application preflight default does not point to packet contract")
    if source_preflight_payload.get("application_allowed"):
        failures.append("source preflight unexpectedly allows application")
    if parser_write_approval_response_application_packet_contract_count != 1:
        failures.append(f"expected 1 approval response application packet contract, got {parser_write_approval_response_application_packet_contract_count}")
    if application_field_count != 10:
        failures.append(f"expected 10 application fields, got {application_field_count}")
    if eligibility_rule_count != 8:
        failures.append(f"expected 8 eligibility rules, got {eligibility_rule_count}")
    if blocked_action_count != 12:
        failures.append(f"expected 12 blocked actions, got {blocked_action_count}")
    if hold_condition_count != 6:
        failures.append(f"expected 6 hold conditions, got {hold_condition_count}")
    if evidence_link_count != 5:
        failures.append(f"expected 5 evidence links, got {evidence_link_count}")
    if application_allowed:
        failures.append("application should not be allowed by the packet contract")
    if target_task_exists_before:
        failures.append(f"target approval response application packet contract task already exists: {contract_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"approval response application packet contract evidence already exists: {contract_evidence_id}")
    if tasks_table_rows_before != 255:
        failures.append(f"expected 255 task rows before approval response application packet contract, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 163:
        failures.append(f"expected 163 evidence rows before approval response application packet contract, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_packet_contract.v1",
        "generated_utc": generated_utc,
        "contract_lane_id": lane_id,
        "contract_task_id": contract_task_id,
        "contract_evidence_id": contract_evidence_id,
        "source_preflight_task_id": source_preflight_task_id,
        "source_preflight_evidence_id": source_preflight_evidence_id,
        "parser_write_approval_response_application_packet_contract_count": parser_write_approval_response_application_packet_contract_count,
        "application_field_count": application_field_count,
        "eligibility_rule_count": eligibility_rule_count,
        "blocked_action_count": blocked_action_count,
        "hold_condition_count": hold_condition_count,
        "evidence_link_count": evidence_link_count,
        "application_allowed": application_allowed,
        "application_fields": application_fields,
        "eligibility_rules": eligibility_rules,
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
        "# Agent Company Migration Decision Parser Write Approval Response Application Packet Contract",
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
        "## Application Fields",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in application_fields)
    md_lines.extend(["", "## Eligibility Rules", ""])
    md_lines.extend(f"- {item}" for item in eligibility_rules)
    md_lines.extend(["", "## Blocked Actions", ""])
    md_lines.extend(f"- {item}" for item in blocked_actions)
    md_lines.extend(["", "## Hold Conditions", ""])
    md_lines.extend(f"- {item}" for item in hold_conditions)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only application packet contract. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                contract_task_id,
                lane_id,
                "Create agent company migration decision parser write approval response application packet contract",
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
                "evidence_id": contract_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser write approval response application packet contract",
                "status": "local_agent_company_migration_decision_parser_write_approval_response_application_packet_contract_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from approval response application preflight; no approval response was applied.",
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
    task_rows_inserted_by_parser_write_approval_response_application_packet_contract = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (contract_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (contract_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (contract_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_write_approval_response_application_packet_contract != 1:
        failures.append(f"expected 1 task row inserted by approval response application packet contract, got {task_rows_inserted_by_parser_write_approval_response_application_packet_contract}")
    if tasks_table_rows_after != 256:
        failures.append(f"expected 256 task rows after approval response application packet contract, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 164:
        failures.append(f"expected 164 evidence rows after approval response application packet contract, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("approval response application packet contract evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by approval response application packet contract, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during approval response application packet contract")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_write_approval_response_application_packet_contract": task_rows_inserted_by_parser_write_approval_response_application_packet_contract,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_packet_contract_validation.v1",
        "generated_utc": generated_utc,
        "contract_path": str(json_output_path),
        "contract_lane_id": lane_id,
        "contract_task_id": contract_task_id,
        "source_preflight_task_id": source_preflight_task_id,
        "parser_write_approval_response_application_packet_contract_count": parser_write_approval_response_application_packet_contract_count,
        "application_field_count": application_field_count,
        "eligibility_rule_count": eligibility_rule_count,
        "blocked_action_count": blocked_action_count,
        "hold_condition_count": hold_condition_count,
        "evidence_link_count": evidence_link_count,
        "application_allowed": application_allowed,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_write_approval_response_application_packet_contract": task_rows_inserted_by_parser_write_approval_response_application_packet_contract,
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
                "contract_lane_id": lane_id,
                "contract_task_id": contract_task_id,
                "application_field_count": application_field_count,
                "eligibility_rule_count": eligibility_rule_count,
                "blocked_action_count": blocked_action_count,
                "hold_condition_count": hold_condition_count,
                "task_rows_inserted_by_parser_write_approval_response_application_packet_contract": task_rows_inserted_by_parser_write_approval_response_application_packet_contract,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


