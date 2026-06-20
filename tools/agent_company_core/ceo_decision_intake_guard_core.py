from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .ceo_decision_intake_guard_content import build_ceo_decision_intake_guard_content
from .constants import (
    CEO_DECISION_INTAKE_GUARD_JSON,
    CEO_DECISION_INTAKE_GUARD_REPORT,
    CEO_DECISION_INTAKE_GUARD_VALIDATION_JSON,
    CEO_DECISION_PACKET_DRAFTS_JSON,
    CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_intake_guard(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_INTAKE_GUARD_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_INTAKE_GUARD_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_INTAKE_GUARD_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    guard_task_id = "task-ceo-decision-intake-guard-20260616"
    guard_evidence_id = "ceo-decision-intake-guard-20260616"
    source_drafts_task_id = "task-ceo-decision-packet-drafts-20260616"
    source_drafts_evidence_id = "ceo-decision-packet-drafts-20260616"
    duplicate_key = "ceo-decision-intake-guard-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_drafts_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_drafts_evidence_id,),
    ).fetchone()
    drafts_validation = load_json(CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON)
    drafts_payload = load_json(CEO_DECISION_PACKET_DRAFTS_JSON)
    packet_drafts = drafts_payload.get("packet_drafts", [])
    source_packet_draft_count = int(drafts_payload.get("packet_draft_count", 0))
    source_decision_option_count = int(drafts_payload.get("decision_option_count", 0))

    guard_content = build_ceo_decision_intake_guard_content(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        guard_task_id=guard_task_id,
        guard_evidence_id=guard_evidence_id,
        source_drafts_task_id=source_drafts_task_id,
        source_drafts_evidence_id=source_drafts_evidence_id,
        source_drafts_validation_path=CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON,
        packet_drafts=packet_drafts,
        source_packet_draft_count=source_packet_draft_count,
        source_decision_option_count=source_decision_option_count,
    )
    local_decision = guard_content["local_decision"]
    recommended_default = guard_content["recommended_default"]
    required_field_count = guard_content["required_field_count"]
    invalid_decision_rule_count = guard_content["invalid_decision_rule_count"]
    known_packet_ids = guard_content["known_packet_ids"]
    known_option_ids = guard_content["known_option_ids"]
    accepted_decision_count = guard_content["accepted_decision_count"]
    approval_request_count = guard_content["approval_request_count"]
    runnable_without_approval_count = guard_content["runnable_without_approval_count"]
    guard_summary = guard_content["summary"]
    guard_next_action = guard_content["next_action"]
    runtime_boundary = guard_content["runtime_boundary"]
    payload = guard_content["payload"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (guard_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    guard_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (guard_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO decision packet drafts task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_decision_packet_drafts_complete":
        failures.append("source CEO decision packet drafts evidence is missing or not complete")
    if not drafts_validation.get("all_checks_passed") or drafts_validation.get("failure_count") != 0:
        failures.append("source CEO decision packet drafts validation is not clean")
    if source_packet_draft_count != 3:
        failures.append(f"expected 3 source packet drafts, got {source_packet_draft_count}")
    if source_decision_option_count != 9:
        failures.append(f"expected 9 source decision options, got {source_decision_option_count}")
    if required_field_count != 8:
        failures.append(f"expected 8 required fields, got {required_field_count}")
    if invalid_decision_rule_count != 6:
        failures.append(f"expected 6 invalid decision rules, got {invalid_decision_rule_count}")
    if accepted_decision_count != 0:
        failures.append(f"expected 0 accepted decisions, got {accepted_decision_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if len(known_packet_ids) != 3:
        failures.append(f"expected 3 known packet ids, got {len(known_packet_ids)}")
    if len(known_option_ids) != 3:
        failures.append(f"expected 3 distinct known option ids, got {len(known_option_ids)}")
    if target_task_exists_before:
        failures.append(f"target CEO decision intake guard task already exists: {guard_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if guard_evidence_exists_before:
        failures.append(f"CEO decision intake guard evidence already exists: {guard_evidence_id}")
    if tasks_table_rows_before != 192:
        failures.append(f"expected 192 task rows before CEO decision intake guard, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 100:
        failures.append(f"expected 100 evidence rows before CEO decision intake guard, got {lane_evidence_rows_before}")

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(guard_content["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                guard_task_id,
                lane_id,
                "Create CEO decision intake guard",
                45,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                guard_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": guard_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision intake guard",
                "status": "local_ceo_decision_intake_guard_complete",
                "summary": guard_summary,
                "next_action": guard_next_action,
                "ownership_note": "Generated by platform_engineering from CEO decision packet drafts; guard is non-authoritative and accepts no decision.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_guard = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (guard_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (guard_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (guard_task_id,)) else 0
    if task_rows_inserted_by_guard != 1:
        failures.append(f"expected 1 task row inserted by CEO decision intake guard, got {task_rows_inserted_by_guard}")
    if tasks_table_rows_after != 193:
        failures.append(f"expected 193 task rows after CEO decision intake guard, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 101:
        failures.append(f"expected 101 evidence rows after CEO decision intake guard, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision intake guard evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision intake guard")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_guard": task_rows_inserted_by_guard,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_intake_guard_validation.v1",
        "generated_utc": generated_utc,
        "guard_path": str(json_output_path),
        "guard_lane_id": lane_id,
        "guard_task_id": guard_task_id,
        "source_drafts_task_id": source_drafts_task_id,
        "source_drafts_evidence_id": source_drafts_evidence_id,
        "source_packet_draft_count": source_packet_draft_count,
        "source_decision_option_count": source_decision_option_count,
        "required_field_count": required_field_count,
        "invalid_decision_rule_count": invalid_decision_rule_count,
        "accepted_decision_count": accepted_decision_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_guard": task_rows_inserted_by_guard,
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
                "guard_lane_id": lane_id,
                "guard_task_id": guard_task_id,
                "required_field_count": required_field_count,
                "task_rows_inserted_by_guard": task_rows_inserted_by_guard,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )