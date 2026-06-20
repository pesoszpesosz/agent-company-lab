from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Copy polish, approval, post-approval, and gated-hold writers."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_JSON,
    DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_APPROVAL_REQUEST_DRAFTS_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_JSON,
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_REPORT,
    DIGITAL_PRODUCTS_LOCAL_COPY_POLISH_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_REPORT,
    DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_JSON,
    DIGITAL_PRODUCTS_LOCAL_GATE_CHOICE_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_JSON,
    DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_REPORT,
    DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_VALIDATION_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_JSON,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_REPORT,
    DIGITAL_PRODUCTS_LOCAL_POST_POLISH_READINESS_VALIDATION_JSON,
)
from .digital_products_approval_gated_hold_content import build_digital_products_gated_hold_register_content
from .io import load_json, now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_digital_products_local_gated_hold_register(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_GATED_HOLD_REGISTER_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    register_task_id = "task-digital-products-local-gated-hold-register-20260616"
    register_evidence_id = "digital-products-local-gated-hold-register-20260616"
    source_plan_task_id = "task-digital-products-local-post-approval-simulation-plan-20260616"
    source_plan_evidence_id = "digital-products-local-post-approval-simulation-plan-20260616"
    duplicate_key = "digital-products-local-gated-hold-register-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
    tasks_table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_before = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }

    lane = conn.execute("SELECT lane_id, status, owner_agent_id FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    source_task = conn.execute("SELECT task_id, status, next_action FROM tasks WHERE task_id = ?", (source_plan_task_id,)).fetchone()
    source_evidence = conn.execute(
        "SELECT evidence_id, status, source_path, summary, next_action FROM lane_evidence WHERE evidence_id = ?",
        (source_plan_evidence_id,),
    ).fetchone()
    plan_validation = load_json(DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_VALIDATION_JSON)
    plan_payload = load_json(DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_JSON)
    simulation_scenarios = plan_payload.get("simulation_scenarios", [])
    blocked_questions = plan_payload.get("blocked_by_gate_questions", [])

    source_simulation_scenario_count = len(simulation_scenarios)
    register_content = build_digital_products_gated_hold_register_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_plan_validation_path=str(DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_VALIDATION_JSON),
        lane_id=lane_id,
        register_task_id=register_task_id,
        register_evidence_id=register_evidence_id,
        source_plan_task_id=source_plan_task_id,
        source_plan_evidence_id=source_plan_evidence_id,
        selected_candidate_id=selected_candidate_id,
        blocked_questions=blocked_questions,
        source_simulation_scenario_count=source_simulation_scenario_count,
    )
    local_decision = register_content["local_decision"]
    recommended_default = register_content["recommended_default"]
    approval_request_count = register_content["approval_request_count"]
    runnable_without_approval_count = register_content["runnable_without_approval_count"]
    hold_entries = register_content["hold_entries"]
    active_hold_count = register_content["active_hold_count"]
    explicit_approval_required_count = register_content["explicit_approval_required_count"]
    register_summary = register_content["summary"]
    register_next_action = register_content["next_action"]
    runtime_boundary = register_content["runtime_boundary"]

    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (register_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    register_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (register_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source post-approval simulation plan task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_post_approval_simulation_plan_complete":
        failures.append("source post-approval simulation plan evidence is missing or not complete")
    if not plan_validation.get("all_checks_passed") or plan_validation.get("failure_count") != 0:
        failures.append("source post-approval simulation plan validation is not clean")
    if plan_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {plan_payload.get('selected_candidate_id')}")
    if source_simulation_scenario_count != 2:
        failures.append(f"expected 2 source simulation scenarios, got {source_simulation_scenario_count}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if len(hold_entries) != 4:
        failures.append(f"expected 4 hold entries, got {len(hold_entries)}")
    if active_hold_count != 4:
        failures.append(f"expected 4 active holds, got {active_hold_count}")
    if explicit_approval_required_count != 4:
        failures.append(f"expected 4 explicit approval requirements, got {explicit_approval_required_count}")
    if runnable_without_approval_count != 0:
        failures.append(f"expected 0 runnable-without-approval holds, got {runnable_without_approval_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if target_task_exists_before:
        failures.append(f"target gated hold register task already exists: {register_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if register_evidence_exists_before:
        failures.append(f"gated hold register evidence already exists: {register_evidence_id}")
    if tasks_table_rows_before != 188:
        failures.append(f"expected 188 task rows before gated hold register, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 96:
        failures.append(f"expected 96 evidence rows before gated hold register, got {lane_evidence_rows_before}")

    payload = register_content["payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(register_content["markdown"], encoding="utf-8")

    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                register_task_id,
                lane_id,
                "Create local digital-products gated hold register",
                49,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                register_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": register_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local gated hold register",
                "status": "local_gated_hold_register_complete",
                "summary": register_summary,
                "next_action": register_next_action,
                "ownership_note": "Generated by platform_engineering from the post-approval simulation plan; all holds remain active until explicit user approval.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_register = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (register_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (register_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (register_task_id,)) else 0
    if task_rows_inserted_by_register != 1:
        failures.append(f"expected 1 task row inserted by gated hold register, got {task_rows_inserted_by_register}")
    if tasks_table_rows_after != 189:
        failures.append(f"expected 189 task rows after gated hold register, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 97:
        failures.append(f"expected 97 evidence rows after gated hold register, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("gated hold register evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during gated hold register")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_register": task_rows_inserted_by_register,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_gated_hold_register_validation.v1",
        "generated_utc": generated_utc,
        "register_path": str(json_output_path),
        "register_lane_id": lane_id,
        "register_task_id": register_task_id,
        "source_plan_task_id": source_plan_task_id,
        "source_plan_evidence_id": source_plan_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "hold_entry_count": len(hold_entries),
        "source_simulation_scenario_count": source_simulation_scenario_count,
        "active_hold_count": active_hold_count,
        "explicit_approval_required_count": explicit_approval_required_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "approval_request_count": approval_request_count,
        "blocked_by_gate_count": len(blocked_questions),
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_register": task_rows_inserted_by_register,
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
                "register_lane_id": lane_id,
                "register_task_id": register_task_id,
                "task_rows_inserted_by_register": task_rows_inserted_by_register,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

