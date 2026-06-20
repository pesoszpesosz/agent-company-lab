from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Report-only migration draft, apply preflight, and operator review writers."""

from .agent_company_migration_apply_preflight_content import build_agent_company_migration_apply_preflight_artifacts

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
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_apply_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_APPLY_PREFLIGHT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    preflight_task_id = "task-agent-company-migration-apply-preflight-20260616"
    preflight_evidence_id = "agent-company-migration-apply-preflight-20260616"
    source_migration_task_id = "task-agent-company-report-only-migration-draft-20260616"
    source_migration_evidence_id = "agent-company-report-only-migration-draft-20260616"
    duplicate_key = "agent-company-migration-apply-preflight-20260616"
    preflight_packet_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    source_migration_validation = load_json(AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_VALIDATION_JSON)
    source_migration_payload = load_json(AGENT_COMPANY_REPORT_ONLY_MIGRATION_DRAFT_JSON)
    operator_gates = source_migration_payload.get("apply_gates", [])
    preflight_checks = [
        "source_migration_validation_all_checks_passed",
        "migration_sql_present_but_not_executed",
        "operator_approval_missing_by_design",
        "backup_path_required_before_apply",
        "throwaway_copy_dry_run_required_before_apply",
        "rollback_sql_present_for_every_index_and_table",
        "service_request_counts_must_remain_constant",
        "worker_pool_must_remain_stopped",
        "post_apply_chain_integrity_required_before_next_layer",
    ]
    dry_run_steps = [
        "copy_agent_company_sqlite_to_timestamped_sandbox",
        "run_report_only_sql_against_sandbox_copy",
        "execute_validation_queries_against_sandbox_copy",
        "compare_table_and_index_inventory_against_plan",
        "verify_existing_tasks_and_lane_evidence_counts_on_sandbox",
        "run_rollback_sql_against_sandbox_copy",
        "verify_rollback_restores_pre_apply_table_inventory",
        "write_sandbox_dry_run_report_before_live_apply_request",
    ]
    apply_command_contract = {
        "command_name": "apply-agent-company-department-schema-migration",
        "default_enabled": False,
        "required_inputs": ["operator_approval_id", "backup_path", "dry_run_report_path", "migration_draft_path"],
        "must_refuse_when": ["approval_missing", "backup_missing", "dry_run_failed", "service_request_drift_detected"],
    }
    rollback_drills = [
        "drop_planned_indexes_in_reverse_order_on_sandbox",
        "drop_planned_tables_in_reverse_order_on_sandbox",
        "re-run_chain_integrity_after_sandbox_rollback",
    ]
    preflight_check_count = len(preflight_checks)
    operator_gate_count = len(operator_gates)
    dry_run_step_count = len(dry_run_steps)
    apply_command_contract_count = 1
    rollback_drill_count = len(rollback_drills)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_migration_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_migration_task_id,),
    ).fetchone()
    source_migration_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_migration_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_migration_task or source_migration_task["status"] != "complete":
        failures.append("source migration draft task is missing or incomplete")
    if not source_migration_evidence or source_migration_evidence["status"] != "local_agent_company_report_only_migration_draft_complete":
        failures.append("source migration draft evidence is missing or not complete")
    if not source_migration_validation.get("all_checks_passed") or source_migration_validation.get("failure_count") != 0:
        failures.append("source migration draft validation is not clean")
    if preflight_packet_count != 1:
        failures.append(f"expected 1 preflight packet, got {preflight_packet_count}")
    if preflight_check_count != 9:
        failures.append(f"expected 9 preflight checks, got {preflight_check_count}")
    if operator_gate_count != 7:
        failures.append(f"expected 7 operator gates, got {operator_gate_count}")
    if dry_run_step_count != 8:
        failures.append(f"expected 8 dry-run steps, got {dry_run_step_count}")
    if apply_command_contract_count != 1:
        failures.append(f"expected 1 apply command contract, got {apply_command_contract_count}")
    if rollback_drill_count != 3:
        failures.append(f"expected 3 rollback drills, got {rollback_drill_count}")
    if target_task_exists_before:
        failures.append(f"target apply preflight task already exists: {preflight_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"apply preflight evidence already exists: {preflight_evidence_id}")
    if tasks_table_rows_before != 229:
        failures.append(f"expected 229 task rows before apply preflight, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 137:
        failures.append(f"expected 137 evidence rows before apply preflight, got {lane_evidence_rows_before}")

    artifacts = build_agent_company_migration_apply_preflight_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        preflight_task_id=preflight_task_id,
        preflight_evidence_id=preflight_evidence_id,
        source_migration_task_id=source_migration_task_id,
        source_migration_evidence_id=source_migration_evidence_id,
        preflight_checks=preflight_checks,
        operator_gates=operator_gates,
        dry_run_steps=dry_run_steps,
        apply_command_contract=apply_command_contract,
        rollback_drills=rollback_drills,
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
                preflight_task_id,
                lane_id,
                "Create agent company migration apply preflight",
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
                "evidence_id": preflight_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration apply preflight",
                "status": "local_agent_company_migration_apply_preflight_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the report-only migration draft; apply command remains disabled and no SQL was executed.",
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
    task_rows_inserted_by_preflight = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (preflight_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_preflight != 1:
        failures.append(f"expected 1 task row inserted by preflight, got {task_rows_inserted_by_preflight}")
    if tasks_table_rows_after != 230:
        failures.append(f"expected 230 task rows after preflight, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 138:
        failures.append(f"expected 138 evidence rows after preflight, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("apply preflight evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by apply preflight, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during apply preflight")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_apply_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": str(json_output_path),
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "source_migration_task_id": source_migration_task_id,
        "preflight_packet_count": preflight_packet_count,
        "preflight_check_count": preflight_check_count,
        "operator_gate_count": operator_gate_count,
        "dry_run_step_count": dry_run_step_count,
        "apply_command_contract_count": apply_command_contract_count,
        "rollback_drill_count": rollback_drill_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
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
                "preflight_lane_id": lane_id,
                "preflight_task_id": preflight_task_id,
                "preflight_check_count": preflight_check_count,
                "operator_gate_count": operator_gate_count,
                "dry_run_step_count": dry_run_step_count,
                "apply_command_contract_count": apply_command_contract_count,
                "rollback_drill_count": rollback_drill_count,
                "task_rows_inserted_by_preflight": task_rows_inserted_by_preflight,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )



