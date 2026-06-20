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

def write_ceo_decision_parser_report_only_harness(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    harness_task_id = "task-ceo-decision-parser-report-only-harness-20260616"
    harness_evidence_id = "ceo-decision-parser-report-only-harness-20260616"
    source_suite_task_id = "task-ceo-decision-parser-fixture-suite-20260616"
    source_suite_evidence_id = "ceo-decision-parser-fixture-suite-20260616"
    duplicate_key = "ceo-decision-parser-report-only-harness-20260616"
    local_decision = "ceo_decision_parser_report_only_harness_ready_parser_not_run"
    recommended_default = "implement_report_only_parser_against_harness_before_mutations"
    parser_execution_count = 0
    accepted_decision_count = 0
    approval_request_count = 0
    queue_mutation_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_suite_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_suite_task_id,)).fetchone()
    source_suite_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_suite_evidence_id,),
    ).fetchone()
    suite_validation = load_json(CEO_DECISION_PARSER_FIXTURE_SUITE_VALIDATION_JSON)
    suite_payload = load_json(CEO_DECISION_PARSER_FIXTURE_SUITE_JSON)
    fixture_suite_count = int(suite_payload.get("fixture_suite_count", 0))
    negative_fixture_count = int(suite_payload.get("negative_fixture_count", 0))
    positive_fixture_count = int(suite_payload.get("positive_fixture_count", 0))
    expected_preview_state = ""
    for entry in suite_payload.get("suite_entries", []):
        if entry.get("suite_entry_id") == "positive-fixture":
            expected_preview_state = entry.get("expected_preview_state") or ""

    harness_cases = [
        {
            "case_id": "reject-negative-fixtures",
            "source": "negative-fixtures",
            "fixture_count": negative_fixture_count,
            "required_result": "all_negative_fixtures_rejected",
        },
        {
            "case_id": "positive-dry-run-preview",
            "source": "positive-fixture",
            "fixture_count": positive_fixture_count,
            "required_result": "exactly_one_dry_run_preview",
            "expected_preview_state": expected_preview_state,
        },
        {
            "case_id": "no-queue-mutations",
            "source": "runtime-boundary",
            "fixture_count": fixture_suite_count,
            "required_result": "service_requests_and_tasks_not_mutated_by_parser",
        },
        {
            "case_id": "no-approval-escalation",
            "source": "runtime-boundary",
            "fixture_count": fixture_suite_count,
            "required_result": "approval_request_count_stays_zero",
        },
        {
            "case_id": "no-external-side-effects",
            "source": "runtime-boundary",
            "fixture_count": fixture_suite_count,
            "required_result": "browser_api_public_account_wallet_payment_and_real_money_actions_stay_zero",
        },
    ]
    harness_case_count = len(harness_cases)
    required_pass_count = harness_case_count

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (harness_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    harness_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (harness_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_suite_task or source_suite_task["status"] != "complete":
        failures.append("source fixture-suite task is missing or incomplete")
    if not source_suite_evidence or source_suite_evidence["status"] != "local_ceo_decision_parser_fixture_suite_complete":
        failures.append("source fixture-suite evidence is missing or not complete")
    if not suite_validation.get("all_checks_passed") or suite_validation.get("failure_count") != 0:
        failures.append("source fixture-suite validation is not clean")
    if fixture_suite_count != 7:
        failures.append(f"expected 7 fixture-suite rows, got {fixture_suite_count}")
    if negative_fixture_count != 6:
        failures.append(f"expected 6 negative fixtures, got {negative_fixture_count}")
    if positive_fixture_count != 1:
        failures.append(f"expected 1 positive fixture, got {positive_fixture_count}")
    if expected_preview_state != "would_create_bounded_service_request_update":
        failures.append(f"unexpected positive fixture preview state: {expected_preview_state}")
    if harness_case_count != 5:
        failures.append(f"expected 5 harness cases, got {harness_case_count}")
    if required_pass_count != 5:
        failures.append(f"expected 5 required passes, got {required_pass_count}")
    if parser_execution_count != 0:
        failures.append(f"expected 0 parser executions, got {parser_execution_count}")
    if accepted_decision_count != 0:
        failures.append(f"expected 0 accepted decisions, got {accepted_decision_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser report-only harness task already exists: {harness_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if harness_evidence_exists_before:
        failures.append(f"CEO decision parser report-only harness evidence already exists: {harness_evidence_id}")
    if tasks_table_rows_before != 198:
        failures.append(f"expected 198 task rows before CEO decision parser report-only harness, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 106:
        failures.append(f"expected 106 evidence rows before CEO decision parser report-only harness, got {lane_evidence_rows_before}")

    harness_summary = (
        "Defined a local report-only acceptance harness for the future CEO decision parser. The harness requires all seven parser fixtures to pass while queue mutation, approval escalation, browser/API use, and external side effects remain disabled."
    )
    harness_next_action = (
        "Implement the first report-only parser runner against this harness; keep it read-only and emit previews only until the harness passes and explicit mutation approval exists."
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
        "schema_version": "agent_company.ceo_decision_parser_report_only_harness.v1",
        "generated_utc": generated_utc,
        "harness_lane_id": lane_id,
        "harness_task_id": harness_task_id,
        "harness_evidence_id": harness_evidence_id,
        "source_suite_task_id": source_suite_task_id,
        "source_suite_evidence_id": source_suite_evidence_id,
        "source_suite_validation_path": str(CEO_DECISION_PARSER_FIXTURE_SUITE_VALIDATION_JSON),
        "fixture_suite_count": fixture_suite_count,
        "negative_fixture_count": negative_fixture_count,
        "positive_fixture_count": positive_fixture_count,
        "harness_case_count": harness_case_count,
        "required_pass_count": required_pass_count,
        "harness_cases": harness_cases,
        "parser_execution_count": parser_execution_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "queue_mutation_count": queue_mutation_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": harness_summary,
        "next_action": harness_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Report-Only Harness",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        harness_summary,
        "",
        "## Harness Cases",
        "",
        "| Case | Fixtures | Required Result |",
        "| --- | ---: | --- |",
    ]
    for case in harness_cases:
        md_lines.append(f"| `{case['case_id']}` | `{case['fixture_count']}` | `{case['required_result']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local acceptance harness only. It runs no parser, accepts no decision, mutates no queue, requests no approval, starts no worker, calls no API, and performs no browser, account, wallet, payment, real-money, security-testing, public, or external action.",
            "",
            "## Next Action",
            "",
            harness_next_action,
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
                harness_task_id,
                lane_id,
                "Create CEO decision parser report-only harness",
                39,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                harness_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": harness_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser report-only harness",
                "status": "local_ceo_decision_parser_report_only_harness_complete",
                "summary": harness_summary,
                "next_action": harness_next_action,
                "ownership_note": "Generated by platform_engineering from the parser fixture suite; harness is local validation data only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_harness = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (harness_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (harness_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (harness_task_id,)) else 0
    if task_rows_inserted_by_harness != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser report-only harness, got {task_rows_inserted_by_harness}")
    if tasks_table_rows_after != 199:
        failures.append(f"expected 199 task rows after CEO decision parser report-only harness, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 107:
        failures.append(f"expected 107 evidence rows after CEO decision parser report-only harness, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser report-only harness evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser report-only harness")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_harness": task_rows_inserted_by_harness,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_report_only_harness_validation.v1",
        "generated_utc": generated_utc,
        "harness_path": str(json_output_path),
        "harness_lane_id": lane_id,
        "harness_task_id": harness_task_id,
        "source_suite_task_id": source_suite_task_id,
        "fixture_suite_count": fixture_suite_count,
        "negative_fixture_count": negative_fixture_count,
        "positive_fixture_count": positive_fixture_count,
        "harness_case_count": harness_case_count,
        "required_pass_count": required_pass_count,
        "parser_execution_count": parser_execution_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "queue_mutation_count": queue_mutation_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_harness": task_rows_inserted_by_harness,
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
                "harness_lane_id": lane_id,
                "harness_task_id": harness_task_id,
                "harness_case_count": harness_case_count,
                "task_rows_inserted_by_harness": task_rows_inserted_by_harness,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

