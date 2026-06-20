from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Signed CEO decision apply-command contract writer."""

from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .ceo_decision_signed_apply_command_contract_content import build_signed_apply_command_contract_content


def write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    contract_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract-20260616"
    contract_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract-20260616"
    source_packet_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet-20260616"
    source_packet_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    packet_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_VALIDATION_JSON)
    packet_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_JSON)
    approval_packet = packet_payload.get("operator_apply_approval_packet", {}) or {}
    target_request_id = packet_payload.get("target_request_id") or approval_packet.get("target_request_id")
    target_request = (
        conn.execute(
            "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    target_status_before = target_request["status"] if target_request else None
    target_status_after = target_status_before
    contract_content = build_signed_apply_command_contract_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_packet_validation_path=str(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_VALIDATION_JSON),
        lane_id=lane_id,
        contract_task_id=contract_task_id,
        contract_evidence_id=contract_evidence_id,
        source_packet_task_id=source_packet_task_id,
        source_packet_evidence_id=source_packet_evidence_id,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
        target_status_after=target_status_after,
    )
    apply_command_contract = contract_content["apply_command_contract"]
    approval_granted_by_contract = contract_content["approval_granted_by_contract"]
    explicit_operator_apply_approval_present = contract_content["explicit_operator_apply_approval_present"]
    apply_command_enabled = contract_content["apply_command_enabled"]
    apply_execution_allowed = contract_content["apply_execution_allowed"]
    target_update_fields = contract_content["target_update_fields"]
    bounded_update_shape = contract_content["bounded_update_shape"]
    command_step_count = contract_content["command_step_count"]
    guard_check_count = contract_content["guard_check_count"]
    target_update_field_count = contract_content["target_update_field_count"]
    rollback_step_count = contract_content["rollback_step_count"]
    local_decision = contract_content["local_decision"]
    recommended_default = contract_content["recommended_default"]
    apply_command_contract_count = contract_content["apply_command_contract_count"]
    mutation_applied_count = contract_content["mutation_applied_count"]
    queue_mutation_count = contract_content["queue_mutation_count"]
    approval_request_count = contract_content["approval_request_count"]
    contract_summary = contract_content["summary"]
    contract_next_action = contract_content["next_action"]
    runtime_boundary = contract_content["runtime_boundary"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_packet_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_packet_task_id,),
    ).fetchone()
    source_packet_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_packet_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (contract_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    contract_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (contract_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_packet_task or source_packet_task["status"] != "complete":
        failures.append("source signed-decision operator apply approval packet task is missing or incomplete")
    if not source_packet_evidence or source_packet_evidence["status"] != "local_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet_complete":
        failures.append("source signed-decision operator apply approval packet evidence is missing or not complete")
    if not packet_validation.get("all_checks_passed") or packet_validation.get("failure_count") != 0:
        failures.append("source signed-decision operator apply approval packet validation is not clean")
    if packet_payload.get("schema_version") != "agent_company.ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet.v1":
        failures.append("source signed-decision operator apply approval packet payload schema drifted")
    if packet_validation.get("approval_granted_by_packet") is not False:
        failures.append("source packet unexpectedly grants approval")
    if packet_validation.get("apply_command_enabled") is not False:
        failures.append("source packet unexpectedly enables apply command")
    if apply_command_contract_count != 1:
        failures.append(f"expected 1 apply command contract, got {apply_command_contract_count}")
    if command_step_count != 7:
        failures.append(f"expected 7 command steps, got {command_step_count}")
    if guard_check_count != 10:
        failures.append(f"expected 10 guard checks, got {guard_check_count}")
    if target_update_field_count != 2:
        failures.append(f"expected 2 target update fields, got {target_update_field_count}")
    if rollback_step_count != 4:
        failures.append(f"expected 4 rollback steps, got {rollback_step_count}")
    if approval_granted_by_contract is not False:
        failures.append("apply command contract unexpectedly grants approval")
    if explicit_operator_apply_approval_present is not False:
        failures.append("explicit operator apply approval unexpectedly present")
    if apply_command_enabled is not False:
        failures.append("apply command contract unexpectedly enables apply command")
    if apply_execution_allowed is not False:
        failures.append("apply command contract unexpectedly allows execution")
    if bounded_update_shape.get("set_fields") != target_update_fields or bounded_update_shape.get("max_rows") != 1:
        failures.append("bounded update shape drifted from the two-field single-row contract")
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
        failures.append("target request already has approval_scope or decision_note before apply command contract")
    if target_task_exists_before:
        failures.append(f"target signed-decision apply command contract task already exists: {contract_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if contract_evidence_exists_before:
        failures.append(f"signed-decision apply command contract evidence already exists: {contract_evidence_id}")
    if tasks_table_rows_before != 219:
        failures.append(f"expected 219 task rows before signed-decision apply command contract, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 127:
        failures.append(f"expected 127 evidence rows before signed-decision apply command contract, got {lane_evidence_rows_before}")

    payload = contract_content["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(contract_content["markdown"], encoding="utf-8")

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
                "Define CEO decision parser apply-readiness signed-decision apply command contract",
                18,
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
                "title": "CEO decision parser apply-readiness signed-decision apply command contract",
                "status": "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract_complete",
                "summary": contract_summary,
                "next_action": contract_next_action,
                "ownership_note": "Generated by platform_engineering from the signed-decision operator apply approval packet; contract remains disabled and performs no mutations.",
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
    task_rows_inserted_by_contract = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (contract_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (contract_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (contract_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during signed-decision apply command contract")
    if task_rows_inserted_by_contract != 1:
        failures.append(f"expected 1 task row inserted by signed-decision apply command contract, got {task_rows_inserted_by_contract}")
    if tasks_table_rows_after != 220:
        failures.append(f"expected 220 task rows after signed-decision apply command contract, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 128:
        failures.append(f"expected 128 evidence rows after signed-decision apply command contract, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("signed-decision apply command contract evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during signed-decision apply command contract")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract_validation.v1",
        "generated_utc": generated_utc,
        "contract_path": str(json_output_path),
        "contract_lane_id": lane_id,
        "contract_task_id": contract_task_id,
        "source_packet_task_id": source_packet_task_id,
        "apply_command_contract_count": apply_command_contract_count,
        "command_step_count": command_step_count,
        "guard_check_count": guard_check_count,
        "target_update_field_count": target_update_field_count,
        "rollback_step_count": rollback_step_count,
        "approval_granted_by_contract": approval_granted_by_contract,
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
                "apply_command_contract_count": apply_command_contract_count,
                "task_rows_inserted_by_contract": task_rows_inserted_by_contract,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
