from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Write-side approval-response fixture suite writer."""

from .agent_company_migration_write_approval_response_fixture_content import (
    build_approval_response_fixture_artifacts,
    build_approval_response_fixture_suite,
)
from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_REQUEST_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_FIXTURE_SUITE_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_FIXTURE_SUITE_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_FIXTURE_SUITE_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_RUNNER_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_write_approval_response_fixture_suite(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_FIXTURE_SUITE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_FIXTURE_SUITE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_FIXTURE_SUITE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-agent-company-migration-decision-parser-write-approval-response-fixture-suite-20260616"
    fixture_evidence_id = "agent-company-migration-decision-parser-write-approval-response-fixture-suite-20260616"
    source_intake_task_id = "task-agent-company-migration-decision-parser-write-approval-response-intake-contract-20260616"
    source_intake_evidence_id = "agent-company-migration-decision-parser-write-approval-response-intake-contract-20260616"
    duplicate_key = "agent-company-migration-decision-parser-write-approval-response-fixture-suite-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_intake_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_VALIDATION_JSON)
    source_intake_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_APPROVAL_RESPONSE_INTAKE_CONTRACT_JSON)
    required_fields = source_intake_payload.get("required_fields", [])
    response_guards = source_intake_payload.get("response_guards", [])
    output_states = source_intake_payload.get("output_states", [])
    expected_target_path = source_intake_payload.get("expected_target_path")
    expected_source_artifact_path = source_intake_payload.get("expected_source_artifact_path")
    expected_source_request_path = source_intake_payload.get("expected_source_request_path")
    accepted_response_types = source_intake_payload.get("accepted_response_types", [])
    fixture_content = build_approval_response_fixture_suite(
        positive_fixture_specs=source_intake_payload.get("positive_fixtures", []),
        expected_target_path=expected_target_path,
        expected_source_artifact_path=expected_source_artifact_path,
        expected_source_request_path=expected_source_request_path,
    )
    positive_fixtures = fixture_content["positive_fixtures"]
    negative_fixtures = fixture_content["negative_fixtures"]
    fixtures = fixture_content["fixtures"]
    parser_write_approval_response_fixture_suite_count = fixture_content[
        "parser_write_approval_response_fixture_suite_count"
    ]
    positive_fixture_count = fixture_content["positive_fixture_count"]
    negative_fixture_count = fixture_content["negative_fixture_count"]
    fixture_assertion_count = fixture_content["fixture_assertion_count"]
    required_field_count = len(required_fields)
    response_guard_count = len(response_guards)
    output_state_count = len(output_states)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_intake_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_intake_task_id,),
    ).fetchone()
    source_intake_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_intake_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_intake_task or source_intake_task["status"] != "complete":
        failures.append("source parser write approval response intake task is missing or incomplete")
    if not source_intake_evidence or source_intake_evidence["status"] != "local_agent_company_migration_decision_parser_write_approval_response_intake_contract_complete":
        failures.append("source parser write approval response intake evidence is missing or not complete")
    if not source_intake_validation.get("all_checks_passed") or source_intake_validation.get("failure_count") != 0:
        failures.append("source parser write approval response intake validation is not clean")
    if source_intake_payload.get("recommended_default") != "build_report_only_parser_write_approval_response_fixture_suite_next_without_applying_approval":
        failures.append("source parser write approval response intake default does not point to fixture suite")
    if accepted_response_types != ["hold", "approve_one_parser_file_write_only", "request_approval_request_rework", "reject_parser_write_request"]:
        failures.append(f"unexpected accepted approval response types: {accepted_response_types}")
    if parser_write_approval_response_fixture_suite_count != 13:
        failures.append(f"expected 13 approval response fixtures, got {parser_write_approval_response_fixture_suite_count}")
    if positive_fixture_count != 4:
        failures.append(f"expected 4 positive fixtures, got {positive_fixture_count}")
    if negative_fixture_count != 9:
        failures.append(f"expected 9 negative fixtures, got {negative_fixture_count}")
    if required_field_count != 10:
        failures.append(f"expected 10 required fields, got {required_field_count}")
    if response_guard_count != 10:
        failures.append(f"expected 10 response guards, got {response_guard_count}")
    if output_state_count != 4:
        failures.append(f"expected 4 output states, got {output_state_count}")
    if fixture_assertion_count != 13:
        failures.append(f"expected 13 fixture assertions, got {fixture_assertion_count}")
    if target_task_exists_before:
        failures.append(f"target approval response fixture suite task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"approval response fixture suite evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 251:
        failures.append(f"expected 251 task rows before approval response fixture suite, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 159:
        failures.append(f"expected 159 evidence rows before approval response fixture suite, got {lane_evidence_rows_before}")

    artifacts = build_approval_response_fixture_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        fixture_task_id=fixture_task_id,
        fixture_evidence_id=fixture_evidence_id,
        source_intake_task_id=source_intake_task_id,
        source_intake_evidence_id=source_intake_evidence_id,
        expected_target_path=expected_target_path,
        expected_source_artifact_path=expected_source_artifact_path,
        expected_source_request_path=expected_source_request_path,
        parser_write_approval_response_fixture_suite_count=parser_write_approval_response_fixture_suite_count,
        positive_fixture_count=positive_fixture_count,
        negative_fixture_count=negative_fixture_count,
        required_field_count=required_field_count,
        response_guard_count=response_guard_count,
        output_state_count=output_state_count,
        fixture_assertion_count=fixture_assertion_count,
        fixtures=fixtures,
        required_fields=required_fields,
        response_guards=response_guards,
        output_states=output_states,
    )
    payload = artifacts["payload"]
    summary = payload["summary"]
    next_action = payload["next_action"]
    local_decision = payload["local_decision"]
    recommended_default = payload["recommended_default"]
    runtime_boundary = payload["runtime_boundary"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(artifacts["markdown"], encoding="utf-8")

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
                "Create agent company migration decision parser write approval response fixture suite",
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
                "title": "Agent company migration decision parser write approval response fixture suite",
                "status": "local_agent_company_migration_decision_parser_write_approval_response_fixture_suite_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from parser write approval response intake contract; fixtures were not executed.",
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
    task_rows_inserted_by_parser_write_approval_response_fixture_suite = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_write_approval_response_fixture_suite != 1:
        failures.append(f"expected 1 task row inserted by approval response fixture suite, got {task_rows_inserted_by_parser_write_approval_response_fixture_suite}")
    if tasks_table_rows_after != 252:
        failures.append(f"expected 252 task rows after approval response fixture suite, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 160:
        failures.append(f"expected 160 evidence rows after approval response fixture suite, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("approval response fixture suite evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by approval response fixture suite, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during approval response fixture suite")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_write_approval_response_fixture_suite": task_rows_inserted_by_parser_write_approval_response_fixture_suite,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_write_approval_response_fixture_suite_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_intake_task_id": source_intake_task_id,
        "parser_write_approval_response_fixture_suite_count": parser_write_approval_response_fixture_suite_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "required_field_count": required_field_count,
        "response_guard_count": response_guard_count,
        "output_state_count": output_state_count,
        "fixture_assertion_count": fixture_assertion_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_write_approval_response_fixture_suite": task_rows_inserted_by_parser_write_approval_response_fixture_suite,
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
                "parser_write_approval_response_fixture_suite_count": parser_write_approval_response_fixture_suite_count,
                "positive_fixture_count": positive_fixture_count,
                "negative_fixture_count": negative_fixture_count,
                "fixture_assertion_count": fixture_assertion_count,
                "task_rows_inserted_by_parser_write_approval_response_fixture_suite": task_rows_inserted_by_parser_write_approval_response_fixture_suite,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


__all__ = [
    "write_agent_company_migration_decision_parser_write_approval_response_fixture_suite",
]
