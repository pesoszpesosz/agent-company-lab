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
from .agent_company_migration_write_application_fixture_content import (
    build_application_packet_fixture_suite,
    build_application_packet_fixture_suite_artifacts,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_FIXTURE_SUITE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_FIXTURE_SUITE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_FIXTURE_SUITE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite-20260616"
    fixture_evidence_id = "agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite-20260616"
    source_contract_task_id = "task-agent-company-migration-decision-parser-write-approval-response-application-packet-contract-20260616"
    source_contract_evidence_id = "agent-company-migration-decision-parser-write-approval-response-application-packet-contract-20260616"
    duplicate_key = "agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite-20260616"
    application_allowed = False
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_contract_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_VALIDATION_JSON)
    source_contract_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PACKET_CONTRACT_JSON)
    approval_request_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_JSON)
    application_fields = source_contract_payload.get("application_fields", [])
    eligibility_rules = source_contract_payload.get("eligibility_rules", [])
    expected_target_path = approval_request_payload.get("target_path")
    expected_source_artifact_path = approval_request_payload.get("source_artifact_path")
    expected_source_preflight_path = str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_APPLICATION_PREFLIGHT_JSON)
    expected_source_runner_review_path = str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_JSON)
    expected_signed_response_artifact_path = str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_JSON)
    fixture_content = build_application_packet_fixture_suite(
        expected_target_path=expected_target_path,
        expected_source_artifact_path=expected_source_artifact_path,
        expected_source_preflight_path=expected_source_preflight_path,
        expected_source_runner_review_path=expected_source_runner_review_path,
        expected_signed_response_artifact_path=expected_signed_response_artifact_path,
    )
    fixture_artifacts = build_application_packet_fixture_suite_artifacts(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        lane_id=lane_id,
        fixture_task_id=fixture_task_id,
        fixture_evidence_id=fixture_evidence_id,
        source_contract_task_id=source_contract_task_id,
        source_contract_evidence_id=source_contract_evidence_id,
        application_fields=application_fields,
        eligibility_rules=eligibility_rules,
        application_allowed=application_allowed,
        fixture_content=fixture_content,
    )
    application_packet_guards = fixture_artifacts["application_packet_guards"]
    parser_write_approval_response_application_packet_fixture_suite_count = fixture_artifacts["parser_write_approval_response_application_packet_fixture_suite_count"]
    positive_fixture_count = fixture_artifacts["positive_fixture_count"]
    negative_fixture_count = fixture_artifacts["negative_fixture_count"]
    application_field_count = fixture_artifacts["application_field_count"]
    eligibility_rule_count = fixture_artifacts["eligibility_rule_count"]
    application_packet_guard_count = fixture_artifacts["application_packet_guard_count"]
    fixture_assertion_count = fixture_artifacts["fixture_assertion_count"]
    local_decision = fixture_artifacts["local_decision"]
    recommended_default = fixture_artifacts["recommended_default"]
    summary = fixture_artifacts["summary"]
    next_action = fixture_artifacts["next_action"]
    runtime_boundary = fixture_artifacts["runtime_boundary"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_contract_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_contract_task_id,),
    ).fetchone()
    source_contract_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_contract_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_contract_task or source_contract_task["status"] != "complete":
        failures.append("source approval response application packet contract task is missing or incomplete")
    if not source_contract_evidence or source_contract_evidence["status"] != "local_agent_company_migration_decision_parser_write_approval_response_application_packet_contract_complete":
        failures.append("source approval response application packet contract evidence is missing or not complete")
    if not source_contract_validation.get("all_checks_passed") or source_contract_validation.get("failure_count") != 0:
        failures.append("source approval response application packet contract validation is not clean")
    if source_contract_payload.get("recommended_default") != "wait_for_signed_approval_response_application_packet_without_applying":
        failures.append("source approval response application packet contract default does not point to signed packet hold")
    if source_contract_payload.get("application_allowed"):
        failures.append("source approval response application packet contract unexpectedly allows application")
    if parser_write_approval_response_application_packet_fixture_suite_count != 10:
        failures.append(f"expected 10 application packet fixtures, got {parser_write_approval_response_application_packet_fixture_suite_count}")
    if positive_fixture_count != 1:
        failures.append(f"expected 1 positive fixture, got {positive_fixture_count}")
    if negative_fixture_count != 9:
        failures.append(f"expected 9 negative fixtures, got {negative_fixture_count}")
    if application_field_count != 10:
        failures.append(f"expected 10 application fields, got {application_field_count}")
    if eligibility_rule_count != 8:
        failures.append(f"expected 8 eligibility rules, got {eligibility_rule_count}")
    if application_packet_guard_count != 10:
        failures.append(f"expected 10 application packet guards, got {application_packet_guard_count}")
    if fixture_assertion_count != 10:
        failures.append(f"expected 10 fixture assertions, got {fixture_assertion_count}")
    if application_allowed:
        failures.append("fixture suite should not allow application")
    if target_task_exists_before:
        failures.append(f"target approval response application packet fixture suite task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"approval response application packet fixture suite evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 256:
        failures.append(f"expected 256 task rows before approval response application packet fixture suite, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 164:
        failures.append(f"expected 164 evidence rows before approval response application packet fixture suite, got {lane_evidence_rows_before}")

    payload = fixture_artifacts["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(fixture_artifacts["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fixture_task_id,
                lane_id,
                "Create agent company migration decision parser write approval response application packet fixture suite",
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
                "evidence_id": fixture_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser write approval response application packet fixture suite",
                "status": "local_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from approval response application packet contract; fixtures were not executed.",
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
    task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite != 1:
        failures.append(f"expected 1 task row inserted by approval response application packet fixture suite, got {task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite}")
    if tasks_table_rows_after != 257:
        failures.append(f"expected 257 task rows after approval response application packet fixture suite, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 165:
        failures.append(f"expected 165 evidence rows after approval response application packet fixture suite, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("approval response application packet fixture suite evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by approval response application packet fixture suite, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during approval response application packet fixture suite")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite": task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_application_packet_fixture_suite_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_contract_task_id": source_contract_task_id,
        "parser_write_approval_response_application_packet_fixture_suite_count": parser_write_approval_response_application_packet_fixture_suite_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "application_field_count": application_field_count,
        "eligibility_rule_count": eligibility_rule_count,
        "application_packet_guard_count": application_packet_guard_count,
        "fixture_assertion_count": fixture_assertion_count,
        "application_allowed": application_allowed,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite": task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite,
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
                "fixture_lane_id": lane_id,
                "fixture_task_id": fixture_task_id,
                "parser_write_approval_response_application_packet_fixture_suite_count": parser_write_approval_response_application_packet_fixture_suite_count,
                "positive_fixture_count": positive_fixture_count,
                "negative_fixture_count": negative_fixture_count,
                "application_packet_guard_count": application_packet_guard_count,
                "task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite": task_rows_inserted_by_parser_write_approval_response_application_packet_fixture_suite,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


