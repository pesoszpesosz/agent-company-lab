#!/usr/bin/env python3
"""Validate signed runtime-start decisions without applying or executing them."""

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
SCHEMA_PATH = ARCH / "runtime-start-signed-decision-guard-v1.schema.json"
PREFLIGHT_VALIDATION = REPORTS / "runtime-start-preflight-v1-validation-20260617.json"
PREFLIGHT_REPORT = REPORTS / "runtime-start-preflight-v1-20260617.json"
FIXTURE_DIR = REPORTS / "runtime-start-signed-decision-guard-v1-fixtures"
REPORT_JSON = REPORTS / "runtime-start-signed-decision-guard-v1-20260617.json"
VALIDATION_JSON = REPORTS / "runtime-start-signed-decision-guard-v1-validation-20260617.json"
REPORT_MD = REPORTS / "runtime-start-signed-decision-guard-v1-20260617.md"

WORKER_POOL_ID = "service-worker-local-runtime-adapter-pool"
ATTESTATION = (
    "I approve preflight review only and understand this does not start a runtime or worker."
)

NEXT_ACTION = (
    "Use this guard before any future apply command; a separate apply preflight "
    "must still prove exact process, command, output, trace, and zero side effects."
)
EVALUATION_UTC = "2026-06-17T20:00:00Z"

