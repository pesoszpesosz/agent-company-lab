from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

"""Base CEO decision parser apply-readiness report writer."""

from .constants import (
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_JSON,
    CEO_DECISION_PARSER_APPLY_DRY_RUNNER_VALIDATION_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_JSON,
    CEO_DECISION_PARSER_APPLY_READINESS_REPORT,
    CEO_DECISION_PARSER_APPLY_READINESS_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar
from .ceo_decision_apply_readiness_base_content import build_ceo_apply_readiness_base_content


def write_ceo_decision_parser_apply_readiness(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else CEO_DECISION_PARSER_APPLY_READINESS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else CEO_DECISION_PARSER_APPLY_READINESS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else CEO_DECISION_PARSER_APPLY_READINESS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "platform_engineering"
    readiness_task_id = "task-ceo-decision-parser-apply-readiness-20260616"
    readiness_evidence_id = "ceo-decision-parser-apply-readiness-20260616"
    source_dry_runner_task_id = "task-ceo-decision-parser-apply-dry-runner-20260616"
    source_dry_runner_evidence_id = "ceo-decision-parser-apply-dry-runner-20260616"
    target_request_id = "req-wave4-digital-products-browser-readonly-20260614"
    duplicate_key = "ceo-decision-parser-apply-readiness-20260616"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_dry_runner_task = conn.execute(
        "SELECT task_id, status, next_action FROM tasks WHERE task_id = ?",
        (source_dry_runner_task_id,),
    ).fetchone()
    source_dry_runner_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_dry_runner_evidence_id,),
    ).fetchone()
    dry_runner_validation = load_json(CEO_DECISION_PARSER_APPLY_DRY_RUNNER_VALIDATION_JSON)
    dry_runner_payload = load_json(CEO_DECISION_PARSER_APPLY_DRY_RUNNER_JSON)
    dry_preview = dry_runner_payload.get("dry_run_result", {}).get("preview_update", {})
    target_request = conn.execute(
        "SELECT request_id, status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
        (target_request_id,),
    ).fetchone()
    target_service_request_count = 1 if target_request else 0
    target_status_before = target_request["status"] if target_request else None
    target_status_after = target_status_before
    planned_updates = dry_preview.get("field_updates", {})
    if not isinstance(planned_updates, dict):
        planned_updates = {}
    target_request_payload = {key: target_request[key] for key in target_request.keys()} if target_request else None
    readiness_content = build_ceo_apply_readiness_base_content(
        target_request_id=target_request_id,
        target_request=target_request_payload,
        planned_updates=planned_updates,
    )
    local_decision = readiness_content["local_decision"]
    recommended_default = readiness_content["recommended_default"]
    readiness_packet_count = readiness_content["readiness_packet_count"]
    mutation_applied_count = readiness_content["mutation_applied_count"]
    queue_mutation_count = readiness_content["queue_mutation_count"]
    approval_request_count = readiness_content["approval_request_count"]
    planned_field_update_count = readiness_content["planned_field_update_count"]
    rollback_checks = readiness_content["rollback_checks"]
    required_operator_approvals = readiness_content["required_operator_approvals"]
    rollback_check_count = readiness_content["rollback_check_count"]
    required_operator_approval_count = readiness_content["required_operator_approval_count"]
    readiness_packet = readiness_content["readiness_packet"]
    readiness_summary = readiness_content["summary"]
    readiness_next_action = readiness_content["next_action"]
    runtime_boundary = readiness_content["runtime_boundary"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (readiness_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    readiness_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (readiness_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("platform engineering lane is missing, inactive, or unowned")
    if not source_dry_runner_task or source_dry_runner_task["status"] != "complete":
        failures.append("source apply dry-runner task is missing or incomplete")
    if not source_dry_runner_evidence or source_dry_runner_evidence["status"] != "local_ceo_decision_parser_apply_dry_runner_complete":
        failures.append("source apply dry-runner evidence is missing or not complete")
    if not dry_runner_validation.get("all_checks_passed") or dry_runner_validation.get("failure_count") != 0:
        failures.append("source apply dry-runner validation is not clean")
    if readiness_packet_count != 1:
        failures.append(f"expected 1 readiness packet, got {readiness_packet_count}")
    if target_service_request_count != 1:
        failures.append(f"expected 1 target service request, got {target_service_request_count}")
    if planned_field_update_count != 2:
        failures.append(f"expected 2 planned field updates, got {planned_field_update_count}")
    if rollback_check_count != 4:
        failures.append(f"expected 4 rollback checks, got {rollback_check_count}")
    if required_operator_approval_count != 5:
        failures.append(f"expected 5 required operator approvals, got {required_operator_approval_count}")
    if mutation_applied_count != 0:
        failures.append(f"expected 0 applied mutations, got {mutation_applied_count}")
    if queue_mutation_count != 0:
        failures.append(f"expected 0 queue mutations, got {queue_mutation_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_status_before != "needs_review":
        failures.append(f"expected target status before needs_review, got {target_status_before}")
    if target_status_after != "needs_review":
        failures.append(f"expected target status after needs_review, got {target_status_after}")
    if target_request and (target_request["approval_scope"] is not None or target_request["decision_note"] is not None):
        failures.append("target request already has approval_scope or decision_note before readiness packet")
    if target_task_exists_before:
        failures.append(f"target CEO decision parser apply readiness task already exists: {readiness_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if readiness_evidence_exists_before:
        failures.append(f"CEO decision parser apply readiness evidence already exists: {readiness_evidence_id}")
    if tasks_table_rows_before != 205:
        failures.append(f"expected 205 task rows before CEO decision parser apply readiness, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 113:
        failures.append(f"expected 113 evidence rows before CEO decision parser apply readiness, got {lane_evidence_rows_before}")

    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness.v1",
        "generated_utc": generated_utc,
        "readiness_lane_id": lane_id,
        "readiness_task_id": readiness_task_id,
        "readiness_evidence_id": readiness_evidence_id,
        "source_dry_runner_task_id": source_dry_runner_task_id,
        "source_dry_runner_evidence_id": source_dry_runner_evidence_id,
        "source_dry_runner_validation_path": str(CEO_DECISION_PARSER_APPLY_DRY_RUNNER_VALIDATION_JSON),
        "readiness_packet_count": readiness_packet_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": planned_field_update_count,
        "rollback_check_count": rollback_check_count,
        "required_operator_approval_count": required_operator_approval_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "readiness_packet": readiness_packet,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": readiness_summary,
        "next_action": readiness_next_action,
        "runtime_boundary": runtime_boundary,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_lines = [
        "# CEO Decision Parser Apply Readiness",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        readiness_summary,
        "",
        "## Planned Update",
        "",
        f"- Target request: `{target_request_id}`",
        f"- Fields: `{', '.join(sorted(planned_updates.keys()))}`",
        "- Apply allowed now: `False`",
        "",
        "## Required Operator Approvals",
        "",
    ]
    for approval in required_operator_approvals:
        md_lines.append(f"- {approval}")
    md_lines.extend(
        [
            "",
            "## Rollback Checks",
            "",
        ]
    )
    for check in rollback_checks:
        md_lines.append(f"- {check}")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This readiness packet applies nothing. It writes local artifacts only and does not update service requests, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            readiness_next_action,
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
                readiness_task_id,
                lane_id,
                "Create CEO decision parser apply readiness packet",
                32,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                readiness_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": readiness_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "CEO decision parser apply readiness",
                "status": "local_ceo_decision_parser_apply_readiness_complete",
                "summary": readiness_summary,
                "next_action": readiness_next_action,
                "ownership_note": "Generated by platform_engineering from the apply dry-runner; readiness packet is local planning data only.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    target_after = conn.execute(
        "SELECT status, approval_scope, decision_note, assigned_agent_id, started_at, completed_at, updated_at FROM service_requests WHERE request_id = ?",
        (target_request_id,),
    ).fetchone()
    task_rows_inserted_by_readiness = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (readiness_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (readiness_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (readiness_task_id,)) else 0
    if target_request and target_after and (
        target_after["status"] != target_request["status"]
        or target_after["approval_scope"] != target_request["approval_scope"]
        or target_after["decision_note"] != target_request["decision_note"]
        or target_after["assigned_agent_id"] != target_request["assigned_agent_id"]
        or target_after["started_at"] != target_request["started_at"]
        or target_after["completed_at"] != target_request["completed_at"]
        or target_after["updated_at"] != target_request["updated_at"]
    ):
        failures.append("target service request changed during apply readiness packet")
    if task_rows_inserted_by_readiness != 1:
        failures.append(f"expected 1 task row inserted by CEO decision parser apply readiness, got {task_rows_inserted_by_readiness}")
    if tasks_table_rows_after != 206:
        failures.append(f"expected 206 task rows after CEO decision parser apply readiness, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 114:
        failures.append(f"expected 114 evidence rows after CEO decision parser apply readiness, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("CEO decision parser apply readiness evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during CEO decision parser apply readiness")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_readiness": task_rows_inserted_by_readiness,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_validation.v1",
        "generated_utc": generated_utc,
        "readiness_path": str(json_output_path),
        "readiness_lane_id": lane_id,
        "readiness_task_id": readiness_task_id,
        "source_dry_runner_task_id": source_dry_runner_task_id,
        "readiness_packet_count": readiness_packet_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": planned_field_update_count,
        "rollback_check_count": rollback_check_count,
        "required_operator_approval_count": required_operator_approval_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_readiness": task_rows_inserted_by_readiness,
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
                "readiness_lane_id": lane_id,
                "readiness_task_id": readiness_task_id,
                "readiness_packet_count": readiness_packet_count,
                "planned_field_update_count": planned_field_update_count,
                "task_rows_inserted_by_readiness": task_rows_inserted_by_readiness,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

