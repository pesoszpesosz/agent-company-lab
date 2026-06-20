#!/usr/bin/env python3
"""Core helpers for report-only egress-route signed-decision guards."""

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

SCHEMA_PATH = ARCH / "egress-route-signed-decision-guard-v1.schema.json"
INTAKE_REPORT = REPORTS / "egress-route-signed-decision-intake-contract-v1-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
FIXTURE_DIR = REPORTS / "egress-route-signed-decision-guard-v1-fixtures"
REPORT_JSON = REPORTS / "egress-route-signed-decision-guard-v1-20260618.json"
VALIDATION_JSON = REPORTS / "egress-route-signed-decision-guard-v1-validation-20260618.json"
REPORT_MD = REPORTS / "egress-route-signed-decision-guard-v1-20260618.md"

TARGET_ROUTE_ID = "browser_read_only_gateway"
TARGET_EGRESS_TYPE = "browser_read_only"
ATTESTATION = (
    "I approve egress route preflight review only and understand this does not register "
    "a gateway, start a gateway, start a worker, open a browser, call a model/API, "
    "call MCP, mutate service requests, or perform live egress."
)
EVALUATION_UTC = "2026-06-18T00:20:00Z"
NEXT_ACTION = (
    "Build egress route apply preflight blocker for the accepted "
    "browser_read_only_gateway decision before any gateway registration, browser session, "
    "worker start, or live egress."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "decision_authority_granted_by_contract": False,
    "approval_granted_by_contract": False,
    "apply_allowed": False,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registrations": 0,
    "gateway_starts": 0,
    "live_egress_events": 0,
    "dependency_installs": 0,
    "worker_registrations": 0,
    "worker_starts": 0,
    "runtime_starts": 0,
    "browser_sessions_started": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "telemetry_exports": 0,
    "external_side_effects": False,
}

