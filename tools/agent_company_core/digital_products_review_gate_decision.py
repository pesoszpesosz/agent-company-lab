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


def digital_products_gate_decision_options() -> list[dict[str, object]]:
    return [
        {
            "option_id": "continue-local",
            "requires_approval": False,
            "gate_required": None,
            "rationale": "Best immediate path because revised local completeness is clean, but live demand, seller terms, and payment constraints remain unverified.",
            "allowed_next_action": "Draft another local refinement or prepare a future approval request packet without browsing or submitting.",
        },
        {
            "option_id": "request-read-only-browser",
            "requires_approval": True,
            "gate_required": "browser_read_only_session",
            "rationale": "Useful later to compare public marketplace demand, saturation, price bands, and buyer language.",
            "allowed_next_action": "Ask the user for explicit read-only browser approval before opening marketplace or public category pages.",
        },
        {
            "option_id": "request-legal-payment-review",
            "requires_approval": True,
            "gate_required": "legal_kyc_tax_payment",
            "rationale": "Needed before seller terms, tax/KYC, refunds, platform fees, payment setup, or payout configuration.",
            "allowed_next_action": "Ask the user for explicit legal/payment review approval; do not accept terms or configure payouts.",
        },
        {
            "option_id": "pause-candidate",
            "requires_approval": False,
            "gate_required": None,
            "rationale": "Appropriate if the lane should move attention to another candidate before spending approval budget.",
            "allowed_next_action": "Record a pause reason and return to local digital-products candidate discovery.",
        },
    ]


def write_digital_products_local_gate_decision_packet(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_GATE_DECISION_PACKET_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    packet_task_id = "task-digital-products-local-gate-decision-packet-20260616"
    packet_evidence_id = "digital-products-local-gate-decision-packet-20260616"
    source_check_task_id = "task-digital-products-local-revised-completeness-20260616"
    source_check_evidence_id = "digital-products-local-revised-completeness-20260616"
    duplicate_key = "digital-products-local-gate-decision-packet-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    recommended_option_id = "continue-local"
    local_decision = "gate_decision_packet_ready_no_gate_requested"
    approval_request_count = 0
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_check_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_check_evidence_id,),
    ).fetchone()
    check_validation = load_json(DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_VALIDATION_JSON)
    check_payload = load_json(DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_JSON)
    gate_options = digital_products_gate_decision_options()
    blocked_questions = check_payload.get("blocked_by_gate_questions", [])

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    packet_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source revised-completeness task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_revised_completeness_complete":
        failures.append("source revised-completeness evidence is missing or not complete")
    if not check_validation.get("all_checks_passed") or check_validation.get("failure_count") != 0:
        failures.append("source revised-completeness validation is not clean")
    if check_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {check_payload.get('selected_candidate_id')}")
    if len(gate_options) != 4:
        failures.append(f"expected 4 gate options, got {len(gate_options)}")
    if recommended_option_id not in {option.get("option_id") for option in gate_options}:
        failures.append(f"recommended option is missing: {recommended_option_id}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target gate-decision packet task already exists: {packet_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if packet_evidence_exists_before:
        failures.append(f"gate-decision packet evidence already exists: {packet_evidence_id}")
    if tasks_table_rows_before != 176:
        failures.append(f"expected 176 task rows before gate-decision packet, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 89:
        failures.append(f"expected 89 evidence rows before gate-decision packet, got {lane_evidence_rows_before}")

    packet_summary = (
        "Prepared a local gate-decision packet for the revised AI builder launch checklist pack. "
        "The packet compares four next-step options and recommends continue-local while making no approval request and taking no external action."
    )
    packet_next_action = (
        "Choose whether to continue local refinement, request read-only browser approval, request legal/payment review, or pause; no gate is requested or exercised by this packet."
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
        "schema_version": "agent_company.digital_products_local_gate_decision_packet.v1",
        "generated_utc": generated_utc,
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "packet_evidence_id": packet_evidence_id,
        "source_check_task_id": source_check_task_id,
        "source_check_evidence_id": source_check_evidence_id,
        "source_check_validation_path": str(DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_option_id": recommended_option_id,
        "approval_request_count": approval_request_count,
        "gate_option_count": len(gate_options),
        "gate_options": gate_options,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": packet_summary,
        "next_action": packet_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Gate Decision Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        packet_summary,
        "",
        "## Options",
        "",
        "| Option | Requires approval | Gate | Rationale | Allowed next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for option in gate_options:
        md_lines.append(
            f"| `{option['option_id']}` | `{option['requires_approval']}` | `{option['gate_required']}` | {option['rationale']} | {option['allowed_next_action']} |"
        )
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is local only. It does not request approval, browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            packet_next_action,
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
                packet_task_id,
                lane_id,
                "Prepare local digital-products gate-decision packet",
                60,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                packet_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": packet_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local gate-decision packet",
                "status": "local_gate_decision_packet_complete",
                "summary": packet_summary,
                "next_action": packet_next_action,
                "ownership_note": "Generated by platform_engineering from revised local completeness; digital-products lane manager owns any explicit future gate request.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_packet = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (packet_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (packet_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (packet_task_id,)) else 0
    if task_rows_inserted_by_packet != 1:
        failures.append(f"expected 1 task row inserted by gate-decision packet, got {task_rows_inserted_by_packet}")
    if tasks_table_rows_after != 177:
        failures.append(f"expected 177 task rows after gate-decision packet, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 90:
        failures.append(f"expected 90 evidence rows after gate-decision packet, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("gate-decision packet evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during gate-decision packet")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_gate_decision_packet_validation.v1",
        "generated_utc": generated_utc,
        "packet_path": str(json_output_path),
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "source_check_task_id": source_check_task_id,
        "source_check_evidence_id": source_check_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "gate_option_count": len(gate_options),
        "recommended_option_id": recommended_option_id,
        "approval_request_count": approval_request_count,
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
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
                "packet_lane_id": lane_id,
                "packet_task_id": packet_task_id,
                "task_rows_inserted_by_packet": task_rows_inserted_by_packet,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
