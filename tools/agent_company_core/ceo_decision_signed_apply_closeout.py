from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Signed CEO decision apply-command closeout writer."""

from .ceo_decision_signed_apply_closeout_content import (
    build_signed_apply_command_closeout_artifacts,
    build_signed_apply_command_closeout_content,
)
from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CLOSEOUT_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CLOSEOUT_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CLOSEOUT_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CLOSEOUT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CLOSEOUT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CLOSEOUT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    closeout_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout-20260616"
    closeout_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout-20260616"
    source_positive_runner_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner-20260616"
    source_positive_runner_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_validations = [
        {
            "id": "apply_command_contract",
            "task_id": "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract-20260616",
            "path": CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON,
            "validation": load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_CONTRACT_VALIDATION_JSON),
        },
        {
            "id": "apply_command_negative_fixtures",
            "task_id": "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures-20260616",
            "path": CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_VALIDATION_JSON,
            "validation": load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_NEGATIVE_FIXTURES_VALIDATION_JSON),
        },
        {
            "id": "apply_command_guard_runner",
            "task_id": "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-guard-runner-20260616",
            "path": CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_GUARD_RUNNER_VALIDATION_JSON,
            "validation": load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_GUARD_RUNNER_VALIDATION_JSON),
        },
        {
            "id": "apply_command_positive_runner",
            "task_id": source_positive_runner_task_id,
            "path": CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_VALIDATION_JSON,
            "validation": load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_VALIDATION_JSON),
        },
    ]
    closeout_content = build_signed_apply_command_closeout_content(source_validations)
    apply_command_closeout_count = closeout_content["apply_command_closeout_count"]
    source_validation_count = closeout_content["source_validation_count"]
    passed_source_validation_count = closeout_content["passed_source_validation_count"]
    remaining_gate_count = closeout_content["remaining_gate_count"]
    ready_for_real_mutation = closeout_content["ready_for_real_mutation"]
    approval_granted_by_closeout = closeout_content["approval_granted_by_closeout"]
    explicit_operator_apply_approval_present = closeout_content["explicit_operator_apply_approval_present"]
    apply_command_enabled = closeout_content["apply_command_enabled"]
    apply_execution_allowed = closeout_content["apply_execution_allowed"]
    mutation_applied_count = closeout_content["mutation_applied_count"]
    queue_mutation_count = closeout_content["queue_mutation_count"]
    approval_request_count = closeout_content["approval_request_count"]
    closeout_summary = closeout_content["summary"]
    closeout_next_action = closeout_content["next_action"]
    runtime_boundary = closeout_content["runtime_boundary"]
    target_request_id = "req-wave4-digital-products-browser-readonly-20260614"
    target_request = conn.execute(
        "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
        (target_request_id,),
    ).fetchone()
    target_status_before = target_request["status"] if target_request else None
    target_status_after = target_status_before

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_positive_runner_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_positive_runner_task_id,),
    ).fetchone()
    source_positive_runner_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_positive_runner_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (closeout_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    closeout_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (closeout_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_positive_runner_task or source_positive_runner_task["status"] != "complete":
        failures.append("source signed-decision apply command positive runner task is missing or incomplete")
    if not source_positive_runner_evidence or source_positive_runner_evidence["status"] != "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner_complete":
        failures.append("source signed-decision apply command positive runner evidence is missing or not complete")
    if apply_command_closeout_count != 1:
        failures.append(f"expected 1 apply command closeout, got {apply_command_closeout_count}")
    if source_validation_count != 4:
        failures.append(f"expected 4 source validations, got {source_validation_count}")
    if passed_source_validation_count != 4:
        failures.append(f"expected 4 passed source validations, got {passed_source_validation_count}")
    if remaining_gate_count != 5:
        failures.append(f"expected 5 remaining gates, got {remaining_gate_count}")
    if ready_for_real_mutation is not False:
        failures.append("closeout unexpectedly marks real mutation ready")
    if approval_granted_by_closeout is not False:
        failures.append("closeout unexpectedly grants approval")
    if explicit_operator_apply_approval_present is not False:
        failures.append("explicit operator apply approval unexpectedly present")
    if apply_command_enabled is not False:
        failures.append("closeout unexpectedly enables apply command")
    if apply_execution_allowed is not False:
        failures.append("closeout unexpectedly allows apply execution")
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
        failures.append("target request already has approval_scope or decision_note before apply command closeout")
    if target_task_exists_before:
        failures.append(f"target signed-decision apply command closeout task already exists: {closeout_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if closeout_evidence_exists_before:
        failures.append(f"signed-decision apply command closeout evidence already exists: {closeout_evidence_id}")
    if tasks_table_rows_before != 224:
        failures.append(f"expected 224 task rows before signed-decision apply command closeout, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 132:
        failures.append(f"expected 132 evidence rows before signed-decision apply command closeout, got {lane_evidence_rows_before}")

    artifacts = build_signed_apply_command_closeout_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        closeout_task_id=closeout_task_id,
        closeout_evidence_id=closeout_evidence_id,
        source_positive_runner_task_id=source_positive_runner_task_id,
        source_positive_runner_evidence_id=source_positive_runner_evidence_id,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
        target_status_after=target_status_after,
        closeout_content=closeout_content,
    )
    payload = artifacts["payload"]
    local_decision = payload["local_decision"]
    recommended_default = payload["recommended_default"]
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
                closeout_task_id,
                lane_id,
                "Close out CEO decision parser apply-readiness signed-decision apply command readiness",
                13,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                closeout_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": closeout_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser apply-readiness signed-decision apply command closeout",
                "status": "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout_complete",
                "summary": closeout_summary,
                "next_action": closeout_next_action,
                "ownership_note": "Generated by platform_engineering from the signed-decision apply command positive runner; closeout is local-only and performs no mutations.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    target_after = conn.execute(
        "SELECT status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
        (target_request_id,),
    ).fetchone()
    task_rows_inserted_by_closeout = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (closeout_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (closeout_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (closeout_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during signed-decision apply command closeout")
    if task_rows_inserted_by_closeout != 1:
        failures.append(f"expected 1 task row inserted by signed-decision apply command closeout, got {task_rows_inserted_by_closeout}")
    if tasks_table_rows_after != 225:
        failures.append(f"expected 225 task rows after signed-decision apply command closeout, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 133:
        failures.append(f"expected 133 evidence rows after signed-decision apply command closeout, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("signed-decision apply command closeout evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during signed-decision apply command closeout")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_closeout": task_rows_inserted_by_closeout,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout_validation.v1",
        "generated_utc": generated_utc,
        "closeout_path": str(json_output_path),
        "closeout_lane_id": lane_id,
        "closeout_task_id": closeout_task_id,
        "source_positive_runner_task_id": source_positive_runner_task_id,
        "apply_command_closeout_count": apply_command_closeout_count,
        "source_validation_count": source_validation_count,
        "passed_source_validation_count": passed_source_validation_count,
        "remaining_gate_count": remaining_gate_count,
        "ready_for_real_mutation": ready_for_real_mutation,
        "approval_granted_by_closeout": approval_granted_by_closeout,
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
        "task_rows_inserted_by_closeout": task_rows_inserted_by_closeout,
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
                "closeout_lane_id": lane_id,
                "closeout_task_id": closeout_task_id,
                "apply_command_closeout_count": apply_command_closeout_count,
                "remaining_gate_count": remaining_gate_count,
                "task_rows_inserted_by_closeout": task_rows_inserted_by_closeout,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


