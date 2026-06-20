from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Discovery, demand proof, and build brief writers for local digital-product work."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .digital_products_demand_memo_content import (
    digital_products_memo_candidates,
    digital_products_memo_sections,
)


def write_digital_products_local_demand_memo(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    memo_task_id = "task-digital-products-local-demand-memo-20260615"
    memo_evidence_id = "digital-products-local-demand-memo-20260615"
    source_proof_task_id = "task-digital_products_templates_plugins-first-local-proof-20260615"
    source_proof_evidence_id = "digital-products-local-demand-proof-20260615"
    duplicate_key = "digital-products-local-demand-memo-20260615"
    local_decision = "prepare_build_brief_no_live_marketplace_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_proof_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_proof_evidence_id,),
    ).fetchone()
    parked_requests = [
        dict(row)
        for row in conn.execute(
            """
            SELECT request_id, service_id, request_type, status, risk_gate, decision_note
            FROM service_requests
            WHERE lane_id = ? AND status = 'needs_review'
            ORDER BY request_id
            """,
            (lane_id,),
        )
    ]
    proof_validation = load_json(DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_VALIDATION_JSON)
    proof_payload = load_json(DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_JSON)
    proof_questions = proof_payload.get("questions", [])
    candidates = digital_products_memo_candidates()
    blocked_questions = [item for item in proof_questions if item.get("mode") == "blocked_by_gate"]
    memo_sections = digital_products_memo_sections()

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (memo_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    memo_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (memo_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source digital proof task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_proof_complete":
        failures.append("source digital proof evidence is missing or not complete")
    if not proof_validation.get("all_checks_passed") or proof_validation.get("failure_count") != 0:
        failures.append("source digital proof validation is not clean")
    if len(parked_requests) != 3:
        failures.append(f"expected 3 parked digital service requests, got {len(parked_requests)}")
    if len(memo_sections) != 6:
        failures.append(f"expected 6 memo sections, got {len(memo_sections)}")
    if len(candidates) != 3:
        failures.append(f"expected 3 memo candidates, got {len(candidates)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target memo task already exists: {memo_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if memo_evidence_exists_before:
        failures.append(f"memo evidence already exists: {memo_evidence_id}")
    if tasks_table_rows_before != 152:
        failures.append(f"expected 152 task rows before memo, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 77:
        failures.append(f"expected 77 evidence rows before memo, got {lane_evidence_rows_before}")

    memo_summary = (
        "Converted the local digital-products demand proof into a local demand memo with three candidate product shapes, "
        "six decision sections, and the same live-marketplace/legal/payment gates preserved."
    )
    memo_next_action = (
        "Prepare a local build brief for the strongest candidate; request marketplace/browser approval only if live demand comparison is needed."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_demand_memo.v1",
        "generated_utc": generated_utc,
        "memo_lane_id": lane_id,
        "memo_task_id": memo_task_id,
        "memo_evidence_id": memo_evidence_id,
        "source_proof_task_id": source_proof_task_id,
        "source_proof_evidence_id": source_proof_evidence_id,
        "source_proof_validation_path": str(DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_VALIDATION_JSON),
        "parked_service_request_count": len(parked_requests),
        "parked_service_requests": parked_requests,
        "memo_section_count": len(memo_sections),
        "memo_sections": memo_sections,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "local_decision": local_decision,
        "summary": memo_summary,
        "next_action": memo_next_action,
        "forbidden_actions": [
            "Do not browse marketplace pages, create seller accounts, accept terms, publish listings, or configure payouts from this memo.",
            "Do not mutate service requests, assign/start workers, call APIs, touch wallets/payments, trade, submit, post, or create external side effects from this memo.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Demand Memo",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        memo_summary,
        "",
        "## Candidate Products",
        "",
        "| Candidate | Shape | Buyer | Promise | Live validation needed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for candidate in candidates:
        md_lines.append(
            f"| `{candidate['candidate_id']}` | {candidate['product_shape']} | {candidate['buyer']} | {candidate['promise']} | {candidate['needs_live_validation']} |"
        )
    md_lines.extend(["", "## Memo Sections", "", "| Section | Summary |", "| --- | --- |"])
    for section in memo_sections:
        md_lines.append(f"| `{section['section_id']}` | {section['summary']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This memo is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            memo_next_action,
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
                memo_task_id,
                lane_id,
                "Draft local digital-products demand memo",
                84,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                memo_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": memo_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local demand memo",
                "status": "local_memo_complete",
                "summary": memo_summary,
                "next_action": memo_next_action,
                "ownership_note": "Generated by platform_engineering from the local demand proof; digital-products lane manager owns build-brief follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_memo = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (memo_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (memo_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (memo_task_id,)) else 0
    if task_rows_inserted_by_memo != 1:
        failures.append(f"expected 1 task row inserted by memo, got {task_rows_inserted_by_memo}")
    if tasks_table_rows_after != 153:
        failures.append(f"expected 153 task rows after memo, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 78:
        failures.append(f"expected 78 evidence rows after memo, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("memo evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during memo")
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
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_memo": task_rows_inserted_by_memo,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_demand_memo_validation.v1",
        "generated_utc": generated_utc,
        "memo_path": str(json_output_path),
        "memo_lane_id": lane_id,
        "memo_task_id": memo_task_id,
        "source_proof_task_id": source_proof_task_id,
        "source_proof_evidence_id": source_proof_evidence_id,
        "parked_service_request_count": len(parked_requests),
        "memo_section_count": len(memo_sections),
        "candidate_count": len(candidates),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_memo": task_rows_inserted_by_memo,
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
                "memo_lane_id": lane_id,
                "memo_task_id": memo_task_id,
                "task_rows_inserted_by_memo": task_rows_inserted_by_memo,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

