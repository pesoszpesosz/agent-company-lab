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
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .agent_company_migration_write_decision_runner_content import build_parser_write_decision_runner_content
from .agent_company_migration_write_decision_runner_evaluator import evaluate_parser_write_decision_fixture


def write_agent_company_migration_decision_parser_write_decision_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_RUNNER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    runner_task_id = "task-agent-company-migration-decision-parser-write-decision-runner-20260616"
    runner_evidence_id = "agent-company-migration-decision-parser-write-decision-runner-20260616"
    source_fixture_task_id = "task-agent-company-migration-decision-parser-write-decision-fixture-suite-20260616"
    source_fixture_evidence_id = "agent-company-migration-decision-parser-write-decision-fixture-suite-20260616"
    duplicate_key = "agent-company-migration-decision-parser-write-decision-runner-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    fixture_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_FIXTURE_SUITE_VALIDATION_JSON)
    fixture_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_WRITE_DECISION_FIXTURE_SUITE_JSON)
    fixtures = fixture_payload.get("fixtures", [])
    parser_guards = fixture_payload.get("parser_guards", [])
    output_states = fixture_payload.get("output_states", [])
    required_fields = set(fixture_payload.get("required_fields", []))
    expected_target_path = fixture_payload.get("expected_target_path")
    expected_source_artifact_path = fixture_payload.get("expected_source_artifact_path")
    expected_source_review_path = fixture_payload.get("expected_source_review_path")
    accepted_decision_types = {"hold", "approve_one_parser_file_write_only", "request_runner_review_rework", "reject_parser_write"}

    fixture_results = [
        evaluate_parser_write_decision_fixture(
            item,
            required_fields=required_fields,
            expected_target_path=expected_target_path,
            expected_source_artifact_path=expected_source_artifact_path,
            expected_source_review_path=expected_source_review_path,
            accepted_decision_types=accepted_decision_types,
        )
        for item in fixtures
    ]
    parser_guard_count = len(parser_guards)
    output_state_count = len(output_states)
    runner_content = build_parser_write_decision_runner_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        lane_id=lane_id,
        runner_task_id=runner_task_id,
        runner_evidence_id=runner_evidence_id,
        source_fixture_task_id=source_fixture_task_id,
        source_fixture_evidence_id=source_fixture_evidence_id,
        fixture_results=fixture_results,
        parser_guard_count=parser_guard_count,
        output_state_count=output_state_count,
    )
    parser_write_decision_runner_count = runner_content["parser_write_decision_runner_count"]
    fixture_suite_count = runner_content["fixture_suite_count"]
    fixtures_evaluated = runner_content["fixtures_evaluated"]
    accepted_result_count = runner_content["accepted_result_count"]
    rejected_result_count = runner_content["rejected_result_count"]
    passed_fixture_count = runner_content["passed_fixture_count"]
    failed_fixture_count = runner_content["failed_fixture_count"]
    local_decision = runner_content["local_decision"]
    recommended_default = runner_content["recommended_default"]
    summary = runner_content["summary"]
    next_action = runner_content["next_action"]
    runtime_boundary = runner_content["runtime_boundary"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_fixture_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_fixture_task_id,),
    ).fetchone()
    source_fixture_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_fixture_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_fixture_task or source_fixture_task["status"] != "complete":
        failures.append("source parser write fixture suite task is missing or incomplete")
    if not source_fixture_evidence or source_fixture_evidence["status"] != "local_agent_company_migration_decision_parser_write_decision_fixture_suite_complete":
        failures.append("source parser write fixture suite evidence is missing or not complete")
    if not fixture_validation.get("all_checks_passed") or fixture_validation.get("failure_count") != 0:
        failures.append("source parser write fixture suite validation is not clean")
    if fixture_payload.get("recommended_default") != "build_report_only_parser_write_decision_runner_next_without_writing_parser":
        failures.append("source parser write fixture suite default does not point to runner")
    if parser_write_decision_runner_count != 1:
        failures.append(f"expected 1 parser write decision runner, got {parser_write_decision_runner_count}")
    if fixture_suite_count != 12:
        failures.append(f"expected 12 fixture cases, got {fixture_suite_count}")
    if fixtures_evaluated != 12:
        failures.append(f"expected 12 evaluated fixtures, got {fixtures_evaluated}")
    if accepted_result_count != 4:
        failures.append(f"expected 4 accepted fixture results, got {accepted_result_count}")
    if rejected_result_count != 8:
        failures.append(f"expected 8 rejected fixture results, got {rejected_result_count}")
    if passed_fixture_count != 12:
        failures.append(f"expected 12 passed fixtures, got {passed_fixture_count}")
    if failed_fixture_count != 0:
        failures.append(f"expected 0 failed fixtures, got {failed_fixture_count}")
    if parser_guard_count != 9:
        failures.append(f"expected 9 parser guards, got {parser_guard_count}")
    if output_state_count != 4:
        failures.append(f"expected 4 output states, got {output_state_count}")
    if target_task_exists_before:
        failures.append(f"target parser write decision runner task already exists: {runner_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"parser write decision runner evidence already exists: {runner_evidence_id}")
    if tasks_table_rows_before != 247:
        failures.append(f"expected 247 task rows before parser write decision runner, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 155:
        failures.append(f"expected 155 evidence rows before parser write decision runner, got {lane_evidence_rows_before}")

    payload = runner_content["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(runner_content["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                runner_task_id,
                lane_id,
                "Create agent company migration decision parser write decision runner",
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
                "evidence_id": runner_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser write decision runner",
                "status": "local_agent_company_migration_decision_parser_write_decision_runner_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from parser write decision fixture suite; no parser was written or imported.",
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
    task_rows_inserted_by_parser_write_decision_runner = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (runner_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_write_decision_runner != 1:
        failures.append(f"expected 1 task row inserted by parser write decision runner, got {task_rows_inserted_by_parser_write_decision_runner}")
    if tasks_table_rows_after != 248:
        failures.append(f"expected 248 task rows after parser write decision runner, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 156:
        failures.append(f"expected 156 evidence rows after parser write decision runner, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("parser write decision runner evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by parser write decision runner, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during parser write decision runner")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_write_decision_runner": task_rows_inserted_by_parser_write_decision_runner,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_write_decision_runner_validation.v1",
        "generated_utc": generated_utc,
        "runner_path": str(json_output_path),
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "source_fixture_task_id": source_fixture_task_id,
        "parser_write_decision_runner_count": parser_write_decision_runner_count,
        "fixture_suite_count": fixture_suite_count,
        "fixtures_evaluated": fixtures_evaluated,
        "accepted_result_count": accepted_result_count,
        "rejected_result_count": rejected_result_count,
        "passed_fixture_count": passed_fixture_count,
        "failed_fixture_count": failed_fixture_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_write_decision_runner": task_rows_inserted_by_parser_write_decision_runner,
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
                "runner_lane_id": lane_id,
                "runner_task_id": runner_task_id,
                "fixtures_evaluated": fixtures_evaluated,
                "accepted_result_count": accepted_result_count,
                "rejected_result_count": rejected_result_count,
                "passed_fixture_count": passed_fixture_count,
                "failed_fixture_count": failed_fixture_count,
                "task_rows_inserted_by_parser_write_decision_runner": task_rows_inserted_by_parser_write_decision_runner,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

