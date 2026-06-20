"""Core guard logic for report-only MCP egress apply commands."""

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

SCHEMA_PATH = ARCH / "mcp-egress-apply-command-guard-v1.schema.json"
APPLY_PREFLIGHT_REPORT = REPORTS / "mcp-egress-apply-preflight-blocker-v1-20260618.json"
APPLY_PREFLIGHT_VALIDATION = REPORTS / "mcp-egress-apply-preflight-blocker-v1-validation-20260618.json"
GUARD_VALIDATION = REPORTS / "mcp-egress-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
MCP_REGISTRY_VALIDATION = REPORTS / "mcp-tool-registry-gate-v1-validation-20260617.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "mcp-egress-apply-command-guard-v1-fixtures"
REPORT_JSON = REPORTS / "mcp-egress-apply-command-guard-v1-20260618.json"
VALIDATION_JSON = REPORTS / "mcp-egress-apply-command-guard-v1-validation-20260618.json"
REPORT_MD = REPORTS / "mcp-egress-apply-command-guard-v1-20260618.md"

TARGET_ROUTE_ID = "mcp_tool_gateway"
TARGET_EGRESS_TYPE = "mcp_tool"
TRACE_ID = "trace-mcp-egress-apply-command-guard-v1-20260618"
NEXT_ACTION = "Keep MCP egress blocked until a real signed operator MCP egress decision and exact command preview exist; then build an execution guard before any MCP server enable/start, MCP tool call, credential access, worker start, or live egress."

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registrations": 0,
    "gateway_starts": 0,
    "live_egress_events": 0,
    "mcp_servers_started": 0,
    "mcp_servers_enabled": 0,
    "mcp_server_enable_allowed": False,
    "mcp_tool_call_allowed": False,
    "credentials_created": False,
    "credential_access_allowed": False,
    "registry_publications": 0,
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
    "command_id",
    "command_type",
    "target_route_id",
    "target_egress_type",
    "source_apply_preflight_blocker_path",
    "source_guard_validation_path",
    "source_intake_validation_path",
    "source_gateway_docket_validation_path",
    "expected_source_apply_preflight_status",
    "real_signed_decision_path",
    "real_signed_decision_present",
    "allowed_scope",
    "target_request_ids",
    "apply_command_allowed",
    "apply_allowed",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "mcp_server_enable_allowed",
    "mcp_tool_call_allowed",
    "mcp_servers_started",
    "mcp_servers_enabled",
    "credentials_created",
    "credential_access_allowed",
    "worker_start_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
    "runtime_boundary",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return str(value).startswith(str(ROOT)) and ".." not in str(value)


