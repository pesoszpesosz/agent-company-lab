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

def write_ceo_decision_parser_dry_run_contract(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_DRY_RUN_CONTRACT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_DRY_RUN_CONTRACT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_DRY_RUN_CONTRACT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    contract_task_id = "task-ceo-decision-parser-dry-run-contract-20260616"
    contract_evidence_id = "ceo-decision-parser-dry-run-contract-20260616"
    source_preflight_task_id = "task-ceo-decision-parser-preflight-20260616"
    source_preflight_evidence_id = "ceo-decision-parser-preflight-20260616"
    duplicate_key = "ceo-decision-parser-dry-run-contract-20260616"
    local_decision = "ceo_decision_parser_dry_run_contract_ready_parser_not_executed"
    recommended_default = "report_only_dry_run_before_any_mutation"
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
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_preflight_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_preflight_evidence_id,),
    ).fetchone()
    preflight_validation = load_json(CEO_DECISION_PARSER_PREFLIGHT_VALIDATION_JSON)
    preflight_payload = load_json(CEO_DECISION_PARSER_PREFLIGHT_JSON)
    source_preflight_check_count = int(preflight_payload.get("preflight_check_count", 0))
    source_blocking_check_count = int(preflight_payload.get("blocking_check_count", 0))

    contract_sections = [
        {
            "section_id": "input_snapshot",
            "required": True,
            "description": "Echo the submitted decision intake and loaded guard version without modifying it.",
        },
        {
            "section_id": "field_validation",
            "required": True,
            "description": "Report missing, unknown, malformed, or ambiguous required fields.",
        },
        {
            "section_id": "rule_evaluation",
            "required": True,
            "description": "Map every rejection or acceptance condition to an explicit guard/preflight rule id.",
        },
        {
            "section_id": "scope_boundary",
            "required": True,
            "description": "List allowed blocker ids, allowed actions, forbidden actions, and expiration/review time.",
        },
        {
            "section_id": "mutation_preview",
            "required": True,
            "description": "Preview proposed service_request status changes and worker starts without applying them.",
        },
        {
            "section_id": "audit_footer",
            "required": True,
            "description": "Emit parser version, source artifact paths, hash inputs, and zero-side-effect counters.",
        },
    ]
    mutation_preview_states = [
        "no_change",
        "would_keep_held",
        "would_reject_or_park",
        "would_create_bounded_service_request_update",
    ]
    contract_section_count = len(contract_sections)
    mutation_preview_state_count = len(mutation_preview_states)

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (contract_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    contract_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (contract_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO decision parser preflight task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_decision_parser_preflight_complete":
        failures.append("source CEO decision parser preflight evidence is missing or not complete")
    if not preflight_validation.get("all_checks_passed") or preflight_validation.get("failure_count") != 0:
        failures.append("source CEO decision parser preflight validation is not clean")
    if source_preflight_check_count != 7:
        failures.append(f"expected 7 source preflight checks, got {source_preflight_check_count}")
    if source_blocking_check_count != 7:
        failures.append(f"expected 7 source blocking checks, got {source_blocking_check_count}")
    if contract_section_count != 6:
        failures.append(f"expected 6 contract sections, got {contract_section_count}")
    if mutation_preview_state_count != 4:
        failures.append(f"expected 4 mutation preview states, got {mutation_preview_state_count}")
    if parser_execution_count != 0:
        failures.append(f"expected 0 parser executions, got {parser_execution_count}")
    if accepted_decision_count != 0:
        failures.append(f"expected 0 accepted decisions, got {accepted_decision_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser dry-run contract task already exists: {contract_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if contract_evidence_exists_before:
        failures.append(f"CEO decision parser dry-run contract evidence already exists: {contract_evidence_id}")
    if tasks_table_rows_before != 195:
        failures.append(f"expected 195 task rows before CEO decision parser dry-run contract, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 103:
        failures.append(f"expected 103 evidence rows before CEO decision parser dry-run contract, got {lane_evidence_rows_before}")

    contract_summary = (
        "Created a local dry-run output contract for any future CEO decision parser. The contract defines report-only sections and mutation-preview states without executing a parser."
    )
    contract_next_action = (
        "Implement a report-only parser against this contract before any real service_request mutation path is allowed."
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
        "schema_version": "agent_company.ceo_decision_parser_dry_run_contract.v1",
        "generated_utc": generated_utc,
        "contract_lane_id": lane_id,
        "contract_task_id": contract_task_id,
        "contract_evidence_id": contract_evidence_id,
        "source_preflight_task_id": source_preflight_task_id,
        "source_preflight_evidence_id": source_preflight_evidence_id,
        "source_preflight_validation_path": str(CEO_DECISION_PARSER_PREFLIGHT_VALIDATION_JSON),
        "source_preflight_check_count": source_preflight_check_count,
        "source_blocking_check_count": source_blocking_check_count,
        "contract_section_count": contract_section_count,
        "contract_sections": contract_sections,
        "mutation_preview_state_count": mutation_preview_state_count,
        "mutation_preview_states": mutation_preview_states,
        "parser_execution_count": parser_execution_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": contract_summary,
        "next_action": contract_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Dry-Run Contract",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        contract_summary,
        "",
        "## Contract Sections",
        "",
    ]
    for section in contract_sections:
        md_lines.append(f"- `{section['section_id']}`: {section['description']}")
    md_lines.extend(["", "## Mutation Preview States", ""])
    for state in mutation_preview_states:
        md_lines.append(f"- `{state}`")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local dry-run contract only. It runs no parser, accepts no decisions, and does not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            contract_next_action,
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
                contract_task_id,
                lane_id,
                "Create CEO decision parser dry-run contract",
                42,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                contract_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": contract_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser dry-run contract",
                "status": "local_ceo_decision_parser_dry_run_contract_complete",
                "summary": contract_summary,
                "next_action": contract_next_action,
                "ownership_note": "Generated by platform_engineering from CEO decision parser preflight; contract is local and runs no parser.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_contract = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (contract_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (contract_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (contract_task_id,)) else 0
    if task_rows_inserted_by_contract != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser dry-run contract, got {task_rows_inserted_by_contract}")
    if tasks_table_rows_after != 196:
        failures.append(f"expected 196 task rows after CEO decision parser dry-run contract, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 104:
        failures.append(f"expected 104 evidence rows after CEO decision parser dry-run contract, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser dry-run contract evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser dry-run contract")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_contract": task_rows_inserted_by_contract,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_dry_run_contract_validation.v1",
        "generated_utc": generated_utc,
        "contract_path": str(json_output_path),
        "contract_lane_id": lane_id,
        "contract_task_id": contract_task_id,
        "source_preflight_task_id": source_preflight_task_id,
        "source_preflight_evidence_id": source_preflight_evidence_id,
        "source_preflight_check_count": source_preflight_check_count,
        "source_blocking_check_count": source_blocking_check_count,
        "contract_section_count": contract_section_count,
        "mutation_preview_state_count": mutation_preview_state_count,
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
        "task_rows_inserted_by_contract": task_rows_inserted_by_contract,
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
                "contract_lane_id": lane_id,
                "contract_task_id": contract_task_id,
                "contract_section_count": contract_section_count,
                "task_rows_inserted_by_contract": task_rows_inserted_by_contract,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

