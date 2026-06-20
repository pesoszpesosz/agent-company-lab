from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Human-decision packet, post-decision, drift, command-safety, authority, and preflight reporting."""

from .constants import (
    SERVICE_WORKER_APPROVAL_REVIEW_JSON,
    SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON,
    SERVICE_WORKER_GATE_MAP_JSON,
    SERVICE_WORKER_HUMAN_DECISION_PACKET_DIR,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_REPORT,
    SERVICE_WORKER_HUMAN_DECISION_PACKETS_VALIDATION_JSON,
    SERVICE_WORKER_POST_DECISION_SIMULATION_JSON,
    SERVICE_WORKER_POST_DECISION_SIMULATION_REPORT,
    SERVICE_WORKER_POST_DECISION_SIMULATION_VALIDATION_JSON,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_JSON,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_REPORT,
    SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_DRIFT_JSON,
    SERVICE_WORKER_DECISION_DRIFT_REPORT,
    SERVICE_WORKER_DECISION_DRIFT_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_COMMAND_SAFETY_JSON,
    SERVICE_WORKER_DECISION_COMMAND_SAFETY_REPORT,
    SERVICE_WORKER_DECISION_COMMAND_SAFETY_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_JSON,
    SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_REPORT,
    SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_VALIDATION_JSON,
    SERVICE_WORKER_DECISION_PREFLIGHT_JSON,
    SERVICE_WORKER_DECISION_PREFLIGHT_REPORT,
    SERVICE_WORKER_DECISION_PREFLIGHT_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR, ROLE_REGISTRY_PATH, ROOT
from .utils import md_cell, safe_id_fragment
from .service_worker_utils import (
    db_scalar,
    load_report_json_or_error,
)


def service_worker_decision_drift_rows(
    conn: sqlite3.Connection, generated_utc: str
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    human_payload, human_errors = load_report_json_or_error(SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON)
    refresh_payload, refresh_errors = load_report_json_or_error(SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = human_errors + refresh_errors + integrity_errors
    packets = human_payload.get("decision_packets", []) if human_payload else []
    if human_payload and not isinstance(packets, list):
        failures.append("human decision payload field decision_packets is not a list")
        packets = []
    refresh_ok = bool(refresh_payload and refresh_payload.get("failure_count") == 0)
    integrity_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if refresh_payload and not refresh_ok:
        failures.append("post-decision refresh-plan validation is not passing")
    if integrity_payload and not integrity_ok:
        failures.append("chain integrity validation is not passing")

    rows: list[dict[str, Any]] = []
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        request_id = packet.get("source_service_request_id")
        if not request_id:
            failures.append("human decision packet is missing source_service_request_id")
            continue
        service_row = conn.execute(
            """
            SELECT request_id, status, assigned_agent_id, approval_scope, artifact_path,
                   started_at, completed_at, updated_at, decision_note
            FROM service_requests
            WHERE request_id = ?
            """,
            (request_id,),
        ).fetchone()
        latest_approval = conn.execute(
            """
            SELECT approval_id, status, approved_by, exact_scope, created_at
            FROM approvals
            WHERE request_id = ?
            ORDER BY created_at DESC, approval_id DESC
            LIMIT 1
            """,
            (request_id,),
        ).fetchone()
        drift_reasons: list[str] = []
        current_status = service_row["status"] if service_row else None
        packet_status = packet.get("service_status")
        packet_generated_utc = packet.get("generated_utc")
        if not service_row:
            drift_reasons.append("missing_current_service_request")
        else:
            if current_status != packet_status:
                drift_reasons.append("status_changed_since_packet")
            if service_row["assigned_agent_id"]:
                drift_reasons.append("assigned_agent_present")
            if service_row["started_at"]:
                drift_reasons.append("started_at_present")
            if service_row["completed_at"]:
                drift_reasons.append("completed_at_present")
            if packet_generated_utc and service_row["updated_at"] > packet_generated_utc:
                drift_reasons.append("service_request_updated_after_packet")
        if latest_approval:
            drift_reasons.append("approval_or_rejection_record_present")
        rows.append(
            {
                "schema_version": "service_worker_decision_drift_guard_row.v1",
                "generated_utc": generated_utc,
                "source_service_request_id": request_id,
                "lane_id": packet.get("lane_id"),
                "worker_type": packet.get("worker_type"),
                "risk_gate": packet.get("risk_gate"),
                "packet_generated_utc": packet_generated_utc,
                "packet_service_status": packet_status,
                "current_service_status": current_status,
                "current_updated_at": service_row["updated_at"] if service_row else None,
                "current_assigned_agent_id": service_row["assigned_agent_id"] if service_row else None,
                "current_started_at": service_row["started_at"] if service_row else None,
                "current_completed_at": service_row["completed_at"] if service_row else None,
                "latest_approval_id": latest_approval["approval_id"] if latest_approval else None,
                "latest_approval_status": latest_approval["status"] if latest_approval else None,
                "latest_approval_created_at": latest_approval["created_at"] if latest_approval else None,
                "packet_stale": bool(drift_reasons),
                "drift_reasons": drift_reasons,
                "recommended_recovery_command_previews": [
                    ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-gate-map"],
                    ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-human-decision-packets"],
                    ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-post-decision-simulation"],
                    ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-post-decision-refresh-plan"],
                    ["python", str(ROOT / "tools" / "agent_company.py"), "write-service-worker-chain-integrity"],
                ],
                "would_execute_recovery_commands_by_report": False,
                "chain_integrity_all_checks_passed": integrity_ok,
                "refresh_plan_preconditions_passed": refresh_ok,
                "approval_granted_by_drift_guard": False,
                "rejection_granted_by_drift_guard": False,
                "recovery_commands_run_by_drift_guard": 0,
                "pools_registered_by_drift_guard": 0,
                "service_requests_assigned_by_drift_guard": 0,
                "service_requests_updated_by_drift_guard": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    source_state = {
        "human_decision_packets_loaded": human_payload is not None,
        "human_decision_packets_generated_utc": human_payload.get("generated_utc") if human_payload else None,
        "post_decision_refresh_plan_validation_loaded": refresh_payload is not None,
        "post_decision_refresh_plan_failure_count": refresh_payload.get("failure_count") if refresh_payload else None,
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": integrity_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
    }
    return rows, source_state, failures


def write_service_worker_decision_drift_guard(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_DECISION_DRIFT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_DECISION_DRIFT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_DECISION_DRIFT_VALIDATION_JSON
    generated_utc = now_utc()
    rows, source_state, failures = service_worker_decision_drift_rows(conn, generated_utc)
    validation_failures = list(failures)
    drift_check_count = len(rows)
    stale_packet_count = sum(1 for row in rows if row["packet_stale"])
    status_changed_count = sum(1 for row in rows if "status_changed_since_packet" in row["drift_reasons"])
    approval_record_count = sum(1 for row in rows if row["latest_approval_id"])
    assigned_count = sum(1 for row in rows if row["current_assigned_agent_id"])
    started_count = sum(1 for row in rows if row["current_started_at"])
    completed_count = sum(1 for row in rows if row["current_completed_at"])
    updated_after_packet_count = sum(
        1 for row in rows if "service_request_updated_after_packet" in row["drift_reasons"]
    )
    recovery_command_preview_count = sum(len(row["recommended_recovery_command_previews"]) for row in rows)
    all_no_execution = all(not row["would_execute_recovery_commands_by_report"] for row in rows)
    all_preconditions = all(
        row["chain_integrity_all_checks_passed"] and row["refresh_plan_preconditions_passed"]
        for row in rows
    )
    all_packets_current = stale_packet_count == 0
    if drift_check_count != 11:
        validation_failures.append(f"expected 11 decision drift checks, wrote {drift_check_count}")
    if stale_packet_count != 0:
        validation_failures.append(f"expected 0 stale decision packets, found {stale_packet_count}")
    if not all_no_execution:
        validation_failures.append("one or more drift rows would execute recovery commands")
    if not all_preconditions:
        validation_failures.append("one or more drift rows failed input preconditions")

    payload = {
        "schema_version": "service_worker_decision_drift_guard.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_state": source_state,
        "drift_check_count": drift_check_count,
        "stale_packet_count": stale_packet_count,
        "status_changed_count": status_changed_count,
        "approval_record_count": approval_record_count,
        "assigned_count": assigned_count,
        "started_count": started_count,
        "completed_count": completed_count,
        "updated_after_packet_count": updated_after_packet_count,
        "recovery_command_preview_count": recovery_command_preview_count,
        "all_packets_current": all_packets_current,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "drift_rows": rows,
        "execution_notice": "Decision drift guard only. It does not run recovery commands, approve or reject requests, register pools, assign requests, update requests, start workers, call APIs, or perform external actions.",
        "approval_granted_by_drift_guard": False,
        "rejection_granted_by_drift_guard": False,
        "recovery_commands_run_by_drift_guard": 0,
        "pools_registered_by_drift_guard": 0,
        "service_requests_assigned_by_drift_guard": 0,
        "service_requests_updated_by_drift_guard": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_decision_drift_guard_validation.v1",
        "generated_utc": generated_utc,
        "drift_guard_path": str(json_output_path),
        "drift_check_count": drift_check_count,
        "stale_packet_count": stale_packet_count,
        "status_changed_count": status_changed_count,
        "approval_record_count": approval_record_count,
        "assigned_count": assigned_count,
        "started_count": started_count,
        "completed_count": completed_count,
        "updated_after_packet_count": updated_after_packet_count,
        "recovery_command_preview_count": recovery_command_preview_count,
        "all_packets_current": all_packets_current,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "approval_granted_by_drift_guard": False,
        "rejection_granted_by_drift_guard": False,
        "recovery_commands_run_by_drift_guard": 0,
        "pools_registered_by_drift_guard": 0,
        "service_requests_assigned_by_drift_guard": 0,
        "service_requests_updated_by_drift_guard": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Decision Drift Guard",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report compares human/CRO decision packets with live SQLite service-request state. It flags stale packets after status, approval, assignment, start, completion, or update drift. It does not repair drift, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Drift checks: `{drift_check_count}`",
        f"- Stale packets: `{stale_packet_count}`",
        f"- Approval/rejection records found: `{approval_record_count}`",
        f"- Assigned rows: `{assigned_count}`",
        f"- Updated after packet: `{updated_after_packet_count}`",
        f"- Recovery command previews: `{recovery_command_preview_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Drift Rows",
        "",
        "| Request | Packet Status | Current Status | Stale | Reasons |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['source_service_request_id']}`",
                    f"`{row.get('packet_service_status') or ''}`",
                    f"`{row.get('current_service_status') or ''}`",
                    f"`{row['packet_stale']}`",
                    md_cell(", ".join(row["drift_reasons"]) or "none", 220),
                ]
            )
            + " |"
        )
    if validation_failures:
        lines.extend(["", "## Validation Failures", ""])
        for failure in validation_failures:
            lines.append(f"- {failure}")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "If any packet becomes stale, do not use its approve/reject preview. Refresh the gate map, human decision packets, post-decision simulation, post-decision refresh plan, and chain integrity before any manual decision or worker step.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": not validation_failures,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "drift_check_count": drift_check_count,
                "stale_packet_count": stale_packet_count,
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
