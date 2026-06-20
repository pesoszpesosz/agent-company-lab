"""Core guard logic for telemetry export signed egress decisions."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from egress_signed_decision_guard_shared_core import collect_common_signed_decision_errors

ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "telemetry-export-egress-signed-decision-guard-v1.schema.json"
INTAKE_REPORT = REPORTS / "egress-route-signed-decision-intake-contract-v1-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET = REPORTS / "unified-agent-egress-gateway-docket-v1-20260618.json"
EGRESS_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-fixtures"
REPORT_JSON = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-20260618.json"
VALIDATION_JSON = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT_MD = REPORTS / "telemetry-export-egress-signed-decision-guard-v1-20260618.md"

TARGET_ROUTE_ID = "telemetry_export_gateway"
TARGET_EGRESS_TYPE = "telemetry_export"
EVALUATION_UTC = "2026-06-18T06:00:00Z"
ATTESTATION = (
    "I approve telemetry export egress route preflight review only and understand this does not export traces, "
    "upload private prompts, export credentials, sync unredacted logs, start workers, mutate service requests, "
    "call models or MCP tools, or perform live egress."
)
NEXT_ACTION = (
    "Build telemetry_export_gateway apply preflight blocker before any external trace export, private prompt "
    "upload, credential export, unredacted log sync, service-request mutation, worker start, model/MCP call, "
    "live egress, or external side effect."
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
    "telemetry_export_allowed": False,
    "telemetry_exports": 0,
    "external_trace_export_allowed": False,
    "external_trace_exports": 0,
    "private_prompt_upload_allowed": False,
    "private_prompts_uploaded": 0,
    "credential_export_allowed": False,
    "credentials_exported": 0,
    "unredacted_log_sync_allowed": False,
    "unredacted_logs_synced": 0,
    "redaction_policy_approved": False,
    "destination_scope_approved": False,
    "retention_policy_approved": False,
    "sample_trace_artifact_approved": False,
    "worker_registrations": 0,
    "worker_start_allowed": False,
    "worker_starts": 0,
    "runtime_starts": 0,
    "dependency_installs": 0,
    "browser_session_start_allowed": False,
    "browser_sessions_started": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "mcp_tool_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "real_money_actions": False,
    "security_testing_actions": False,
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
    "telemetry_export_allowed",
    "external_trace_export_allowed",
    "private_prompt_upload_allowed",
    "credential_export_allowed",
    "unredacted_log_sync_allowed",
    "worker_start_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
    "runtime_boundary",
]

SCHEMA_FALSE_PROPS = [
    "telemetry_export_allowed",
    "external_trace_export_allowed",
    "private_prompt_upload_allowed",
    "credential_export_allowed",
    "unredacted_log_sync_allowed",
    "live_egress_allowed",
]
DECISION_FALSE_FIELDS = [
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "telemetry_export_allowed",
    "external_trace_export_allowed",
    "private_prompt_upload_allowed",
    "credential_export_allowed",
    "unredacted_log_sync_allowed",
    "redaction_policy_approved",
    "destination_scope_approved",
    "retention_policy_approved",
    "sample_trace_artifact_approved",
    "worker_registration_allowed",
    "worker_start_allowed",
    "runtime_start_allowed",
    "browser_session_start_allowed",
    "mcp_tool_calls",
    "model_api_calls",
    "public_actions",
    "account_actions",
    "wallet_actions",
    "payment_actions",
    "external_side_effects",
]
DECISION_ZERO_FIELDS = ["service_requests_assigned", "service_requests_updated"]


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
        "signed_utc": "2026-06-18T05:55:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if deny else f"egress_route_preflight_only:{TARGET_ROUTE_ID}",
        "allowed_gate_ids": [] if deny else copy.deepcopy(route["required_gates"]),
        "allowed_evidence_artifact_paths": [],
        "approval_is_not_apply": True,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "telemetry_export_allowed": False,
        "external_trace_export_allowed": False,
        "private_prompt_upload_allowed": False,
        "credential_export_allowed": False,
        "unredacted_log_sync_allowed": False,
        "redaction_policy_approved": False,
        "destination_scope_approved": False,
        "retention_policy_approved": False,
        "sample_trace_artifact_approved": False,
        "worker_registration_allowed": False,
        "worker_start_allowed": False,
        "runtime_start_allowed": False,
        "browser_session_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "mcp_tool_calls": False,
        "model_api_calls": False,
        "public_actions": False,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "external_side_effects": False,
        "rollback_plan": (
            "No egress route decision is applied."
            if deny
            else "Discard generated report-only telemetry export egress route decision artifacts; no trace export, "
            "private prompt upload, credential export, unredacted log sync, service-request mutation, worker, "
            "browser, model/API, MCP, public, account, wallet, payment, or external action was started."
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_telemetry_export_route",
            "expected": "accepted",
            "decision": base_decision("telemetry-export-guard-positive-deny", "deny"),
        },
        {
            "name": "positive_telemetry_export_preflight_only",
            "expected": "accepted",
            "decision": base_decision("telemetry-export-guard-positive-preflight-only"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(f"telemetry-export-guard-negative-{name}")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    for field, value in [
        ("operator_id", ""),
        ("operator_attestation", "I approve live telemetry export."),
        ("expires_utc", "2000-01-01T00:00:00Z"),
        ("route_id", "model_api_gateway"),
        ("egress_type", "model_api"),
        ("source_gateway_docket_path", ""),
        ("source_gateway_docket_sha256", "0" * 64),
        ("allowed_scope", "telemetry_export_live_execution"),
        ("allowed_gate_ids", ["agent_egress_event_ledger_v1"]),
        ("approval_is_not_apply", False),
        ("gateway_registration_allowed", True),
        ("gateway_start_allowed", True),
        ("live_egress_allowed", True),
        ("telemetry_export_allowed", True),
        ("external_trace_export_allowed", True),
        ("private_prompt_upload_allowed", True),
        ("credential_export_allowed", True),
        ("unredacted_log_sync_allowed", True),
        ("redaction_policy_approved", True),
        ("destination_scope_approved", True),
        ("retention_policy_approved", True),
        ("sample_trace_artifact_approved", True),
        ("worker_registration_allowed", True),
        ("worker_start_allowed", True),
        ("runtime_start_allowed", True),
        ("browser_session_start_allowed", True),
        ("service_requests_assigned", 1),
        ("service_requests_updated", 1),
        ("mcp_tool_calls", True),
        ("model_api_calls", True),
        ("public_actions", True),
        ("account_actions", True),
        ("wallet_actions", True),
        ("payment_actions", True),
        ("external_side_effects", True),
    ]:
        negative(field, lambda d, f=field, v=value: d.update({f: v}))
    negative("outside_docket_path", lambda d: d.update({"source_gateway_docket_path": r"C:\Temp\gateway.json"}))
    negative("extra_unknown_gate", lambda d: d.update({"allowed_gate_ids": d["allowed_gate_ids"] + ["unknown_gate"]}))
    negative("short_rollback", lambda d: d.update({"rollback_plan": "undo"}))
    for key, value in [
        ("decisions_applied", 1),
        ("approval_rows_written", 1),
        ("gateway_registrations", 1),
        ("gateway_starts", 1),
        ("live_egress_events", 1),
        ("telemetry_export_allowed", True),
        ("telemetry_exports", 1),
        ("external_trace_export_allowed", True),
        ("external_trace_exports", 1),
        ("private_prompt_upload_allowed", True),
        ("private_prompts_uploaded", 1),
        ("credential_export_allowed", True),
        ("credentials_exported", 1),
        ("unredacted_log_sync_allowed", True),
        ("unredacted_logs_synced", 1),
        ("redaction_policy_approved", True),
        ("destination_scope_approved", True),
        ("retention_policy_approved", True),
        ("sample_trace_artifact_approved", True),
        ("worker_starts", 1),
        ("runtime_starts", 1),
        ("browser_sessions_started", 1),
        ("service_requests_updated", 1),
        ("mcp_tool_calls", True),
        ("model_api_calls", True),
        ("public_actions", True),
        ("account_actions", True),
        ("wallet_actions", True),
        ("payment_actions", True),
        ("external_side_effects", True),
    ]:
        negative(f"boundary_{key}", lambda d, k=key, v=value: d["runtime_boundary"].update({k: v}))
    return fixtures


def validate_decision(
    decision: dict[str, Any],
    schema: dict[str, Any],
    route: dict[str, Any],
    intake_validation: dict[str, Any],
    egress_validation: dict[str, Any],
    identity_validation: dict[str, Any],
) -> dict[str, Any]:
    errors = collect_common_signed_decision_errors(
        schema=schema,
        decision=decision,
        route=route,
        required_fields=REQUIRED_FIELDS,
        schema_version="agent_company.egress_route_signed_decision_intake_contract.v1",
        target_route_id=TARGET_ROUTE_ID,
        target_egress_type=TARGET_EGRESS_TYPE,
        evaluation_utc=EVALUATION_UTC,
        expected_docket_path=str(GATEWAY_DOCKET),
        expected_docket_sha256=sha256_path(GATEWAY_DOCKET),
        path_inside_root=path_inside_root,
        parse_utc=parse_utc,
        schema_false_props=SCHEMA_FALSE_PROPS,
        schema_route_error="schema_route_const_must_target_telemetry_export_gateway",
        schema_type_error="schema_egress_type_const_must_target_telemetry_export",
        route_error="route_id_must_match_telemetry_export_gateway",
        type_error="egress_type_must_be_telemetry_export",
        decision_false_fields=DECISION_FALSE_FIELDS,
        decision_zero_fields=DECISION_ZERO_FIELDS,
        zero_boundary=ZERO_BOUNDARY,
    )
    if intake_validation.get("all_checks_passed") is not True:
        errors.append("source_intake_contract_validation_not_passing")
    if (
        egress_validation.get("all_checks_passed") is not True
        or egress_validation.get("live_egress_events_recorded") != 0
    ):
        errors.append("source_agent_egress_event_ledger_must_have_zero_live_events")
    if (
        identity_validation.get("all_checks_passed") is not True
        or identity_validation.get("credentials_created") is not False
    ):
        errors.append("source_identity_envelope_must_not_create_credentials")

    decision_value = decision.get("decision")
    required_gates = copy.deepcopy(route["required_gates"])

    if decision_value == "deny":
        pass
    else:
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("operator_attestation_must_match_exact_telemetry_text")
        for gate in [
            "telemetry_privacy_export_gate_v1",
            "agent_egress_event_ledger_v1",
            "secrets_credentials_handling_gate",
        ]:
            if gate not in decision.get("allowed_gate_ids", []):
                errors.append(f"missing_required_gate:{gate}")
        if len(str(decision.get("rollback_plan", "")).strip()) < 60:
            errors.append("rollback_plan_too_short")

    accepted = not errors
    return {
        "decision_id": decision.get("decision_id"),
        "decision": decision_value,
        "route_id": decision.get("route_id"),
        "accepted_for_apply_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "telemetry_export_allowed": False,
        "external_trace_export_allowed": False,
        "private_prompt_upload_allowed": False,
        "credential_export_allowed": False,
        "unredacted_log_sync_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "worker_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    route = route_summary()["route"]
    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        decision = copy.deepcopy(fixture["decision"]) if "decision" in fixture else load_json(Path(fixture["path"]))
        result = validate_decision(decision, schema, route, intake_validation, egress_validation, identity_validation)
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
        "schema_version": "agent_company.telemetry_export_egress_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_intake_contract_path": str(INTAKE_REPORT),
        "source_intake_contract_validation_path": str(INTAKE_VALIDATION),
        "source_agent_egress_event_ledger_validation_path": str(EGRESS_VALIDATION),
        "source_identity_validation_path": str(IDENTITY_VALIDATION),
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
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.telemetry_export_egress_signed_decision_guard_validation.v1",
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
