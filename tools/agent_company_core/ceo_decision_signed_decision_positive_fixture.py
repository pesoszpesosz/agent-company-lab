from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_GUARD_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_GUARD_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_RUNNER_VALIDATION_JSON,
)
from .ceo_decision_signed_decision_positive_fixture_content import build_signed_decision_positive_fixture_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


"""CEO apply-readiness signed-decision fixture writers."""


def write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_FIXTURE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_FIXTURE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_POSITIVE_FIXTURE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-positive-fixture-20260616"
    fixture_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-positive-fixture-20260616"
    source_guard_runner_task_id = "task-ceo-decision-parser-apply-readiness-signed-decision-guard-runner-20260616"
    source_guard_runner_evidence_id = "ceo-decision-parser-apply-readiness-signed-decision-guard-runner-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-signed-decision-positive-fixture-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_guard_runner_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_guard_runner_task_id,),
    ).fetchone()
    source_guard_runner_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_guard_runner_evidence_id,),
    ).fetchone()
    guard_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_GUARD_RUNNER_VALIDATION_JSON)
    intake_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_DECISION_INTAKE_PACKET_JSON)
    intake_packet = intake_payload.get("decision_intake_packet", {})
    decision_fields_template = dict(intake_packet.get("decision_fields") or {})
    approval_statements = intake_packet.get("required_approval_statements") or []
    target_request_id = decision_fields_template.get("target_request_id")
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
    fixture_content = build_signed_decision_positive_fixture_content(
        decision_fields_template=decision_fields_template,
        approval_statements=approval_statements,
        target_status_before=target_status_before,
        generated_utc=generated_utc,
    )
    local_decision = fixture_content["local_decision"]
    recommended_default = fixture_content["recommended_default"]
    positive_signed_decision_fixture_count = fixture_content["positive_signed_decision_fixture_count"]
    expected_acceptance_count = fixture_content["expected_acceptance_count"]
    decision_field_count = fixture_content["decision_field_count"]
    approval_statement_count = fixture_content["approval_statement_count"]
    signed_decision_preview_only = fixture_content["signed_decision_preview_only"]
    apply_command_enabled = fixture_content["apply_command_enabled"]
    approval_granted_by_fixture = fixture_content["approval_granted_by_fixture"]
    mutation_applied_count = fixture_content["mutation_applied_count"]
    queue_mutation_count = fixture_content["queue_mutation_count"]
    approval_request_count = fixture_content["approval_request_count"]
    target_status_after = fixture_content["target_status_after"]
    positive_signed_decision_fixture = fixture_content["positive_signed_decision_fixture"]
    fixture_summary = fixture_content["summary"]
    fixture_next_action = fixture_content["next_action"]
    runtime_boundary = fixture_content["runtime_boundary"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    fixture_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_guard_runner_task or source_guard_runner_task["status"] != "complete":
        failures.append("source signed-decision guard runner task is missing or incomplete")
    if not source_guard_runner_evidence or source_guard_runner_evidence["status"] != "local_ceo_decision_parser_apply_readiness_signed_decision_guard_runner_complete":
        failures.append("source signed-decision guard runner evidence is missing or not complete")
    if not guard_validation.get("all_checks_passed") or guard_validation.get("failure_count") != 0:
        failures.append("source signed-decision guard runner validation is not clean")
    if positive_signed_decision_fixture_count != 1:
        failures.append(f"expected 1 positive signed-decision fixture, got {positive_signed_decision_fixture_count}")
    if expected_acceptance_count != 1:
        failures.append(f"expected 1 expected acceptance, got {expected_acceptance_count}")
    if decision_field_count != 12:
        failures.append(f"expected 12 decision fields, got {decision_field_count}")
    if approval_statement_count != 5:
        failures.append(f"expected 5 approval statements, got {approval_statement_count}")
    if target_service_request_count != 1:
        failures.append(f"expected 1 target service request, got {target_service_request_count}")
    if signed_decision_preview_only is not True:
        failures.append("positive signed-decision fixture is not preview-only")
    if apply_command_enabled is not False:
        failures.append("positive signed-decision fixture unexpectedly enables apply")
    if approval_granted_by_fixture is not False:
        failures.append("positive signed-decision fixture unexpectedly grants approval")
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
        failures.append("target request already has approval_scope or decision_note before positive signed-decision fixture")
    if target_task_exists_before:
        failures.append(f"target signed-decision positive fixture task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if fixture_evidence_exists_before:
        failures.append(f"signed-decision positive fixture evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 215:
        failures.append(f"expected 215 task rows before signed-decision positive fixture, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 123:
        failures.append(f"expected 123 evidence rows before signed-decision positive fixture, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_positive_fixture.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_guard_runner_task_id": source_guard_runner_task_id,
        "source_guard_runner_evidence_id": source_guard_runner_evidence_id,
        "source_guard_runner_validation_path": str(CEO_DECISION_PARSER_APPLY_READINESS_SIGNED_DECISION_GUARD_RUNNER_VALIDATION_JSON),
        "positive_signed_decision_fixture_count": positive_signed_decision_fixture_count,
        "expected_acceptance_count": expected_acceptance_count,
        "decision_field_count": decision_field_count,
        "approval_statement_count": approval_statement_count,
        "target_service_request_count": target_service_request_count,
        "signed_decision_preview_only": signed_decision_preview_only,
        "apply_command_enabled": apply_command_enabled,
        "approval_granted_by_fixture": approval_granted_by_fixture,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "positive_signed_decision_fixture": positive_signed_decision_fixture,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Positive Fixture",
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
        "## Fixture",
        "",
        "- Fixture: `valid-signed-decision-preview-only`",
        "- Expected accepted: `True`",
        "- Apply command enabled: `False`",
        "- Real mutation expected: `False`",
        "",
        "## Boundary",
        "",
        "This fixture is local test data only. It grants no approval, enables no apply command, updates no service request, emits no approval request, starts no worker, calls no API, opens no browser, and performs no account, wallet, payment, public, security-testing, external, or real-money action.",
        "",
        "## Next Action",
        "",
        fixture_next_action,
        "",
    ]
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
                "Create CEO decision parser apply-readiness signed-decision positive fixture",
                22,
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
                "title": "CEO decision parser apply-readiness signed-decision positive fixture",
                "status": "local_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture_complete",
                "summary": fixture_summary,
                "next_action": fixture_next_action,
                "ownership_note": "Generated by platform_engineering from the signed-decision guard runner; fixture is local validation data only.",
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
        failures.append("target service request changed during signed-decision positive fixture")
    if task_rows_inserted_by_fixture != 1:
        failures.append(f"expected 1 task row inserted by signed-decision positive fixture, got {task_rows_inserted_by_fixture}")
    if tasks_table_rows_after != 216:
        failures.append(f"expected 216 task rows after signed-decision positive fixture, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 124:
        failures.append(f"expected 124 evidence rows after signed-decision positive fixture, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("signed-decision positive fixture evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during signed-decision positive fixture")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_positive_fixture_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_guard_runner_task_id": source_guard_runner_task_id,
        "positive_signed_decision_fixture_count": positive_signed_decision_fixture_count,
        "expected_acceptance_count": expected_acceptance_count,
        "decision_field_count": decision_field_count,
        "approval_statement_count": approval_statement_count,
        "target_service_request_count": target_service_request_count,
        "signed_decision_preview_only": signed_decision_preview_only,
        "apply_command_enabled": apply_command_enabled,
        "approval_granted_by_fixture": approval_granted_by_fixture,
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
                "positive_signed_decision_fixture_count": positive_signed_decision_fixture_count,
                "task_rows_inserted_by_fixture": task_rows_inserted_by_fixture,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

