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


def write_digital_products_local_operator_approval_brief(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    brief_task_id = "task-digital-products-local-operator-approval-brief-20260616"
    brief_evidence_id = "digital-products-local-operator-approval-brief-20260616"
    source_drafts_task_id = "task-digital-products-local-approval-request-drafts-20260616"
    source_drafts_evidence_id = "digital-products-local-approval-request-drafts-20260616"
    duplicate_key = "digital-products-local-operator-approval-brief-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "operator_approval_brief_ready_not_requested"
    recommended_default = "hold_until_explicit_user_approval"
    approval_request_count = 0
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
    drafts_validation = load_json(DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_VALIDATION_JSON)
    drafts_payload = load_json(DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_JSON)
    draft_packets = drafts_payload.get("draft_packets", [])
    blocked_questions = drafts_payload.get("blocked_by_gate_questions", [])

    decision_items = [
        {
            "decision_id": "approve-read-only-browser-validation",
            "source_draft_id": "read-only-browser-validation",
            "approval_required": True,
            "gate_required": "browser_read_only_session",
            "default_without_approval": "Do not open marketplace/category pages or collect live browser evidence.",
            "approval_text_draft": "Approve one read-only browser validation pass for public marketplace/category pages only, with no login, posting, listing, messaging, checkout, account settings, personal data entry, or saved changes.",
            "operator_review_note": "Use this only to validate demand, price bands, saturation, and buyer language for the polished AI builder launch checklist pack.",
        },
        {
            "decision_id": "approve-legal-payment-review",
            "source_draft_id": "legal-payment-review",
            "approval_required": True,
            "gate_required": "legal_kyc_tax_payment",
            "default_without_approval": "Do not accept terms, create seller accounts, configure payouts, list products, or provide KYC/tax/payment data.",
            "approval_text_draft": "Approve local legal/payment review of platform terms, fees, refund exposure, KYC/tax obligations, and payout constraints in a non-accepting read-only mode.",
            "operator_review_note": "This is not permission to register, sell, connect payment methods, or accept agreements.",
        },
    ]
    explicit_approval_required_count = sum(1 for item in decision_items if item.get("approval_required"))

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (brief_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    brief_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (brief_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source approval-request drafts task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_approval_request_drafts_complete":
        failures.append("source approval-request drafts evidence is missing or not complete")
    if not drafts_validation.get("all_checks_passed") or drafts_validation.get("failure_count") != 0:
        failures.append("source approval-request drafts validation is not clean")
    if drafts_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {drafts_payload.get('selected_candidate_id')}")
    if len(draft_packets) != 2:
        failures.append(f"expected 2 source draft packets, got {len(draft_packets)}")
    if len(decision_items) != 2:
        failures.append(f"expected 2 decision items, got {len(decision_items)}")
    if explicit_approval_required_count != 2:
        failures.append(f"expected 2 explicit approval decisions, got {explicit_approval_required_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target operator approval brief task already exists: {brief_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if brief_evidence_exists_before:
        failures.append(f"operator approval brief evidence already exists: {brief_evidence_id}")
    if tasks_table_rows_before != 186:
        failures.append(f"expected 186 task rows before operator approval brief, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 94:
        failures.append(f"expected 94 evidence rows before operator approval brief, got {lane_evidence_rows_before}")

    brief_summary = (
        "Prepared a local operator approval brief that converts the two draft packets into exact approval decisions for "
        "read-only browser validation and legal/payment review. No approval was requested or executed."
    )
    brief_next_action = (
        "User/operator must explicitly approve one or both decision items before any browser validation or legal/payment review; otherwise hold the lane locally."
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
        "schema_version": "agent_company.digital_products_local_operator_approval_brief.v1",
        "generated_utc": generated_utc,
        "brief_lane_id": lane_id,
        "brief_task_id": brief_task_id,
        "brief_evidence_id": brief_evidence_id,
        "source_drafts_task_id": source_drafts_task_id,
        "source_drafts_evidence_id": source_drafts_evidence_id,
        "source_drafts_validation_path": str(DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "approval_request_count": approval_request_count,
        "decision_item_count": len(decision_items),
        "explicit_approval_required_count": explicit_approval_required_count,
        "decision_items": decision_items,
        "source_draft_packet_count": len(draft_packets),
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": brief_summary,
        "next_action": brief_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Operator Approval Brief",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        brief_summary,
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        "## Decision Items",
        "",
    ]
    for item in decision_items:
        md_lines.extend(
            [
                f"### {item['decision_id']}",
                "",
                f"Source draft: `{item['source_draft_id']}`",
                f"Gate: `{item['gate_required']}`",
                f"Approval required: `{item['approval_required']}`",
                "",
                f"Draft approval text: {item['approval_text_draft']}",
                "",
                f"Default without approval: {item['default_without_approval']}",
                "",
                f"Operator note: {item['operator_review_note']}",
                "",
            ]
        )
    md_lines.extend(["## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a local briefing only. It does not submit approval requests, browse marketplaces, open accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            brief_next_action,
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
                brief_task_id,
                lane_id,
                "Prepare local digital-products operator approval brief",
                51,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                brief_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": brief_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local operator approval brief",
                "status": "local_operator_approval_brief_complete",
                "summary": brief_summary,
                "next_action": brief_next_action,
                "ownership_note": "Generated by platform_engineering from approval-request drafts; user/operator owns any explicit approval decision.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_brief = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (brief_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (brief_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (brief_task_id,)) else 0
    if task_rows_inserted_by_brief != 1:
        failures.append(f"expected 1 task row inserted by operator approval brief, got {task_rows_inserted_by_brief}")
    if tasks_table_rows_after != 187:
        failures.append(f"expected 187 task rows after operator approval brief, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 95:
        failures.append(f"expected 95 evidence rows after operator approval brief, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("operator approval brief evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during operator approval brief")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_brief": task_rows_inserted_by_brief,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_operator_approval_brief_validation.v1",
        "generated_utc": generated_utc,
        "brief_path": str(json_output_path),
        "brief_lane_id": lane_id,
        "brief_task_id": brief_task_id,
        "source_drafts_task_id": source_drafts_task_id,
        "source_drafts_evidence_id": source_drafts_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "decision_item_count": len(decision_items),
        "explicit_approval_required_count": explicit_approval_required_count,
        "approval_request_count": approval_request_count,
        "blocked_by_gate_count": len(blocked_questions),
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_brief": task_rows_inserted_by_brief,
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
                "brief_lane_id": lane_id,
                "brief_task_id": brief_task_id,
                "task_rows_inserted_by_brief": task_rows_inserted_by_brief,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
