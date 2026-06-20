#!/usr/bin/env python3
"""Validate browser read-only worker policy plans without opening a browser."""

from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from runtime_boundary_shared_core import collect_runtime_boundary_errors


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
STATE_DB = ROOT / "state" / "agent_company.sqlite"
SCHEMA_PATH = ARCH / "browser-read-only-worker-policy-v1.schema.json"
FIXTURE_DIR = REPORTS / "browser-read-only-worker-policy-v1-fixtures"
REPORT_JSON = REPORTS / "browser-read-only-worker-policy-v1-20260617.json"
VALIDATION_JSON = REPORTS / "browser-read-only-worker-policy-v1-validation-20260617.json"
REPORT_MD = REPORTS / "browser-read-only-worker-policy-v1-20260617.md"

TRACE_ID = "trace-browser-read-only-worker-policy-v1-20260617"
POSITIVE_REQUEST_ID = "req-wave4-money-source-discovery-browser-readonly-20260614"
SERVICE_ID = "browser_read_only_session"
REQUEST_TYPE = "browser_research"

NEXT_ACTION = (
    "After operator approval exists, wire this policy into browser_read_only_session "
    "assignment preflight before any in-app browser or Browser Use worker starts."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "browser_sessions_started": 0,
    "worker_starts": 0,
    "service_requests_assigned": 0,
    "service_requests_mutated": 0,
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

READ_ONLY_ACTIONS = [
    "navigate_public_https_url",
    "read_visible_public_text",
    "capture_source_url",
    "write_local_markdown_evidence",
]

FORBIDDEN_ACTIONS = [
    "login",
    "signup",
    "submit_form",
    "accept_terms",
    "post_comment",
    "like_follow_reply_repost",
    "create_or_edit_account",
    "upload_file",
    "download_private_file",
    "purchase",
    "payment_method",
    "connect_wallet",
    "sign_wallet_message",
    "security_testing",
    "scrape_prohibited_source",
    "api_key_or_secret_access",
]

PROHIBITED_ACTION_TOKENS = {
    "login": ["login", "sign_in", "authenticate"],
    "form_submit_actions": ["submit_form", "submit_search_form", "accept_terms", "send_message"],
    "account_actions": ["signup", "create_account", "edit_profile", "save_settings", "seller_onboarding"],
    "wallet_actions": ["connect_wallet", "sign_wallet_message", "wallet_public_address", "claim_airdrop"],
    "payment_actions": ["purchase", "payment_method", "checkout", "withdraw", "deposit"],
    "public_actions": [
        "post_comment",
        "reply",
        "like",
        "follow",
        "repost",
        "publish",
        "open_pull_request",
        "claim_bounty",
    ],
    "security_testing_actions": ["security_testing", "exploit", "live_poc", "scan_target"],
    "file_transfer_actions": ["upload_file", "download_private_file", "download_dataset"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    try:
        path = Path(value)
    except Exception:
        return False
    return str(path).startswith(str(ROOT)) and ".." not in str(path)


def hostname(value: str) -> str:
    return (urlparse(value).hostname or "").lower()


def request_index() -> dict[str, dict[str, Any]]:
    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT request_id, service_id, request_type, lane_id, status, risk_gate,
               requested_action, artifact_path, intake_json
        FROM service_requests
        WHERE request_type = ? OR service_id = ?
        ORDER BY request_id
        """,
        (REQUEST_TYPE, SERVICE_ID),
    ).fetchall()
    con.close()
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        item = dict(row)
        try:
            item["intake"] = json.loads(item.get("intake_json") or "{}")
        except json.JSONDecodeError:
            item["intake"] = {}
        indexed[item["request_id"]] = item
    return indexed


def base_plan(plan_id: str = "browser-read-only-policy-positive-public-plan") -> dict[str, Any]:
    return {
        "policy_plan_id": plan_id,
        "request_id": POSITIVE_REQUEST_ID,
        "service_id": SERVICE_ID,
        "request_type": REQUEST_TYPE,
        "lane_id": "money_source_discovery",
        "session_mode": "public_read_only_no_login",
        "navigation_scope": "explicit_allowlist_only",
        "target_urls": ["https://github.com/topics/bounty"],
        "allowed_domains": ["github.com"],
        "allowed_actions": copy.deepcopy(READ_ONLY_ACTIONS),
        "forbidden_actions": copy.deepcopy(FORBIDDEN_ACTIONS),
        "evidence_output_artifact_path": str(REPORTS / "browser-read-only-worker-policy-v1-evidence-placeholder.md"),
        "declared_capture_log_path": str(REPORTS / "browser-read-only-worker-policy-v1-capture-log-placeholder.json"),
        "teardown_required": True,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "trace_id": TRACE_ID,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [{"name": "positive_public_read_only_plan_start_blocked", "expected": "accepted", "entry": base_plan()}]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        entry = base_plan(f"browser-read-only-policy-negative-{name}")
        mutate(entry)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "entry": entry})

    negative("missing_service_request", lambda e: e.update({"request_id": "req-missing-browser-readonly"}))
    negative("wrong_service_id", lambda e: e.update({"service_id": "public_action_execution"}))
    negative("signed_in_session", lambda e: e.update({"session_mode": "signed_in_named_scope"}))
    negative("unknown_session", lambda e: e.update({"session_mode": "unknown"}))
    negative("missing_allowlist", lambda e: e.update({"allowed_domains": []}))
    negative("wildcard_domain", lambda e: e.update({"allowed_domains": ["*"]}))
    negative("unbounded_navigation", lambda e: e.update({"navigation_scope": "unbounded"}))
    negative("target_outside_allowlist", lambda e: e.update({"target_urls": ["https://example.com/not-allowed"]}))
    negative("http_url", lambda e: e.update({"target_urls": ["http://github.com/topics/bounty"]}))
    negative("login_allowed", lambda e: e["allowed_actions"].append("login"))
    negative("form_submit_allowed", lambda e: e["allowed_actions"].append("submit_form"))
    negative("public_action_allowed", lambda e: e["allowed_actions"].append("post_comment"))
    negative("account_action_allowed", lambda e: e["allowed_actions"].append("edit_profile"))
    negative("wallet_action_allowed", lambda e: e["allowed_actions"].append("connect_wallet"))
    negative("payment_action_allowed", lambda e: e["allowed_actions"].append("payment_method"))
    negative("security_testing_allowed", lambda e: e["allowed_actions"].append("security_testing"))
    negative("file_upload_allowed", lambda e: e["allowed_actions"].append("upload_file"))
    negative("file_download_allowed", lambda e: e["allowed_actions"].append("download_private_file"))
    negative("missing_capture_log", lambda e: e.update({"declared_capture_log_path": ""}))
    negative("missing_output_artifact", lambda e: e.update({"evidence_output_artifact_path": ""}))
    negative("teardown_not_required", lambda e: e.update({"teardown_required": False}))
    negative("browser_start_allowed", lambda e: e.update({"browser_session_start_allowed": True}))
    negative("worker_start_allowed", lambda e: e.update({"worker_start_allowed": True}))
    negative("browser_started", lambda e: e["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("service_request_assigned", lambda e: e["runtime_boundary"].update({"service_requests_assigned": 1}))
    negative("service_request_mutated", lambda e: e["runtime_boundary"].update({"service_requests_mutated": 1}))
    negative("mcp_tool_called", lambda e: e["runtime_boundary"].update({"mcp_tool_calls": True}))
    negative("external_side_effect", lambda e: e["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_plan(entry: dict[str, Any], schema: dict[str, Any], requests: dict[str, dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []

    if schema.get("properties", {}).get("session_mode", {}).get("enum", [None])[0] != "public_read_only_no_login":
        errors.append("schema_session_mode_must_start_public_read_only_no_login")
    if entry.get("service_id") != SERVICE_ID:
        errors.append("service_id_must_be_browser_read_only_session")
    if entry.get("request_type") != REQUEST_TYPE:
        errors.append("request_type_must_be_browser_research")
    if entry.get("session_mode") != "public_read_only_no_login":
        errors.append("session_mode_must_be_public_read_only_no_login")
    if entry.get("navigation_scope") != "explicit_allowlist_only":
        errors.append("navigation_scope_must_be_explicit_allowlist_only")
    if entry.get("browser_session_start_allowed") is not False:
        errors.append("browser_session_start_allowed_must_be_false")
    if entry.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")
    if entry.get("teardown_required") is not True:
        errors.append("teardown_required_must_be_true")
    if not str(entry.get("trace_id", "")):
        errors.append("trace_id_missing")

    request_id = str(entry.get("request_id", ""))
    request = requests.get(request_id)
    if not request:
        errors.append("service_request_not_found")
    else:
        if request.get("service_id") != SERVICE_ID:
            errors.append("service_request_service_id_mismatch")
        if request.get("request_type") != REQUEST_TYPE:
            errors.append("service_request_type_mismatch")
        if request.get("status") != "needs_review":
            errors.append("service_request_must_remain_needs_review")
        if request.get("risk_gate") != "catalog_required_approval_no_external_action":
            errors.append("service_request_risk_gate_must_block_external_action")
        if request.get("lane_id") != entry.get("lane_id"):
            errors.append("service_request_lane_mismatch")
        sensitivity = str(request.get("intake", {}).get("session_sensitivity", "")).lower()
        if "signed" in sensitivity and "no_signed_in" not in sensitivity:
            errors.append("service_request_intake_must_not_require_signed_in_session")

    allowed_domains = entry.get("allowed_domains", [])
    if not isinstance(allowed_domains, list) or not allowed_domains:
        errors.append("allowed_domains_must_be_nonempty")
        allowed_domains = []
    if any(domain in {"*", "*.*"} or "*" in str(domain) for domain in allowed_domains):
        errors.append("allowed_domains_must_not_use_wildcards")
    normalized_domains = {str(domain).lower() for domain in allowed_domains}

    target_urls = entry.get("target_urls", [])
    if not isinstance(target_urls, list) or not target_urls:
        errors.append("target_urls_must_be_nonempty")
        target_urls = []
    for url in target_urls:
        if not isinstance(url, str) or not url.startswith("https://"):
            errors.append("target_urls_must_be_https")
            continue
        host = hostname(url)
        if host not in normalized_domains and not any(host.endswith("." + domain) for domain in normalized_domains):
            errors.append("target_url_host_must_be_in_allowed_domains")
            break

    allowed_actions = entry.get("allowed_actions", [])
    if not isinstance(allowed_actions, list) or not allowed_actions:
        errors.append("allowed_actions_must_be_nonempty")
        allowed_actions = []
    allowed_set = {str(action) for action in allowed_actions}
    missing_read_only = sorted(set(READ_ONLY_ACTIONS) - allowed_set)
    if missing_read_only:
        errors.append("allowed_actions_missing_required_read_only_actions")
    for action in allowed_set:
        for boundary_key, tokens in PROHIBITED_ACTION_TOKENS.items():
            if action in tokens:
                errors.append(f"allowed_actions_include_prohibited_{boundary_key}")
                break

    forbidden_actions = set(str(action) for action in entry.get("forbidden_actions", []))
    missing_forbidden = sorted(set(FORBIDDEN_ACTIONS) - forbidden_actions)
    if missing_forbidden:
        errors.append("forbidden_actions_missing_required_stops")

    for path_key in ["evidence_output_artifact_path", "declared_capture_log_path"]:
        path_value = str(entry.get(path_key, ""))
        if not path_value:
            errors.append(f"{path_key}_missing")
        elif not path_inside_root(path_value):
            errors.append(f"{path_key}_must_stay_inside_lab")

    errors.extend(collect_runtime_boundary_errors(entry, ZERO_BOUNDARY))

    accepted = not errors
    return {
        "policy_plan_id": entry.get("policy_plan_id"),
        "request_id": entry.get("request_id"),
        "accepted_for_browser_read_only_policy": accepted,
        "rejected": not accepted,
        "errors": errors,
        "policy_verdict": "public_read_only_plan_valid_start_blocked" if accepted else "rejected_policy_violation",
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    requests = request_index()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        entry = (
            copy.deepcopy(fixture["entry"])
            if "entry" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_plan(entry, schema, requests)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_browser_read_only_policy"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_browser_read_only_policy"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.browser_read_only_worker_policy_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "service_request_source": str(STATE_DB),
        "policy_verdict": "public_read_only_plan_valid_start_blocked",
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "positive_fixture": {
            "request_id": POSITIVE_REQUEST_ID,
            "expected_result": "pass_read_only_plan_start_blocked",
            "browser_session_start_allowed": False,
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
        "schema_version": "agent_company.browser_read_only_worker_policy_validation.v1",
        "generated_utc": generated,
        "validator_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "policy_verdict": report["policy_verdict"],
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return report, validation


