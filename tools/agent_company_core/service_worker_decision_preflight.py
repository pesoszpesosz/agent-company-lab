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


def service_worker_decision_preflight_rows(
    generated_utc: str,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    drift_payload, drift_errors = load_report_json_or_error(SERVICE_WORKER_DECISION_DRIFT_JSON)
    command_payload, command_errors = load_report_json_or_error(SERVICE_WORKER_DECISION_COMMAND_SAFETY_JSON)
    authority_payload, authority_errors = load_report_json_or_error(SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = drift_errors + command_errors + authority_errors + integrity_errors
    drift_rows = drift_payload.get("drift_rows", []) if drift_payload else []
    command_rows = command_payload.get("command_safety_rows", []) if command_payload else []
    authority_rows = authority_payload.get("authority_rows", []) if authority_payload else []
    for label, rows in [
        ("decision drift guard", drift_rows),
        ("decision command safety", command_rows),
        ("decision authority matrix", authority_rows),
    ]:
        if not isinstance(rows, list):
            failures.append(f"{label} rows field is not a list")
    drift_by_request = {
        row.get("source_service_request_id"): row
        for row in drift_rows
        if isinstance(row, dict) and row.get("source_service_request_id")
    }
    command_by_request = {
        row.get("source_service_request_id"): row
        for row in command_rows
        if isinstance(row, dict) and row.get("source_service_request_id")
    }
    authority_by_request = {
        row.get("source_service_request_id"): row
        for row in authority_rows
        if isinstance(row, dict) and row.get("source_service_request_id")
    }
    all_request_ids = sorted(set(drift_by_request) | set(command_by_request) | set(authority_by_request))
    integrity_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if integrity_payload and not integrity_ok:
        failures.append("chain integrity validation is not passing")

    rows: list[dict[str, Any]] = []
    for request_id in all_request_ids:
        drift = drift_by_request.get(request_id)
        command = command_by_request.get(request_id)
        authority = authority_by_request.get(request_id)
        missing_sources = []
        if not drift:
            missing_sources.append("decision_drift_guard")
        if not command:
            missing_sources.append("decision_command_safety")
        if not authority:
            missing_sources.append("decision_authority_matrix")
        packet_current = bool(drift and drift.get("packet_stale") is False)
        command_safe_for_review = bool(
            command
            and command.get("manual_review_required_before_any_command") is True
            and command.get("approve_command_directly_runnable") is False
            and command.get("reject_command_directly_runnable") is False
        )
        authority_classified = bool(authority and authority.get("authority_roles_present") is True)
        preflight_passed = bool(
            not missing_sources
            and packet_current
            and command_safe_for_review
            and authority_classified
            and integrity_ok
        )
        manual_decision_blockers = list(missing_sources)
        if not packet_current:
            manual_decision_blockers.append("packet_not_current")
        if not command_safe_for_review:
            manual_decision_blockers.append("command_safety_not_ready")
        if not authority_classified:
            manual_decision_blockers.append("authority_not_classified")
        if not integrity_ok:
            manual_decision_blockers.append("chain_integrity_not_passing")
        manual_decision_ready = bool(
            preflight_passed
            and authority
            and authority.get("cro_required") is True
            and command
            and command.get("approve_requires_exact_scope_replacement") is True
        )
        rows.append(
            {
                "schema_version": "service_worker_decision_preflight_row.v1",
                "generated_utc": generated_utc,
                "source_service_request_id": request_id,
                "lane_id": (authority or drift or command or {}).get("lane_id"),
                "worker_type": (authority or drift or command or {}).get("worker_type"),
                "risk_gate": (authority or drift or command or {}).get("risk_gate"),
                "packet_current": packet_current,
                "command_safe_for_manual_review": command_safe_for_review,
                "authority_classified": authority_classified,
                "required_authorities": authority.get("required_authorities", []) if authority else [],
                "authority_route": authority.get("authority_route") if authority else None,
                "manual_decision_preflight_passed": preflight_passed,
                "manual_decision_ready_for_human_review": manual_decision_ready,
                "manual_decision_blockers": manual_decision_blockers,
                "execution_allowed_by_preflight": False,
                "assignment_allowed_by_preflight": False,
                "worker_start_allowed_by_preflight": False,
                "chain_integrity_all_checks_passed": integrity_ok,
                "decision_authority_granted_by_preflight": False,
                "approval_granted_by_preflight": False,
                "rejection_granted_by_preflight": False,
                "pools_registered_by_preflight": 0,
                "service_requests_assigned_by_preflight": 0,
                "service_requests_updated_by_preflight": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    source_state = {
        "decision_drift_guard_loaded": drift_payload is not None,
        "decision_drift_guard_generated_utc": drift_payload.get("generated_utc") if drift_payload else None,
        "decision_command_safety_loaded": command_payload is not None,
        "decision_command_safety_generated_utc": command_payload.get("generated_utc") if command_payload else None,
        "decision_authority_matrix_loaded": authority_payload is not None,
        "decision_authority_matrix_generated_utc": authority_payload.get("generated_utc") if authority_payload else None,
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": integrity_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
    }
    return rows, source_state, failures


def write_service_worker_decision_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_DECISION_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_DECISION_PREFLIGHT_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_DECISION_PREFLIGHT_VALIDATION_JSON
    generated_utc = now_utc()
    rows, source_state, failures = service_worker_decision_preflight_rows(generated_utc)
    validation_failures = list(failures)
    preflight_count = len(rows)
    ready_for_human_review_count = sum(1 for row in rows if row["manual_decision_ready_for_human_review"])
    preflight_passed_count = sum(1 for row in rows if row["manual_decision_preflight_passed"])
    execution_allowed_count = sum(1 for row in rows if row["execution_allowed_by_preflight"])
    assignment_allowed_count = sum(1 for row in rows if row["assignment_allowed_by_preflight"])
    worker_start_allowed_count = sum(1 for row in rows if row["worker_start_allowed_by_preflight"])
    blocked_count = sum(1 for row in rows if row["manual_decision_blockers"])
    all_no_execution = execution_allowed_count == 0 and assignment_allowed_count == 0 and worker_start_allowed_count == 0
    all_preconditions = all(row["chain_integrity_all_checks_passed"] for row in rows)
    if preflight_count != 11:
        validation_failures.append(f"expected 11 decision preflight rows, wrote {preflight_count}")
    if ready_for_human_review_count != 11:
        validation_failures.append(
            f"expected 11 rows ready for human review, found {ready_for_human_review_count}"
        )
    if preflight_passed_count != 11:
        validation_failures.append(f"expected 11 preflight-passed rows, found {preflight_passed_count}")
    if blocked_count != 0:
        validation_failures.append(f"expected 0 blocked preflight rows, found {blocked_count}")
    if not all_no_execution:
        validation_failures.append("one or more preflight rows allowed execution, assignment, or worker start")
    if not all_preconditions:
        validation_failures.append("one or more preflight rows failed input preconditions")

    payload = {
        "schema_version": "service_worker_decision_preflight.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_state": source_state,
        "preflight_count": preflight_count,
        "ready_for_human_review_count": ready_for_human_review_count,
        "preflight_passed_count": preflight_passed_count,
        "blocked_count": blocked_count,
        "execution_allowed_count": execution_allowed_count,
        "assignment_allowed_count": assignment_allowed_count,
        "worker_start_allowed_count": worker_start_allowed_count,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "preflight_rows": rows,
        "execution_notice": "Decision preflight only. It does not grant authority, approve or reject requests, register pools, assign requests, update requests, start workers, call APIs, or perform external actions.",
        "decision_authority_granted_by_preflight": False,
        "approval_granted_by_preflight": False,
        "rejection_granted_by_preflight": False,
        "pools_registered_by_preflight": 0,
        "service_requests_assigned_by_preflight": 0,
        "service_requests_updated_by_preflight": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_decision_preflight_validation.v1",
        "generated_utc": generated_utc,
        "preflight_path": str(json_output_path),
        "preflight_count": preflight_count,
        "ready_for_human_review_count": ready_for_human_review_count,
        "preflight_passed_count": preflight_passed_count,
        "blocked_count": blocked_count,
        "execution_allowed_count": execution_allowed_count,
        "assignment_allowed_count": assignment_allowed_count,
        "worker_start_allowed_count": worker_start_allowed_count,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "decision_authority_granted_by_preflight": False,
        "approval_granted_by_preflight": False,
        "rejection_granted_by_preflight": False,
        "pools_registered_by_preflight": 0,
        "service_requests_assigned_by_preflight": 0,
        "service_requests_updated_by_preflight": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Decision Preflight",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report rolls up decision drift, command safety, and authority classification before a human uses a decision packet. It can mark a packet ready for human review, but it does not grant authority, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Preflight rows: `{preflight_count}`",
        f"- Ready for human review: `{ready_for_human_review_count}`",
        f"- Blocked rows: `{blocked_count}`",
        f"- Execution allowed: `{execution_allowed_count}`",
        f"- Assignment allowed: `{assignment_allowed_count}`",
        f"- Worker starts allowed: `{worker_start_allowed_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Preflight Rows",
        "",
        "| Request | Ready | Authorities | Route | Blockers |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['source_service_request_id']}`",
                    f"`{row['manual_decision_ready_for_human_review']}`",
                    md_cell(", ".join(row["required_authorities"]), 180),
                    md_cell(row.get("authority_route") or "", 180),
                    md_cell(", ".join(row["manual_decision_blockers"]) or "none", 180),
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
            "A human/CRO can use this report as the final local checklist before reviewing a decision packet. Replace exact-scope placeholders and rerun drift/command/authority checks before any state-changing command.",
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
                "preflight_count": preflight_count,
                "ready_for_human_review_count": ready_for_human_review_count,
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
