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
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .ceo_decision_apply_readiness_decision_intake_content import (
    build_ceo_apply_readiness_decision_intake_artifacts,
    build_ceo_apply_readiness_decision_intake_writer_fields,
    build_ceo_apply_readiness_decision_intake_writer_content,
)


def write_ceo_decision_parser_apply_readiness_decision_intake_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    intake_task_id = "task-ceo-decision-parser-apply-readiness-decision-intake-packet-20260616"
    intake_evidence_id = "ceo-decision-parser-apply-readiness-decision-intake-packet-20260616"
    source_blocker_task_id = "task-ceo-decision-parser-apply-readiness-no-approval-blocker-20260616"
    source_blocker_evidence_id = "ceo-decision-parser-apply-readiness-no-approval-blocker-20260616"
    source_packet_task_id = "task-ceo-decision-parser-apply-readiness-operator-approval-packet-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-decision-intake-packet-20260616"
    local_decision = "ceo_decision_parser_apply_readiness_decision_intake_packet_ready_no_approval"
    recommended_default = "collect_signed_operator_decision_before_apply_command"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_blocker_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_blocker_task_id,),
    ).fetchone()
    source_blocker_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_blocker_evidence_id,),
    ).fetchone()
    blocker_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_NO_APPROVAL_BLOCKER_VALIDATION_JSON)
    packet_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_OPERATOR_APPROVAL_PACKET_JSON)
    operator_approval_packet = packet_payload.get("operator_approval_packet", {})
    target_request_id = operator_approval_packet.get("target_request_id")
    writer_fields = build_ceo_apply_readiness_decision_intake_writer_fields(
        operator_approval_packet=operator_approval_packet,
        source_blocker_task_id=source_blocker_task_id,
        artifact_output_path=str(json_output_path),
    )
    decision_intake_packet_count = writer_fields["decision_intake_packet_count"]
    approval_granted_by_intake_packet = writer_fields["approval_granted_by_intake_packet"]
    apply_command_enabled = writer_fields["apply_command_enabled"]
    mutation_applied_count = writer_fields["mutation_applied_count"]
    queue_mutation_count = writer_fields["queue_mutation_count"]
    approval_request_count = writer_fields["approval_request_count"]
    intake_summary = writer_fields["summary"]
    intake_next_action = writer_fields["next_action"]
    boundary_text = writer_fields["boundary_text"]
    runtime_boundary = writer_fields["runtime_boundary"]
    approval_statement_count = writer_fields["approval_statement_count"]
    decision_fields = writer_fields["decision_fields"]
    decision_field_count = writer_fields["decision_field_count"]
    requires_explicit_signed_decision = writer_fields["requires_explicit_signed_decision"]
    requires_exact_target_request_id = writer_fields["requires_exact_target_request_id"]
    requires_approval_scope_text = writer_fields["requires_approval_scope_text"]
    requires_decision_note_text = writer_fields["requires_decision_note_text"]
    requires_rollback_snapshot_match = writer_fields["requires_rollback_snapshot_match"]
    requires_scope_expiration = writer_fields["requires_scope_expiration"]
    requires_no_external_side_effects_default = writer_fields["requires_no_external_side_effects_default"]
    decision_intake_packet = writer_fields["decision_intake_packet"]
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
    blocked_apply_attempt_count = int(blocker_validation.get("blocked_apply_attempt_count") or 0)


    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (intake_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    intake_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (intake_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_blocker_task or source_blocker_task["status"] != "complete":
        failures.append("source apply-readiness no-approval blocker task is missing or incomplete")
    if not source_blocker_evidence or source_blocker_evidence["status"] != "local_ceo_decision_parser_apply_readiness_no_approval_blocker_complete":
        failures.append("source apply-readiness no-approval blocker evidence is missing or not complete")
    if not blocker_validation.get("all_checks_passed") or blocker_validation.get("failure_count") != 0:
        failures.append("source apply-readiness no-approval blocker validation is not clean")
    if blocked_apply_attempt_count != 1:
        failures.append(f"expected 1 blocked apply attempt, got {blocked_apply_attempt_count}")
    if decision_intake_packet_count != 1:
        failures.append(f"expected 1 decision intake packet, got {decision_intake_packet_count}")
    if decision_field_count != 12:
        failures.append(f"expected 12 decision fields, got {decision_field_count}")
    if approval_statement_count != 5:
        failures.append(f"expected 5 approval statements, got {approval_statement_count}")
    if target_service_request_count != 1:
        failures.append(f"expected 1 target service request, got {target_service_request_count}")
    if not requires_explicit_signed_decision:
        failures.append("decision intake does not require an explicit signed decision")
    if not requires_exact_target_request_id:
        failures.append("decision intake does not require the exact target request id")
    if not requires_approval_scope_text:
        failures.append("decision intake does not require approval_scope text")
    if not requires_decision_note_text:
        failures.append("decision intake does not require decision_note text")
    if not requires_rollback_snapshot_match:
        failures.append("decision intake does not require rollback snapshot match")
    if not requires_scope_expiration:
        failures.append("decision intake does not require scope expiration")
    if not requires_no_external_side_effects_default:
        failures.append("decision intake does not default to no external side effects")
    if approval_granted_by_intake_packet is not False:
        failures.append("decision intake packet unexpectedly grants approval")
    if apply_command_enabled is not False:
        failures.append("decision intake packet unexpectedly enables apply")
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
        failures.append("target request already has approval_scope or decision_note before decision intake packet")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply-readiness decision intake packet task already exists: {intake_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if intake_evidence_exists_before:
        failures.append(f"CEO decision parser apply-readiness decision intake packet evidence already exists: {intake_evidence_id}")
    if tasks_table_rows_before != 212:
        failures.append(f"expected 212 task rows before CEO decision parser apply-readiness decision intake packet, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 120:
        failures.append(f"expected 120 evidence rows before CEO decision parser apply-readiness decision intake packet, got {lane_evidence_rows_before}")

    artifacts = build_ceo_apply_readiness_decision_intake_artifacts(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_blocker_validation_path=str(CEO_DECISION_PARSER_APPLY_READINESS_NO_APPROVAL_BLOCKER_VALIDATION_JSON),
        lane_id=lane_id,
        intake_task_id=intake_task_id,
        intake_evidence_id=intake_evidence_id,
        source_blocker_task_id=source_blocker_task_id,
        source_blocker_evidence_id=source_blocker_evidence_id,
        source_packet_task_id=source_packet_task_id,
        blocked_apply_attempt_count=blocked_apply_attempt_count,
        target_service_request_count=target_service_request_count,
        target_status_before=target_status_before,
        target_status_after=target_status_after,
        local_decision=local_decision,
        recommended_default=recommended_default,
        writer_fields=writer_fields,
    )
    payload = artifacts["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(str(artifacts["markdown"]), encoding="utf-8")
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
                "Prepare CEO decision parser apply-readiness decision intake packet",
                25,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                intake_next_action,
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
                "title": "CEO decision parser apply-readiness decision intake packet",
                "status": "local_ceo_decision_parser_apply_readiness_decision_intake_packet_complete",
                "summary": intake_summary,
                "next_action": intake_next_action,
                "ownership_note": "Generated by platform_engineering from the no-approval blocker; packet is local intake scaffolding only and grants no approval.",
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
    task_rows_inserted_by_intake = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (intake_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (intake_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (intake_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during apply-readiness decision intake packet")
    if task_rows_inserted_by_intake != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser apply-readiness decision intake packet, got {task_rows_inserted_by_intake}")
    if tasks_table_rows_after != 213:
        failures.append(f"expected 213 task rows after CEO decision parser apply-readiness decision intake packet, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 121:
        failures.append(f"expected 121 evidence rows after CEO decision parser apply-readiness decision intake packet, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply-readiness decision intake packet evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply-readiness decision intake packet")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_intake": task_rows_inserted_by_intake,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_decision_intake_packet_validation.v1",
        "generated_utc": generated_utc,
        "intake_path": str(json_output_path),
        "intake_lane_id": lane_id,
        "intake_task_id": intake_task_id,
        "source_blocker_task_id": source_blocker_task_id,
        "source_packet_task_id": source_packet_task_id,
        "decision_intake_packet_count": decision_intake_packet_count,
        "decision_field_count": decision_field_count,
        "approval_statement_count": approval_statement_count,
        "blocked_apply_attempt_count": blocked_apply_attempt_count,
        "target_service_request_count": target_service_request_count,
        "requires_explicit_signed_decision": requires_explicit_signed_decision,
        "requires_exact_target_request_id": requires_exact_target_request_id,
        "requires_approval_scope_text": requires_approval_scope_text,
        "requires_decision_note_text": requires_decision_note_text,
        "requires_rollback_snapshot_match": requires_rollback_snapshot_match,
        "requires_scope_expiration": requires_scope_expiration,
        "requires_no_external_side_effects_default": requires_no_external_side_effects_default,
        "approval_granted_by_intake_packet": approval_granted_by_intake_packet,
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
        "task_rows_inserted_by_intake": task_rows_inserted_by_intake,
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
                "decision_intake_packet_count": decision_intake_packet_count,
                "decision_field_count": decision_field_count,
                "task_rows_inserted_by_intake": task_rows_inserted_by_intake,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )





