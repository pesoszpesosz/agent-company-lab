from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Local digital-products revision pass writer."""

from .digital_products_review_revision_pass_content import digital_products_revision_pass_files
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

def write_digital_products_local_revision_pass(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    revision_task_id = "task-digital-products-local-revision-pass-20260616"
    revision_evidence_id = "digital-products-local-revision-pass-20260616"
    source_decision_task_id = "task-digital-products-local-private-review-decision-20260616"
    source_decision_evidence_id = "digital-products-local-private-review-decision-20260616"
    duplicate_key = "digital-products-local-revision-pass-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    selected_decision_id = "continue-local"
    local_decision = "revision_pass_ready_for_local_completeness_check"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_decision_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_decision_evidence_id,),
    ).fetchone()
    decision_validation = load_json(DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_VALIDATION_JSON)
    decision_payload = load_json(DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_JSON)
    revision_items = decision_payload.get("revision_items", [])
    blocked_questions = decision_payload.get("blocked_by_gate_questions", [])
    revised_files = digital_products_revision_pass_files()

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (revision_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    revision_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (revision_evidence_id,))
    all_text = "\n".join(
        section
        for file_payload in revised_files
        for section in file_payload.get("content_sections", [])
        if isinstance(section, str)
    ).lower()
    boundary_terms = ["marketplace", "account", "legal", "tax", "kyc", "payout", "publishing"]
    boundary_phrase_count = sum(1 for term in boundary_terms if term in all_text)
    placeholder_stub_count = all_text.count("placeholder stub")
    filled_example_count = sum(1 for file_payload in revised_files if file_payload.get("file_id") == "filled-example")

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source private-review decision task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_private_review_decision_complete":
        failures.append("source private-review decision evidence is missing or not complete")
    if not decision_validation.get("all_checks_passed") or decision_validation.get("failure_count") != 0:
        failures.append("source private-review decision validation is not clean")
    if decision_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {decision_payload.get('selected_candidate_id')}")
    if decision_payload.get("selected_decision_id") != selected_decision_id:
        failures.append(f"expected selected decision {selected_decision_id}, got {decision_payload.get('selected_decision_id')}")
    if len(revision_items) != 6:
        failures.append(f"expected 6 source revision items, got {len(revision_items)}")
    if len(revised_files) != 6:
        failures.append(f"expected 6 revised files, got {len(revised_files)}")
    if filled_example_count != 1:
        failures.append(f"expected 1 filled example, got {filled_example_count}")
    if boundary_phrase_count != 7:
        failures.append(f"expected 7 boundary phrases, got {boundary_phrase_count}")
    if placeholder_stub_count != 0:
        failures.append(f"expected 0 placeholder stubs, got {placeholder_stub_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target revision pass task already exists: {revision_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if revision_evidence_exists_before:
        failures.append(f"revision pass evidence already exists: {revision_evidence_id}")
    if tasks_table_rows_before != 172:
        failures.append(f"expected 172 task rows before revision pass, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 87:
        failures.append(f"expected 87 evidence rows before revision pass, got {lane_evidence_rows_before}")

    revision_summary = (
        "Drafted the local revision pass for the AI builder launch checklist pack. "
        "The pass turns the six private-review revision items into six local package file drafts, including one filled example and repeated gate language."
    )
    revision_next_action = (
        "Run a local revised-package completeness check against these six files; do not browse, publish, list, price, create accounts, configure payouts, or request external validation."
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
        "schema_version": "agent_company.digital_products_local_revision_pass.v1",
        "generated_utc": generated_utc,
        "revision_lane_id": lane_id,
        "revision_task_id": revision_task_id,
        "revision_evidence_id": revision_evidence_id,
        "source_decision_task_id": source_decision_task_id,
        "source_decision_evidence_id": source_decision_evidence_id,
        "source_decision_validation_path": str(DIGITAL_PRODUCTS_LOCAL_PRIVATE_REVIEW_DECISION_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "selected_decision_id": selected_decision_id,
        "local_decision": local_decision,
        "revision_item_count": len(revision_items),
        "revision_items": revision_items,
        "revised_file_count": len(revised_files),
        "revised_files": revised_files,
        "filled_example_count": filled_example_count,
        "boundary_phrase_count": boundary_phrase_count,
        "placeholder_stub_count": placeholder_stub_count,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": revision_summary,
        "next_action": revision_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Revision Pass",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        revision_summary,
        "",
        "## Revised Files",
        "",
    ]
    for file_payload in revised_files:
        md_lines.extend(
            [
                f"### {file_payload['filename']}",
                "",
                f"Revision sources: {', '.join(file_payload['revision_sources'])}",
                "",
            ]
        )
        for section in file_payload["content_sections"]:
            md_lines.append(f"- {section}")
        md_lines.append("")
    md_lines.extend(["## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This revision pass is local only. It does not browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
            "",
            "## Next Action",
            "",
            revision_next_action,
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
                revision_task_id,
                lane_id,
                "Draft local digital-products revision pass",
                64,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                revision_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": revision_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local revision pass",
                "status": "local_revision_pass_complete",
                "summary": revision_summary,
                "next_action": revision_next_action,
                "ownership_note": "Generated by platform_engineering from the private-review decision; digital-products lane manager owns the local completeness follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_revision = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (revision_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (revision_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (revision_task_id,)) else 0
    if task_rows_inserted_by_revision != 1:
        failures.append(f"expected 1 task row inserted by revision pass, got {task_rows_inserted_by_revision}")
    if tasks_table_rows_after != 173:
        failures.append(f"expected 173 task rows after revision pass, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 88:
        failures.append(f"expected 88 evidence rows after revision pass, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("revision pass evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during revision pass")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_revision": task_rows_inserted_by_revision,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_revision_pass_validation.v1",
        "generated_utc": generated_utc,
        "revision_path": str(json_output_path),
        "revision_lane_id": lane_id,
        "revision_task_id": revision_task_id,
        "source_decision_task_id": source_decision_task_id,
        "source_decision_evidence_id": source_decision_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "selected_decision_id": selected_decision_id,
        "local_decision": local_decision,
        "revision_item_count": len(revision_items),
        "revised_file_count": len(revised_files),
        "filled_example_count": filled_example_count,
        "boundary_phrase_count": boundary_phrase_count,
        "placeholder_stub_count": placeholder_stub_count,
        "blocked_by_gate_count": len(blocked_questions),
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_revision": task_rows_inserted_by_revision,
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
                "revision_lane_id": lane_id,
                "revision_task_id": revision_task_id,
                "task_rows_inserted_by_revision": task_rows_inserted_by_revision,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

__all__ = [
    "digital_products_revision_pass_files",
    "write_digital_products_local_revision_pass",
]
