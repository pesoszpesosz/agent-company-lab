from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Parser install decision intake contract writer."""

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
from .agent_company_migration_parser_install_contract_content import build_parser_install_intake_contract_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_install_decision_intake_contract(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_DECISION_INTAKE_CONTRACT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    intake_task_id = "task-agent-company-migration-decision-parser-install-decision-intake-contract-20260616"
    intake_evidence_id = "agent-company-migration-decision-parser-install-decision-intake-contract-20260616"
    source_review_task_id = "task-agent-company-migration-decision-parser-install-review-20260616"
    source_review_evidence_id = "agent-company-migration-decision-parser-install-review-20260616"
    duplicate_key = "agent-company-migration-decision-parser-install-decision-intake-contract-20260616"
    local_decision = "agent_company_migration_decision_parser_install_decision_intake_contract_ready_for_report_only_fixture_suite"
    recommended_default = "build_report_only_install_decision_fixture_suite_next_without_applying_install_decision"
    install_decision_intake_contract_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")

    }
    source_review_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_VALIDATION_JSON)
    source_review_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_JSON)
    preflight_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_JSON)
    contract_content = build_parser_install_intake_contract_content(
        source_review_payload=source_review_payload,
        preflight_payload=preflight_payload,
    )
    expected_target_path = contract_content["expected_target_path"]
    expected_source_artifact_path = contract_content["expected_source_artifact_path"]
    install_decision_intake_contract_count = contract_content["install_decision_intake_contract_count"]
    accepted_install_decision_types = contract_content["accepted_install_decision_types"]
    required_fields = contract_content["required_fields"]
    positive_fixtures = contract_content["positive_fixtures"]
    negative_fixtures = contract_content["negative_fixtures"]
    parser_guards = contract_content["parser_guards"]
    output_states = contract_content["output_states"]
    accepted_install_decision_type_count = contract_content["accepted_install_decision_type_count"]
    required_field_count = contract_content["required_field_count"]
    positive_fixture_count = contract_content["positive_fixture_count"]
    negative_fixture_count = contract_content["negative_fixture_count"]
    parser_guard_count = contract_content["parser_guard_count"]
    output_state_count = contract_content["output_state_count"]
    summary = contract_content["summary"]
    next_action = contract_content["next_action"]
    runtime_boundary = contract_content["runtime_boundary"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_review_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_review_task_id,),
    ).fetchone()
    source_review_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_review_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (intake_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (intake_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_review_task or source_review_task["status"] != "complete":
        failures.append("source parser install review task is missing or incomplete")
    if not source_review_evidence or source_review_evidence["status"] != "local_agent_company_migration_decision_parser_install_review_complete":
        failures.append("source parser install review evidence is missing or not complete")
    if not source_review_validation.get("all_checks_passed") or source_review_validation.get("failure_count") != 0:
        failures.append("source parser install review validation is not clean")
    if source_review_payload.get("recommended_default") != "hold_without_signed_operator_file_write_approval":
        failures.append("source parser install review default is not hold")
    if accepted_install_decision_types != ["hold", "approve_one_file_write_only", "request_preflight_rework", "reject_parser_install"]:
        failures.append(f"unexpected accepted install decision types: {accepted_install_decision_types}")
    if not expected_target_path or not expected_source_artifact_path:
        failures.append("source preflight target path or source artifact path is missing")
    if install_decision_intake_contract_count != 1:
        failures.append(f"expected 1 install decision intake contract, got {install_decision_intake_contract_count}")
    if accepted_install_decision_type_count != 4:
        failures.append(f"expected 4 accepted install decision types, got {accepted_install_decision_type_count}")
    if required_field_count != 8:
        failures.append(f"expected 8 required fields, got {required_field_count}")
    if positive_fixture_count != 4:
        failures.append(f"expected 4 positive fixtures, got {positive_fixture_count}")
    if negative_fixture_count != 7:
        failures.append(f"expected 7 negative fixtures, got {negative_fixture_count}")
    if parser_guard_count != 8:
        failures.append(f"expected 8 parser guards, got {parser_guard_count}")
    if output_state_count != 4:
        failures.append(f"expected 4 output states, got {output_state_count}")
    if target_task_exists_before:
        failures.append(f"target install decision intake contract task already exists: {intake_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"install decision intake contract evidence already exists: {intake_evidence_id}")
    if tasks_table_rows_before != 241:
        failures.append(f"expected 241 task rows before install decision intake contract, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 149:
        failures.append(f"expected 149 evidence rows before install decision intake contract, got {lane_evidence_rows_before}")
    payload = {
        "schema_version": "agent_company.migration_decision_parser_install_decision_intake_contract.v1",
        "generated_utc": generated_utc,
        "intake_lane_id": lane_id,
        "intake_task_id": intake_task_id,
        "intake_evidence_id": intake_evidence_id,
        "source_review_task_id": source_review_task_id,
        "source_review_evidence_id": source_review_evidence_id,
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "install_decision_intake_contract_count": install_decision_intake_contract_count,
        "accepted_install_decision_type_count": accepted_install_decision_type_count,
        "required_field_count": required_field_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "accepted_install_decision_types": accepted_install_decision_types,
        "required_fields": required_fields,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
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
        "# Agent Company Migration Decision Parser Install Decision Intake Contract",
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
        "## Required Fields",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in required_fields)
    md_lines.extend(["", "## Accepted Install Decisions", ""])
    md_lines.extend(f"- `{item}`" for item in accepted_install_decision_types)
    md_lines.extend(["", "## Positive Fixtures", ""])
    md_lines.extend(f"- `{item['fixture']}` -> `{item['expected_state']}`" for item in positive_fixtures)
    md_lines.extend(["", "## Negative Fixtures", ""])
    md_lines.extend(f"- `{item}`" for item in negative_fixtures)
    md_lines.extend(["", "## Parser Guards", ""])
    md_lines.extend(f"- `{item}`" for item in parser_guards)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only intake contract. It does not apply an install decision, write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
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
                intake_task_id,
                lane_id,
                "Create agent company migration decision parser install decision intake contract",
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
                "evidence_id": intake_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser install decision intake contract",
                "status": "local_agent_company_migration_decision_parser_install_decision_intake_contract_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from parser install review; no install decision was applied.",
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
    task_rows_inserted_by_install_decision_intake_contract = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (intake_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (intake_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (intake_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_install_decision_intake_contract != 1:
        failures.append(f"expected 1 task row inserted by install decision intake contract, got {task_rows_inserted_by_install_decision_intake_contract}")
    if tasks_table_rows_after != 242:
        failures.append(f"expected 242 task rows after install decision intake contract, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 150:
        failures.append(f"expected 150 evidence rows after install decision intake contract, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("install decision intake contract evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by install decision intake contract, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during install decision intake contract")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_install_decision_intake_contract": task_rows_inserted_by_install_decision_intake_contract,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_install_decision_intake_contract_validation.v1",
        "generated_utc": generated_utc,
        "contract_path": str(json_output_path),
        "intake_lane_id": lane_id,
        "intake_task_id": intake_task_id,
        "source_review_task_id": source_review_task_id,
        "install_decision_intake_contract_count": install_decision_intake_contract_count,
        "accepted_install_decision_type_count": accepted_install_decision_type_count,
        "required_field_count": required_field_count,
        "positive_fixture_count": positive_fixture_count,
        "negative_fixture_count": negative_fixture_count,
        "parser_guard_count": parser_guard_count,
        "output_state_count": output_state_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_install_decision_intake_contract": task_rows_inserted_by_install_decision_intake_contract,
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
                "intake_lane_id": lane_id,
                "intake_task_id": intake_task_id,
                "accepted_install_decision_type_count": accepted_install_decision_type_count,
                "required_field_count": required_field_count,
                "positive_fixture_count": positive_fixture_count,
                "negative_fixture_count": negative_fixture_count,
                "parser_guard_count": parser_guard_count,
                "output_state_count": output_state_count,
                "task_rows_inserted_by_install_decision_intake_contract": task_rows_inserted_by_install_decision_intake_contract,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


__all__ = [
    "write_agent_company_migration_decision_parser_install_decision_intake_contract",
]

