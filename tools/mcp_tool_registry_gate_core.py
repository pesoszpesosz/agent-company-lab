#!/usr/bin/env python3
"""Core helpers for MCP tool registry gate fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "mcp-tool-registry-gate-v1.schema.json"
PACKET = REPORTS / "mcp-tool-registry-gate-packet-v1-20260617.json"
EGRESS_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "mcp-tool-registry-gate-v1-fixtures"
REPORT_JSON = REPORTS / "mcp-tool-registry-gate-v1-20260617.json"
VALIDATION_JSON = REPORTS / "mcp-tool-registry-gate-v1-validation-20260617.json"
REPORT_MD = REPORTS / "mcp-tool-registry-gate-v1-20260617.md"

EVALUATION_UTC = "2026-06-17T19:50:00Z"
POOL_ID = "service-worker-local-runtime-adapter-pool"
IDENTITY_ID = "identity-positive-local-runtime-adapter-report-only"
SERVER_ID = "local-report-only-fixture-mcp"
TOOL_ID = "local-report-only-fixture-mcp.echo_artifact_summary"

ZERO_BOUNDARY = {
    "report_only": True,
    "mcp_servers_started": 0,
    "mcp_servers_installed": 0,
    "mcp_servers_enabled": 0,
    "mcp_tool_calls": False,
    "credentials_created": False,
    "registry_publications": 0,
    "browser_sessions_started": 0,
    "worker_starts": 0,
    "service_requests_assigned": 0,
    "public_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "external_side_effects": False,
}

REQUIRED_SERVER_FIELDS = [
    "mcp_registry_entry_id",
    "server_id",
    "server_name",
    "server_source_type",
    "source_url",
    "package_or_endpoint",
    "publisher",
    "publisher_verification",
    "version",
    "digest_or_commit",
    "license",
    "risk_tier",
    "default_status",
    "allowed_lanes",
    "allowed_agent_ids",
    "allowed_worker_pool_ids",
    "allowed_identity_envelope_ids",
    "allowed_tools",
    "blocked_tools",
    "credential_requirements",
    "oauth_or_auth_mode",
    "network_scope",
    "data_sensitivity_ceiling",
    "write_action_capable",
    "public_action_capable",
    "payment_or_wallet_capable",
    "file_system_capable",
    "browser_capable",
    "rate_limit_scope",
    "budget_scope",
    "logging_required",
    "recording_required",
    "redaction_required",
    "review_artifact_path",
    "approval_artifact_path",
    "egress_event_required",
    "created_utc",
    "expires_utc",
    "revocation_status",
    "tool",
    "runtime_boundary",
]

REQUIRED_TOOL_FIELDS = [
    "tool_id",
    "server_id",
    "tool_name",
    "tool_description",
    "tool_input_schema_artifact_path",
    "tool_output_schema_artifact_path",
    "tool_side_effect_class",
    "allowed_input_artifact_types",
    "required_output_artifact_type",
    "requires_operator_decision",
    "requires_identity_envelope",
    "requires_egress_event",
    "requires_post_execution_evidence",
    "default_policy_verdict",
    "risk_reasons",
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
    return value.startswith(str(ROOT)) and ".." not in value


def base_entry(entry_id: str = "mcp-entry-positive-local-report-only") -> dict[str, Any]:
    return {
        "mcp_registry_entry_id": entry_id,
        "server_id": SERVER_ID,
        "server_name": "Local Report Only Fixture MCP",
        "server_source_type": "local_fixture",
        "source_url": "",
        "package_or_endpoint": "local-fixture-only",
        "publisher": "agent-company-lab",
        "publisher_verification": "local_fixture",
        "version": "2026-06-17",
        "digest_or_commit": "local-fixture-no-package",
        "license": "internal-report-only",
        "risk_tier": "local_report_only",
        "default_status": "approved_report_only",
        "allowed_lanes": ["platform_engineering"],
        "allowed_agent_ids": [POOL_ID],
        "allowed_worker_pool_ids": [POOL_ID],
        "allowed_identity_envelope_ids": [IDENTITY_ID],
        "allowed_tools": [TOOL_ID],
        "blocked_tools": ["*"],
        "credential_requirements": "none",
        "oauth_or_auth_mode": "none",
        "network_scope": "none",
        "data_sensitivity_ceiling": "local_report_only",
        "write_action_capable": False,
        "public_action_capable": False,
        "payment_or_wallet_capable": False,
        "file_system_capable": False,
        "browser_capable": False,
        "rate_limit_scope": "local_only",
        "budget_scope": "zero_or_not_applicable",
        "logging_required": True,
        "recording_required": True,
        "redaction_required": True,
        "review_artifact_path": str(PACKET),
        "approval_artifact_path": "",
        "egress_event_required": True,
        "created_utc": "2026-06-17T19:48:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "revocation_status": "active",
        "tool": {
            "tool_id": TOOL_ID,
            "server_id": SERVER_ID,
            "tool_name": "echo_artifact_summary",
            "tool_description": "Local fixture for validating registry fields; no server is started and no tool is called.",
            "tool_input_schema_artifact_path": str(SCHEMA_PATH),
            "tool_output_schema_artifact_path": str(SCHEMA_PATH),
            "tool_side_effect_class": "read_only",
            "allowed_input_artifact_types": ["local_report_json"],
            "required_output_artifact_type": "local_report_json",
            "requires_operator_decision": True,
            "requires_identity_envelope": True,
            "requires_egress_event": True,
            "requires_post_execution_evidence": True,
            "default_policy_verdict": "allow_report_only_preflight",
            "risk_reasons": ["local_fixture_only", "no_server_start", "no_tool_call"],
        },
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [{"name": "positive_local_report_only_registry_entry", "expected": "accepted", "entry": base_entry()}]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        entry = base_entry(f"mcp-entry-negative-{name}")
        mutate(entry)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "entry": entry})

    negative("unknown_server", lambda e: e.update({"server_id": "unknown-public-server"}))
    negative("unknown_tool", lambda e: e["tool"].update({"tool_id": "unknown.tool"}))
    negative("disabled_server_call", lambda e: e.update({"default_status": "disabled"}))
    negative("revoked_server_call", lambda e: e.update({"revocation_status": "revoked"}))
    negative("implicit_credentials", lambda e: e.update({"credential_requirements": "env:token"}))
    negative("missing_identity_envelope", lambda e: e.update({"allowed_identity_envelope_ids": []}))
    negative("identity_scope_mismatch", lambda e: e.update({"allowed_identity_envelope_ids": ["identity-other"]}))
    negative("missing_egress_event", lambda e: e.update({"egress_event_required": False}))
    negative("missing_operator_decision", lambda e: e["tool"].update({"requires_operator_decision": False}))
    negative("write_tool_as_read_only", lambda e: e["tool"].update({"tool_side_effect_class": "external_write"}))
    negative("public_action_without_cro", lambda e: e.update({"public_action_capable": True}))
    negative("wallet_payment_tool_non_deny", lambda e: e.update({"payment_or_wallet_capable": True}))
    negative("missing_schema_artifacts", lambda e: e["tool"].update({"tool_input_schema_artifact_path": ""}))
    negative("missing_output_artifact", lambda e: e["tool"].update({"tool_output_schema_artifact_path": ""}))
    negative("unbounded_rate_or_budget", lambda e: e.update({"rate_limit_scope": "*", "budget_scope": "*"}))
    negative("network_scope_external", lambda e: e.update({"network_scope": "https://api.github.com"}))
    negative("file_system_capable", lambda e: e.update({"file_system_capable": True}))
    negative("browser_capable", lambda e: e.update({"browser_capable": True}))
    negative("mcp_server_started", lambda e: e["runtime_boundary"].update({"mcp_servers_started": 1}))
    negative("mcp_tool_called", lambda e: e["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("registry_published", lambda e: e["runtime_boundary"].update({"registry_publications": 1}))
    return fixtures


def validate_entry(entry: dict[str, Any], schema: dict[str, Any], identity_validation: dict[str, Any], egress_validation: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    for field in REQUIRED_SERVER_FIELDS:
        if field not in entry:
            errors.append(f"missing_required_field:{field}")
    tool = entry.get("tool", {})
    if not isinstance(tool, dict):
        errors.append("tool_must_be_object")
        tool = {}
    for field in REQUIRED_TOOL_FIELDS:
        if field not in tool:
            errors.append(f"missing_tool_field:{field}")

    if schema.get("properties", {}).get("default_status", {}).get("enum", [None])[0] != "disabled":
        errors.append("schema_default_status_must_start_disabled")
    if not identity_validation.get("all_checks_passed"):
        errors.append("identity_validation_not_passing")
    if not egress_validation.get("all_checks_passed"):
        errors.append("egress_validation_not_passing")
    if egress_validation.get("live_egress_allowed") is not False:
        errors.append("egress_validation_must_not_allow_live_egress")

    created = parse_utc(str(entry.get("created_utc", "")))
    expires = parse_utc(str(entry.get("expires_utc", "")))
    if created is None:
        errors.append("created_utc_invalid")
    if expires is None:
        errors.append("expires_utc_invalid")
    if created and expires and expires <= created:
        errors.append("expires_not_after_created")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("registry_entry_expired")
    if entry.get("revocation_status") != "active":
        errors.append("registry_entry_not_active")

    if entry.get("server_id") != SERVER_ID:
        errors.append("server_id_not_registered_for_local_fixture")
    if entry.get("server_source_type") != "local_fixture":
        errors.append("server_source_type_must_be_local_fixture_for_positive_path")
    if entry.get("publisher_verification") != "local_fixture":
        errors.append("publisher_verification_must_be_local_fixture")
    if entry.get("risk_tier") != "local_report_only":
        errors.append("risk_tier_must_be_local_report_only")
    if entry.get("default_status") != "approved_report_only":
        errors.append("default_status_must_be_approved_report_only_for_positive_fixture")

    if "platform_engineering" not in entry.get("allowed_lanes", []):
        errors.append("allowed_lanes_must_include_platform_engineering")
    if POOL_ID not in entry.get("allowed_agent_ids", []):
        errors.append("allowed_agent_ids_must_include_local_pool")
    if POOL_ID not in entry.get("allowed_worker_pool_ids", []):
        errors.append("allowed_worker_pool_ids_must_include_local_pool")
    if IDENTITY_ID not in entry.get("allowed_identity_envelope_ids", []):
        errors.append("allowed_identity_envelope_ids_must_include_valid_identity")
    if TOOL_ID not in entry.get("allowed_tools", []):
        errors.append("allowed_tools_must_include_fixture_tool")

    for field in ["credential_requirements", "oauth_or_auth_mode", "network_scope"]:
        if entry.get(field) != "none":
            errors.append(f"{field}_must_be_none")
    for field in ["write_action_capable", "public_action_capable", "payment_or_wallet_capable", "file_system_capable", "browser_capable"]:
        if entry.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    if entry.get("rate_limit_scope") != "local_only":
        errors.append("rate_limit_scope_must_be_local_only")
    if entry.get("budget_scope") != "zero_or_not_applicable":
        errors.append("budget_scope_must_be_zero_or_not_applicable")
    for field in ["logging_required", "recording_required", "redaction_required", "egress_event_required"]:
        if entry.get(field) is not True:
            errors.append(f"{field}_must_be_true")

    review_path = str(entry.get("review_artifact_path", ""))
    if not review_path:
        errors.append("review_artifact_path_missing")
    elif not Path(review_path).exists():
        errors.append("review_artifact_path_not_found")

    if tool.get("server_id") != entry.get("server_id"):
        errors.append("tool_server_id_must_match_registry_server")
    if tool.get("tool_id") not in entry.get("allowed_tools", []):
        errors.append("tool_id_must_be_allowlisted")
    if tool.get("tool_side_effect_class") != "read_only":
        errors.append("tool_side_effect_class_must_be_read_only")
    for field in ["requires_operator_decision", "requires_identity_envelope", "requires_egress_event", "requires_post_execution_evidence"]:
        if tool.get(field) is not True:
            errors.append(f"tool_{field}_must_be_true")
    if tool.get("default_policy_verdict") != "allow_report_only_preflight":
        errors.append("tool_default_policy_verdict_must_be_allow_report_only_preflight")
    for field in ["tool_input_schema_artifact_path", "tool_output_schema_artifact_path"]:
        path = str(tool.get(field, ""))
        if not path:
            errors.append(f"{field}_missing")
        elif not path_inside_root(path):
            errors.append(f"{field}_must_stay_inside_lab")

    boundary = entry.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    accepted = not errors
    return {
        "mcp_registry_entry_id": entry.get("mcp_registry_entry_id"),
        "accepted_for_local_report_only_registry": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], identity_validation: dict[str, Any], egress_validation: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        entry = copy.deepcopy(fixture["entry"]) if "entry" in fixture else load_json(Path(fixture["path"]))
        result = validate_entry(entry, schema, identity_validation, egress_validation)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_local_report_only_registry"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_local_report_only_registry"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.mcp_tool_registry_gate_validator_report.v1",
        "generated_utc": generated,
        "packet_path": str(PACKET),
        "packet_sha256": sha256_path(PACKET),
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "egress_validation_path": str(EGRESS_VALIDATION),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "positive_fixture": {
            "fixture_id": "local-report-only-fixture-mcp",
            "expected_result": "pass_local_report_only_registry_entry",
        },
        "results": results,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Promote identity, egress, and MCP validators into activation preflight before worker registration candidates.",
    }
    validation = {
        "schema_version": "agent_company.mcp_tool_registry_gate_validation.v1",
        "generated_utc": generated,
        "validator_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "mcp_server_enable_allowed": False,
        "mcp_tool_call_allowed": False,
        "mcp_servers_started": 0,
        "mcp_servers_installed": 0,
        "mcp_servers_enabled": 0,
        "mcp_tool_calls": False,
        "credentials_created": False,
        "registry_publications": 0,
        "browser_sessions_started": 0,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "public_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "external_side_effects": False,
        "failures": failures,
    }
    return report, validation


