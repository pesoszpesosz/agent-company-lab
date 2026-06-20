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

def write_ceo_decision_parser_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_PREFLIGHT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    preflight_task_id = "task-ceo-decision-parser-preflight-20260616"
    preflight_evidence_id = "ceo-decision-parser-preflight-20260616"
    source_fixtures_task_id = "task-ceo-decision-intake-negative-fixtures-20260616"
    source_fixtures_evidence_id = "ceo-decision-intake-negative-fixtures-20260616"
    duplicate_key = "ceo-decision-parser-preflight-20260616"
    local_decision = "ceo_decision_parser_preflight_ready_parser_not_implemented"
    recommended_default = "do_not_parse_or_apply_decisions_until_preflight_is_implemented"
    parser_implementation_status = "not_implemented"
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
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_fixtures_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_fixtures_evidence_id,),
    ).fetchone()
    fixtures_validation = load_json(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON)
    fixtures_payload = load_json(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON)
    source_negative_fixture_count = int(fixtures_payload.get("negative_fixture_count", 0))
    source_expected_rejection_count = int(fixtures_payload.get("expected_rejection_count", 0))
    source_accepted_fixture_count = int(fixtures_payload.get("accepted_fixture_count", 0))

    preflight_checks = [
        {
            "check_id": "load_guard_contract",
            "blocking": True,
            "requirement": "Parser must load the current CEO decision intake guard schema and known packet/option IDs.",
        },
        {
            "check_id": "validate_required_fields",
            "blocking": True,
            "requirement": "Parser must require all eight intake fields before considering a decision.",
        },
        {
            "check_id": "reject_all_negative_fixtures",
            "blocking": True,
            "requirement": "Parser must reject all six negative fixtures with the expected rule ids.",
        },
        {
            "check_id": "scope_to_known_blockers",
            "blocking": True,
            "requirement": "Parser must accept only known blocker ids from the selected decision packet.",
        },
        {
            "check_id": "enforce_forbidden_actions",
            "blocking": True,
            "requirement": "Parser must reject any scope that permits forbidden public, account, payment, wallet, submission, or security-testing actions.",
        },
        {
            "check_id": "require_expiration_or_review",
            "blocking": True,
            "requirement": "Parser must require an expiration or review time before any bounded approval can be considered.",
        },
        {
            "check_id": "dry_run_before_mutation",
            "blocking": True,
            "requirement": "Parser must produce a dry-run mutation preview before changing service_requests or starting workers.",
        },
    ]
    preflight_check_count = len(preflight_checks)
    blocking_check_count = sum(1 for check in preflight_checks if check["blocking"])

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    preflight_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO decision intake negative fixtures task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_decision_intake_negative_fixtures_complete":
        failures.append("source CEO decision intake negative fixtures evidence is missing or not complete")
    if not fixtures_validation.get("all_checks_passed") or fixtures_validation.get("failure_count") != 0:
        failures.append("source CEO decision intake negative fixtures validation is not clean")
    if source_negative_fixture_count != 6:
        failures.append(f"expected 6 source negative fixtures, got {source_negative_fixture_count}")
    if source_expected_rejection_count != 6:
        failures.append(f"expected 6 source expected rejections, got {source_expected_rejection_count}")
    if source_accepted_fixture_count != 0:
        failures.append(f"expected 0 source accepted fixtures, got {source_accepted_fixture_count}")
    if preflight_check_count != 7:
        failures.append(f"expected 7 preflight checks, got {preflight_check_count}")
    if blocking_check_count != 7:
        failures.append(f"expected 7 blocking checks, got {blocking_check_count}")
    if parser_implementation_status != "not_implemented":
        failures.append(f"expected parser status not_implemented, got {parser_implementation_status}")
    if accepted_decision_count != 0:
        failures.append(f"expected 0 accepted decisions, got {accepted_decision_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser preflight task already exists: {preflight_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if preflight_evidence_exists_before:
        failures.append(f"CEO decision parser preflight evidence already exists: {preflight_evidence_id}")
    if tasks_table_rows_before != 194:
        failures.append(f"expected 194 task rows before CEO decision parser preflight, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 102:
        failures.append(f"expected 102 evidence rows before CEO decision parser preflight, got {lane_evidence_rows_before}")

    preflight_summary = (
        "Created a local CEO decision parser preflight defining seven blocking checks required before any future parser can mutate service requests."
    )
    preflight_next_action = (
        "Implement a dry-run parser only after these preflight checks are encoded; until then no decision text can be parsed or applied."
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
        "schema_version": "agent_company.ceo_decision_parser_preflight.v1",
        "generated_utc": generated_utc,
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "preflight_evidence_id": preflight_evidence_id,
        "source_fixtures_task_id": source_fixtures_task_id,
        "source_fixtures_evidence_id": source_fixtures_evidence_id,
        "source_fixtures_validation_path": str(CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON),
        "source_negative_fixture_count": source_negative_fixture_count,
        "source_expected_rejection_count": source_expected_rejection_count,
        "source_accepted_fixture_count": source_accepted_fixture_count,
        "preflight_check_count": preflight_check_count,
        "blocking_check_count": blocking_check_count,
        "preflight_checks": preflight_checks,
        "parser_implementation_status": parser_implementation_status,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": preflight_summary,
        "next_action": preflight_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Preflight",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        preflight_summary,
        "",
        f"Parser implementation status: `{parser_implementation_status}`",
        "",
        "## Blocking Checks",
        "",
    ]
    for check in preflight_checks:
        md_lines.append(f"- `{check['check_id']}`: {check['requirement']}")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local preflight only. It implements no parser, accepts no decisions, and does not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            preflight_next_action,
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
                preflight_task_id,
                lane_id,
                "Create CEO decision parser preflight",
                43,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                preflight_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": preflight_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser preflight",
                "status": "local_ceo_decision_parser_preflight_complete",
                "summary": preflight_summary,
                "next_action": preflight_next_action,
                "ownership_note": "Generated by platform_engineering from CEO decision intake negative fixtures; preflight is local and implements no parser.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_preflight = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (preflight_task_id,)) else 0
    if task_rows_inserted_by_preflight != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser preflight, got {task_rows_inserted_by_preflight}")
    if tasks_table_rows_after != 195:
        failures.append(f"expected 195 task rows after CEO decision parser preflight, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 103:
        failures.append(f"expected 103 evidence rows after CEO decision parser preflight, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser preflight evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser preflight")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": str(json_output_path),
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "source_fixtures_task_id": source_fixtures_task_id,
        "source_fixtures_evidence_id": source_fixtures_evidence_id,
        "source_negative_fixture_count": source_negative_fixture_count,
        "source_expected_rejection_count": source_expected_rejection_count,
        "source_accepted_fixture_count": source_accepted_fixture_count,
        "preflight_check_count": preflight_check_count,
        "blocking_check_count": blocking_check_count,
        "parser_implementation_status": parser_implementation_status,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
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
                "preflight_lane_id": lane_id,
                "preflight_task_id": preflight_task_id,
                "preflight_check_count": preflight_check_count,
                "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

