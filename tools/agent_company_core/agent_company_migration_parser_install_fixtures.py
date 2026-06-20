from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Parser install decision fixture suite writer."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_RUNNER_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_VALIDATION_JSON,
)
from .agent_company_migration_parser_install_fixture_content import build_parser_install_fixture_suite_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_install_decision_fixture_suite(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_FIXTURE_SUITE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-agent-company-migration-decision-parser-install-decision-fixture-suite-20260616"
    fixture_evidence_id = "agent-company-migration-decision-parser-install-decision-fixture-suite-20260616"
    source_intake_task_id = "task-agent-company-migration-decision-parser-install-decision-intake-contract-20260616"
    source_intake_evidence_id = "agent-company-migration-decision-parser-install-decision-intake-contract-20260616"
    duplicate_key = "agent-company-migration-decision-parser-install-decision-fixture-suite-20260616"
    local_decision = "agent_company_migration_decision_parser_install_decision_fixture_suite_ready_for_report_only_runner"
    recommended_default = "build_report_only_install_decision_runner_next_without_applying_install_decision"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_intake_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_VALIDATION_JSON)
    source_intake_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_JSON)
    fixture_content = build_parser_install_fixture_suite_content(source_intake_payload)
    accepted_install_decision_types = fixture_content["accepted_install_decision_types"]
    required_fields = fixture_content["required_fields"]
    parser_guards = fixture_content["parser_guards"]
    output_states = fixture_content["output_states"]
    expected_target_path = fixture_content["expected_target_path"]
    expected_source_artifact_path = fixture_content["expected_source_artifact_path"]
    fixtures = fixture_content["fixtures"]
    install_decision_fixture_suite_count = fixture_content["install_decision_fixture_suite_count"]
    positive_fixture_count = fixture_content["positive_fixture_count"]
    negative_fixture_count = fixture_content["negative_fixture_count"]
    required_field_count = fixture_content["required_field_count"]
    parser_guard_count = fixture_content["parser_guard_count"]
    output_state_count = fixture_content["output_state_count"]
    fixture_assertion_count = fixture_content["fixture_assertion_count"]

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
        failures.append("source install decision intake contract task is missing or incomplete")
    if not source_intake_evidence or source_intake_evidence["status"] != "local_agent_company_migration_decision_parser_install_decision_intake_contract_complete":
        failures.append("source install decision intake contract evidence is missing or not complete")
    if not source_intake_validation.get("all_checks_passed") or source_intake_validation.get("failure_count") != 0:
        failures.append("source install decision intake contract validation is not clean")
    if source_intake_payload.get("recommended_default") != "build_report_only_install_decision_fixture_suite_next_without_applying_install_decision":
        failures.append("source install decision intake contract default does not point to fixture suite")
    if accepted_install_decision_types != ["hold", "approve_one_file_write_only", "request_preflight_rework", "reject_parser_install"]:
        failures.append(f"unexpected accepted install decision types: {accepted_install_decision_types}")
    if install_decision_fixture_suite_count != 11:
        failures.append(f"expected 11 install decision fixtures, got {install_decision_fixture_suite_count}")
    if positive_fixture_count != 4:
        failures.append(f"expected 4 positive fixtures, got {positive_fixture_count}")
    if negative_fixture_count != 7:
        failures.append(f"expected 7 negative fixtures, got {negative_fixture_count}")
    if required_field_count != 8:
        failures.append(f"expected 8 required fields, got {required_field_count}")
    if parser_guard_count != 8:
        failures.append(f"expected 8 parser guards, got {parser_guard_count}")
    if output_state_count != 4:
        failures.append(f"expected 4 output states, got {output_state_count}")
    if fixture_assertion_count != 11:
        failures.append(f"expected 11 fixture assertions, got {fixture_assertion_count}")
    if target_task_exists_before:
        failures.append(f"target install decision fixture suite task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"install decision fixture suite evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 242:
        failures.append(f"expected 242 task rows before install decision fixture suite, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 150:
        failures.append(f"expected 150 evidence rows before install decision fixture suite, got {lane_evidence_rows_before}")

    summary = "Materialized the report-only install-decision fixture suite from the intake contract, covering accepted decisions, rejection cases, and parser guard assertions."
    next_action = "Build a report-only install-decision runner next; do not execute fixtures through an importable parser or apply an install decision."
    runtime_boundary = {
        "operator_install_decision_applied": False,
        "parser_module_file_written": False,
        "parser_module_imported": False,
        "fixtures_executed": False,
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
        "schema_version": "agent_company.migration_decision_parser_install_decision_fixture_suite.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_intake_task_id": source_intake_task_id,
        "source_intake_evidence_id": source_intake_evidence_id,
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "install_decision_fixture_suite_count": install_decision_fixture_suite_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "required_field_count": required_field_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "fixture_assertion_count": fixture_assertion_count,
        "fixtures": fixtures,
        "required_fields": required_fields,
        "parser_guards": parser_guards,
        "output_states": output_states,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Agent Company Migration Decision Parser Install Decision Fixture Suite",
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
        "## Fixture Counts",
        "",
        f"- Positive fixtures: {positive_fixture_count}",
        f"- Negative fixtures: {negative_fixture_count}",
        f"- Assertions: {fixture_assertion_count}",
        "",
        "## Fixtures",
        "",
    ]
    for item in fixtures:
        expected = item["expected_state"] if item["expected_valid"] else item["expected_guard"]
        md_lines.append(f"- `{item['fixture_id']}` ({item['kind']}): {expected}")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only fixture suite. It does not execute fixtures, apply an install decision, write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                fixture_task_id,
                lane_id,
                "Create agent company migration decision parser install decision fixture suite",
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
                "title": "Agent company migration decision parser install decision fixture suite",
                "status": "local_agent_company_migration_decision_parser_install_decision_fixture_suite_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from install decision intake contract; fixtures were not executed.",
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
    task_rows_inserted_by_install_decision_fixture_suite = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_install_decision_fixture_suite != 1:
        failures.append(f"expected 1 task row inserted by install decision fixture suite, got {task_rows_inserted_by_install_decision_fixture_suite}")
    if tasks_table_rows_after != 243:
        failures.append(f"expected 243 task rows after install decision fixture suite, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 151:
        failures.append(f"expected 151 evidence rows after install decision fixture suite, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("install decision fixture suite evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by install decision fixture suite, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during install decision fixture suite")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_install_decision_fixture_suite": task_rows_inserted_by_install_decision_fixture_suite,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_install_decision_fixture_suite_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_intake_task_id": source_intake_task_id,
        "install_decision_fixture_suite_count": install_decision_fixture_suite_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "required_field_count": required_field_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "fixture_assertion_count": fixture_assertion_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_install_decision_fixture_suite": task_rows_inserted_by_install_decision_fixture_suite,
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
                "install_decision_fixture_suite_count": install_decision_fixture_suite_count,
                "positive_fixture_count": positive_fixture_count,
                "negative_fixture_count": negative_fixture_count,
                "fixture_assertion_count": fixture_assertion_count,
                "task_rows_inserted_by_install_decision_fixture_suite": task_rows_inserted_by_install_decision_fixture_suite,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


__all__ = [
    "write_agent_company_migration_decision_parser_install_decision_fixture_suite",
]

