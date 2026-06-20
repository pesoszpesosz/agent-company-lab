from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Negative fixtures, guard runner, positive fixture, and positive runner writers for apply readiness."""

from .constants import (
    CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_POSITIVE_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_VALIDATION_JSON,
)
from .ceo_decision_apply_readiness_negative_fixture_content import build_ceo_apply_readiness_negative_fixture_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_parser_apply_readiness_negative_fixtures(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_NEGATIVE_FIXTURES_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-ceo-decision-parser-apply-readiness-negative-fixtures-20260616"
    fixture_evidence_id = "ceo-decision-parser-apply-readiness-negative-fixtures-20260616"
    source_readiness_task_id = "task-ceo-decision-parser-apply-readiness-20260616"
    source_readiness_evidence_id = "ceo-decision-parser-apply-readiness-20260616"
    duplicate_key = "ceo-decision-parser-apply-readiness-negative-fixtures-20260616"
    local_decision = "ceo_decision_parser_apply_readiness_negative_fixtures_ready"
    recommended_default = "reject_apply_readiness_when_packet_or_target_state_drifts"
    accepted_readiness_count = 0
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_readiness_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_readiness_task_id,)).fetchone()
    source_readiness_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_readiness_evidence_id,),
    ).fetchone()
    readiness_validation = load_json(CEO_DECISION_PARSER_APPLY_READINESS_VALIDATION_JSON)
    readiness_payload = load_json(CEO_DECISION_PARSER_APPLY_READINESS_JSON)
    readiness_packet = readiness_payload.get("readiness_packet", {})
    fixture_content = build_ceo_apply_readiness_negative_fixture_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_readiness_validation_path=str(CEO_DECISION_PARSER_APPLY_READINESS_VALIDATION_JSON),
        lane_id=lane_id,
        fixture_task_id=fixture_task_id,
        fixture_evidence_id=fixture_evidence_id,
        source_readiness_task_id=source_readiness_task_id,
        source_readiness_evidence_id=source_readiness_evidence_id,
        readiness_packet=readiness_packet,
    )
    required_readiness_fields = fixture_content["required_readiness_fields"]
    required_readiness_field_count = fixture_content["required_readiness_field_count"]
    negative_readiness_fixtures = fixture_content["negative_readiness_fixtures"]
    negative_readiness_fixture_count = fixture_content["negative_readiness_fixture_count"]
    expected_rejection_count = fixture_content["expected_rejection_count"]
    accepted_readiness_count = fixture_content["accepted_readiness_count"]
    mutation_applied_count = fixture_content["mutation_applied_count"]
    queue_mutation_count = fixture_content["queue_mutation_count"]
    approval_request_count = fixture_content["approval_request_count"]
    local_decision = fixture_content["local_decision"]
    recommended_default = fixture_content["recommended_default"]
    fixture_summary = fixture_content["summary"]
    fixture_next_action = fixture_content["next_action"]
    runtime_boundary = fixture_content["runtime_boundary"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    fixture_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_readiness_task or source_readiness_task["status"] != "complete":
        failures.append("source apply-readiness task is missing or incomplete")
    if not source_readiness_evidence or source_readiness_evidence["status"] != "local_ceo_decision_parser_apply_readiness_complete":
        failures.append("source apply-readiness evidence is missing or not complete")
    if not readiness_validation.get("all_checks_passed") or readiness_validation.get("failure_count") != 0:
        failures.append("source apply-readiness validation is not clean")
    if readiness_payload.get("readiness_packet_count") != 1:
        failures.append(f"expected 1 source readiness packet, got {readiness_payload.get('readiness_packet_count')}")
    if negative_readiness_fixture_count != 6:
        failures.append(f"expected 6 negative readiness fixtures, got {negative_readiness_fixture_count}")
    if expected_rejection_count != 6:
        failures.append(f"expected 6 expected rejections, got {expected_rejection_count}")
    if accepted_readiness_count != 0:
        failures.append(f"expected 0 accepted readiness fixtures, got {accepted_readiness_count}")
    if required_readiness_field_count != 6:
        failures.append(f"expected 6 required readiness fields, got {required_readiness_field_count}")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply-readiness negative fixtures task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if fixture_evidence_exists_before:
        failures.append(f"CEO decision parser apply-readiness negative fixtures evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 206:
        failures.append(f"expected 206 task rows before CEO decision parser apply-readiness negative fixtures, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 114:
        failures.append(f"expected 114 evidence rows before CEO decision parser apply-readiness negative fixtures, got {lane_evidence_rows_before}")

    payload = fixture_content["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(fixture_content["markdown"], encoding="utf-8")
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
                "Create CEO decision parser apply-readiness negative fixtures",
                31,
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
                "title": "CEO decision parser apply-readiness negative fixtures",
                "status": "local_ceo_decision_parser_apply_readiness_negative_fixtures_complete",
                "summary": fixture_summary,
                "next_action": fixture_next_action,
                "ownership_note": "Generated by platform_engineering from the apply-readiness packet; fixtures are local validation data only.",
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
        failures.append(f"expected 1 task row inserted by CEO decision parser apply-readiness negative fixtures, got {task_rows_inserted_by_fixtures}")
    if tasks_table_rows_after != 207:
        failures.append(f"expected 207 task rows after CEO decision parser apply-readiness negative fixtures, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 115:
        failures.append(f"expected 115 evidence rows after CEO decision parser apply-readiness negative fixtures, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply-readiness negative fixtures evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply-readiness negative fixtures")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_negative_fixtures_validation.v1",
        "generated_utc": generated_utc,
        "fixtures_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_readiness_task_id": source_readiness_task_id,
        "negative_readiness_fixture_count": negative_readiness_fixture_count,
        "expected_rejection_count": expected_rejection_count,
        "accepted_readiness_count": accepted_readiness_count,
        "required_readiness_field_count": required_readiness_field_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
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
                "negative_readiness_fixture_count": negative_readiness_fixture_count,
                "task_rows_inserted_by_fixtures": task_rows_inserted_by_fixtures,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )



