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


def service_worker_post_decision_refresh_plan_rows(generated_utc: str) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    simulation_payload, simulation_errors = load_report_json_or_error(SERVICE_WORKER_POST_DECISION_SIMULATION_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = simulation_errors + integrity_errors
    simulations = simulation_payload.get("simulations", []) if simulation_payload else []
    if simulation_payload and not isinstance(simulations, list):
        failures.append("post-decision simulation payload field simulations is not a list")
        simulations = []
    integrity_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if integrity_payload and not integrity_ok:
        failures.append("chain integrity validation is not passing")
    simulation_ok = bool(simulation_payload and len(simulation_payload.get("failures", [])) == 0)
    if simulation_payload and not simulation_ok:
        failures.append("post-decision simulation validation is not passing")

    approval_refresh_commands = [
        "write-service-worker-scope-diff",
        "write-service-worker-gate-map",
        "write-service-worker-pool-registry",
        "write-service-worker-pool-registration-plan",
        "write-service-worker-assignment-plan",
        "write-service-worker-execution-readiness",
        "write-service-worker-chain-integrity",
    ]
    rejection_refresh_commands = [
        "write-service-worker-gate-map",
        "write-service-worker-chain-integrity",
    ]
    approval_remaining_gates = [
        "exact_scope_compatibility_refresh_required",
        "service_worker_pool_registration_required",
        "manual_assignment_required",
        "execution_readiness_required",
        "separate_worker_start_required",
    ]
    rows: list[dict[str, Any]] = []
    for simulation in simulations:
        if not isinstance(simulation, dict):
            continue
        request_id = simulation.get("source_service_request_id")
        if not request_id:
            failures.append("post-decision simulation row is missing source_service_request_id")
            continue
        approval_branch = simulation.get("approval_simulation", {})
        rejection_branch = simulation.get("rejection_simulation", {})
        approval_steps = [
            {
                "order": 1,
                "step_id": "confirm_manual_approval_record",
                "command_preview_argv": None,
                "requires_human_completed_decision": True,
                "would_execute_by_report": False,
                "expected_gate_after_step": "approval_record_exists_or_stop",
            }
        ]
        approval_steps.extend(
            {
                "order": index + 2,
                "step_id": command,
                "command_preview_argv": ["python", str(ROOT / "tools" / "agent_company.py"), command],
                "requires_human_completed_decision": True,
                "would_execute_by_report": False,
                "expected_gate_after_step": approval_remaining_gates[min(index, len(approval_remaining_gates) - 1)],
            }
            for index, command in enumerate(approval_refresh_commands)
        )
        approval_steps.append(
            {
                "order": len(approval_steps) + 1,
                "step_id": "stop_before_worker_start",
                "command_preview_argv": None,
                "requires_human_completed_decision": True,
                "would_execute_by_report": False,
                "expected_gate_after_step": "separate_worker_start_required",
            }
        )
        rejection_steps = [
            {
                "order": 1,
                "step_id": "confirm_manual_rejection_record",
                "command_preview_argv": None,
                "requires_human_completed_decision": True,
                "would_execute_by_report": False,
                "expected_gate_after_step": "rejection_record_exists_or_stop",
            }
        ]
        rejection_steps.extend(
            {
                "order": index + 2,
                "step_id": command,
                "command_preview_argv": ["python", str(ROOT / "tools" / "agent_company.py"), command],
                "requires_human_completed_decision": True,
                "would_execute_by_report": False,
                "expected_gate_after_step": "terminal_no_execution",
            }
            for index, command in enumerate(rejection_refresh_commands)
        )
        rows.append(
            {
                "schema_version": "service_worker_post_decision_refresh_plan_row.v1",
                "generated_utc": generated_utc,
                "source_service_request_id": request_id,
                "lane_id": simulation.get("lane_id"),
                "worker_type": simulation.get("worker_type"),
                "risk_gate": simulation.get("risk_gate"),
                "recommended_worker_pool_id": simulation.get("recommended_worker_pool_id"),
                "approval_expected_status_if_human_runs_later": approval_branch.get("expected_status_if_human_runs_approve_later"),
                "rejection_expected_status_if_human_runs_later": rejection_branch.get("expected_status_if_human_runs_reject_later"),
                "approval_refresh_steps": approval_steps,
                "rejection_refresh_steps": rejection_steps,
                "approval_refresh_command_preview_count": len(approval_refresh_commands),
                "rejection_refresh_command_preview_count": len(rejection_refresh_commands),
                "approval_remaining_gates_after_refresh_plan": approval_remaining_gates,
                "rejection_remaining_gates_after_refresh_plan": [],
                "chain_integrity_all_checks_passed": integrity_ok,
                "post_decision_simulation_preconditions_passed": simulation_ok
                and simulation.get("chain_integrity_all_checks_passed") is True
                and simulation.get("human_decision_packet_preconditions_passed") is True,
                "would_execute_refresh_commands_by_report": False,
                "approval_granted_by_refresh_plan": False,
                "rejection_granted_by_refresh_plan": False,
                "refresh_commands_run_by_plan": 0,
                "pools_registered_by_refresh_plan": 0,
                "service_requests_assigned_by_refresh_plan": 0,
                "service_requests_updated_by_refresh_plan": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    source_state = {
        "post_decision_simulation_loaded": simulation_payload is not None,
        "post_decision_simulation_generated_utc": simulation_payload.get("generated_utc") if simulation_payload else None,
        "post_decision_simulation_failure_count": len(simulation_payload.get("failures", [])) if simulation_payload else None,
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": integrity_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
    }
    return rows, source_state, failures


def write_service_worker_post_decision_refresh_plan(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_POST_DECISION_REFRESH_PLAN_VALIDATION_JSON
    generated_utc = now_utc()
    rows, source_state, failures = service_worker_post_decision_refresh_plan_rows(generated_utc)
    validation_failures = list(failures)
    refresh_plan_count = len(rows)
    approval_sequence_count = sum(1 for row in rows if row.get("approval_refresh_steps"))
    rejection_sequence_count = sum(1 for row in rows if row.get("rejection_refresh_steps"))
    approval_command_preview_count = sum(row.get("approval_refresh_command_preview_count", 0) for row in rows)
    rejection_command_preview_count = sum(row.get("rejection_refresh_command_preview_count", 0) for row in rows)
    command_preview_count = approval_command_preview_count + rejection_command_preview_count
    if refresh_plan_count != 11:
        validation_failures.append(f"expected 11 post-decision refresh plans, wrote {refresh_plan_count}")
    if approval_sequence_count != 11:
        validation_failures.append(f"expected 11 approval refresh sequences, wrote {approval_sequence_count}")
    if rejection_sequence_count != 11:
        validation_failures.append(f"expected 11 rejection refresh sequences, wrote {rejection_sequence_count}")
    if command_preview_count != 99:
        validation_failures.append(f"expected 99 refresh command previews, wrote {command_preview_count}")
    all_no_execution = all(not row["would_execute_refresh_commands_by_report"] for row in rows)
    all_preconditions = all(
        row["chain_integrity_all_checks_passed"] and row["post_decision_simulation_preconditions_passed"]
        for row in rows
    )
    all_start_blocked = all(
        "separate_worker_start_required" in row["approval_remaining_gates_after_refresh_plan"]
        for row in rows
    )
    if not all_no_execution:
        validation_failures.append("one or more refresh plans would execute commands")
    if not all_preconditions:
        validation_failures.append("one or more refresh plans failed input preconditions")
    if not all_start_blocked:
        validation_failures.append("one or more refresh plans failed to preserve the worker-start gate")

    payload = {
        "schema_version": "service_worker_post_decision_refresh_plan.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_state": source_state,
        "refresh_plan_count": refresh_plan_count,
        "approval_sequence_count": approval_sequence_count,
        "rejection_sequence_count": rejection_sequence_count,
        "approval_command_preview_count": approval_command_preview_count,
        "rejection_command_preview_count": rejection_command_preview_count,
        "command_preview_count": command_preview_count,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "all_worker_starts_remain_blocked": all_start_blocked,
        "refresh_plans": rows,
        "execution_notice": "Post-decision refresh plan only. It does not run refresh commands, grant approvals or rejections, register pools, assign requests, update requests, start workers, call APIs, or perform external actions.",
        "approval_granted_by_refresh_plan": False,
        "rejection_granted_by_refresh_plan": False,
        "refresh_commands_run_by_plan": 0,
        "pools_registered_by_refresh_plan": 0,
        "service_requests_assigned_by_refresh_plan": 0,
        "service_requests_updated_by_refresh_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_post_decision_refresh_plan_validation.v1",
        "generated_utc": generated_utc,
        "refresh_plan_path": str(json_output_path),
        "refresh_plan_count": refresh_plan_count,
        "approval_sequence_count": approval_sequence_count,
        "rejection_sequence_count": rejection_sequence_count,
        "approval_command_preview_count": approval_command_preview_count,
        "rejection_command_preview_count": rejection_command_preview_count,
        "command_preview_count": command_preview_count,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "all_worker_starts_remain_blocked": all_start_blocked,
        "approval_granted_by_refresh_plan": False,
        "rejection_granted_by_refresh_plan": False,
        "refresh_commands_run_by_plan": 0,
        "pools_registered_by_refresh_plan": 0,
        "service_requests_assigned_by_refresh_plan": 0,
        "service_requests_updated_by_refresh_plan": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Post-Decision Refresh Plan",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report tells the CEO/CRO which local reports to refresh after a human manually approves or rejects a service-worker decision packet. It does not run those commands, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Refresh plans: `{refresh_plan_count}`",
        f"- Approval sequences: `{approval_sequence_count}`",
        f"- Rejection sequences: `{rejection_sequence_count}`",
        f"- Command previews: `{command_preview_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Refresh Rows",
        "",
        "| Request | Approval Refresh Commands | Rejection Refresh Commands | Start Gate |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        approval_commands = ", ".join(step["step_id"] for step in row["approval_refresh_steps"] if step["command_preview_argv"])
        rejection_commands = ", ".join(step["step_id"] for step in row["rejection_refresh_steps"] if step["command_preview_argv"])
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['source_service_request_id']}`",
                    md_cell(approval_commands, 260),
                    md_cell(rejection_commands, 180),
                    "`separate_worker_start_required`",
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
            "After any manual approve/reject command is run by a human/CRO, refresh the listed local reports and re-run chain integrity before assigning a service request or starting a worker. This plan itself is only a checklist.",
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
                "refresh_plan_count": refresh_plan_count,
                "command_preview_count": command_preview_count,
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
