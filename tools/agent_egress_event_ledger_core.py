#!/usr/bin/env python3
"""Core helpers for agent egress event ledger fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from runtime_boundary_shared_core import collect_runtime_boundary_errors


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "agent-egress-event-ledger-v1.schema.json"
PACKET = REPORTS / "agent-egress-event-ledger-packet-v1-20260617.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
IDENTITY_REPORT = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-20260617.json"
OPERATOR_DECISION = REPORTS / "worker-pool-operator-decision-packet-v1-20260617.json"
FIXTURE_DIR = REPORTS / "agent-egress-event-ledger-v1-fixtures"
REPORT_JSON = REPORTS / "agent-egress-event-ledger-v1-20260617.json"
VALIDATION_JSON = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
REPORT_MD = REPORTS / "agent-egress-event-ledger-v1-20260617.md"

EVALUATION_UTC = "2026-06-17T19:45:00Z"
EGRESS_SCHEMA_VERSION = "agent_company.agent_egress_event_ledger.v1"
POOL_ID = "service-worker-local-runtime-adapter-pool"

ZERO_BOUNDARY = {
    "report_only": True,
    "gateway_started": False,
    "gateway_installed": False,
    "api_keys_created": False,
    "live_egress_events_recorded": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "browser_sessions_started": 0,
    "worker_pools_registered": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "credential_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "external_side_effects": False,
}

REQUIRED_FIELDS = [
    "egress_event_id",
    "egress_schema_version",
    "created_utc",
    "expires_utc",
    "request_id",
    "task_id",
    "lane_id",
    "agent_id",
    "worker_pool_id",
    "identity_envelope_id",
    "identity_envelope_artifact_path",
    "operator_decision_id",
    "operator_decision_artifact_path",
    "service_request_artifact_path",
    "egress_type",
    "target",
    "tool_or_model",
    "input_artifact_path",
    "output_artifact_path",
    "credential_scope",
    "browser_scope",
    "mcp_scope",
    "model_api_scope",
    "wallet_scope",
    "payment_scope",
    "public_action_scope",
    "budget_scope",
    "rate_limit_scope",
    "policy_verdict",
    "policy_reasons",
    "policy_evaluator",
    "redaction_required",
    "recording_required",
    "rollback_or_teardown_artifact_path",
    "runtime_boundary",
    "external_side_effects_expected",
    "post_execution_evidence_required",
    "revocation_status",
]

ALLOWED_EGRESS_TYPES = {
    "model_api",
    "mcp_tool",
    "direct_api",
    "browser_read_only",
    "browser_signed_in",
    "computer_use",
    "public_submission",
    "wallet_payment",
    "account_registration",
    "credential_access",
    "github_public_action",
    "marketplace_action",
    "outreach_delivery",
    "agent_to_agent",
}

REPORT_ONLY_TYPES = {"agent_to_agent"}
EXTERNAL_TYPES = ALLOWED_EGRESS_TYPES - REPORT_ONLY_TYPES


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


def identity_fixture_path() -> Path:
    return (
        REPORTS
        / "local-runtime-adapter-pool-identity-envelope-v1-fixtures"
        / "positive_report_only_identity_candidate.json"
    )


def base_event(event_id: str = "egress-positive-local-report-only-preflight") -> dict[str, Any]:
    return {
        "egress_event_id": event_id,
        "egress_schema_version": EGRESS_SCHEMA_VERSION,
        "created_utc": "2026-06-17T19:42:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "request_id": "req-local-runtime-adapter-report-only-preflight",
        "task_id": "task-local-runtime-adapter-pool-identity-envelope-validator-v1-20260617",
        "lane_id": "platform_engineering",
        "agent_id": POOL_ID,
        "worker_pool_id": POOL_ID,
        "identity_envelope_id": "identity-positive-local-runtime-adapter-report-only",
        "identity_envelope_artifact_path": str(identity_fixture_path()),
        "operator_decision_id": "operator-decision-packet-report-only-reference",
        "operator_decision_artifact_path": str(OPERATOR_DECISION),
        "service_request_artifact_path": "",
        "egress_type": "agent_to_agent",
        "target": "local_agent_company_report_artifact",
        "tool_or_model": "none",
        "input_artifact_path": str(IDENTITY_VALIDATION),
        "output_artifact_path": str(REPORTS / "agent-egress-event-ledger-v1-20260617.json"),
        "credential_scope": "none",
        "browser_scope": "none",
        "mcp_scope": "none",
        "model_api_scope": "none",
        "wallet_scope": "none",
        "payment_scope": "none",
        "public_action_scope": "none",
        "budget_scope": "zero_or_not_applicable",
        "rate_limit_scope": "local_only",
        "policy_verdict": "allow_report_only_preflight",
        "policy_reasons": [
            "identity_validator_passed",
            "local_report_only",
            "no_live_egress",
            "zero_external_side_effects",
        ],
        "policy_evaluator": "validate_agent_egress_event_ledger.py",
        "redaction_required": True,
        "recording_required": True,
        "rollback_or_teardown_artifact_path": str(
            REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "external_side_effects_expected": False,
        "post_execution_evidence_required": True,
        "revocation_status": "active",
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [{"name": "positive_report_only_preflight_event", "expected": "accepted", "event": base_event()}]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        event = base_event(f"egress-negative-{name}")
        mutate(event)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "event": event})

    negative("missing_identity_envelope", lambda e: e.update({"identity_envelope_artifact_path": ""}))
    negative("missing_operator_decision", lambda e: e.update({"operator_decision_artifact_path": ""}))
    negative("expired_egress_event", lambda e: e.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("unknown_egress_type", lambda e: e.update({"egress_type": "carrier_pigeon"}))
    negative("implicit_credentials", lambda e: e.update({"credential_scope": "implicit_env"}))
    negative("implicit_budget", lambda e: e.update({"budget_scope": ""}))
    negative("missing_output_artifact", lambda e: e.update({"output_artifact_path": ""}))
    negative(
        "scope_broadened_from_identity",
        lambda e: e.update({"egress_type": "direct_api", "target": "https://api.example.com"}),
    )
    negative("scope_broadened_from_decision", lambda e: e.update({"policy_verdict": "allow_after_operator_approval"}))
    negative(
        "signed_in_browser_as_read_only",
        lambda e: e.update({"egress_type": "browser_signed_in", "browser_scope": "signed_in_session"}),
    )
    negative(
        "public_action_allowed_without_cro",
        lambda e: e.update({"egress_type": "public_submission", "public_action_scope": "submit"}),
    )
    negative(
        "wallet_payment_non_deny",
        lambda e: e.update({"egress_type": "wallet_payment", "wallet_scope": "send", "payment_scope": "token"}),
    )
    negative(
        "model_api_no_provider_cost",
        lambda e: e.update({"egress_type": "model_api", "model_api_scope": "provider:any"}),
    )
    negative(
        "mcp_server_not_registered",
        lambda e: e.update({"egress_type": "mcp_tool", "mcp_scope": "github/issues.list"}),
    )
    negative("external_side_effects_report_only", lambda e: e.update({"external_side_effects_expected": True}))
    negative("gateway_started", lambda e: e["runtime_boundary"].update({"gateway_started": True}))
    negative("api_key_created", lambda e: e["runtime_boundary"].update({"api_keys_created": True}))
    negative("model_call_recorded", lambda e: e["runtime_boundary"].update({"model_api_calls": True}))
    negative("mcp_call_recorded", lambda e: e["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("browser_started", lambda e: e["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("worker_started", lambda e: e["runtime_boundary"].update({"worker_starts": 1}))
    negative("service_request_assigned", lambda e: e["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("revoked_event", lambda e: e.update({"revocation_status": "revoked"}))
    return fixtures


def validate_event(
    event: dict[str, Any],
    schema: dict[str, Any],
    identity_validation: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    for field in REQUIRED_FIELDS:
        if field not in event:
            errors.append(f"missing_required_field:{field}")

    if event.get("egress_schema_version") != EGRESS_SCHEMA_VERSION:
        errors.append("egress_schema_version_mismatch")
    if event.get("lane_id") != "platform_engineering":
        errors.append("lane_id_mismatch")
    if event.get("worker_pool_id") != POOL_ID:
        errors.append("worker_pool_id_mismatch")
    if event.get("agent_id") != POOL_ID:
        errors.append("agent_id_mismatch")

    created = parse_utc(str(event.get("created_utc", "")))
    expires = parse_utc(str(event.get("expires_utc", "")))
    if created is None:
        errors.append("created_utc_invalid")
    if expires is None:
        errors.append("expires_utc_invalid")
    if created and expires and expires <= created:
        errors.append("expires_not_after_created")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("egress_event_expired")

    if event.get("revocation_status") != "active":
        errors.append("egress_event_not_active")

    egress_type = str(event.get("egress_type", ""))
    if egress_type not in ALLOWED_EGRESS_TYPES:
        errors.append("unknown_egress_type")
    if egress_type in EXTERNAL_TYPES:
        errors.append(f"egress_type_requires_future_gate:{egress_type}")

    identity_path = str(event.get("identity_envelope_artifact_path", ""))
    if not identity_path:
        errors.append("identity_envelope_artifact_path_missing")
    elif not Path(identity_path).exists():
        errors.append("identity_envelope_artifact_path_not_found")
    if not identity_validation.get("all_checks_passed"):
        errors.append("identity_validator_not_passing")
    if identity_validation.get("accepted_count") != 1:
        errors.append("identity_validator_expected_one_positive_candidate")

    operator_path = str(event.get("operator_decision_artifact_path", ""))
    if not operator_path:
        errors.append("operator_decision_artifact_path_missing")
    elif not Path(operator_path).exists():
        errors.append("operator_decision_artifact_path_not_found")

    for field in [
        "credential_scope",
        "browser_scope",
        "mcp_scope",
        "model_api_scope",
        "wallet_scope",
        "payment_scope",
        "public_action_scope",
    ]:
        if event.get(field) != "none":
            errors.append(f"{field}_must_be_none")

    if event.get("budget_scope") not in {"zero_or_not_applicable", "none"}:
        errors.append("budget_scope_must_be_zero_or_not_applicable")
    if event.get("rate_limit_scope") != "local_only":
        errors.append("rate_limit_scope_must_be_local_only")

    verdict = event.get("policy_verdict")
    if verdict == "allow_report_only_preflight":
        if egress_type not in REPORT_ONLY_TYPES:
            errors.append("allow_report_only_preflight_requires_report_only_egress_type")
    elif verdict in {"allow_after_operator_approval", "pause_for_review"}:
        errors.append(f"policy_verdict_not_allowed_in_local_validator:{verdict}")
    elif verdict != "deny":
        errors.append("policy_verdict_invalid")

    if not isinstance(event.get("policy_reasons"), list) or not event.get("policy_reasons"):
        errors.append("policy_reasons_required")
    if not str(event.get("policy_evaluator", "")).strip():
        errors.append("policy_evaluator_required")

    for path_field in ["input_artifact_path", "output_artifact_path", "rollback_or_teardown_artifact_path"]:
        value = str(event.get(path_field, ""))
        if not value:
            errors.append(f"{path_field}_missing")
        elif not path_inside_root(value):
            errors.append(f"{path_field}_must_stay_inside_lab")

    for field in ["redaction_required", "recording_required", "post_execution_evidence_required"]:
        if event.get(field) is not True:
            errors.append(f"{field}_must_be_true")
    if event.get("external_side_effects_expected") is not False:
        errors.append("external_side_effects_expected_must_be_false")

    errors.extend(collect_runtime_boundary_errors(event, ZERO_BOUNDARY))

    schema_default = schema.get("properties", {}).get("policy_verdict", {}).get("enum", [None])[0]
    if schema_default != "deny":
        errors.append("schema_policy_verdict_must_start_with_deny")

    accepted = not errors
    return {
        "egress_event_id": event.get("egress_event_id"),
        "accepted_for_local_report_only_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "live_egress_allowed": False,
        "registration_allowed": False,
        "assignment_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(
    schema: dict[str, Any],
    identity_validation: dict[str, Any],
    fixtures: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        event = copy.deepcopy(fixture["event"]) if "event" in fixture else load_json(Path(fixture["path"]))
        result = validate_event(event, schema, identity_validation)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_local_report_only_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_local_report_only_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.agent_egress_event_ledger_validator_report.v1",
        "generated_utc": generated,
        "packet_path": str(PACKET),
        "packet_sha256": sha256_path(PACKET),
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "identity_report_path": str(IDENTITY_REPORT),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "positive_fixture": {
            "fixture_id": "local_runtime_adapter_dry_run_evidence",
            "expected_result": "pass_report_only_preflight_event",
        },
        "results": results,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "live_egress_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": (
            "Promote identity and egress validators into activation preflight; build MCP registry validator next "
            "before any tool access."
        ),
    }
    validation = {
        "schema_version": "agent_company.agent_egress_event_ledger_validation.v1",
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
        "live_egress_allowed": False,
        "gateway_started": False,
        "gateway_installed": False,
        "api_keys_created": False,
        "live_egress_events_recorded": 0,
        "model_api_calls": False,
        "mcp_tool_calls": False,
        "browser_sessions_started": 0,
        "worker_pools_registered": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "credential_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "external_side_effects": False,
        "failures": failures,
    }
    return report, validation


