#!/usr/bin/env python3
"""Core helpers for report-only runtime-process egress apply-command contracts."""

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

SCHEMA_PATH = ARCH / "runtime-process-egress-apply-command-contract-v1.schema.json"
APPLY_PREFLIGHT_VALIDATION = REPORTS / "runtime-process-egress-apply-preflight-blocker-v1-validation-20260618.json"
GUARD_VALIDATION = REPORTS / "runtime-process-egress-signed-decision-guard-v1-validation-20260618.json"
INTAKE_VALIDATION = REPORTS / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
GATEWAY_DOCKET_VALIDATION = REPORTS / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
EGRESS_LEDGER_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
RUNTIME_PREFLIGHT_VALIDATION = REPORTS / "runtime-start-preflight-v1-validation-20260617.json"
RUNTIME_SIGNED_GUARD_VALIDATION = REPORTS / "runtime-start-signed-decision-guard-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "runtime-process-egress-apply-command-contract-v1-fixtures"
REPORT_JSON = REPORTS / "runtime-process-egress-apply-command-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "runtime-process-egress-apply-command-contract-v1-validation-20260618.json"
REPORT_MD = REPORTS / "runtime-process-egress-apply-command-contract-v1-20260618.md"

TARGET_ROUTE_ID = "runtime_process_gateway"
TARGET_EGRESS_TYPE = "runtime_start"
TRACE_ID = "trace-runtime-process-egress-apply-command-contract-v1-20260618"
NEXT_ACTION = (
    "Build runtime process egress apply-command guard v1 only after a real signed operator decision and "
    "executable command preview exist; until then, keep runtime process egress blocked."
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
    "dependency_installs": 0,
    "worker_registrations": 0,
    "worker_start_allowed": False,
    "worker_starts": 0,
    "runtime_start_allowed": False,
    "runtime_starts": 0,
    "queue_mutations": 0,
    "browser_sessions_started": False,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "mcp_tool_calls": False,
    "model_api_calls": False,
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
    "runtime_start_allowed",
    "runtime_starts",
    "dependency_installs",
    "queue_mutations",
    "worker_start_allowed",
    "worker_starts",
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
}
SCHEMA_FALSE_PROPS = [
    "runtime_start_allowed",
    "live_egress_allowed",
]
SOURCE_FALSE_FIELDS = [
    "apply_allowed",
    "runtime_start_allowed",
    "external_side_effects",
]
SOURCE_ZERO_FIELDS = [
    "runtime_starts",
    "dependency_installs",
    "queue_mutations",
]
COMMAND_FALSE_FIELDS = [
    "apply_command_allowed",
    "apply_allowed",
    "gateway_registration_allowed",
    "gateway_start_allowed",
    "live_egress_allowed",
    "runtime_start_allowed",
    "worker_start_allowed",
    "mcp_tool_calls",
    "model_api_calls",
    "browser_sessions_started",
    "external_side_effects",
]
COMMAND_ZERO_FIELDS = [
    "runtime_starts",
    "dependency_installs",
    "queue_mutations",
    "worker_starts",
    "service_requests_assigned",
    "service_requests_updated",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    try:
        return Path(value).resolve().is_relative_to(ROOT.resolve())
    except Exception:
        return False


def source_summary() -> dict[str, Any]:
    preflight = load_json(APPLY_PREFLIGHT_VALIDATION)
    guard = load_json(GUARD_VALIDATION)
    intake = load_json(INTAKE_VALIDATION)
    gateway = load_json(GATEWAY_DOCKET_VALIDATION)
    egress = load_json(EGRESS_LEDGER_VALIDATION)
    runtime_preflight = load_json(RUNTIME_PREFLIGHT_VALIDATION)
    runtime_guard = load_json(RUNTIME_SIGNED_GUARD_VALIDATION)
    return {
        "apply_preflight_validation_path": str(APPLY_PREFLIGHT_VALIDATION),
        "apply_preflight_all_checks_passed": preflight.get("all_checks_passed"),
        "apply_preflight_status": preflight.get("apply_preflight_status"),
        "apply_allowed": preflight.get("apply_allowed"),
        "runtime_start_allowed": preflight.get("runtime_start_allowed"),
        "runtime_starts": preflight.get("runtime_starts"),
        "dependency_installs": preflight.get("dependency_installs"),
        "queue_mutations": preflight.get("queue_mutations"),
        "worker_starts": preflight.get("worker_starts"),
        "service_requests_updated": preflight.get("service_requests_updated"),
        "external_side_effects": preflight.get("external_side_effects"),
        "guard_validation_path": str(GUARD_VALIDATION),
        "guard_all_checks_passed": guard.get("all_checks_passed"),
        "guard_target_route_id": guard.get("target_route_id"),
        "guard_target_egress_type": guard.get("target_egress_type"),
        "guard_runtime_start_allowed": guard.get("runtime_start_allowed"),
        "guard_runtime_starts": guard.get("runtime_starts"),
        "intake_validation_path": str(INTAKE_VALIDATION),
        "intake_all_checks_passed": intake.get("all_checks_passed"),
        "gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "gateway_all_checks_passed": gateway.get("all_checks_passed"),
        "egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "egress_ledger_all_checks_passed": egress.get("all_checks_passed"),
        "runtime_preflight_validation_path": str(RUNTIME_PREFLIGHT_VALIDATION),
        "runtime_preflight_all_checks_passed": runtime_preflight.get("all_checks_passed"),
        "runtime_guard_validation_path": str(RUNTIME_SIGNED_GUARD_VALIDATION),
        "runtime_guard_all_checks_passed": runtime_guard.get("all_checks_passed"),
    }


def base_command(command_id: str, command_type: str = "report_only_apply_command_contract") -> dict[str, Any]:
    return {
        "schema_version": "agent_company.runtime_process_egress_apply_command_contract.v1",
        "command_id": command_id,
        "command_type": command_type,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "source_apply_preflight_blocker_path": str(APPLY_PREFLIGHT_VALIDATION),
        "source_guard_validation_path": str(GUARD_VALIDATION),
        "source_intake_validation_path": str(INTAKE_VALIDATION),
        "source_gateway_docket_validation_path": str(GATEWAY_DOCKET_VALIDATION),
        "source_egress_ledger_validation_path": str(EGRESS_LEDGER_VALIDATION),
        "source_runtime_start_preflight_validation_path": str(RUNTIME_PREFLIGHT_VALIDATION),
        "source_runtime_start_signed_guard_validation_path": str(RUNTIME_SIGNED_GUARD_VALIDATION),
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
        "runtime_start_allowed": False,
        "runtime_starts": 0,
        "dependency_installs": 0,
        "queue_mutations": 0,
        "worker_start_allowed": False,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "mcp_tool_calls": False,
        "model_api_calls": False,
        "browser_sessions_started": False,
        "external_side_effects": False,
        "rollback_plan": "No runtime process egress apply command exists; discard report-only contract artifacts.",
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_noop",
            "expected": "accepted",
            "command": base_command("runtime-process-apply-command-positive-deny", "deny_noop"),
        },
        {
            "name": "positive_report_only_contract",
            "expected": "accepted",
            "command": base_command("runtime-process-apply-command-positive-contract"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        command = base_command(f"runtime-process-apply-command-negative-{name}")
        mutate(command)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "command": command})

    negative("wrong_route", lambda c: c.update({"target_route_id": "model_api_gateway"}))
    negative("wrong_egress_type", lambda c: c.update({"target_egress_type": "model_api"}))
    negative("missing_source_preflight", lambda c: c.update({"source_apply_preflight_blocker_path": ""}))
    negative(
        "outside_source_preflight",
        lambda c: c.update({"source_apply_preflight_blocker_path": r"C:\Temp\preflight.json"}),
    )
    negative(
        "wrong_source_preflight",
        lambda c: c.update(
            {"source_apply_preflight_blocker_path": str(REPORTS / "stale-runtime-preflight.json")}
        ),
    )
    negative(
        "wrong_guard_validation",
        lambda c: c.update({"source_guard_validation_path": str(REPORTS / "stale-runtime-guard.json")}),
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
        "wrong_expected_status",
        lambda c: c.update({"expected_source_apply_preflight_status": "ready_for_live_apply"}),
    )
    negative(
        "real_signed_decision_present",
        lambda c: c.update(
            {
                "real_signed_decision_present": True,
                "real_signed_decision_path": str(REPORTS / "real-runtime-decision.json"),
            }
        ),
    )
    negative("execute_command_type", lambda c: c.update({"command_type": "execute_runtime_process_apply"}))
    negative("execute_scope", lambda c: c.update({"allowed_scope": "runtime_process_live_apply"}))
    negative("target_request_id", lambda c: c.update({"target_request_ids": ["req-runtime-process-start-20260618"]}))
    negative("apply_command_allowed", lambda c: c.update({"apply_command_allowed": True}))
    negative("apply_allowed", lambda c: c.update({"apply_allowed": True}))
    negative("gateway_registration_allowed", lambda c: c.update({"gateway_registration_allowed": True}))
    negative("gateway_start_allowed", lambda c: c.update({"gateway_start_allowed": True}))
    negative("live_egress_allowed", lambda c: c.update({"live_egress_allowed": True}))
    negative("runtime_start_allowed", lambda c: c.update({"runtime_start_allowed": True}))
    negative("runtime_started", lambda c: c.update({"runtime_starts": 1}))
    negative("dependency_install", lambda c: c.update({"dependency_installs": 1}))
    negative("queue_mutation", lambda c: c.update({"queue_mutations": 1}))
    negative("worker_start_allowed", lambda c: c.update({"worker_start_allowed": True}))
    negative("worker_started", lambda c: c.update({"worker_starts": 1}))
    negative("service_request_assigned", lambda c: c.update({"service_requests_assigned": 1}))
    negative("service_request_updated", lambda c: c.update({"service_requests_updated": 1}))
    negative("mcp_tool_call", lambda c: c.update({"mcp_tool_calls": True}))
    negative("model_api_call", lambda c: c.update({"model_api_calls": True}))
    negative("browser_started", lambda c: c.update({"browser_sessions_started": True}))
    negative("external_side_effect_top_level", lambda c: c.update({"external_side_effects": True}))
    negative("short_rollback", lambda c: c.update({"rollback_plan": "none"}))
    negative("command_written", lambda c: c["runtime_boundary"].update({"apply_commands_written": 1}))
    negative("command_executed", lambda c: c["runtime_boundary"].update({"apply_commands_executed": 1}))
    negative("decision_applied", lambda c: c["runtime_boundary"].update({"decisions_applied": 1}))
    negative("approval_written", lambda c: c["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("gateway_registered", lambda c: c["runtime_boundary"].update({"gateway_registrations": 1}))
    negative("gateway_started", lambda c: c["runtime_boundary"].update({"gateway_starts": 1}))
    negative("live_egress_event", lambda c: c["runtime_boundary"].update({"live_egress_events": 1}))
    negative("dependency_install_boundary", lambda c: c["runtime_boundary"].update({"dependency_installs": 1}))
    negative("runtime_started_boundary", lambda c: c["runtime_boundary"].update({"runtime_starts": 1}))
    negative("queue_mutation_boundary", lambda c: c["runtime_boundary"].update({"queue_mutations": 1}))
    negative("worker_started_boundary", lambda c: c["runtime_boundary"].update({"worker_starts": 1}))
    negative(
        "service_request_updated_boundary",
        lambda c: c["runtime_boundary"].update({"service_requests_updated": 1}),
    )
    negative("mcp_tool_call_boundary", lambda c: c["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("model_api_call_boundary", lambda c: c["runtime_boundary"].update({"model_api_calls": True}))
    negative("payment_action_boundary", lambda c: c["runtime_boundary"].update({"payment_actions": True}))
    negative("external_side_effect_boundary", lambda c: c["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_command(command: dict[str, Any], schema: dict[str, Any], sources: dict[str, Any]) -> dict[str, Any]:
    errors = collect_common_contract_errors(
        schema=schema,
        command=command,
        sources=sources,
        required_fields=REQUIRED_FIELDS,
        schema_version="agent_company.runtime_process_egress_apply_command_contract.v1",
        target_route_id=TARGET_ROUTE_ID,
        target_egress_type=TARGET_EGRESS_TYPE,
        schema_false_props=SCHEMA_FALSE_PROPS,
        schema_route_error="schema_target_route_id_must_be_runtime_process_gateway",
        schema_type_error="schema_target_egress_type_must_be_runtime_start",
        route_error="target_route_id_must_match_runtime_process_gateway",
        type_error="target_egress_type_must_be_runtime_start",
        expected_paths=EXPECTED_SOURCE_PATHS,
        path_inside_root=path_inside_root,
        source_false_fields=SOURCE_FALSE_FIELDS,
        source_zero_fields=SOURCE_ZERO_FIELDS,
        command_false_fields=COMMAND_FALSE_FIELDS,
        command_zero_fields=COMMAND_ZERO_FIELDS,
        zero_boundary=ZERO_BOUNDARY,
    )

    if sources["apply_preflight_all_checks_passed"] is not True:
        errors.append("source_apply_preflight_not_passing")
    if sources["apply_preflight_status"] != "blocked_no_real_signed_decision":
        errors.append("source_apply_preflight_status_must_be_blocked_no_real_signed_decision")
    if command.get("expected_source_apply_preflight_status") != "blocked_no_real_signed_decision":
        errors.append("expected_source_apply_preflight_status_must_match")
    if sources["guard_all_checks_passed"] is not True:
        errors.append("source_guard_not_passing")
    if sources["guard_target_route_id"] != TARGET_ROUTE_ID or sources["guard_target_egress_type"] != TARGET_EGRESS_TYPE:
        errors.append("source_guard_target_mismatch")
    if sources["guard_runtime_start_allowed"] is not False or sources["guard_runtime_starts"] != 0:
        errors.append("source_guard_must_block_runtime_start")
    for key in [
        "intake_all_checks_passed",
        "gateway_all_checks_passed",
        "egress_ledger_all_checks_passed",
        "runtime_preflight_all_checks_passed",
        "runtime_guard_all_checks_passed",
    ]:
        if sources[key] is not True:
            errors.append(f"source_{key}_not_passing")

    if command.get("real_signed_decision_present") is not False:
        errors.append("real_signed_decision_present_must_be_false")
    if command.get("real_signed_decision_path") not in {"", None}:
        errors.append("real_signed_decision_path_must_be_empty")

    if len(str(command.get("rollback_plan", "")).strip()) < 20:
        errors.append("rollback_plan_too_short")

    accepted = not errors
    return {
        "command_id": command.get("command_id"),
        "command_type": command.get("command_type"),
        "target_route_id": command.get("target_route_id"),
        "target_egress_type": command.get("target_egress_type"),
        "accepted_for_contract_only": accepted,
        "rejected": not accepted,
        "errors": errors,
        "apply_command_allowed": False,
        "apply_allowed": False,
        "runtime_start_allowed": False,
        "runtime_starts": 0,
        "dependency_installs": 0,
        "queue_mutations": 0,
        "worker_start_allowed": False,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = source_summary()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        command = copy.deepcopy(fixture["command"]) if "command" in fixture else load_json(Path(fixture["path"]))
        result = validate_command(command, schema, sources)
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
        "schema_version": "agent_company.runtime_process_egress_apply_command_contract_report.v1",
        "generated_utc": generated,
        "target_route_id": TARGET_ROUTE_ID,
        "target_egress_type": TARGET_EGRESS_TYPE,
        "trace_id": TRACE_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_summary": sources,
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
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.runtime_process_egress_apply_command_contract_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
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
        "apply_command_allowed": False,
        "apply_allowed": False,
        "gateway_registration_allowed": False,
        "gateway_start_allowed": False,
        "live_egress_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation
