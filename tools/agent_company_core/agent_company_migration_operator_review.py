from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Report-only migration draft, apply preflight, and operator review writers."""

from .constants import (
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_JSON,
    AGENT_COMPANY_DEPARTMENT_SCHEMA_PLAN_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_JSON,
    AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_REPORT,
    AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_JSON,
    AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_REPORT,
    AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_VALIDATION_JSON,
)
from .agent_company_migration_operator_review_content import (
    build_agent_company_migration_operator_review_artifacts,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_operator_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_OPERATOR_REVIEW_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    review_task_id = "task-agent-company-migration-operator-review-20260616"
    review_evidence_id = "agent-company-migration-operator-review-20260616"
    source_preflight_task_id = "task-agent-company-migration-apply-preflight-20260616"
    source_preflight_evidence_id = "agent-company-migration-apply-preflight-20260616"
    duplicate_key = "agent-company-migration-operator-review-20260616"
    local_decision = "agent_company_migration_operator_review_packet_ready_for_signed_decision_or_hold"
    recommended_default = "hold_without_signed_operator_approval"
    operator_review_packet_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    preflight_validation = load_json(AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_VALIDATION_JSON)
    preflight_payload = load_json(AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_JSON)
    decision_options = [
        {"option": "hold", "effect": "No apply command is enabled; continue report-only planning.", "default": True},
        {"option": "approve_sandbox_dry_run_only", "effect": "Allow a future command to copy the DB and test migration SQL on a throwaway copy only.", "default": False},
        {"option": "request_rework", "effect": "Send the migration packet back for table, rollback, or gate revisions.", "default": False},
        {"option": "reject_migration_path", "effect": "Close this schema path and keep the current control-plane tables unchanged.", "default": False},
    ]
    approval_conditions = [
        "operator supplies an explicit signed decision id",
        "decision scope names sandbox dry-run only unless separately approved",
        "backup path is specified and outside the live DB file",
        "migration draft and preflight validation both pass",
        "service request counts are snapshotted before any sandbox action",
        "rollback drill is required on the sandbox copy",
        "post-dry-run integrity report is required before any next ask",
        "approval expires unless used for the named command and artifact set",
    ]
    refusal_conditions = [
        "missing signed decision id",
        "approval tries to include live SQL apply",
        "backup path is missing or points to the live DB",
        "preflight or migration validation is stale or failing",
        "service request state drift is detected",
        "worker start, browser, account, wallet, payment, public, or security action is requested",
        "rollback drill is omitted",
        "artifact paths do not match this review packet",
    ]
    human_instructions = [
        "Review the migration draft markdown before approving anything.",
        "Prefer hold unless a sandbox dry-run is genuinely needed.",
        "Do not approve live migration SQL from this packet.",
        "If approving, write the exact option and artifact paths into the decision.",
        "Limit any approval to one command run and one timestamped sandbox copy.",
        "Require a post-run validation report before considering schema apply.",
        "Reject or request rework if any gate language is ambiguous.",
    ]
    evidence_links = [
        str(AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_REPORT),
        str(AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_VALIDATION_JSON),
        str(AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_REPORT),
        str(AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_VALIDATION_JSON),
    ]
    decision_option_count = len(decision_options)
    approval_condition_count = len(approval_conditions)
    refusal_condition_count = len(refusal_conditions)
    human_instruction_count = len(human_instructions)
    evidence_link_count = len(evidence_links)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_preflight_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_preflight_task_id,),
    ).fetchone()
    source_preflight_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_preflight_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (review_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (review_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_preflight_task or source_preflight_task["status"] != "complete":
        failures.append("source apply preflight task is missing or incomplete")
    if not source_preflight_evidence or source_preflight_evidence["status"] != "local_agent_company_migration_apply_preflight_complete":
        failures.append("source apply preflight evidence is missing or not complete")
    if not preflight_validation.get("all_checks_passed") or preflight_validation.get("failure_count") != 0:
        failures.append("source apply preflight validation is not clean")
    if preflight_payload.get("runtime_boundary", {}).get("apply_command_enabled") is not False:
        failures.append("source apply preflight does not keep apply command disabled")
    if operator_review_packet_count != 1:
        failures.append(f"expected 1 operator review packet, got {operator_review_packet_count}")
    if decision_option_count != 4:
        failures.append(f"expected 4 decision options, got {decision_option_count}")
    if approval_condition_count != 8:
        failures.append(f"expected 8 approval conditions, got {approval_condition_count}")
    if refusal_condition_count != 8:
        failures.append(f"expected 8 refusal conditions, got {refusal_condition_count}")
    if human_instruction_count != 7:
        failures.append(f"expected 7 human instructions, got {human_instruction_count}")
    if evidence_link_count != 4:
        failures.append(f"expected 4 evidence links, got {evidence_link_count}")
    if target_task_exists_before:
        failures.append(f"target operator review task already exists: {review_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"operator review evidence already exists: {review_evidence_id}")
    if tasks_table_rows_before != 230:
        failures.append(f"expected 230 task rows before operator review, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 138:
        failures.append(f"expected 138 evidence rows before operator review, got {lane_evidence_rows_before}")

    artifacts = build_agent_company_migration_operator_review_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        review_task_id=review_task_id,
        review_evidence_id=review_evidence_id,
        source_preflight_task_id=source_preflight_task_id,
        source_preflight_evidence_id=source_preflight_evidence_id,
        decision_options=decision_options,
        approval_conditions=approval_conditions,
        refusal_conditions=refusal_conditions,
        human_instructions=human_instructions,
        evidence_links=evidence_links,
    )
    payload = artifacts["payload"]
    summary = payload["summary"]
    next_action = payload["next_action"]
    local_decision = payload["local_decision"]
    recommended_default = payload["recommended_default"]
    runtime_boundary = payload["runtime_boundary"]

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    output_path.write_text(artifacts["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                review_task_id,
                lane_id,
                "Create agent company migration operator review packet",
                11,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": review_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration operator review packet",
                "status": "local_agent_company_migration_operator_review_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the apply preflight; default is hold and no operator decision was applied.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_after = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    tables_created = int(table_count_after) - int(table_count_before)
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_review = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (review_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (review_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (review_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_review != 1:
        failures.append(f"expected 1 task row inserted by review, got {task_rows_inserted_by_review}")
    if tasks_table_rows_after != 231:
        failures.append(f"expected 231 task rows after operator review, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 139:
        failures.append(f"expected 139 evidence rows after operator review, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("operator review evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by operator review, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during operator review")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_review": task_rows_inserted_by_review,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_operator_review_validation.v1",
        "generated_utc": generated_utc,
        "review_path": str(json_output_path),
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "source_preflight_task_id": source_preflight_task_id,
        "operator_review_packet_count": operator_review_packet_count,
        "decision_option_count": decision_option_count,
        "approval_condition_count": approval_condition_count,
        "refusal_condition_count": refusal_condition_count,
        "human_instruction_count": human_instruction_count,
        "evidence_link_count": evidence_link_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_review": task_rows_inserted_by_review,
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
                "review_lane_id": lane_id,
                "review_task_id": review_task_id,
                "decision_option_count": decision_option_count,
                "approval_condition_count": approval_condition_count,
                "refusal_condition_count": refusal_condition_count,
                "human_instruction_count": human_instruction_count,
                "evidence_link_count": evidence_link_count,
                "task_rows_inserted_by_review": task_rows_inserted_by_review,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

