from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Private review, revision, gate decision, and gate choice writers."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT,
    DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_REPORT,
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_JSON,
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_REPORT,
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_REPORT,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_REPORT,
    DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_JSON,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_JSON,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_JSON,
    DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_JSON,
    DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_VALIDATION_JSON,
    SERVICE_WORKER_CHAIN_INTEGRITY_REPORT,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def digital_products_gate_choice_followup_items() -> list[dict[str, str]]:
    return [
        {
            "followup_id": "tighten-local-copy",
            "action": "Create one local copy-polish pass over README, checklist, filled example, QA checklist, private listing draft, and scorecard.",
            "reason": "Continue-local is the cheapest next move while live marketplace and seller constraints remain gated.",
        },
        {
            "followup_id": "prepare-future-browser-request",
            "action": "Draft a separate read-only browser approval request packet, but do not open marketplaces or public pages.",
            "reason": "Keeps the possible demand-validation path explicit without exercising the browser gate.",
        },
        {
            "followup_id": "prepare-future-legal-payment-request",
            "action": "Draft a separate legal/payment review request packet, but do not accept terms, create accounts, or configure payouts.",
            "reason": "Keeps seller-term and payout risk visible without exercising legal or payment gates.",
        },
    ]


def write_digital_products_local_gate_choice(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    choice_task_id = "task-digital-products-local-gate-choice-20260616"
    choice_evidence_id = "digital-products-local-gate-choice-20260616"
    source_packet_task_id = "task-digital-products-local-gate-decision-packet-20260616"
    source_packet_evidence_id = "digital-products-local-gate-decision-packet-20260616"
    duplicate_key = "digital-products-local-gate-choice-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    selected_option_id = "continue-local"
    local_decision = "continue_local_no_gate_exercised"
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_packet_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_packet_evidence_id,),
    ).fetchone()
    packet_validation = load_json(DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_VALIDATION_JSON)
    packet_payload = load_json(DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_JSON)
    gate_options = packet_payload.get("gate_options", [])
    blocked_questions = packet_payload.get("blocked_by_gate_questions", [])
    followup_items = digital_products_gate_choice_followup_items()
    selected_option = next((option for option in gate_options if option.get("option_id") == selected_option_id), None)

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (choice_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    choice_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (choice_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source gate-decision packet task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_gate_decision_packet_complete":
        failures.append("source gate-decision packet evidence is missing or not complete")
    if not packet_validation.get("all_checks_passed") or packet_validation.get("failure_count") != 0:
        failures.append("source gate-decision packet validation is not clean")
    if packet_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {packet_payload.get('selected_candidate_id')}")
    if packet_payload.get("recommended_option_id") != selected_option_id:
        failures.append(f"expected recommended option {selected_option_id}, got {packet_payload.get('recommended_option_id')}")
    if not selected_option or selected_option.get("requires_approval"):
        failures.append("selected continue-local option is missing or unexpectedly requires approval")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if len(followup_items) != 3:
        failures.append(f"expected 3 follow-up items, got {len(followup_items)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target gate-choice task already exists: {choice_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if choice_evidence_exists_before:
        failures.append(f"gate-choice evidence already exists: {choice_evidence_id}")
    if tasks_table_rows_before != 178:
        failures.append(f"expected 178 task rows before gate choice, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 90:
        failures.append(f"expected 90 evidence rows before gate choice, got {lane_evidence_rows_before}")

    choice_summary = (
        "Recorded the local gate choice for the revised AI builder launch checklist pack. "
        "The lane selects continue-local, creates no approval request, and keeps browser, marketplace, legal, payment, account, wallet, API, and public actions gated."
    )
    choice_next_action = (
        "Run a local copy-polish pass on the revised package and optionally draft separate future approval-request packets without exercising any gate."
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
        "schema_version": "agent_company.digital_products_local_gate_choice.v1",
        "generated_utc": generated_utc,
        "choice_lane_id": lane_id,
        "choice_task_id": choice_task_id,
        "choice_evidence_id": choice_evidence_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "source_packet_validation_path": str(DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "selected_option_id": selected_option_id,
        "selected_option": selected_option,
        "approval_request_count": approval_request_count,
        "local_decision": local_decision,
        "followup_item_count": len(followup_items),
        "followup_items": followup_items,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": choice_summary,
        "next_action": choice_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Gate Choice",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Choice",
        "",
        f"`{selected_option_id}`: `{local_decision}`",
        "",
        choice_summary,
        "",
        "## Follow-Up Items",
        "",
        "| Follow-up | Action | Reason |",
        "| --- | --- | --- |",
    ]
    for item in followup_items:
        md_lines.append(f"| `{item['followup_id']}` | {item['action']} | {item['reason']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This choice is local only. It does not request approval, browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            choice_next_action,
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
                choice_task_id,
                lane_id,
                "Record local digital-products gate choice",
                58,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                choice_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": choice_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local gate choice",
                "status": "local_gate_choice_complete",
                "summary": choice_summary,
                "next_action": choice_next_action,
                "ownership_note": "Generated by platform_engineering from the local gate-decision packet; digital-products lane manager owns local follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_choice = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (choice_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (choice_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (choice_task_id,)) else 0
    if task_rows_inserted_by_choice != 1:
        failures.append(f"expected 1 task row inserted by gate choice, got {task_rows_inserted_by_choice}")
    if tasks_table_rows_after != 179:
        failures.append(f"expected 179 task rows after gate choice, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 91:
        failures.append(f"expected 91 evidence rows after gate choice, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("gate-choice evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during gate choice")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_choice": task_rows_inserted_by_choice,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_gate_choice_validation.v1",
        "generated_utc": generated_utc,
        "choice_path": str(json_output_path),
        "choice_lane_id": lane_id,
        "choice_task_id": choice_task_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "selected_option_id": selected_option_id,
        "approval_request_count": approval_request_count,
        "followup_item_count": len(followup_items),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_choice": task_rows_inserted_by_choice,
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
                "choice_lane_id": lane_id,
                "choice_task_id": choice_task_id,
                "task_rows_inserted_by_choice": task_rows_inserted_by_choice,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
