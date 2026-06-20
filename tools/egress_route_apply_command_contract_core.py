#!/usr/bin/env python3
"""Core helpers for report-only egress-route apply-command contracts."""

from __future__ import annotations

import argparse
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

SCHEMA_PATH = ARCH / "egress-route-apply-command-contract-v1.schema.json"
APPLY_PREFLIGHT_REPORT = REPORTS / "egress-route-apply-preflight-blocker-v1-20260618.json"
APPLY_PREFLIGHT_VALIDATION = REPORTS / "egress-route-apply-preflight-blocker-v1-validation-20260618.json"
GUARD_VALIDATION = REPORTS / "egress-route-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
FIXTURE_DIR = REPORTS / "egress-route-apply-command-contract-v1-fixtures"
REPORT_JSON = REPORTS / "egress-route-apply-command-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "egress-route-apply-command-contract-v1-validation-20260618.json"
REPORT_MD = REPORTS / "egress-route-apply-command-contract-v1-20260618.md"

TARGET_ROUTE_ID = "browser_read_only_gateway"
TRACE_ID = "trace-egress-route-apply-command-contract-v1-20260618"

ZERO_BOUNDARY = {
    "report_only": True,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
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
    "command_id",
    "command_type",
    "target_route_id",
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
    "browser_session_start_allowed",
    "worker_start_allowed",
    "service_requests_assigned",
    "service_requests_updated",
    "rollback_plan",
    "runtime_boundary",
]

EXPECTED_SOURCE_PATHS = {
    "source_guard_validation_path": str(GUARD_VALIDATION),
    "source_intake_validation_path": str(INTAKE_VALIDATION),
    "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
}
SOURCE_FALSE_FIELDS = [
    "apply_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "browser_session_start_allowed",
    "worker_start_allowed",
    "external_side_effects",
]
COMMAND_FALSE_FIELDS = [
    "apply_command_allowed",
    "apply_allowed",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "browser_session_start_allowed",
    "worker_start_allowed",
    "model_api_calls",
    "mcp_tool_calls",
    "external_side_effects",
]
COMMAND_ZERO_FIELDS = ["service_requests_assigned", "service_requests_updated"]


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
    return {
        "apply_preflight_validation_path": str(APPLY_PREFLIGHT_VALIDATION),
        "apply_preflight_all_checks_passed": preflight_validation.get("all_checks_passed"),
        "apply_preflight_status": preflight_validation.get("apply_preflight_status"),
        "apply_command_contract_present": preflight_validation.get("apply_command_contract_present"),
        "apply_allowed": preflight_validation.get("apply_allowed"),
        "gateway_start_allowed": preflight_validation.get("gateway_start_allowed"),
        "live_egress_allowed": preflight_validation.get("live_egress_allowed"),
        "browser_session_start_allowed": preflight_validation.get("browser_session_start_allowed"),
        "worker_start_allowed": preflight_validation.get("worker_start_allowed"),
        "service_requests_assigned": preflight_validation.get("service_requests_assigned"),
        "service_requests_updated": preflight_validation.get("service_requests_updated"),
        "external_side_effects": preflight_validation.get("external_side_effects"),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_all_checks_passed": guard_validation.get("all_checks_passed"),
        "guard_target_route_id": guard_validation.get("target_route_id"),
        "guard_live_egress_events": guard_validation.get("live_egress_events"),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_all_checks_passed": intake_validation.get("all_checks_passed"),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_all_checks_passed": gateway_validation.get("all_checks_passed"),
    }


def base_command(command_id: str, command_type: str = "report_only_apply_command_contract") -> dict[str, Any]:
    return {
        "schema_version": "agent_company.egress_route_apply_command_contract.v1",
        "command_id": command_id,
        "command_type": command_type,
        "target_route_id": TARGET_ROUTE_ID,
        "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
        "source_guard_validation_path": str(GUARD_VALIDATION),
        "source_intake_validation_path": str(INTAKE_VALIDATION),
        "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
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
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "model_api_calls": False,
        "mcp_tool_calls": False,
        "external_side_effects": False,
        "rollback_plan": "No egress apply command exists; discard report-only contract artifacts.",
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_noop",
            "expected": "accepted",
            "command": base_command("egress-route-apply-command-positive-deny", "deny_noop"),
        },
        {
            "name": "positive_report_only_contract",
            "expected": "accepted",
            "command": base_command("egress-route-apply-command-positive-contract"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        command = base_command(f"egress-route-apply-command-negative-{name}")
        mutate(command)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "command": command})

    negative("wrong_route", lambda c: c.update({"target_route_id": "mcp_tool_gateway"}))
    negative("missing_source_preflight", lambda c: c.update({"source_apply_preflight_blocker_path": ""}))
    negative(
        "outside_source_preflight",
        lambda c: c.update({"source_apply_preflight_blocker_path": r"C:\Temp\preflight.json"}),
    )
    negative(
        "wrong_source_preflight",
        lambda c: c.update({"source_apply_preflight_blocker_path": str(REPORTS / "stale-egress-preflight.json")}),
    )
    negative(
        "wrong_guard_validation",
        lambda c: c.update({"source_guard_validation_path": str(REPORTS / "stale-egress-guard.json")}),
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
        "wrong_expected_status",
        lambda c: c.update({"expected_source_apply_preflight_status": "ready_for_live_apply"}),
    )
    negative(
        "real_signed_decision_present",
        lambda c: c.update(
            {
                "real_signed_decision_present": True,
                "real_signed_decision_path": str(REPORTS / "real-egress-decision.json"),
            }
        ),
    )
    negative("execute_command_type", lambda c: c.update({"command_type": "execute_browser_gateway_apply"}))
    negative("execute_scope", lambda c: c.update({"allowed_scope": "browser_read_only_live_apply"}))
    negative(
        "target_request_id",
        lambda c: c.update({"target_request_ids": ["req-wave4-digital-products-browser-readonly-20260614"]}),
    )
    negative("apply_command_allowed", lambda c: c.update({"apply_command_allowed": True}))
    negative("apply_allowed", lambda c: c.update({"apply_allowed": True}))
    negative("gateway_registration_allowed", lambda c: c.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda c: c.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda c: c.update({"live_egress_allowed": True}))
    negative("browser_start_allowed", lambda c: c.update({"browser_session_start_allowed": True}))
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
    negative("browser_started", lambda c: c["runtime_boundary"].update({"browser_sessions_started": 1}))
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
        schema_version="agent_company.egress_route_apply_command_contract.v1",
        target_route_id=TARGET_ROUTE_ID,
        target_egress_type=None,
        schema_false_props=[],
        schema_route_error="schema_target_route_must_be_browser_read_only_gateway",
        schema_type_error="schema_target_egress_type_must_be_browser_read_only",
        route_error="target_route_id_must_match_browser_read_only_gateway",
        type_error="target_egress_type_must_be_browser_read_only",
        expected_paths=EXPECTED_SOURCE_PATHS,
        path_inside_root=path_inside_root,
        source_false_fields=SOURCE_FALSE_FIELDS,
        source_zero_fields=[],
        command_false_fields=COMMAND_FALSE_FIELDS,
        command_zero_fields=COMMAND_ZERO_FIELDS,
        zero_boundary=ZERO_BOUNDARY,
        check_command_shape=False,
    )
    warnings: list[str] = []

    source_preflight = str(command.get("source_apply_preflight_blocker_path", ""))
    if not source_preflight:
        errors.append("source_apply_preflight_blocker_path_missing")
    elif not path_inside_root(source_preflight):
        errors.append("source_apply_preflight_blocker_path_must_stay_inside_lab")
    elif source_preflight != str(APPLY_PREFLIGHT_VALIDATION):
        errors.append("source_apply_preflight_blocker_path_must_match_current_validation")
    elif not Path(source_preflight).exists():
        errors.append("source_apply_preflight_blocker_path_not_found")

    if source.get("apply_preflight_all_checks_passed") is not True:
        errors.append("source_apply_preflight_must_pass")
    if source.get("apply_preflight_status") != "blocked_no_real_signed_decision":
        errors.append("source_apply_preflight_status_must_be_blocked_no_real_signed_decision")
    if command.get("expected_source_apply_preflight_status") != source.get("apply_preflight_status"):
        errors.append("expected_source_apply_preflight_status_must_match_source")
    if source.get("guard_all_checks_passed") is not True or source.get("guard_target_route_id") != TARGET_ROUTE_ID:
        errors.append("source_guard_validation_must_pass_for_target_route")
    if source.get("intake_all_checks_passed") is not True:
        errors.append("source_intake_validation_must_pass")
    if source.get("gateway_all_checks_passed") is not True:
        errors.append("source_gateway_validation_must_pass")
    if source.get("service_requests_assigned") != 0 or source.get("service_requests_updated") != 0:
        errors.append("source_service_requests_must_not_be_mutated")

    if command.get("real_signed_decision_present") is not False:
        errors.append("real_signed_decision_present_must_be_false")
    if command.get("real_signed_decision_path"):
        errors.append("real_signed_decision_path_must_be_empty_for_contract_only")

    command_type = command.get("command_type")
    if command_type == "deny_noop":
        if command.get("allowed_scope") != "none":
            errors.append("deny_noop_scope_must_be_none")
    elif command_type == "report_only_apply_command_contract":
        if command.get("allowed_scope") != "report_only_apply_command_contract":
            errors.append("report_only_contract_scope_must_match")
    else:
        errors.append("command_type_invalid")

    targets = command.get("target_request_ids", [])
    if not isinstance(targets, list):
        errors.append("target_request_ids_must_be_list")
    elif targets:
        errors.append("target_request_ids_must_be_empty_without_real_signed_decision")

    if len(str(command.get("rollback_plan", "")).strip()) < 20:
        errors.append("rollback_plan_too_short")

    accepted = not errors
    return {
        "command_id": command.get("command_id"),
        "command_type": command_type,
        "target_route_id": command.get("target_route_id"),
        "accepted_for_contract_only": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "browser_session_start_allowed": False,
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
        "schema_version": "agent_company.egress_route_apply_command_contract_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "target_route_id": TARGET_ROUTE_ID,
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
            "browser_session_start_allowed": False,
            "worker_start_allowed": False,
        },
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "next_action": (
            "Build egress route apply-command guard v1 only after a real signed operator decision and executable "
            "command preview exist; until then, keep browser egress blocked."
        ),
        **copy.deepcopy(ZERO_BOUNDARY),
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.egress_route_apply_command_contract_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "target_route_id": TARGET_ROUTE_ID,
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
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


