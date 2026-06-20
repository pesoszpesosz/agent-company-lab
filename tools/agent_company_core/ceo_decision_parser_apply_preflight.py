from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .constants import (
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_GUARD_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_GUARD_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_PARSER_APPLY_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_PARSER_APPLY_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_MUTATION_PREFLIGHT_JSON,
    CEO_DECISION_PARSER_MUTATION_PREFLIGHT_REPORT,
    CEO_DECISION_PARSER_MUTATION_PREFLIGHT_VALIDATION_JSON,
    CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_JSON,
    CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_VALIDATION_JSON,
)
from .ceo_decision_parser_apply_preflight_content import build_ceo_decision_parser_mutation_preflight_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


"""CEO decision parser mutation-preflight writer."""


def write_ceo_decision_parser_mutation_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_MUTATION_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_MUTATION_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_MUTATION_PREFLIGHT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    preflight_task_id = "task-ceo-decision-parser-mutation-preflight-20260616"
    preflight_evidence_id = "ceo-decision-parser-mutation-preflight-20260616"
    source_runner_task_id = "task-ceo-decision-parser-report-only-runner-20260616"
    source_runner_evidence_id = "ceo-decision-parser-report-only-runner-20260616"
    duplicate_key = "ceo-decision-parser-mutation-preflight-20260616"
    local_decision = "ceo_decision_parser_mutation_preflight_ready_no_apply"
    recommended_default = "require_explicit_operator_mutation_approval_before_apply"
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
    source_runner_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_runner_task_id,)).fetchone()
    source_runner_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_runner_evidence_id,),
    ).fetchone()
    runner_validation = load_json(CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_VALIDATION_JSON)
    runner_payload = load_json(CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_JSON)
    positive_payload = load_json(CEO_DECISION_PARSER_POSITIVE_FIXTURE_JSON)
    positive_fixture = positive_payload.get("positive_fixture", {})
    submitted_intake = positive_fixture.get("submitted_intake", {})
    content = build_ceo_decision_parser_mutation_preflight_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        lane_id=lane_id,
        preflight_task_id=preflight_task_id,
        preflight_evidence_id=preflight_evidence_id,
        source_runner_task_id=source_runner_task_id,
        source_runner_evidence_id=source_runner_evidence_id,
        source_runner_validation_path=str(CEO_DECISION_PARSER_REPORT_ONLY_RUNNER_VALIDATION_JSON),
        runner_payload=runner_payload,
        positive_fixture=positive_fixture,
    )
    candidate_preview_count = content["candidate_preview_count"]
    required_approval_fields = content["required_approval_fields"]
    required_approval_field_count = content["required_approval_field_count"]
    required_blocker_count = content["required_blocker_count"]
    forbidden_action_count = content["forbidden_action_count"]
    missing_approval_fields = [field for field in required_approval_fields if submitted_intake.get(field) in (None, "", [])]
    mutation_applied_count = content["mutation_applied_count"]
    queue_mutation_count = content["queue_mutation_count"]
    approval_request_count = content["approval_request_count"]
    preflight_packet = content["preflight_packet"]
    local_decision = content["local_decision"]
    recommended_default = content["recommended_default"]
    preflight_summary = content["summary"]
    preflight_next_action = content["next_action"]
    runtime_boundary = content["runtime_boundary"]
    payload = content["payload"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    preflight_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_runner_task or source_runner_task["status"] != "complete":
        failures.append("source report-only runner task is missing or incomplete")
    if not source_runner_evidence or source_runner_evidence["status"] != "local_ceo_decision_parser_report_only_runner_complete":
        failures.append("source report-only runner evidence is missing or not complete")
    if not runner_validation.get("all_checks_passed") or runner_validation.get("failure_count") != 0:
        failures.append("source report-only runner validation is not clean")
    if candidate_preview_count != 1:
        failures.append(f"expected 1 accepted candidate preview, got {candidate_preview_count}")
    if required_approval_field_count != 8:
        failures.append(f"expected 8 required approval fields, got {required_approval_field_count}")
    if missing_approval_fields:
        failures.append(f"missing approval fields in positive fixture: {', '.join(missing_approval_fields)}")
    if required_blocker_count != 2:
        failures.append(f"expected 2 required blocker ids, got {required_blocker_count}")
    if forbidden_action_count != 10:
        failures.append(f"expected 10 forbidden actions, got {forbidden_action_count}")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser mutation preflight task already exists: {preflight_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if preflight_evidence_exists_before:
        failures.append(f"CEO decision parser mutation preflight evidence already exists: {preflight_evidence_id}")
    if tasks_table_rows_before != 200:
        failures.append(f"expected 200 task rows before CEO decision parser mutation preflight, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 108:
        failures.append(f"expected 108 evidence rows before CEO decision parser mutation preflight, got {lane_evidence_rows_before}")

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(content["markdown"], encoding="utf-8")
    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                preflight_task_id,
                lane_id,
                "Create CEO decision parser mutation preflight",
                37,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                preflight_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": preflight_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser mutation preflight",
                "status": "local_ceo_decision_parser_mutation_preflight_complete",
                "summary": preflight_summary,
                "next_action": preflight_next_action,
                "ownership_note": "Generated by platform_engineering from the report-only parser runner; preflight is a local approval checklist only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_preflight = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (preflight_task_id,)) else 0
    if task_rows_inserted_by_preflight != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser mutation preflight, got {task_rows_inserted_by_preflight}")
    if tasks_table_rows_after != 201:
        failures.append(f"expected 201 task rows after CEO decision parser mutation preflight, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 109:
        failures.append(f"expected 109 evidence rows after CEO decision parser mutation preflight, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser mutation preflight evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser mutation preflight")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_mutation_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": str(json_output_path),
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "source_runner_task_id": source_runner_task_id,
        "candidate_preview_count": candidate_preview_count,
        "required_approval_field_count": required_approval_field_count,
        "required_blocker_count": required_blocker_count,
        "forbidden_action_count": forbidden_action_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
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
                "preflight_lane_id": lane_id,
                "preflight_task_id": preflight_task_id,
                "candidate_preview_count": candidate_preview_count,
                "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


__all__ = [
    "write_ceo_decision_parser_mutation_preflight",
]

