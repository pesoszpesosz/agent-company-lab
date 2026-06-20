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

def write_ceo_decision_parser_positive_fixture(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_POSITIVE_FIXTURE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_POSITIVE_FIXTURE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-ceo-decision-parser-positive-fixture-20260616"
    fixture_evidence_id = "ceo-decision-parser-positive-fixture-20260616"
    source_contract_task_id = "task-ceo-decision-parser-dry-run-contract-20260616"
    source_contract_evidence_id = "ceo-decision-parser-dry-run-contract-20260616"
    duplicate_key = "ceo-decision-parser-positive-fixture-20260616"
    local_decision = "ceo_decision_parser_positive_fixture_ready_parser_not_executed"
    recommended_default = "report_only_dry_run_before_any_mutation"
    expected_preview_state = "would_create_bounded_service_request_update"
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
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_contract_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_contract_evidence_id,),
    ).fetchone()
    contract_validation = load_json(CEO_DECISION_PARSER_DRY_RUN_CONTRACT_VALIDATION_JSON)
    contract_payload = load_json(CEO_DECISION_PARSER_DRY_RUN_CONTRACT_JSON)
    source_contract_section_count = int(contract_payload.get("contract_section_count", 0))
    source_mutation_preview_state_count = int(contract_payload.get("mutation_preview_state_count", 0))
    mutation_preview_states = contract_payload.get("mutation_preview_states", [])

    positive_fixture = {
        "fixture_id": "valid-digital-products-readonly-browser-preview",
        "decision_packet_id": "decision-packet-batch-digital-products-marketplace-validation",
        "selected_option_id": "approve_bounded_readonly_scope",
        "submitted_intake": {
            "decision_packet_id": "decision-packet-batch-digital-products-marketplace-validation",
            "selected_option_id": "approve_bounded_readonly_scope",
            "approved_blocker_ids": [
                "req-wave4-digital-products-browser-readonly-20260614",
                "hold-live-marketplace-demand",
            ],
            "allowed_action_scope": "Read-only public digital-product marketplace/category pages for demand, price-band, saturation, and buyer-language notes only; no login, posting, listing, messaging, checkout, account settings, personal data entry, saved changes, or payment/account actions.",
            "forbidden_actions_acknowledged": True,
            "expiration_or_review_time": "2026-06-16T23:59:59Z",
            "approver_identity": "user",
            "operator_confirmation_text": "I approve only this bounded read-only browser validation scope for the listed blocker ids until 2026-06-16T23:59:59Z.",
        },
        "expected_parser_result": {
            "accepted_for_dry_run": True,
            "expected_preview_state": expected_preview_state,
            "expected_real_mutation": False,
            "expected_service_requests_updated": 0,
            "expected_worker_starts": 0,
        },
    }
    positive_fixture_count = 1
    expected_dry_run_preview_count = 1

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    fixture_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO decision parser dry-run contract task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_decision_parser_dry_run_contract_complete":
        failures.append("source CEO decision parser dry-run contract evidence is missing or not complete")
    if not contract_validation.get("all_checks_passed") or contract_validation.get("failure_count") != 0:
        failures.append("source CEO decision parser dry-run contract validation is not clean")
    if source_contract_section_count != 6:
        failures.append(f"expected 6 source contract sections, got {source_contract_section_count}")
    if source_mutation_preview_state_count != 4:
        failures.append(f"expected 4 source mutation preview states, got {source_mutation_preview_state_count}")
    if expected_preview_state not in mutation_preview_states:
        failures.append(f"expected preview state {expected_preview_state} not in contract states")
    if positive_fixture_count != 1:
        failures.append(f"expected 1 positive fixture, got {positive_fixture_count}")
    if expected_dry_run_preview_count != 1:
        failures.append(f"expected 1 dry-run preview, got {expected_dry_run_preview_count}")
    if parser_execution_count != 0:
        failures.append(f"expected 0 parser executions, got {parser_execution_count}")
    if accepted_decision_count != 0:
        failures.append(f"expected 0 accepted decisions, got {accepted_decision_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser positive fixture task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if fixture_evidence_exists_before:
        failures.append(f"CEO decision parser positive fixture evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 196:
        failures.append(f"expected 196 task rows before CEO decision parser positive fixture, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 104:
        failures.append(f"expected 104 evidence rows before CEO decision parser positive fixture, got {lane_evidence_rows_before}")

    fixture_summary = (
        "Created one local positive dry-run fixture for a future CEO decision parser. The fixture should produce a report-only bounded service-request update preview and no mutation."
    )
    fixture_next_action = (
        "Use this fixture with the negative fixtures when implementing the report-only parser; do not apply any preview until explicit mutation approval exists."
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
        "schema_version": "agent_company.ceo_decision_parser_positive_fixture.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_contract_task_id": source_contract_task_id,
        "source_contract_evidence_id": source_contract_evidence_id,
        "source_contract_validation_path": str(CEO_DECISION_PARSER_DRY_RUN_CONTRACT_VALIDATION_JSON),
        "source_contract_section_count": source_contract_section_count,
        "source_mutation_preview_state_count": source_mutation_preview_state_count,
        "positive_fixture_count": positive_fixture_count,
        "positive_fixture": positive_fixture,
        "expected_dry_run_preview_count": expected_dry_run_preview_count,
        "expected_preview_state": expected_preview_state,
        "parser_execution_count": parser_execution_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Positive Fixture",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        fixture_summary,
        "",
        "## Fixture",
        "",
        f"Fixture ID: `{positive_fixture['fixture_id']}`",
        f"Expected preview state: `{expected_preview_state}`",
        "Expected real mutation: `False`",
        "",
        "Allowed scope:",
        "",
        positive_fixture["submitted_intake"]["allowed_action_scope"],
        "",
        "## Boundary",
        "",
        "This is a local positive fixture only. It runs no parser, accepts no decision, approves nothing, and does not assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
        "",
        "## Next Action",
        "",
        fixture_next_action,
        "",
    ]
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
                "Create CEO decision parser positive fixture",
                41,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                fixture_next_action,
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
                "title": "CEO decision parser positive fixture",
                "status": "local_ceo_decision_parser_positive_fixture_complete",
                "summary": fixture_summary,
                "next_action": fixture_next_action,
                "ownership_note": "Generated by platform_engineering from CEO decision parser dry-run contract; fixture is local validation data only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_fixture = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    if task_rows_inserted_by_fixture != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser positive fixture, got {task_rows_inserted_by_fixture}")
    if tasks_table_rows_after != 197:
        failures.append(f"expected 197 task rows after CEO decision parser positive fixture, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 105:
        failures.append(f"expected 105 evidence rows after CEO decision parser positive fixture, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser positive fixture evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser positive fixture")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_fixture": task_rows_inserted_by_fixture,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_positive_fixture_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_contract_task_id": source_contract_task_id,
        "source_contract_evidence_id": source_contract_evidence_id,
        "source_contract_section_count": source_contract_section_count,
        "source_mutation_preview_state_count": source_mutation_preview_state_count,
        "positive_fixture_count": positive_fixture_count,
        "expected_dry_run_preview_count": expected_dry_run_preview_count,
        "expected_preview_state": expected_preview_state,
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
        "task_rows_inserted_by_fixture": task_rows_inserted_by_fixture,
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
                "positive_fixture_count": positive_fixture_count,
                "task_rows_inserted_by_fixture": task_rows_inserted_by_fixture,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
