#!/usr/bin/env python3
"""Core helpers for report-only local A2A egress apply-command contracts."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from egress_apply_command_contract_shared_core import collect_common_contract_errors

ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"

SCHEMA_PATH = ARCH / "local-a2a-egress-apply-command-contract-v1.schema.json"
APPLY_PREFLIGHT_VALIDATION = REPORTS / "local-a2a-egress-apply-preflight-blocker-v1-validation-20260618.json"
GUARD_VALIDATION = REPORTS / "local-a2a-egress-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "local-a2a-egress-apply-command-contract-v1-fixtures"
REPORT_JSON = REPORTS / "local-a2a-egress-apply-command-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "local-a2a-egress-apply-command-contract-v1-validation-20260618.json"
REPORT_MD = REPORTS / "local-a2a-egress-apply-command-contract-v1-20260618.md"

TARGET_ROUTE_ID = "local_agent_to_agent_report_only"
TARGET_EGRESS_TYPE = "agent_to_agent"
TRACE_ID = "trace-local-a2a-egress-apply-command-contract-v1-20260618"
NEXT_ACTION = (
    "Build local A2A egress apply-command guard v1 only after a real signed operator decision and "
    "executable command preview exist; until then, keep local A2A egress blocked."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "gateway_registrations": 0,
    "gateway_starts": 0,
    "live_egress_events": 0,
    "agent_message_send_allowed": False,
    "agent_messages_sent": 0,
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
    "source_egress_ledger_validation_path",
    "source_identity_validation_path",
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
    "agent_message_send_allowed",
    "agent_messages_sent",
    "worker_start_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
    "runtime_boundary",
]

EXPECTED_SOURCE_PATHS = {
    "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
    "source_guard_validation_path": str(GUARD_VALIDATION),
    "source_intake_validation_path": str(INTAKE_VALIDATION),
    "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
    "source_egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
    "source_identity_validation_path": str(IDENTITY_VALIDATION),
}
SCHEMA_FALSE_PROPS = [
    "agent_message_send_allowed",
]
SOURCE_FALSE_FIELDS = [
    "apply_allowed",
    "agent_message_send_allowed",
    "external_side_effects",
]
SOURCE_ZERO_FIELDS = [
    "agent_messages_sent",
]
COMMAND_FALSE_FIELDS = [
    "apply_command_allowed",
    "apply_allowed",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "agent_message_send_allowed",
    "worker_start_allowed",
    "model_api_calls",
    "mcp_tool_calls",
    "external_side_effects",
]
COMMAND_ZERO_FIELDS = [
    "agent_messages_sent",
    "service_requests_assigned",
    "service_requests_updated",
    "browser_sessions_started",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    try:
        path = Path(value).resolve()
        return path.is_relative_to(ROOT.resolve())
    except Exception:
        return False


def source_summary() -> dict[str, Any]:
    preflight_validation = load_json(APPLY_PREFLIGHT_VALIDATION)
    guard_validation = load_json(GUARD_VALIDATION)
    intake_validation = load_json(INTAKE_VALIDATION)
    gateway_validation = load_json(GATEWAY_DOCKET_VALIDATION)
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
        "agent_message_send_allowed": preflight_validation.get("agent_message_send_allowed"),
        "agent_messages_sent": preflight_validation.get("agent_messages_sent"),
        "worker_start_allowed": preflight_validation.get("worker_start_allowed"),
        "service_requests_assigned": preflight_validation.get("service_requests_assigned"),
        "service_requests_updated": preflight_validation.get("service_requests_updated"),
        "external_side_effects": preflight_validation.get("external_side_effects"),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_all_checks_passed": guard_validation.get("all_checks_passed"),
        "guard_target_route_id": guard_validation.get("target_route_id"),
        "guard_target_egress_type": guard_validation.get("target_egress_type"),
        "guard_agent_message_send_allowed": guard_validation.get("agent_message_send_allowed"),
        "guard_agent_messages_sent": guard_validation.get("agent_messages_sent"),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_all_checks_passed": intake_validation.get("all_checks_passed"),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_all_checks_passed": gateway_validation.get("all_checks_passed"),
        "egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "egress_ledger_all_checks_passed": egress_ledger_validation.get("all_checks_passed"),
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "identity_all_checks_passed": identity_validation.get("all_checks_passed"),
    }


def base_command(command_id: str, command_type: str = "report_only_apply_command_contract") -> dict[str, Any]:
    return {
        "schema_version": "agent_company.local_a2a_egress_apply_command_contract.v1",
        "command_id": command_id,
        "command_type": command_type,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
        "source_guard_validation_path": str(GUARD_VALIDATION),
        "source_intake_validation_path": str(INTAKE_VALIDATION),
        "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "source_egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "source_identity_validation_path": str(IDENTITY_VALIDATION),
        "expected_source_apply_preflight_status": "blocked_no_real_signed_decision",
        "real_signed_decision_path": "",
        "real_signed_decision_present": False,
        "allowed_scope": "none" if command_type == "deny_noop" else "report_only_apply_command_contract",
        "target_request_ids": [],
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "agent_message_send_allowed": False,
        "agent_messages_sent": 0,
        "worker_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "model_api_calls": False,
        "mcp_tool_calls": False,
        "browser_sessions_started": 0,
        "external_side_effects": False,
        "rollback_plan": "No local A2A egress apply command exists; discard report-only contract artifacts.",
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_noop",
            "expected": "accepted",
            "command": base_command("local-a2a-apply-command-positive-deny", "deny_noop"),
        },
        {
            "name": "positive_report_only_contract",
            "expected": "accepted",
            "command": base_command("local-a2a-apply-command-positive-contract"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        command = base_command(f"local-a2a-apply-command-negative-{name}")
        mutate(command)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "command": command})

    negative("wrong_route", lambda c: c.update({"target_route_id": "mcp_tool_gateway"}))
    negative("wrong_egress_type", lambda c: c.update({"target_egress_type": "mcp_tool"}))
    negative("missing_source_preflight", lambda c: c.update({"source_apply_preflight_blocker_path": ""}))
    negative(
        "outside_source_preflight",
        lambda c: c.update({"source_apply_preflight_blocker_path": r"C:\Temp\preflight.json"}),
    )
    negative(
        "wrong_source_preflight",
        lambda c: c.update({"source_apply_preflight_blocker_path": str(REPORTS / "stale-a2a-preflight.json")}),
    )
    negative(
        "wrong_guard_validation",
        lambda c: c.update({"source_guard_validation_path": str(REPORTS / "stale-a2a-guard.json")}),
    )
    negative(
        "wrong_intake_validation",
        lambda c: c.update({"source_intake_validation_path": str(REPORTS / "stale-egress-intake.json")}),
    )
    negative(
        "wrong_gateway_validation",
        lambda c: c.update({"source_gateway_docket_validation_path": str(REPORTS / "stale-gateway.json")}),
    )
    negative(
        "wrong_egress_ledger_validation",
        lambda c: c.update(
            {"source_egress_ledger_validation_path": str(REPORTS / "stale-egress-ledger.json")}
        ),
    )
    negative(
        "wrong_identity_validation",
        lambda c: c.update({"source_identity_validation_path": str(REPORTS / "stale-identity.json")}),
    )
    negative(
        "wrong_expected_status",
        lambda c: c.update({"expected_source_apply_preflight_status": "ready_for_live_apply"}),
    )
    negative(
        "real_signed_decision_present",
        lambda c: c.update(
            {
                "real_signed_decision_present": True,
                "real_signed_decision_path": str(REPORTS / "real-a2a-decision.json"),
            }
        ),
    )
    negative("execute_command_type", lambda c: c.update({"command_type": "execute_local_a2a_apply"}))
    negative("execute_scope", lambda c: c.update({"allowed_scope": "local_agent_to_agent_live_apply"}))
    negative("target_request_id", lambda c: c.update({"target_request_ids": ["req-local-a2a-message-send-20260618"]}))
    negative("apply_command_allowed", lambda c: c.update({"apply_command_allowed": True}))
    negative("apply_allowed", lambda c: c.update({"apply_allowed": True}))
    negative("gateway_registration_allowed", lambda c: c.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda c: c.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda c: c.update({"live_egress_allowed": True}))
    negative("agent_message_send_allowed", lambda c: c.update({"agent_message_send_allowed": True}))
    negative("agent_messages_sent", lambda c: c.update({"agent_messages_sent": 1}))
    negative("worker_start_allowed", lambda c: c.update({"worker_start_allowed": True}))
    negative("service_request_assigned", lambda c: c.update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda c: c.update({"service_requests_updated": 1}))
    negative("model_api_call", lambda c: c.update({"model_api_calls": True}))
    negative("mcp_tool_call", lambda c: c.update({"mcp_tool_calls": True}))
    negative("browser_started", lambda c: c.update({"browser_sessions_started": 1}))
    negative("external_side_effect_top_level", lambda c: c.update({"external_side_effects": True}))
    negative("short_rollback", lambda c: c.update({"rollback_plan": "none"}))
    negative("command_written", lambda c: c["runtime_boundary"].update({"apply_commands_written": 1}))
    negative("command_executed", lambda c: c["runtime_boundary"].update({"apply_commands_executed": 1}))
    negative("decision_applied", lambda c: c["runtime_boundary"].update({"decisions_applied": 1}))
    negative("approval_written", lambda c: c["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("gateway_registered", lambda c: c["runtime_boundary"].update({"gateway_registrations": 1}))
    negative("gateway_started", lambda c: c["runtime_boundary"].update({"gateway_starts": 1}))
    negative("live_egress", lambda c: c["runtime_boundary"].update({"live_egress_events": 1}))
    negative(
        "agent_message_boundary_allowed",
        lambda c: c["runtime_boundary"].update({"agent_message_send_allowed": True}),
    )
    negative("agent_message_boundary_sent", lambda c: c["runtime_boundary"].update({"agent_messages_sent": 1}))
    negative("worker_started", lambda c: c["runtime_boundary"].update({"worker_starts": 1}))
    negative("service_request_boundary", lambda c: c["runtime_boundary"].update({"service_requests_updated": 1}))
    negative("public_action", lambda c: c["runtime_boundary"].update({"public_actions": True}))
    negative("external_side_effect_boundary", lambda c: c["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_command(command: dict[str, Any], schema: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    errors = collect_common_contract_errors(
        schema=schema,
        command=command,
        sources=source,
        required_fields=REQUIRED_FIELDS,
        schema_version="agent_company.local_a2a_egress_apply_command_contract.v1",
        target_route_id=TARGET_ROUTE_ID,
        target_egress_type=TARGET_EGRESS_TYPE,
        schema_false_props=SCHEMA_FALSE_PROPS,
        schema_route_error="schema_target_route_must_be_local_agent_to_agent_report_only",
        schema_type_error="schema_target_egress_type_must_be_agent_to_agent",
        route_error="target_route_id_must_match_local_agent_to_agent_report_only",
        type_error="target_egress_type_must_be_agent_to_agent",
        expected_paths=EXPECTED_SOURCE_PATHS,
        path_inside_root=path_inside_root,
        source_false_fields=SOURCE_FALSE_FIELDS,
        source_zero_fields=SOURCE_ZERO_FIELDS,
        command_false_fields=COMMAND_FALSE_FIELDS,
        command_zero_fields=COMMAND_ZERO_FIELDS,
        zero_boundary=ZERO_BOUNDARY,
    )
    warnings: list[str] = []

    if source.get("apply_preflight_all_checks_passed") is not True:
        errors.append("source_apply_preflight_must_pass")
    if source.get("apply_preflight_status") != "blocked_no_real_signed_decision":
        errors.append("source_apply_preflight_status_must_be_blocked_no_real_signed_decision")
    if source.get("apply_command_contract_present") is not True:
        errors.append("source_apply_preflight_must_report_contract_present")
    if source.get("apply_allowed") is not False:
        errors.append("source_apply_preflight_must_keep_apply_blocked")
    if source.get("agent_message_send_allowed") is not False or source.get("agent_messages_sent") != 0:
        errors.append("source_apply_preflight_must_have_zero_agent_messages")
    if command.get("expected_source_apply_preflight_status") != source.get("apply_preflight_status"):
        errors.append("expected_source_apply_preflight_status_must_match_source")
    if source.get("guard_all_checks_passed") is not True or source.get("guard_target_route_id") != TARGET_ROUTE_ID:
        errors.append("source_guard_must_pass_for_target_route")
    if source.get("guard_target_egress_type") != TARGET_EGRESS_TYPE:
        errors.append("source_guard_must_target_agent_to_agent")
    if source.get("guard_agent_message_send_allowed") is not False or source.get("guard_agent_messages_sent") != 0:
        errors.append("source_guard_must_have_zero_agent_messages")
    if source.get("intake_all_checks_passed") is not True:
        errors.append("source_intake_must_pass")
    if source.get("gateway_all_checks_passed") is not True:
        errors.append("source_gateway_docket_must_pass")
    if source.get("egress_ledger_all_checks_passed") is not True:
        errors.append("source_egress_ledger_must_pass")
    if source.get("identity_all_checks_passed") is not True:
        errors.append("source_identity_must_pass")

    if command.get("real_signed_decision_present") is not False:
        errors.append("real_signed_decision_present_must_be_false_for_contract_only")
    if command.get("real_signed_decision_path"):
        errors.append("real_signed_decision_path_must_be_empty_for_contract_only")

    command_type = command.get("command_type")
    if len(str(command.get("rollback_plan", "")).strip()) < 20:
        errors.append("rollback_plan_too_short")

    accepted = not errors
    return {
        "command_id": command.get("command_id"),
        "command_type": command_type,
        "target_route_id": command.get("target_route_id"),
        "target_egress_type": command.get("target_egress_type"),
        "accepted_for_contract_only": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "agent_message_send_allowed": False,
        "agent_messages_sent": 0,
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
        actual_accept = bool(result["accepted_for_contract_only"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_contract_only"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.local_a2a_egress_apply_command_contract_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_apply_preflight": source,
        "positive_authority": {
            "accepted_scope": "report_only_apply_command_contract",
            "apply_command_allowed": False,
            "apply_allowed": False,
            "gateway_registration_allowed": False,
            "gateway_start_allowed": False,
            "live_egress_allowed": False,
            "agent_message_send_allowed": False,
            "agent_messages_sent": 0,
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
        "agent_message_send_allowed": False,
        "agent_messages_sent": 0,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.local_a2a_egress_apply_command_contract_validation.v1",
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
        "agent_message_send_allowed": False,
        "agent_messages_sent": 0,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation
