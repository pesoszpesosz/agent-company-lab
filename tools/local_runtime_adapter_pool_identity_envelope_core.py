#!/usr/bin/env python3
"""Core helpers for local runtime adapter pool identity envelopes."""

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
SCHEMA_PATH = ARCH / "local-runtime-adapter-pool-identity-envelope-v1.schema.json"
CONTRACT_DESIGN = REPORTS / "local-runtime-adapter-pool-identity-envelope-contract-v1-20260617.json"
FIXTURE_DIR = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-fixtures"
REPORT_JSON = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-20260617.json"
VALIDATION_JSON = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
REPORT_MD = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-20260617.md"

EVALUATION_UTC = "2026-06-17T19:40:00Z"
IDENTITY_SCHEMA_VERSION = "agent_company.local_runtime_adapter_pool_identity_envelope.v1"
POOL_ID = "service-worker-local-runtime-adapter-pool"
ROLE_ID = "observability_worker"
DEPARTMENT_ID = "service_worker_observability"
RUNTIME_MODE = "report_only_local_dry_run"

ZERO_BOUNDARY = {
    "report_only": True,
    "identity_system_installed": False,
    "credentials_created": False,
    "spiffe_ids_issued": False,
    "svids_issued": False,
    "worker_pools_registered": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "network_calls_by_worker": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "external_side_effects": False,
}

