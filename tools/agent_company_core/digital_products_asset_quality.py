from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Quality pass helpers and report writer for local digital products."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_JSON,
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_JSON,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .digital_products_asset_quality_content import (
    digital_products_quality_checks,
    digital_products_quality_revision_items,
)


def write_digital_products_local_quality_pass(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    quality_task_id = "task-digital-products-local-quality-pass-20260616"
    quality_evidence_id = "digital-products-local-quality-pass-20260616"
    source_draft_task_id = "task-digital-products-local-asset-draft-20260616"
    source_draft_evidence_id = "digital-products-local-asset-draft-20260616"
    duplicate_key = "digital-products-local-quality-pass-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "quality_pass_complete_ready_for_local_packaging_no_public_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_draft_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_draft_evidence_id,),
    ).fetchone()
    draft_validation = load_json(DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_VALIDATION_JSON)
    draft_payload = load_json(DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_JSON)
    draft_candidate_id = draft_payload.get("selected_candidate_id")
    blocked_questions = draft_payload.get("blocked_by_gate_questions", [])
    quality_checks = digital_products_quality_checks()
    revision_items = digital_products_quality_revision_items()
    passed_check_count = sum(1 for check in quality_checks if check["status"] == "pass")

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (quality_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    quality_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (quality_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source digital asset draft task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_asset_draft_complete":
        failures.append("source digital asset draft evidence is missing or not complete")
    if not draft_validation.get("all_checks_passed") or draft_validation.get("failure_count") != 0:
        failures.append("source digital asset draft validation is not clean")
    if draft_candidate_id != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {draft_candidate_id}")
    if len(quality_checks) != 8:
        failures.append(f"expected 8 quality checks, got {len(quality_checks)}")
    if passed_check_count != 8:
        failures.append(f"expected 8 passing checks, got {passed_check_count}")
    if len(revision_items) != 5:
        failures.append(f"expected 5 revision items, got {len(revision_items)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target quality pass task already exists: {quality_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if quality_evidence_exists_before:
        failures.append(f"quality pass evidence already exists: {quality_evidence_id}")
    if tasks_table_rows_before != 160:
        failures.append(f"expected 160 task rows before quality pass, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 81:
        failures.append(f"expected 81 evidence rows before quality pass, got {lane_evidence_rows_before}")

    quality_summary = (
        "Ran a local quality pass on the AI builder launch checklist pack draft. "
        "The draft passes eight local readiness checks and has five packaging revisions to complete before any marketplace or legal/payment gate is requested."
    )
    quality_next_action = (
        "Create a local packaging manifest and README revision for the draft; keep live marketplace, listing, account, legal, and payment validation gated."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_quality_pass.v1",
        "generated_utc": generated_utc,
        "quality_lane_id": lane_id,
        "quality_task_id": quality_task_id,
        "quality_evidence_id": quality_evidence_id,
        "source_draft_task_id": source_draft_task_id,
        "source_draft_evidence_id": source_draft_evidence_id,
        "source_draft_validation_path": str(DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "quality_check_count": len(quality_checks),
        "passed_check_count": passed_check_count,
        "quality_checks": quality_checks,
        "revision_item_count": len(revision_items),
        "revision_items": revision_items,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "local_decision": local_decision,
        "summary": quality_summary,
        "next_action": quality_next_action,
        "forbidden_actions": [
            "Do not publish, browse marketplaces, create seller accounts, accept terms, configure payouts, set prices, or claim live demand from this quality pass.",
            "Do not mutate service requests, assign/start workers, call APIs, touch wallets/payments, trade, submit, post, or create external side effects from this quality pass.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Quality Pass",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        quality_summary,
        "",
        "## Quality Checks",
        "",
        "| Check | Status | Finding |",
        "| --- | --- | --- |",
    ]
    for check in quality_checks:
        md_lines.append(f"| `{check['check_id']}` | `{check['status']}` | {check['finding']} |")
    md_lines.extend(["", "## Revision Items", "", "| Revision | Priority | Instruction |", "| --- | --- | --- |"])
    for item in revision_items:
        md_lines.append(f"| `{item['revision_id']}` | `{item['priority']}` | {item['instruction']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This quality pass is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            quality_next_action,
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
                quality_task_id,
                lane_id,
                "Run local digital-products asset quality pass",
                76,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                quality_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": quality_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local quality pass",
                "status": "local_quality_pass_complete",
                "summary": quality_summary,
                "next_action": quality_next_action,
                "ownership_note": "Generated by platform_engineering from the local asset draft; digital-products lane manager owns packaging-manifest follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_quality_pass = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (quality_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (quality_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (quality_task_id,)) else 0
    if task_rows_inserted_by_quality_pass != 1:
        failures.append(f"expected 1 task row inserted by quality pass, got {task_rows_inserted_by_quality_pass}")
    if tasks_table_rows_after != 161:
        failures.append(f"expected 161 task rows after quality pass, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 82:
        failures.append(f"expected 82 evidence rows after quality pass, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("quality pass evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during quality pass")
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
            "task_rows_inserted_by_quality_pass": task_rows_inserted_by_quality_pass,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_quality_pass_validation.v1",
        "generated_utc": generated_utc,
        "quality_path": str(json_output_path),
        "quality_lane_id": lane_id,
        "quality_task_id": quality_task_id,
        "source_draft_task_id": source_draft_task_id,
        "source_draft_evidence_id": source_draft_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "quality_check_count": len(quality_checks),
        "passed_check_count": passed_check_count,
        "revision_item_count": len(revision_items),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_quality_pass": task_rows_inserted_by_quality_pass,
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
                "quality_lane_id": lane_id,
                "quality_task_id": quality_task_id,
                "task_rows_inserted_by_quality_pass": task_rows_inserted_by_quality_pass,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
