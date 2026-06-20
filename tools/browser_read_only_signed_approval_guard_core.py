#!/usr/bin/env python3
"""Core helpers for report-only browser read-only signed approval guards."""

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
SCHEMA_PATH = ARCH / "browser-read-only-signed-approval-guard-v1.schema.json"
ASSIGNMENT_PREFLIGHT_VALIDATION = REPORTS / "browser-read-only-assignment-preflight-v1-validation-20260617.json"
ASSIGNMENT_PREFLIGHT_REPORT = REPORTS / "browser-read-only-assignment-preflight-v1-20260617.json"
FIXTURE_DIR = REPORTS / "browser-read-only-signed-approval-guard-v1-fixtures"
REPORT_JSON = REPORTS / "browser-read-only-signed-approval-guard-v1-20260617.json"
VALIDATION_JSON = REPORTS / "browser-read-only-signed-approval-guard-v1-validation-20260617.json"
REPORT_MD = REPORTS / "browser-read-only-signed-approval-guard-v1-20260617.md"

TRACE_ID = "trace-browser-read-only-signed-approval-guard-v1-20260617"
ATTESTATION = "I approve browser read-only assignment preflight review only and understand this does not assign a worker or open a browser."
EVALUATION_UTC = "2026-06-17T20:20:00Z"
NEXT_ACTION = (
    "Build a separate apply preflight before any accepted browser-read-only approval "
    "can assign a request or open a browser."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "service_requests_assigned": 0,
    "service_requests_mutated": 0,
    "browser_sessions_started": 0,
    "worker_starts": 0,
    "login_actions": False,
    "form_submit_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "public_actions": False,
    "security_testing_actions": False,
    "file_transfer_actions": False,
    "mcp_tool_calls": False,
    "model_api_calls": False,
    "credentials_accessed": False,
    "external_side_effects": False,
}

