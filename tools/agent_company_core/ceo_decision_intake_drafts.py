from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .ceo_decision_intake_drafts_content import build_ceo_decision_packet_drafts_content
from .constants import (
    CEO_BLOCKER_TRIAGE_JSON,
    CEO_BLOCKER_TRIAGE_VALIDATION_JSON,
    CEO_DECISION_PACKET_DRAFTS_JSON,
    CEO_DECISION_PACKET_DRAFTS_REPORT,
    CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_decision_packet_drafts(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PACKET_DRAFTS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PACKET_DRAFTS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    draft_task_id = "task-ceo-decision-packet-drafts-20260616"
    draft_evidence_id = "ceo-decision-packet-drafts-20260616"
    source_triage_task_id = "task-ceo-blocker-triage-20260616"
    source_triage_evidence_id = "ceo-blocker-triage-20260616"
    duplicate_key = "ceo-decision-packet-drafts-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_triage_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_triage_evidence_id,),
    ).fetchone()
    triage_validation = load_json(CEO_BLOCKER_TRIAGE_VALIDATION_JSON)
    triage_payload = load_json(CEO_BLOCKER_TRIAGE_JSON)
    triage_batches = triage_payload.get("triage_batches", [])
    source_active_blocker_count = int(triage_payload.get("source_active_blocker_count", 0))
    source_triage_batch_count = int(triage_payload.get("triage_batch_count", 0))
    source_high_leverage_batch_count = int(triage_payload.get("high_leverage_batch_count", 0))

    draft_content = build_ceo_decision_packet_drafts_content(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        source_triage_validation_path=CEO_BLOCKER_TRIAGE_VALIDATION_JSON,
        lane_id=lane_id,
        draft_task_id=draft_task_id,
        draft_evidence_id=draft_evidence_id,
        source_triage_task_id=source_triage_task_id,
        source_triage_evidence_id=source_triage_evidence_id,
        triage_batches=triage_batches,
        source_active_blocker_count=source_active_blocker_count,
        source_triage_batch_count=source_triage_batch_count,
        source_high_leverage_batch_count=source_high_leverage_batch_count,
    )
    local_decision = draft_content["local_decision"]
    recommended_default = draft_content["recommended_default"]
    approval_request_count = draft_content["approval_request_count"]
    runnable_without_approval_count = draft_content["runnable_without_approval_count"]
    packet_draft_count = draft_content["packet_draft_count"]
    decision_option_count = draft_content["decision_option_count"]
    draft_summary = draft_content["summary"]
    draft_next_action = draft_content["next_action"]
    runtime_boundary = draft_content["runtime_boundary"]
    payload = draft_content["payload"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (draft_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    draft_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (draft_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO blocker triage task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_blocker_triage_complete":
        failures.append("source CEO blocker triage evidence is missing or not complete")
    if not triage_validation.get("all_checks_passed") or triage_validation.get("failure_count") != 0:
        failures.append("source CEO blocker triage validation is not clean")
    if source_active_blocker_count != 15:
        failures.append(f"expected 15 source active blockers, got {source_active_blocker_count}")
    if source_triage_batch_count != 5:
        failures.append(f"expected 5 source triage batches, got {source_triage_batch_count}")
    if source_high_leverage_batch_count != 3:
        failures.append(f"expected 3 source high-leverage batches, got {source_high_leverage_batch_count}")
    if packet_draft_count != 3:
        failures.append(f"expected 3 packet drafts, got {packet_draft_count}")
    if decision_option_count != 9:
        failures.append(f"expected 9 decision options, got {decision_option_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval items, got {runnable_without_approval_count}")
    if target_task_exists_before:
        failures.append(f"target CEO decision packet drafts task already exists: {draft_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if draft_evidence_exists_before:
        failures.append(f"CEO decision packet drafts evidence already exists: {draft_evidence_id}")
    if tasks_table_rows_before != 191:
        failures.append(f"expected 191 task rows before CEO decision packet drafts, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 99:
        failures.append(f"expected 99 evidence rows before CEO decision packet drafts, got {lane_evidence_rows_before}")

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(draft_content["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                draft_task_id,
                lane_id,
                "Draft CEO decision packets",
                46,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                draft_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": draft_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision packet drafts",
                "status": "local_ceo_decision_packet_drafts_complete",
                "summary": draft_summary,
                "next_action": draft_next_action,
                "ownership_note": "Generated by platform_engineering from CEO blocker triage; drafts are non-authoritative and cannot approve action.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_drafts = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (draft_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (draft_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (draft_task_id,)) else 0
    if task_rows_inserted_by_drafts != 1:
        failures.append(f"expected 1 task row inserted by CEO decision packet drafts, got {task_rows_inserted_by_drafts}")
    if tasks_table_rows_after != 192:
        failures.append(f"expected 192 task rows after CEO decision packet drafts, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 100:
        failures.append(f"expected 100 evidence rows after CEO decision packet drafts, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision packet drafts evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision packet drafts")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_drafts": task_rows_inserted_by_drafts,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_packet_drafts_validation.v1",
        "generated_utc": generated_utc,
        "draft_path": str(json_output_path),
        "draft_lane_id": lane_id,
        "draft_task_id": draft_task_id,
        "source_triage_task_id": source_triage_task_id,
        "source_triage_evidence_id": source_triage_evidence_id,
        "source_active_blocker_count": source_active_blocker_count,
        "source_triage_batch_count": source_triage_batch_count,
        "source_high_leverage_batch_count": source_high_leverage_batch_count,
        "packet_draft_count": packet_draft_count,
        "decision_option_count": decision_option_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_drafts": task_rows_inserted_by_drafts,
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
                "draft_lane_id": lane_id,
                "draft_task_id": draft_task_id,
                "packet_draft_count": packet_draft_count,
                "task_rows_inserted_by_drafts": task_rows_inserted_by_drafts,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )