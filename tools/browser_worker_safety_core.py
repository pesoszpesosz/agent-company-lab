#!/usr/bin/env python3
"""Validate browser-worker safety fixture classifications locally."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = ROOT / "reports" / "browser-worker-safety-fixture-v1-20260617.json"
DEFAULT_JSON_OUT = ROOT / "reports" / "browser-worker-safety-validation-20260617.json"
DEFAULT_MD_OUT = ROOT / "reports" / "browser-worker-safety-fixture-v1-20260617.md"
DEFAULT_SCHEMA = ROOT / "architecture" / "browser-worker-safety-fixture-v1.schema.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def has_any(text: str, terms: list[str]) -> bool:
    low = text.lower()
    return any(term.lower() in low for term in terms)


def has_positive_action(text: str, terms: list[str]) -> bool:
    low = text.lower()
    for term in terms:
        term_low = term.lower()
        idx = low.find(term_low)
        while idx != -1:
            prefix = low[max(0, idx - 12) : idx]
            if "do not " not in prefix and "don't " not in prefix and "without " not in prefix:
                return True
            idx = low.find(term_low, idx + 1)
    return False


def classify(case: dict[str, Any]) -> tuple[str, str, str | None, list[str]]:
    text = f"{case['action_text']} {case['target_url']}".lower()
    session = case["session_sensitivity"]
    prohibited = {"service_request_mutation"}

    wallet_terms = [
        "connect wallet",
        "sign message",
        "claim airdrop",
        "withdraw",
        "deposit",
        "payment method",
        "buy",
        "trade",
    ]
    if has_any(text, wallet_terms):
        prohibited.update(["wallet_action", "payment_action", "public_action", "real_money_action"])
        return "wallet_or_payment_action", "prohibit", "wallet_setup_packet", sorted(prohibited)

    if has_any(text, ["exploit", "live proof-of-concept", "run a live", "submit a vulnerability report"]):
        prohibited.update(["security_testing", "public_action", "account_action"])
        return "security_sensitive_action", "prohibit", "security_report_submission_gate", sorted(prohibited)

    if has_any(text, ["api key", "provider console", "model api", "model-backed", "paste it into the worker"]):
        prohibited.update(["model_api_call", "account_action"])
        return "model_or_api_action", "prohibit", "model_api_execution_gate", sorted(prohibited)

    if session == "signed_in_named_scope" and "read-only" in text:
        prohibited.update(["public_action", "account_action", "payment_action"])
        return "signed_in_read_only", "needs_human_cro_review", "browser_signed_in_read_only", sorted(prohibited)

    public_action_terms = [
        "submit a proposal",
        "comment on issue",
        "claim the bounty",
        "publish",
        "reply",
        "follow",
        "like",
        "repost",
        "open pull request",
    ]
    if has_positive_action(text, public_action_terms):
        prohibited.update(["public_action", "account_action", "payment_action"])
        if "github.com" in text or "issue" in text or "bounty" in text:
            return "public_action", "block_until_separate_gate", "github_public_action_gate", sorted(prohibited)
        return "public_action", "block_until_separate_gate", "outreach_delivery_gate", sorted(prohibited)

    account_terms = [
        "create account",
        "accept terms",
        "register for",
        "save settings",
        "edit profile",
        "publish profile",
    ]
    if has_positive_action(text, account_terms):
        prohibited.update(["account_action", "public_action", "payment_action"])
        return (
            "account_or_profile_action",
            "block_until_separate_gate",
            "account_registration_intake",
            sorted(prohibited),
        )

    if session == "signed_in_named_scope":
        prohibited.update(["public_action", "account_action", "payment_action"])
        return "signed_in_read_only", "needs_human_cro_review", "browser_signed_in_read_only", sorted(prohibited)

    if session == "public" and has_any(text, ["read", "capture", "visible", "public"]):
        prohibited.update(["account_action", "payment_action", "public_action"])
        if "vrp" in text or "security" in case["lane_id"]:
            prohibited.add("security_testing")
        return "public_read_only", "allow_after_approval", "browser_read_only_session", sorted(prohibited)

    prohibited.update(["browser_session", "account_action", "payment_action", "public_action"])
    return "prohibited", "prohibit", None, sorted(prohibited)


def validate_case(case: dict[str, Any]) -> dict[str, Any]:
    actual_classification, decision, gate, prohibited = classify(case)
    failures: list[str] = []
    if case.get("external_side_effects") is not False:
        failures.append("case external_side_effects must be false")
    if actual_classification != case["expected_classification"]:
        failures.append(f"classification expected {case['expected_classification']}, got {actual_classification}")
    if decision != case["expected_decision"]:
        failures.append(f"decision expected {case['expected_decision']}, got {decision}")
    if gate != case["expected_required_gate"]:
        failures.append(f"required gate expected {case['expected_required_gate']}, got {gate}")
    missing_prohibited = sorted(set(case["expected_prohibited_actions"]) - set(prohibited))
    if missing_prohibited:
        failures.append(f"missing prohibited actions: {', '.join(missing_prohibited)}")
    return {
        "case_id": case["case_id"],
        "lane_id": case["lane_id"],
        "request_id": case["request_id"],
        "actual_classification": actual_classification,
        "actual_decision": decision,
        "actual_required_gate": gate,
        "actual_prohibited_actions": prohibited,
        "failures": failures,
    }




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
) -> dict[str, Any]:
    rows = [validate_case(case) for case in fixture["cases"]]
    failed_count = sum(1 for row in rows if row["failures"])
    return {
        "schema_version": "agent_company.browser_worker_safety_validation.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "cases_checked": len(rows),
        "passed_count": len(rows) - failed_count,
        "failed_count": failed_count,
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "model_api_calls": False,
        "service_requests_updated": 0,
        "worker_starts": 0,
        "external_side_effects": False,
        "rows": rows,
    }