REQUIRED_FIELDS = [
    "schema_version",
    "decision_id",
    "source_assignment_preflight_path",
    "source_adapter_contract_validation_path",
    "decision",
    "operator_id",
    "operator_attestation",
    "signed_utc",
    "expires_utc",
    "allowed_scope",
    "allowed_candidate_request_ids",
    "assignment_allowed",
    "browser_session_start_allowed",
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
    return str(value).startswith(str(ROOT)) and ".." not in str(value)


def assignment_preflight_summary() -> dict[str, Any]:
    data = load_json(ASSIGNMENT_PREFLIGHT_VALIDATION)
    report = load_json(ASSIGNMENT_PREFLIGHT_REPORT)
    adapter_contract_validation = report.get("adapter_contract_validation", {})
    return {
        "path": str(ASSIGNMENT_PREFLIGHT_VALIDATION),
        "report_path": str(ASSIGNMENT_PREFLIGHT_REPORT),
        "all_checks_passed": data.get("all_checks_passed"),
        "preflight_verdict": data.get("preflight_verdict"),
        "adapter_contract_gate": data.get("adapter_contract_gate"),
        "adapter_contract_validation_path": data.get("adapter_contract_validation_path"),
        "adapter_contract_validation": adapter_contract_validation,
        "candidate_request_count": data.get("candidate_request_count"),
        "assignment_allowed_count": data.get("assignment_allowed_count"),
        "blocked_no_signed_approval_count": data.get("blocked_no_signed_approval_count"),
        "operator_signed_approval_present": data.get("operator_signed_approval_present"),
        "browser_sessions_started": data.get("browser_sessions_started"),
        "service_requests_assigned": data.get("service_requests_assigned"),
        "service_requests_mutated": data.get("service_requests_mutated"),
        "external_side_effects": data.get("external_side_effects"),
        "candidate_request_ids": [row["request_id"] for row in report.get("candidate_requests", [])],
    }


def base_decision(decision_id: str, decision: str = "approve_browser_read_only_assignment_preflight_only") -> dict[str, Any]:
    preflight = assignment_preflight_summary()
    return {
        "schema_version": "agent_company.browser_read_only_signed_approval_guard.v1",
        "decision_id": decision_id,
        "source_assignment_preflight_path": str(ASSIGNMENT_PREFLIGHT_VALIDATION),
        "source_adapter_contract_validation_path": preflight["adapter_contract_validation_path"],
        "decision": decision,
        "operator_id": "human-operator",
        "operator_attestation": "deny-all-no-browser-assignment" if decision == "deny" else ATTESTATION,
        "signed_utc": "2026-06-17T20:20:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "allowed_scope": "none" if decision == "deny" else "browser_read_only_assignment_preflight_only",
        "allowed_candidate_request_ids": [] if decision == "deny" else preflight["candidate_request_ids"],
        "assignment_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "rollback_plan": (
            "No browser assignment decision is applied."
            if decision == "deny"
            else "Discard generated report-only browser approval artifacts; no service "
            "request was assigned and no browser session was opened."
        ),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_deny_all",
            "expected": "accepted",
            "decision": base_decision("browser-read-only-approval-positive-deny", "deny"),
        },
        {
            "name": "positive_preflight_only",
            "expected": "accepted",
            "decision": base_decision("browser-read-only-approval-positive-preflight-only"),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(f"browser-read-only-approval-negative-{name}")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    negative("missing_operator", lambda d: d.update({"operator_id": ""}))
    negative("missing_attestation", lambda d: d.update({"operator_attestation": ""}))
    negative("wrong_attestation", lambda d: d.update({"operator_attestation": "I approve."}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("expires_before_signed", lambda d: d.update({"expires_utc": "2026-06-01T00:00:00Z"}))
    negative("missing_preflight", lambda d: d.update({"source_assignment_preflight_path": ""}))
    negative("outside_preflight", lambda d: d.update({"source_assignment_preflight_path": r"C:\Temp\preflight.json"}))
    negative("missing_adapter_contract_path", lambda d: d.update({"source_adapter_contract_validation_path": ""}))
    negative(
        "wrong_adapter_contract_path",
        lambda d: d.update({"source_adapter_contract_validation_path": r"C:\Temp\adapter-contract.json"}),
    )
    negative(
        "stale_adapter_contract_path",
        lambda d: d.update(
            {
                "source_adapter_contract_validation_path": str(
                    REPORTS / "stale-browser-worker-adapter-contract-validation.json"
                )
            }
        ),
    )
    negative("execute_scope", lambda d: d.update({"allowed_scope": "browser_execute"}))
    negative("assignment_allowed", lambda d: d.update({"assignment_allowed": True}))
    negative("browser_start_allowed", lambda d: d.update({"browser_session_start_allowed": True}))
    negative("worker_start_allowed", lambda d: d.update({"worker_start_allowed": True}))
    negative("missing_candidate_ids", lambda d: d.update({"allowed_candidate_request_ids": []}))
    negative("unknown_candidate_id", lambda d: d.update({"allowed_candidate_request_ids": ["req-unknown-browser"]}))
    negative("decision_applied", lambda d: d["runtime_boundary"].update({"decisions_applied": 1}))
    negative("approval_row_written", lambda d: d["runtime_boundary"].update({"approval_rows_written": 1}))
    negative("service_request_assigned", lambda d: d["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("service_request_mutated", lambda d: d["runtime_boundary"].update({"service_requests_mutated": 1}))
    negative("browser_started", lambda d: d["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("worker_started", lambda d: d["runtime_boundary"].update({"worker_starts": 1}))
    negative("login_action", lambda d: d["runtime_boundary"].update({"login_actions": True}))
    negative("public_action", lambda d: d["runtime_boundary"].update({"public_actions": True}))
    negative("payment_action", lambda d: d["runtime_boundary"].update({"payment_actions": True}))
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

    if decision.get("schema_version") != "agent_company.browser_read_only_signed_approval_guard.v1":
        errors.append("schema_version_mismatch")
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

    preflight_path = str(decision.get("source_assignment_preflight_path", ""))
    if not preflight_path:
        errors.append("source_assignment_preflight_path_missing")
    elif not path_inside_root(preflight_path):
        errors.append("source_assignment_preflight_path_must_stay_inside_lab")
    elif not Path(preflight_path).exists():
        errors.append("source_assignment_preflight_path_not_found")

    adapter_contract_path = str(decision.get("source_adapter_contract_validation_path", ""))
    expected_adapter_contract_path = str(preflight.get("adapter_contract_validation_path", ""))
    if not adapter_contract_path:
        errors.append("source_adapter_contract_validation_path_missing")
    elif not path_inside_root(adapter_contract_path):
        errors.append("source_adapter_contract_validation_path_must_stay_inside_lab")
    elif adapter_contract_path != expected_adapter_contract_path:
        errors.append("source_adapter_contract_validation_path_must_match_source_preflight")
    elif not Path(adapter_contract_path).exists():
        errors.append("source_adapter_contract_validation_path_not_found")

    if preflight.get("all_checks_passed") is not True:
        errors.append("source_assignment_preflight_not_passing")
    if preflight.get("preflight_verdict") != "candidates_valid_assignment_blocked_no_signed_approval":
        errors.append("source_assignment_preflight_verdict_must_be_blocked_without_signed_approval")
    if preflight.get("assignment_allowed_count") != 0:
        errors.append("source_assignment_preflight_must_not_allow_assignments")
    if preflight.get("browser_sessions_started") != 0:
        errors.append("source_assignment_preflight_must_not_start_browser")
    if preflight.get("service_requests_assigned") != 0 or preflight.get("service_requests_mutated") != 0:
        errors.append("source_assignment_preflight_must_not_mutate_queue")
    if preflight.get("external_side_effects") is not False:
        errors.append("source_assignment_preflight_must_have_no_external_side_effects")
    if preflight.get("adapter_contract_gate") != "present_valid_start_blocked":
        errors.append("source_assignment_preflight_adapter_contract_gate_must_be_valid_start_blocked")
    adapter_contract = preflight.get("adapter_contract_validation", {})
    if not isinstance(adapter_contract, dict):
        errors.append("source_assignment_preflight_adapter_contract_validation_must_be_object")
        adapter_contract = {}
    if adapter_contract.get("all_checks_passed") is not True:
        errors.append("adapter_contract_validation_must_pass")
    if adapter_contract.get("contract_verdict") != "adapter_contract_valid_start_blocked":
        errors.append("adapter_contract_validation_verdict_must_be_valid_start_blocked")
    if adapter_contract.get("browser_session_start_allowed") is not False:
        errors.append("adapter_contract_must_not_allow_browser_start")
    if adapter_contract.get("browser_sessions_started") != 0:
        errors.append("adapter_contract_must_not_start_browser")
    if adapter_contract.get("worker_start_allowed") is not False:
        errors.append("adapter_contract_must_not_allow_worker_start")
    if adapter_contract.get("workers_started") != 0:
        errors.append("adapter_contract_must_not_start_workers")
    if adapter_contract.get("mcp_servers_started") != 0:
        errors.append("adapter_contract_must_not_start_mcp_servers")
    if adapter_contract.get("service_requests_assigned") != 0 or adapter_contract.get("service_requests_mutated") != 0:
        errors.append("adapter_contract_must_not_mutate_service_requests")
    if adapter_contract.get("external_side_effects") is not False:
        errors.append("adapter_contract_must_have_no_external_side_effects")

    decision_value = decision.get("decision")
    allowed_ids = decision.get("allowed_candidate_request_ids", [])
    if not isinstance(allowed_ids, list):
        errors.append("allowed_candidate_request_ids_must_be_list")
        allowed_ids = []
    known_ids = set(preflight.get("candidate_request_ids", []))
    unknown_ids = sorted(set(str(item) for item in allowed_ids) - known_ids)
    if unknown_ids:
        errors.append("allowed_candidate_request_ids_unknown:" + ",".join(unknown_ids))

    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_decision_scope_must_be_none")
        if allowed_ids:
            warnings.append("deny_decision_ignores_allowed_candidate_request_ids")
    elif decision_value == "approve_browser_read_only_assignment_preflight_only":
        if decision.get("operator_attestation") != ATTESTATION:
            errors.append("preflight_only_attestation_mismatch")
        if decision.get("allowed_scope") != "browser_read_only_assignment_preflight_only":
            errors.append("allowed_scope_must_be_browser_read_only_assignment_preflight_only")
        if not allowed_ids:
            errors.append("allowed_candidate_request_ids_missing")
        if set(str(item) for item in allowed_ids) != known_ids:
            errors.append("allowed_candidate_request_ids_must_match_current_candidates")
        if len(str(decision.get("rollback_plan", "")).strip()) < 20:
            errors.append("rollback_plan_too_short")
    else:
        errors.append("decision_value_invalid")

    if decision.get("assignment_allowed") is not False:
        errors.append("assignment_allowed_must_be_false")
    if decision.get("browser_session_start_allowed") is not False:
        errors.append("browser_session_start_allowed_must_be_false")
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
        "assignment_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    preflight = assignment_preflight_summary()
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
        "schema_version": "agent_company.browser_read_only_signed_approval_guard_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_assignment_preflight_path": str(ASSIGNMENT_PREFLIGHT_VALIDATION),
        "source_assignment_preflight_sha256": sha256_path(ASSIGNMENT_PREFLIGHT_VALIDATION),
        "source_preflight": preflight,
        "positive_authority": {
            "accepted_scope": "browser_read_only_assignment_preflight_only",
            "assignment_allowed": False,
            "browser_session_start_allowed": False,
            "worker_start_allowed": False,
        },
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "assignment_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "adapter_contract_gate": preflight.get("adapter_contract_gate"),
        "adapter_contract_validation_path": preflight.get("adapter_contract_validation_path"),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.browser_read_only_signed_approval_guard_validation.v1",
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
        "assignment_allowed": False,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "adapter_contract_gate": preflight.get("adapter_contract_gate"),
        "adapter_contract_validation_path": preflight.get("adapter_contract_validation_path"),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


