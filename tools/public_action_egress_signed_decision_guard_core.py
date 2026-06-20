#!/usr/bin/env python3
"""Core helpers for report-only public-action signed-decision guards."""

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

SCHEMA_PATH = ARCH / "public-action-egress-signed-decision-guard-v1.schema.json"
INTAKE_REPORT = REPORTS / "egress-route-signed-decision-intake-contract-v1-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
EGRESS_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "public-action-egress-signed-decision-guard-v1-fixtures"
REPORT_JSON = REPORTS / "public-action-egress-signed-decision-guard-v1-20260618.json"
VALIDATION_JSON = REPORTS / "public-action-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT_MD = REPORTS / "public-action-egress-signed-decision-guard-v1-20260618.md"

TARGET_ROUTE_ID = "public_action_gateway"
TARGET_EGRESS_TYPE = "public_submission"
EVALUATION_UTC = "2026-06-18T05:00:00Z"
ATTESTATION = (
    "I approve public action egress route preflight review only and understand this does not post, submit a "
    "form, open a PR, claim a bounty, send a message, start a browser session, mutate an account, mutate "
    "service requests, or perform live egress."
)
NEXT_ACTION = (
    "Build public_action_gateway apply preflight blocker before any post, form submission, PR, bounty claim, "
    "message send, browser mutation, account action, service-request mutation, or live egress."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "decision_authority_granted_by_contract": False,
    "approval_granted_by_contract": False,
    "apply_allowed": False,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registration_allowed": False,
    "gateway_start_allowed": False,
    "live_egress_allowed": False,
    "gateway_registrations": 0,
    "gateway_starts": 0,
    "live_egress_events": 0,
    "public_action_allowed": False,
    "public_actions": False,
    "posts_created": 0,
    "forms_submitted": 0,
    "prs_opened": 0,
    "bounty_claims": 0,
    "messages_sent": 0,
    "browser_session_start_allowed": False,
    "browser_sessions_started": 0,
    "account_actions": False,
    "worker_registrations": 0,
    "worker_start_allowed": False,
    "worker_starts": 0,
    "runtime_starts": 0,
    "dependency_installs": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "mcp_tool_calls": False,
    "model_api_calls": False,
    "wallet_actions": False,
    "payment_actions": False,
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
    "public_action_allowed",
    "public_actions",
    "browser_session_start_allowed",
    "browser_sessions_started",
    "worker_start_allowed",
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
    try:
        return Path(value).resolve().is_relative_to(ROOT.resolve())
    except Exception:
        return False


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
        "signed_utc": "2026-06-18T04:50:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if deny else f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
        "allowed_gate_ids": [] if deny else copy.deepcopy(route["required_gates"]),
        "allowed_evidence_artifact_paths": [],
        "approval_is_not_apply": True,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "public_action_allowed": False,
        "public_actions": False,
        "browser_session_start_allowed": False,
        "browser_sessions_started": 0,
        "worker_registration_allowed": False,
        "worker_start_allowed": False,
        "runtime_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "mcp_tool_calls": False,
        "model_api_calls": False,
        "account_actions": False,
        "external_side_effects": False,
        "rollback_plan": (
            "No egress route decision is applied."
            if deny
            else "Discard generated report-only public action egress route decision artifacts; no post, form "
            "submission, PR, bounty claim, message, browser session, account action, service-request mutation, "
            "MCP/model call, payment, wallet, or external action was started."
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {"name": "positive_deny_public_action_route", "expected": "accepted", "decision": base_decision("public-action-egress-guard-positive-deny", "deny")},
        {"name": "positive_public_action_preflight_only", "expected": "accepted", "decision": base_decision("public-action-egress-guard-positive-preflight-only")},
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(f"public-action-egress-guard-negative-{name}")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("wrong_attestation", lambda d: d.update({"operator_attestation": "I approve posting publicly."}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("wrong_route", lambda d: d.update({"route_id": "runtime_process_gateway"}))
    negative("wrong_egress_type", lambda d: d.update({"egress_type": "runtime_start"}))
    negative("missing_docket_path", lambda d: d.update({"source_gateway_docket_path": ""}))
    negative("outside_docket_path", lambda d: d.update({"source_gateway_docket_path": r"C:\Temp\gateway.json"}))
    negative("docket_hash_mismatch", lambda d: d.update({"source_gateway_docket_sha256": "0" * 64}))
    negative("execute_scope", lambda d: d.update({"allowed_scope": "public_action_execute"}))
    negative("missing_required_gate", lambda d: d.update({"allowed_gate_ids": ["agent_egress_event_ledger_v1"]}))
    negative("extra_unknown_gate", lambda d: d.update({"allowed_gate_ids": d["allowed_gate_ids"] + ["unknown_gate"]}))
    negative("approval_is_apply", lambda d: d.update({"approval_is_not_apply": False}))
    negative("gateway_registration_allowed", lambda d: d.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda d: d.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda d: d.update({"live_egress_allowed": True}))
    negative("public_action_allowed", lambda d: d.update({"public_action_allowed": True}))
    negative("public_actions", lambda d: d.update({"public_actions": True}))
    negative("browser_start_allowed", lambda d: d.update({"browser_session_start_allowed": True}))
    negative("browser_started", lambda d: d.update({"browser_sessions_started": 1}))
    negative("account_action", lambda d: d.update({"account_actions": True}))
    negative("worker_registration_allowed", lambda d: d.update({"worker_registration_allowed": True}))
    negative("worker_start_allowed", lambda d: d.update({"worker_start_allowed": True}))
    negative("runtime_start_allowed", lambda d: d.update({"runtime_start_allowed": True}))
    negative("service_request_assigned", lambda d: d.update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda d: d.update({"service_requests_updated": 1}))
    negative("mcp_tool_call", lambda d: d.update({"mcp_tool_calls": True}))
    negative("model_api_call", lambda d: d.update({"model_api_calls": True}))
    negative("external_side_effect", lambda d: d.update({"external_side_effects": True}))
    negative("short_rollback", lambda d: d.update({"rollback_plan": "undo"}))
    negative("boundary_decision_applied", lambda d: d["runtime_boundary"].update({"decisions_applied": 1}))
    negative("boundary_approval_written", lambda d: d["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("boundary_gateway_started", lambda d: d["runtime_boundary"].update({"gateway_starts": 1}))
    negative("boundary_live_egress", lambda d: d["runtime_boundary"].update({"live_egress_events": 1}))
    negative("boundary_public_action_allowed", lambda d: d["runtime_boundary"].update({"public_action_allowed": True}))
    negative("boundary_public_actions", lambda d: d["runtime_boundary"].update({"public_actions": True}))
    negative("boundary_post_created", lambda d: d["runtime_boundary"].update({"posts_created": 1}))
    negative("boundary_form_submitted", lambda d: d["runtime_boundary"].update({"forms_submitted": 1}))
    negative("boundary_pr_opened", lambda d: d["runtime_boundary"].update({"prs_opened": 1}))
    negative("boundary_bounty_claim", lambda d: d["runtime_boundary"].update({"bounty_claims": 1}))
    negative("boundary_message_sent", lambda d: d["runtime_boundary"].update({"messages_sent": 1}))
    negative("boundary_browser_started", lambda d: d["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("boundary_account_action", lambda d: d["runtime_boundary"].update({"account_actions": True}))
    negative("boundary_worker_started", lambda d: d["runtime_boundary"].update({"worker_starts": 1}))
    negative("boundary_service_request_updated", lambda d: d["runtime_boundary"].update({"service_requests_updated": 1}))
    negative("boundary_mcp_tool_call", lambda d: d["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("boundary_model_api_call", lambda d: d["runtime_boundary"].update({"model_api_calls": True}))
    negative("boundary_payment_action", lambda d: d["runtime_boundary"].update({"payment_actions": True}))
    negative("boundary_external_side_effect", lambda d: d["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_decision(
    decision: dict[str, Any],
    schema: dict[str, Any],
    route: dict[str, Any],
    intake_validation: dict[str, Any],
    egress_validation: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    if schema.get("properties", {}).get("route_id", {}).get("const") != TARGET_ROUTE_ID:
        errors.append("schema_route_const_must_target_public_action_gateway")
    if schema.get("properties", {}).get("egress_type", {}).get("const") != TARGET_EGRESS_TYPE:
        errors.append("schema_egress_type_const_must_target_public_submission")
    if schema.get("properties", {}).get("public_action_allowed", {}).get("const") is not False:
        errors.append("schema_public_action_allowed_must_be_false")
    if schema.get("properties", {}).get("live_egress_allowed", {}).get("const") is not False:
        errors.append("schema_live_egress_allowed_must_be_false")

    for field in REQUIRED_FIELDS:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    if intake_validation.get("all_checks_passed") is not True:
        errors.append("source_intake_contract_validation_not_passing")
    if intake_validation.get("route_count") < 8 or intake_validation.get("template_count") < 8:
        errors.append("source_intake_contract_must_cover_gateway_routes")
    if intake_validation.get("decisions_applied") != 0 or intake_validation.get("external_side_effects") is not False:
        errors.append("source_intake_contract_must_be_report_only")
    if egress_validation.get("all_checks_passed") is not True:
        errors.append("source_agent_egress_event_ledger_validation_not_passing")
    if egress_validation.get("live_egress_events_recorded") != 0:
        errors.append("source_agent_egress_event_ledger_must_have_zero_live_events")

    decision_value = decision.get("decision")
    if decision_value not in {"deny", "approve_route_preflight_only"}:
        errors.append("decision_must_be_deny_or_preflight_only")
    if decision.get("schema_version") != "agent_company.egress_route_signed_decision_intake_contract.v1":
        errors.append("schema_version_mismatch")
    if decision.get("route_id") != TARGET_ROUTE_ID:
        errors.append("route_id_must_match_public_action_gateway")
    if decision.get("egress_type") != TARGET_EGRESS_TYPE:
        errors.append("egress_type_must_be_public_submission")
    if not decision.get("operator_id"):
        errors.append("operator_id_required")
    if not decision.get("operator_attestation"):
        errors.append("operator_attestation_required")

    signed = parse_utc(str(decision.get("signed_utc", "")))
    expires = parse_utc(str(decision.get("expires_utc", "")))
    if signed is None:
        errors.append("signed_utc_must_be_valid")
    if expires is None:
        errors.append("expires_utc_must_be_valid")
    if signed and expires and expires <= signed:
        errors.append("expires_utc_must_be_after_signed_utc")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("decision_expired")

    docket_path = str(decision.get("source_gateway_docket_path", ""))
    if decision.get("source_gateway_docket_path") != str(GATEWAY_DOCKET):
        errors.append("source_gateway_docket_path_must_match")
    if not path_inside_root(docket_path):
        errors.append("source_gateway_docket_path_must_stay_inside_lab")
    if decision.get("source_gateway_docket_sha256") != sha256_path(GATEWAY_DOCKET):
        errors.append("source_gateway_docket_sha256_mismatch")

    required_gates = copy.deepcopy(route["required_gates"])
    if route.get("egress_type") != TARGET_EGRESS_TYPE:
        errors.append("source_route_egress_type_mismatch")
    if route.get("gateway_registration_allowed") is not False or route.get("gateway_start_allowed") is not False:
        errors.append("source_route_gateway_must_remain_blocked")
    if route.get("live_execution_allowed") is not False:
        errors.append("source_route_live_execution_must_be_false")

    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_scope_must_be_none")
        if decision.get("allowed_gate_ids") != []:
            errors.append("deny_allowed_gate_ids_must_be_empty")
        if decision.get("operator_attestation") != "deny-all-no-egress":
            errors.append("deny_attestation_must_match")
    else:
        if decision.get("allowed_scope") != f"egress_route_preflight_only:{TARGET_ROUTE_ID}":
            errors.append("allowed_scope_must_be_exact_preflight_scope")
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("operator_attestation_must_match_exact_public_action_text")
        if decision.get("allowed_gate_ids") != required_gates:
            errors.append("allowed_gate_ids_must_match_route_required_gates")
        for gate in [
            "public_action_execution_gate",
            "reputation_review_worker",
            "agent_egress_event_ledger_v1",
            "exact_action_body_approval",
        ]:
            if gate not in decision.get("allowed_gate_ids", []):
                errors.append(f"missing_required_gate:{gate}")
        if len(str(decision.get("rollback_plan", "")).strip()) < 40:
            errors.append("rollback_plan_too_short")

    false_keys = [
        "gateway_registration_allowed",
        "gateway_start_allowed",
        "live_egress_allowed",
        "public_action_allowed",
        "public_actions",
        "browser_session_start_allowed",
        "worker_registration_allowed",
        "worker_start_allowed",
        "runtime_start_allowed",
        "account_actions",
        "mcp_tool_calls",
        "model_api_calls",
        "external_side_effects",
    ]
    for key in false_keys:
        if decision.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    for key in ["browser_sessions_started", "service_requests_assigned", "service_requests_updated"]:
        if decision.get(key) != 0:
            errors.append(f"{key}_must_be_zero")
    if decision.get("approval_is_not_apply") is not True:
        errors.append("approval_is_not_apply_must_be_true")

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
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "public_action_allowed": False,
        "public_actions": False,
        "browser_session_start_allowed": False,
        "browser_sessions_started": 0,
        "account_actions": False,
        "worker_start_allowed": False,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "mcp_tool_calls": False,
        "model_api_calls": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    route = route_summary()["route"]
    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        decision = copy.deepcopy(fixture["decision"]) if "decision" in fixture else load_json(Path(fixture["path"]))
        result = validate_decision(decision, schema, route, intake_validation, egress_validation)
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
        "schema_version": "agent_company.public_action_egress_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_intake_contract_path": str(INTAKE_REPORT),
        "source_intake_contract_validation_path": str(INTAKE_VALIDATION),
        "source_agent_egress_event_ledger_validation_path": str(EGRESS_VALIDATION),
        "source_gateway_docket_path": str(GATEWAY_DOCKET),
        "source_gateway_docket_sha256": sha256_path(GATEWAY_DOCKET),
        "target_route_required_gates": copy.deepcopy(route["required_gates"]),
        "blocked_actions": copy.deepcopy(route["blocked_actions"]),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "positive_authority": {
            "accepted_scope": f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
            "public_action_allowed": False,
            "public_actions": False,
            "browser_session_start_allowed": False,
            "browser_sessions_started": 0,
            "account_actions": False,
            "gateway_registration_allowed": False,
            "gateway_start_allowed": False,
            "live_egress_allowed": False,
            "worker_start_allowed": False,
        },
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.public_action_egress_signed_decision_guard_validation.v1",
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
        "apply_allowed": False,
        "decisions_applied": 0,
        "approval_rows_written": 0,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation
