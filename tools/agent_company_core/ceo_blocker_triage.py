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
from .ceo_blocker_triage_content import build_ceo_blocker_triage_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_ceo_blocker_triage(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_BLOCKER_TRIAGE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_BLOCKER_TRIAGE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_BLOCKER_TRIAGE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    triage_lane_id = "platform_engineering"
    triage_task_id = "task-ceo-blocker-triage-20260616"
    triage_evidence_id = "ceo-blocker-triage-20260616"
    source_board_task_id = "task-ceo-gate-blocker-board-20260616"
    source_board_evidence_id = "ceo-gate-blocker-board-20260616"
    duplicate_key = "ceo-blocker-triage-20260616"

    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (triage_lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_board_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_board_evidence_id,),
    ).fetchone()
    board_validation = load_json(CEO_GATE_BLOCKER_BOARD_VALIDATION_JSON)
    board_payload = load_json(CEO_GATE_BLOCKER_BOARD_JSON)
    blocker_items = board_payload.get("blocker_items", [])
    source_active_blocker_count = int(board_payload.get("active_blocker_count", 0))
    service_request_needs_review_count = int(board_payload.get("service_request_needs_review_count", 0))
    active_hold_count = int(board_payload.get("active_hold_count", 0))

    triage_content = build_ceo_blocker_triage_content(blocker_items)
    local_decision = triage_content["local_decision"]
    recommended_default = triage_content["recommended_default"]
    approval_request_count = triage_content["approval_request_count"]
    runnable_without_approval_count = triage_content["runnable_without_approval_count"]
    triage_batches = triage_content["triage_batches"]
    triage_batch_count = triage_content["triage_batch_count"]
    high_leverage_batch_count = triage_content["high_leverage_batch_count"]
    covered_blocker_ids = triage_content["covered_blocker_ids"]
    missing_blocker_ids = triage_content["missing_blocker_ids"]
    triage_summary = triage_content["summary"]
    triage_next_action = triage_content["next_action"]
    runtime_boundary = triage_content["runtime_boundary"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (triage_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    triage_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (triage_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source CEO gate blocker board task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_ceo_gate_blocker_board_complete":
        failures.append("source CEO gate blocker board evidence is missing or not complete")
    if not board_validation.get("all_checks_passed") or board_validation.get("failure_count") != 0:
        failures.append("source CEO gate blocker board validation is not clean")
    if source_active_blocker_count != 15:
        failures.append(f"expected 15 source active blockers, got {source_active_blocker_count}")
    if len(blocker_items) != 15:
        failures.append(f"expected 15 blocker items, got {len(blocker_items)}")
    if service_request_needs_review_count != 11:
        failures.append(f"expected 11 service requests needing review, got {service_request_needs_review_count}")
    if active_hold_count != 4:
        failures.append(f"expected 4 active holds, got {active_hold_count}")
    if triage_batch_count != 5:
        failures.append(f"expected 5 triage batches, got {triage_batch_count}")
    if high_leverage_batch_count != 3:
        failures.append(f"expected 3 high-leverage batches, got {high_leverage_batch_count}")
    if len(covered_blocker_ids) != 15:
        failures.append(f"expected 15 covered blockers, got {len(covered_blocker_ids)}")
    if missing_blocker_ids:
        failures.append(f"triage batches did not cover blockers: {', '.join(missing_blocker_ids)}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval blockers, got {runnable_without_approval_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target CEO blocker triage task already exists: {triage_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if triage_evidence_exists_before:
        failures.append(f"CEO blocker triage evidence already exists: {triage_evidence_id}")
    if tasks_table_rows_before != 190:
        failures.append(f"expected 190 task rows before CEO blocker triage, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 98:
        failures.append(f"expected 98 evidence rows before CEO blocker triage, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.ceo_blocker_triage.v1",
        "generated_utc": generated_utc,
        "triage_lane_id": triage_lane_id,
        "triage_task_id": triage_task_id,
        "triage_evidence_id": triage_evidence_id,
        "source_board_task_id": source_board_task_id,
        "source_board_evidence_id": source_board_evidence_id,
        "source_board_validation_path": str(CEO_GATE_BLOCKER_BOARD_VALIDATION_JSON),
        "source_active_blocker_count": source_active_blocker_count,
        "service_request_needs_review_count": service_request_needs_review_count,
        "active_hold_count": active_hold_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "triage_batch_count": triage_batch_count,
        "high_leverage_batch_count": high_leverage_batch_count,
        "covered_blocker_count": len(covered_blocker_ids),
        "missing_blocker_ids": missing_blocker_ids,
        "triage_batches": triage_batches,
        "summary": triage_summary,
        "next_action": triage_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Blocker Triage",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        triage_summary,
        "",
        "## Ranked Batches",
        "",
        "| Priority | Batch | Leverage | Blockers |",
        "| --- | --- | --- | --- |",
    ]
    for batch in triage_batches:
        md_lines.append(
            f"| `{batch['priority']}` | `{batch['batch_id']}` | `{batch['leverage']}` | `{len(batch['blocker_ids'])}` |"
        )
    md_lines.extend(["", "## Batch Notes", ""])
    for batch in triage_batches:
        md_lines.extend(
            [
                f"### {batch['batch_id']}",
                "",
                f"Decision needed: {batch['decision_needed']}",
                "",
                f"Why it matters: {batch['why_it_matters']}",
                "",
                "Blockers:",
            ]
        )
        for blocker_id in batch["blocker_ids"]:
            md_lines.append(f"- `{blocker_id}`")
        md_lines.append("")
    md_lines.extend(
        [
            "## Boundary",
            "",
            "This is a local triage view only. It does not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            triage_next_action,
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
                triage_task_id,
                triage_lane_id,
                "Create CEO blocker triage",
                47,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                triage_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": triage_evidence_id,
                "lane_id": triage_lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO blocker triage",
                "status": "local_ceo_blocker_triage_complete",
                "summary": triage_summary,
                "next_action": triage_next_action,
                "ownership_note": "Generated by platform_engineering from the CEO gate blocker board; triage is read-only and cannot authorize action.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_triage = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (triage_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (triage_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (triage_task_id,)) else 0
    if task_rows_inserted_by_triage != 1:
        failures.append(f"expected 1 task row inserted by CEO blocker triage, got {task_rows_inserted_by_triage}")
    if tasks_table_rows_after != 191:
        failures.append(f"expected 191 task rows after CEO blocker triage, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 99:
        failures.append(f"expected 99 evidence rows after CEO blocker triage, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO blocker triage evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO blocker triage")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_triage": task_rows_inserted_by_triage,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_blocker_triage_validation.v1",
        "generated_utc": generated_utc,
        "triage_path": str(json_output_path),
        "triage_lane_id": triage_lane_id,
        "triage_task_id": triage_task_id,
        "source_board_task_id": source_board_task_id,
        "source_board_evidence_id": source_board_evidence_id,
        "source_active_blocker_count": source_active_blocker_count,
        "triage_batch_count": triage_batch_count,
        "high_leverage_batch_count": high_leverage_batch_count,
        "service_request_needs_review_count": service_request_needs_review_count,
        "active_hold_count": active_hold_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_triage": task_rows_inserted_by_triage,
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
                "triage_lane_id": triage_lane_id,
                "triage_task_id": triage_task_id,
                "triage_batch_count": triage_batch_count,
                "task_rows_inserted_by_triage": task_rows_inserted_by_triage,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


