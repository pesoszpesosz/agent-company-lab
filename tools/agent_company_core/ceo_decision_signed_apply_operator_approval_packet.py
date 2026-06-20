from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Signed CEO decision apply preflight and operator approval packet writers."""

from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_PREFLIGHT_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_PREFLIGHT_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_PREFLIGHT_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_RUNNER_VALIDATION_JSON,
)
from .ceo_decision_signed_apply_operator_approval_packet_content import build_signed_apply_operator_approval_packet_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_OPERATOR_APPLY_APPROVAL_PACKET_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    packet_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet-20260616"
    packet_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet-20260616"
    source_preflight_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-preflight-20260616"
    source_preflight_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-preflight-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet-20260616"

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    preflight_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_PREFLIGHT_VALIDATION_JSON)
    preflight_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_PREFLIGHT_JSON)
    intake_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_JSON)
    decision_fields_template = dict((intake_payload.get("decision_intake_packet", {}) or {}).get("decision_fields") or {})
    target_request_id = preflight_payload.get("target_request_id") or decision_fields_template.get("target_request_id")
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
    packet_content = build_signed_apply_operator_approval_packet_content(
        decision_fields_template=decision_fields_template,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
    )
    local_decision = packet_content["local_decision"]
    recommended_default = packet_content["recommended_default"]
    operator_apply_approval_packet_count = packet_content["operator_apply_approval_packet_count"]
    approval_granted_by_packet = packet_content["approval_granted_by_packet"]
    explicit_operator_apply_approval_present = packet_content["explicit_operator_apply_approval_present"]
    apply_command_enabled = packet_content["apply_command_enabled"]
    mutation_applied_count = packet_content["mutation_applied_count"]
    queue_mutation_count = packet_content["queue_mutation_count"]
    approval_request_count = packet_content["approval_request_count"]
    required_approval_fields = packet_content["required_approval_fields"]
    required_confirmations = packet_content["required_confirmations"]
    required_approval_field_count = packet_content["required_approval_field_count"]
    required_confirmation_count = packet_content["required_confirmation_count"]
    operator_apply_approval_packet = packet_content["operator_apply_approval_packet"]
    packet_summary = packet_content["summary"]
    packet_next_action = packet_content["next_action"]
    runtime_boundary = packet_content["runtime_boundary"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_preflight_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_preflight_task_id,),
    ).fetchone()
    source_preflight_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_preflight_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    packet_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_preflight_task or source_preflight_task["status"] != "complete":
        failures.append("source signed-decision apply preflight task is missing or incomplete")
    if not source_preflight_evidence or source_preflight_evidence["status"] != "local_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight_complete":
        failures.append("source signed-decision apply preflight evidence is missing or not complete")
    if not preflight_validation.get("all_checks_passed") or preflight_validation.get("failure_count") != 0:
        failures.append("source signed-decision apply preflight validation is not clean")
    if preflight_payload.get("schema_version") != "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_preflight.v1":
        failures.append("source signed-decision apply preflight payload schema drifted")
    if preflight_validation.get("apply_blocked_count") != 1:
        failures.append("source apply preflight does not prove apply is blocked")
    if preflight_validation.get("explicit_operator_apply_approval_present") is not False:
        failures.append("source preflight unexpectedly reports explicit operator apply approval")
    if operator_apply_approval_packet_count != 1:
        failures.append(f"expected 1 operator apply approval packet, got {operator_apply_approval_packet_count}")
    if required_approval_field_count != 8:
        failures.append(f"expected 8 required approval fields, got {required_approval_field_count}")
    if required_confirmation_count != 6:
        failures.append(f"expected 6 required confirmations, got {required_confirmation_count}")
    if approval_granted_by_packet is not False:
        failures.append("approval packet unexpectedly grants approval")
    if explicit_operator_apply_approval_present is not False:
        failures.append("explicit operator apply approval unexpectedly present")
    if apply_command_enabled is not False:
        failures.append("approval packet unexpectedly enables apply command")
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
        failures.append("target request already has approval_scope or decision_note before operator apply approval packet")
    if target_task_exists_before:
        failures.append(f"target signed-decision operator apply approval packet task already exists: {packet_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if packet_evidence_exists_before:
        failures.append(f"signed-decision operator apply approval packet evidence already exists: {packet_evidence_id}")
    if tasks_table_rows_before != 218:
        failures.append(f"expected 218 task rows before signed-decision operator apply approval packet, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 126:
        failures.append(f"expected 126 evidence rows before signed-decision operator apply approval packet, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet.v1",
        "generated_utc": generated_utc,
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "packet_evidence_id": packet_evidence_id,
        "source_preflight_task_id": source_preflight_task_id,
        "source_preflight_evidence_id": source_preflight_evidence_id,
        "source_preflight_validation_path": str(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_PREFLIGHT_VALIDATION_JSON),
        "operator_apply_approval_packet_count": operator_apply_approval_packet_count,
        "required_approval_field_count": required_approval_field_count,
        "required_confirmation_count": required_confirmation_count,
        "operator_apply_approval_packet": operator_apply_approval_packet,
        "approval_granted_by_packet": approval_granted_by_packet,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": packet_summary,
        "next_action": packet_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Operator Apply Approval Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        packet_summary,
        "",
        "## Required Fields",
        "",
    ]
    md_lines.extend(f"- `{field}`" for field in required_approval_fields)
    md_lines.extend(["", "## Required Confirmations", ""])
    md_lines.extend(f"- `{confirmation}`" for confirmation in required_confirmations)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is a local draft. It does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            packet_next_action,
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
                packet_task_id,
                lane_id,
                "Draft CEO decision parser apply-readiness signed-decision operator apply approval packet",
                19,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                packet_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": packet_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser apply-readiness signed-decision operator apply approval packet",
                "status": "local_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet_complete",
                "summary": packet_summary,
                "next_action": packet_next_action,
                "ownership_note": "Generated by platform_engineering from the signed-decision apply preflight; packet is a local approval template and performs no mutations.",
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
    task_rows_inserted_by_packet = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (packet_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during signed-decision operator apply approval packet")
    if task_rows_inserted_by_packet != 1:
        failures.append(f"expected 1 task row inserted by signed-decision operator apply approval packet, got {task_rows_inserted_by_packet}")
    if tasks_table_rows_after != 219:
        failures.append(f"expected 219 task rows after signed-decision operator apply approval packet, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 127:
        failures.append(f"expected 127 evidence rows after signed-decision operator apply approval packet, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("signed-decision operator apply approval packet evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during signed-decision operator apply approval packet")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet_validation.v1",
        "generated_utc": generated_utc,
        "packet_path": str(json_output_path),
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "source_preflight_task_id": source_preflight_task_id,
        "operator_apply_approval_packet_count": operator_apply_approval_packet_count,
        "required_approval_field_count": required_approval_field_count,
        "required_confirmation_count": required_confirmation_count,
        "approval_granted_by_packet": approval_granted_by_packet,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
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
        "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
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
                "packet_lane_id": lane_id,
                "packet_task_id": packet_task_id,
                "operator_apply_approval_packet_count": operator_apply_approval_packet_count,
                "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


