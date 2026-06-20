#!/usr/bin/env python3
"""Validate service-worker approval authority coverage without granting authority."""

from __future__ import annotations

import copy
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
STATE_DB = ROOT / "state" / "agent_company.sqlite"
SCHEMA_PATH = ARCH / "service-worker-approval-authority-coverage-v1.schema.json"
ROLE_REGISTRY = ARCH / "role-registry-draft.json"
REPORT_JSON = REPORTS / "service-worker-approval-authority-coverage-v1-20260617.json"
VALIDATION_JSON = REPORTS / "service-worker-approval-authority-coverage-v1-validation-20260617.json"
REPORT_MD = REPORTS / "service-worker-approval-authority-coverage-v1-20260617.md"

EXTERNAL_AUTHORITIES = {"user", "human_user", "requesting_manager"}

ZERO_BOUNDARY = {
    "report_only": True,
    "approval_granted_by_coverage": False,
    "decision_authority_granted_by_coverage": False,
    "rejection_granted_by_coverage": False,
    "authority_commands_run": 0,
    "approval_rows_written": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "worker_starts": 0,
    "browser_sessions_started": False,
    "api_calls": False,
    "external_side_effects": False,
}
NEXT_ACTION = (
    "Use this catalog-wide authority coverage before generating service-specific signed decision "
    "intake contracts."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def decode_json(value: str) -> Any:
    try:
        return json.loads(value)
    except Exception:
        return value


def role_ids() -> set[str]:
    data = load_json(ROLE_REGISTRY)
    return {role["id"] for role in data.get("roles", [])}


def service_catalog_rows() -> list[dict[str, Any]]:
    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    rows = []
    for row in con.execute(
        """
        SELECT service_id, department_id, name, request_type, owner_role_id, purpose,
               allowed_actions_json, hard_gates_json, required_intake_json,
               approval_required_by_json, output_artifacts_json, default_status
        FROM service_catalog
        ORDER BY service_id
        """
    ):
        item = dict(row)
        item["allowed_actions"] = decode_json(item.pop("allowed_actions_json"))
        item["hard_gates"] = decode_json(item.pop("hard_gates_json"))
        item["required_intake"] = decode_json(item.pop("required_intake_json"))
        item["approval_required_by"] = decode_json(item.pop("approval_required_by_json"))
        item["output_artifacts"] = decode_json(item.pop("output_artifacts_json"))
        rows.append(item)
    con.close()
    return rows


def service_request_rows() -> list[dict[str, Any]]:
    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    rows = [dict(row) for row in con.execute(
        """
        SELECT request_id, service_id, request_type, lane_id, status, risk_gate,
               requested_action, approval_scope, artifact_path, assigned_agent_id,
               started_at, completed_at
        FROM service_requests
        ORDER BY request_id
        """
    )]
    con.close()
    return rows


def normalized_authorities(values: list[str]) -> list[str]:
    result = []
    for value in values:
        if value == "user":
            result.append("human_user")
        elif value == "requesting_manager":
            result.append("requesting_manager")
        else:
            result.append(value)
    return result


def derive_authority_route(service: dict[str, Any]) -> str:
    service_id = service["service_id"]
    request_type = service["request_type"]
    authorities = set(normalized_authorities(service.get("approval_required_by", [])))
    if service_id == "browser_read_only_session":
        return "requesting_manager_and_cro_preflight_only_no_browser_start"
    if service_id in {"public_action_execution", "github_public_action_gate", "outreach_delivery_gate"}:
        return "human_user_cro_reputation_required_exact_public_action_only"
    if service_id in {"wallet_setup_packet", "wallet_public_address_response"}:
        return "human_user_cro_required_wallet_no_key_or_fund_control"
    if service_id in {"real_money_trade_gate", "legal_kyc_tax_payment_gate"}:
        return "human_user_cro_or_user_only_decision_packet_no_commitment"
    if service_id == "model_api_execution_gate":
        return "human_user_cro_observability_required_cost_data_scope"
    if service_id in {
        "security_report_submission_gate",
        "secrets_credentials_handling_gate",
        "data_purchase_api_access_gate",
        "account_registration_intake",
    }:
        return "human_user_cro_required_review_packet_no_external_action"
    if "human_user" in authorities and "chief_risk_officer" in authorities:
        return "human_user_cro_required"
    if request_type:
        return "catalog_authority_route_defined_no_authority_granted"
    return "blocked_missing_service_coverage"


def service_risk_family(service: dict[str, Any]) -> str:
    text = " ".join([
        service["service_id"],
        service["request_type"],
        " ".join(service.get("hard_gates", [])),
        " ".join(service.get("allowed_actions", [])),
    ]).lower()
    if "wallet" in text or "fund" in text or "trade" in text:
        return "wallet_payment_or_real_money"
    if "public" in text or "comment" in text or "reply" in text or "outreach" in text or "github" in text:
        return "public_reputation"
    if "credential" in text or "secret" in text or "api key" in text:
        return "secrets_or_api"
    if "browser" in text:
        return "browser"
    if "security" in text or "vulnerability" in text:
        return "security"
    if "account" in text or "terms" in text or "kyc" in text or "tax" in text:
        return "account_legal"
    return "general_service"


def build_service_row(service: dict[str, Any], known_roles: set[str]) -> dict[str, Any]:
    authorities = normalized_authorities(service.get("approval_required_by", []))
    missing_roles = sorted(
        {
            role
            for role in [service.get("owner_role_id"), *authorities]
            if role not in known_roles and role not in EXTERNAL_AUTHORITIES
        }
    )
    requires_user = "human_user" in authorities or "user" in service.get("approval_required_by", [])
    requires_cro = "chief_risk_officer" in authorities
    route = derive_authority_route(service)
    hard_gate_text = " ".join(service.get("hard_gates", [])).lower()
    hard_gates_block_side_effects = any(
        token in hard_gate_text
        for token in [
            "do not",
            "without explicit",
            "without approved",
            "without a separate exact approval",
        ]
    )
    covered = route != "blocked_missing_service_coverage" and not missing_roles and hard_gates_block_side_effects
    return {
        "schema_version": "agent_company.service_worker_approval_authority_coverage_row.v1",
        "service_id": service["service_id"],
        "request_type": service["request_type"],
        "owner_role_id": service["owner_role_id"],
        "risk_family": service_risk_family(service),
        "default_status": service["default_status"],
        "approval_required_by": authorities,
        "requires_human_user": requires_user,
        "requires_cro": requires_cro,
        "requires_reputation_review": "reputation_review_worker" in authorities,
        "requires_observability": "observability_worker" in authorities,
        "authority_route": route,
        "hard_gates_block_side_effects": hard_gates_block_side_effects,
        "missing_role_ids": missing_roles,
        "covered": covered,
        **copy.deepcopy(ZERO_BOUNDARY),
    }


def build_request_row(
    request: dict[str, Any],
    services_by_id: dict[str, dict[str, Any]],
    services_by_type: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    service = services_by_id.get(str(request.get("service_id") or "")) or services_by_type.get(
        str(request.get("request_type") or "")
    )
    fallback_route = None
    risk_gate = str(request.get("risk_gate") or "")
    request_type = str(request.get("request_type") or "")
    if not service and request_type == "research_enrichment" and "browser_grok_or_x" in risk_gate:
        fallback_route = "human_user_cro_required_signed_in_browser_research_enrichment_no_public_action"
    elif not service and request_type == "lifecycle_test" and risk_gate == "test_no_external_action":
        fallback_route = "local_lifecycle_test_no_external_action_no_authority_granted"
    covered = bool(service or fallback_route)
    return {
        "request_id": request["request_id"],
        "service_id": request.get("service_id"),
        "request_type": request.get("request_type"),
        "lane_id": request.get("lane_id"),
        "status": request.get("status"),
        "risk_gate": request.get("risk_gate"),
        "authority_route": (
            service.get("authority_route")
            if service
            else fallback_route or "blocked_request_without_service_route"
        ),
        "covered": covered,
        "assignment_state": "unassigned" if not request.get("assigned_agent_id") else "assigned",
        "start_state": "not_started" if not request.get("started_at") else "started",
        **copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(
    schema: dict[str, Any],
    *,
    known_roles: set[str] | None = None,
    services: list[dict[str, Any]] | None = None,
    requests: list[dict[str, Any]] | None = None,
    minimum_service_count: int = 13,
) -> tuple[dict[str, Any], dict[str, Any]]:
    failures: list[str] = []
    generated = utc_now()
    coverage_status_enum = schema.get("properties", {}).get("coverage_status", {}).get("enum", [None])
    if coverage_status_enum[0] != "report_only_no_authority_granted":
        failures.append("schema_coverage_status_must_start_report_only_no_authority_granted")

    known_roles = set(known_roles) if known_roles is not None else role_ids()
    services = copy.deepcopy(services) if services is not None else service_catalog_rows()
    service_rows = [build_service_row(service, known_roles) for service in services]
    services_by_id = {row["service_id"]: row for row in service_rows}
    services_by_type = {row["request_type"]: row for row in service_rows}
    requests = copy.deepcopy(requests) if requests is not None else service_request_rows()
    request_rows = [build_request_row(request, services_by_id, services_by_type) for request in requests]

    missing_roles = sorted({role for row in service_rows for role in row["missing_role_ids"]})
    uncovered_services = [row["service_id"] for row in service_rows if not row["covered"]]
    uncovered_requests = [row["request_id"] for row in request_rows if not row["covered"]]
    if missing_roles:
        failures.append("missing_authority_roles:" + ",".join(missing_roles))
    if uncovered_services:
        failures.append("uncovered_services:" + ",".join(uncovered_services))
    if uncovered_requests:
        failures.append("uncovered_requests:" + ",".join(uncovered_requests))
    if len(services) < minimum_service_count:
        failures.append(f"service_count_expected_at_least_{minimum_service_count}_got_{len(services)}")

    status = "report_only_no_authority_granted"
    if missing_roles:
        status = "blocked_missing_role"
    elif uncovered_services:
        status = "blocked_missing_service_coverage"
    elif uncovered_requests:
        status = "blocked_request_without_service_route"

    report = {
        "schema_version": "agent_company.service_worker_approval_authority_coverage.v1",
        "generated_utc": generated,
        "coverage_status": status,
        "db": str(STATE_DB),
        "role_registry_path": str(ROLE_REGISTRY),
        "schema_path": str(SCHEMA_PATH),
        "service_count": len(services),
        "service_rows_covered": sum(1 for row in service_rows if row["covered"]),
        "service_rows": service_rows,
        "current_request_count": len(requests),
        "current_requests_covered": sum(1 for row in request_rows if row["covered"]),
        "request_rows": request_rows,
        "missing_role_count": len(missing_roles),
        "missing_role_ids": missing_roles,
        "services_requiring_user_count": sum(1 for row in service_rows if row["requires_human_user"]),
        "services_requiring_cro_count": sum(1 for row in service_rows if row["requires_cro"]),
        "gated_default_count": sum(1 for row in service_rows if row["default_status"] == "gated"),
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.service_worker_approval_authority_coverage_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "coverage_status": status,
        "service_count": report["service_count"],
        "service_rows_covered": report["service_rows_covered"],
        "current_request_count": report["current_request_count"],
        "current_requests_covered": report["current_requests_covered"],
        "missing_role_count": report["missing_role_count"],
        "services_requiring_user_count": report["services_requiring_user_count"],
        "services_requiring_cro_count": report["services_requiring_cro_count"],
        "gated_default_count": report["gated_default_count"],
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


