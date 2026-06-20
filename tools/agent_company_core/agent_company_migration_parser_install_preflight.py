from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Migration decision parser install preflight and install review writers."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_REVIEW_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_VALIDATION_JSON,
)
from .agent_company_migration_parser_install_preflight_content import (
    build_agent_company_migration_decision_parser_install_preflight_artifacts,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_install_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_INSTALL_PREFLIGHT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    preflight_task_id = "task-agent-company-migration-decision-parser-install-preflight-20260616"
    preflight_evidence_id = "agent-company-migration-decision-parser-install-preflight-20260616"
    source_static_review_task_id = "task-agent-company-migration-decision-parser-static-review-20260616"
    source_static_review_evidence_id = "agent-company-migration-decision-parser-static-review-20260616"
    duplicate_key = "agent-company-migration-decision-parser-install-preflight-20260616"
    local_decision = "agent_company_migration_decision_parser_install_preflight_ready_for_operator_install_review"
    recommended_default = "hold_without_operator_approval_to_write_parser_module_file"
    install_preflight_count = 1
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    static_review_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_STATIC_REVIEW_VALIDATION_JSON)
    file_draft_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_JSON)
    target_files = [
        {
            "target_path": "E:\\agent-company-lab\\tools\\migration_decision_parser.py",
            "source_artifact": str(AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_FILE_DRAFT_JSON),
            "line_count": file_draft_payload.get("module_source_line_count"),
            "install_status": "not_written_requires_operator_approval",
        }
    ]
    install_gates = [
        "operator_signed_file_write_approval_required",
        "target_path_must_be_inside_agent_company_lab_tools",
        "backup_existing_target_if_present",
        "write_to_temp_file_before_replace",
        "run_py_compile_on_temp_file",
        "run_saved_fixture_runner_against_temp_file",
        "do_not_import_from_live_command_path",
        "preserve_service_request_counts",
        "write_post_install_static_review_before_enabling_live_parse",
    ]
    preflight_checks = [
        "source_static_review_clean",
        "source_file_draft_available",
        "target_file_path_declared",
        "module_source_line_count_matches_draft",
        "fixture_coverage_count_is_12",
        "operator_approval_missing_by_default",
        "rollback_steps_declared",
        "live_decision_parsing_disabled",
        "service_request_mutation_forbidden",
        "external_actions_forbidden",
    ]
    rollback_steps = [
        "delete_temp_file_if_compile_fails",
        "restore_existing_target_from_backup_if_replace_fails",
        "remove_new_target_if_post_install_static_review_fails",
        "restore_pre_install_artifact_index",
        "rerun_chain_integrity_after_rollback",
    ]
    approval_requirements = [
        "signed_operator_decision_id",
        "exact_target_path",
        "exact_source_artifact_path",
        "permission_to_write_one_local_file_only",
        "permission_expires_after_one_attempt",
        "no_permission_to_parse_live_decisions",
    ]
    install_gate_count = len(install_gates)
    preflight_check_count = len(preflight_checks)
    rollback_step_count = len(rollback_steps)
    approval_requirement_count = len(approval_requirements)
    target_file_count = len(target_files)

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_static_review_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_static_review_task_id,),
    ).fetchone()
    source_static_review_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_static_review_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_static_review_task or source_static_review_task["status"] != "complete":
        failures.append("source parser static review task is missing or incomplete")
    if not source_static_review_evidence or source_static_review_evidence["status"] != "local_agent_company_migration_decision_parser_static_review_complete":
        failures.append("source parser static review evidence is missing or not complete")
    if not static_review_validation.get("all_checks_passed") or static_review_validation.get("failure_count") != 0:
        failures.append("source parser static review validation is not clean")
    if install_preflight_count != 1:
        failures.append(f"expected 1 install preflight, got {install_preflight_count}")
    if install_gate_count != 9:
        failures.append(f"expected 9 install gates, got {install_gate_count}")
    if preflight_check_count != 10:
        failures.append(f"expected 10 preflight checks, got {preflight_check_count}")
    if rollback_step_count != 5:
        failures.append(f"expected 5 rollback steps, got {rollback_step_count}")
    if approval_requirement_count != 6:
        failures.append(f"expected 6 approval requirements, got {approval_requirement_count}")
    if target_file_count != 1:
        failures.append(f"expected 1 target file, got {target_file_count}")
    if target_task_exists_before:
        failures.append(f"target parser install preflight task already exists: {preflight_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"parser install preflight evidence already exists: {preflight_evidence_id}")
    if tasks_table_rows_before != 239:
        failures.append(f"expected 239 task rows before parser install preflight, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 147:
        failures.append(f"expected 147 evidence rows before parser install preflight, got {lane_evidence_rows_before}")

    artifacts = build_agent_company_migration_decision_parser_install_preflight_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        preflight_task_id=preflight_task_id,
        preflight_evidence_id=preflight_evidence_id,
        source_static_review_task_id=source_static_review_task_id,
        source_static_review_evidence_id=source_static_review_evidence_id,
        target_files=target_files,
        install_gates=install_gates,
        preflight_checks=preflight_checks,
        rollback_steps=rollback_steps,
        approval_requirements=approval_requirements,
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
                "Create agent company migration decision parser install preflight",
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
                "title": "Agent company migration decision parser install preflight",
                "status": "local_agent_company_migration_decision_parser_install_preflight_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from parser static review; preflight is report-only and does not install the parser.",
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
    task_rows_inserted_by_install_preflight = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (preflight_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (preflight_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (preflight_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_install_preflight != 1:
        failures.append(f"expected 1 task row inserted by install preflight, got {task_rows_inserted_by_install_preflight}")
    if tasks_table_rows_after != 240:
        failures.append(f"expected 240 task rows after install preflight, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 148:
        failures.append(f"expected 148 evidence rows after install preflight, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("parser install preflight evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by install preflight, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during install preflight")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_install_preflight": task_rows_inserted_by_install_preflight,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_install_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": str(json_output_path),
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "source_static_review_task_id": source_static_review_task_id,
        "install_preflight_count": install_preflight_count,
        "install_gate_count": install_gate_count,
        "preflight_check_count": preflight_check_count,
        "rollback_step_count": rollback_step_count,
        "approval_requirement_count": approval_requirement_count,
        "target_file_count": target_file_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_install_preflight": task_rows_inserted_by_install_preflight,
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
                "install_gate_count": install_gate_count,
                "preflight_check_count": preflight_check_count,
                "rollback_step_count": rollback_step_count,
                "approval_requirement_count": approval_requirement_count,
                "target_file_count": target_file_count,
                "task_rows_inserted_by_install_preflight": task_rows_inserted_by_install_preflight,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

