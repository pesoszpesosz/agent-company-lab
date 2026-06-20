from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Decision-intake contract, fixture suite, and runner writers for migration work."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_SUITE_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_SUITE_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_SUITE_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_INTAKE_CONTRACT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_INTAKE_CONTRACT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_INTAKE_CONTRACT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .agent_company_migration_decision_fixture_runner_evaluator import evaluate_migration_decision_fixture


def write_agent_company_migration_decision_fixture_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_RUNNER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    runner_task_id = "task-agent-company-migration-decision-fixture-runner-20260616"
    runner_evidence_id = "agent-company-migration-decision-fixture-runner-20260616"
    source_suite_task_id = "task-agent-company-migration-decision-fixture-suite-20260616"
    source_suite_evidence_id = "agent-company-migration-decision-fixture-suite-20260616"
    duplicate_key = "agent-company-migration-decision-fixture-runner-20260616"
    local_decision = "agent_company_migration_decision_fixture_runner_ready_for_report_only_parser_scaffold"
    recommended_default = "build_report_only_parser_scaffold_next_without_parsing_live_decisions"
    fixture_runner_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    suite_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_SUITE_VALIDATION_JSON)
    suite_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_FIXTURE_SUITE_JSON)
    fixtures = suite_payload.get("fixtures", [])
    parser_guards = suite_payload.get("parser_guards", [])
    output_states = suite_payload.get("output_states", [])
    accepted_decision_types = {"hold", "approve_sandbox_dry_run_only", "request_rework", "reject_migration_path"}
    required_fields = {
        "decision_id",
        "operator_name",
        "decision_type",
        "scope",
        "artifact_paths",
        "expires_at",
        "risk_acknowledgement",
        "signed_utc",
    }

    fixture_results = [
        evaluate_migration_decision_fixture(
            item,
            accepted_decision_types=accepted_decision_types,
            required_fields=required_fields,
        )
        for item in fixtures
    ]
    fixture_suite_count = len(fixtures)
    fixtures_evaluated = len(fixture_results)
    accepted_result_count = sum(1 for item in fixture_results if item["actual"] == "accept")
    rejected_result_count = sum(1 for item in fixture_results if item["actual"] == "reject")
    passed_fixture_count = sum(1 for item in fixture_results if item["passed"])
    failed_fixture_count = fixtures_evaluated - passed_fixture_count
    parser_guard_count = len(parser_guards)
    output_state_count = len(output_states)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_suite_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_suite_task_id,),
    ).fetchone()
    source_suite_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_suite_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_suite_task or source_suite_task["status"] != "complete":
        failures.append("source decision fixture suite task is missing or incomplete")
    if not source_suite_evidence or source_suite_evidence["status"] != "local_agent_company_migration_decision_fixture_suite_complete":
        failures.append("source decision fixture suite evidence is missing or not complete")
    if not suite_validation.get("all_checks_passed") or suite_validation.get("failure_count") != 0:
        failures.append("source decision fixture suite validation is not clean")
    if fixture_runner_count != 1:
        failures.append(f"expected 1 fixture runner, got {fixture_runner_count}")
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
        failures.append(f"target decision fixture runner task already exists: {runner_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"decision fixture runner evidence already exists: {runner_evidence_id}")
    if tasks_table_rows_before != 233:
        failures.append(f"expected 233 task rows before fixture runner, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 141:
        failures.append(f"expected 141 evidence rows before fixture runner, got {lane_evidence_rows_before}")

    summary = "Evaluated the migration decision fixture suite with a deterministic report-only runner; all 12 synthetic fixtures matched expected accept/reject outcomes."
    next_action = "Build the report-only parser scaffold next; do not parse live decisions or apply operator decisions."
    runtime_boundary = {
        "report_only_fixtures_evaluated": True,
        "live_decisions_parsed": False,
        "operator_decision_applied": False,
        "migration_sql_executed": False,
        "apply_command_enabled": False,
        "tables_created": 0,
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
        "schema_version": "agent_company.migration_decision_fixture_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_suite_task_id": source_suite_task_id,
        "source_suite_evidence_id": source_suite_evidence_id,
        "fixture_runner_count": fixture_runner_count,
        "fixture_suite_count": fixture_suite_count,
        "fixtures_evaluated": fixtures_evaluated,
        "accepted_result_count": accepted_result_count,
        "rejected_result_count": rejected_result_count,
        "passed_fixture_count": passed_fixture_count,
        "failed_fixture_count": failed_fixture_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "fixture_results": fixture_results,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Fixture Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        summary,
        "",
        "## Runner Results",
        "",
        f"- Fixtures evaluated: {fixtures_evaluated}",
        f"- Accepted results: {accepted_result_count}",
        f"- Rejected results: {rejected_result_count}",
        f"- Passed fixtures: {passed_fixture_count}",
        f"- Failed fixtures: {failed_fixture_count}",
        "",
        "| Fixture | Expected | Actual | Passed | Reasons |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in fixture_results:
        md_lines.append(f"| `{item['fixture_id']}` | `{item['expected']}` | `{item['actual']}` | `{item['passed']}` | {', '.join(item['reasons']) or 'none'} |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner evaluates saved synthetic fixtures only. It does not parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                runner_task_id,
                lane_id,
                "Create agent company migration decision fixture runner",
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
                "title": "Agent company migration decision fixture runner",
                "status": "local_agent_company_migration_decision_fixture_runner_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the decision fixture suite; only saved synthetic fixtures were evaluated.",
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
    task_rows_inserted_by_fixture_runner = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (runner_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_fixture_runner != 1:
        failures.append(f"expected 1 task row inserted by fixture runner, got {task_rows_inserted_by_fixture_runner}")
    if tasks_table_rows_after != 234:
        failures.append(f"expected 234 task rows after fixture runner, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 142:
        failures.append(f"expected 142 evidence rows after fixture runner, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("decision fixture runner evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by fixture runner, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during fixture runner")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_fixture_runner": task_rows_inserted_by_fixture_runner,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_fixture_runner_validation.v1",
        "generated_utc": generated_utc,
        "runner_path": str(json_output_path),
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "source_suite_task_id": source_suite_task_id,
        "fixture_runner_count": fixture_runner_count,
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
        "task_rows_inserted_by_fixture_runner": task_rows_inserted_by_fixture_runner,
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
                "task_rows_inserted_by_fixture_runner": task_rows_inserted_by_fixture_runner,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

