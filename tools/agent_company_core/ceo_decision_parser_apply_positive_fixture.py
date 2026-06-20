from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .ceo_decision_parser_apply_positive_fixture_content import (
    build_ceo_decision_parser_apply_positive_fixture_content,
)
from .constants import (
    CEO_DECISION_PARSER_APPLY_GUARD_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_REPORT,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_VALIDATION_JSON,
    CEO_DECISION_PARSER_MUTATION_PREFLIGHT_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


"""CEO decision parser apply fixture writers."""


def write_ceo_decision_parser_apply_positive_fixture(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    fixture_task_id = "task-ceo-decision-parser-apply-positive-fixture-20260616"
    fixture_evidence_id = "ceo-decision-parser-apply-positive-fixture-20260616"
    source_guard_runner_task_id = "task-ceo-decision-parser-apply-guard-runner-20260616"
    source_guard_runner_evidence_id = "ceo-decision-parser-apply-guard-runner-20260616"
    target_request_id = "req-wave4-digital-products-browser-readonly-20260614"
    duplicate_key = "ceo-decision-parser-apply-positive-fixture-20260616"
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
    guard_validation = load_json(CEO_DECISION_PARSER_APPLY_GUARD_RUNNER_VALIDATION_JSON)
    preflight_payload = load_json(CEO_DECISION_PARSER_MUTATION_PREFLIGHT_JSON)
    preflight_packet = preflight_payload.get("preflight_packet", {})
    target_request = conn.execute("SELECT * FROM service_requests WHERE request_id = ?", (target_request_id,)).fetchone()
    target_service_request_count = 1 if target_request else 0
    target_status_before = target_request["status"] if target_request else None
    target_approval_scope_before = target_request["approval_scope"] if target_request else None
    target_decision_note_before = target_request["decision_note"] if target_request else None

    fixture_content = build_ceo_decision_parser_apply_positive_fixture_content(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        fixture_task_id=fixture_task_id,
        fixture_evidence_id=fixture_evidence_id,
        source_guard_runner_task_id=source_guard_runner_task_id,
        source_guard_runner_evidence_id=source_guard_runner_evidence_id,
        source_guard_runner_validation_path=CEO_DECISION_PARSER_APPLY_GUARD_RUNNER_VALIDATION_JSON,
        preflight_packet=preflight_packet,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
        target_approval_scope_before=target_approval_scope_before,
        target_decision_note_before=target_decision_note_before,
    )
    positive_apply_fixture_count = fixture_content["positive_apply_fixture_count"]
    expected_preview_update_count = fixture_content["expected_preview_update_count"]
    mutation_applied_count = fixture_content["mutation_applied_count"]
    queue_mutation_count = fixture_content["queue_mutation_count"]
    approval_request_count = fixture_content["approval_request_count"]
    target_status_after = fixture_content["target_status_after"]
    local_decision = fixture_content["local_decision"]
    recommended_default = fixture_content["recommended_default"]
    fixture_summary = fixture_content["summary"]
    fixture_next_action = fixture_content["next_action"]
    runtime_boundary = fixture_content["runtime_boundary"]
    payload = fixture_content["payload"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    fixture_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_guard_runner_task or source_guard_runner_task["status"] != "complete":
        failures.append("source apply guard runner task is missing or incomplete")
    if not source_guard_runner_evidence or source_guard_runner_evidence["status"] != "local_ceo_decision_parser_apply_guard_runner_complete":
        failures.append("source apply guard runner evidence is missing or not complete")
    if not guard_validation.get("all_checks_passed") or guard_validation.get("failure_count") != 0:
        failures.append("source apply guard runner validation is not clean")
    if positive_apply_fixture_count != 1:
        failures.append(f"expected 1 positive apply fixture, got {positive_apply_fixture_count}")
    if target_service_request_count != 1:
        failures.append(f"expected 1 target service request, got {target_service_request_count}")
    if expected_preview_update_count != 1:
        failures.append(f"expected 1 preview update, got {expected_preview_update_count}")
    if target_status_before != "needs_review":
        failures.append(f"expected target status before needs_review, got {target_status_before}")
    if target_status_after != "needs_review":
        failures.append(f"expected target status after needs_review, got {target_status_after}")
    if target_approval_scope_before is not None:
        failures.append("expected target approval_scope to remain unset before dry-run preview")
    if target_decision_note_before is not None:
        failures.append("expected target decision_note to remain unset before dry-run preview")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply positive fixture task already exists: {fixture_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if fixture_evidence_exists_before:
        failures.append(f"CEO decision parser apply positive fixture evidence already exists: {fixture_evidence_id}")
    if tasks_table_rows_before != 203:
        failures.append(f"expected 203 task rows before CEO decision parser apply positive fixture, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 111:
        failures.append(f"expected 111 evidence rows before CEO decision parser apply positive fixture, got {lane_evidence_rows_before}")

    payload["target_service_request_count"] = target_service_request_count
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
                "Create CEO decision parser apply positive dry-run fixture",
                34,
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
                "title": "CEO decision parser apply positive fixture",
                "status": "local_ceo_decision_parser_apply_positive_fixture_complete",
                "summary": fixture_summary,
                "next_action": fixture_next_action,
                "ownership_note": "Generated by platform_engineering from the apply guard runner; fixture is local dry-run data only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    target_request_after = conn.execute("SELECT status, approval_scope, decision_note FROM service_requests WHERE request_id = ?", (target_request_id,)).fetchone()
    task_rows_inserted_by_fixture = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (fixture_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (fixture_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (fixture_task_id,)) else 0
    if target_request_after and (
        target_request_after["status"] != target_status_before
        or target_request_after["approval_scope"] != target_approval_scope_before
        or target_request_after["decision_note"] != target_decision_note_before
    ):
        failures.append("target service request changed during positive apply dry-run fixture")
    if task_rows_inserted_by_fixture != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser apply positive fixture, got {task_rows_inserted_by_fixture}")
    if tasks_table_rows_after != 204:
        failures.append(f"expected 204 task rows after CEO decision parser apply positive fixture, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 112:
        failures.append(f"expected 112 evidence rows after CEO decision parser apply positive fixture, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply positive fixture evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply positive fixture")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_positive_fixture_validation.v1",
        "generated_utc": generated_utc,
        "fixture_path": str(json_output_path),
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "source_guard_runner_task_id": source_guard_runner_task_id,
        "positive_apply_fixture_count": positive_apply_fixture_count,
        "target_service_request_count": target_service_request_count,
        "expected_preview_update_count": expected_preview_update_count,
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
                "positive_apply_fixture_count": positive_apply_fixture_count,
                "expected_preview_update_count": expected_preview_update_count,
                "task_rows_inserted_by_fixture": task_rows_inserted_by_fixture,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )