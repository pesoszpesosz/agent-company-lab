from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Local digital-products copy polish report writer."""

from .digital_products_approval_copy_polish_content import digital_products_copy_polish_files
from .constants import (
    DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_JSON,
    DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_JSON,
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_REPORT,
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_REPORT,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_JSON,
    DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_REPORT,
    DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar

def write_digital_products_local_copy_polish(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    polish_task_id = "task-digital-products-local-copy-polish-20260616"
    polish_evidence_id = "digital-products-local-copy-polish-20260616"
    source_choice_task_id = "task-digital-products-local-gate-choice-20260616"
    source_choice_evidence_id = "digital-products-local-gate-choice-20260616"
    duplicate_key = "digital-products-local-copy-polish-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    selected_option_id = "continue-local"
    local_decision = "copy_polish_complete_no_gate_exercised"
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_choice_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_choice_evidence_id,),
    ).fetchone()
    choice_validation = load_json(DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON)
    choice_payload = load_json(DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_JSON)
    polished_files = digital_products_copy_polish_files()
    blocked_questions = choice_payload.get("blocked_by_gate_questions", [])
    all_text = "\n".join(
        line
        for file_payload in polished_files
        for line in file_payload.get("polished_copy", [])
        if isinstance(line, str)
    ).lower()
    boundary_terms = ["marketplace", "account", "legal", "tax", "kyc", "payout", "publishing"]
    boundary_phrase_count = sum(1 for term in boundary_terms if term in all_text)
    copy_change_count = sum(len(file_payload.get("copy_changes", [])) for file_payload in polished_files)

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (polish_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    polish_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (polish_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source gate-choice task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_gate_choice_complete":
        failures.append("source gate-choice evidence is missing or not complete")
    if not choice_validation.get("all_checks_passed") or choice_validation.get("failure_count") != 0:
        failures.append("source gate-choice validation is not clean")
    if choice_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {choice_payload.get('selected_candidate_id')}")
    if choice_payload.get("selected_option_id") != selected_option_id:
        failures.append(f"expected selected option {selected_option_id}, got {choice_payload.get('selected_option_id')}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if len(polished_files) != 6:
        failures.append(f"expected 6 polished files, got {len(polished_files)}")
    if copy_change_count != 9:
        failures.append(f"expected 9 copy changes, got {copy_change_count}")
    if boundary_phrase_count != 7:
        failures.append(f"expected 7 boundary phrases, got {boundary_phrase_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target copy-polish task already exists: {polish_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if polish_evidence_exists_before:
        failures.append(f"copy-polish evidence already exists: {polish_evidence_id}")
    if tasks_table_rows_before != 180:
        failures.append(f"expected 180 task rows before copy polish, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 91:
        failures.append(f"expected 91 evidence rows before copy polish, got {lane_evidence_rows_before}")

    polish_summary = (
        "Completed a local copy-polish pass for the revised AI builder launch checklist pack. "
        "The pass tightens six local file drafts, records nine copy changes, and keeps all gate language intact."
    )
    polish_next_action = (
        "Run a local post-polish readiness check and decide whether to continue locally or draft separate future approval-request packets; do not exercise any gate."
    )
    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "agent_company.digital_products_local_copy_polish.v1",
        "generated_utc": generated_utc,
        "polish_lane_id": lane_id,
        "polish_task_id": polish_task_id,
        "polish_evidence_id": polish_evidence_id,
        "source_choice_task_id": source_choice_task_id,
        "source_choice_evidence_id": source_choice_evidence_id,
        "source_choice_validation_path": str(DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "selected_option_id": selected_option_id,
        "local_decision": local_decision,
        "approval_request_count": approval_request_count,
        "polished_file_count": len(polished_files),
        "polished_files": polished_files,
        "copy_change_count": copy_change_count,
        "boundary_phrase_count": boundary_phrase_count,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": polish_summary,
        "next_action": polish_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Copy Polish",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        polish_summary,
        "",
        "## Polished Files",
        "",
    ]
    for file_payload in polished_files:
        md_lines.extend([f"### {file_payload['filename']}", "", "Copy changes:"])
        for change in file_payload["copy_changes"]:
            md_lines.append(f"- {change}")
        md_lines.extend(["", "Polished copy:"])
        for line in file_payload["polished_copy"]:
            md_lines.append(f"- {line}")
        md_lines.append("")
    md_lines.extend(["## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This copy-polish pass is local only. It does not request approval, browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            polish_next_action,
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
                polish_task_id,
                lane_id,
                "Run local digital-products copy-polish pass",
                56,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                polish_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": polish_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local copy polish",
                "status": "local_copy_polish_complete",
                "summary": polish_summary,
                "next_action": polish_next_action,
                "ownership_note": "Generated by platform_engineering from the local gate choice; digital-products lane manager owns local readiness follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_polish = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (polish_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (polish_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (polish_task_id,)) else 0
    if task_rows_inserted_by_polish != 1:
        failures.append(f"expected 1 task row inserted by copy polish, got {task_rows_inserted_by_polish}")
    if tasks_table_rows_after != 181:
        failures.append(f"expected 181 task rows after copy polish, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 92:
        failures.append(f"expected 92 evidence rows after copy polish, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("copy-polish evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during copy polish")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_polish": task_rows_inserted_by_polish,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_copy_polish_validation.v1",
        "generated_utc": generated_utc,
        "polish_path": str(json_output_path),
        "polish_lane_id": lane_id,
        "polish_task_id": polish_task_id,
        "source_choice_task_id": source_choice_task_id,
        "source_choice_evidence_id": source_choice_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "selected_option_id": selected_option_id,
        "local_decision": local_decision,
        "approval_request_count": approval_request_count,
        "polished_file_count": len(polished_files),
        "copy_change_count": copy_change_count,
        "boundary_phrase_count": boundary_phrase_count,
        "blocked_by_gate_count": len(blocked_questions),
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_polish": task_rows_inserted_by_polish,
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
                "polish_lane_id": lane_id,
                "polish_task_id": polish_task_id,
                "task_rows_inserted_by_polish": task_rows_inserted_by_polish,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

__all__ = [
    "digital_products_copy_polish_files",
    "write_digital_products_local_copy_polish",
]
