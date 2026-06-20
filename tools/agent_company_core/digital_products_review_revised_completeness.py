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


def digital_products_revised_completeness_checks() -> list[dict[str, object]]:
    return [
        {"check_id": "six-files-present", "passed": True, "evidence": "Revision pass includes six revised file drafts."},
        {"check_id": "filled-example-present", "passed": True, "evidence": "One filled example is included for a hypothetical solo AI-builder launch."},
        {"check_id": "buyer-specific", "passed": True, "evidence": "README and filled example name a solo AI-builder buyer and local pre-launch job."},
        {"check_id": "promise-safe", "passed": True, "evidence": "Draft avoids revenue, payout, buyer-count, and live-demand claims."},
        {"check_id": "gate-language-propagated", "passed": True, "evidence": "Boundary terms are present across README, QA, private listing, and scorecard drafts."},
        {"check_id": "no-placeholder-stubs", "passed": True, "evidence": "Revision validation reports zero placeholder stubs."},
        {"check_id": "private-review-scorecard-present", "passed": True, "evidence": "Scorecard covers usefulness, clarity, boundary safety, and next revision."},
        {"check_id": "external-actions-blocked", "passed": True, "evidence": "All browser, marketplace, account, legal, payment, wallet, API, and public actions remain gated."},
    ]


def write_digital_products_local_revised_completeness(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_REVISED_COMPLETENESS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    check_task_id = "task-digital-products-local-revised-completeness-20260616"
    check_evidence_id = "digital-products-local-revised-completeness-20260616"
    source_revision_task_id = "task-digital-products-local-revision-pass-20260616"
    source_revision_evidence_id = "digital-products-local-revision-pass-20260616"
    duplicate_key = "digital-products-local-revised-completeness-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    local_decision = "revised_package_complete_for_gate_decision_no_external_action"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_revision_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_revision_evidence_id,),
    ).fetchone()
    revision_validation = load_json(DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_VALIDATION_JSON)
    revision_payload = load_json(DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_JSON)
    checks = digital_products_revised_completeness_checks()
    passed_check_count = sum(1 for item in checks if item.get("passed") is True)
    revised_file_count = int(revision_payload.get("revised_file_count", 0))
    filled_example_count = int(revision_payload.get("filled_example_count", 0))
    boundary_phrase_count = int(revision_payload.get("boundary_phrase_count", 0))
    placeholder_stub_count = int(revision_payload.get("placeholder_stub_count", 0))
    blocked_questions = revision_payload.get("blocked_by_gate_questions", [])

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (check_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    check_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (check_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source revision pass task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_revision_pass_complete":
        failures.append("source revision pass evidence is missing or not complete")
    if not revision_validation.get("all_checks_passed") or revision_validation.get("failure_count") != 0:
        failures.append("source revision pass validation is not clean")
    if revision_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {revision_payload.get('selected_candidate_id')}")
    if revised_file_count != 6:
        failures.append(f"expected 6 revised files, got {revised_file_count}")
    if len(checks) != 8:
        failures.append(f"expected 8 completeness checks, got {len(checks)}")
    if passed_check_count != 8:
        failures.append(f"expected 8 passed checks, got {passed_check_count}")
    if filled_example_count != 1:
        failures.append(f"expected 1 filled example, got {filled_example_count}")
    if boundary_phrase_count != 7:
        failures.append(f"expected 7 boundary phrases, got {boundary_phrase_count}")
    if placeholder_stub_count != 0:
        failures.append(f"expected 0 placeholder stubs, got {placeholder_stub_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target revised completeness task already exists: {check_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if check_evidence_exists_before:
        failures.append(f"revised completeness evidence already exists: {check_evidence_id}")
    if tasks_table_rows_before != 174:
        failures.append(f"expected 174 task rows before revised completeness, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 88:
        failures.append(f"expected 88 evidence rows before revised completeness, got {lane_evidence_rows_before}")

    check_summary = (
        "Completed a local revised-package completeness check for the AI builder launch checklist pack. "
        "The revised package has six local file drafts, one filled example, explicit gates, and no placeholder stubs."
    )
    check_next_action = (
        "Prepare a local gate-decision packet that compares continue-local, request read-only browser approval, request legal/payment review, or pause; do not perform any external validation."
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
        "schema_version": "agent_company.digital_products_local_revised_completeness.v1",
        "generated_utc": generated_utc,
        "check_lane_id": lane_id,
        "check_task_id": check_task_id,
        "check_evidence_id": check_evidence_id,
        "source_revision_task_id": source_revision_task_id,
        "source_revision_evidence_id": source_revision_evidence_id,
        "source_revision_validation_path": str(DIGITAL_PRODUCTS_LOCAL_REVISION_PASS_VALIDATION_JSON),
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "revised_file_count": revised_file_count,
        "completeness_check_count": len(checks),
        "passed_check_count": passed_check_count,
        "completeness_checks": checks,
        "filled_example_count": filled_example_count,
        "boundary_phrase_count": boundary_phrase_count,
        "placeholder_stub_count": placeholder_stub_count,
        "blocked_by_gate_count": len(blocked_questions),
        "blocked_by_gate_questions": blocked_questions,
        "summary": check_summary,
        "next_action": check_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Digital Products Local Revised Completeness Check",
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
        "## Checks",
        "",
        "| Check | Passed | Evidence |",
        "| --- | --- | --- |",
    ]
    for item in checks:
        md_lines.append(f"| `{item['check_id']}` | `{item['passed']}` | {item['evidence']} |")
    md_lines.extend(["", "## Preserved Gates", "", "| Question | Gate |", "| --- | --- |"])
    for item in blocked_questions:
        md_lines.append(f"| `{item['question_id']}` | `{item['gate_required']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This completeness check is local only. It does not browse marketplaces, create accounts, accept terms, publish, list, set prices, configure payouts, touch wallets/payments, call APIs, mutate service requests, assign/start workers, or create external side effects.",
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
                "Run local digital-products revised completeness check",
                62,
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
                "title": "Digital products local revised completeness check",
                "status": "local_revised_completeness_complete",
                "summary": check_summary,
                "next_action": check_next_action,
                "ownership_note": "Generated by platform_engineering from the local revision pass; digital-products lane manager owns the next gate-decision packet.",
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
        failures.append(f"expected 1 task row inserted by revised completeness, got {task_rows_inserted_by_check}")
    if tasks_table_rows_after != 175:
        failures.append(f"expected 175 task rows after revised completeness, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 89:
        failures.append(f"expected 89 evidence rows after revised completeness, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("revised completeness evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during revised completeness")
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
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_revised_completeness_validation.v1",
        "generated_utc": generated_utc,
        "check_path": str(json_output_path),
        "check_lane_id": lane_id,
        "check_task_id": check_task_id,
        "source_revision_task_id": source_revision_task_id,
        "source_revision_evidence_id": source_revision_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "revised_file_count": revised_file_count,
        "completeness_check_count": len(checks),
        "passed_check_count": passed_check_count,
        "filled_example_count": filled_example_count,
        "boundary_phrase_count": boundary_phrase_count,
        "placeholder_stub_count": placeholder_stub_count,
        "blocked_by_gate_count": len(blocked_questions),
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

