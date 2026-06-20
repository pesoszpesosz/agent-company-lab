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


def service_worker_decision_authority_for_packet(packet: dict[str, Any]) -> dict[str, Any]:
    risk_gate = packet.get("risk_gate") or ""
    worker_type = packet.get("worker_type") or ""
    required_authorities = ["chief_risk_officer"]
    authority_route = "cro_review_required"
    if risk_gate == "catalog_required_approval_no_external_action":
        required_authorities = ["chief_risk_officer"]
        authority_route = "cro_can_approve_after_exact_scope_review"
    elif risk_gate == "browser_grok_or_x_requires_signed_in_browser_and_no_public_actions":
        required_authorities = ["human_user", "chief_risk_officer"]
        authority_route = "human_user_and_cro_required_signed_in_browser"
    elif risk_gate == "legal_kyc_tax_payment_requires_user_decision_no_commitment":
        required_authorities = ["human_user", "chief_risk_officer"]
        authority_route = "human_user_and_cro_required_legal_payment"
    elif risk_gate == "security_report_submission_requires_user_and_cro_approval_no_submission":
        required_authorities = ["human_user", "chief_risk_officer", "reputation_review_worker"]
        authority_route = "human_user_cro_and_reputation_review_required"
    elif risk_gate == "model_api_call_requires_provider_model_cost_lane_and_artifact_scope":
        required_authorities = ["human_user", "chief_risk_officer", "ceo_orchestrator"]
        authority_route = "human_user_cro_and_ceo_required_model_api_cost"
    elif worker_type in {"public_submission", "legal_kyc_tax_payment_review", "model_api_execution"}:
        required_authorities = ["human_user", "chief_risk_officer"]
        authority_route = "human_user_and_cro_required_high_risk_worker"
    return {
        "required_authorities": required_authorities,
        "authority_route": authority_route,
        "human_user_required": "human_user" in required_authorities,
        "cro_required": "chief_risk_officer" in required_authorities,
        "ceo_required": "ceo_orchestrator" in required_authorities,
        "reputation_review_required": "reputation_review_worker" in required_authorities,
    }


