from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Signed CEO decision apply-command runner writers."""

from .ceo_decision_signed_apply_command_positive_runner_content import build_signed_apply_command_positive_runner_artifacts, build_signed_apply_command_positive_runner_content
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
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_RUNNER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    runner_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner-20260616"
    runner_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner-20260616"
    source_fixture_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-fixture-20260616"
    source_fixture_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-fixture-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner-20260616"
    local_decision = "ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner_accepted_preview_only_no_mutation"
    recommended_default = "positive_apply_runner_still_requires_explicit_real_operator_approval_before_mutation"
    approval_granted_by_runner = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    apply_execution_allowed = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    fixture_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_FIXTURE_VALIDATION_JSON)
    fixture_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_FIXTURE_JSON)
    signed_fixture = fixture_payload.get("signed_operator_apply_fixture", {}) or {}
    target_request_id = signed_fixture.get("target_request_id") or fixture_payload.get("target_request_id")
    target_request = (
        conn.execute(
            "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    target_status_before = target_request["status"] if target_request else None
    runner_content = build_signed_apply_command_positive_runner_content(
        signed_fixture=signed_fixture,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
    )
    target_status_after = runner_content["target_status_after"]
    local_decision = runner_content["local_decision"]
    recommended_default = runner_content["recommended_default"]
    positive_results = runner_content["positive_results"]
    positive_apply_command_execution_count = runner_content["positive_apply_command_execution_count"]
    accepted_apply_fixture_count = runner_content["accepted_apply_fixture_count"]
    rejected_apply_fixture_count = runner_content["rejected_apply_fixture_count"]
    preview_state_match_count = runner_content["preview_state_match_count"]
    real_mutation_allowed_count = runner_content["real_mutation_allowed_count"]
    approval_granted_by_runner = runner_content["approval_granted_by_runner"]
    explicit_operator_apply_approval_present = runner_content["explicit_operator_apply_approval_present"]
    apply_command_enabled = runner_content["apply_command_enabled"]
    apply_execution_allowed = runner_content["apply_execution_allowed"]
    mutation_applied_count = runner_content["mutation_applied_count"]
    queue_mutation_count = runner_content["queue_mutation_count"]
    approval_request_count = runner_content["approval_request_count"]
    runner_summary = runner_content["summary"]
    runner_next_action = runner_content["next_action"]
    runtime_boundary = runner_content["runtime_boundary"]
    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_fixture_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_fixture_task_id,),
    ).fetchone()
    source_fixture_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_fixture_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    runner_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_fixture_task or source_fixture_task["status"] != "complete":
        failures.append("source signed-decision apply command positive fixture task is missing or incomplete")
    if not source_fixture_evidence or source_fixture_evidence["status"] != "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture_complete":
        failures.append("source signed-decision apply command positive fixture evidence is missing or not complete")
    if not fixture_validation.get("all_checks_passed") or fixture_validation.get("failure_count") != 0:
        failures.append("source signed-decision apply command positive fixture validation is not clean")
    if fixture_payload.get("schema_version") != "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture.v1":
        failures.append("source signed-decision apply command positive fixture payload schema drifted")
    if positive_apply_command_execution_count != 1:
        failures.append(f"expected 1 positive apply command execution, got {positive_apply_command_execution_count}")
    if accepted_apply_fixture_count != 1:
        failures.append(f"expected 1 accepted apply fixture, got {accepted_apply_fixture_count}")
    if rejected_apply_fixture_count != 0:
        failures.append(f"expected 0 rejected apply fixtures, got {rejected_apply_fixture_count}")
    if preview_state_match_count != 1:
        failures.append(f"expected 1 matching preview state, got {preview_state_match_count}")
    if real_mutation_allowed_count != 0:
        failures.append(f"expected 0 real mutation allowances, got {real_mutation_allowed_count}")
    if approval_granted_by_runner is not False:
        failures.append("positive runner unexpectedly grants approval")
    if explicit_operator_apply_approval_present is not False:
        failures.append("explicit operator apply approval unexpectedly present")
    if apply_command_enabled is not False:
        failures.append("positive runner unexpectedly enables apply command")
    if apply_execution_allowed is not False:
        failures.append("positive runner unexpectedly allows apply execution")
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
        failures.append("target request already has approval_scope or decision_note before positive apply command runner")
    if target_task_exists_before:
        failures.append(f"target signed-decision apply command positive runner task already exists: {runner_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if runner_evidence_exists_before:
        failures.append(f"signed-decision apply command positive runner evidence already exists: {runner_evidence_id}")
    if tasks_table_rows_before != 223:
        failures.append(f"expected 223 task rows before signed-decision apply command positive runner, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 131:
        failures.append(f"expected 131 evidence rows before signed-decision apply command positive runner, got {lane_evidence_rows_before}")

    artifacts = build_signed_apply_command_positive_runner_artifacts(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_fixture_validation_path=str(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_APPLY_COMMAND_POSITIVE_FIXTURE_VALIDATION_JSON),
        lane_id=lane_id,
        runner_task_id=runner_task_id,
        runner_evidence_id=runner_evidence_id,
        source_fixture_task_id=source_fixture_task_id,
        source_fixture_evidence_id=source_fixture_evidence_id,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
        runner_content=runner_content,
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
                runner_task_id,
                lane_id,
                "Run CEO decision parser apply-readiness signed-decision apply command positive runner",
                14,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                runner_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": runner_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser apply-readiness signed-decision apply command positive runner",
                "status": "local_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner_complete",
                "summary": runner_summary,
                "next_action": runner_next_action,
                "ownership_note": "Generated by platform_engineering from the local positive apply command fixture; runner is report-only and performs no mutations.",
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
    task_rows_inserted_by_runner = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (runner_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during signed-decision apply command positive runner")
    if task_rows_inserted_by_runner != 1:
        failures.append(f"expected 1 task row inserted by signed-decision apply command positive runner, got {task_rows_inserted_by_runner}")
    if tasks_table_rows_after != 224:
        failures.append(f"expected 224 task rows after signed-decision apply command positive runner, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 132:
        failures.append(f"expected 132 evidence rows after signed-decision apply command positive runner, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("signed-decision apply command positive runner evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during signed-decision apply command positive runner")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner_validation.v1",
        "generated_utc": generated_utc,
        "runner_path": str(json_output_path),
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "source_fixture_task_id": source_fixture_task_id,
        "positive_apply_command_execution_count": positive_apply_command_execution_count,
        "accepted_apply_fixture_count": accepted_apply_fixture_count,
        "rejected_apply_fixture_count": rejected_apply_fixture_count,
        "preview_state_match_count": preview_state_match_count,
        "real_mutation_allowed_count": real_mutation_allowed_count,
        "approval_granted_by_runner": approval_granted_by_runner,
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
        "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
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
                "runner_lane_id": lane_id,
                "runner_task_id": runner_task_id,
                "positive_apply_command_execution_count": positive_apply_command_execution_count,
                "accepted_apply_fixture_count": accepted_apply_fixture_count,
                "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


