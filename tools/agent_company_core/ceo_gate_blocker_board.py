from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .constants import (
    CEO_BLOCKER_TRIAGE_JSON,
    CEO_BLOCKER_TRIAGE_REPORT,
    CEO_BLOCKER_TRIAGE_VALIDATION_JSON,
    CEO_DECISION_INTAKE_GUARD_JSON,
    CEO_DECISION_INTAKE_GUARD_REPORT,
    CEO_DECISION_INTAKE_GUARD_VALIDATION_JSON,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_JSON,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_REPORT,
    CEO_DECISION_INTAKE_NEGATIVE_FIXTURES_VALIDATION_JSON,
    CEO_DECISION_PACKET_DRAFTS_JSON,
    CEO_DECISION_PACKET_DRAFTS_REPORT,
    CEO_DECISION_PACKET_DRAFTS_VALIDATION_JSON,
    CEO_GATE_BLOCKER_BOARD_JSON,
    CEO_GATE_BLOCKER_BOARD_REPORT,
    CEO_GATE_BLOCKER_BOARD_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON,
)
from .ceo_gate_blocker_board_content import build_ceo_gate_blocker_board_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_gate_blocker_board(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_GATE_BLOCKER_BOARD_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_GATE_BLOCKER_BOARD_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_GATE_BLOCKER_BOARD_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    board_lane_id = "platform_engineering"
    board_task_id = "task-ceo-gate-blocker-board-20260616"
    board_evidence_id = "ceo-gate-blocker-board-20260616"
    source_register_task_id = "task-digital-products-local-gated-hold-register-20260616"
    source_register_evidence_id = "digital-products-local-gated-hold-register-20260616"
    duplicate_key = "ceo-gate-blocker-board-20260616"

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (board_lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_register_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_register_evidence_id,),
    ).fetchone()
    register_validation = load_json(DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON)
    register_payload = load_json(DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_JSON)
    hold_entries = register_payload.get("hold_entries", [])

    service_request_rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT request_id, request_type, lane_id, status, risk_gate, requested_action, assigned_agent_id, updated_at
            FROM service_requests
            ORDER BY updated_at DESC, request_id
            """
        )
    ]
    service_request_status_counts = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    board_content = build_ceo_gate_blocker_board_content(
        service_request_rows=service_request_rows,
        service_request_status_counts=service_request_status_counts,
        hold_entries=hold_entries,
        register_lane_id=register_payload.get("register_lane_id"),
    )
    local_decision = board_content["local_decision"]
    recommended_default = board_content["recommended_default"]
    service_request_total_count = board_content["service_request_total_count"]
    service_request_needs_review_count = board_content["service_request_needs_review_count"]
    service_request_rejected_count = board_content["service_request_rejected_count"]
    service_request_complete_count = board_content["service_request_complete_count"]
    active_hold_count = board_content["active_hold_count"]
    active_blocker_count = board_content["active_blocker_count"]
    active_blocker_lane_count = board_content["active_blocker_lane_count"]
    active_blocker_lane_ids = board_content["active_blocker_lane_ids"]
    runnable_without_approval_count = board_content["runnable_without_approval_count"]
    approval_request_count = board_content["approval_request_count"]
    service_request_blockers = board_content["service_request_blockers"]
    hold_blockers = board_content["hold_blockers"]
    blocker_items = board_content["blocker_items"]
    board_summary = board_content["summary"]
    board_next_action = board_content["next_action"]
    runtime_boundary = board_content["runtime_boundary"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (board_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    board_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (board_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source gated hold register task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_gated_hold_register_complete":
        failures.append("source gated hold register evidence is missing or not complete")
    if not register_validation.get("all_checks_passed") or register_validation.get("failure_count") != 0:
        failures.append("source gated hold register validation is not clean")
    if service_request_total_count != 14:
        failures.append(f"expected 14 service requests, got {service_request_total_count}")
    if service_request_needs_review_count != 11:
        failures.append(f"expected 11 service requests needing review, got {service_request_needs_review_count}")
    if service_request_rejected_count != 2:
        failures.append(f"expected 2 rejected service requests, got {service_request_rejected_count}")
    if service_request_complete_count != 1:
        failures.append(f"expected 1 complete service request, got {service_request_complete_count}")
    if active_hold_count != 4:
        failures.append(f"expected 4 active local holds, got {active_hold_count}")
    if active_blocker_count != 15:
        failures.append(f"expected 15 active blockers, got {active_blocker_count}")
    if active_blocker_lane_count != 7:
        failures.append(f"expected 7 active blocker lanes, got {active_blocker_lane_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval blockers, got {runnable_without_approval_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO gate blocker board task already exists: {board_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if board_evidence_exists_before:
        failures.append(f"CEO gate blocker board evidence already exists: {board_evidence_id}")
    if tasks_table_rows_before != 189:
        failures.append(f"expected 189 task rows before CEO gate blocker board, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 97:
        failures.append(f"expected 97 evidence rows before CEO gate blocker board, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.ceo_gate_blocker_board.v1",
        "generated_utc": generated_utc,
        "board_lane_id": board_lane_id,
        "board_task_id": board_task_id,
        "board_evidence_id": board_evidence_id,
        "source_register_task_id": source_register_task_id,
        "source_register_evidence_id": source_register_evidence_id,
        "source_register_validation_path": str(DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON),
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "service_request_total_count": service_request_total_count,
        "service_request_needs_review_count": service_request_needs_review_count,
        "service_request_rejected_count": service_request_rejected_count,
        "service_request_complete_count": service_request_complete_count,
        "service_request_status_counts": service_request_status_counts,
        "active_hold_count": active_hold_count,
        "active_blocker_count": active_blocker_count,
        "active_blocker_lane_count": active_blocker_lane_count,
        "active_blocker_lane_ids": active_blocker_lane_ids,
        "runnable_without_approval_count": runnable_without_approval_count,
        "approval_request_count": approval_request_count,
        "blocker_items": blocker_items,
        "summary": board_summary,
        "next_action": board_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Gate Blocker Board",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        board_summary,
        "",
        "## Counts",
        "",
        f"- Active blockers: `{active_blocker_count}`",
        f"- Service requests needing review: `{service_request_needs_review_count}`",
        f"- Local gated holds: `{active_hold_count}`",
        f"- Active blocker lanes: `{active_blocker_lane_count}`",
        f"- Runnable without approval: `{runnable_without_approval_count}`",
        "",
        "## Active Blocker Lanes",
        "",
    ]
    for lane_id in active_blocker_lane_ids:
        md_lines.append(f"- `{lane_id}`")
    md_lines.extend(["", "## Service Requests Needing Review", "", "| Request | Lane | Type | Gate |", "| --- | --- | --- | --- |"])
    for item in service_request_blockers:
        md_lines.append(f"| `{item['blocker_id']}` | `{item['lane_id']}` | `{item['request_type']}` | `{item['risk_gate']}` |")
    md_lines.extend(["", "## Local Gated Holds", "", "| Hold | Lane | Gate | Resume Trigger |", "| --- | --- | --- | --- |"])
    for item in hold_blockers:
        md_lines.append(f"| `{item['blocker_id']}` | `{item['lane_id']}` | `{item['risk_gate']}` | {item['resume_trigger']} |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local CEO board only. It does not approve, reject, assign, or update service requests; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; start workers; or create external side effects.",
            "",
            "## Next Action",
            "",
            board_next_action,
            "",
        ]
    )
    output_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                board_task_id,
                board_lane_id,
                "Create CEO gate blocker board",
                48,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                board_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": board_evidence_id,
                "lane_id": board_lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO gate blocker board",
                "status": "local_ceo_gate_blocker_board_complete",
                "summary": board_summary,
                "next_action": board_next_action,
                "ownership_note": "Generated by platform_engineering from service_requests and the digital-products gated hold register; board is read-only and cannot authorize action.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_board = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (board_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (board_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (board_task_id,)) else 0
    if task_rows_inserted_by_board != 1:
        failures.append(f"expected 1 task row inserted by CEO gate blocker board, got {task_rows_inserted_by_board}")
    if tasks_table_rows_after != 190:
        failures.append(f"expected 190 task rows after CEO gate blocker board, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 98:
        failures.append(f"expected 98 evidence rows after CEO gate blocker board, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO gate blocker board evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO gate blocker board")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_board": task_rows_inserted_by_board,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_gate_blocker_board_validation.v1",
        "generated_utc": generated_utc,
        "board_path": str(json_output_path),
        "board_lane_id": board_lane_id,
        "board_task_id": board_task_id,
        "source_register_task_id": source_register_task_id,
        "source_register_evidence_id": source_register_evidence_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "service_request_total_count": service_request_total_count,
        "service_request_needs_review_count": service_request_needs_review_count,
        "service_request_rejected_count": service_request_rejected_count,
        "service_request_complete_count": service_request_complete_count,
        "active_hold_count": active_hold_count,
        "active_blocker_count": active_blocker_count,
        "active_blocker_lane_count": active_blocker_lane_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "approval_request_count": approval_request_count,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_board": task_rows_inserted_by_board,
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
                "board_lane_id": board_lane_id,
                "board_task_id": board_task_id,
                "active_blocker_count": active_blocker_count,
                "task_rows_inserted_by_board": task_rows_inserted_by_board,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

