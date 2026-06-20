#!/usr/bin/env python3
"""Write report-only signed-decision intake templates for egress gateway routes."""

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

SCHEMA_PATH = ARCH / "egress-route-signed-decision-intake-contract-v1.schema.json"
GATEWAY_DOCKET = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
GATEWAY_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
REPORT_JSON = REPORTS / "egress-route-signed-decision-intake-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
REPORT_MD = REPORTS / "egress-route-signed-decision-intake-contract-v1-20260618.md"

ATTESTATION = "I approve egress route preflight review only and understand this does not register a gateway, start a gateway, start a worker, open a browser, call a model/API, call MCP, mutate service requests, or perform live egress."
EVALUATION_UTC = "2026-06-18T00:00:00Z"

REQUIRED_DECISION_FIELDS = [
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


def decision_template(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "template_id": f"egress-route-decision-template-{route['route_id']}",
        "schema_version": "agent_company.egress_route_signed_decision_intake_contract.v1",
        "route_id": route["route_id"],
        "egress_type": route["egress_type"],
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "allowed_decisions": ["deny", "approve_route_preflight_only"],
        "required_fields": copy.deepcopy(REQUIRED_DECISION_FIELDS),
        "required_gates": copy.deepcopy(route["required_gates"]),
        "blocked_actions": copy.deepcopy(route["blocked_actions"]),
        "required_evidence": copy.deepcopy(route["required_evidence"]),
        "operator_attestation_required": True,
        "exact_route_required": True,
        "approval_is_not_apply": True,
        "requires_expiry": True,
        "requires_rollback_plan": True,
        "requires_post_decision_apply_preflight": True,
        "decision_example": base_decision(route, "deny"),
        **copy.deepcopy(ZERO_BOUNDARY),
    }


def base_decision(route: dict[str, Any], decision: str = "approve_route_preflight_only") -> dict[str, Any]:
    deny = decision == "deny"
    return {
        "schema_version": "agent_company.egress_route_signed_decision_intake_contract.v1",
        "decision_id": f"egress-route-decision-{route['route_id']}-{decision}",
        "decision": decision,
        "route_id": route["route_id"],
        "egress_type": route["egress_type"],
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "operator_id": "human-operator",
        "operator_attestation": "deny-all-no-egress" if deny else ATTESTATION,
        "signed_utc": "2026-06-18T00:00:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if deny else f"egress_route_preflight_only:{route['route_id']}",
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
        "rollback_plan": "No egress route decision is applied." if deny else "Discard generated report-only egress route decision artifacts; no gateway, worker, runtime, browser, model/API, MCP, public, account, wallet, payment, or external action was started.",
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set(routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {route["route_id"]: route for route in routes}
    browser = by_id["browser_read_only_gateway"]
    mcp = by_id["mcp_tool_gateway"]
    fixtures = [
        {"name": "positive_deny_browser_route", "expected": "accepted", "decision": base_decision(browser, "deny")},
        {"name": "positive_browser_route_preflight_only", "expected": "accepted", "decision": base_decision(browser)},
        {"name": "positive_mcp_route_preflight_only", "expected": "accepted", "decision": base_decision(mcp)},
    ]

    def negative(name: str, mutate) -> None:
        decision = base_decision(browser)
        decision["decision_id"] = f"egress-route-decision-negative-{name}"
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("wrong_attestation", lambda d: d.update({"operator_attestation": "I approve live egress."}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("unknown_route", lambda d: d.update({"route_id": "unknown_route"}))
    negative("egress_type_mismatch", lambda d: d.update({"egress_type": "model_api"}))
    negative("missing_docket", lambda d: d.update({"source_gateway_docket_path": ""}))
    negative("outside_docket", lambda d: d.update({"source_gateway_docket_path": r"C:\Temp\docket.json"}))
    negative("docket_hash_mismatch", lambda d: d.update({"source_gateway_docket_sha256": "0" * 64}))
    negative("execute_scope", lambda d: d.update({"allowed_scope": "live_egress_execute"}))
    negative("missing_required_gate", lambda d: d.update({"allowed_gate_ids": ["agent_egress_event_ledger_v1"]}))
    negative("extra_unknown_gate", lambda d: d.update({"allowed_gate_ids": d["allowed_gate_ids"] + ["unknown_gate"]}))
    negative("approval_is_apply", lambda d: d.update({"approval_is_not_apply": False}))
    negative("gateway_registration_allowed", lambda d: d.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda d: d.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda d: d.update({"live_egress_allowed": True}))
    negative("worker_start_allowed", lambda d: d.update({"worker_start_allowed": True}))
    negative("runtime_start_allowed", lambda d: d.update({"runtime_start_allowed": True}))
    negative("browser_session_start_allowed", lambda d: d.update({"browser_session_start_allowed": True}))
    negative("service_request_assigned", lambda d: d.update({"service_requests_assigned": 1}))
    negative("boundary_decision_applied", lambda d: d["runtime_boundary"].update({"decisions_applied": 1}))
    negative("boundary_gateway_started", lambda d: d["runtime_boundary"].update({"gateway_starts": 1}))
    negative("boundary_live_egress", lambda d: d["runtime_boundary"].update({"live_egress_events": 1}))
    negative("boundary_model_api", lambda d: d["runtime_boundary"].update({"model_api_calls": True}))
    negative("boundary_mcp", lambda d: d["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("boundary_public_action", lambda d: d["runtime_boundary"].update({"public_actions": True}))
    negative("boundary_external_side_effect", lambda d: d["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_decision(decision: dict[str, Any], schema: dict[str, Any], routes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    for field in REQUIRED_DECISION_FIELDS:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    if decision.get("schema_version") != "agent_company.egress_route_signed_decision_intake_contract.v1":
        errors.append("schema_version_mismatch")
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

    route_id = str(decision.get("route_id", ""))
    route = routes.get(route_id)
    if not route:
        errors.append("route_id_unknown")
        route = {}
    elif decision.get("egress_type") != route.get("egress_type"):
        errors.append("egress_type_must_match_route")

    decision_value = decision.get("decision")
    allowed_gate_ids = decision.get("allowed_gate_ids", [])
    if not isinstance(allowed_gate_ids, list):
        errors.append("allowed_gate_ids_must_be_list")
        allowed_gate_ids = []
    required_gates = route.get("required_gates", [])
    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_decision_scope_must_be_none")
        if allowed_gate_ids:
            warnings.append("deny_decision_ignores_allowed_gate_ids")
    elif decision_value == "approve_route_preflight_only":
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("preflight_only_attestation_mismatch")
        if decision.get("allowed_scope") != f"egress_route_preflight_only:{route_id}":
            errors.append("allowed_scope_must_be_exact_route_preflight_only")
        if sorted(allowed_gate_ids) != sorted(required_gates):
            errors.append("allowed_gate_ids_must_equal_route_required_gates")
        for gate in allowed_gate_ids:
            if gate not in required_gates:
                errors.append(f"unknown_or_extra_gate:{gate}")
        if len(str(decision.get("rollback_plan", "")).strip()) < 40:
            errors.append("rollback_plan_too_short")
    else:
        errors.append("decision_value_invalid")

    for key in [
        "approval_is_not_apply",
    ]:
        if decision.get(key) is not True:
            errors.append(f"{key}_must_be_true")
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

    return {
        "decision_id": decision.get("decision_id"),
        "route_id": decision.get("route_id"),
        "decision": decision_value,
        "accepted": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def validate_template(template: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    for field in REQUIRED_DECISION_FIELDS:
        if field not in template.get("required_fields", []):
            errors.append(f"template_missing_required_field:{field}")
    if "deny" not in template.get("allowed_decisions", []):
        errors.append("deny_must_be_allowed")
    if "approve_route_preflight_only" not in template.get("allowed_decisions", []):
        errors.append("preflight_only_must_be_allowed")
    if template.get("approval_is_not_apply") is not True:
        errors.append("approval_is_not_apply_must_be_true")
    if template.get("requires_post_decision_apply_preflight") is not True:
        errors.append("requires_post_decision_apply_preflight_must_be_true")
    for key, expected in ZERO_BOUNDARY.items():
        if template.get(key) != expected:
            errors.append(f"template_boundary_{key}_must_equal_{expected}")
    return errors


def build_report() -> tuple[dict[str, Any], dict[str, Any]]:
    generated = utc_now()
    schema = load_json(SCHEMA_PATH)
    gateway = load_json(GATEWAY_DOCKET)
    gateway_validation = load_json(GATEWAY_VALIDATION)
    routes = gateway.get("gateway_routes", [])
    route_by_id = {route["route_id"]: route for route in routes}
    failures: list[str] = []

    if gateway_validation.get("all_checks_passed") is not True:
        failures.append("gateway_docket_validation_not_passing")
    if gateway_validation.get("live_egress_allowed") is not False:
        failures.append("gateway_docket_must_not_allow_live_egress")
    if len(routes) < 8:
        failures.append("route_count_below_8")

    templates = [decision_template(route) for route in routes]
    template_errors = []
    for template in templates:
        errors = validate_template(template, schema)
        if errors:
            template_errors.append({"template_id": template["template_id"], "errors": errors})
    if template_errors:
        failures.append("template_validation_failures")

    fixtures = fixture_set(routes)
    fixture_results = []
    for fixture in fixtures:
        result = validate_decision(fixture["decision"], schema, route_by_id)
        fixture_results.append({"name": fixture["name"], "expected": fixture["expected"], **result})
    accepted_count = sum(1 for item in fixture_results if item["accepted"])
    rejected_count = sum(1 for item in fixture_results if not item["accepted"])
    mismatches = [
        item["name"]
        for item in fixture_results
        if (item["expected"] == "accepted" and not item["accepted"]) or (item["expected"] == "rejected" and item["accepted"])
    ]
    if mismatches:
        failures.append("fixture_expectation_mismatch")

    report = {
        "schema_version": "agent_company.egress_route_signed_decision_intake_contract_report.v1",
        "generated_utc": generated,
        "contract_status": "report_only_intake_contract_ready" if not failures else "blocked_contract_validation_failed",
        "schema_path": str(SCHEMA_PATH),
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "source_gateway_validation_path": str(GATEWAY_VALIDATION),
        "route_count": len(routes),
        "template_count": len(templates),
        "decision_templates": templates,
        "fixture_count": len(fixtures),
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "fixture_expectation_mismatches": mismatches,
        "fixture_results": fixture_results,
        "template_errors": template_errors,
        "next_action": "Build egress route signed-decision guard for one exact route decision before any apply preflight, gateway registration, gateway start, or live egress.",
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.egress_route_signed_decision_intake_contract_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "route_count": len(routes),
        "template_count": len(templates),
        "fixture_count": len(fixtures),
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "fixture_expectation_mismatch_count": len(mismatches),
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Egress Route Signed Decision Intake Contract v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Source gateway docket: `{GATEWAY_DOCKET}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Contract status: `{report['contract_status']}`",
        f"- Route templates: `{validation['template_count']}` / `{validation['route_count']}`",
        f"- Fixture results: `{validation['accepted_count']}` accepted, `{validation['rejected_count']}` rejected",
        f"- Gateway registration allowed: `{validation['gateway_registrations']}`",
        f"- Gateway starts: `{validation['gateway_starts']}`",
        f"- Live egress events: `{validation['live_egress_events']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
        f"- Runtime starts: `{validation['runtime_starts']}`",
        f"- Browser sessions started: `{validation['browser_sessions_started']}`",
        f"- Model/API calls: `{validation['model_api_calls']}`",
        f"- MCP tool calls: `{validation['mcp_tool_calls']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Templates",
        "",
        "| Route | Egress Type | Allowed Decisions | Required Gates |",
        "| --- | --- | --- | --- |",
    ]
    for template in report["decision_templates"]:
        lines.append(
            f"| `{template['route_id']}` | `{template['egress_type']}` | {', '.join(f'`{x}`' for x in template['allowed_decisions'])} | {', '.join(f'`{x}`' for x in template['required_gates'])} |"
        )
    lines.extend(
        [
            "",
            "## Fixture Validation",
            "",
            "| Fixture | Expected | Accepted | Errors |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for item in report["fixture_results"]:
        lines.append(f"| `{item['name']}` | `{item['expected']}` | `{item['accepted']}` | `{len(item['errors'])}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This contract only defines and validates signed-decision intake records. It does not apply decisions, write approvals, register gateways, start gateways, start workers, mutate service requests, or perform live egress.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    report, validation = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(
        json.dumps(
            {
                "ok": validation["all_checks_passed"],
                "report_path": str(REPORT_JSON),
                "validation_path": str(VALIDATION_JSON),
                "route_count": validation["route_count"],
                "fixture_count": validation["fixture_count"],
                "failure_count": validation["failure_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
