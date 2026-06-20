from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Negative fixtures, guard runner, positive fixture, and positive runner writers for apply readiness."""

from .ceo_decision_apply_readiness_evaluator import evaluate_ceo_apply_readiness_packet
from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_guard_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    runner_task_id = "task-ceo-decision-parser-apply-readiness-guard-runner-20260616"
    runner_evidence_id = "ceo-decision-parser-apply-readiness-guard-runner-20260616"
    source_fixtures_task_id = "task-ceo-decision-parser-apply-readiness-negative-fixtures-20260616"
    source_fixtures_evidence_id = "ceo-decision-parser-apply-readiness-negative-fixtures-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-guard-runner-20260616"
    local_decision = "ceo_decision_parser_apply_readiness_guard_runner_passed_no_mutations"
    recommended_default = "keep_apply_disabled_until_readiness_guard_passes_and_operator_approves"
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_fixtures_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_fixtures_task_id,)).fetchone()
    source_fixtures_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_fixtures_evidence_id,),
    ).fetchone()
    fixtures_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_VALIDATION_JSON)
    fixtures_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_JSON)
    readiness_fixtures = fixtures_payload.get("negative_readiness_fixtures", [])
    negative_readiness_fixture_count = len(readiness_fixtures)

    readiness_guard_results: list[dict[str, object]] = []
    for fixture in readiness_fixtures:
        result = evaluate_ceo_apply_readiness_packet(fixture.get("submitted_readiness", {}))
        expected_rule_id = fixture.get("expected_rule_id")
        readiness_guard_results.append(
            {
                "fixture_id": fixture.get("fixture_id"),
                "expected_accepted": fixture.get("expected_accepted"),
                "actual_accepted": result.get("accepted_readiness"),
                "expected_rule_id": expected_rule_id,
                "actual_rule_id": result.get("rule_id"),
                "matched_expected": result.get("accepted_readiness") is False and result.get("rule_id") == expected_rule_id,
            }
        )

    readiness_guard_execution_count = len(readiness_guard_results)
    rejected_readiness_count = sum(1 for result in readiness_guard_results if result.get("actual_accepted") is False)
    accepted_readiness_count = sum(1 for result in readiness_guard_results if result.get("actual_accepted") is True)
    expected_rejection_match_count = sum(1 for result in readiness_guard_results if result.get("matched_expected") is True)

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    runner_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_fixtures_task or source_fixtures_task["status"] != "complete":
        failures.append("source apply-readiness negative fixtures task is missing or incomplete")
    if not source_fixtures_evidence or source_fixtures_evidence["status"] != "local_ceo_decision_parser_apply_readiness_negative_fixtures_complete":
        failures.append("source apply-readiness negative fixtures evidence is missing or not complete")
    if not fixtures_validation.get("all_checks_passed") or fixtures_validation.get("failure_count") != 0:
        failures.append("source apply-readiness negative fixtures validation is not clean")
    if negative_readiness_fixture_count != 6:
        failures.append(f"expected 6 readiness fixtures, got {negative_readiness_fixture_count}")
    if readiness_guard_execution_count != 6:
        failures.append(f"expected 6 readiness guard executions, got {readiness_guard_execution_count}")
    if rejected_readiness_count != 6:
        failures.append(f"expected 6 rejected readiness packets, got {rejected_readiness_count}")
    if accepted_readiness_count != 0:
        failures.append(f"expected 0 accepted readiness packets, got {accepted_readiness_count}")
    if expected_rejection_match_count != 6:
        failures.append(f"expected 6 matching readiness rejections, got {expected_rejection_match_count}")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply-readiness guard runner task already exists: {runner_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if runner_evidence_exists_before:
        failures.append(f"CEO decision parser apply-readiness guard runner evidence already exists: {runner_evidence_id}")
    if tasks_table_rows_before != 207:
        failures.append(f"expected 207 task rows before CEO decision parser apply-readiness guard runner, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 115:
        failures.append(f"expected 115 evidence rows before CEO decision parser apply-readiness guard runner, got {lane_evidence_rows_before}")

    runner_summary = (
        "Ran a local report-only apply-readiness guard against six negative readiness fixtures. The guard rejected every drifted, underspecified, or unsafe readiness packet and performed no mutation."
    )
    runner_next_action = (
        "Keep real apply disabled; next create a positive apply-readiness fixture that passes the guard but still requires explicit operator approval before any DB update command."
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_guard_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixtures_task_id": source_fixtures_task_id,
        "source_fixtures_evidence_id": source_fixtures_evidence_id,
        "source_fixtures_validation_path": str(CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_VALIDATION_JSON),
        "negative_readiness_fixture_count": negative_readiness_fixture_count,
        "readiness_guard_execution_count": readiness_guard_execution_count,
        "rejected_readiness_count": rejected_readiness_count,
        "accepted_readiness_count": accepted_readiness_count,
        "expected_rejection_match_count": expected_rejection_match_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "readiness_guard_results": readiness_guard_results,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Apply Readiness Guard Runner",
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
        "## Guard Results",
        "",
        "| Fixture | Expected Rule | Actual Rule | Match |",
        "| --- | --- | --- | --- |",
    ]
    for result in readiness_guard_results:
        md_lines.append(
            f"| `{result.get('fixture_id')}` | `{result.get('expected_rule_id')}` | `{result.get('actual_rule_id')}` | `{result.get('matched_expected')}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner is report-only. It evaluated local readiness fixtures and wrote local artifacts only; it did not mutate service requests, assign work, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
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
                "Run CEO decision parser apply-readiness guard fixtures",
                30,
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
                "title": "CEO decision parser apply-readiness guard runner",
                "status": "local_ceo_decision_parser_apply_readiness_guard_runner_complete",
                "summary": runner_summary,
                "next_action": runner_next_action,
                "ownership_note": "Generated by platform_engineering from local apply-readiness negative fixtures; runner is report-only and performs no mutations.",
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
        failures.append(f"expected 1 task row inserted by CEO decision parser apply-readiness guard runner, got {task_rows_inserted_by_runner}")
    if tasks_table_rows_after != 208:
        failures.append(f"expected 208 task rows after CEO decision parser apply-readiness guard runner, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 116:
        failures.append(f"expected 116 evidence rows after CEO decision parser apply-readiness guard runner, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply-readiness guard runner evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply-readiness guard runner")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_guard_runner_validation.v1",
        "generated_utc": generated_utc,
        "runner_path": str(json_output_path),
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "source_fixtures_task_id": source_fixtures_task_id,
        "negative_readiness_fixture_count": negative_readiness_fixture_count,
        "readiness_guard_execution_count": readiness_guard_execution_count,
        "rejected_readiness_count": rejected_readiness_count,
        "accepted_readiness_count": accepted_readiness_count,
        "expected_rejection_match_count": expected_rejection_match_count,
        "mutation_applied_count": mutation_applied_count,
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
                "readiness_guard_execution_count": readiness_guard_execution_count,
                "rejected_readiness_count": rejected_readiness_count,
                "accepted_readiness_count": accepted_readiness_count,
                "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

