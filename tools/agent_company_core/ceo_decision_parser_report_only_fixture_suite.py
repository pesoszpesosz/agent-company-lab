from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .constants import (
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_DRY_RUN_CONTRACT_JSON,
    CEO_DECISION_PARSER_DRY_RUN_CONTRACT_REPORT,
    CEO_DECISION_PARSER_DRY_RUN_CONTRACT_VALIDATION_JSON,
    CEO_DECISION_PARSER_FIXTURE_SUITE_JSON,
    CEO_DECISION_PARSER_FIXTURE_SUITE_REPORT,
    CEO_DECISION_PARSER_FIXTURE_SUITE_VALIDATION_JSON,
    CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_PREFLIGHT_JSON,
    CEO_DECISION_PARSER_PREFLIGHT_REPORT,
    CEO_DECISION_PARSER_PREFLIGHT_VALIDATION_JSON,
    CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_JSON,
    CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_REPORT,
    CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_VALIDATION_JSON,
    CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_JSON,
    CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_REPORT,
    CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar

def write_ceo_decision_parser_fixture_suite(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_FIXTURE_SUITE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_FIXTURE_SUITE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_FIXTURE_SUITE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    suite_task_id = "task-ceo-decision-parser-fixture-suite-20260616"
    suite_evidence_id = "ceo-decision-parser-fixture-suite-20260616"
    source_negative_task_id = "task-ceo-decision-intake-negative-fixtures-20260616"
    source_negative_evidence_id = "ceo-decision-intake-negative-fixtures-20260616"
    source_positive_task_id = "task-ceo-decision-parser-positive-fixture-20260616"
    source_positive_evidence_id = "ceo-decision-parser-positive-fixture-20260616"
    duplicate_key = "ceo-decision-parser-fixture-suite-20260616"
    local_decision = "ceo_decision_parser_fixture_suite_ready_parser_not_executed"
    recommended_default = "pass_fixture_suite_before_parser_execution"
    parser_execution_count = 0
    accepted_decision_count = 0
    approval_request_count = 0
    runnable_without_approval_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_negative_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_negative_task_id,)).fetchone()
    source_negative_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_negative_evidence_id,),
    ).fetchone()
    source_positive_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_positive_task_id,)).fetchone()
    source_positive_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_positive_evidence_id,),
    ).fetchone()
    negative_validation = load_json(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON)
    negative_payload = load_json(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON)
    positive_validation = load_json(CEO_DECISION_PARSER_POSITIVE_FIXTURE_VALIDATION_JSON)
    positive_payload = load_json(CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON)

    negative_fixture_count = int(negative_payload.get("negative_fixture_count", 0))
    positive_fixture_count = int(positive_payload.get("positive_fixture_count", 0))
    expected_rejection_count = int(negative_payload.get("expected_rejection_count", 0))
    expected_dry_run_preview_count = int(positive_payload.get("expected_dry_run_preview_count", 0))
    fixture_suite_count = negative_fixture_count + positive_fixture_count
    suite_entries = [
        {
            "suite_entry_id": "negative-fixtures",
            "source_path": str(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON),
            "fixture_count": negative_fixture_count,
            "expected_result": "reject_all",
        },
        {
            "suite_entry_id": "positive-fixture",
            "source_path": str(CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON),
            "fixture_count": positive_fixture_count,
            "expected_result": "dry_run_preview_only",
            "expected_preview_state": positive_payload.get("expected_preview_state"),
        },
    ]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (suite_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    suite_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (suite_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_negative_task or source_negative_task["status"] != "complete":
        failures.append("source negative fixtures task is missing or incomplete")
    if not source_negative_evidence or source_negative_evidence["status"] != "local_ceo_decision_intake_negative_fixtures_complete":
        failures.append("source negative fixtures evidence is missing or not complete")
    if not source_positive_task or source_positive_task["status"] != "complete":
        failures.append("source positive fixture task is missing or incomplete")
    if not source_positive_evidence or source_positive_evidence["status"] != "local_ceo_decision_parser_positive_fixture_complete":
        failures.append("source positive fixture evidence is missing or not complete")
    if not negative_validation.get("all_checks_passed") or negative_validation.get("failure_count") != 0:
        failures.append("source negative fixtures validation is not clean")
    if not positive_validation.get("all_checks_passed") or positive_validation.get("failure_count") != 0:
        failures.append("source positive fixture validation is not clean")
    if negative_fixture_count != 6:
        failures.append(f"expected 6 negative fixtures, got {negative_fixture_count}")
    if positive_fixture_count != 1:
        failures.append(f"expected 1 positive fixture, got {positive_fixture_count}")
    if fixture_suite_count != 7:
        failures.append(f"expected 7 suite fixtures, got {fixture_suite_count}")
    if expected_rejection_count != 6:
        failures.append(f"expected 6 expected rejections, got {expected_rejection_count}")
    if expected_dry_run_preview_count != 1:
        failures.append(f"expected 1 expected dry-run preview, got {expected_dry_run_preview_count}")
    if parser_execution_count != 0:
        failures.append(f"expected 0 parser executions, got {parser_execution_count}")
    if accepted_decision_count != 0:
        failures.append(f"expected 0 accepted decisions, got {accepted_decision_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser fixture suite task already exists: {suite_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if suite_evidence_exists_before:
        failures.append(f"CEO decision parser fixture suite evidence already exists: {suite_evidence_id}")
    if tasks_table_rows_before != 197:
        failures.append(f"expected 197 task rows before CEO decision parser fixture suite, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 105:
        failures.append(f"expected 105 evidence rows before CEO decision parser fixture suite, got {lane_evidence_rows_before}")

    suite_summary = (
        "Created a local parser fixture-suite manifest combining six negative fixtures and one positive dry-run fixture. A future parser must pass the suite before any queue mutation path is allowed."
    )
    suite_next_action = (
        "Use this suite as the acceptance gate for a report-only parser; do not execute or apply parser results until the suite passes and mutation approval exists."
    )
    runtime_boundary = {
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
        "schema_version": "agent_company.ceo_decision_parser_fixture_suite.v1",
        "generated_utc": generated_utc,
        "suite_lane_id": lane_id,
        "suite_task_id": suite_task_id,
        "suite_evidence_id": suite_evidence_id,
        "source_negative_task_id": source_negative_task_id,
        "source_negative_evidence_id": source_negative_evidence_id,
        "source_positive_task_id": source_positive_task_id,
        "source_positive_evidence_id": source_positive_evidence_id,
        "source_negative_validation_path": str(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON),
        "source_positive_validation_path": str(CEO_DECISION_PARSER_POSITIVE_FIXTURE_VALIDATION_JSON),
        "negative_fixture_count": negative_fixture_count,
        "positive_fixture_count": positive_fixture_count,
        "fixture_suite_count": fixture_suite_count,
        "expected_rejection_count": expected_rejection_count,
        "expected_dry_run_preview_count": expected_dry_run_preview_count,
        "suite_entries": suite_entries,
        "parser_execution_count": parser_execution_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": suite_summary,
        "next_action": suite_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Fixture Suite",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        suite_summary,
        "",
        "## Suite Entries",
        "",
        "| Entry | Fixtures | Expected Result |",
        "| --- | --- | --- |",
    ]
    for entry in suite_entries:
        md_lines.append(f"| `{entry['suite_entry_id']}` | `{entry['fixture_count']}` | `{entry['expected_result']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local fixture-suite manifest only. It runs no parser, accepts no decision, approves nothing, and does not assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            suite_next_action,
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
                suite_task_id,
                lane_id,
                "Create CEO decision parser fixture suite",
                40,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                suite_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": suite_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser fixture suite",
                "status": "local_ceo_decision_parser_fixture_suite_complete",
                "summary": suite_summary,
                "next_action": suite_next_action,
                "ownership_note": "Generated by platform_engineering from parser positive/negative fixtures; suite is local validation data only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_suite = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (suite_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (suite_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (suite_task_id,)) else 0
    if task_rows_inserted_by_suite != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser fixture suite, got {task_rows_inserted_by_suite}")
    if tasks_table_rows_after != 198:
        failures.append(f"expected 198 task rows after CEO decision parser fixture suite, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 106:
        failures.append(f"expected 106 evidence rows after CEO decision parser fixture suite, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser fixture suite evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser fixture suite")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_suite": task_rows_inserted_by_suite,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_fixture_suite_validation.v1",
        "generated_utc": generated_utc,
        "suite_path": str(json_output_path),
        "suite_lane_id": lane_id,
        "suite_task_id": suite_task_id,
        "source_negative_task_id": source_negative_task_id,
        "source_positive_task_id": source_positive_task_id,
        "negative_fixture_count": negative_fixture_count,
        "positive_fixture_count": positive_fixture_count,
        "fixture_suite_count": fixture_suite_count,
        "expected_rejection_count": expected_rejection_count,
        "expected_dry_run_preview_count": expected_dry_run_preview_count,
        "parser_execution_count": parser_execution_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_suite": task_rows_inserted_by_suite,
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
                "suite_lane_id": lane_id,
                "suite_task_id": suite_task_id,
                "fixture_suite_count": fixture_suite_count,
                "task_rows_inserted_by_suite": task_rows_inserted_by_suite,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