def source_summary() -> dict[str, Any]:
    preflight_validation = load_json(APPLY_PREFLIGHT_VALIDATION)
    guard_validation = load_json(GUARD_VALIDATION)
    intake_validation = load_json(INTAKE_VALIDATION)
    gateway_validation = load_json(GATEWAY_DOCKET_VALIDATION)
    mcp_registry_validation = load_json(MCP_REGISTRY_VALIDATION)
    egress_ledger_validation = load_json(EGRESS_LEDGER_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    return {
        "apply_preflight_validation_path": str(APPLY_PREFLIGHT_VALIDATION),
        "apply_preflight_all_checks_passed": preflight_validation.get("all_checks_passed"),
        "apply_preflight_status": preflight_validation.get("apply_preflight_status"),
        "apply_command_contract_present": preflight_validation.get("apply_command_contract_present"),
        "apply_allowed": preflight_validation.get("apply_allowed"),
        "gateway_start_allowed": preflight_validation.get("gateway_start_allowed"),
        "live_egress_allowed": preflight_validation.get("live_egress_allowed"),
        "mcp_server_enable_allowed": preflight_validation.get("mcp_server_enable_allowed"),
        "mcp_tool_call_allowed": preflight_validation.get("mcp_tool_call_allowed"),
        "mcp_servers_started": preflight_validation.get("mcp_servers_started"),
        "mcp_servers_enabled": preflight_validation.get("mcp_servers_enabled"),
        "mcp_tool_calls": preflight_validation.get("mcp_tool_calls"),
        "credentials_created": preflight_validation.get("credentials_created"),
        "credential_access_allowed": preflight_validation.get("credential_access_allowed"),
        "worker_start_allowed": preflight_validation.get("worker_start_allowed"),
        "service_requests_assigned": preflight_validation.get("service_requests_assigned"),
        "service_requests_updated": preflight_validation.get("service_requests_updated"),
        "external_side_effects": preflight_validation.get("external_side_effects"),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_all_checks_passed": guard_validation.get("all_checks_passed"),
        "guard_target_route_id": guard_validation.get("target_route_id"),
        "guard_target_egress_type": guard_validation.get("target_egress_type"),
        "guard_live_egress_events": guard_validation.get("live_egress_events"),
        "guard_mcp_servers_started": guard_validation.get("mcp_servers_started"),
        "guard_mcp_servers_enabled": guard_validation.get("mcp_servers_enabled"),
        "guard_mcp_tool_calls": guard_validation.get("mcp_tool_calls"),
        "guard_credentials_created": guard_validation.get("credentials_created"),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_all_checks_passed": intake_validation.get("all_checks_passed"),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_all_checks_passed": gateway_validation.get("all_checks_passed"),
        "mcp_registry_validation_path": str(MCP_REGISTRY_VALIDATION),
        "mcp_registry_all_checks_passed": mcp_registry_validation.get("all_checks_passed"),
        "mcp_registry_mcp_servers_started": mcp_registry_validation.get("mcp_servers_started"),
        "mcp_registry_mcp_servers_enabled": mcp_registry_validation.get("mcp_servers_enabled"),
        "mcp_registry_mcp_tool_calls": mcp_registry_validation.get("mcp_tool_calls"),
        "mcp_registry_credentials_created": mcp_registry_validation.get("credentials_created"),
        "egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "egress_ledger_all_checks_passed": egress_ledger_validation.get("all_checks_passed"),
        "egress_ledger_live_egress_allowed": egress_ledger_validation.get("live_egress_allowed"),
        "egress_ledger_mcp_tool_calls": egress_ledger_validation.get("mcp_tool_calls"),
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "identity_all_checks_passed": identity_validation.get("all_checks_passed"),
        "identity_worker_starts": identity_validation.get("worker_starts"),
        "identity_credentials_created": identity_validation.get("credentials_created"),
    }


def base_command(command_id: str, command_type: str = "report_only_apply_command_guard") -> dict[str, Any]:
    return {
        "schema_version": "agent_company.mcp_egress_apply_command_guard.v1",
        "command_id": command_id,
        "command_type": command_type,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
        "source_guard_validation_path": str(GUARD_VALIDATION),
        "source_intake_validation_path": str(INTAKE_VALIDATION),
        "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "expected_source_apply_preflight_status": "blocked_no_real_signed_decision",
        "real_signed_decision_path": "",
        "real_signed_decision_present": False,
        "allowed_scope": "none" if command_type == "deny_noop" else "report_only_mcp_apply_command_guard",
        "target_request_ids": [],
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "mcp_servers_started": 0,
        "mcp_servers_enabled": 0,
        "credentials_created": False,
        "credential_access_allowed": False,
        "worker_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "model_api_calls": False,
        "mcp_tool_calls": False,
        "external_side_effects": False,
        "rollback_plan": "No MCP egress apply command exists; discard report-only guard artifacts.",
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {"name": "positive_deny_noop", "expected": "accepted", "command": base_command("mcp-egress-apply-command-positive-deny", "deny_noop")},
        {"name": "positive_report_only_guard", "expected": "accepted", "command": base_command("mcp-egress-apply-command-positive-guard")},
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        command = base_command(f"mcp-egress-apply-command-negative-{name}")
        mutate(command)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "command": command})

    negative("wrong_route", lambda c: c.update({"target_route_id": "browser_read_only_gateway"}))
    negative("wrong_egress_type", lambda c: c.update({"target_egress_type": "browser_read_only"}))
    negative("missing_source_preflight", lambda c: c.update({"source_apply_preflight_blocker_path": ""}))
    negative("outside_source_preflight", lambda c: c.update({"source_apply_preflight_blocker_path": r"C:\Temp\preflight.json"}))
    negative("wrong_source_preflight", lambda c: c.update({"source_apply_preflight_blocker_path": str(REPORTS / "stale-egress-preflight.json")}))
    negative("wrong_guard_validation", lambda c: c.update({"source_guard_validation_path": str(REPORTS / "stale-egress-guard.json")}))
    negative("wrong_intake_validation", lambda c: c.update({"source_intake_validation_path": str(REPORTS / "stale-egress-intake.json")}))
    negative("wrong_gateway_validation", lambda c: c.update({"source_gateway_docket_validation_path": str(REPORTS / "stale-gateway.json")}))
    negative("wrong_expected_status", lambda c: c.update({"expected_source_apply_preflight_status": "ready_for_live_apply"}))
    negative("real_signed_decision_present", lambda c: c.update({"real_signed_decision_present": True, "real_signed_decision_path": str(REPORTS / "real-egress-decision.json")}))
    negative("execute_command_type", lambda c: c.update({"command_type": "execute_mcp_gateway_apply"}))
    negative("execute_scope", lambda c: c.update({"allowed_scope": "mcp_tool_live_apply"}))
    negative("target_request_id", lambda c: c.update({"target_request_ids": ["req-wave4-digital-products-browser-readonly-20260614"]}))
    negative("apply_command_allowed", lambda c: c.update({"apply_command_allowed": True}))
    negative("apply_allowed", lambda c: c.update({"apply_allowed": True}))
    negative("gateway_registration_allowed", lambda c: c.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda c: c.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda c: c.update({"live_egress_allowed": True}))
    negative("mcp_server_enable_allowed", lambda c: c.update({"mcp_server_enable_allowed": True}))
    negative("mcp_tool_call_allowed", lambda c: c.update({"mcp_tool_call_allowed": True}))
    negative("mcp_server_started", lambda c: c.update({"mcp_servers_started": 1}))
    negative("mcp_server_enabled", lambda c: c.update({"mcp_servers_enabled": 1}))
    negative("credentials_created", lambda c: c.update({"credentials_created": True}))
    negative("credential_access_allowed", lambda c: c.update({"credential_access_allowed": True}))
    negative("worker_start_allowed", lambda c: c.update({"worker_start_allowed": True}))
    negative("service_request_assigned", lambda c: c.update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda c: c.update({"service_requests_updated": 1}))
    negative("model_api_call", lambda c: c.update({"model_api_calls": True}))
    negative("mcp_tool_call", lambda c: c.update({"mcp_tool_calls": True}))
    negative("external_side_effect_top_level", lambda c: c.update({"external_side_effects": True}))
    negative("short_rollback", lambda c: c.update({"rollback_plan": "none"}))
    negative("command_written", lambda c: c["runtime_boundary"].update({"apply_commands_written": 1}))
    negative("command_executed", lambda c: c["runtime_boundary"].update({"apply_commands_executed": 1}))
    negative("decision_applied", lambda c: c["runtime_boundary"].update({"decisions_applied": 1}))
    negative("approval_written", lambda c: c["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("gateway_registered", lambda c: c["runtime_boundary"].update({"gateway_registrations": 1}))
    negative("gateway_started", lambda c: c["runtime_boundary"].update({"gateway_starts": 1}))
    negative("live_egress", lambda c: c["runtime_boundary"].update({"live_egress_events": 1}))
    negative("boundary_mcp_server_enable_allowed", lambda c: c["runtime_boundary"].update({"mcp_server_enable_allowed": True}))
    negative("boundary_mcp_tool_call_allowed", lambda c: c["runtime_boundary"].update({"mcp_tool_call_allowed": True}))
    negative("boundary_mcp_server_started", lambda c: c["runtime_boundary"].update({"mcp_servers_started": 1}))
    negative("boundary_mcp_server_enabled", lambda c: c["runtime_boundary"].update({"mcp_servers_enabled": 1}))
    negative("boundary_credentials_created", lambda c: c["runtime_boundary"].update({"credentials_created": True}))
    negative("boundary_credential_access_allowed", lambda c: c["runtime_boundary"].update({"credential_access_allowed": True}))
    negative("registry_publication", lambda c: c["runtime_boundary"].update({"registry_publications": 1}))
    negative("worker_started", lambda c: c["runtime_boundary"].update({"worker_starts": 1}))
    negative("service_request_boundary", lambda c: c["runtime_boundary"].update({"service_requests_updated": 1}))
    negative("public_action", lambda c: c["runtime_boundary"].update({"public_actions": True}))
    negative("external_side_effect_boundary", lambda c: c["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_command(command: dict[str, Any], schema: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if schema.get("properties", {}).get("command_type", {}).get("enum", [None])[0] != "deny_noop":
        errors.append("schema_command_type_enum_must_start_deny_noop")
    if schema.get("properties", {}).get("target_route_id", {}).get("const") != TARGET_ROUTE_ID:
        errors.append("schema_target_route_must_be_mcp_tool_gateway")
    if schema.get("properties", {}).get("target_egress_type", {}).get("const") != TARGET_EGRESS_TYPE:
        errors.append("schema_target_egress_type_must_be_mcp_tool")
    for field in REQUIRED_FIELDS:
        if field not in command:
            errors.append(f"missing_required_field:{field}")

    if command.get("schema_version") != "agent_company.mcp_egress_apply_command_guard.v1":
        errors.append("schema_version_mismatch")
    if command.get("target_route_id") != TARGET_ROUTE_ID:
        errors.append("target_route_id_must_match_mcp_tool_gateway")
    if command.get("target_egress_type") != TARGET_EGRESS_TYPE:
        errors.append("target_egress_type_must_match_mcp_tool")

    source_preflight = str(command.get("source_apply_preflight_blocker_path", ""))
    if not source_preflight:
        errors.append("source_apply_preflight_blocker_path_missing")
    elif not path_inside_root(source_preflight):
        errors.append("source_apply_preflight_blocker_path_must_stay_inside_lab")
    elif source_preflight != str(APPLY_PREFLIGHT_VALIDATION):
        errors.append("source_apply_preflight_blocker_path_must_match_current_validation")
    elif not Path(source_preflight).exists():
        errors.append("source_apply_preflight_blocker_path_not_found")

    for key, expected in [
        ("source_guard_validation_path", str(GUARD_VALIDATION)),
        ("source_intake_validation_path", str(INTAKE_VALIDATION)),
        ("source_gateway_docket_validation_path", str(GATEWAY_DOCKET_VALIDATION)),
    ]:
        value = str(command.get(key, ""))
        if value != expected:
            errors.append(f"{key}_must_match_current_source")
        if value and not path_inside_root(value):
            errors.append(f"{key}_must_stay_inside_lab")

    if source.get("apply_preflight_all_checks_passed") is not True:
        errors.append("source_apply_preflight_must_pass")
    if source.get("apply_preflight_status") != "blocked_no_real_signed_decision":
        errors.append("source_apply_preflight_status_must_be_blocked_no_real_signed_decision")
    if command.get("expected_source_apply_preflight_status") != source.get("apply_preflight_status"):
        errors.append("expected_source_apply_preflight_status_must_match_source")
    if (
        source.get("guard_all_checks_passed") is not True
        or source.get("guard_target_route_id") != TARGET_ROUTE_ID
        or source.get("guard_target_egress_type") != TARGET_EGRESS_TYPE
    ):
        errors.append("source_guard_validation_must_pass_for_target_route")
    for key in ["guard_mcp_servers_started", "guard_mcp_servers_enabled"]:
        if source.get(key) != 0:
            errors.append(f"source_{key}_must_be_zero")
    for key in ["guard_mcp_tool_calls", "guard_credentials_created"]:
        if source.get(key) is not False:
            errors.append(f"source_{key}_must_be_false")
    if source.get("intake_all_checks_passed") is not True:
        errors.append("source_intake_validation_must_pass")
    if source.get("gateway_all_checks_passed") is not True:
        errors.append("source_gateway_validation_must_pass")
    if source.get("mcp_registry_all_checks_passed") is not True:
        errors.append("source_mcp_registry_validation_must_pass")
    for key in ["mcp_registry_mcp_servers_started", "mcp_registry_mcp_servers_enabled"]:
        if source.get(key) != 0:
            errors.append(f"source_{key}_must_be_zero")
    for key in ["mcp_registry_mcp_tool_calls", "mcp_registry_credentials_created"]:
        if source.get(key) is not False:
            errors.append(f"source_{key}_must_be_false")
    if source.get("egress_ledger_all_checks_passed") is not True:
        errors.append("source_egress_ledger_validation_must_pass")
    if source.get("egress_ledger_live_egress_allowed") is not False or source.get("egress_ledger_mcp_tool_calls") is not False:
        errors.append("source_egress_ledger_must_block_mcp_live_egress")
    if source.get("identity_all_checks_passed") is not True:
        errors.append("source_identity_validation_must_pass")
    if source.get("identity_worker_starts") != 0 or source.get("identity_credentials_created") is not False:
        errors.append("source_identity_must_not_start_workers_or_create_credentials")
    for key in [
        "apply_allowed",
        "gateway_start_allowed",
        "live_egress_allowed",
        "mcp_server_enable_allowed",
        "mcp_tool_call_allowed",
        "worker_start_allowed",
        "credentials_created",
        "credential_access_allowed",
        "mcp_tool_calls",
    ]:
        if source.get(key) is not False:
            errors.append(f"source_{key}_must_be_false")
    for key in ["mcp_servers_started", "mcp_servers_enabled"]:
        if source.get(key) != 0:
            errors.append(f"source_{key}_must_be_zero")
    if source.get("service_requests_assigned") != 0 or source.get("service_requests_updated") != 0:
        errors.append("source_service_requests_must_not_be_mutated")
    if source.get("external_side_effects") is not False:
        errors.append("source_external_side_effects_must_be_false")

    if command.get("real_signed_decision_present") is not False:
        errors.append("real_signed_decision_present_must_be_false")
    if command.get("real_signed_decision_path"):
        errors.append("real_signed_decision_path_must_be_empty_for_guard_only")

    command_type = command.get("command_type")
    if command_type == "deny_noop":
        if command.get("allowed_scope") != "none":
            errors.append("deny_noop_scope_must_be_none")
    elif command_type == "report_only_apply_command_guard":
        if command.get("allowed_scope") != "report_only_mcp_apply_command_guard":
            errors.append("report_only_guard_scope_must_match")
    else:
        errors.append("command_type_invalid")

    targets = command.get("target_request_ids", [])
    if not isinstance(targets, list):
        errors.append("target_request_ids_must_be_list")
    elif targets:
        errors.append("target_request_ids_must_be_empty_without_real_signed_decision")

    for key in [
        "apply_command_allowed",
        "apply_allowed",
        "gateway_registration_allowed",
        "gateway_start_allowed",
        "live_egress_allowed",
        "mcp_server_enable_allowed",
        "mcp_tool_call_allowed",
        "credentials_created",
        "credential_access_allowed",
        "worker_start_allowed",
        "model_api_calls",
        "mcp_tool_calls",
        "external_side_effects",
    ]:
        if command.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    for key in ["mcp_servers_started", "mcp_servers_enabled", "service_requests_assigned", "service_requests_updated"]:
        if command.get(key) != 0:
            errors.append(f"{key}_must_be_zero")
    if len(str(command.get("rollback_plan", "")).strip()) < 20:
        errors.append("rollback_plan_too_short")

    boundary = command.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    accepted = not errors
    return {
        "command_id": command.get("command_id"),
        "command_type": command_type,
        "target_route_id": command.get("target_route_id"),
        "accepted_for_guard_only": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "mcp_servers_started": 0,
        "mcp_servers_enabled": 0,
        "credentials_created": False,
        "credential_access_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    source = source_summary()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        command = copy.deepcopy(fixture["command"]) if "command" in fixture else load_json(Path(fixture["path"]))
        result = validate_command(command, schema, source)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_guard_only"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_guard_only"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.mcp_egress_apply_command_guard_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_apply_preflight": source,
        "positive_authority": {
            "accepted_scope": "report_only_mcp_apply_command_guard",
            "apply_command_allowed": False,
            "apply_allowed": False,
            "gateway_registration_allowed": False,
            "gateway_start_allowed": False,
            "live_egress_allowed": False,
            "mcp_server_enable_allowed": False,
            "mcp_tool_call_allowed": False,
            "mcp_servers_started": 0,
            "mcp_servers_enabled": 0,
            "credentials_created": False,
            "credential_access_allowed": False,
            "worker_start_allowed": False,
        },
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "mcp_servers_started": 0,
        "mcp_servers_enabled": 0,
        "mcp_tool_calls": False,
        "credentials_created": False,
        "credential_access_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.mcp_egress_apply_command_guard_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "fixture_expectation_mismatch_count": len(failures),
        **copy.deepcopy(ZERO_BOUNDARY),
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "mcp_servers_started": 0,
        "mcp_servers_enabled": 0,
        "mcp_tool_calls": False,
        "credentials_created": False,
        "credential_access_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


