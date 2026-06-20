from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Signed CEO decision apply-command fixture writers."""

from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_GUARD_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_GUARD_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_JSON,
)
from .ceo_decision_signed_apply_command_negative_fixture_content import (
    build_signed_apply_command_negative_fixture_artifacts,
    build_signed_apply_command_negative_fixtures,
    build_signed_apply_command_negative_fixtures_content,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures-20260616"
    fixture_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures-20260616"
    source_contract_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract-20260616"
    source_contract_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    contract_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON)
    contract_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_JSON)
    contract = contract_payload.get("apply_command_contract", {}) or {}
    target_request_id = contract_payload.get("target_request_id") or contract.get("target_request_id")
    target_request = (
        conn.execute(
            "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    target_status_before = target_request["status"] if target_request else None
    target_updated_at = target_request["updated_at"] if target_request else None
    fixture_content = build_signed_apply_command_negative_fixtures_content(
        negative_fixtures=build_signed_apply_command_negative_fixtures(),
        target_request_id=target_request_id,
        target_status_before=target_status_before,
    )
    local_decision = fixture_content["local_decision"]
    recommended_default = fixture_content["recommended_default"]
    negative_fixtures = fixture_content["negative_fixtures"]
    fixture_results = fixture_content["fixture_results"]
    apply_command_negative_fixture_count = fixture_content["apply_command_negative_fixture_count"]
    expected_rejection_count = fixture_content["expected_rejection_count"]
    unique_rejection_rule_count = fixture_content["unique_rejection_rule_count"]
    apply_command_execution_count = fixture_content["apply_command_execution_count"]
    approval_granted_by_fixtures = fixture_content["approval_granted_by_fixtures"]
    explicit_operator_apply_approval_present = fixture_content["explicit_operator_apply_approval_present"]
    apply_command_enabled = fixture_content["apply_command_enabled"]
    apply_execution_allowed = fixture_content["apply_execution_allowed"]
    mutation_applied_count = fixture_content["mutation_applied_count"]
    queue_mutation_count = fixture_content["queue_mutation_count"]
    approval_request_count = fixture_content["approval_request_count"]
    target_status_after = fixture_content["target_status_after"]
    fixture_summary = fixture_content["summary"]
    fixture_next_action = fixture_content["next_action"]
    runtime_boundary = fixture_content["runtime_boundary"]
    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_contract_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_contract_task_id,),
    ).fetchone()
    source_contract_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_contract_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    fixture_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_contract_task or source_contract_task["status"] != "complete":
        failures.append("source signed-decision apply command contract task is missing or incomplete")
    if not source_contract_evidence or source_contract_evidence["status"] != "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract_complete":
        failures.append("source signed-decision apply command contract evidence is missing or not complete")
    if not contract_validation.get("all_checks_passed") or contract_validation.get("failure_count") != 0:
        failures.append("source signed-decision apply command contract validation is not clean")
    if contract_payload.get("schema_version") != "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract.v1":
        failures.append("source signed-decision apply command contract payload schema drifted")
    if contract_validation.get("apply_command_enabled") is not False or contract_validation.get("apply_execution_allowed") is not False:
        failures.append("source apply command contract unexpectedly enables execution")
    if apply_command_negative_fixture_count != 6:
        failures.append(f"expected 6 apply command negative fixtures, got {apply_command_negative_fixture_count}")
    if expected_rejection_count != 6:
        failures.append(f"expected 6 rejected fixtures, got {expected_rejection_count}")
    if unique_rejection_rule_count != 6:
        failures.append(f"expected 6 unique rejection rules, got {unique_rejection_rule_count}")
    if any(item.get("matched_expected") is not True for item in fixture_results):
        failures.append("one or more apply command negative fixtures did not match expected rejection")
    if apply_command_execution_count != 0:
        failures.append(f"expected 0 apply command executions, got {apply_command_execution_count}")
    if approval_granted_by_fixtures is not False:
        failures.append("negative fixtures unexpectedly grant approval")
    if explicit_operator_apply_approval_present is not False:
        failures.append("explicit operator apply approval unexpectedly present")
    if apply_command_enabled is not False:
        failures.append("negative fixtures unexpectedly enable apply command")
    if apply_execution_allowed is not False:
        failures.append("negative fixtures unexpectedly allow apply execution")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 transmitted approval requests, got {approval_request_count}")
    if target_status_before != "needs_review":
        failures.append(f"expected target status before needs_review, got {target_status_before}")
    if target_status_after != "needs_review":
        failures.append(f"expected target status after needs_review, got {target_status_after}")
    if target_request and (target_request["approval_scope"] is not None or target_request["decision_note"] is not None):
        failures.append("target request already has approval_scope or decision_note before apply command negative fixtures")
    if target_updated_at != "2026-06-14T14:37:52Z":
        failures.append(f"expected target updated_at snapshot 2026-06-14T14:37:52Z, got {target_updated_at}")
    if target_task_exists_before:
        failures.append(f"target signed-decision apply command negative fixtures task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if fixture_evidence_exists_before:
        failures.append(f"signed-decision apply command negative fixtures evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 220:
        failures.append(f"expected 220 task rows before signed-decision apply command negative fixtures, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 128:
        failures.append(f"expected 128 evidence rows before signed-decision apply command negative fixtures, got {lane_evidence_rows_before}")

    artifacts = build_signed_apply_command_negative_fixture_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        fixture_lane_id=lane_id,
        fixture_task_id=fixture_task_id,
        fixture_evidence_id=fixture_evidence_id,
        source_contract_task_id=source_contract_task_id,
        source_contract_evidence_id=source_contract_evidence_id,
        source_contract_validation_path=CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON,
        fixture_content=fixture_content,
    )
    payload = artifacts["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(artifacts["markdown"], encoding="utf-8")

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
                "Create CEO decision parser apply-readiness signed-decision apply command negative fixtures",
                17,
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
                "title": "CEO decision parser apply-readiness signed-decision apply command negative fixtures",
                "status": "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures_complete",
                "summary": fixture_summary,
                "next_action": fixture_next_action,
                "ownership_note": "Generated by platform_engineering from the signed-decision apply command contract; fixtures are local-only and perform no mutations.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    target_after = (
        conn.execute(
            "SELECT status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    task_rows_inserted_by_fixture = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during signed-decision apply command negative fixtures")
    if task_rows_inserted_by_fixture != 1:
        failures.append(f"expected 1 task row inserted by signed-decision apply command negative fixtures, got {task_rows_inserted_by_fixture}")
    if tasks_table_rows_after != 221:
        failures.append(f"expected 221 task rows after signed-decision apply command negative fixtures, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 129:
        failures.append(f"expected 129 evidence rows after signed-decision apply command negative fixtures, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("signed-decision apply command negative fixtures evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during signed-decision apply command negative fixtures")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_contract_task_id": source_contract_task_id,
        "apply_command_negative_fixture_count": apply_command_negative_fixture_count,
        "expected_rejection_count": expected_rejection_count,
        "unique_rejection_rule_count": unique_rejection_rule_count,
        "apply_command_execution_count": apply_command_execution_count,
        "approval_granted_by_fixtures": approval_granted_by_fixtures,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
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
                "apply_command_negative_fixture_count": apply_command_negative_fixture_count,
                "task_rows_inserted_by_fixture": task_rows_inserted_by_fixture,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


