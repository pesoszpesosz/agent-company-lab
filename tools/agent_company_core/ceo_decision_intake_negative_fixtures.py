from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .ceo_decision_intake_negative_fixture_content import build_ceo_decision_intake_negative_fixture_content
from .constants import (
    CEO_BLOCKER_TRIAGE_JSON,
    CEO_BLOCKER_TRIAGE_REPORT,
    CEO_BLOCKER_TRIAGE_VALIDATION_JSON,
    CEO_DECISION_INTAKE_GUARD_JSON,
    CEO_DECISION_INTAKE_GUARD_REPORT,
    CEO_DECISION_INTAKE_GUARD_VALIDATION_JSON,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PACKET_DRAFTS_JSON,
    CEO_DECISION_PACKET_DRAFTS_REPORT,
    CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON,
    CEO_GATE_BLOCKER_BOARD_JSON,
    CEO_GATE_BLOCKER_BOARD_REPORT,
    CEO_GATE_BLOCKER_BOARD_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_intake_negative_fixtures(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-ceo-decision-intake-negative-fixtures-20260616"
    fixture_evidence_id = "ceo-decision-intake-negative-fixtures-20260616"
    source_guard_task_id = "task-ceo-decision-intake-guard-20260616"
    source_guard_evidence_id = "ceo-decision-intake-guard-20260616"
    duplicate_key = "ceo-decision-intake-negative-fixtures-20260616"
    local_decision = "ceo_decision_intake_negative_fixtures_ready"
    recommended_default = "reject_ambiguous_or_unscoped_decisions"
    approval_request_count = 0
    runnable_without_approval_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_guard_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_guard_evidence_id,),
    ).fetchone()
    guard_validation = load_json(CEO_DECISION_INTAKE_GUARD_VALIDATION_JSON)
    guard_payload = load_json(CEO_DECISION_INTAKE_GUARD_JSON)
    known_packet_ids = guard_payload.get("known_packet_ids", [])
    known_option_ids = guard_payload.get("known_option_ids", [])
    required_fields = guard_payload.get("required_fields", [])
    source_required_field_count = int(guard_payload.get("required_field_count", 0))
    source_invalid_decision_rule_count = int(guard_payload.get("invalid_decision_rule_count", 0))

    fixture_content = build_ceo_decision_intake_negative_fixture_content(
        known_packet_ids=known_packet_ids,
        known_option_ids=known_option_ids,
    )
    negative_fixtures = fixture_content["negative_fixtures"]
    negative_fixture_count = fixture_content["negative_fixture_count"]
    expected_rejection_count = fixture_content["expected_rejection_count"]
    accepted_fixture_count = fixture_content["accepted_fixture_count"]
    covered_rule_ids = fixture_content["covered_rule_ids"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    fixture_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO decision intake guard task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_decision_intake_guard_complete":
        failures.append("source CEO decision intake guard evidence is missing or not complete")
    if not guard_validation.get("all_checks_passed") or guard_validation.get("failure_count") != 0:
        failures.append("source CEO decision intake guard validation is not clean")
    if source_required_field_count != 8:
        failures.append(f"expected 8 source required fields, got {source_required_field_count}")
    if len(required_fields) != 8:
        failures.append(f"expected 8 required field names, got {len(required_fields)}")
    if source_invalid_decision_rule_count != 6:
        failures.append(f"expected 6 source invalid decision rules, got {source_invalid_decision_rule_count}")
    if negative_fixture_count != 6:
        failures.append(f"expected 6 negative fixtures, got {negative_fixture_count}")
    if expected_rejection_count != 6:
        failures.append(f"expected 6 expected rejections, got {expected_rejection_count}")
    if accepted_fixture_count != 0:
        failures.append(f"expected 0 accepted fixtures, got {accepted_fixture_count}")
    if len(covered_rule_ids) != 6:
        failures.append(f"expected fixtures to cover 6 rules, got {len(covered_rule_ids)}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision intake negative fixtures task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if fixture_evidence_exists_before:
        failures.append(f"CEO decision intake negative fixtures evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 193:
        failures.append(f"expected 193 task rows before CEO decision intake negative fixtures, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 101:
        failures.append(f"expected 101 evidence rows before CEO decision intake negative fixtures, got {lane_evidence_rows_before}")

    fixture_summary = (
        "Created local negative fixtures for the CEO decision intake guard, covering every rejection rule with no accepted fixture."
    )
    fixture_next_action = (
        "Use these fixtures when implementing any future decision parser; a parser must reject all six before it can mutate service requests."
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
        "schema_version": "agent_company.ceo_decision_intake_negative_fixtures.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_guard_task_id": source_guard_task_id,
        "source_guard_evidence_id": source_guard_evidence_id,
        "source_guard_validation_path": str(CEO_DECISION_INTAKE_GUARD_VALIDATION_JSON),
        "source_required_field_count": source_required_field_count,
        "source_invalid_decision_rule_count": source_invalid_decision_rule_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "negative_fixture_count": negative_fixture_count,
        "expected_rejection_count": expected_rejection_count,
        "accepted_fixture_count": accepted_fixture_count,
        "covered_rule_ids": covered_rule_ids,
        "negative_fixtures": negative_fixtures,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Intake Negative Fixtures",
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
        "## Fixtures",
        "",
        "| Fixture | Expected Rule | Accepted |",
        "| --- | --- | --- |",
    ]
    for fixture in negative_fixtures:
        md_lines.append(f"| `{fixture['fixture_id']}` | `{fixture['expected_rule_id']}` | `{fixture['expected_accepted']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These are local negative fixtures only. They accept no decisions and do not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            fixture_next_action,
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
                "Create CEO decision intake negative fixtures",
                44,
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
                "title": "CEO decision intake negative fixtures",
                "status": "local_ceo_decision_intake_negative_fixtures_complete",
                "summary": fixture_summary,
                "next_action": fixture_next_action,
                "ownership_note": "Generated by platform_engineering from CEO decision intake guard; fixtures are local validation data only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_fixtures = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    if task_rows_inserted_by_fixtures != 1:
        failures.append(f"expected 1 task row inserted by CEO decision intake negative fixtures, got {task_rows_inserted_by_fixtures}")
    if tasks_table_rows_after != 194:
        failures.append(f"expected 194 task rows after CEO decision intake negative fixtures, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 102:
        failures.append(f"expected 102 evidence rows after CEO decision intake negative fixtures, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision intake negative fixtures evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision intake negative fixtures")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_fixtures": task_rows_inserted_by_fixtures,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_intake_negative_fixtures_validation.v1",
        "generated_utc": generated_utc,
        "fixtures_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_guard_task_id": source_guard_task_id,
        "source_guard_evidence_id": source_guard_evidence_id,
        "source_required_field_count": source_required_field_count,
        "source_invalid_decision_rule_count": source_invalid_decision_rule_count,
        "negative_fixture_count": negative_fixture_count,
        "expected_rejection_count": expected_rejection_count,
        "accepted_fixture_count": accepted_fixture_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_fixtures": task_rows_inserted_by_fixtures,
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
                "negative_fixture_count": negative_fixture_count,
                "task_rows_inserted_by_fixtures": task_rows_inserted_by_fixtures,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


