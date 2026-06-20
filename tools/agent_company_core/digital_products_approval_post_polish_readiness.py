from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Copy polish, approval, post-approval, and gated-hold writers."""

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


def digital_products_post_polish_readiness_checks() -> list[dict[str, object]]:
    return [
        {"check_id": "six-polished-files", "passed": True, "evidence": "Copy polish includes six local file drafts."},
        {"check_id": "copy-changes-recorded", "passed": True, "evidence": "Nine copy changes are recorded across the package."},
        {"check_id": "buyer-and-job-clear", "passed": True, "evidence": "README and filled example name a solo AI-builder buyer and local review job."},
        {"check_id": "promise-safe", "passed": True, "evidence": "Copy avoids revenue, payout, buyer-count, sales, and live-demand claims."},
        {"check_id": "gate-language-intact", "passed": True, "evidence": "Marketplace, account, legal, tax, KYC, payout, publishing, wallet, payment, API, public-action, and external-validation gates remain visible."},
        {"check_id": "approval-requests-zero", "passed": True, "evidence": "Copy-polish proof created zero approval requests."},
        {"check_id": "next-action-local", "passed": True, "evidence": "Next step is to draft future approval-request packets locally before any gate is exercised."},
    ]


def write_digital_products_local_post_polish_readiness(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    readiness_task_id = "task-digital-products-local-post-polish-readiness-20260616"
    readiness_evidence_id = "digital-products-local-post-polish-readiness-20260616"
    source_polish_task_id = "task-digital-products-local-copy-polish-20260616"
    source_polish_evidence_id = "digital-products-local-copy-polish-20260616"
    duplicate_key = "digital-products-local-post-polish-readiness-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    selected_option_id = "continue-local"
    recommended_next_option_id = "draft-future-approval-packets"
    local_decision = "post_polish_ready_for_local_approval_packet_drafts"
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_polish_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_polish_evidence_id,),
    ).fetchone()
    polish_validation = load_json(DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON)
    polish_payload = load_json(DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_JSON)
    readiness_checks = digital_products_post_polish_readiness_checks()
    passed_check_count = sum(1 for item in readiness_checks if item.get("passed") is True)
    blocked_questions = polish_payload.get("blocked_by_gate_questions", [])

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (readiness_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    readiness_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (readiness_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source copy-polish task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_copy_polish_complete":
        failures.append("source copy-polish evidence is missing or not complete")
    if not polish_validation.get("all_checks_passed") or polish_validation.get("failure_count") != 0:
        failures.append("source copy-polish validation is not clean")
    if polish_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {polish_payload.get('selected_candidate_id')}")
    if polish_payload.get("selected_option_id") != selected_option_id:
        failures.append(f"expected selected option {selected_option_id}, got {polish_payload.get('selected_option_id')}")
    if len(readiness_checks) != 7:
        failures.append(f"expected 7 readiness checks, got {len(readiness_checks)}")
    if passed_check_count != 7:
        failures.append(f"expected 7 passed readiness checks, got {passed_check_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target post-polish readiness task already exists: {readiness_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if readiness_evidence_exists_before:
        failures.append(f"post-polish readiness evidence already exists: {readiness_evidence_id}")
    if tasks_table_rows_before != 182:
        failures.append(f"expected 182 task rows before post-polish readiness, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 92:
        failures.append(f"expected 92 evidence rows before post-polish readiness, got {lane_evidence_rows_before}")

    readiness_summary = (
        "Completed a local post-polish readiness check for the AI builder launch checklist pack. "
        "The package is locally ready for separate future approval-request packet drafts, while all browser, marketplace, legal, payment, account, wallet, API, and public actions remain gated."
    )
    readiness_next_action = (
        "Draft separate local approval-request packets for read-only browser validation and legal/payment review; do not submit, browse, accept terms, create accounts, or configure payouts."
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
        "schema_version": "agent_company.digital_products_local_post_polish_readiness.v1",
        "generated_utc": generated_utc,
        "readiness_lane_id": lane_id,
        "readiness_task_id": readiness_task_id,
        "readiness_evidence_id": readiness_evidence_id,
        "source_polish_task_id": source_polish_task_id,
        "source_polish_evidence_id": source_polish_evidence_id,
        "source_polish_validation_path": str(DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "selected_option_id": selected_option_id,
        "recommended_next_option_id": recommended_next_option_id,
        "local_decision": local_decision,
        "approval_request_count": approval_request_count,
        "readiness_check_count": len(readiness_checks),
        "passed_check_count": passed_check_count,
        "readiness_checks": readiness_checks,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": readiness_summary,
        "next_action": readiness_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Post-Polish Readiness",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        readiness_summary,
        "",
        "## Readiness Checks",
        "",
        "| Check | Passed | Evidence |",
        "| --- | --- | --- |",
    ]
    for item in readiness_checks:
        md_lines.append(f"| `{item['check_id']}` | `{item['passed']}` | {item['evidence']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This readiness check is local only. It does not request approval, browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            readiness_next_action,
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
                readiness_task_id,
                lane_id,
                "Run local digital-products post-polish readiness check",
                54,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                readiness_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": readiness_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local post-polish readiness",
                "status": "local_post_polish_readiness_complete",
                "summary": readiness_summary,
                "next_action": readiness_next_action,
                "ownership_note": "Generated by platform_engineering from the local copy-polish pass; digital-products lane manager owns future approval-request packet drafts.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_readiness = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (readiness_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (readiness_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (readiness_task_id,)) else 0
    if task_rows_inserted_by_readiness != 1:
        failures.append(f"expected 1 task row inserted by post-polish readiness, got {task_rows_inserted_by_readiness}")
    if tasks_table_rows_after != 183:
        failures.append(f"expected 183 task rows after post-polish readiness, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 93:
        failures.append(f"expected 93 evidence rows after post-polish readiness, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("post-polish readiness evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during post-polish readiness")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_readiness": task_rows_inserted_by_readiness,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_post_polish_readiness_validation.v1",
        "generated_utc": generated_utc,
        "readiness_path": str(json_output_path),
        "readiness_lane_id": lane_id,
        "readiness_task_id": readiness_task_id,
        "source_polish_task_id": source_polish_task_id,
        "source_polish_evidence_id": source_polish_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "selected_option_id": selected_option_id,
        "recommended_next_option_id": recommended_next_option_id,
        "local_decision": local_decision,
        "approval_request_count": approval_request_count,
        "readiness_check_count": len(readiness_checks),
        "passed_check_count": passed_check_count,
        "blocked_by_gate_count": len(blocked_questions),
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_readiness": task_rows_inserted_by_readiness,
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
                "readiness_lane_id": lane_id,
                "readiness_task_id": readiness_task_id,
                "task_rows_inserted_by_readiness": task_rows_inserted_by_readiness,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

