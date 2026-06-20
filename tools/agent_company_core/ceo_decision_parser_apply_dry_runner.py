from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .ceo_decision_parser_apply_dry_runner_content import build_ceo_decision_parser_apply_dry_runner_content
from .constants import (
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_REPORT,
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_JSON,
    CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


"""CEO decision parser apply runner writers."""


def write_ceo_decision_parser_apply_dry_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_DRY_RUNNER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_DRY_RUNNER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_DRY_RUNNER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    runner_task_id = "task-ceo-decision-parser-apply-dry-runner-20260616"
    runner_evidence_id = "ceo-decision-parser-apply-dry-runner-20260616"
    source_positive_fixture_task_id = "task-ceo-decision-parser-apply-positive-fixture-20260616"
    source_positive_fixture_evidence_id = "ceo-decision-parser-apply-positive-fixture-20260616"
    duplicate_key = "ceo-decision-parser-apply-dry-runner-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_positive_fixture_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_positive_fixture_task_id,),
    ).fetchone()
    source_positive_fixture_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_positive_fixture_evidence_id,),
    ).fetchone()
    fixture_validation = load_json(CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_VALIDATION_JSON)
    fixture_payload = load_json(CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_JSON)
    positive_fixture = fixture_payload.get("positive_apply_fixture", {})
    submitted_apply = positive_fixture.get("submitted_apply", {})
    expected_preview = fixture_payload.get("preview_update", {})
    target_ids = submitted_apply.get("target_service_request_ids") or []
    target_request_id = target_ids[0] if target_ids else None
    target_request_before = (
        conn.execute(
            "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    target_status_before = target_request_before["status"] if target_request_before else None
    approval_scope_before = target_request_before["approval_scope"] if target_request_before else None
    decision_note_before = target_request_before["decision_note"] if target_request_before else None

    runner_content = build_ceo_decision_parser_apply_dry_runner_content(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        runner_task_id=runner_task_id,
        runner_evidence_id=runner_evidence_id,
        source_positive_fixture_task_id=source_positive_fixture_task_id,
        source_positive_fixture_evidence_id=source_positive_fixture_evidence_id,
        source_positive_fixture_validation_path=CEO_DECISION_PARSER_APPLY_POSITIVE_FIXTURE_VALIDATION_JSON,
        positive_fixture=positive_fixture,
        expected_preview=expected_preview,
        target_request_id=target_request_id,
        target_status_before=target_status_before,
    )
    positive_apply_fixture_count = int(fixture_payload.get("positive_apply_fixture_count", 0))
    apply_dry_run_execution_count = runner_content["apply_dry_run_execution_count"]
    accepted_apply_preview_count = runner_content["accepted_apply_preview_count"]
    expected_preview_match_count = runner_content["expected_preview_match_count"]
    preview_update_count = runner_content["preview_update_count"]
    mutation_applied_count = runner_content["mutation_applied_count"]
    queue_mutation_count = runner_content["queue_mutation_count"]
    approval_request_count = runner_content["approval_request_count"]
    target_status_after = runner_content["target_status_after"]
    dry_run_result = runner_content["dry_run_result"]
    local_decision = runner_content["local_decision"]
    recommended_default = runner_content["recommended_default"]
    runner_summary = runner_content["summary"]
    runner_next_action = runner_content["next_action"]
    runtime_boundary = runner_content["runtime_boundary"]
    payload = runner_content["payload"]
    payload["positive_apply_fixture_count"] = positive_apply_fixture_count

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    runner_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_positive_fixture_task or source_positive_fixture_task["status"] != "complete":
        failures.append("source apply positive fixture task is missing or incomplete")
    if not source_positive_fixture_evidence or source_positive_fixture_evidence["status"] != "local_ceo_decision_parser_apply_positive_fixture_complete":
        failures.append("source apply positive fixture evidence is missing or not complete")
    if not fixture_validation.get("all_checks_passed") or fixture_validation.get("failure_count") != 0:
        failures.append("source apply positive fixture validation is not clean")
    if positive_apply_fixture_count != 1:
        failures.append(f"expected 1 positive apply fixture, got {positive_apply_fixture_count}")
    if apply_dry_run_execution_count != 1:
        failures.append(f"expected 1 apply dry-run execution, got {apply_dry_run_execution_count}")
    if accepted_apply_preview_count != 1:
        failures.append(f"expected 1 accepted apply preview, got {accepted_apply_preview_count}")
    if expected_preview_match_count != 1:
        failures.append(f"expected 1 matching preview, got {expected_preview_match_count}")
    if preview_update_count != 1:
        failures.append(f"expected 1 preview update, got {preview_update_count}")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_status_before != "needs_review":
        failures.append(f"expected target status before needs_review, got {target_status_before}")
    if approval_scope_before is not None:
        failures.append("expected target approval_scope to remain unset before dry-run runner")
    if decision_note_before is not None:
        failures.append("expected target decision_note to remain unset before dry-run runner")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply dry-runner task already exists: {runner_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if runner_evidence_exists_before:
        failures.append(f"CEO decision parser apply dry-runner evidence already exists: {runner_evidence_id}")
    if tasks_table_rows_before != 204:
        failures.append(f"expected 204 task rows before CEO decision parser apply dry-runner, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 112:
        failures.append(f"expected 112 evidence rows before CEO decision parser apply dry-runner, got {lane_evidence_rows_before}")

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(runner_content["markdown"], encoding="utf-8")

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
                "Run CEO decision parser apply dry-run preview",
                33,
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
                "title": "CEO decision parser apply dry-runner",
                "status": "local_ceo_decision_parser_apply_dry_runner_complete",
                "summary": runner_summary,
                "next_action": runner_next_action,
                "ownership_note": "Generated by platform_engineering from the positive apply fixture; runner is report-only and performs no mutations.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    target_request_after = (
        conn.execute(
            "SELECT status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at FROM service_requests WHERE request_id = ?",
            (target_request_id,),
        ).fetchone()
        if target_request_id
        else None
    )
    task_rows_inserted_by_runner = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (runner_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (runner_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (runner_task_id,)) else 0
    if target_request_after and (
        target_request_after["status"] != target_status_before
        or target_request_after["approval_scope"] != approval_scope_before
        or target_request_after["decision_note"] != decision_note_before
        or target_request_after["assigned_agent_id"] is not None
        or target_request_after["started_at"] is not None
        or target_request_after["completed_at"] is not None
    ):
        failures.append("target service request changed during apply dry-runner")
    if task_rows_inserted_by_runner != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser apply dry-runner, got {task_rows_inserted_by_runner}")
    if tasks_table_rows_after != 205:
        failures.append(f"expected 205 task rows after CEO decision parser apply dry-runner, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 113:
        failures.append(f"expected 113 evidence rows after CEO decision parser apply dry-runner, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply dry-runner evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply dry-runner")
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
        "schema_version": "agent_company.ceo_decision_parser_apply_dry_runner_validation.v1",
        "generated_utc": generated_utc,
        "runner_path": str(json_output_path),
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "source_positive_fixture_task_id": source_positive_fixture_task_id,
        "positive_apply_fixture_count": positive_apply_fixture_count,
        "apply_dry_run_execution_count": apply_dry_run_execution_count,
        "accepted_apply_preview_count": accepted_apply_preview_count,
        "expected_preview_match_count": expected_preview_match_count,
        "preview_update_count": preview_update_count,
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
                "apply_dry_run_execution_count": apply_dry_run_execution_count,
                "accepted_apply_preview_count": accepted_apply_preview_count,
                "preview_update_count": preview_update_count,
                "task_rows_inserted_by_runner": task_rows_inserted_by_runner,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )