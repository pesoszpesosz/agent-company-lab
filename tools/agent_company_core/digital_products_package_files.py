from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Local digital-products package files report writer."""

from .digital_products_package_files_content import (
    digital_products_post_launch_prompts,
    digital_products_qa_rows,
    digital_products_screenshot_rows,
)
from .constants import (
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_JSON,
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_REPORT,
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_JSON,
    DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_JSON,
    DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_JSON,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar

def write_digital_products_local_package_files(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    files_task_id = "task-digital-products-local-package-files-20260616"
    files_evidence_id = "digital-products-local-package-files-20260616"
    source_manifest_task_id = "task-digital-products-local-packaging-manifest-20260616"
    source_manifest_evidence_id = "digital-products-local-packaging-manifest-20260616"
    duplicate_key = "digital-products-local-package-files-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "local_package_files_drafted_no_distribution_or_payment_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_manifest_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_manifest_evidence_id,),
    ).fetchone()
    manifest_validation = load_json(DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_VALIDATION_JSON)
    manifest_payload = load_json(DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_JSON)
    manifest_candidate_id = manifest_payload.get("selected_candidate_id")
    blocked_questions = manifest_payload.get("blocked_by_gate_questions", [])
    readme_sections = manifest_payload.get("readme_sections", [])
    screenshot_rows = digital_products_screenshot_rows()
    qa_rows = digital_products_qa_rows()
    review_prompts = digital_products_post_launch_prompts()
    drafted_files = [
        {"file_id": "README.md", "section_count": len(readme_sections), "status": "drafted_locally"},
        {"file_id": "screenshot-shotlist.md", "row_count": len(screenshot_rows), "status": "drafted_locally"},
        {"file_id": "qa-pass.md", "row_count": len(qa_rows), "status": "drafted_locally"},
        {"file_id": "post-launch-review.md", "prompt_count": len(review_prompts), "status": "drafted_locally"},
    ]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (files_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    files_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (files_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source digital packaging manifest task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_packaging_manifest_complete":
        failures.append("source digital packaging manifest evidence is missing or not complete")
    if not manifest_validation.get("all_checks_passed") or manifest_validation.get("failure_count") != 0:
        failures.append("source digital packaging manifest validation is not clean")
    if manifest_candidate_id != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {manifest_candidate_id}")
    if len(drafted_files) != 4:
        failures.append(f"expected 4 drafted files, got {len(drafted_files)}")
    if len(readme_sections) != 7:
        failures.append(f"expected 7 README sections, got {len(readme_sections)}")
    if len(screenshot_rows) != 6:
        failures.append(f"expected 6 screenshot rows, got {len(screenshot_rows)}")
    if len(qa_rows) != 7:
        failures.append(f"expected 7 QA rows, got {len(qa_rows)}")
    if len(review_prompts) != 6:
        failures.append(f"expected 6 review prompts, got {len(review_prompts)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target package files task already exists: {files_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if files_evidence_exists_before:
        failures.append(f"package files evidence already exists: {files_evidence_id}")
    if tasks_table_rows_before != 164:
        failures.append(f"expected 164 task rows before package files, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 83:
        failures.append(f"expected 83 evidence rows before package files, got {lane_evidence_rows_before}")

    files_summary = (
        "Drafted four remaining local package files for the AI builder launch checklist pack: README, screenshot shot list, QA pass, and post-launch review. "
        "The draft remains private and local, with marketplace validation, distribution, accounts, pricing, and payouts gated."
    )
    files_next_action = (
        "Run a local package completeness check across all six manifest files; do not distribute, list, price, browse marketplaces, create accounts, or configure payouts."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_package_files.v1",
        "generated_utc": generated_utc,
        "files_lane_id": lane_id,
        "files_task_id": files_task_id,
        "files_evidence_id": files_evidence_id,
        "source_manifest_task_id": source_manifest_task_id,
        "source_manifest_evidence_id": source_manifest_evidence_id,
        "source_manifest_validation_path": str(DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "drafted_file_count": len(drafted_files),
        "drafted_files": drafted_files,
        "readme_section_count": len(readme_sections),
        "readme_sections": readme_sections,
        "screenshot_row_count": len(screenshot_rows),
        "screenshot_rows": screenshot_rows,
        "qa_row_count": len(qa_rows),
        "qa_rows": qa_rows,
        "review_prompt_count": len(review_prompts),
        "review_prompts": review_prompts,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "local_decision": local_decision,
        "summary": files_summary,
        "next_action": files_next_action,
        "forbidden_actions": [
            "Do not distribute, publish, browse marketplaces, create seller accounts, accept terms, configure payouts, set prices, or claim live demand from these package files.",
            "Do not mutate service requests, assign/start workers, call APIs, touch wallets/payments, trade, submit, post, or create external side effects from these package files.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Package Files",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        files_summary,
        "",
        "## README.md",
        "",
        "| Section | Content |",
        "| --- | --- |",
    ]
    for section in readme_sections:
        md_lines.append(f"| `{section['section_id']}` | {section['content']} |")
    md_lines.extend(["", "## screenshot-shotlist.md", "", "| Shot | State | Caption | Status |", "| --- | --- | --- | --- |"])
    for row in screenshot_rows:
        md_lines.append(f"| `{row['shot_id']}` | {row['state']} | {row['caption']} | `{row['status']}` |")
    md_lines.extend(["", "## qa-pass.md", "", "| Area | Check | Status |", "| --- | --- | --- |"])
    for row in qa_rows:
        md_lines.append(f"| `{row['area']}` | {row['check']} | `{row['status']}` |")
    md_lines.extend(["", "## post-launch-review.md", "", "| Prompt | Text |", "| --- | --- |"])
    for prompt in review_prompts:
        md_lines.append(f"| `{prompt['prompt_id']}` | {prompt['prompt']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These package files are local only. They create and complete one local coordination task and add one local evidence row; they do not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            files_next_action,
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
                files_task_id,
                lane_id,
                "Draft local digital-products package files",
                72,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                files_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": files_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local package files",
                "status": "local_package_files_complete",
                "summary": files_summary,
                "next_action": files_next_action,
                "ownership_note": "Generated by platform_engineering from the local packaging manifest; digital-products lane manager owns completeness-check follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_files = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (files_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (files_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (files_task_id,)) else 0
    if task_rows_inserted_by_files != 1:
        failures.append(f"expected 1 task row inserted by package files, got {task_rows_inserted_by_files}")
    if tasks_table_rows_after != 165:
        failures.append(f"expected 165 task rows after package files, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 84:
        failures.append(f"expected 84 evidence rows after package files, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("package files evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during package files")
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
            "task_rows_inserted_by_files": task_rows_inserted_by_files,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_package_files_validation.v1",
        "generated_utc": generated_utc,
        "files_path": str(json_output_path),
        "files_lane_id": lane_id,
        "files_task_id": files_task_id,
        "source_manifest_task_id": source_manifest_task_id,
        "source_manifest_evidence_id": source_manifest_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "drafted_file_count": len(drafted_files),
        "readme_section_count": len(readme_sections),
        "screenshot_row_count": len(screenshot_rows),
        "qa_row_count": len(qa_rows),
        "review_prompt_count": len(review_prompts),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_files": task_rows_inserted_by_files,
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
                "files_lane_id": lane_id,
                "files_task_id": files_task_id,
                "task_rows_inserted_by_files": task_rows_inserted_by_files,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

__all__ = [
    "digital_products_post_launch_prompts",
    "digital_products_qa_rows",
    "digital_products_screenshot_rows",
    "write_digital_products_local_package_files",
]
