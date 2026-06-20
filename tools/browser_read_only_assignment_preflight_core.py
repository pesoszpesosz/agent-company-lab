#!/usr/bin/env python3
"""Validate browser read-only service-request assignment preflight without assigning workers."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
STATE_DB = ROOT / "state" / "agent_company.sqlite"
SCHEMA_PATH = ARCH / "browser-read-only-assignment-preflight-v1.schema.json"
POLICY_VALIDATION = REPORTS / "browser-read-only-worker-policy-v1-validation-20260617.json"
ADAPTER_CONTRACT_VALIDATION = REPORTS / "browser-worker-adapter-contract-v1-validation-20260618.json"
REPORT_JSON = REPORTS / "browser-read-only-assignment-preflight-v1-20260617.json"
VALIDATION_JSON = REPORTS / "browser-read-only-assignment-preflight-v1-validation-20260617.json"
REPORT_MD = REPORTS / "browser-read-only-assignment-preflight-v1-20260617.md"

TRACE_ID = "trace-browser-read-only-assignment-preflight-v1-20260617"
SERVICE_ID = "browser_read_only_session"
REQUEST_TYPE = "browser_research"

NEXT_ACTION = (
    "Require a real signed operator approval packet before any browser_read_only_session "
    "request can be assigned or started."
)

ZERO_BOUNDARY = {
    "report_only": True,
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return str(value).startswith(str(ROOT)) and ".." not in str(value)


def browser_requests() -> list[dict[str, Any]]:
    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT request_id, service_id, request_type, lane_id, status, risk_gate,
               requested_action, approval_scope, artifact_path, assigned_agent_id,
               started_at, completed_at, intake_json
        FROM service_requests
        WHERE service_id = ? AND request_type = ?
        ORDER BY request_id
        """,
        (SERVICE_ID, REQUEST_TYPE),
    ).fetchall()
    con.close()
    result = []
    for row in rows:
        item = dict(row)
        try:
            item["intake"] = json.loads(item.get("intake_json") or "{}")
        except json.JSONDecodeError:
            item["intake"] = {}
        result.append(item)
    return result


def classify_request(
    row: dict[str, Any],
    policy_ok: bool,
    adapter_contract_ok: bool,
    operator_signed_approval_present: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    if row.get("service_id") != SERVICE_ID:
        errors.append("service_id_mismatch")
    if row.get("request_type") != REQUEST_TYPE:
        errors.append("request_type_mismatch")
    if row.get("status") != "needs_review":
        errors.append("status_must_remain_needs_review")
    if row.get("risk_gate") != "catalog_required_approval_no_external_action":
        errors.append("risk_gate_must_require_no_external_action_approval")
    if row.get("assigned_agent_id"):
        errors.append("request_must_not_already_be_assigned")
    if row.get("started_at"):
        errors.append("request_must_not_already_be_started")
    if not row.get("artifact_path") or not path_inside_root(str(row.get("artifact_path"))):
        errors.append("artifact_path_must_stay_inside_lab")

    intake = row.get("intake", {})
    required_intake_fields = [
        "allowed_read_scope",
        "evidence_needed",
        "forbidden_actions",
        "lane_id",
        "session_sensitivity",
        "target_url",
    ]
    for required in required_intake_fields:
        if not intake.get(required):
            errors.append(f"intake_missing_{required}")
    forbidden = str(intake.get("forbidden_actions", "")).lower()
    forbidden_families = {
        "login": ["login", "signed", "oauth", "credential"],
        "payment": ["payment", "purchase", "payout", "wallet", "funds", "checkout", "tax", "kyc"],
        "public": [
            "public",
            "comment",
            "reply",
            "follow",
            "like",
            "repost",
            "publish",
            "promotion",
            "message",
            "pr",
            "pull request",
            "issue",
            "submission",
            "claim",
        ],
        "account": [
            "account",
            "login",
            "signup",
            "sign-up",
            "registration",
            "register",
            "join",
            "seller onboarding",
            "profile",
            "oauth",
            "credential",
        ],
    }
    for family, tokens in forbidden_families.items():
        if not any(token in forbidden for token in tokens):
            errors.append(f"forbidden_actions_must_cover_{family}_risk")
    if str(intake.get("lane_id")) != row.get("lane_id"):
        errors.append("intake_lane_mismatch")

    assignment_allowed = bool(policy_ok and adapter_contract_ok and operator_signed_approval_present and not errors)
    return {
        "request_id": row.get("request_id"),
        "lane_id": row.get("lane_id"),
        "status": row.get("status"),
        "risk_gate": row.get("risk_gate"),
        "artifact_path": row.get("artifact_path"),
        "assignment_allowed": assignment_allowed,
        "blocked_reason": None if assignment_allowed else "no_signed_operator_approval",
        "packet_complete": not errors,
        "errors": errors,
    }


def build_report(schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    failures: list[str] = []
    generated = utc_now()

    verdict_enum = schema.get("properties", {}).get("preflight_verdict", {}).get("enum", [None])
    if verdict_enum[0] != "blocked_missing_policy_validation":
        failures.append("schema_preflight_verdict_must_start_blocked_missing_policy_validation")

    policy_exists = POLICY_VALIDATION.exists()
    policy_validation = {
        "path": str(POLICY_VALIDATION),
        "exists": policy_exists,
        "sha256": sha256_path(POLICY_VALIDATION),
        "all_checks_passed": False,
        "policy_verdict": "blocked_missing_policy_validation",
    }
    if policy_exists:
        data = load_json(POLICY_VALIDATION)
        policy_validation.update(
            {
                "schema_version": data.get("schema_version"),
                "all_checks_passed": bool(data.get("all_checks_passed")),
                "failure_count": data.get("failure_count"),
                "policy_verdict": data.get("policy_verdict"),
                "browser_session_start_allowed": data.get("browser_session_start_allowed"),
                "browser_sessions_started": data.get("browser_sessions_started"),
                "service_requests_assigned": data.get("service_requests_assigned"),
                "service_requests_mutated": data.get("service_requests_mutated"),
                "external_side_effects": data.get("external_side_effects"),
            }
        )

    policy_ok = bool(
        policy_validation.get("exists")
        and policy_validation.get("all_checks_passed")
        and policy_validation.get("policy_verdict") == "public_read_only_plan_valid_start_blocked"
        and policy_validation.get("browser_session_start_allowed") is False
        and policy_validation.get("browser_sessions_started") == 0
        and policy_validation.get("service_requests_assigned") == 0
        and policy_validation.get("service_requests_mutated") == 0
        and policy_validation.get("external_side_effects") is False
    )
    if not policy_validation.get("exists"):
        failures.append("policy_validation_missing")
    elif not policy_ok:
        failures.append("policy_validation_not_passing_zero_side_effect_gate")

    adapter_exists = ADAPTER_CONTRACT_VALIDATION.exists()
    adapter_contract_validation = {
        "path": str(ADAPTER_CONTRACT_VALIDATION),
        "exists": adapter_exists,
        "sha256": sha256_path(ADAPTER_CONTRACT_VALIDATION),
        "all_checks_passed": False,
        "contract_verdict": "blocked_missing_adapter_contract_validation",
    }
    if adapter_exists:
        data = load_json(ADAPTER_CONTRACT_VALIDATION)
        adapter_contract_validation.update(
            {
                "schema_version": data.get("schema_version"),
                "all_checks_passed": bool(data.get("all_checks_passed")),
                "failure_count": data.get("failure_count"),
                "contract_verdict": data.get("contract_verdict"),
                "browser_session_start_allowed": data.get("browser_session_start_allowed"),
                "browser_sessions_started": data.get("browser_sessions_started"),
                "worker_start_allowed": data.get("worker_start_allowed"),
                "workers_started": data.get("workers_started"),
                "mcp_servers_started": data.get("mcp_servers_started"),
                "service_requests_assigned": data.get("service_requests_assigned"),
                "service_requests_mutated": data.get("service_requests_mutated"),
                "external_side_effects": data.get("external_side_effects"),
            }
        )
    adapter_contract_ok = bool(
        adapter_contract_validation.get("exists")
        and adapter_contract_validation.get("all_checks_passed")
        and adapter_contract_validation.get("contract_verdict") == "adapter_contract_valid_start_blocked"
        and adapter_contract_validation.get("browser_session_start_allowed") is False
        and adapter_contract_validation.get("browser_sessions_started") == 0
        and adapter_contract_validation.get("worker_start_allowed") is False
        and adapter_contract_validation.get("workers_started") == 0
        and adapter_contract_validation.get("mcp_servers_started") == 0
        and adapter_contract_validation.get("service_requests_assigned") == 0
        and adapter_contract_validation.get("service_requests_mutated") == 0
        and adapter_contract_validation.get("external_side_effects") is False
    )
    if not adapter_contract_validation.get("exists"):
        failures.append("adapter_contract_validation_missing")
    elif not adapter_contract_ok:
        failures.append("adapter_contract_validation_not_passing_zero_side_effect_gate")

    operator_signed_approval_present = False
    requests = browser_requests()
    if not requests:
        failures.append("no_browser_read_only_candidate_requests")
    candidate_requests = [
        classify_request(row, policy_ok, adapter_contract_ok, operator_signed_approval_present) for row in requests
    ]
    incomplete = [row["request_id"] for row in candidate_requests if not row["packet_complete"]]
    if incomplete:
        failures.append("candidate_request_packets_incomplete:" + ",".join(incomplete))

    assignment_allowed_count = sum(1 for row in candidate_requests if row["assignment_allowed"])
    blocked_no_signed_approval_count = sum(
        1 for row in candidate_requests if row["blocked_reason"] == "no_signed_operator_approval"
    )
    if assignment_allowed_count != 0:
        failures.append("assignment_allowed_without_signed_approval")
    if blocked_no_signed_approval_count != len(candidate_requests):
        failures.append("all_candidates_must_be_blocked_without_signed_approval")

    if not policy_validation.get("exists"):
        verdict = "blocked_missing_policy_validation"
    elif not policy_ok:
        verdict = "blocked_policy_validation_failed"
    elif not adapter_contract_validation.get("exists"):
        verdict = "blocked_missing_adapter_contract_validation"
    elif not adapter_contract_ok:
        verdict = "blocked_adapter_contract_validation_failed"
    elif not candidate_requests:
        verdict = "blocked_no_candidate_requests"
    else:
        verdict = "candidates_valid_assignment_blocked_no_signed_approval"

    adapter_contract_gate = (
        "present_valid_start_blocked"
        if adapter_contract_ok
        else (
            "missing"
            if not adapter_contract_validation.get("exists")
            else "present_invalid_or_side_effectful"
        )
    )

    report = {
        "schema_version": "agent_company.browser_read_only_assignment_preflight_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "preflight_id": "browser-read-only-assignment-preflight-current-queue",
        "service_id": SERVICE_ID,
        "request_type": REQUEST_TYPE,
        "schema_path": str(SCHEMA_PATH),
        "policy_validation": policy_validation,
        "adapter_contract_validation": adapter_contract_validation,
        "operator_signed_approval_present": operator_signed_approval_present,
        "preflight_verdict": verdict,
        "candidate_request_count": len(candidate_requests),
        "assignment_allowed_count": assignment_allowed_count,
        "blocked_no_signed_approval_count": blocked_no_signed_approval_count,
        "candidate_requests": candidate_requests,
        "runtime_boundary": ZERO_BOUNDARY.copy(),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.browser_read_only_assignment_preflight_validation.v1",
        "generated_utc": generated,
        "validator_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "policy_validation_path": str(POLICY_VALIDATION),
        "adapter_contract_validation_path": str(ADAPTER_CONTRACT_VALIDATION),
        "adapter_contract_gate": adapter_contract_gate,
        "preflight_verdict": verdict,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "candidate_request_count": len(candidate_requests),
        "assignment_allowed_count": assignment_allowed_count,
        "blocked_no_signed_approval_count": blocked_no_signed_approval_count,
        "operator_signed_approval_present": operator_signed_approval_present,
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


