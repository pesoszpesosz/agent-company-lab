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


def service_worker_decision_command_safety_rows(
    generated_utc: str,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    human_payload, human_errors = load_report_json_or_error(SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON)
    drift_payload, drift_errors = load_report_json_or_error(SERVICE_WORKER_DECISION_DRIFT_VALIDATION_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = human_errors + drift_errors + integrity_errors
    packets = human_payload.get("decision_packets", []) if human_payload else []
    if human_payload and not isinstance(packets, list):
        failures.append("human decision payload field decision_packets is not a list")
        packets = []
    drift_ok = bool(drift_payload and drift_payload.get("failure_count") == 0)
    integrity_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if drift_payload and not drift_ok:
        failures.append("decision drift guard validation is not passing")
    if integrity_payload and not integrity_ok:
        failures.append("chain integrity validation is not passing")

    placeholder = "REPLACE_WITH_MANUALLY_REVIEWED_EXACT_SCOPE_FROM_SUGGESTED_SCOPE"
    rows: list[dict[str, Any]] = []
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        request_id = packet.get("source_service_request_id")
        if not request_id:
            failures.append("human decision packet is missing source_service_request_id")
            continue
        approve_argv = packet.get("approve_command_preview_argv", [])
        reject_argv = packet.get("reject_command_preview_argv", [])
        if not isinstance(approve_argv, list):
            approve_argv = []
        if not isinstance(reject_argv, list):
            reject_argv = []
        approve_placeholder_present = placeholder in approve_argv
        approve_has_exact_scope_flag = "--exact-scope" in approve_argv
        reject_has_reason_flag = "--reason" in reject_argv
        safety_findings: list[str] = []
        if approve_placeholder_present:
            safety_findings.append("approve_exact_scope_placeholder_present")
        if not approve_has_exact_scope_flag:
            safety_findings.append("approve_exact_scope_flag_missing")
        if reject_has_reason_flag:
            safety_findings.append("reject_reason_requires_manual_review")
        rows.append(
            {
                "schema_version": "service_worker_decision_command_safety_row.v1",
                "generated_utc": generated_utc,
                "source_service_request_id": request_id,
                "lane_id": packet.get("lane_id"),
                "worker_type": packet.get("worker_type"),
                "risk_gate": packet.get("risk_gate"),
                "review_route": packet.get("review_route"),
                "approve_command_preview_argv": approve_argv,
                "reject_command_preview_argv": reject_argv,
                "approve_exact_scope_placeholder_present": approve_placeholder_present,
                "approve_exact_scope_flag_present": approve_has_exact_scope_flag,
                "approve_requires_exact_scope_replacement": approve_placeholder_present,
                "reject_requires_reason_review": reject_has_reason_flag,
                "approve_command_directly_runnable": False,
                "reject_command_directly_runnable": False,
                "manual_review_required_before_any_command": True,
                "drift_guard_all_checks_passed": drift_ok,
                "chain_integrity_all_checks_passed": integrity_ok,
                "safety_findings": safety_findings,
                "would_execute_decision_command_by_report": False,
                "approval_granted_by_command_safety": False,
                "rejection_granted_by_command_safety": False,
                "decision_commands_run_by_safety": 0,
                "pools_registered_by_command_safety": 0,
                "service_requests_assigned_by_command_safety": 0,
                "service_requests_updated_by_command_safety": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    source_state = {
        "human_decision_packets_loaded": human_payload is not None,
        "human_decision_packets_generated_utc": human_payload.get("generated_utc") if human_payload else None,
        "decision_drift_guard_validation_loaded": drift_payload is not None,
        "decision_drift_guard_failure_count": drift_payload.get("failure_count") if drift_payload else None,
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": integrity_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
    }
    return rows, source_state, failures


def write_service_worker_decision_command_safety(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_DECISION_COMMAND_SAFETY_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_DECISION_COMMAND_SAFETY_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SERVICE_WORKER_DECISION_COMMAND_SAFETY_VALIDATION_JSON
    generated_utc = now_utc()
    rows, source_state, failures = service_worker_decision_command_safety_rows(generated_utc)
    validation_failures = list(failures)
    command_review_count = len(rows)
    approve_command_count = sum(1 for row in rows if row["approve_command_preview_argv"])
    reject_command_count = sum(1 for row in rows if row["reject_command_preview_argv"])
    decision_command_count = approve_command_count + reject_command_count
    approve_placeholder_scope_count = sum(1 for row in rows if row["approve_exact_scope_placeholder_present"])
    approve_requires_scope_replacement_count = sum(1 for row in rows if row["approve_requires_exact_scope_replacement"])
    reject_requires_reason_review_count = sum(1 for row in rows if row["reject_requires_reason_review"])
    directly_runnable_approve_count = sum(1 for row in rows if row["approve_command_directly_runnable"])
    directly_runnable_reject_count = sum(1 for row in rows if row["reject_command_directly_runnable"])
    all_commands_require_manual_review = all(row["manual_review_required_before_any_command"] for row in rows)
    all_approve_commands_require_scope_replacement = all(
        row["approve_requires_exact_scope_replacement"] for row in rows
    )
    all_no_execution = all(not row["would_execute_decision_command_by_report"] for row in rows)
    all_preconditions = all(
        row["drift_guard_all_checks_passed"] and row["chain_integrity_all_checks_passed"] for row in rows
    )
    if command_review_count != 11:
        validation_failures.append(f"expected 11 command safety reviews, wrote {command_review_count}")
    if decision_command_count != 22:
        validation_failures.append(f"expected 22 decision command previews, wrote {decision_command_count}")
    if approve_placeholder_scope_count != 11:
        validation_failures.append(f"expected 11 approve placeholder scopes, found {approve_placeholder_scope_count}")
    if directly_runnable_approve_count != 0:
        validation_failures.append(f"expected 0 directly runnable approve commands, found {directly_runnable_approve_count}")
    if directly_runnable_reject_count != 0:
        validation_failures.append(f"expected 0 directly runnable reject commands, found {directly_runnable_reject_count}")
    if not all_commands_require_manual_review:
        validation_failures.append("one or more decision command previews did not require manual review")
    if not all_approve_commands_require_scope_replacement:
        validation_failures.append("one or more approve command previews did not require exact-scope replacement")
    if not all_no_execution:
        validation_failures.append("one or more command-safety rows would execute a command")
    if not all_preconditions:
        validation_failures.append("one or more command-safety rows failed input preconditions")

    payload = {
        "schema_version": "service_worker_decision_command_safety.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_state": source_state,
        "command_review_count": command_review_count,
        "approve_command_count": approve_command_count,
        "reject_command_count": reject_command_count,
        "decision_command_count": decision_command_count,
        "approve_placeholder_scope_count": approve_placeholder_scope_count,
        "approve_requires_scope_replacement_count": approve_requires_scope_replacement_count,
        "reject_requires_reason_review_count": reject_requires_reason_review_count,
        "directly_runnable_approve_count": directly_runnable_approve_count,
        "directly_runnable_reject_count": directly_runnable_reject_count,
        "all_commands_require_manual_review": all_commands_require_manual_review,
        "all_approve_commands_require_scope_replacement": all_approve_commands_require_scope_replacement,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "command_safety_rows": rows,
        "execution_notice": "Decision command safety report only. It does not run approve/reject commands, grant approvals or rejections, register pools, assign requests, update requests, start workers, call APIs, or perform external actions.",
        "approval_granted_by_command_safety": False,
        "rejection_granted_by_command_safety": False,
        "decision_commands_run_by_safety": 0,
        "pools_registered_by_command_safety": 0,
        "service_requests_assigned_by_command_safety": 0,
        "service_requests_updated_by_command_safety": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_decision_command_safety_validation.v1",
        "generated_utc": generated_utc,
        "command_safety_path": str(json_output_path),
        "command_review_count": command_review_count,
        "approve_command_count": approve_command_count,
        "reject_command_count": reject_command_count,
        "decision_command_count": decision_command_count,
        "approve_placeholder_scope_count": approve_placeholder_scope_count,
        "approve_requires_scope_replacement_count": approve_requires_scope_replacement_count,
        "reject_requires_reason_review_count": reject_requires_reason_review_count,
        "directly_runnable_approve_count": directly_runnable_approve_count,
        "directly_runnable_reject_count": directly_runnable_reject_count,
        "all_commands_require_manual_review": all_commands_require_manual_review,
        "all_approve_commands_require_scope_replacement": all_approve_commands_require_scope_replacement,
        "all_no_execution": all_no_execution,
        "all_input_preconditions_passed": all_preconditions,
        "approval_granted_by_command_safety": False,
        "rejection_granted_by_command_safety": False,
        "decision_commands_run_by_safety": 0,
        "pools_registered_by_command_safety": 0,
        "service_requests_assigned_by_command_safety": 0,
        "service_requests_updated_by_command_safety": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Decision Command Safety",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report reviews approve/reject command previews for human decision packets. It marks approve previews as not directly runnable while they contain the exact-scope placeholder, and marks all decision commands as requiring manual review. It does not run approve/reject commands, grant approvals or rejections, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Command reviews: `{command_review_count}`",
        f"- Decision command previews: `{decision_command_count}`",
        f"- Approve placeholders requiring replacement: `{approve_placeholder_scope_count}`",
        f"- Directly runnable approve commands: `{directly_runnable_approve_count}`",
        f"- Directly runnable reject commands: `{directly_runnable_reject_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Command Safety Rows",
        "",
        "| Request | Approve Needs Scope | Reject Needs Review | Directly Runnable | Findings |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['source_service_request_id']}`",
                    f"`{row['approve_requires_exact_scope_replacement']}`",
                    f"`{row['reject_requires_reason_review']}`",
                    "`False`",
                    md_cell(", ".join(row["safety_findings"]) or "none", 220),
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
            "Before any human/CRO runs an approve command, replace the exact-scope placeholder with a reviewed scope from the packet and rerun drift guard. Reject commands also require manual reason review. This report itself is only a safety review.",
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
                "command_review_count": command_review_count,
                "decision_command_count": decision_command_count,
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
