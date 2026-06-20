#!/usr/bin/env python3
"""Validate runtime-start preflight fixtures without starting any runtime process."""

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
SCHEMA_PATH = ARCH / "runtime-start-preflight-v1.schema.json"
ACTIVATION_CHAIN_VALIDATION = REPORTS / "worker-activation-preflight-chain-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "runtime-start-preflight-v1-fixtures"
REPORT_JSON = REPORTS / "runtime-start-preflight-v1-20260617.json"
VALIDATION_JSON = REPORTS / "runtime-start-preflight-v1-validation-20260617.json"
REPORT_MD = REPORTS / "runtime-start-preflight-v1-20260617.md"

WORKER_POOL_ID = "service-worker-local-runtime-adapter-pool"
TRACE_ID = "trace-runtime-start-preflight-v1-20260617"

NEXT_ACTION = (
    "Require a signed operator decision route before converting this dry-run preview "
    "into any executable runtime start."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "runtime_processes_started": 0,
    "command_previews_executed": 0,
    "worker_starts": 0,
    "worker_pools_registered": 0,
    "service_requests_assigned": 0,
    "mcp_servers_started": 0,
    "mcp_tool_calls": False,
    "browser_sessions_started": 0,
    "model_api_calls": False,
    "dependencies_installed": 0,
    "credentials_created": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "external_side_effects": False,
}

