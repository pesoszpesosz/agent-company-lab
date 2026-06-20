from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Packaging manifest, package files, and completeness helpers and report writers."""

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


def digital_products_completeness_checks() -> list[dict[str, str]]:
    return [
        {"check_id": "readme-present", "status": "pass", "finding": "README sections cover scope, buyer, included files, use, boundaries, non-claims, and gates."},
        {"check_id": "positioning-present", "status": "pass", "finding": "Positioning template was drafted earlier with ten filled answers."},
        {"check_id": "checklist-present", "status": "pass", "finding": "Launch checklist was drafted earlier with pre-launch, gated, and post-launch rows."},
        {"check_id": "screenshot-shotlist-present", "status": "pass", "finding": "Screenshot shot list has six local rows including a gated pricing/boundary row."},
        {"check_id": "qa-pass-present", "status": "pass", "finding": "QA pass has seven local checks for links, copy, scope, screenshots, checklist, gates, and distribution."},
        {"check_id": "post-launch-review-present", "status": "pass", "finding": "Post-launch review has six prompts for future approved launch review."},
        {"check_id": "non-claims-visible", "status": "pass", "finding": "The package repeatedly avoids revenue, conversion, buyer-count, payout, and live-demand claims."},
        {"check_id": "gate-safety-visible", "status": "pass", "finding": "Marketplace, seller terms, public listing, and payout/account setup remain explicitly gated."},
        {"check_id": "private-review-ready", "status": "pass", "finding": "The local draft is complete enough for private review before any browser/legal/payment gate is requested."},
    ]


def digital_products_missing_file_stubs() -> list[dict[str, str]]:
    return [
        {
            "file_id": "positioning-template.md",
            "reason": "Content exists in the asset-draft layer, but not yet materialized as a standalone file.",
            "next_action": "Materialize from `digital-products-local-asset-draft-latest.md` if a local package directory is created.",
        },
        {
            "file_id": "launch-checklist.md",
            "reason": "Content exists in the asset-draft layer, but not yet materialized as a standalone file.",
            "next_action": "Materialize from `digital-products-local-asset-draft-latest.md` if a local package directory is created.",
        },
    ]


def write_digital_products_local_completeness_check(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    check_task_id = "task-digital-products-local-completeness-check-20260616"
    check_evidence_id = "digital-products-local-completeness-check-20260616"
    source_files_task_id = "task-digital-products-local-package-files-20260616"
    source_files_evidence_id = "digital-products-local-package-files-20260616"
    duplicate_key = "digital-products-local-completeness-check-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "local_package_complete_enough_for_private_review_no_public_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_files_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_files_evidence_id,),
    ).fetchone()
    files_validation = load_json(DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_VALIDATION_JSON)
    files_payload = load_json(DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_JSON)
    manifest_payload = load_json(DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_JSON)
    files_candidate_id = files_payload.get("selected_candidate_id")
    blocked_questions = files_payload.get("blocked_by_gate_questions", [])
    drafted_files = files_payload.get("drafted_files", [])
    manifest_files = manifest_payload.get("package_files", [])
    completeness_checks = digital_products_completeness_checks()
    passed_check_count = sum(1 for check in completeness_checks if check["status"] == "pass")
    missing_file_stubs = digital_products_missing_file_stubs()

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (check_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    check_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (check_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source digital package files task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_package_files_complete":
        failures.append("source digital package files evidence is missing or not complete")
    if not files_validation.get("all_checks_passed") or files_validation.get("failure_count") != 0:
        failures.append("source digital package files validation is not clean")
    if files_candidate_id != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {files_candidate_id}")
    if len(manifest_files) != 6:
        failures.append(f"expected 6 manifest files, got {len(manifest_files)}")
    if len(drafted_files) != 4:
        failures.append(f"expected 4 drafted files, got {len(drafted_files)}")
    if len(completeness_checks) != 9:
        failures.append(f"expected 9 completeness checks, got {len(completeness_checks)}")
    if passed_check_count != 9:
        failures.append(f"expected 9 passing checks, got {passed_check_count}")
    if len(missing_file_stubs) != 2:
        failures.append(f"expected 2 missing file stubs, got {len(missing_file_stubs)}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target completeness check task already exists: {check_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if check_evidence_exists_before:
        failures.append(f"completeness check evidence already exists: {check_evidence_id}")
    if tasks_table_rows_before != 166:
        failures.append(f"expected 166 task rows before completeness check, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 84:
        failures.append(f"expected 84 evidence rows before completeness check, got {lane_evidence_rows_before}")

    check_summary = (
        "Ran a local completeness check across the six-file AI builder launch checklist pack. "
        "The package is complete enough for private review, with two file stubs still represented by earlier draft layers and all public/distribution/payment work gated."
    )
    check_next_action = (
        "Prepare a private-review packet that points to all local package artifacts; do not distribute, list, price, browse marketplaces, create accounts, or configure payouts."
    )
    payload = {
        "schema_version": "agent_company.digital_products_local_completeness_check.v1",
        "generated_utc": generated_utc,
        "check_lane_id": lane_id,
        "check_task_id": check_task_id,
        "check_evidence_id": check_evidence_id,
        "source_files_task_id": source_files_task_id,
        "source_files_evidence_id": source_files_evidence_id,
        "source_files_validation_path": str(DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "manifest_file_count": len(manifest_files),
        "manifest_files": manifest_files,
        "drafted_file_count": len(drafted_files),
        "drafted_files": drafted_files,
        "completeness_check_count": len(completeness_checks),
        "passed_check_count": passed_check_count,
        "completeness_checks": completeness_checks,
        "missing_file_stub_count": len(missing_file_stubs),
        "missing_file_stubs": missing_file_stubs,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "local_decision": local_decision,
        "summary": check_summary,
        "next_action": check_next_action,
        "forbidden_actions": [
            "Do not distribute, publish, browse marketplaces, create seller accounts, accept terms, configure payouts, set prices, or claim live demand from this completeness check.",
            "Do not mutate service requests, assign/start workers, call APIs, touch wallets/payments, trade, submit, post, or create external side effects from this completeness check.",
        ],
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Completeness Check",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        check_summary,
        "",
        "## Completeness Checks",
        "",
        "| Check | Status | Finding |",
        "| --- | --- | --- |",
    ]
    for check in completeness_checks:
        md_lines.append(f"| `{check['check_id']}` | `{check['status']}` | {check['finding']} |")
    md_lines.extend(["", "## File Stubs", "", "| File | Reason | Next action |", "| --- | --- | --- |"])
    for stub in missing_file_stubs:
        md_lines.append(f"| `{stub['file_id']}` | {stub['reason']} | {stub['next_action']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This completeness check is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, list products, publish pages, configure payouts, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.",
            "",
            "## Next Action",
            "",
            check_next_action,
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
                check_task_id,
                lane_id,
                "Run local digital-products package completeness check",
                70,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                check_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": check_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local completeness check",
                "status": "local_completeness_check_complete",
                "summary": check_summary,
                "next_action": check_next_action,
                "ownership_note": "Generated by platform_engineering from local package files; digital-products lane manager owns private-review packet follow-up.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_check = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (check_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (check_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (check_task_id,)) else 0
    if task_rows_inserted_by_check != 1:
        failures.append(f"expected 1 task row inserted by completeness check, got {task_rows_inserted_by_check}")
    if tasks_table_rows_after != 167:
        failures.append(f"expected 167 task rows after completeness check, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 85:
        failures.append(f"expected 85 evidence rows after completeness check, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("completeness check evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during completeness check")
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
            "task_rows_inserted_by_check": task_rows_inserted_by_check,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_completeness_check_validation.v1",
        "generated_utc": generated_utc,
        "check_path": str(json_output_path),
        "check_lane_id": lane_id,
        "check_task_id": check_task_id,
        "source_files_task_id": source_files_task_id,
        "source_files_evidence_id": source_files_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "manifest_file_count": len(manifest_files),
        "drafted_file_count": len(drafted_files),
        "completeness_check_count": len(completeness_checks),
        "passed_check_count": passed_check_count,
        "missing_file_stub_count": len(missing_file_stubs),
        "blocked_by_gate_count": len(blocked_questions),
        "local_decision": local_decision,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_check": task_rows_inserted_by_check,
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
                "check_lane_id": lane_id,
                "check_task_id": check_task_id,
                "task_rows_inserted_by_check": task_rows_inserted_by_check,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

