#!/usr/bin/env python3
"""Validate service-worker signed decision intake contracts without applying decisions."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "service-worker-signed-decision-intake-contract-v1.schema.json"
AUTHORITY_COVERAGE = REPORTS / "service-worker-approval-authority-coverage-v1-20260617.json"
AUTHORITY_VALIDATION = REPORTS / "service-worker-approval-authority-coverage-v1-validation-20260617.json"
REPORT_JSON = REPORTS / "service-worker-signed-decision-intake-contract-v1-20260617.json"
VALIDATION_JSON = REPORTS / "service-worker-signed-decision-intake-contract-v1-validation-20260617.json"
REPORT_MD = REPORTS / "service-worker-signed-decision-intake-contract-v1-20260617.md"

REQUIRED_DECISION_FIELDS = [
    "schema_version",
    "decision_id",
    "decision",
    "service_id",
    "request_type",
    "source_authority_coverage_path",
    "operator_id",
    "operator_attestation",
    "signed_utc",
    "expires_utc",
    "allowed_scope",
    "allowed_request_ids",
    "exact_scope_required",
    "approval_is_not_apply",
    "runtime_boundary",
]

ZERO_BOUNDARY = {
    "report_only": True,
    "approval_granted_by_contract": False,
    "decision_authority_granted_by_contract": False,
    "rejection_granted_by_contract": False,
    "apply_allowed": False,
    "approval_rows_written": 0,
    "decisions_applied": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "worker_starts": 0,
    "browser_sessions_started": False,
    "api_calls": False,
    "external_side_effects": False,
}
NEXT_ACTION = (
    "Use these templates to validate service-specific signed decisions before any apply "
    "preflight or queue mutation."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def request_ids_for_service(authority: dict[str, Any], service_id: str, request_type: str) -> list[str]:
    ids = []
    for row in authority.get("request_rows", []):
        if row.get("service_id") == service_id or row.get("request_type") == request_type:
            ids.append(row["request_id"])
    return sorted(ids)


def allowed_decisions_for_route(route: str, service_id: str) -> list[str]:
    decisions = ["deny", "approve_review_packet_only"]
    if "preflight" in route or service_id in {"browser_read_only_session", "model_api_execution_gate"}:
        decisions.append("approve_assignment_preflight_only")
    if service_id in {
        "public_action_execution",
        "github_public_action_gate",
        "outreach_delivery_gate",
        "wallet_public_address_response",
    }:
        decisions.append("approve_exact_action_preflight_only")
    return decisions


def template_for_service(row: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    allowed_request_ids = request_ids_for_service(authority, row["service_id"], row["request_type"])
    allowed_decisions = allowed_decisions_for_route(row["authority_route"], row["service_id"])
    return {
        "schema_version": "agent_company.service_worker_signed_decision_intake_contract.v1",
        "template_id": f"service-worker-decision-template-{row['service_id']}",
        "service_id": row["service_id"],
        "request_type": row["request_type"],
        "risk_family": row["risk_family"],
        "authority_route": row["authority_route"],
        "required_authorities": row["approval_required_by"],
        "allowed_decisions": allowed_decisions,
        "required_fields": copy.deepcopy(REQUIRED_DECISION_FIELDS),
        "source_authority_coverage_path": str(AUTHORITY_COVERAGE),
        "source_authority_coverage_sha256": sha256_path(AUTHORITY_COVERAGE),
        "allowed_request_ids": allowed_request_ids,
        "operator_attestation_required": True,
        "exact_scope_required": True,
        "approval_is_not_apply": True,
        "requires_expiry": True,
        "requires_rollback_plan": True,
        "requires_post_decision_apply_preflight": True,
        "forbidden_apply_effects": [
            "approval_rows_written",
            "decisions_applied",
            "service_requests_assigned",
            "service_requests_updated",
            "worker_starts",
            "browser_sessions_started",
            "api_calls",
            "external_side_effects",
        ],
        "decision_example": {
            "schema_version": "agent_company.service_worker_signed_decision_intake_contract.v1",
            "decision_id": f"service-worker-decision-{row['service_id']}-example-deny",
            "decision": "deny",
            "service_id": row["service_id"],
            "request_type": row["request_type"],
            "source_authority_coverage_path": str(AUTHORITY_COVERAGE),
            "operator_id": "human-operator",
            "operator_attestation": (
                "I deny this service-worker request and understand this record does not "
                "apply a decision."
            ),
            "signed_utc": "2026-06-17T20:30:00Z",
            "expires_utc": "2099-01-01T00:00:00Z",
            "allowed_scope": "none",
            "allowed_request_ids": [],
            "exact_scope_required": True,
            "approval_is_not_apply": True,
            "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        },
        **copy.deepcopy(ZERO_BOUNDARY),
    }


def validate_template(template: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    for field in REQUIRED_DECISION_FIELDS:
        if field not in template.get("required_fields", []):
            errors.append(f"template_missing_required_field:{field}")
    if not template.get("operator_attestation_required"):
        errors.append("operator_attestation_must_be_required")
    if template.get("exact_scope_required") is not True:
        errors.append("exact_scope_required_must_be_true")
    if template.get("approval_is_not_apply") is not True:
        errors.append("approval_is_not_apply_must_be_true")
    if template.get("requires_post_decision_apply_preflight") is not True:
        errors.append("requires_post_decision_apply_preflight_must_be_true")
    if "deny" not in template.get("allowed_decisions", []):
        errors.append("deny_must_be_allowed")
    boundary = template.get("decision_example", {}).get("runtime_boundary", {})
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"decision_example_boundary_{key}_must_equal_{expected}")
    for key, expected in ZERO_BOUNDARY.items():
        if template.get(key) != expected:
            errors.append(f"template_boundary_{key}_must_equal_{expected}")
    return errors


def build_report(
    schema: dict[str, Any],
    *,
    authority: dict[str, Any] | None = None,
    authority_validation: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    generated = utc_now()
    authority = copy.deepcopy(authority) if authority is not None else load_json(AUTHORITY_COVERAGE)
    authority_validation = (
        copy.deepcopy(authority_validation)
        if authority_validation is not None
        else load_json(AUTHORITY_VALIDATION)
    )
    failures: list[str] = []

    if authority_validation.get("all_checks_passed") is not True:
        failures.append("authority_coverage_validation_not_passing")
    if authority.get("coverage_status") != "report_only_no_authority_granted":
        failures.append("authority_coverage_status_not_report_only")

    templates = [template_for_service(row, authority) for row in authority.get("service_rows", [])]
    template_errors: list[dict[str, Any]] = []
    for template in templates:
        errors = validate_template(template, schema)
        if errors:
            template_errors.append({"template_id": template["template_id"], "errors": errors})
    if template_errors:
        failures.append("template_validation_failures")

    service_count = int(authority.get("service_count", 0))
    current_request_count = int(authority.get("current_request_count", 0))
    current_requests_covered = int(authority.get("current_requests_covered", 0))
    if len(templates) != service_count:
        failures.append(f"template_count_expected_{service_count}_got_{len(templates)}")
    if current_request_count != current_requests_covered:
        failures.append("authority_coverage_current_requests_not_fully_covered")

    missing_required_field_count = sum(len(item["errors"]) for item in template_errors)
    contract_status = "report_only_intake_contract_ready" if not failures else "blocked_contract_validation_failed"
    report = {
        "schema_version": "agent_company.service_worker_signed_decision_intake_contract_report.v1",
        "generated_utc": generated,
        "contract_status": contract_status,
        "schema_path": str(SCHEMA_PATH),
        "source_authority_coverage_path": str(AUTHORITY_COVERAGE),
        "source_authority_coverage_sha256": sha256_path(AUTHORITY_COVERAGE),
        "source_authority_validation_path": str(AUTHORITY_VALIDATION),
        "service_count": service_count,
        "service_template_count": len(templates),
        "service_templates": templates,
        "current_request_count": current_request_count,
        "current_requests_covered": current_requests_covered,
        "missing_required_field_count": missing_required_field_count,
        "template_errors": template_errors,
        "templates_with_exact_scope_required_count": sum(1 for t in templates if t["exact_scope_required"]),
        "templates_with_attestation_required_count": sum(1 for t in templates if t["operator_attestation_required"]),
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.service_worker_signed_decision_intake_contract_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "contract_status": contract_status,
        "service_count": service_count,
        "service_template_count": len(templates),
        "current_request_count": current_request_count,
        "current_requests_covered": current_requests_covered,
        "missing_required_field_count": missing_required_field_count,
        "templates_with_exact_scope_required_count": report["templates_with_exact_scope_required_count"],
        "templates_with_attestation_required_count": report["templates_with_attestation_required_count"],
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


