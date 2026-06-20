from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Migration decision parser scaffold and report-only module draft writers."""

from .constants import (
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_REPORT,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_VALIDATION_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_SCAFFOLD_JSON,
    AGENT_COMPANY_MIGRATION_DECISION_PARSER_SCAFFOLD_VALIDATION_JSON,
)
from .agent_company_migration_parser_module_draft_content import (
    build_agent_company_migration_decision_parser_module_draft_artifacts,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_agent_company_migration_decision_parser_module_draft(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else AGENT_COMPANY_MIGRATION_DECISION_PARSER_MODULE_DRAFT_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    module_task_id = "task-agent-company-migration-decision-parser-module-draft-20260616"
    module_evidence_id = "agent-company-migration-decision-parser-module-draft-20260616"
    source_scaffold_task_id = "task-agent-company-migration-decision-parser-scaffold-20260616"
    source_scaffold_evidence_id = "agent-company-migration-decision-parser-scaffold-20260616"
    duplicate_key = "agent-company-migration-decision-parser-module-draft-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    table_count_before = db_scalar(conn, "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    scaffold_validation = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_SCAFFOLD_VALIDATION_JSON)
    scaffold_payload = load_json(AGENT_COMPANY_MIGRATION_DECISION_PARSER_SCAFFOLD_JSON)
    guard_functions = scaffold_payload.get("guard_functions", [])
    accepted_decision_types = scaffold_payload.get("accepted_decision_types", [])
    result_fields = scaffold_payload.get("result_fields", [])
    refusal_reasons = scaffold_payload.get("refusal_reasons", [])
    fixture_coverage = scaffold_payload.get("fixture_coverage", [])
    draft_artifacts = build_agent_company_migration_decision_parser_module_draft_artifacts(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        validation_path=validation_path,
        lane_id=lane_id,
        module_task_id=module_task_id,
        module_evidence_id=module_evidence_id,
        source_scaffold_task_id=source_scaffold_task_id,
        source_scaffold_evidence_id=source_scaffold_evidence_id,
        guard_functions=guard_functions,
        accepted_decision_types=accepted_decision_types,
        result_fields=result_fields,
        refusal_reasons=refusal_reasons,
        fixture_coverage=fixture_coverage,
    )
    payload = draft_artifacts["payload"]
    local_decision = payload["local_decision"]
    recommended_default = payload["recommended_default"]
    summary = payload["summary"]
    next_action = payload["next_action"]
    runtime_boundary = payload["runtime_boundary"]
    parser_module_draft_count = payload["parser_module_draft_count"]
    module_section_count = payload["module_section_count"]
    function_block_count = payload["function_block_count"]
    guard_function_count = payload["guard_function_count"]
    accepted_decision_type_count = payload["accepted_decision_type_count"]
    result_field_count = payload["result_field_count"]
    refusal_reason_count = payload["refusal_reason_count"]
    fixture_coverage_count = payload["fixture_coverage_count"]

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_scaffold_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_scaffold_task_id,),
    ).fetchone()
    source_scaffold_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_scaffold_evidence_id,),
    ).fetchone()
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (module_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (module_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_scaffold_task or source_scaffold_task["status"] != "complete":
        failures.append("source parser scaffold task is missing or incomplete")
    if not source_scaffold_evidence or source_scaffold_evidence["status"] != "local_agent_company_migration_decision_parser_scaffold_complete":
        failures.append("source parser scaffold evidence is missing or not complete")
    if not scaffold_validation.get("all_checks_passed") or scaffold_validation.get("failure_count") != 0:
        failures.append("source parser scaffold validation is not clean")
    if parser_module_draft_count != 1:
        failures.append(f"expected 1 parser module draft, got {parser_module_draft_count}")
    if module_section_count != 8:
        failures.append(f"expected 8 module sections, got {module_section_count}")
    if function_block_count != 9:
        failures.append(f"expected 9 function blocks, got {function_block_count}")
    if guard_function_count != 9:
        failures.append(f"expected 9 guard functions, got {guard_function_count}")
    if accepted_decision_type_count != 4:
        failures.append(f"expected 4 accepted decision types, got {accepted_decision_type_count}")
    if result_field_count != 8:
        failures.append(f"expected 8 result fields, got {result_field_count}")
    if refusal_reason_count != 8:
        failures.append(f"expected 8 refusal reasons, got {refusal_reason_count}")
    if fixture_coverage_count != 12:
        failures.append(f"expected 12 fixture coverage rows, got {fixture_coverage_count}")
    if target_task_exists_before:
        failures.append(f"target parser module draft task already exists: {module_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if evidence_exists_before:
        failures.append(f"parser module draft evidence already exists: {module_evidence_id}")
    if tasks_table_rows_before != 235:
        failures.append(f"expected 235 task rows before parser module draft, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 143:
        failures.append(f"expected 143 evidence rows before parser module draft, got {lane_evidence_rows_before}")

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(draft_artifacts["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                module_task_id,
                lane_id,
                "Create agent company migration decision parser module draft",
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
                "evidence_id": module_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Agent company migration decision parser module draft",
                "status": "local_agent_company_migration_decision_parser_module_draft_complete",
                "summary": summary,
                "next_action": next_action,
                "ownership_note": "Generated by platform_engineering from the parser scaffold; draft is report-only and no importable parser module was written.",
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
    task_rows_inserted_by_parser_module_draft = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (module_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (module_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (module_task_id,)) else 0
    runtime_boundary["tables_created"] = tables_created
    if task_rows_inserted_by_parser_module_draft != 1:
        failures.append(f"expected 1 task row inserted by parser module draft, got {task_rows_inserted_by_parser_module_draft}")
    if tasks_table_rows_after != 236:
        failures.append(f"expected 236 task rows after parser module draft, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 144:
        failures.append(f"expected 144 evidence rows after parser module draft, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("parser module draft evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if tables_created != 0:
        failures.append(f"expected 0 tables created by parser module draft, got {tables_created}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during parser module draft")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_parser_module_draft": task_rows_inserted_by_parser_module_draft,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
            "runtime_boundary": runtime_boundary,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.migration_decision_parser_module_draft_validation.v1",
        "generated_utc": generated_utc,
        "module_draft_path": str(json_output_path),
        "module_lane_id": lane_id,
        "module_task_id": module_task_id,
        "source_scaffold_task_id": source_scaffold_task_id,
        "parser_module_draft_count": parser_module_draft_count,
        "module_section_count": module_section_count,
        "function_block_count": function_block_count,
        "guard_function_count": guard_function_count,
        "accepted_decision_type_count": accepted_decision_type_count,
        "result_field_count": result_field_count,
        "refusal_reason_count": refusal_reason_count,
        "fixture_coverage_count": fixture_coverage_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_parser_module_draft": task_rows_inserted_by_parser_module_draft,
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
                "module_lane_id": lane_id,
                "module_task_id": module_task_id,
                "module_section_count": module_section_count,
                "function_block_count": function_block_count,
                "guard_function_count": guard_function_count,
                "accepted_decision_type_count": accepted_decision_type_count,
                "result_field_count": result_field_count,
                "refusal_reason_count": refusal_reason_count,
                "fixture_coverage_count": fixture_coverage_count,
                "task_rows_inserted_by_parser_module_draft": task_rows_inserted_by_parser_module_draft,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "tables_created": tables_created,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

