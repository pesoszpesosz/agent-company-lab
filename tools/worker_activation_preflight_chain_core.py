#!/usr/bin/env python3
"""Validate the local worker activation preflight chain without enabling workers."""

from __future__ import annotations

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
SCHEMA_PATH = ARCH / "worker-activation-preflight-chain-v1.schema.json"
IDENTITY_VALIDATION = REPORTS / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
EGRESS_VALIDATION = REPORTS / "agent-egress-event-ledger-v1-validation-20260617.json"
MCP_VALIDATION = REPORTS / "mcp-tool-registry-gate-v1-validation-20260617.json"
ACTIVATION_PREFLIGHT = REPORTS / "local-runtime-adapter-pool-activation-preflight-v1-20260617.json"
FIXTURE_DIR = REPORTS / "worker-activation-preflight-chain-v1-fixtures"
REPORT_JSON = REPORTS / "worker-activation-preflight-chain-v1-20260617.json"
VALIDATION_JSON = REPORTS / "worker-activation-preflight-chain-v1-validation-20260617.json"
REPORT_MD = REPORTS / "worker-activation-preflight-chain-v1-20260617.md"

WORKER_POOL_ID = "service-worker-local-runtime-adapter-pool"

ZERO_BOUNDARY = {
    "report_only": True,
    "worker_pools_registered": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "mcp_servers_started": 0,
    "mcp_tool_calls": False,
    "browser_sessions_started": 0,
    "model_api_calls": False,
    "credentials_created": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "external_side_effects": False,
}
NEXT_ACTION = (
    "Use this chain as the pre-registration blocker; build a runtime-start preflight only "
    "after a signed operator decision route exists."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return value.startswith(str(ROOT)) and ".." not in value


def base_chain(chain_id: str = "chain-positive-local-runtime-preflight") -> dict[str, Any]:
    return {
        "chain_id": chain_id,
        "worker_pool_id": WORKER_POOL_ID,
        "lane_id": "platform_engineering",
        "identity_validation_path": str(IDENTITY_VALIDATION),
        "egress_validation_path": str(EGRESS_VALIDATION),
        "mcp_registry_validation_path": str(MCP_VALIDATION),
        "activation_preflight_path": str(ACTIVATION_PREFLIGHT),
        "operator_decision_status": "report_only",
        "chain_verdict": "preflight_passed_registration_blocked",
        "registration_allowed": False,
        "worker_start_allowed": False,
        "mcp_tool_call_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_preflight_passed_registration_blocked",
            "expected": "accepted",
            "entry": base_chain(),
        }
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        entry = base_chain(f"chain-negative-{name}")
        mutate(entry)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "entry": entry})

    negative("missing_identity_validator", lambda e: e.update({"identity_validation_path": ""}))
    negative("missing_egress_validator", lambda e: e.update({"egress_validation_path": ""}))
    negative("missing_mcp_registry_validator", lambda e: e.update({"mcp_registry_validation_path": ""}))
    negative("signed_approval_claimed", lambda e: e.update({"operator_decision_status": "signed_approved"}))
    negative(
        "registration_allowed",
        lambda e: e.update(
            {"registration_allowed": True, "chain_verdict": "approved_registration_candidate"}
        ),
    )
    negative("worker_start_allowed", lambda e: e.update({"worker_start_allowed": True}))
    negative("mcp_tool_call_allowed", lambda e: e.update({"mcp_tool_call_allowed": True}))
    negative("worker_registered_side_effect", lambda e: e["runtime_boundary"].update({"worker_pools_registered": 1}))
    negative(
        "service_request_assigned_side_effect",
        lambda e: e["runtime_boundary"].update({"service_requests_assigned": 1}),
    )
    negative("external_side_effect", lambda e: e["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validation_summary(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "all_checks_passed": False}
    data = load_json(path)
    return {
        "path": str(path),
        "exists": True,
        "all_checks_passed": bool(data.get("all_checks_passed")),
        "accepted_count": data.get("accepted_count"),
        "rejected_count": data.get("rejected_count"),
        "failure_count": data.get("failure_count"),
    }


def validate_chain(
    entry: dict[str, Any],
    schema: dict[str, Any],
    composed: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []

    if schema.get("properties", {}).get("chain_verdict", {}).get("enum", [None])[0] != "blocked_missing_validator":
        errors.append("schema_chain_verdict_must_start_blocked_missing_validator")
    if entry.get("worker_pool_id") != WORKER_POOL_ID:
        errors.append("worker_pool_id_must_match_local_runtime_adapter_pool")
    if entry.get("lane_id") != "platform_engineering":
        errors.append("lane_id_must_be_platform_engineering")
    if entry.get("operator_decision_status") != "report_only":
        errors.append("operator_decision_must_remain_report_only")
    if entry.get("chain_verdict") != "preflight_passed_registration_blocked":
        errors.append("chain_verdict_must_block_registration")

    for key in [
        "identity_validation_path",
        "egress_validation_path",
        "mcp_registry_validation_path",
        "activation_preflight_path",
    ]:
        path = str(entry.get(key, ""))
        if not path:
            errors.append(f"{key}_missing")
        elif not path_inside_root(path):
            errors.append(f"{key}_must_stay_inside_lab")
        elif not Path(path).exists():
            errors.append(f"{key}_not_found")

    for key, summary in composed.items():
        if not summary.get("exists"):
            errors.append(f"{key}_validation_missing")
        if not summary.get("all_checks_passed"):
            errors.append(f"{key}_validation_not_passing")
        if summary.get("accepted_count") != 1:
            errors.append(f"{key}_accepted_count_must_be_1")

    if entry.get("registration_allowed") is not False:
        errors.append("registration_allowed_must_be_false")
    if entry.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")
    if entry.get("mcp_tool_call_allowed") is not False:
        errors.append("mcp_tool_call_allowed_must_be_false")

    errors.extend(collect_runtime_boundary_errors(entry, ZERO_BOUNDARY))

    accepted = not errors
    return {
        "chain_id": entry.get("chain_id"),
        "accepted_for_activation_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "registration_allowed": False,
        "worker_start_allowed": False,
        "mcp_tool_call_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(
    schema: dict[str, Any],
    fixtures: list[dict[str, Any]],
    *,
    composed: dict[str, dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    composed = copy.deepcopy(composed) if composed is not None else {
        "identity": validation_summary(IDENTITY_VALIDATION),
        "egress": validation_summary(EGRESS_VALIDATION),
        "mcp_registry": validation_summary(MCP_VALIDATION),
    }
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        entry = (
            copy.deepcopy(fixture["entry"])
            if "entry" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_chain(entry, schema, composed)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_activation_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        fixture_summary = {key: value for key, value in fixture.items() if key != "entry"}
        results.append({**fixture_summary, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_activation_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.worker_activation_preflight_chain_report.v1",
        "generated_utc": generated,
        "worker_pool_id": WORKER_POOL_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "activation_preflight_path": str(ACTIVATION_PREFLIGHT),
        "composed_validators": composed,
        "chain_verdict": "preflight_passed_registration_blocked",
        "registration_allowed": False,
        "worker_start_allowed": False,
        "mcp_tool_call_allowed": False,
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.worker_activation_preflight_chain_validation.v1",
        "generated_utc": generated,
        "worker_pool_id": WORKER_POOL_ID,
        "validator_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "chain_verdict": "preflight_passed_registration_blocked",
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "registration_allowed": False,
        "worker_start_allowed": False,
        "mcp_tool_call_allowed": False,
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


