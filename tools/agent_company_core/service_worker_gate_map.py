from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Gate-map reporting for service-worker assignment readiness."""

from .constants import (
    SERVICE_WORKER_GATE_MAP_JSON,
    SERVICE_WORKER_GATE_MAP_REPORT,
    SERVICE_WORKER_GATE_MAP_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_worker_assignment_core import service_worker_assignment_plan_entry
from .service_worker_gate_map_content import build_service_worker_gate_map_artifacts
from .service_worker_pool_registry import service_worker_pool_registry_entries
from .service_worker_scope import service_worker_approval_review_entry


def service_worker_gate_map_entry(
    conn: sqlite3.Connection,
    row: dict[str, Any],
    generated_utc: str,
    pool_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    review = service_worker_approval_review_entry(conn, row, generated_utc)
    assignment = service_worker_assignment_plan_entry(conn, row, generated_utc)
    pool = pool_by_id.get(assignment["recommended_worker_pool_id"], {})
    terminal = row["status"] in {"complete", "rejected", "cancelled"}
    checks = {
        "packet_valid": not review.get("packet_errors"),
        "not_terminal": not terminal,
        "human_cro_review_candidate": review["recommended_decision"] == "human_cro_review_required",
        "scope_compatible_with_packet": bool(review["scope_compatible_with_packet"]),
        "pool_registered": bool(pool.get("registered_pool_available")),
        "service_status_approved_or_assigned": row["status"] in {"approved", "assigned"},
        "execution_readiness_ready": assignment["assignment_checks"].get("execution_readiness_ready") is True,
        "assignable_now": assignment["can_assign_now"] is True,
    }
    if terminal:
        gate = "terminal_no_execution"
        next_action = "Do not execute terminal requests; keep audit evidence or create a fresh scoped request."
    elif not checks["packet_valid"]:
        gate = "packet_repair_required"
        next_action = "Repair the service-worker packet before any review or assignment."
    elif not checks["human_cro_review_candidate"]:
        gate = "human_cro_review_not_ready"
        next_action = "Resolve CRO review blockers before approval consideration."
    elif not checks["service_status_approved_or_assigned"]:
        gate = "human_cro_approval_required"
        next_action = "Use the CRO review queue for a separate manual approve/reject decision."
    elif not checks["scope_compatible_with_packet"]:
        gate = "exact_scope_compatibility_required"
        next_action = "Revise and approve exact scope, then rerun the scope-diff report."
    elif not checks["pool_registered"]:
        gate = "service_worker_pool_registration_required"
        next_action = "Review and manually run the pool registration packet, then rerun pool registry and assignment plan."
    elif not checks["execution_readiness_ready"]:
        gate = "execution_readiness_required"
        next_action = "Rerun execution readiness and fix missing checks before assignment/start."
    elif not checks["assignable_now"]:
        gate = "manual_assignment_review_required"
        next_action = "Perform final manual assignment review; this report still grants no authority."
    else:
        gate = "ready_for_manual_assignment_but_report_grants_no_authority"
        next_action = "Manual operator may separately assign after confirming all gates and approvals."
    return {
        "source_service_request_id": row["request_id"],
        "lane_id": row.get("lane_id"),
        "worker_type": review.get("worker_type"),
        "service_status": row["status"],
        "risk_gate": review.get("risk_gate"),
        "current_blocking_gate": gate,
        "next_action": next_action,
        "gate_checks": checks,
        "approval_review_route": review["review_route"],
        "scope_diff_route": review["scope_diff_route"],
        "assignment_route": assignment["assignment_route"],
        "execution_readiness_route": assignment["execution_readiness_route"],
        "recommended_worker_pool_id": assignment["recommended_worker_pool_id"],
        "recommended_worker_role_id": assignment["recommended_worker_role_id"],
        "pool_status": pool.get("pool_status"),
        "pool_registered": bool(pool.get("registered_pool_available")),
        "registration_required": not bool(pool.get("registered_pool_available")),
        "approval_granted_by_gate_map": False,
        "pool_registered_by_gate_map": False,
        "service_request_assigned_by_gate_map": False,
        "service_request_updated_by_gate_map": False,
        "worker_started": False,
        "api_calls": False,
        "external_side_effects": False,
    }


def write_service_worker_gate_map(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_GATE_MAP_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_GATE_MAP_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_GATE_MAP_VALIDATION_JSON
    generated_utc = now_utc()
    clauses: list[str] = []
    params: list[Any] = []
    if args.request_id:
        clauses.append("sr.request_id = ?")
        params.append(args.request_id)
    if args.lane_id:
        clauses.append("sr.lane_id = ?")
        params.append(args.lane_id)
    if args.status:
        clauses.append("sr.status = ?")
        params.append(args.status)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT sr.*, l.department
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            {where}
            ORDER BY sr.request_id
            """,
            params,
        )
    ]
    all_rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT sr.*, l.department
            FROM service_requests sr
            LEFT JOIN lanes l ON l.lane_id = sr.lane_id
            ORDER BY sr.request_id
            """
        )
    ]
    all_assignment_entries = [service_worker_assignment_plan_entry(conn, row, generated_utc) for row in all_rows]
    pool_by_id = {
        pool["worker_pool_id"]: pool
        for pool in service_worker_pool_registry_entries(conn, all_assignment_entries)
    }
    entries = [service_worker_gate_map_entry(conn, row, generated_utc, pool_by_id) for row in rows]
    artifacts = build_service_worker_gate_map_artifacts(
        generated_utc=generated_utc,
        db_path=DB_PATH,
        filters={
            "request_id": args.request_id,
            "lane_id": args.lane_id,
            "status": args.status,
        },
        entries=entries,
        json_output_path=json_output_path,
        validation_path=validation_path,
    )
    payload = artifacts["payload"]
    validation_payload = artifacts["validation_payload"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(artifacts["markdown"], encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "count": len(entries),
                "ready_for_assignment_count": artifacts["ready_for_assignment_count"],
            },
            indent=2,
        )
    )
