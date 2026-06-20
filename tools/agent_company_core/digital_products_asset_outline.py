from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Asset outline and draft helpers and report writers for local digital products."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_JSON,
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT,
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_JSON,
    DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_REPORT,
    DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_JSON,
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .digital_products_asset_outline_content import (
    digital_products_asset_outline_components,
    digital_products_positioning_template_fields,
    digital_products_sample_positioning_sections,
)


def write_digital_products_local_asset_outline(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    outline_task_id = "task-digital-products-local-asset-outline-20260616"
    outline_evidence_id = "digital-products-local-asset-outline-20260616"
    source_brief_task_id = "task-digital-products-local-build-brief-20260616"
    source_brief_evidence_id = "digital-products-local-build-brief-20260616"
    duplicate_key = "digital-products-local-asset-outline-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "draft_first_template_locally_no_marketplace_or_payment_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_brief_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_brief_evidence_id,),
    ).fetchone()
    brief_validation = load_json(DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_VALIDATION_JSON)
    brief_payload = load_json(DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_JSON)
    brief_candidate_id = brief_payload.get("selected_candidate_id")
    blocked_questions = brief_payload.get("blocked_by_gate_questions", [])
    components = digital_products_asset_outline_components()
    template_fields = digital_products_positioning_template_fields()
    sample_sections = digital_products_sample_positioning_sections()

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (outline_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    outline_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (outline_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source digital build brief task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_build_brief_complete":
        failures.append("source digital build brief evidence is missing or not complete")
    if not brief_validation.get("all_checks_passed") or brief_validation.get("failure_count") != 0:
        failures.append("source digital build brief validation is not clean")
    if brief_candidate_id != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {brief_candidate_id}")
    if len(components) != 6:
        failures.append(f"expected 6 asset components, got {len(components)}")
    if len(template_fields) != 10:
        failures.append(f"expected 10 template fields, got {len(template_fields)}")
    if len(sample_sections) != 5:
        failures.append(f"expected 5 sample template sections, got {len(sample_sections)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target asset outline task already exists: {outline_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if outline_evidence_exists_before:
        failures.append(f"asset outline evidence already exists: {outline_evidence_id}")
    if tasks_table_rows_before != 156:
        failures.append(f"expected 156 task rows before asset outline, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 79:
        failures.append(f"expected 79 evidence rows before asset outline, got {lane_evidence_rows_before}")

    outline_summary = (
        "Drafted a local asset outline and first fillable positioning template for the AI builder launch checklist pack. "
        "The outline defines six local components, ten positioning fields, and five sample filled sections while preserving all live-marketplace and payment gates."
    )
    outline_next_action = (
        "Create the local markdown asset draft for the positioning template and launch checklist; do not publish, list, price, browse marketplaces, or configure payouts."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_asset_outline.v1",
        "generated_utc": generated_utc,
        "outline_lane_id": lane_id,
        "outline_task_id": outline_task_id,
        "outline_evidence_id": outline_evidence_id,
        "source_brief_task_id": source_brief_task_id,
        "source_brief_evidence_id": source_brief_evidence_id,
        "source_brief_validation_path": str(DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "asset_component_count": len(components),
        "asset_components": components,
        "template_field_count": len(template_fields),
        "template_fields": template_fields,
        "sample_template_section_count": len(sample_sections),
        "sample_template_sections": sample_sections,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "local_decision": local_decision,
        "summary": outline_summary,
        "next_action": outline_next_action,
        "forbidden_actions": [
            "Do not browse marketplaces, create seller accounts, accept terms, publish listings, configure payouts, set prices, or claim live demand from this outline.",
            "Do not mutate service requests, assign/start workers, call APIs, touch wallets/payments, trade, submit, post, or create external side effects from this outline.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Asset Outline",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        outline_summary,
        "",
        "## Asset Components",
        "",
        "| Component | Title | Purpose |",
        "| --- | --- | --- |",
    ]
    for component in components:
        md_lines.append(f"| `{component['component_id']}` | {component['title']} | {component['purpose']} |")
    md_lines.extend(["", "## Positioning Template Fields", "", "| Field | Prompt |", "| --- | --- |"])
    for field in template_fields:
        md_lines.append(f"| `{field['field_id']}` | {field['prompt']} |")
    md_lines.extend(["", "## Sample Filled Sections", "", "| Section | Sample text |", "| --- | --- |"])
    for section in sample_sections:
        md_lines.append(f"| `{section['section_id']}` | {section['sample_text']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This asset outline is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            outline_next_action,
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
                outline_task_id,
                lane_id,
                "Draft local digital-products asset outline",
                80,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                outline_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": outline_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local asset outline",
                "status": "local_asset_outline_complete",
                "summary": outline_summary,
                "next_action": outline_next_action,
                "ownership_note": "Generated by platform_engineering from the local build brief; digital-products lane manager owns local asset-draft follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_outline = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (outline_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (outline_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (outline_task_id,)) else 0
    if task_rows_inserted_by_outline != 1:
        failures.append(f"expected 1 task row inserted by asset outline, got {task_rows_inserted_by_outline}")
    if tasks_table_rows_after != 157:
        failures.append(f"expected 157 task rows after asset outline, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 80:
        failures.append(f"expected 80 evidence rows after asset outline, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("asset outline evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during asset outline")
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
            "task_rows_inserted_by_outline": task_rows_inserted_by_outline,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_asset_outline_validation.v1",
        "generated_utc": generated_utc,
        "outline_path": str(json_output_path),
        "outline_lane_id": lane_id,
        "outline_task_id": outline_task_id,
        "source_brief_task_id": source_brief_task_id,
        "source_brief_evidence_id": source_brief_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "asset_component_count": len(components),
        "template_field_count": len(template_fields),
        "sample_template_section_count": len(sample_sections),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_outline": task_rows_inserted_by_outline,
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
                "outline_lane_id": lane_id,
                "outline_task_id": outline_task_id,
                "task_rows_inserted_by_outline": task_rows_inserted_by_outline,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
