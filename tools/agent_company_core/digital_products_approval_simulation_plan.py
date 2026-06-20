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
from .io import load_json, now_utc
from .digital_products_approval_simulation_plan_content import build_digital_products_post_approval_simulation_plan_content
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def write_digital_products_local_post_approval_simulation_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_JSON
    validation_path = Path(args.validation_path) if args.validation_path else DIGITAL_PRODUCTS_LOCAL_POST_APPROVAL_SIMULATION_PLAN_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lane_id = "digital_products_templates_plugins"
    plan_task_id = "task-digital-products-local-post-approval-simulation-plan-20260616"
    plan_evidence_id = "digital-products-local-post-approval-simulation-plan-20260616"
    source_brief_task_id = "task-digital-products-local-operator-approval-brief-20260616"
    source_brief_evidence_id = "digital-products-local-operator-approval-brief-20260616"
    duplicate_key = "digital-products-local-post-approval-simulation-plan-20260616"
    selected_candidate_id = "ai-builder-launch-checklist-pack"
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
    brief_validation = load_json(DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_VALIDATION_JSON)
    brief_payload = load_json(DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_JSON)
    decision_items = brief_payload.get("decision_items", [])
    blocked_questions = brief_payload.get("blocked_by_gate_questions", [])
    requires_explicit_approval_count = sum(1 for item in decision_items if item.get("approval_required"))

    plan_content = build_digital_products_post_approval_simulation_plan_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        source_brief_validation_path=str(DIGITAL_PRODUCTS_LOCAL_OPERATOR_APPROVAL_BRIEF_VALIDATION_JSON),
        lane_id=lane_id,
        plan_task_id=plan_task_id,
        plan_evidence_id=plan_evidence_id,
        source_brief_task_id=source_brief_task_id,
        source_brief_evidence_id=source_brief_evidence_id,
        selected_candidate_id=selected_candidate_id,
        blocked_questions=blocked_questions,
        requires_explicit_approval_count=requires_explicit_approval_count,
    )
    local_decision = plan_content["local_decision"]
    recommended_default = plan_content["recommended_default"]
    approval_request_count = plan_content["approval_request_count"]
    simulated_browser_sessions = plan_content["simulated_browser_sessions"]
    simulated_legal_payment_reviews = plan_content["simulated_legal_payment_reviews"]
    simulation_scenarios = plan_content["simulation_scenarios"]
    simulation_scenario_count = plan_content["simulation_scenario_count"]
    plan_summary = plan_content["summary"]
    plan_next_action = plan_content["next_action"]
    runtime_boundary = plan_content["runtime_boundary"]
    payload = plan_content["payload"]
    target_task_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (plan_task_id,))
    duplicate_key_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE duplicate_key = ?", (duplicate_key,))
    plan_evidence_exists_before = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (plan_evidence_id,))

    if not lane or lane["status"] != "active" or not lane["owner_agent_id"]:
        failures.append("digital products lane is missing, inactive, or unowned")
    if not source_task or source_task["status"] != "complete":
        failures.append("source operator approval brief task is missing or incomplete")
    if not source_evidence or source_evidence["status"] != "local_operator_approval_brief_complete":
        failures.append("source operator approval brief evidence is missing or not complete")
    if not brief_validation.get("all_checks_passed") or brief_validation.get("failure_count") != 0:
        failures.append("source operator approval brief validation is not clean")
    if brief_payload.get("selected_candidate_id") != selected_candidate_id:
        failures.append(f"expected selected candidate {selected_candidate_id}, got {brief_payload.get('selected_candidate_id')}")
    if len(decision_items) != 2:
        failures.append(f"expected 2 source decision items, got {len(decision_items)}")
    if requires_explicit_approval_count != 2:
        failures.append(f"expected 2 source explicit approval requirements, got {requires_explicit_approval_count}")
    if simulation_scenario_count != 2:
        failures.append(f"expected 2 simulation scenarios, got {simulation_scenario_count}")
    if approval_request_count != 0:
        failures.append(f"expected 0 approval requests, got {approval_request_count}")
    if simulated_browser_sessions != 0:
        failures.append(f"expected 0 simulated browser sessions executed, got {simulated_browser_sessions}")
    if simulated_legal_payment_reviews != 0:
        failures.append(f"expected 0 simulated legal/payment reviews executed, got {simulated_legal_payment_reviews}")
    if len(blocked_questions) != 4:
        failures.append(f"expected 4 blocked gate questions, got {len(blocked_questions)}")
    if target_task_exists_before:
        failures.append(f"target post-approval simulation plan task already exists: {plan_task_id}")
    if duplicate_key_exists_before:
        failures.append(f"duplicate key already exists: {duplicate_key}")
    if plan_evidence_exists_before:
        failures.append(f"post-approval simulation plan evidence already exists: {plan_evidence_id}")
    if tasks_table_rows_before != 187:
        failures.append(f"expected 187 task rows before post-approval simulation plan, got {tasks_table_rows_before}")
    if lane_evidence_rows_before != 95:
        failures.append(f"expected 95 evidence rows before post-approval simulation plan, got {lane_evidence_rows_before}")

    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(str(plan_content["markdown"]), encoding="utf-8")
    if not failures:
        ts = now_utc()
        conn.execute(
            """
            INSERT INTO tasks(task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key, evidence_required, next_action, created_at, updated_at, completed_at)
            VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                plan_task_id,
                lane_id,
                "Prepare local digital-products post-approval simulation plan",
                50,
                lane["owner_agent_id"],
                duplicate_key,
                str(output_path),
                plan_next_action,
                ts,
                ts,
                ts,
            ),
        )
        upsert_evidence(
            conn,
            {
                "evidence_id": plan_evidence_id,
                "lane_id": lane_id,
                "source_path": str(output_path),
                "source_url": None,
                "title": "Digital products local post-approval simulation plan",
                "status": "local_post_approval_simulation_plan_complete",
                "summary": plan_summary,
                "next_action": plan_next_action,
                "ownership_note": "Generated by platform_engineering from the operator approval brief; no scenario may execute without explicit user approval.",
            },
        )
        conn.commit()

    tasks_table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM tasks")
    lane_evidence_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence")
    service_requests_after = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    task_rows_inserted_by_plan = int(tasks_table_rows_after) - int(tasks_table_rows_before)
    evidence_rows_inserted_or_updated = 1 if db_scalar(conn, "SELECT COUNT(*) FROM lane_evidence WHERE evidence_id = ?", (plan_evidence_id,)) else 0
    live_tasks_created = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ?", (plan_task_id,)) else 0
    live_tasks_completed = 1 if db_scalar(conn, "SELECT COUNT(*) FROM tasks WHERE task_id = ? AND status = 'complete'", (plan_task_id,)) else 0
    if task_rows_inserted_by_plan != 1:
        failures.append(f"expected 1 task row inserted by post-approval simulation plan, got {task_rows_inserted_by_plan}")
    if tasks_table_rows_after != 188:
        failures.append(f"expected 188 task rows after post-approval simulation plan, got {tasks_table_rows_after}")
    if lane_evidence_rows_after != 96:
        failures.append(f"expected 96 evidence rows after post-approval simulation plan, got {lane_evidence_rows_after}")
    if evidence_rows_inserted_or_updated != 1:
        failures.append("post-approval simulation plan evidence row was not inserted or updated")
    if live_tasks_created != 1:
        failures.append(f"expected 1 live task created, got {live_tasks_created}")
    if live_tasks_completed != 1:
        failures.append(f"expected 1 live task completed, got {live_tasks_completed}")
    if service_requests_before != service_requests_after:
        failures.append("service request status counts changed during post-approval simulation plan")
    payload.update(
        {
            "live_tasks_created": live_tasks_created,
            "live_tasks_completed": live_tasks_completed,
            "tasks_table_rows_before": tasks_table_rows_before,
            "tasks_table_rows_after": tasks_table_rows_after,
            "task_rows_inserted_by_plan": task_rows_inserted_by_plan,
            "lane_evidence_rows_before": lane_evidence_rows_before,
            "lane_evidence_rows_after": lane_evidence_rows_after,
            "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
        }
    )
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.digital_products_local_post_approval_simulation_plan_validation.v1",
        "generated_utc": generated_utc,
        "plan_path": str(json_output_path),
        "plan_lane_id": lane_id,
        "plan_task_id": plan_task_id,
        "source_brief_task_id": source_brief_task_id,
        "source_brief_evidence_id": source_brief_evidence_id,
        "selected_candidate_id": selected_candidate_id,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "simulation_scenario_count": simulation_scenario_count,
        "requires_explicit_approval_count": requires_explicit_approval_count,
        "approval_request_count": approval_request_count,
        "blocked_by_gate_count": len(blocked_questions),
        "simulated_browser_sessions": simulated_browser_sessions,
        "simulated_legal_payment_reviews": simulated_legal_payment_reviews,
        "live_tasks_created": live_tasks_created,
        "live_tasks_completed": live_tasks_completed,
        "tasks_table_rows_before": tasks_table_rows_before,
        "tasks_table_rows_after": tasks_table_rows_after,
        "task_rows_inserted_by_plan": task_rows_inserted_by_plan,
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
                "plan_lane_id": lane_id,
                "plan_task_id": plan_task_id,
                "task_rows_inserted_by_plan": task_rows_inserted_by_plan,
                "evidence_rows_inserted_or_updated": evidence_rows_inserted_or_updated,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )


