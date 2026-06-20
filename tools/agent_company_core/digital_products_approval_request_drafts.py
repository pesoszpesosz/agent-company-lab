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


def digital_products_approval_request_draft_packets() -> list[dict[str, object]]:
    return [
        {
            "draft_id": "read-only-browser-validation",
            "gate_required": "browser_read_only_session",
            "request_type": "future_approval_request_draft",
            "approval_status": "not_requested",
            "purpose": "Compare public marketplace/category demand, saturation, price bands, and buyer language for the polished checklist pack.",
            "allowed_if_approved": [
                "Open read-only public marketplace or category pages.",
                "Record observed demand language, price ranges, and saturation signals.",
                "Avoid login, posting, listing, messaging, checkout, account settings, and personal data entry.",
            ],
            "blocked_until_approved": [
                "Do not browse marketplaces from this draft.",
                "Do not create accounts, save listings, post comments, publish pages, or transmit data.",
            ],
        },
        {
            "draft_id": "legal-payment-review",
            "gate_required": "legal_kyc_tax_payment",
            "request_type": "future_approval_request_draft",
            "approval_status": "not_requested",
            "purpose": "Review seller terms, platform fees, refund exposure, tax/KYC obligations, payout setup, and payment constraints before any seller work.",
            "allowed_if_approved": [
                "Read terms and fee pages in a non-accepting review mode.",
                "Summarize obligations, risks, and required user decisions.",
                "Identify what remains blocked before account or payout setup.",
            ],
            "blocked_until_approved": [
                "Do not accept agreements, create seller accounts, configure payouts, connect payment methods, or provide KYC/tax data.",
                "Do not list, price, sell, or claim platform readiness.",
            ],
        },
    ]


def write_digital_products_local_approval_request_drafts(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    draft_task_id = "task-digital-products-local-approval-request-drafts-20260616"
    draft_evidence_id = "digital-products-local-approval-request-drafts-20260616"
    source_readiness_task_id = "task-digital-products-local-post-polish-readiness-20260616"
    source_readiness_evidence_id = "digital-products-local-post-polish-readiness-20260616"
    duplicate_key = "digital-products-local-approval-request-drafts-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "approval_request_drafts_ready_not_submitted"
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_readiness_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_readiness_evidence_id,),
    ).fetchone()
    readiness_validation = load_json(DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON)
    readiness_payload = load_json(DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_JSON)
    draft_packets = digital_products_approval_request_draft_packets()
    blocked_questions = readiness_payload.get("blocked_by_gate_questions", [])
    browser_draft_count = sum(1 for packet in draft_packets if packet.get("gate_required") == "browser_read_only_session")
    legal_payment_draft_count = sum(1 for packet in draft_packets if packet.get("gate_required") == "legal_kyc_tax_payment")

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (draft_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    draft_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (draft_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source post-polish readiness task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_post_polish_readiness_complete":
        failures.append("source post-polish readiness evidence is missing or not complete")
    if not readiness_validation.get("all_checks_passed") or readiness_validation.get("failure_count") != 0:
        failures.append("source post-polish readiness validation is not clean")
    if readiness_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {readiness_payload.get('selected_candidate_id')}")
    if len(draft_packets) != 2:
        failures.append(f"expected 2 draft packets, got {len(draft_packets)}")
    if browser_draft_count != 1:
        failures.append(f"expected 1 browser draft, got {browser_draft_count}")
    if legal_payment_draft_count != 1:
        failures.append(f"expected 1 legal/payment draft, got {legal_payment_draft_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target approval-request drafts task already exists: {draft_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if draft_evidence_exists_before:
        failures.append(f"approval-request drafts evidence already exists: {draft_evidence_id}")
    if tasks_table_rows_before != 184:
        failures.append(f"expected 184 task rows before approval-request drafts, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 93:
        failures.append(f"expected 93 evidence rows before approval-request drafts, got {lane_evidence_rows_before}")

    draft_summary = (
        "Drafted two local approval-request packets for the polished AI builder launch checklist pack: "
        "one read-only browser validation draft and one legal/payment review draft. They are not submitted and do not mutate service requests."
    )
    draft_next_action = (
        "Review these local drafts and decide whether to explicitly request browser or legal/payment approval; do not browse, submit, accept terms, create accounts, or configure payouts."
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
        "schema_version": "agent_company.digital_products_local_approval_request_drafts.v1",
        "generated_utc": generated_utc,
        "draft_lane_id": lane_id,
        "draft_task_id": draft_task_id,
        "draft_evidence_id": draft_evidence_id,
        "source_readiness_task_id": source_readiness_task_id,
        "source_readiness_evidence_id": source_readiness_evidence_id,
        "source_readiness_validation_path": str(DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "approval_request_count": approval_request_count,
        "draft_packet_count": len(draft_packets),
        "browser_draft_count": browser_draft_count,
        "legal_payment_draft_count": legal_payment_draft_count,
        "draft_packets": draft_packets,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": draft_summary,
        "next_action": draft_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Approval Request Drafts",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        draft_summary,
        "",
        "## Draft Packets",
        "",
    ]
    for packet in draft_packets:
        md_lines.extend(
            [
                f"### {packet['draft_id']}",
                "",
                f"Gate: `{packet['gate_required']}`",
                f"Approval status: `{packet['approval_status']}`",
                "",
                f"Purpose: {packet['purpose']}",
                "",
                "Allowed if approved:",
            ]
        )
        for item in packet["allowed_if_approved"]:
            md_lines.append(f"- {item}")
        md_lines.append("")
        md_lines.append("Blocked until approved:")
        for item in packet["blocked_until_approved"]:
            md_lines.append(f"- {item}")
        md_lines.append("")
    md_lines.extend(["## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These packets are local drafts only. They do not request approval, browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            draft_next_action,
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
                draft_task_id,
                lane_id,
                "Draft local digital-products approval request packets",
                52,
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
                "title": "Digital products local approval request drafts",
                "status": "local_approval_request_drafts_complete",
                "summary": draft_summary,
                "next_action": draft_next_action,
                "ownership_note": "Generated by platform_engineering from post-polish readiness; digital-products lane manager owns any explicit future approval request.",
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
        failures.append(f"expected 1 task row inserted by approval-request drafts, got {task_rows_inserted_by_drafts}")
    if tasks_table_rows_after != 185:
        failures.append(f"expected 185 task rows after approval-request drafts, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 94:
        failures.append(f"expected 94 evidence rows after approval-request drafts, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("approval-request drafts evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during approval-request drafts")
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
        "schema_version": "agent_company.digital_products_local_approval_request_drafts_validation.v1",
        "generated_utc": generated_utc,
        "draft_path": str(json_output_path),
        "draft_lane_id": lane_id,
        "draft_task_id": draft_task_id,
        "source_readiness_task_id": source_readiness_task_id,
        "source_readiness_evidence_id": source_readiness_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "draft_packet_count": len(draft_packets),
        "browser_draft_count": browser_draft_count,
        "legal_payment_draft_count": legal_payment_draft_count,
        "approval_request_count": approval_request_count,
        "blocked_by_gate_count": len(blocked_questions),
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
                "task_rows_inserted_by_drafts": task_rows_inserted_by_drafts,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
