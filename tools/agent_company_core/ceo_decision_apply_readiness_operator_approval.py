from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Operator approval, no-approval blocker, and decision intake packet writers for apply readiness."""

from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_NO_APPROVAL_BLOCKER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_NO_APPROVAL_BLOCKER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_NO_APPROVAL_BLOCKER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_VALIDATION_JSON,
)
from .ceo_decision_apply_readiness_operator_approval_content import build_ceo_apply_readiness_operator_approval_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_operator_approval_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    packet_task_id = "task-ceo-decision-parser-apply-readiness-operator-approval-packet-20260616"
    packet_evidence_id = "ceo-decision-parser-apply-readiness-operator-approval-packet-20260616"
    source_runner_task_id = "task-ceo-decision-parser-apply-readiness-positive-runner-20260616"
    source_runner_evidence_id = "ceo-decision-parser-apply-readiness-positive-runner-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-operator-approval-packet-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_runner_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_runner_task_id,),
    ).fetchone()
    source_runner_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_runner_evidence_id,),
    ).fetchone()
    runner_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_VALIDATION_JSON)
    positive_fixture_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_JSON)
    positive_fixture = positive_fixture_payload.get("positive_readiness_fixture", {})
    readiness_packet = positive_fixture.get("submitted_readiness", {})
    target_request_id = readiness_packet.get("target_request_id")
    target_request = (
        conn.execute(
            "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    target_service_request_count = 1 if target_request else 0
    target_status_before = target_request["status"] if target_request else None
    target_status_after = target_status_before
    packet_content = build_ceo_apply_readiness_operator_approval_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_runner_validation_path=str(CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_VALIDATION_JSON),
        lane_id=lane_id,
        packet_task_id=packet_task_id,
        packet_evidence_id=packet_evidence_id,
        source_runner_task_id=source_runner_task_id,
        source_runner_evidence_id=source_runner_evidence_id,
        readiness_packet=readiness_packet,
        target_service_request_count=target_service_request_count,
        target_status_before=target_status_before,
        target_status_after=target_status_after,
    )
    planned_field_update_count = packet_content["planned_field_update_count"]
    rollback_check_count = packet_content["rollback_check_count"]
    required_operator_approval_count = packet_content["required_operator_approval_count"]
    approval_statement_count = packet_content["approval_statement_count"]
    operator_approval_packet = packet_content["operator_approval_packet"]
    local_decision = packet_content["local_decision"]
    recommended_default = packet_content["recommended_default"]
    operator_approval_packet_count = packet_content["operator_approval_packet_count"]
    mutation_applied_count = packet_content["mutation_applied_count"]
    queue_mutation_count = packet_content["queue_mutation_count"]
    approval_request_count = packet_content["approval_request_count"]
    packet_summary = packet_content["summary"]
    packet_next_action = packet_content["next_action"]
    runtime_boundary = packet_content["runtime_boundary"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    packet_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_runner_task or source_runner_task["status"] != "complete":
        failures.append("source apply-readiness positive runner task is missing or incomplete")
    if not source_runner_evidence or source_runner_evidence["status"] != "local_ceo_decision_parser_apply_readiness_positive_runner_complete":
        failures.append("source apply-readiness positive runner evidence is missing or not complete")
    if not runner_validation.get("all_checks_passed") or runner_validation.get("failure_count") != 0:
        failures.append("source apply-readiness positive runner validation is not clean")
    if runner_validation.get("accepted_readiness_count") != 1 or runner_validation.get("real_mutation_allowed_count") != 0:
        failures.append("source apply-readiness positive runner did not prove preview-only acceptance")
    if operator_approval_packet_count != 1:
        failures.append(f"expected 1 operator approval packet, got {operator_approval_packet_count}")
    if target_service_request_count != 1:
        failures.append(f"expected 1 target service request, got {target_service_request_count}")
    if planned_field_update_count != 2:
        failures.append(f"expected 2 planned field updates, got {planned_field_update_count}")
    if rollback_check_count != 4:
        failures.append(f"expected 4 rollback checks, got {rollback_check_count}")
    if required_operator_approval_count != 5:
        failures.append(f"expected 5 required operator approvals, got {required_operator_approval_count}")
    if approval_statement_count != 5:
        failures.append(f"expected 5 approval statements, got {approval_statement_count}")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_status_before != "needs_review":
        failures.append(f"expected target status before needs_review, got {target_status_before}")
    if target_status_after != "needs_review":
        failures.append(f"expected target status after needs_review, got {target_status_after}")
    if target_request and (target_request["approval_scope"] is not None or target_request["decision_note"] is not None):
        failures.append("target request already has approval_scope or decision_note before operator approval packet")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply-readiness operator approval packet task already exists: {packet_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if packet_evidence_exists_before:
        failures.append(f"CEO decision parser apply-readiness operator approval packet evidence already exists: {packet_evidence_id}")
    if tasks_table_rows_before != 210:
        failures.append(f"expected 210 task rows before CEO decision parser apply-readiness operator approval packet, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 118:
        failures.append(f"expected 118 evidence rows before CEO decision parser apply-readiness operator approval packet, got {lane_evidence_rows_before}")

    payload = packet_content["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(packet_content["markdown"], encoding="utf-8")

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
                "Prepare CEO decision parser apply-readiness operator approval packet",
                27,
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
                "title": "CEO decision parser apply-readiness operator approval packet",
                "status": "local_ceo_decision_parser_apply_readiness_operator_approval_packet_complete",
                "summary": packet_summary,
                "next_action": packet_next_action,
                "ownership_note": "Generated by platform_engineering from the positive runner; packet is local approval preparation only and does not request approval.",
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
        failures.append("target service request changed during apply-readiness operator approval packet")
    if task_rows_inserted_by_packet != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser apply-readiness operator approval packet, got {task_rows_inserted_by_packet}")
    if tasks_table_rows_after != 211:
        failures.append(f"expected 211 task rows after CEO decision parser apply-readiness operator approval packet, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 119:
        failures.append(f"expected 119 evidence rows after CEO decision parser apply-readiness operator approval packet, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply-readiness operator approval packet evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply-readiness operator approval packet")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_operator_approval_packet_validation.v1",
        "generated_utc": generated_utc,
        "packet_path": str(json_output_path),
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "source_runner_task_id": source_runner_task_id,
        "operator_approval_packet_count": operator_approval_packet_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": planned_field_update_count,
        "rollback_check_count": rollback_check_count,
        "required_operator_approval_count": required_operator_approval_count,
        "approval_statement_count": approval_statement_count,
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
                "operator_approval_packet_count": operator_approval_packet_count,
                "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )



