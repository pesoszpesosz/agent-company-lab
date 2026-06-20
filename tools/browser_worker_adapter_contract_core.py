#!/usr/bin/env python3
"""Core browser-worker adapter contract validation helpers."""

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
SCHEMA_PATH = ARCH / "browser-worker-adapter-contract-v1.schema.json"
FIXTURE_DIR = REPORTS / "browser-worker-adapter-contract-v1-fixtures"
REPORT_JSON = REPORTS / "browser-worker-adapter-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "browser-worker-adapter-contract-v1-validation-20260618.json"
TRACE_METADATA_JSON = REPORTS / "browser-worker-adapter-contract-v1-trace-metadata-20260618.json"
REPORT_MD = REPORTS / "browser-worker-adapter-contract-v1-20260618.md"

TRACE_ID = "trace-browser-worker-adapter-contract-v1-20260618"
POSITIVE_REQUEST_ID = "req-wave4-money-source-discovery-browser-readonly-20260614"
SERVICE_ID = "browser_read_only_session"
REQUEST_TYPE = "browser_research"

ZERO_BOUNDARY = {
    "report_only": True,
    "browser_sessions_started": 0,
    "workers_started": 0,
    "mcp_servers_started": 0,
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
    "model_api_calls": False,
    "credentials_accessed": False,
    "external_side_effects": False,
}

ALLOWED_ACTION_CLASSES = [
    "navigate_public_https_url",
    "read_visible_public_text",
    "capture_accessibility_snapshot",
    "capture_screenshot",
    "write_local_evidence",
]

DENIED_ACTION_CLASSES = [
    "login",
    "signup",
    "submit_form",
    "accept_terms",
    "post_comment",
    "reply_like_follow_repost",
    "create_or_edit_account",
    "upload_file",
    "download_private_file",
    "purchase_or_payment",
    "connect_or_sign_wallet",
    "security_testing",
    "unbounded_scrape_or_crawl",
    "execute_arbitrary_browser_code",
    "credential_or_secret_access",
]

PROHIBITED_ALLOWED_CLASSES = {
    "login_actions": ["login", "signup", "accept_terms"],
    "form_submit_actions": ["submit_form"],
    "account_actions": ["create_or_edit_account"],
    "wallet_actions": ["connect_or_sign_wallet"],
    "payment_actions": ["purchase_or_payment"],
    "public_actions": ["post_comment", "reply_like_follow_repost"],
    "security_testing_actions": ["security_testing"],
    "file_transfer_actions": ["upload_file", "download_private_file"],
    "mcp_servers_started": ["execute_arbitrary_browser_code"],
    "credentials_accessed": ["credential_or_secret_access"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


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
        SELECT request_id, service_id, request_type, lane_id, status, risk_gate, intake_json
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


def base_contract(contract_id: str = "browser-worker-adapter-contract-positive-playwright") -> dict[str, Any]:
    return {
        "adapter_contract_id": contract_id,
        "request_id": POSITIVE_REQUEST_ID,
        "service_id": SERVICE_ID,
        "request_type": REQUEST_TYPE,
        "lane_id": "money_source_discovery",
        "adapter_kind": "playwright_deterministic",
        "runtime_candidate": "microsoft/playwright",
        "execution_mode": "report_only_contract",
        "session_mode": "public_read_only_no_login",
        "navigation_scope": "explicit_allowlist_only",
        "allowed_domains": ["github.com"],
        "target_urls": ["https://github.com/topics/bounty"],
        "allowed_action_classes": copy.deepcopy(ALLOWED_ACTION_CLASSES),
        "denied_action_classes": copy.deepcopy(DENIED_ACTION_CLASSES),
        "required_artifacts": {
            "capture_log_path": str(REPORTS / "browser-worker-adapter-contract-v1-capture-log-placeholder.json"),
            "evidence_markdown_path": str(REPORTS / "browser-worker-adapter-contract-v1-evidence-placeholder.md"),
            "screenshot_dir": str(REPORTS / "browser-worker-adapter-contract-v1-screenshots"),
            "trace_metadata_path": str(REPORTS / "browser-worker-adapter-contract-v1-trace-metadata-placeholder.json"),
        },
        "lifecycle": {
            "preflight_required": True,
            "teardown_required": True,
            "manual_approval_required_before_start": True,
            "kill_switch_required": True,
            "max_session_minutes": 0,
        },
        "egress_trace": {
            "trace_id": TRACE_ID,
            "source": "browser_worker_adapter_contract_v1",
            "event_type": "browser_worker_adapter_contract_validated",
            "artifact_path": str(VALIDATION_JSON),
        },
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_playwright_read_only_adapter_start_blocked",
            "expected": "accepted",
            "entry": base_contract(),
        }
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        entry = base_contract(f"browser-worker-adapter-contract-negative-{name}")
        mutate(entry)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "entry": entry})

    negative("missing_request", lambda e: e.update({"request_id": "req-missing-browser-worker"}))
    negative("wrong_service", lambda e: e.update({"service_id": "public_action_execution"}))
    negative(
        "stagehand_runtime_without_api_gate",
        lambda e: e.update(
            {"adapter_kind": "stagehand_agent_sdk", "runtime_candidate": "browserbase/stagehand"}
        ),
    )
    negative("signed_in_session", lambda e: e.update({"session_mode": "signed_in_named_scope"}))
    negative("approved_runtime_mode", lambda e: e.update({"execution_mode": "approved_read_only_browser_session"}))
    negative("unbounded_navigation", lambda e: e.update({"navigation_scope": "unbounded"}))
    negative("wildcard_domain", lambda e: e.update({"allowed_domains": ["*"]}))
    negative("target_outside_allowlist", lambda e: e.update({"target_urls": ["https://example.com/not-allowed"]}))
    negative("non_https_target", lambda e: e.update({"target_urls": ["http://github.com/topics/bounty"]}))
    negative("missing_screenshot_artifact", lambda e: e["required_artifacts"].pop("screenshot_dir"))
    negative(
        "artifact_outside_lab",
        lambda e: e["required_artifacts"].update({"capture_log_path": r"C:\temp\capture.json"}),
    )
    negative("missing_kill_switch", lambda e: e["lifecycle"].update({"kill_switch_required": False}))
    negative("positive_session_duration", lambda e: e["lifecycle"].update({"max_session_minutes": 15}))
    negative("browser_start_allowed", lambda e: e.update({"browser_session_start_allowed": True}))
    negative("worker_start_allowed", lambda e: e.update({"worker_start_allowed": True}))
    negative("allowed_login", lambda e: e["allowed_action_classes"].append("login"))
    negative("allowed_form_submit", lambda e: e["allowed_action_classes"].append("submit_form"))
    negative("allowed_public_action", lambda e: e["allowed_action_classes"].append("post_comment"))
    negative("allowed_wallet", lambda e: e["allowed_action_classes"].append("connect_or_sign_wallet"))
    negative("allowed_browser_code", lambda e: e["allowed_action_classes"].append("execute_arbitrary_browser_code"))
    negative("missing_denied_class", lambda e: e["denied_action_classes"].remove("credential_or_secret_access"))
    negative("browser_started", lambda e: e["runtime_boundary"].update({"browser_sessions_started": 1}))
    negative("worker_started", lambda e: e["runtime_boundary"].update({"workers_started": 1}))
    negative("mcp_started", lambda e: e["runtime_boundary"].update({"mcp_servers_started": 1}))
    negative("external_side_effect", lambda e: e["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_contract(
    entry: dict[str, Any],
    schema: dict[str, Any],
    requests: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []

    adapter_enum = schema.get("properties", {}).get("adapter_kind", {}).get("enum", [])
    if not adapter_enum or adapter_enum[0] != "playwright_deterministic":
        errors.append("schema_adapter_kind_must_start_playwright_deterministic")
    if entry.get("service_id") != SERVICE_ID:
        errors.append("service_id_must_be_browser_read_only_session")
    if entry.get("request_type") != REQUEST_TYPE:
        errors.append("request_type_must_be_browser_research")
    if entry.get("adapter_kind") != "playwright_deterministic":
        errors.append("only_playwright_deterministic_allowed_for_contract_v1")
    if entry.get("runtime_candidate") != "microsoft/playwright":
        errors.append("runtime_candidate_must_be_microsoft_playwright")
    if entry.get("execution_mode") != "report_only_contract":
        errors.append("execution_mode_must_be_report_only_contract")
    if entry.get("session_mode") != "public_read_only_no_login":
        errors.append("session_mode_must_be_public_read_only_no_login")
    if entry.get("navigation_scope") != "explicit_allowlist_only":
        errors.append("navigation_scope_must_be_explicit_allowlist_only")
    if entry.get("browser_session_start_allowed") is not False:
        errors.append("browser_session_start_allowed_must_be_false")
    if entry.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")

    request = requests.get(str(entry.get("request_id", "")))
    if not request:
        errors.append("service_request_not_found")
    else:
        if request.get("service_id") != SERVICE_ID:
            errors.append("service_request_service_id_mismatch")
        if request.get("status") != "needs_review":
            errors.append("service_request_must_remain_needs_review")
        if request.get("risk_gate") != "catalog_required_approval_no_external_action":
            errors.append("service_request_must_still_block_external_action")
        if request.get("lane_id") != entry.get("lane_id"):
            errors.append("service_request_lane_mismatch")

    domains = entry.get("allowed_domains", [])
    if not isinstance(domains, list) or not domains:
        errors.append("allowed_domains_must_be_nonempty")
        domains = []
    if any("*" in str(domain) for domain in domains):
        errors.append("allowed_domains_must_not_use_wildcards")
    normalized_domains = {str(domain).lower() for domain in domains}

    urls = entry.get("target_urls", [])
    if not isinstance(urls, list) or not urls:
        errors.append("target_urls_must_be_nonempty")
        urls = []
    for url in urls:
        if not isinstance(url, str) or not url.startswith("https://"):
            errors.append("target_urls_must_be_https")
            continue
        host = hostname(url)
        if host not in normalized_domains and not any(host.endswith("." + domain) for domain in normalized_domains):
            errors.append("target_url_host_must_be_in_allowed_domains")
            break

    allowed = set(str(action) for action in entry.get("allowed_action_classes", []))
    denied = set(str(action) for action in entry.get("denied_action_classes", []))
    if set(ALLOWED_ACTION_CLASSES) - allowed:
        errors.append("allowed_action_classes_missing_required_read_only_actions")
    if set(DENIED_ACTION_CLASSES) - denied:
        errors.append("denied_action_classes_missing_required_denials")
    for action in allowed:
        for boundary_key, tokens in PROHIBITED_ALLOWED_CLASSES.items():
            if action in tokens:
                errors.append(f"allowed_action_classes_include_prohibited_{boundary_key}")
                break

    artifacts = entry.get("required_artifacts", {})
    required_artifact_keys = {"capture_log_path", "evidence_markdown_path", "screenshot_dir", "trace_metadata_path"}
    if not isinstance(artifacts, dict):
        errors.append("required_artifacts_must_be_object")
        artifacts = {}
    missing_artifacts = required_artifact_keys - set(artifacts)
    if missing_artifacts:
        errors.append("required_artifacts_missing_paths")
    for key in required_artifact_keys & set(artifacts):
        if not path_inside_root(str(artifacts[key])):
            errors.append(f"required_artifacts_{key}_must_stay_inside_lab")

    lifecycle = entry.get("lifecycle", {})
    if not isinstance(lifecycle, dict):
        errors.append("lifecycle_must_be_object")
        lifecycle = {}
    for key in [
        "preflight_required",
        "teardown_required",
        "manual_approval_required_before_start",
        "kill_switch_required",
    ]:
        if lifecycle.get(key) is not True:
            errors.append(f"lifecycle_{key}_must_be_true")
    if lifecycle.get("max_session_minutes") != 0:
        errors.append("lifecycle_max_session_minutes_must_be_zero_until_approval")

    egress_trace = entry.get("egress_trace", {})
    if not isinstance(egress_trace, dict) or not egress_trace.get("trace_id") or not egress_trace.get("artifact_path"):
        errors.append("egress_trace_must_include_trace_id_and_artifact_path")

    errors.extend(collect_runtime_boundary_errors(entry, ZERO_BOUNDARY))

    accepted = not errors
    return {
        "adapter_contract_id": entry.get("adapter_contract_id"),
        "request_id": entry.get("request_id"),
        "adapter_kind": entry.get("adapter_kind"),
        "accepted_for_adapter_contract": accepted,
        "rejected": not accepted,
        "errors": errors,
        "contract_verdict": (
            "adapter_contract_valid_start_blocked" if accepted else "rejected_adapter_contract_violation"
        ),
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    requests = request_index()
    results = []
    failures: list[str] = []
    for fixture in fixtures:
        entry = copy.deepcopy(fixture["entry"]) if "entry" in fixture else load_json(Path(fixture["path"]))
        result = validate_contract(entry, schema, requests)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_adapter_contract"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_adapter_contract"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.browser_worker_adapter_contract_report.v1",
        "generated_utc": generated,
        "trace_id": TRACE_ID,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "contract_verdict": "adapter_contract_valid_start_blocked",
        "browser_session_start_allowed": False,
        "worker_start_allowed": False,
        "positive_fixture": {
            "request_id": POSITIVE_REQUEST_ID,
            "adapter_kind": "playwright_deterministic",
            "runtime_candidate": "microsoft/playwright",
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
        "next_action": (
            "Wire this contract into browser read-only assignment preflight before any "
            "approved Playwright, Stagehand, Browser Use, MCP, or browser CLI runtime "
            "can start."
        ),
    }
    validation = {
        "schema_version": "agent_company.browser_worker_adapter_contract_validation.v1",
        "generated_utc": generated,
        "validator_report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "contract_verdict": report["contract_verdict"],
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


def build_trace_metadata(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "agent_company.trace_metadata.v1",
        "generated_utc": validation["generated_utc"],
        "trace_id": TRACE_ID,
        "span_kind": "internal",
        "runtime": "codex_local_report_only",
        "api_calls": False,
        "browser_actions": False,
        "external_side_effects": False,
        "lane_id": "platform_engineering",
        "task_id": "task-browser-worker-adapter-contract-v1-20260618",
        "artifact_slug": "browser-worker-adapter-contract-v1-20260618",
        "fixture_count": validation["fixture_count"],
        "accepted_count": validation["accepted_count"],
        "rejected_count": validation["rejected_count"],
        "contract_verdict": validation["contract_verdict"],
    }


