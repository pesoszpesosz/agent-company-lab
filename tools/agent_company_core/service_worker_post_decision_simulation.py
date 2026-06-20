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


def service_worker_post_decision_simulation_rows(generated_utc: str) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    human_payload, human_errors = load_report_json_or_error(SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = human_errors + integrity_errors
    packets = human_payload.get("decision_packets", []) if human_payload else []
    if human_payload and not isinstance(packets, list):
        failures.append("human decision payload field decision_packets is not a list")
        packets = []
    integrity_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if integrity_payload and not integrity_ok:
        failures.append("chain integrity validation is not passing")
    simulations: list[dict[str, Any]] = []
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        request_id = packet.get("source_service_request_id")
        if not request_id:
            failures.append("human decision packet is missing source_service_request_id")
            continue
        approval_simulation = {
            "branch": "manual_approve_preview",
            "would_execute_command": False,
            "would_grant_approval_by_report": False,
            "would_update_service_request_by_report": False,
            "would_register_pool_by_report": False,
            "would_assign_service_request_by_report": False,
            "would_start_worker_by_report": False,
            "expected_status_if_human_runs_approve_later": "approved",
            "gates_cleared_if_human_approves_later": ["human_cro_approval_required"],
            "remaining_gates_after_human_approval": [
                "exact_scope_compatibility_refresh_required",
                "service_worker_pool_registration_required",
                "manual_assignment_required",
                "execution_readiness_required",
                "separate_worker_start_required",
            ],
            "next_report_to_refresh_after_manual_approval": "write-service-worker-scope-diff",
            "reason": "Approval would only be valid if a human/CRO manually runs the approve preview with reviewed exact scope; this simulator does not run it.",
        }
        rejection_simulation = {
            "branch": "manual_reject_preview",
            "would_execute_command": False,
            "would_grant_rejection_by_report": False,
            "would_update_service_request_by_report": False,
            "would_register_pool_by_report": False,
            "would_assign_service_request_by_report": False,
            "would_start_worker_by_report": False,
            "expected_status_if_human_runs_reject_later": "rejected",
            "gates_cleared_if_human_rejects_later": ["terminal_no_execution"],
            "remaining_gates_after_human_rejection": [],
            "next_report_to_refresh_after_manual_rejection": "write-service-worker-gate-map",
            "reason": "Rejection would be terminal for this service request if a human/CRO manually runs the reject preview; this simulator does not run it.",
        }
        simulations.append(
            {
                "schema_version": "service_worker_post_decision_simulation_row.v1",
                "generated_utc": generated_utc,
                "source_service_request_id": request_id,
                "lane_id": packet.get("lane_id"),
                "worker_type": packet.get("worker_type"),
                "risk_gate": packet.get("risk_gate"),
                "review_route": packet.get("review_route"),
                "current_blocking_gate": packet.get("current_blocking_gate"),
                "recommended_worker_pool_id": packet.get("recommended_worker_pool_id"),
                "pool_status": packet.get("pool_status"),
                "scope_diff_route": packet.get("scope_diff_route"),
                "approve_command_preview_argv": packet.get("approve_command_preview_argv", []),
                "reject_command_preview_argv": packet.get("reject_command_preview_argv", []),
                "approval_simulation": approval_simulation,
                "rejection_simulation": rejection_simulation,
                "chain_integrity_all_checks_passed": integrity_ok,
                "human_decision_packet_preconditions_passed": packet.get("all_preconditions_for_human_decision_packet") is True,
                "approval_granted_by_simulation": False,
                "rejection_granted_by_simulation": False,
                "pools_registered_by_simulation": 0,
                "service_requests_assigned_by_simulation": 0,
                "service_requests_updated_by_simulation": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    source_state = {
        "human_decision_packets_loaded": human_payload is not None,
        "human_decision_packets_generated_utc": human_payload.get("generated_utc") if human_payload else None,
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": integrity_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
    }
    return simulations, source_state, failures


def write_service_worker_post_decision_simulation(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_POST_DECISION_SIMULATION_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_POST_DECISION_SIMULATION_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_POST_DECISION_SIMULATION_VALIDATION_JSON
    generated_utc = now_utc()
    simulations, source_state, failures = service_worker_post_decision_simulation_rows(generated_utc)
    branch_count = len(simulations) * 2
    validation_failures = list(failures)
    if len(simulations) != 11:
        validation_failures.append(f"expected 11 post-decision simulations, wrote {len(simulations)}")
    if branch_count != 22:
        validation_failures.append(f"expected 22 approve/reject branches, wrote {branch_count}")
    all_no_execution = all(
        not row["approval_simulation"]["would_execute_command"]
        and not row["rejection_simulation"]["would_execute_command"]
        for row in simulations
    )
    all_preconditions = all(
        row["chain_integrity_all_checks_passed"] and row["human_decision_packet_preconditions_passed"]
        for row in simulations
    )
    if not all_no_execution:
        validation_failures.append("one or more simulation branches would execute a command")
    if not all_preconditions:
        validation_failures.append("one or more simulation rows failed input preconditions")
    payload = {
        "schema_version": "service_worker_post_decision_simulation.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_state": source_state,
        "simulation_count": len(simulations),
        "branch_count": branch_count,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "simulations": simulations,
        "execution_notice": "Post-decision simulation only. It does not run approve/reject previews, grant approval/rejection, register pools, assign requests, update requests, start workers, call APIs, or perform external actions.",
        "approval_granted_by_simulation": False,
        "rejection_granted_by_simulation": False,
        "pools_registered_by_simulation": 0,
        "service_requests_assigned_by_simulation": 0,
        "service_requests_updated_by_simulation": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_post_decision_simulation_validation.v1",
        "generated_utc": generated_utc,
        "simulation_path": str(json_output_path),
        "simulation_count": len(simulations),
        "branch_count": branch_count,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "approval_granted_by_simulation": False,
        "rejection_granted_by_simulation": False,
        "pools_registered_by_simulation": 0,
        "service_requests_assigned_by_simulation": 0,
        "service_requests_updated_by_simulation": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Post-Decision Simulation",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report simulates what would remain after a human manually approves or rejects a decision packet. It does not run approve/reject commands, grant approvals or rejections, register pools, assign service requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Simulations: `{len(simulations)}`",
        f"- Branches: `{branch_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Simulation Rows",
        "",
        "| Request | Approve Branch Remaining Gates | Reject Branch Result | Pool |",
        "| --- | --- | --- | --- |",
    ]
    for row in simulations:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['source_service_request_id']}`",
                    md_cell(", ".join(row["approval_simulation"]["remaining_gates_after_human_approval"]), 260),
                    f"`{row['rejection_simulation']['expected_status_if_human_runs_reject_later']}`",
                    f"`{row.get('recommended_worker_pool_id') or ''}`",
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
            "If a human/CRO manually approves a request later, refresh scope diff, gate map, pool registration, assignment plan, readiness, and chain integrity before any assignment or worker start. If a human/CRO manually rejects it, refresh the gate map and chain integrity to confirm terminal no-execution state.",
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
                "simulation_count": len(simulations),
                "branch_count": branch_count,
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
