from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Local digital-products private review decision writer."""

from .digital_products_review_private_decision_content import (
    digital_products_private_review_answers,
    digital_products_private_review_revision_items,
)
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

def write_digital_products_local_private_review_decision(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    decision_task_id = "task-digital-products-local-private-review-decision-20260616"
    decision_evidence_id = "digital-products-local-private-review-decision-20260616"
    source_packet_task_id = "task-digital-products-local-private-review-packet-20260616"
    source_packet_evidence_id = "digital-products-local-private-review-packet-20260616"
    duplicate_key = "digital-products-local-private-review-decision-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    selected_decision_id = "continue-local"
    local_decision = "continue_local_revision_queue_no_external_validation"
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
    packet_validation = load_json(DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_VALIDATION_JSON)
    packet_payload = load_json(DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_JSON)
    review_answers = digital_products_private_review_answers()
    revision_items = digital_products_private_review_revision_items()
    blocked_questions = packet_payload.get("blocked_by_gate_questions", [])
    decision_options = packet_payload.get("decision_options", [])

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (decision_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    decision_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (decision_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source private-review packet task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_private_review_packet_complete":
        failures.append("source private-review packet evidence is missing or not complete")
    if not packet_validation.get("all_checks_passed") or packet_validation.get("failure_count") != 0:
        failures.append("source private-review packet validation is not clean")
    if packet_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {packet_payload.get('selected_candidate_id')}")
    if selected_decision_id not in {option.get("decision_id") for option in decision_options}:
        failures.append(f"selected decision option is missing: {selected_decision_id}")
    if len(review_answers) != 8:
        failures.append(f"expected 8 review answers, got {len(review_answers)}")
    if len(revision_items) != 6:
        failures.append(f"expected 6 revision items, got {len(revision_items)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target private review decision task already exists: {decision_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if decision_evidence_exists_before:
        failures.append(f"private review decision evidence already exists: {decision_evidence_id}")
    if tasks_table_rows_before != 170:
        failures.append(f"expected 170 task rows before private review decision, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 86:
        failures.append(f"expected 86 evidence rows before private review decision, got {lane_evidence_rows_before}")

    decision_summary = (
        "Recorded the local private-review decision for the AI builder launch checklist pack. "
        "The lane continues locally with a six-item revision queue and keeps browser, marketplace, account, legal, payment, wallet, API, and public actions gated."
    )
    decision_next_action = (
        "Draft the local revision pass from the six-item queue, then rerun local package completeness; do not browse, publish, list, price, create accounts, or configure payouts."
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
        "schema_version": "agent_company.digital_products_local_private_review_decision.v1",
        "generated_utc": generated_utc,
        "decision_lane_id": lane_id,
        "decision_task_id": decision_task_id,
        "decision_evidence_id": decision_evidence_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "source_packet_validation_path": str(DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_PACKET_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "selected_decision_id": selected_decision_id,
        "local_decision": local_decision,
        "review_answer_count": len(review_answers),
        "review_answers": review_answers,
        "revision_item_count": len(revision_items),
        "revision_items": revision_items,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": decision_summary,
        "next_action": decision_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Private Review Decision",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{selected_decision_id}`: `{local_decision}`",
        "",
        decision_summary,
        "",
        "## Review Answers",
        "",
        "| Question | Decision effect | Answer |",
        "| --- | --- | --- |",
    ]
    for answer in review_answers:
        md_lines.append(f"| `{answer['question_id']}` | `{answer['decision_effect']}` | {answer['answer']} |")
    md_lines.extend(["", "## Revision Queue", "", "| Revision | Target | Action | Reason |", "| --- | --- | --- | --- |"])
    for item in revision_items:
        md_lines.append(f"| `{item['revision_id']}` | `{item['artifact_target']}` | {item['action']} | {item['reason']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This decision is local only. It chooses continued local refinement and does not browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            decision_next_action,
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
                decision_task_id,
                lane_id,
                "Record local digital-products private review decision",
                66,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                decision_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": decision_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local private review decision",
                "status": "local_private_review_decision_complete",
                "summary": decision_summary,
                "next_action": decision_next_action,
                "ownership_note": "Generated by platform_engineering from local private-review packet; digital-products lane manager owns local revision follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_decision = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (decision_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (decision_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (decision_task_id,)) else 0
    if task_rows_inserted_by_decision != 1:
        failures.append(f"expected 1 task row inserted by private review decision, got {task_rows_inserted_by_decision}")
    if tasks_table_rows_after != 171:
        failures.append(f"expected 171 task rows after private review decision, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 87:
        failures.append(f"expected 87 evidence rows after private review decision, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("private review decision evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during private review decision")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_decision": task_rows_inserted_by_decision,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_private_review_decision_validation.v1",
        "generated_utc": generated_utc,
        "decision_path": str(json_output_path),
        "decision_lane_id": lane_id,
        "decision_task_id": decision_task_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "selected_decision_id": selected_decision_id,
        "local_decision": local_decision,
        "review_answer_count": len(review_answers),
        "revision_item_count": len(revision_items),
        "blocked_by_gate_count": len(blocked_questions),
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_decision": task_rows_inserted_by_decision,
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
                "decision_lane_id": lane_id,
                "decision_task_id": decision_task_id,
                "task_rows_inserted_by_decision": task_rows_inserted_by_decision,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

__all__ = [
    "digital_products_private_review_answers",
    "digital_products_private_review_revision_items",
    "write_digital_products_local_private_review_decision",
]
