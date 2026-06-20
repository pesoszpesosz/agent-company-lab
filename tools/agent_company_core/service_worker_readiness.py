from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .constants import (
    SERVICE_WORKER_READINESS_JSON,
    SERVICE_WORKER_READINESS_REPORT,
    SERVICE_WORKER_READINESS_VALIDATION_JSON,
)
from .io import load_json, now_utc, parse_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_worker_request_synthesis import (
    service_worker_packet_path,
    synthesize_service_worker_request,
    validate_service_worker_request_object,
)
from .utils import md_cell

def latest_approval_for_request(conn: sqlite3.Connection, request_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT *
        FROM approvals
        WHERE request_id = ?
        ORDER BY created_at DESC, approval_id DESC
        LIMIT 1
        """,
        (request_id,),
    ).fetchone()
    return dict(row) if row else None


def approval_not_expired(approval: dict[str, Any] | None) -> bool:
    if not approval:
        return False
    expires_at = approval.get("expires_at")
    if not expires_at:
        return True
    parsed = parse_utc(expires_at)
    if not parsed:
        return False
    return parsed > datetime.now(timezone.utc)


def service_worker_readiness_entry(
    conn: sqlite3.Connection,
    row: dict[str, Any],
    worker_agent_id: str | None,
    generated_utc: str,
) -> dict[str, Any]:
    packet_path = service_worker_packet_path(row["request_id"])
    if packet_path.exists():
        packet = load_json(packet_path)
        packet_source = "existing_packet"
    else:
        packet = synthesize_service_worker_request(row, generated_utc)
        packet_source = "synthesized_from_db"
    packet_errors = validate_service_worker_request_object(packet)
    approval = latest_approval_for_request(conn, row["request_id"])
    exact_scope = row.get("approval_scope") or ""
    checks = {
        "packet_valid": not packet_errors,
        "service_status_executable": row["status"] in {"approved", "assigned", "in_progress"},
        "packet_status_matches_service": packet.get("status") == row["status"],
        "approval_scope_present": bool(exact_scope.strip()),
        "latest_approval_exists": approval is not None,
        "latest_approval_approved": bool(approval and approval.get("status") == "approved"),
        "latest_approval_not_expired": approval_not_expired(approval),
        "approval_scope_matches_latest": bool(
            approval and exact_scope.strip() and approval.get("exact_scope") == exact_scope
        ),
        "assigned_agent_present": bool(row.get("assigned_agent_id")),
        "requested_worker_matches_assignment": bool(
            not worker_agent_id or (row.get("assigned_agent_id") == worker_agent_id)
        ),
        "result_path_present": bool(packet.get("result_artifact_path")),
        "all_side_effect_flags_false": all(
            packet.get(flag) is False
            for flag in [
                "external_side_effects_allowed",
                "real_money_allowed",
                "public_action_allowed",
                "account_or_identity_action_allowed",
                "model_or_api_cost_allowed",
            ]
        ),
    }
    missing = [key for key, value in checks.items() if not value]
    ready = not missing
    if ready:
        route = "ready_for_manual_worker_start_after_final_human_check"
        next_action = "Run start-service-request only if the worker stays inside the exact scope and all stop gates remain clear."
    elif row["status"] in {"complete", "rejected", "cancelled"}:
        route = f"terminal_{row['status']}_not_startable"
        next_action = "Do not start; retain terminal audit evidence or create a new service request."
    elif not checks["service_status_executable"]:
        route = "blocked_until_service_request_approved"
        next_action = "Obtain explicit approval with exact scope before assignment or worker start."
    elif not checks["assigned_agent_present"]:
        route = "blocked_until_worker_assignment"
        next_action = "Assign a worker after approval and before start."
    else:
        route = "blocked_until_readiness_checks_pass"
        next_action = "Resolve missing readiness checks before any worker start."
    return {
        "source_service_request_id": row["request_id"],
        "worker_request_id": packet.get("worker_request_id"),
        "lane_id": row["lane_id"],
        "worker_type": packet.get("worker_type"),
        "service_id": row.get("service_id") or packet.get("service_id"),
        "request_type": row["request_type"],
        "risk_gate": row.get("risk_gate") or packet.get("risk_gate"),
        "service_status": row["status"],
        "packet_status": packet.get("status"),
        "assigned_agent_id": row.get("assigned_agent_id"),
        "requested_worker_agent_id": worker_agent_id,
        "approval_id": approval.get("approval_id") if approval else None,
        "approval_status": approval.get("status") if approval else None,
        "approval_expires_at": approval.get("expires_at") if approval else None,
        "approval_scope": exact_scope,
        "packet_path": str(packet_path),
        "packet_source": packet_source,
        "packet_errors": packet_errors,
        "result_artifact_path": packet.get("result_artifact_path"),
        "checks": checks,
        "missing_checks": missing,
        "ready_to_start": ready,
        "route": route,
        "next_action": next_action,
        "start_command_allowed_by_report": False,
    }


def write_service_worker_execution_readiness(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_READINESS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_READINESS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_READINESS_VALIDATION_JSON
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
    entries = [service_worker_readiness_entry(conn, row, args.worker_agent_id, generated_utc) for row in rows]
    route_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    worker_type_counts: dict[str, int] = {}
    ready_count = 0
    for entry in entries:
        route_counts[entry["route"]] = route_counts.get(entry["route"], 0) + 1
        status_counts[entry["service_status"]] = status_counts.get(entry["service_status"], 0) + 1
        worker_type = entry.get("worker_type") or "unknown"
        worker_type_counts[worker_type] = worker_type_counts.get(worker_type, 0) + 1
        if entry["ready_to_start"]:
            ready_count += 1

    payload = {
        "schema_version": "service_worker_execution_readiness.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "filters": {
            "request_id": args.request_id,
            "lane_id": args.lane_id,
            "status": args.status,
            "worker_agent_id": args.worker_agent_id,
        },
        "request_count": len(entries),
        "ready_to_start_count": ready_count,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
        "readiness": entries,
        "execution_notice": "Read-only readiness verifier. It grants no approval and does not assign, start, complete, enqueue, or execute service workers.",
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_execution_readiness_validation.v1",
        "generated_utc": generated_utc,
        "readiness_path": str(json_output_path),
        "validated_count": len(entries),
        "ready_to_start_count": ready_count,
        "all_reports_no_start_command_authority": all(not item["start_command_allowed_by_report"] for item in entries),
        "service_requests_approved_by_report": 0,
        "service_requests_started_by_report": 0,
        "service_requests_updated_by_report": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "route_counts": dict(sorted(route_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "worker_type_counts": dict(sorted(worker_type_counts.items())),
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Service Worker Execution Readiness",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report is a read-only readiness verifier. It grants no approval and does not assign, start, complete, enqueue, browse, call APIs, post, submit, register, trade, spend, or contact anyone.",
        "",
        f"- Requests evaluated: `{len(entries)}`",
        f"- Ready to start after final human check: `{ready_count}`",
        f"- Route counts: `{json.dumps(validation_payload['route_counts'], sort_keys=True)}`",
        f"- Status counts: `{json.dumps(validation_payload['status_counts'], sort_keys=True)}`",
        f"- Worker starts: `0`",
        f"- Service requests updated: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Readiness Rows",
        "",
        "| Status | Ready | Route | Source Request | Assigned Worker | Missing Checks |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['service_status']}`",
                    f"`{entry['ready_to_start']}`",
                    f"`{entry['route']}`",
                    f"`{entry['source_service_request_id']}`",
                    f"`{entry.get('assigned_agent_id') or ''}`",
                    md_cell(", ".join(entry["missing_checks"]) or "none", 260),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "Use this verifier before any future service-worker start. A real start still needs explicit approval, exact scope, worker assignment, packet validation, and manual confirmation that the worker remains inside all boundaries.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "count": len(entries),
                "ready_to_start_count": ready_count,
            },
            indent=2,
        )
    )