REQUIRED_COMMAND_FIELDS = [
    "mode",
    "command_kind",
    "command_string",
    "declared_read_paths",
    "declared_write_paths",
    "execution_allowed",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return value.startswith(str(ROOT)) and ".." not in value


def activation_chain_summary() -> dict[str, Any]:
    if not ACTIVATION_CHAIN_VALIDATION.exists():
        return {
            "path": str(ACTIVATION_CHAIN_VALIDATION),
            "exists": False,
            "all_checks_passed": False,
            "chain_verdict": "blocked_missing_activation_chain",
        }
    data = load_json(ACTIVATION_CHAIN_VALIDATION)
    return {
        "path": str(ACTIVATION_CHAIN_VALIDATION),
        "exists": True,
        "all_checks_passed": bool(data.get("all_checks_passed")),
        "chain_verdict": data.get("chain_verdict"),
        "registration_allowed": data.get("registration_allowed"),
        "worker_start_allowed": data.get("worker_start_allowed"),
        "worker_pool_id": data.get("worker_pool_id"),
    }


def base_preflight(preflight_id: str = "runtime-start-preflight-positive-local-preview") -> dict[str, Any]:
    return {
        "runtime_preflight_id": preflight_id,
        "worker_pool_id": WORKER_POOL_ID,
        "lane_id": "platform_engineering",
        "activation_chain_validation_path": str(ACTIVATION_CHAIN_VALIDATION),
        "operator_decision_status": "report_only_no_signed_start_authority",
        "runtime_start_verdict": "dry_run_preview_valid_start_blocked",
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "command_preview": {
            "mode": "preview_only",
            "command_kind": "local_python_report_only",
            "command_string": "python E:\\agent-company-lab\\tools\\runtime_adapter_harness.py --dry-run --no-execute",
            "declared_read_paths": [
                str(ACTIVATION_CHAIN_VALIDATION),
                str(REPORTS / "worker-activation-preflight-chain-v1-20260617.json")
            ],
            "declared_write_paths": [
                str(REPORT_JSON),
                str(VALIDATION_JSON),
                str(REPORT_MD)
            ],
            "execution_allowed": False,
        },
        "output_artifact_path": str(REPORT_JSON),
        "trace_id": TRACE_ID,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_dry_run_preview_valid_start_blocked",
            "expected": "accepted",
            "entry": base_preflight(),
        }
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        entry = base_preflight(f"runtime-start-negative-{name}")
        mutate(entry)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "entry": entry})

    negative("missing_activation_chain", lambda e: e.update({"activation_chain_validation_path": ""}))
    negative("signed_start_approval_claimed", lambda e: e.update({"operator_decision_status": "signed_start_approved"}))
    negative(
        "runtime_start_allowed",
        lambda e: e.update(
            {"runtime_start_allowed": True, "runtime_start_verdict": "approved_to_start"}
        ),
    )
    negative("worker_start_allowed", lambda e: e.update({"worker_start_allowed": True}))
    negative("command_mode_execute", lambda e: e["command_preview"].update({"mode": "execute"}))
    negative("command_execution_allowed", lambda e: e["command_preview"].update({"execution_allowed": True}))
    negative("command_preview_executed", lambda e: e["runtime_boundary"].update({"command_previews_executed": 1}))
    negative("runtime_process_started", lambda e: e["runtime_boundary"].update({"runtime_processes_started": 1}))
    negative("service_request_assigned", lambda e: e["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("mcp_tool_called", lambda e: e["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("browser_opened", lambda e: e["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("credential_created", lambda e: e["runtime_boundary"].update({"credentials_created": True}))
    negative("missing_trace_id", lambda e: e.update({"trace_id": ""}))
    negative("missing_output_artifact", lambda e: e.update({"output_artifact_path": ""}))
    negative("external_side_effect", lambda e: e["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_preflight(
    entry: dict[str, Any],
    schema: dict[str, Any],
    activation_chain: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []

    verdict_enum = schema.get("properties", {}).get("runtime_start_verdict", {}).get("enum", [None])
    if verdict_enum[0] != "blocked_missing_activation_chain":
        errors.append("schema_runtime_start_verdict_must_start_blocked_missing_activation_chain")
    if entry.get("worker_pool_id") != WORKER_POOL_ID:
        errors.append("worker_pool_id_must_match_local_runtime_adapter_pool")
    if entry.get("lane_id") != "platform_engineering":
        errors.append("lane_id_must_be_platform_engineering")
    if entry.get("operator_decision_status") != "report_only_no_signed_start_authority":
        errors.append("operator_decision_must_not_claim_signed_start_authority")
    if entry.get("runtime_start_verdict") != "dry_run_preview_valid_start_blocked":
        errors.append("runtime_start_verdict_must_block_start")
    if entry.get("runtime_start_allowed") is not False:
        errors.append("runtime_start_allowed_must_be_false")
    if entry.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")

    activation_path = str(entry.get("activation_chain_validation_path", ""))
    if not activation_path:
        errors.append("activation_chain_validation_path_missing")
    elif not path_inside_root(activation_path):
        errors.append("activation_chain_validation_path_must_stay_inside_lab")
    elif not Path(activation_path).exists():
        errors.append("activation_chain_validation_path_not_found")

    if not activation_chain.get("exists"):
        errors.append("activation_chain_missing")
    if not activation_chain.get("all_checks_passed"):
        errors.append("activation_chain_not_passing")
    if activation_chain.get("chain_verdict") != "preflight_passed_registration_blocked":
        errors.append("activation_chain_verdict_must_be_registration_blocked")
    if activation_chain.get("worker_pool_id") != WORKER_POOL_ID:
        errors.append("activation_chain_worker_pool_mismatch")
    if activation_chain.get("worker_start_allowed") is not False:
        errors.append("activation_chain_worker_start_must_be_false")

    command = entry.get("command_preview", {})
    if not isinstance(command, dict):
        errors.append("command_preview_must_be_object")
        command = {}
    for field in REQUIRED_COMMAND_FIELDS:
        if field not in command:
            errors.append(f"command_preview_missing_{field}")
    if command.get("mode") != "preview_only":
        errors.append("command_preview_mode_must_be_preview_only")
    if command.get("command_kind") != "local_python_report_only":
        errors.append("command_kind_must_be_local_python_report_only")
    if command.get("execution_allowed") is not False:
        errors.append("command_execution_allowed_must_be_false")
    command_string = str(command.get("command_string", ""))
    if " --dry-run" not in command_string or "--no-execute" not in command_string:
        errors.append("command_string_must_be_dry_run_no_execute")
    for list_field in ["declared_read_paths", "declared_write_paths"]:
        values = command.get(list_field, [])
        if not isinstance(values, list) or not values:
            errors.append(f"command_{list_field}_must_be_nonempty_list")
        else:
            for value in values:
                if not isinstance(value, str) or not path_inside_root(value):
                    errors.append(f"command_{list_field}_must_stay_inside_lab")
                    break

    output_path = str(entry.get("output_artifact_path", ""))
    if not output_path:
        errors.append("output_artifact_path_missing")
    elif not path_inside_root(output_path):
        errors.append("output_artifact_path_must_stay_inside_lab")
    if not str(entry.get("trace_id", "")):
        errors.append("trace_id_missing")

    errors.extend(collect_runtime_boundary_errors(entry, ZERO_BOUNDARY))

    accepted = not errors
    return {
        "runtime_preflight_id": entry.get("runtime_preflight_id"),
        "accepted_for_runtime_start_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    activation_chain = activation_chain_summary()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        entry = (
            copy.deepcopy(fixture["entry"])
            if "entry" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_preflight(entry, schema, activation_chain)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_runtime_start_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_runtime_start_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.runtime_start_preflight_report.v1",
        "generated_utc": generated,
        "worker_pool_id": WORKER_POOL_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "activation_chain": activation_chain,
        "runtime_start_verdict": "dry_run_preview_valid_start_blocked",
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "positive_fixture": {
            "runtime_start_allowed": False,
            "expected_result": "pass_dry_run_preview_only_start_blocked",
        },
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
        "schema_version": "agent_company.runtime_start_preflight_validation.v1",
        "generated_utc": generated,
        "worker_pool_id": WORKER_POOL_ID,
        "validator_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "runtime_start_verdict": "dry_run_preview_valid_start_blocked",
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


