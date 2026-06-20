#!/usr/bin/env python3
"""Validate service-worker signed decisions against intake templates without applying them."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "service-worker-signed-decision-guard-v1.schema.json"
INTAKE_CONTRACT = REPORTS / "service-worker-signed-decision-intake-contract-v1-20260617.json"
INTAKE_VALIDATION = REPORTS / "service-worker-signed-decision-intake-contract-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "service-worker-signed-decision-guard-v1-fixtures"
REPORT_JSON = REPORTS / "service-worker-signed-decision-guard-v1-20260617.json"
VALIDATION_JSON = REPORTS / "service-worker-signed-decision-guard-v1-validation-20260617.json"
REPORT_MD = REPORTS / "service-worker-signed-decision-guard-v1-20260617.md"

EVALUATION_UTC = "2026-06-17T20:35:00Z"
ATTESTATION_SUFFIX = (
    "I understand this signed decision is report-only and does not apply approval, "
    "assign requests, start workers, open browsers, call APIs, or perform external actions."
)

NEXT_ACTION = (
    "Build a service-worker signed decision apply preflight blocker before any accepted "
    "guard decision can mutate queue state."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "approval_granted_by_guard": False,
    "decision_authority_granted_by_guard": False,
    "rejection_granted_by_guard": False,
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

REQUIRED_FIELDS = [
    "schema_version",
    "decision_id",
    "decision",
    "service_id",
    "request_type",
    "source_intake_contract_path",
    "operator_id",
    "operator_attestation",
    "signed_utc",
    "expires_utc",
    "allowed_scope",
    "allowed_request_ids",
    "exact_scope_required",
    "approval_is_not_apply",
    "apply_allowed",
    "runtime_boundary",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return str(value).startswith(str(ROOT)) and ".." not in str(value)


def templates_by_service(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {template["service_id"]: template for template in contract.get("service_templates", [])}


def template_for(contract: dict[str, Any], service_id: str) -> dict[str, Any]:
    return templates_by_service(contract)[service_id]


def base_decision(
    decision_id: str,
    service_id: str,
    decision: str,
    request_ids: list[str] | None = None,
) -> dict[str, Any]:
    contract = load_json(INTAKE_CONTRACT)
    template = template_for(contract, service_id)
    ids = []
    if decision != "deny":
        ids = request_ids if request_ids is not None else template.get("allowed_request_ids", [])[:1]
    scope = "none" if decision == "deny" else f"{service_id}:{decision}:exact_scope"
    return {
        "schema_version": "agent_company.service_worker_signed_decision_guard.v1",
        "decision_id": decision_id,
        "decision": decision,
        "service_id": service_id,
        "request_type": template["request_type"],
        "source_intake_contract_path": str(INTAKE_CONTRACT),
        "operator_id": "human-operator",
        "operator_attestation": f"{decision} for {service_id}. {ATTESTATION_SUFFIX}",
        "signed_utc": "2026-06-17T20:35:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": scope,
        "allowed_request_ids": ids,
        "exact_scope_required": True,
        "approval_is_not_apply": True,
        "apply_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_browser",
            "expected": "accepted",
            "decision": base_decision(
                "service-worker-signed-decision-positive-deny-browser",
                "browser_read_only_session",
                "deny",
            ),
        },
        {
            "name": "positive_review_legal",
            "expected": "accepted",
            "decision": base_decision(
                "service-worker-signed-decision-positive-review-legal",
                "legal_kyc_tax_payment_gate",
                "approve_review_packet_only",
            ),
        },
        {
            "name": "positive_assignment_browser",
            "expected": "accepted",
            "decision": base_decision(
                "service-worker-signed-decision-positive-assignment-browser",
                "browser_read_only_session",
                "approve_assignment_preflight_only",
            ),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(
            f"service-worker-signed-decision-negative-{name}",
            "browser_read_only_session",
            "approve_assignment_preflight_only",
        )
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("weak_attestation", lambda d: d.update({"operator_attestation": "approved"}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("expires_before_signed", lambda d: d.update({"expires_utc": "2026-06-01T00:00:00Z"}))
    negative("missing_contract", lambda d: d.update({"source_intake_contract_path": ""}))
    negative("outside_contract", lambda d: d.update({"source_intake_contract_path": r"C:\Temp\contract.json"}))
    negative("unknown_service", lambda d: d.update({"service_id": "unknown_service"}))
    negative("wrong_request_type", lambda d: d.update({"request_type": "wrong_type"}))
    negative(
        "decision_not_allowed_for_service",
        lambda d: d.update({"decision": "approve_exact_action_preflight_only"}),
    )
    negative("broad_scope", lambda d: d.update({"allowed_scope": "all_requests_all_actions"}))
    negative("missing_request_ids_for_non_deny", lambda d: d.update({"allowed_request_ids": []}))
    negative("unknown_request_id", lambda d: d.update({"allowed_request_ids": ["req-does-not-exist"]}))
    negative("exact_scope_false", lambda d: d.update({"exact_scope_required": False}))
    negative("approval_is_apply", lambda d: d.update({"approval_is_not_apply": False}))
    negative("apply_allowed", lambda d: d.update({"apply_allowed": True}))
    negative("approval_row_written", lambda d: d["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("decision_applied", lambda d: d["runtime_boundary"].update({"decisions_applied": 1}))
    negative("service_request_assigned", lambda d: d["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda d: d["runtime_boundary"].update({"service_requests_updated": 1}))
    negative("worker_started", lambda d: d["runtime_boundary"].update({"worker_starts": 1}))
    negative("browser_started", lambda d: d["runtime_boundary"].update({"browser_sessions_started": True}))
    negative("api_called", lambda d: d["runtime_boundary"].update({"api_calls": True}))
    negative("external_side_effect", lambda d: d["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_decision(
    decision: dict[str, Any],
    schema: dict[str, Any],
    contract: dict[str, Any],
    contract_validation: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    if contract_validation.get("all_checks_passed") is not True:
        errors.append("source_intake_contract_validation_not_passing")
    if contract.get("contract_status") != "report_only_intake_contract_ready":
        errors.append("source_intake_contract_not_ready")

    for field in REQUIRED_FIELDS:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    if decision.get("schema_version") != "agent_company.service_worker_signed_decision_guard.v1":
        errors.append("schema_version_mismatch")
    if not str(decision.get("operator_id", "")).strip():
        errors.append("operator_id_missing")
    attestation = str(decision.get("operator_attestation", ""))
    if not attestation.strip():
        errors.append("operator_attestation_missing")
    elif ATTESTATION_SUFFIX not in attestation:
        errors.append("operator_attestation_must_include_report_only_boundary")

    signed = parse_utc(str(decision.get("signed_utc", "")))
    expires = parse_utc(str(decision.get("expires_utc", "")))
    if signed is None:
        errors.append("signed_utc_invalid")
    if expires is None:
        errors.append("expires_utc_invalid")
    if signed and expires and expires <= signed:
        errors.append("expires_not_after_signed")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("decision_expired")

    contract_path = str(decision.get("source_intake_contract_path", ""))
    if not contract_path:
        errors.append("source_intake_contract_path_missing")
    elif not path_inside_root(contract_path):
        errors.append("source_intake_contract_path_must_stay_inside_lab")
    elif not Path(contract_path).exists():
        errors.append("source_intake_contract_path_not_found")

    templates = templates_by_service(contract)
    service_id = str(decision.get("service_id", ""))
    template = templates.get(service_id)
    if not template:
        errors.append("service_id_not_found_in_intake_contract")
        template = {}
    else:
        if decision.get("request_type") != template.get("request_type"):
            errors.append("request_type_must_match_template")
        if decision.get("decision") not in template.get("allowed_decisions", []):
            errors.append("decision_not_allowed_for_service_template")
        allowed_ids = decision.get("allowed_request_ids", [])
        if not isinstance(allowed_ids, list):
            errors.append("allowed_request_ids_must_be_list")
            allowed_ids = []
        unknown_ids = sorted(set(str(item) for item in allowed_ids) - set(template.get("allowed_request_ids", [])))
        if unknown_ids:
            errors.append("allowed_request_ids_unknown_for_template:" + ",".join(unknown_ids))
        if decision.get("decision") != "deny" and template.get("allowed_request_ids") and not allowed_ids:
            errors.append("non_deny_decision_requires_bound_request_ids")

    decision_value = decision.get("decision")
    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_scope_must_be_none")
    else:
        scope = str(decision.get("allowed_scope", ""))
        if not scope or scope in {"all", "all_requests", "all_requests_all_actions"} or "all_" in scope:
            errors.append("allowed_scope_must_be_exact_not_broad")
        if service_id and not scope.startswith(service_id + ":"):
            errors.append("allowed_scope_must_start_with_service_id")

    if decision.get("exact_scope_required") is not True:
        errors.append("exact_scope_required_must_be_true")
    if decision.get("approval_is_not_apply") is not True:
        errors.append("approval_is_not_apply_must_be_true")
    if decision.get("apply_allowed") is not False:
        errors.append("apply_allowed_must_be_false")

    boundary = decision.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    accepted = not errors
    return {
        "decision_id": decision.get("decision_id"),
        "decision": decision.get("decision"),
        "service_id": service_id,
        "accepted_for_later_apply_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "apply_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = load_json(INTAKE_CONTRACT)
    contract_validation = load_json(INTAKE_VALIDATION)
    failures: list[str] = []
    results = []
    for fixture in fixtures:
        decision = (
            copy.deepcopy(fixture["decision"])
            if "decision" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_decision(decision, schema, contract, contract_validation)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_later_apply_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_later_apply_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.service_worker_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "guard_status": (
            "report_only_signed_decision_guard_ready"
            if not failures
            else "blocked_guard_validation_failed"
        ),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_intake_contract_path": str(INTAKE_CONTRACT),
        "source_intake_contract_sha256": sha256_path(INTAKE_CONTRACT),
        "source_intake_validation_path": str(INTAKE_VALIDATION),
        "service_template_count": contract.get("service_template_count"),
        "current_request_count": contract.get("current_request_count"),
        "positive_authority": {
            "accepted_scopes": [
                "none",
                "legal_kyc_tax_payment_gate:approve_review_packet_only:exact_scope",
                "browser_read_only_session:approve_assignment_preflight_only:exact_scope",
            ],
            "apply_allowed": False,
        },
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.service_worker_signed_decision_guard_validation.v1",
        "generated_utc": generated,
        "guard_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "guard_status": report["guard_status"],
        "service_template_count": contract.get("service_template_count"),
        "current_request_count": contract.get("current_request_count"),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


