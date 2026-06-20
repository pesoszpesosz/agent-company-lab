from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .ceo_decision_parser_report_only_runner_content import build_report_only_parser_runner_content
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

def write_ceo_decision_parser_report_only_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    runner_task_id = "task-ceo-decision-parser-report-only-runner-20260616"
    runner_evidence_id = "ceo-decision-parser-report-only-runner-20260616"
    source_harness_task_id = "task-ceo-decision-parser-report-only-harness-20260616"
    source_harness_evidence_id = "ceo-decision-parser-report-only-harness-20260616"
    duplicate_key = "ceo-decision-parser-report-only-runner-20260616"
    local_decision = "ceo_decision_parser_report_only_runner_passed_no_mutations"
    recommended_default = "keep_parser_report_only_until_operator_approves_mutations"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_harness_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_harness_task_id,)).fetchone()
    source_harness_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_harness_evidence_id,),
    ).fetchone()
    harness_validation = load_json(CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_VALIDATION_JSON)
    negative_payload = load_json(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON)
    positive_payload = load_json(CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON)
    negative_fixtures = negative_payload.get("negative_fixtures", [])
    positive_fixture = positive_payload.get("positive_fixture", {})
    runner_content = build_report_only_parser_runner_content(
        negative_fixtures=negative_fixtures,
        positive_fixture=positive_fixture,
        negative_fixture_total=int(negative_payload.get("negative_fixture_count", 0)),
        positive_fixture_total=int(positive_payload.get("positive_fixture_count", 0)),
    )
    fixture_suite_count = runner_content["fixture_suite_count"]
    negative_fixture_count = runner_content["negative_fixture_count"]
    positive_fixture_count = runner_content["positive_fixture_count"]
    parser_results = runner_content["parser_results"]
    parser_execution_count = runner_content["parser_execution_count"]
    rejected_decision_count = runner_content["rejected_decision_count"]
    accepted_dry_run_preview_count = runner_content["accepted_dry_run_preview_count"]
    expected_rejection_match_count = runner_content["expected_rejection_match_count"]
    expected_preview_match_count = runner_content["expected_preview_match_count"]
    queue_mutation_count = runner_content["queue_mutation_count"]
    approval_request_count = runner_content["approval_request_count"]
    runner_summary = runner_content["summary"]
    runner_next_action = runner_content["next_action"]
    boundary_text = runner_content["boundary_text"]
    runtime_boundary = runner_content["runtime_boundary"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    runner_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_harness_task or source_harness_task["status"] != "complete":
        failures.append("source report-only harness task is missing or incomplete")
    if not source_harness_evidence or source_harness_evidence["status"] != "local_ceo_decision_parser_report_only_harness_complete":
        failures.append("source report-only harness evidence is missing or not complete")
    if not harness_validation.get("all_checks_passed") or harness_validation.get("failure_count") != 0:
        failures.append("source report-only harness validation is not clean")
    if fixture_suite_count != 7:
        failures.append(f"expected 7 total fixtures, got {fixture_suite_count}")
    if negative_fixture_count != 6:
        failures.append(f"expected 6 negative fixtures, got {negative_fixture_count}")
    if positive_fixture_count != 1:
        failures.append(f"expected 1 positive fixture, got {positive_fixture_count}")
    if parser_execution_count != 7:
        failures.append(f"expected 7 parser executions, got {parser_execution_count}")
    if rejected_decision_count != 6:
        failures.append(f"expected 6 rejected decisions, got {rejected_decision_count}")
    if accepted_dry_run_preview_count != 1:
        failures.append(f"expected 1 accepted dry-run preview, got {accepted_dry_run_preview_count}")
    if expected_rejection_match_count != 6:
        failures.append(f"expected 6 matching rejections, got {expected_rejection_match_count}")
    if expected_preview_match_count != 1:
        failures.append(f"expected 1 matching preview, got {expected_preview_match_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser report-only runner task already exists: {runner_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if runner_evidence_exists_before:
        failures.append(f"CEO decision parser report-only runner evidence already exists: {runner_evidence_id}")
    if tasks_table_rows_before != 199:
        failures.append(f"expected 199 task rows before CEO decision parser report-only runner, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 107:
        failures.append(f"expected 107 evidence rows before CEO decision parser report-only runner, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.ceo_decision_parser_report_only_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_harness_task_id": source_harness_task_id,
        "source_harness_evidence_id": source_harness_evidence_id,
        "source_harness_validation_path": str(CEO_DECISION_PARSER_REPORT_ONLY_HARNESS_VALIDATION_JSON),
        "fixture_suite_count": fixture_suite_count,
        "negative_fixture_count": negative_fixture_count,
        "positive_fixture_count": positive_fixture_count,
        "parser_execution_count": parser_execution_count,
        "rejected_decision_count": rejected_decision_count,
        "accepted_dry_run_preview_count": accepted_dry_run_preview_count,
        "expected_rejection_match_count": expected_rejection_match_count,
        "expected_preview_match_count": expected_preview_match_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "parser_results": parser_results,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Report-Only Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        runner_summary,
        "",
        "## Parser Results",
        "",
        "| Fixture | Type | Expected | Actual | Match |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in parser_results:
        expected = result.get("expected_rule_id") or result.get("expected_preview_state")
        actual = result.get("actual_rule_id") or result.get("actual_preview_state")
        md_lines.append(
            f"| `{result.get('fixture_id')}` | `{result.get('fixture_type')}` | `{expected}` | `{actual}` | `{result.get('matched_expected')}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            boundary_text,
            "",
            "## Next Action",
            "",
            runner_next_action,
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
                runner_task_id,
                lane_id,
                "Run CEO decision parser report-only fixture suite",
                38,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                runner_next_action,
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
                "title": "CEO decision parser report-only runner",
                "status": "local_ceo_decision_parser_report_only_runner_complete",
                "summary": runner_summary,
                "next_action": runner_next_action,
                "ownership_note": "Generated by platform_engineering from local parser fixtures; runner is report-only and performs no mutations.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_runner = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (runner_task_id,)) else 0
    if task_rows_inserted_by_runner != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser report-only runner, got {task_rows_inserted_by_runner}")
    if tasks_table_rows_after != 200:
        failures.append(f"expected 200 task rows after CEO decision parser report-only runner, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 108:
        failures.append(f"expected 108 evidence rows after CEO decision parser report-only runner, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser report-only runner evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser report-only runner")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_report_only_runner_validation.v1",
        "generated_utc": generated_utc,
        "runner_path": str(json_output_path),
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "source_harness_task_id": source_harness_task_id,
        "fixture_suite_count": fixture_suite_count,
        "negative_fixture_count": negative_fixture_count,
        "positive_fixture_count": positive_fixture_count,
        "parser_execution_count": parser_execution_count,
        "rejected_decision_count": rejected_decision_count,
        "accepted_dry_run_preview_count": accepted_dry_run_preview_count,
        "expected_rejection_match_count": expected_rejection_match_count,
        "expected_preview_match_count": expected_preview_match_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
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
                "parser_execution_count": parser_execution_count,
                "rejected_decision_count": rejected_decision_count,
                "accepted_dry_run_preview_count": accepted_dry_run_preview_count,
                "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