REQUIRED_FIELDS = [
    "schema_version",
    "decision_id",
    "decision",
    "route_id",
    "egress_type",
    "source_gateway_docket_path",
    "source_gateway_docket_sha256",
    "operator_id",
    "operator_attestation",
    "signed_utc",
    "expires_utc",
    "allowed_scope",
    "allowed_gate_ids",
    "allowed_evidence_artifact_paths",
    "approval_is_not_apply",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "worker_registration_allowed",
    "worker_start_allowed",
    "runtime_start_allowed",
    "browser_session_start_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
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


def route_summary() -> dict[str, Any]:
    gateway = load_json(GATEWAY_DOCKET)
    route = next(row for row in gateway["gateway_routes"] if row["route_id"] == TARGET_ROUTE_ID)
    intake = load_json(INTAKE_REPORT)
    template = next(row for row in intake["decision_templates"] if row["route_id"] == TARGET_ROUTE_ID)
    return {"route": route, "template": template}


def base_decision(decision_id: str, decision: str = "approve_route_preflight_only") -> dict[str, Any]:
    route = route_summary()["route"]
    deny = decision == "deny"
    return {
        "schema_version": "agent_company.egress_route_signed_decision_intake_contract.v1",
        "decision_id": decision_id,
        "decision": decision,
        "route_id": TARGET_ROUTE_ID,
        "egress_type": TARGET_EGRESS_TYPE,
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "operator_id": "human-operator",
        "operator_attestation": "deny-all-no-egress" if deny else ATTESTATION,
        "signed_utc": "2026-06-18T00:20:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if deny else f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
        "allowed_gate_ids": [] if deny else copy.deepcopy(route["required_gates"]),
        "allowed_evidence_artifact_paths": [],
        "approval_is_not_apply": True,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "worker_registration_allowed": False,
        "worker_start_allowed": False,
        "runtime_start_allowed": False,
        "browser_session_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "model_api_calls": False,
        "mcp_tool_calls": False,
        "external_side_effects": False,
        "rollback_plan": (
            "No egress route decision is applied."
            if deny
            else "Discard generated report-only browser-read-only egress route decision "
            "artifacts; no gateway, worker, runtime, browser session, model/API, MCP, "
            "public action, account, wallet, payment, or external action was started."
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_browser_route",
            "expected": "accepted",
            "decision": base_decision("egress-route-guard-positive-deny", "deny"),
        },
        {
            "name": "positive_browser_preflight_only",
            "expected": "accepted",
            "decision": base_decision("egress-route-guard-positive-browser-preflight-only"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(f"egress-route-guard-negative-{name}")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("wrong_attestation", lambda d: d.update({"operator_attestation": "I approve live browser use."}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("wrong_route", lambda d: d.update({"route_id": "mcp_tool_gateway"}))
    negative("wrong_egress_type", lambda d: d.update({"egress_type": "mcp_tool"}))
    negative("missing_docket_path", lambda d: d.update({"source_gateway_docket_path": ""}))
    negative("outside_docket_path", lambda d: d.update({"source_gateway_docket_path": r"C:\Temp\gateway.json"}))
    negative("docket_hash_mismatch", lambda d: d.update({"source_gateway_docket_sha256": "0" * 64}))
    negative("execute_scope", lambda d: d.update({"allowed_scope": "browser_read_only_live_execution"}))
    negative("missing_required_gate", lambda d: d.update({"allowed_gate_ids": ["agent_egress_event_ledger_v1"]}))
    negative("extra_unknown_gate", lambda d: d.update({"allowed_gate_ids": d["allowed_gate_ids"] + ["unknown_gate"]}))
    negative("approval_is_apply", lambda d: d.update({"approval_is_not_apply": False}))
    negative("gateway_registration_allowed", lambda d: d.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda d: d.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda d: d.update({"live_egress_allowed": True}))
    negative("worker_registration_allowed", lambda d: d.update({"worker_registration_allowed": True}))
    negative("worker_start_allowed", lambda d: d.update({"worker_start_allowed": True}))
    negative("runtime_start_allowed", lambda d: d.update({"runtime_start_allowed": True}))
    negative("browser_start_allowed", lambda d: d.update({"browser_session_start_allowed": True}))
    negative("service_request_assigned", lambda d: d.update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda d: d.update({"service_requests_updated": 1}))
    negative("model_api_call", lambda d: d.update({"model_api_calls": True}))
    negative("mcp_tool_call", lambda d: d.update({"mcp_tool_calls": True}))
    negative("external_side_effect", lambda d: d.update({"external_side_effects": True}))
    negative("boundary_decision_applied", lambda d: d["runtime_boundary"].update({"decisions_applied": 1}))
    negative("boundary_approval_written", lambda d: d["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("boundary_gateway_registered", lambda d: d["runtime_boundary"].update({"gateway_registrations": 1}))
    negative("boundary_gateway_started", lambda d: d["runtime_boundary"].update({"gateway_starts": 1}))
    negative("boundary_live_egress", lambda d: d["runtime_boundary"].update({"live_egress_events": 1}))
    negative("boundary_browser_started", lambda d: d["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("boundary_worker_started", lambda d: d["runtime_boundary"].update({"worker_starts": 1}))
    negative("boundary_public_action", lambda d: d["runtime_boundary"].update({"public_actions": True}))
    negative("boundary_external_side_effect", lambda d: d["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_decision(
    decision: dict[str, Any],
    schema: dict[str, Any],
    route: dict[str, Any],
    intake_validation: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    if schema.get("properties", {}).get("route_id", {}).get("const") != TARGET_ROUTE_ID:
        errors.append("schema_route_const_must_target_browser_read_only_gateway")
    for field in REQUIRED_FIELDS:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    if intake_validation.get("all_checks_passed") is not True:
        errors.append("source_intake_contract_validation_not_passing")
    if intake_validation.get("route_count") < 8 or intake_validation.get("template_count") < 8:
        errors.append("source_intake_contract_must_cover_gateway_routes")

    if decision.get("schema_version") != "agent_company.egress_route_signed_decision_intake_contract.v1":
        errors.append("schema_version_mismatch")
    if decision.get("route_id") != TARGET_ROUTE_ID:
        errors.append("route_id_must_match_target_route")
    if decision.get("egress_type") != TARGET_EGRESS_TYPE:
        errors.append("egress_type_must_match_target_route")
    if not str(decision.get("operator_id", "")).strip():
        errors.append("operator_id_missing")
    if not str(decision.get("operator_attestation", "")).strip():
        errors.append("operator_attestation_missing")

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

    docket_path = str(decision.get("source_gateway_docket_path", ""))
    if not docket_path:
        errors.append("source_gateway_docket_path_missing")
    elif not path_inside_root(docket_path):
        errors.append("source_gateway_docket_path_must_stay_inside_lab")
    elif not Path(docket_path).exists():
        errors.append("source_gateway_docket_path_not_found")
    elif decision.get("source_gateway_docket_sha256") != sha256_path(Path(docket_path)):
        errors.append("source_gateway_docket_sha256_mismatch")

    required_gates = route["required_gates"]
    allowed_gate_ids = decision.get("allowed_gate_ids", [])
    if not isinstance(allowed_gate_ids, list):
        errors.append("allowed_gate_ids_must_be_list")
        allowed_gate_ids = []

    decision_value = decision.get("decision")
    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_decision_scope_must_be_none")
        if allowed_gate_ids:
            warnings.append("deny_decision_ignores_allowed_gate_ids")
    elif decision_value == "approve_route_preflight_only":
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("preflight_only_attestation_mismatch")
        if decision.get("allowed_scope") != f"egress_route_preflight_only:{TARGET_ROUTE_ID}":
            errors.append("allowed_scope_must_be_exact_target_route_preflight_only")
        if sorted(allowed_gate_ids) != sorted(required_gates):
            errors.append("allowed_gate_ids_must_equal_target_route_required_gates")
        for gate in allowed_gate_ids:
            if gate not in required_gates:
                errors.append(f"unknown_or_extra_gate:{gate}")
        if "browser_read_only_apply_command_contract_v1" not in allowed_gate_ids:
            errors.append("browser_apply_command_gate_required")
        if "agent_egress_event_ledger_v1" not in allowed_gate_ids:
            errors.append("egress_event_ledger_gate_required")
    else:
        errors.append("decision_value_invalid")

    if decision.get("approval_is_not_apply") is not True:
        errors.append("approval_is_not_apply_must_be_true")
    for key in [
        "gateway_registration_allowed",
        "gateway_start_allowed",
        "live_egress_allowed",
        "worker_registration_allowed",
        "worker_start_allowed",
        "runtime_start_allowed",
        "browser_session_start_allowed",
        "model_api_calls",
        "mcp_tool_calls",
        "external_side_effects",
    ]:
        if decision.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    for key in ["service_requests_assigned", "service_requests_updated"]:
        if decision.get(key) != 0:
            errors.append(f"{key}_must_be_zero")

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
        "decision": decision_value,
        "route_id": decision.get("route_id"),
        "accepted_for_apply_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "worker_start_allowed": False,
        "browser_session_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    route = route_summary()["route"]
    intake_validation = load_json(INTAKE_VALIDATION)
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        decision = (
            copy.deepcopy(fixture["decision"])
            if "decision" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_decision(decision, schema, route, intake_validation)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_apply_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_apply_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.egress_route_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_intake_contract_path": str(INTAKE_REPORT),
        "source_intake_contract_validation_path": str(INTAKE_VALIDATION),
        "source_intake_contract_sha256": sha256_path(INTAKE_REPORT),
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "target_route_required_gates": copy.deepcopy(route["required_gates"]),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "positive_authority": {
            "accepted_scope": f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
            "gateway_registration_allowed": False,
            "gateway_start_allowed": False,
            "live_egress_allowed": False,
            "browser_session_start_allowed": False,
            "worker_start_allowed": False,
        },
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.egress_route_signed_decision_guard_validation.v1",
        "generated_utc": generated,
        "guard_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "fixture_expectation_mismatch_count": len(failures),
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