REQUIRED_FIELDS = [
    "identity_envelope_id",
    "identity_schema_version",
    "created_utc",
    "expires_utc",
    "revocation_status",
    "revocation_reason",
    "worker_pool_id",
    "agent_id",
    "role_id",
    "department_id",
    "lane_ids",
    "owner_agent_id",
    "owner_thread_id",
    "principal_mode",
    "delegation_chain",
    "operator_decision_artifact_path",
    "activation_contract_artifact_path",
    "allowed_service_request_types",
    "allowed_runtime_modes",
    "allowed_input_artifact_paths",
    "allowed_output_artifact_roots",
    "allowed_egress_types",
    "allowed_targets",
    "allowed_mcp_servers",
    "allowed_mcp_tools",
    "credential_policy",
    "browser_session_policy",
    "model_api_policy",
    "mcp_policy",
    "wallet_policy",
    "payment_policy",
    "account_policy",
    "public_action_policy",
    "filesystem_policy",
    "network_policy",
    "budget_scope",
    "rate_limit_scope",
    "data_sensitivity_ceiling",
    "recording_required",
    "redaction_required",
    "trace_event_required",
    "post_run_evidence_required",
    "runtime_boundary",
    "policy_verifier",
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


def base_envelope(envelope_id: str = "identity-positive-local-runtime-adapter-report-only") -> dict[str, Any]:
    return {
        "identity_envelope_id": envelope_id,
        "identity_schema_version": IDENTITY_SCHEMA_VERSION,
        "created_utc": "2026-06-17T19:35:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "revocation_status": "active",
        "revocation_reason": "",
        "worker_pool_id": POOL_ID,
        "agent_id": POOL_ID,
        "role_id": ROLE_ID,
        "department_id": DEPARTMENT_ID,
        "lane_ids": ["platform_engineering"],
        "owner_agent_id": "recovered-profitable-edge-infra",
        "owner_thread_id": "019ebbda-2002-7361-8597-03625189c3ff",
        "principal_mode": "non_human_worker_pool_candidate",
        "delegation_chain": ["human_operator", "recovered-profitable-edge-infra", POOL_ID],
        "operator_decision_artifact_path": str(REPORTS / "worker-pool-operator-decision-packet-v1-20260617.json"),
        "activation_contract_artifact_path": str(REPORTS / "local-runtime-adapter-pool-activation-contract-design-v1-20260617.json"),
        "allowed_service_request_types": ["lifecycle_test", "model_api_execution"],
        "allowed_runtime_modes": [RUNTIME_MODE],
        "allowed_input_artifact_paths": [
            str(REPORTS / "worker-activation-runway-v1-20260617.json"),
            str(REPORTS / "local-runtime-adapter-pool-activation-preflight-v1-20260617.json"),
        ],
        "allowed_output_artifact_roots": [str(REPORTS)],
        "allowed_egress_types": [],
        "allowed_targets": [],
        "allowed_mcp_servers": [],
        "allowed_mcp_tools": [],
        "credential_policy": "deny",
        "browser_session_policy": "deny",
        "model_api_policy": "deny_until_separate_costed_provider_approval",
        "mcp_policy": "deny_until_registry_gate_and_egress_event",
        "wallet_policy": "deny",
        "payment_policy": "deny",
        "account_policy": "deny",
        "public_action_policy": "deny",
        "filesystem_policy": {
            "read_scope": "declared_input_artifact_paths_only",
            "write_scope": "declared_output_artifact_roots_only",
            "unbounded_writes": False,
        },
        "network_policy": "deny",
        "budget_scope": "zero_or_not_applicable",
        "rate_limit_scope": "local_only",
        "data_sensitivity_ceiling": "local_report_only",
        "recording_required": True,
        "redaction_required": True,
        "trace_event_required": True,
        "post_run_evidence_required": True,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "policy_verifier": "validate_local_runtime_adapter_pool_identity_envelope.py",
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_report_only_identity_candidate",
            "expected": "accepted",
            "envelope": base_envelope(),
        }
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        envelope = base_envelope(f"identity-negative-{name}")
        mutate(envelope)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "envelope": envelope})

    negative("wrong_worker_pool_id", lambda e: e.update({"worker_pool_id": "service-worker-browser-read-only-pool"}))
    negative("wrong_role_id", lambda e: e.update({"role_id": "browser_action_worker"}))
    negative("wrong_department_id", lambda e: e.update({"department_id": "service_worker_browser_operations"}))
    negative("missing_operator_decision_artifact", lambda e: e.update({"operator_decision_artifact_path": ""}))
    negative("operator_decision_claims_registration_approval", lambda e: e.update({"operator_decision_artifact_path": str(REPORTS / "fake-registration-approval.json")}))
    negative("expired_identity_envelope", lambda e: e.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("revoked_identity_envelope", lambda e: e.update({"revocation_status": "revoked", "revocation_reason": "fixture revocation"}))
    negative("allowed_runtime_mode_live", lambda e: e.update({"allowed_runtime_modes": [RUNTIME_MODE, "live_worker_start"]}))
    negative("allowed_egress_type_browser_read_only", lambda e: e.update({"allowed_egress_types": ["browser_read_only"]}))
    negative("allowed_egress_type_model_api", lambda e: e.update({"allowed_egress_types": ["model_api"]}))
    negative("allowed_mcp_server_non_empty", lambda e: e.update({"allowed_mcp_servers": ["github-mcp-server-read-only-subset"]}))
    negative("allowed_mcp_tool_non_empty", lambda e: e.update({"allowed_mcp_tools": ["issues.list"]}))
    negative("credential_policy_allow", lambda e: e.update({"credential_policy": "allow"}))
    negative("browser_session_policy_allow", lambda e: e.update({"browser_session_policy": "allow"}))
    negative("network_policy_allow", lambda e: e.update({"network_policy": "allow"}))
    negative("wallet_policy_allow", lambda e: e.update({"wallet_policy": "allow"}))
    negative("payment_policy_allow", lambda e: e.update({"payment_policy": "allow"}))
    negative("account_policy_allow", lambda e: e.update({"account_policy": "allow"}))
    negative("public_action_policy_allow", lambda e: e.update({"public_action_policy": "allow"}))
    negative("filesystem_writes_unbounded", lambda e: e["filesystem_policy"].update({"unbounded_writes": True, "write_scope": "*"}))
    negative("trace_event_required_false", lambda e: e.update({"trace_event_required": False}))
    negative("post_run_evidence_required_false", lambda e: e.update({"post_run_evidence_required": False}))
    negative("external_side_effects_true", lambda e: e["runtime_boundary"].update({"external_side_effects": True}))
    negative("service_request_assignment_nonzero", lambda e: e["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("worker_start_nonzero", lambda e: e["runtime_boundary"].update({"worker_starts": 1}))
    return fixtures


def path_inside_root(value: str) -> bool:
    return value.startswith(str(ROOT)) and ".." not in value


def validate_envelope(envelope: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    for field in REQUIRED_FIELDS:
        if field not in envelope:
            errors.append(f"missing_required_field:{field}")

    if envelope.get("identity_schema_version") != IDENTITY_SCHEMA_VERSION:
        errors.append("identity_schema_version_mismatch")
    if envelope.get("worker_pool_id") != POOL_ID:
        errors.append("worker_pool_id_mismatch")
    if envelope.get("role_id") != ROLE_ID:
        errors.append("role_id_mismatch")
    if envelope.get("department_id") != DEPARTMENT_ID:
        errors.append("department_id_mismatch")
    if envelope.get("principal_mode") != "non_human_worker_pool_candidate":
        errors.append("principal_mode_mismatch")

    created = parse_utc(str(envelope.get("created_utc", "")))
    expires = parse_utc(str(envelope.get("expires_utc", "")))
    if created is None:
        errors.append("created_utc_invalid")
    if expires is None:
        errors.append("expires_utc_invalid")
    if created and expires and expires <= created:
        errors.append("expires_not_after_created")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("identity_envelope_expired")

    if envelope.get("revocation_status") != "active":
        errors.append("identity_envelope_not_active")

    operator_path = str(envelope.get("operator_decision_artifact_path", ""))
    if not operator_path:
        errors.append("operator_decision_artifact_path_missing")
    elif "registration-approval" in operator_path or "register-approval" in operator_path:
        errors.append("operator_decision_must_not_claim_registration_approval")
    elif not Path(operator_path).exists():
        errors.append("operator_decision_artifact_path_not_found")

    activation_path = str(envelope.get("activation_contract_artifact_path", ""))
    if not activation_path:
        errors.append("activation_contract_artifact_path_missing")
    elif not Path(activation_path).exists():
        errors.append("activation_contract_artifact_path_not_found")

    lane_ids = envelope.get("lane_ids", [])
    if not isinstance(lane_ids, list) or "platform_engineering" not in lane_ids:
        errors.append("lane_ids_must_include_platform_engineering")

    service_types = envelope.get("allowed_service_request_types", [])
    if not isinstance(service_types, list):
        errors.append("allowed_service_request_types_must_be_list")
        service_types = []
    allowed_service_types = {"lifecycle_test", "model_api_execution"}
    excess_service_types = sorted(set(service_types) - allowed_service_types)
    if excess_service_types:
        errors.append(f"allowed_service_request_types_exceed_scope:{','.join(excess_service_types)}")

    runtime_modes = envelope.get("allowed_runtime_modes", [])
    if runtime_modes != [RUNTIME_MODE]:
        errors.append("allowed_runtime_modes_must_be_report_only_local_dry_run_only")

    empty_scopes = [
        "allowed_egress_types",
        "allowed_targets",
        "allowed_mcp_servers",
        "allowed_mcp_tools",
    ]
    for field in empty_scopes:
        value = envelope.get(field, [])
        if value:
            errors.append(f"{field}_must_be_empty")

    deny_fields = [
        "credential_policy",
        "browser_session_policy",
        "wallet_policy",
        "payment_policy",
        "account_policy",
        "public_action_policy",
        "network_policy",
    ]
    for field in deny_fields:
        if envelope.get(field) != "deny":
            errors.append(f"{field}_must_be_deny")
    if envelope.get("model_api_policy") != "deny_until_separate_costed_provider_approval":
        errors.append("model_api_policy_must_remain_gated")
    if envelope.get("mcp_policy") != "deny_until_registry_gate_and_egress_event":
        errors.append("mcp_policy_must_remain_gated")

    filesystem_policy = envelope.get("filesystem_policy", {})
    if not isinstance(filesystem_policy, dict):
        errors.append("filesystem_policy_must_be_object")
        filesystem_policy = {}
    if filesystem_policy.get("unbounded_writes") is not False:
        errors.append("filesystem_policy_unbounded_writes_must_be_false")
    if "*" in str(filesystem_policy.get("write_scope", "")):
        errors.append("filesystem_policy_write_scope_must_not_be_wildcard")

    output_roots = envelope.get("allowed_output_artifact_roots", [])
    if not isinstance(output_roots, list) or not output_roots:
        errors.append("allowed_output_artifact_roots_required")
    else:
        for output_root in output_roots:
            if not path_inside_root(str(output_root)):
                errors.append("allowed_output_artifact_roots_must_stay_inside_lab")

    for field in ["recording_required", "redaction_required", "trace_event_required", "post_run_evidence_required"]:
        if envelope.get(field) is not True:
            errors.append(f"{field}_must_be_true")

    runtime_boundary = envelope.get("runtime_boundary", {})
    if not isinstance(runtime_boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        runtime_boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if runtime_boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    if not str(envelope.get("policy_verifier", "")).strip():
        errors.append("policy_verifier_required")

    schema_pool_const = schema.get("properties", {}).get("worker_pool_id", {}).get("const")
    if schema_pool_const != POOL_ID:
        errors.append("schema_worker_pool_const_mismatch")

    accepted = not errors
    return {
        "identity_envelope_id": envelope.get("identity_envelope_id"),
        "accepted_for_registration_candidate_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "registration_allowed": False,
        "assignment_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        envelope = copy.deepcopy(fixture["envelope"]) if "envelope" in fixture else load_json(Path(fixture["path"]))
        result = validate_envelope(envelope, schema)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_registration_candidate_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_registration_candidate_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.local_runtime_adapter_pool_identity_envelope_validator_report.v1",
        "generated_utc": generated,
        "contract_design_path": str(CONTRACT_DESIGN),
        "contract_design_sha256": sha256_path(CONTRACT_DESIGN),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "positive_fixture": {
            "fixture_id": "identity_local_runtime_adapter_report_only_candidate",
            "expected_result": "pass_identity_candidate_not_registration_approval",
        },
        "results": results,
        "registration_allowed": False,
        "assignment_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Promote this validator into the activation preflight chain, then build the egress-ledger validator; do not register pools, assign requests, start workers, or perform external actions.",
    }
    validation = {
        "schema_version": "agent_company.local_runtime_adapter_pool_identity_envelope_validation.v1",
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
        "registration_allowed": False,
        "assignment_allowed": False,
        "worker_start_allowed": False,
        "identity_system_installed": False,
        "credentials_created": False,
        "spiffe_ids_issued": False,
        "svids_issued": False,
        "worker_pools_registered": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "browser_sessions_started": 0,
        "model_api_calls": False,
        "mcp_tool_calls": False,
        "network_calls_by_worker": False,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "external_side_effects": False,
        "failures": failures,
    }
    return report, validation


