from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Local digital-products build brief report writer."""

from .digital_products_build_brief_content import (
    digital_products_build_brief_acceptance_criteria,
    digital_products_build_brief_deliverables,
    digital_products_build_brief_sections,
)
from .constants import (
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_JSON,
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_JSON,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar

def write_digital_products_local_build_brief(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    brief_task_id = "task-digital-products-local-build-brief-20260616"
    brief_evidence_id = "digital-products-local-build-brief-20260616"
    source_memo_task_id = "task-digital-products-local-demand-memo-20260615"
    source_memo_evidence_id = "digital-products-local-demand-memo-20260615"
    duplicate_key = "digital-products-local-build-brief-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "draft_assets_locally_no_listing_or_marketplace_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_memo_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_memo_evidence_id,),
    ).fetchone()
    memo_validation = load_json(DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_VALIDATION_JSON)
    memo_payload = load_json(DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_JSON)
    candidates = memo_payload.get("candidates", [])
    selected_candidates = [candidate for candidate in candidates if candidate.get("candidate_id") == selected_candidate_id]
    selected_candidate = selected_candidates[0] if selected_candidates else None
    blocked_questions = memo_payload.get("blocked_by_gate_questions", [])
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
    build_sections = digital_products_build_brief_sections()
    deliverables = digital_products_build_brief_deliverables()
    acceptance_criteria = digital_products_build_brief_acceptance_criteria()

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (brief_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    brief_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (brief_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source digital demand memo task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_memo_complete":
        failures.append("source digital demand memo evidence is missing or not complete")
    if not memo_validation.get("all_checks_passed") or memo_validation.get("failure_count") != 0:
        failures.append("source digital demand memo validation is not clean")
    if not selected_candidate:
        failures.append(f"selected candidate is missing from demand memo: {selected_candidate_id}")
    if len(parked_requests) != 3:
        failures.append(f"expected 3 parked digital service requests, got {len(parked_requests)}")
    if len(build_sections) != 7:
        failures.append(f"expected 7 build brief sections, got {len(build_sections)}")
    if len(deliverables) != 6:
        failures.append(f"expected 6 deliverables, got {len(deliverables)}")
    if len(acceptance_criteria) != 5:
        failures.append(f"expected 5 acceptance criteria, got {len(acceptance_criteria)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target build brief task already exists: {brief_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if brief_evidence_exists_before:
        failures.append(f"build brief evidence already exists: {brief_evidence_id}")
    if tasks_table_rows_before != 154:
        failures.append(f"expected 154 task rows before build brief, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 78:
        failures.append(f"expected 78 evidence rows before build brief, got {lane_evidence_rows_before}")

    brief_summary = (
        "Converted the strongest local digital-products memo candidate into a build brief for an AI builder launch checklist pack. "
        "The brief defines local draft assets, acceptance criteria, and preserved gates without browsing, listing, selling, or payment setup."
    )
    brief_next_action = (
        "Draft the local asset outline and first template for the AI builder launch checklist pack; request live marketplace/legal gates only after the local draft exists."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_build_brief.v1",
        "generated_utc": generated_utc,
        "brief_lane_id": lane_id,
        "brief_task_id": brief_task_id,
        "brief_evidence_id": brief_evidence_id,
        "source_memo_task_id": source_memo_task_id,
        "source_memo_evidence_id": source_memo_evidence_id,
        "source_memo_validation_path": str(DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "selected_candidate": selected_candidate,
        "parked_service_request_count": len(parked_requests),
        "parked_service_requests": parked_requests,
        "build_section_count": len(build_sections),
        "build_sections": build_sections,
        "deliverable_count": len(deliverables),
        "deliverables": deliverables,
        "acceptance_criterion_count": len(acceptance_criteria),
        "acceptance_criteria": acceptance_criteria,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "local_decision": local_decision,
        "summary": brief_summary,
        "next_action": brief_next_action,
        "forbidden_actions": [
            "Do not browse marketplace pages, create seller accounts, accept terms, publish listings, configure payouts, or set prices from this build brief.",
            "Do not mutate service requests, assign/start workers, call APIs, touch wallets/payments, trade, submit, post, or create external side effects from this build brief.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Build Brief",
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
        "## Selected Candidate",
        "",
        f"- Candidate: `{selected_candidate_id}`",
        f"- Buyer: {selected_candidate.get('buyer') if selected_candidate else ''}",
        f"- Promise: {selected_candidate.get('promise') if selected_candidate else ''}",
        "",
        "## Deliverables",
        "",
        "| Deliverable | Format | Description |",
        "| --- | --- | --- |",
    ]
    for deliverable in deliverables:
        md_lines.append(
            f"| `{deliverable['deliverable_id']}` | {deliverable['format']} | {deliverable['description']} |"
        )
    md_lines.extend(["", "## Build Sections", "", "| Section | Summary |", "| --- | --- |"])
    for section in build_sections:
        md_lines.append(f"| `{section['section_id']}` | {section['summary']} |")
    md_lines.extend(["", "## Acceptance Criteria", ""])
    md_lines.extend([f"- {criterion}" for criterion in acceptance_criteria])
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This build brief is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
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
                "Draft local digital-products build brief",
                82,
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
                "title": "Digital products local build brief",
                "status": "local_build_brief_complete",
                "summary": brief_summary,
                "next_action": brief_next_action,
                "ownership_note": "Generated by platform_engineering from the local demand memo; digital-products lane manager owns asset-outline follow-up.",
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
        failures.append(f"expected 1 task row inserted by build brief, got {task_rows_inserted_by_brief}")
    if tasks_table_rows_after != 155:
        failures.append(f"expected 155 task rows after build brief, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 79:
        failures.append(f"expected 79 evidence rows after build brief, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("build brief evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during build brief")
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
            "task_rows_inserted_by_brief": task_rows_inserted_by_brief,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_build_brief_validation.v1",
        "generated_utc": generated_utc,
        "brief_path": str(json_output_path),
        "brief_lane_id": lane_id,
        "brief_task_id": brief_task_id,
        "source_memo_task_id": source_memo_task_id,
        "source_memo_evidence_id": source_memo_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "parked_service_request_count": len(parked_requests),
        "build_section_count": len(build_sections),
        "deliverable_count": len(deliverables),
        "acceptance_criterion_count": len(acceptance_criteria),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
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

__all__ = [
    "digital_products_build_brief_acceptance_criteria",
    "digital_products_build_brief_deliverables",
    "digital_products_build_brief_sections",
    "write_digital_products_local_build_brief",
]