def service_worker_decision_authority_matrix_rows(
    generated_utc: str,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    human_payload, human_errors = load_report_json_or_error(SERVICE_WORKER_HUMAN_DECISION_PACKETS_JSON)
    command_payload, command_errors = load_report_json_or_error(SERVICE_WORKER_DECISION_COMMAND_SAFETY_VALIDATION_JSON)
    integrity_payload, integrity_errors = load_report_json_or_error(SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON)
    failures = human_errors + command_errors + integrity_errors
    packets = human_payload.get("decision_packets", []) if human_payload else []
    if human_payload and not isinstance(packets, list):
        failures.append("human decision payload field decision_packets is not a list")
        packets = []
    command_safety_ok = bool(command_payload and command_payload.get("failure_count") == 0)
    integrity_ok = bool(integrity_payload and integrity_payload.get("all_checks_passed") is True)
    if command_payload and not command_safety_ok:
        failures.append("decision command safety validation is not passing")
    if integrity_payload and not integrity_ok:
        failures.append("chain integrity validation is not passing")
    role_ids = set()
    if ROLE_REGISTRY_PATH.exists():
        try:
            role_payload = json.loads(ROLE_REGISTRY_PATH.read_text(encoding="utf-8"))
            role_ids = {role.get("id") for role in role_payload.get("roles", []) if isinstance(role, dict)}
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON in {ROLE_REGISTRY_PATH}: {exc}")

    rows: list[dict[str, Any]] = []
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        request_id = packet.get("source_service_request_id")
        if not request_id:
            failures.append("human decision packet is missing source_service_request_id")
            continue
        authority = service_worker_decision_authority_for_packet(packet)
        missing_internal_roles = [
            role_id
            for role_id in authority["required_authorities"]
            if role_id != "human_user" and role_id not in role_ids
        ]
        rows.append(
            {
                "schema_version": "service_worker_decision_authority_matrix_row.v1",
                "generated_utc": generated_utc,
                "source_service_request_id": request_id,
                "lane_id": packet.get("lane_id"),
                "worker_type": packet.get("worker_type"),
                "risk_gate": packet.get("risk_gate"),
                "review_route": packet.get("review_route"),
                "required_authorities": authority["required_authorities"],
                "authority_route": authority["authority_route"],
                "human_user_required": authority["human_user_required"],
                "cro_required": authority["cro_required"],
                "ceo_required": authority["ceo_required"],
                "reputation_review_required": authority["reputation_review_required"],
                "missing_internal_role_ids": missing_internal_roles,
                "authority_roles_present": not missing_internal_roles,
                "command_safety_all_checks_passed": command_safety_ok,
                "chain_integrity_all_checks_passed": integrity_ok,
                "decision_authority_granted_by_matrix": False,
                "approval_granted_by_authority_matrix": False,
                "rejection_granted_by_authority_matrix": False,
                "authority_commands_run_by_matrix": 0,
                "pools_registered_by_authority_matrix": 0,
                "service_requests_assigned_by_authority_matrix": 0,
                "service_requests_updated_by_authority_matrix": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            }
        )
    source_state = {
        "human_decision_packets_loaded": human_payload is not None,
        "human_decision_packets_generated_utc": human_payload.get("generated_utc") if human_payload else None,
        "decision_command_safety_validation_loaded": command_payload is not None,
        "decision_command_safety_failure_count": command_payload.get("failure_count") if command_payload else None,
        "chain_integrity_validation_loaded": integrity_payload is not None,
        "chain_integrity_all_checks_passed": integrity_ok,
        "chain_integrity_generated_utc": integrity_payload.get("generated_utc") if integrity_payload else None,
        "role_registry_loaded": ROLE_REGISTRY_PATH.exists(),
    }
    return rows, source_state, failures


def write_service_worker_decision_authority_matrix(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else SERVICE_WORKER_DECISION_AUTHORITY_MATRIX_VALIDATION_JSON
    )
    generated_utc = now_utc()
    rows, source_state, failures = service_worker_decision_authority_matrix_rows(generated_utc)
    validation_failures = list(failures)
    authority_review_count = len(rows)
    human_user_required_count = sum(1 for row in rows if row["human_user_required"])
    cro_required_count = sum(1 for row in rows if row["cro_required"])
    ceo_required_count = sum(1 for row in rows if row["ceo_required"])
    reputation_review_required_count = sum(1 for row in rows if row["reputation_review_required"])
    missing_role_count = sum(len(row["missing_internal_role_ids"]) for row in rows)
    all_roles_present = all(row["authority_roles_present"] for row in rows)
    all_preconditions = all(
        row["command_safety_all_checks_passed"] and row["chain_integrity_all_checks_passed"] for row in rows
    )
    if authority_review_count != 11:
        validation_failures.append(f"expected 11 authority reviews, wrote {authority_review_count}")
    if cro_required_count != 11:
        validation_failures.append(f"expected 11 CRO-required rows, found {cro_required_count}")
    if human_user_required_count != 4:
        validation_failures.append(f"expected 4 human-user-required rows, found {human_user_required_count}")
    if ceo_required_count != 1:
        validation_failures.append(f"expected 1 CEO-required row, found {ceo_required_count}")
    if reputation_review_required_count != 1:
        validation_failures.append(
            f"expected 1 reputation-review-required row, found {reputation_review_required_count}"
        )
    if missing_role_count != 0:
        validation_failures.append(f"expected 0 missing internal role ids, found {missing_role_count}")
    if not all_preconditions:
        validation_failures.append("one or more authority rows failed input preconditions")

    payload = {
        "schema_version": "service_worker_decision_authority_matrix.v1",
        "generated_utc": generated_utc,
        "db": str(DB_PATH),
        "source_state": source_state,
        "authority_review_count": authority_review_count,
        "human_user_required_count": human_user_required_count,
        "cro_required_count": cro_required_count,
        "ceo_required_count": ceo_required_count,
        "reputation_review_required_count": reputation_review_required_count,
        "missing_role_count": missing_role_count,
        "all_authority_roles_present": all_roles_present,
        "all_input_preconditions_passed": all_preconditions,
        "authority_rows": rows,
        "execution_notice": "Decision authority matrix only. It does not grant decision authority, approve or reject requests, register pools, assign requests, update requests, start workers, call APIs, or perform external actions.",
        "decision_authority_granted_by_matrix": False,
        "approval_granted_by_authority_matrix": False,
        "rejection_granted_by_authority_matrix": False,
        "authority_commands_run_by_matrix": 0,
        "pools_registered_by_authority_matrix": 0,
        "service_requests_assigned_by_authority_matrix": 0,
        "service_requests_updated_by_authority_matrix": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failures": validation_failures,
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_payload = {
        "schema_version": "service_worker_decision_authority_matrix_validation.v1",
        "generated_utc": generated_utc,
        "authority_matrix_path": str(json_output_path),
        "authority_review_count": authority_review_count,
        "human_user_required_count": human_user_required_count,
        "cro_required_count": cro_required_count,
        "ceo_required_count": ceo_required_count,
        "reputation_review_required_count": reputation_review_required_count,
        "missing_role_count": missing_role_count,
        "all_authority_roles_present": all_roles_present,
        "all_input_preconditions_passed": all_preconditions,
        "decision_authority_granted_by_matrix": False,
        "approval_granted_by_authority_matrix": False,
        "rejection_granted_by_authority_matrix": False,
        "authority_commands_run_by_matrix": 0,
        "pools_registered_by_authority_matrix": 0,
        "service_requests_assigned_by_authority_matrix": 0,
        "service_requests_updated_by_authority_matrix": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "failure_count": len(validation_failures),
        "failures": validation_failures,
        "source_state": source_state,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Service Worker Decision Authority Matrix",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{DB_PATH}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report maps each pending human/CRO decision packet to required decision authority. It does not grant approval authority, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.",
        "",
        f"- Authority reviews: `{authority_review_count}`",
        f"- CRO-required rows: `{cro_required_count}`",
        f"- Human-user-required rows: `{human_user_required_count}`",
        f"- CEO-required rows: `{ceo_required_count}`",
        f"- Reputation-review-required rows: `{reputation_review_required_count}`",
        f"- Missing internal roles: `{missing_role_count}`",
        f"- Validation failures: `{len(validation_failures)}`",
        f"- Worker starts: `0`",
        f"- API calls: `False`",
        f"- External side effects: `False`",
        "",
        "## Authority Rows",
        "",
        "| Request | Risk Gate | Required Authorities | Route |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['source_service_request_id']}`",
                    f"`{row.get('risk_gate') or ''}`",
                    md_cell(", ".join(row["required_authorities"]), 180),
                    md_cell(row["authority_route"], 180),
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
            "Before any human decision command is run, confirm the required authority route for that packet and re-run command safety plus drift guard. This matrix itself grants no authority.",
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
                "authority_review_count": authority_review_count,
                "failure_count": len(validation_failures),
            },
            indent=2,
        )
    )