ZERO_BOUNDARY = {
    "report_only": True,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "runtime_processes_started": 0,
    "command_previews_executed": 0,
    "worker_starts": 0,
    "worker_pools_registered": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
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

REQUIRED_FIELDS = [
    "schema_version",
    "decision_id",
    "worker_pool_id",
    "source_runtime_start_preflight_path",
    "decision",
    "operator_id",
    "operator_attestation",
    "signed_utc",
    "expires_utc",
    "allowed_scope",
    "allowed_command_preview_sha256",
    "allowed_output_artifact_path",
    "allowed_trace_id",
    "runtime_start_allowed",
    "worker_start_allowed",
    "rollback_plan",
    "runtime_boundary",
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


def preflight_summary() -> dict[str, Any]:
    data = load_json(PREFLIGHT_VALIDATION)
    return {
        "path": str(PREFLIGHT_VALIDATION),
        "all_checks_passed": data.get("all_checks_passed"),
        "worker_pool_id": data.get("worker_pool_id"),
        "runtime_start_verdict": data.get("runtime_start_verdict"),
        "runtime_start_allowed": data.get("runtime_start_allowed"),
        "worker_start_allowed": data.get("worker_start_allowed"),
        "accepted_count": data.get("accepted_count"),
    }


def command_preview_hash() -> str:
    report = load_json(PREFLIGHT_REPORT)
    positive = next(item for item in report["results"] if item["expected"] == "accepted")
    decision_material = load_json(Path(positive["path"]))["command_preview"]
    return hashlib.sha256(json.dumps(decision_material, sort_keys=True).encode("utf-8")).hexdigest()


def base_decision(decision_id: str, decision: str = "approve_runtime_start_preflight_only") -> dict[str, Any]:
    return {
        "schema_version": "agent_company.runtime_start_signed_decision_guard.v1",
        "decision_id": decision_id,
        "worker_pool_id": WORKER_POOL_ID,
        "source_runtime_start_preflight_path": str(PREFLIGHT_VALIDATION),
        "decision": decision,
        "operator_id": "human-operator",
        "operator_attestation": "deny-all-no-runtime-start" if decision == "deny" else ATTESTATION,
        "signed_utc": "2026-06-17T20:00:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if decision == "deny" else "runtime_start_preflight_only",
        "allowed_command_preview_sha256": "" if decision == "deny" else command_preview_hash(),
        "allowed_output_artifact_path": (
            "" if decision == "deny" else str(REPORTS / "runtime-start-preflight-v1-20260617.json")
        ),
        "allowed_trace_id": "" if decision == "deny" else "trace-runtime-start-preflight-v1-20260617",
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "rollback_plan": (
            "No runtime start decision is applied."
            if decision == "deny"
            else (
                "Discard generated report-only runtime-start decision artifacts; "
                "no runtime process or worker was started."
            )
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_all",
            "expected": "accepted",
            "decision": base_decision("runtime-start-decision-positive-deny", "deny"),
        },
        {
            "name": "positive_preflight_only",
            "expected": "accepted",
            "decision": base_decision("runtime-start-decision-positive-preflight-only"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(f"runtime-start-decision-negative-{name}")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("unknown_pool", lambda d: d.update({"worker_pool_id": "unknown-pool"}))
    negative("missing_preflight", lambda d: d.update({"source_runtime_start_preflight_path": ""}))
    negative("execute_scope", lambda d: d.update({"allowed_scope": "runtime_start_execute"}))
    negative("runtime_start_allowed", lambda d: d.update({"runtime_start_allowed": True}))
    negative("worker_start_allowed", lambda d: d.update({"worker_start_allowed": True}))
    negative("wildcard_command_hash", lambda d: d.update({"allowed_command_preview_sha256": "*"}))
    negative("missing_output_artifact", lambda d: d.update({"allowed_output_artifact_path": ""}))
    negative(
        "outside_output_artifact",
        lambda d: d.update({"allowed_output_artifact_path": r"C:\Temp\runtime-start.json"}),
    )
    negative("missing_trace", lambda d: d.update({"allowed_trace_id": ""}))
    negative("decision_applied", lambda d: d["runtime_boundary"].update({"decisions_applied": 1}))
    negative("runtime_process_started", lambda d: d["runtime_boundary"].update({"runtime_processes_started": 1}))
    negative("service_request_assigned", lambda d: d["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("mcp_tool_call", lambda d: d["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("external_side_effect", lambda d: d["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_decision(decision: dict[str, Any], schema: dict[str, Any], preflight: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    evaluation_time = parse_utc(EVALUATION_UTC)

    if schema.get("properties", {}).get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    for field in REQUIRED_FIELDS:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    if decision.get("schema_version") != "agent_company.runtime_start_signed_decision_guard.v1":
        errors.append("schema_version_mismatch")
    if decision.get("worker_pool_id") != WORKER_POOL_ID:
        errors.append("worker_pool_id_must_match_local_runtime_adapter_pool")
    if not str(decision.get("operator_id", "")).strip():
        errors.append("operator_id_missing")
    if not str(decision.get("operator_attestation", "")).strip():
        errors.append("operator_attestation_missing")

    signed = parse_utc(str(decision.get("signed_utc", "")))
    expires = parse_utc(str(decision.get("expires_utc", "")))
    if signed is None:
        errors.append("signed_utc_invalid")
    if expires is None:
        errors.append("expires_utc_invalid")
    if signed and expires and expires <= signed:
        errors.append("expires_not_after_signed")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("decision_expired")

    preflight_path = str(decision.get("source_runtime_start_preflight_path", ""))
    if not preflight_path:
        errors.append("source_runtime_start_preflight_path_missing")
    elif not path_inside_root(preflight_path):
        errors.append("source_runtime_start_preflight_path_must_stay_inside_lab")
    elif not Path(preflight_path).exists():
        errors.append("source_runtime_start_preflight_path_not_found")

    if preflight.get("all_checks_passed") is not True:
        errors.append("source_preflight_not_passing")
    if preflight.get("worker_pool_id") != WORKER_POOL_ID:
        errors.append("source_preflight_pool_mismatch")
    if preflight.get("runtime_start_verdict") != "dry_run_preview_valid_start_blocked":
        errors.append("source_preflight_verdict_must_be_start_blocked")
    if preflight.get("runtime_start_allowed") is not False or preflight.get("worker_start_allowed") is not False:
        errors.append("source_preflight_must_not_allow_starts")

    decision_value = decision.get("decision")
    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_decision_scope_must_be_none")
        for field in ["allowed_command_preview_sha256", "allowed_output_artifact_path", "allowed_trace_id"]:
            if decision.get(field):
                warnings.append(f"deny_decision_ignores_{field}")
    elif decision_value == "approve_runtime_start_preflight_only":
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("preflight_only_attestation_mismatch")
        if decision.get("allowed_scope") != "runtime_start_preflight_only":
            errors.append("allowed_scope_must_be_runtime_start_preflight_only")
        if decision.get("allowed_command_preview_sha256") != command_preview_hash():
            errors.append("allowed_command_preview_sha256_mismatch")
        output_path = str(decision.get("allowed_output_artifact_path", ""))
        if not output_path:
            errors.append("allowed_output_artifact_path_missing")
        elif not path_inside_root(output_path):
            errors.append("allowed_output_artifact_path_must_stay_inside_lab")
        if not str(decision.get("allowed_trace_id", "")):
            errors.append("allowed_trace_id_missing")
        if len(str(decision.get("rollback_plan", "")).strip()) < 20:
            errors.append("rollback_plan_too_short")
    else:
        errors.append("decision_value_invalid")

    if decision.get("runtime_start_allowed") is not False:
        errors.append("runtime_start_allowed_must_be_false")
    if decision.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")

    boundary = decision.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    accepted = not errors
    return {
        "decision_id": decision.get("decision_id"),
        "decision": decision_value,
        "accepted_for_later_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    preflight = preflight_summary()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        decision = (
            copy.deepcopy(fixture["decision"])
            if "decision" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_decision(decision, schema, preflight)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_later_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_later_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.runtime_start_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "worker_pool_id": WORKER_POOL_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_runtime_start_preflight_path": str(PREFLIGHT_VALIDATION),
        "source_runtime_start_preflight_sha256": sha256_path(PREFLIGHT_VALIDATION),
        "source_preflight": preflight,
        "positive_authority": {
            "accepted_scope": "runtime_start_preflight_only",
            "runtime_start_allowed": False,
            "worker_start_allowed": False,
        },
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.runtime_start_signed_decision_guard_validation.v1",
        "generated_utc": generated,
        "guard_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "runtime_start_allowed": False,
        "worker_start_allowed": False,
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


