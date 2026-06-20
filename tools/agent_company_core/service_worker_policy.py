from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Core service-worker request synthesis, approval lookup, and readiness reporting."""

from .constants import (
    SERVICE_WORKER_READINESS_JSON,
    SERVICE_WORKER_READINESS_REPORT,
    SERVICE_WORKER_READINESS_VALIDATION_JSON,
)
from .io import load_json, now_utc, parse_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import md_cell


SERVICE_WORKER_REQUIRED_FIELDS = [
    "schema_version",
    "worker_request_id",
    "source_service_request_id",
    "requesting_lane_id",
    "requesting_agent_id",
    "worker_type",
    "service_id",
    "risk_gate",
    "approval_status_snapshot",
    "approval_scope",
    "created_utc",
    "objective",
    "allowed_actions",
    "prohibited_actions",
    "stop_conditions",
    "credential_boundary",
    "account_boundary",
    "money_boundary",
    "public_action_boundary",
    "data_boundary",
    "external_side_effects_allowed",
    "real_money_allowed",
    "public_action_allowed",
    "account_or_identity_action_allowed",
    "model_or_api_cost_allowed",
    "max_cost_usd",
    "input_artifacts",
    "expected_output_artifacts",
    "execution_plan_path",
    "result_artifact_path",
    "replay_policy",
    "status",
    "metadata",
]


SERVICE_WORKER_TYPES = {
    "browser_read_only",
    "browser_signed_in_read_only",
    "account_registration",
    "wallet_operation",
    "legal_kyc_tax_payment_review",
    "public_submission",
    "model_api_execution",
    "data_ingestion",
    "local_runtime_adapter",
    "other_gated_worker",
}


def service_worker_type_for_request(row: dict[str, Any]) -> str:
    service_id = row.get("service_id") or ""
    request_type = row.get("request_type") or ""
    risk_gate = row.get("risk_gate") or ""
    if service_id == "browser_read_only_session" and request_type == "browser_research":
        return "browser_read_only"
    if "signed_in_browser" in risk_gate or "grok_or_x" in risk_gate:
        return "browser_signed_in_read_only"
    if service_id == "legal_kyc_tax_payment_gate" or request_type == "legal_kyc_tax_payment":
        return "legal_kyc_tax_payment_review"
    if service_id == "security_report_submission_gate" or request_type == "security_report_submission":
        return "public_submission"
    if request_type == "model_api_execution":
        return "model_api_execution"
    if request_type == "lifecycle_test":
        return "local_runtime_adapter"
    return "other_gated_worker"


def service_worker_objective(row: dict[str, Any], worker_type: str) -> str:
    request_id = row["request_id"]
    if worker_type == "browser_read_only":
        return (
            f"After explicit approval only, run a public read-only browser worker for {request_id}; "
            "capture evidence and stop before login, form submission, account, public, payment, wallet, "
            "or real-money action."
        )
    if worker_type == "browser_signed_in_read_only":
        return (
            f"After explicit approval only, run a signed-in read-only research worker for {request_id}; "
            "capture local research notes and perform no public X/Grok action, account setting change, "
            "message, post, or reply."
        )
    if worker_type == "legal_kyc_tax_payment_review":
        return (
            f"Review legal, KYC, tax, payment, and seller-account requirements for {request_id} as a local "
            "decision packet only; make no commitments and enter no private data."
        )
    if worker_type == "public_submission":
        return (
            f"Prepare or review a submission route for {request_id} as a local packet only; do not submit, "
            "comment, message, publish, or contact anyone."
        )
    if worker_type == "model_api_execution":
        return (
            f"Review cost-bearing model/API execution request {request_id}; do not call external providers "
            "until provider, model, max cost, and artifact scope are explicitly approved."
        )
    if worker_type == "local_runtime_adapter":
        return f"Represent lifecycle/local-runtime test request {request_id}; no external service worker action is needed."
    return f"Represent gated service request {request_id} as a local service-worker queue row only; do not execute external side effects."


def service_worker_allowed_actions(row: dict[str, Any], worker_type: str) -> list[str]:
    if row["status"] in {"rejected", "complete"}:
        return ["retain local audit record", "do not execute or reopen without a new service request"]
    if worker_type == "browser_read_only":
        return [
            "read public allowed pages after approval",
            "capture source URLs, page titles, short compliant excerpts, summaries, and local evidence artifacts",
            "stop at login, account, payment, public action, or private-data boundaries",
        ]
    if worker_type == "browser_signed_in_read_only":
        return [
            "after explicit approval, inspect approved signed-in research surface in read-only mode",
            "capture local notes and source references",
            "avoid likes, follows, replies, posts, settings, messages, and account changes",
        ]
    if worker_type == "legal_kyc_tax_payment_review":
        return [
            "prepare local review notes",
            "identify required legal, tax, KYC, payment, seller, and contractual decisions",
            "produce questions for the user/CRO",
        ]
    if worker_type == "public_submission":
        return [
            "prepare local submission route review",
            "check required approvals and private/public route constraints",
            "draft next approval questions only",
        ]
    if worker_type == "model_api_execution":
        return [
            "prepare local cost/scope review",
            "identify provider, model, max cost, input/output artifact scope, and data sensitivity",
            "wait for explicit approval before any API call",
        ]
    if worker_type == "local_runtime_adapter":
        return ["retain test/audit evidence", "summarize lifecycle result"]
    return ["prepare local gate review", "identify missing approval and risk boundaries"]


def service_worker_stop_conditions(row: dict[str, Any], worker_type: str) -> list[str]:
    stops = [
        "service request status is not approved or assigned",
        "requested action exceeds approval scope",
        "required artifact/source is missing or ambiguous",
    ]
    if worker_type.startswith("browser"):
        stops.extend(
            [
                "page requires unapproved login, signup, consent, payment, private data, credentials, OTP, wallet action, file upload, or public submission",
                "worker would need to leave allowed host/scope",
            ]
        )
    if worker_type == "model_api_execution":
        stops.append("provider, model, max cost, data scope, or output artifact path is not approved")
    if worker_type in {"legal_kyc_tax_payment_review", "public_submission"}:
        stops.append("work would create a commitment, public action, account action, payment setup, report submission, or contact")
    return stops


def service_worker_boundaries(worker_type: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    credentials = {
        "credentials_allowed": False,
        "otp_allowed": False,
        "private_data_allowed": False,
        "notes": "No credentials, OTPs, private files, secrets, payment details, tax/KYC data, wallet data, or personal/private data may be entered.",
    }
    account = {
        "login_allowed": False,
        "signup_allowed": False,
        "settings_change_allowed": False,
        "terms_acceptance_allowed": False,
        "notes": "No login, signup, account setting change, seller onboarding, or terms acceptance is allowed by this queue row.",
    }
    if worker_type == "browser_signed_in_read_only":
        account["notes"] = "Signed-in read-only research would require separate explicit approval; this queue row grants none."
    money = {
        "payment_method_allowed": False,
        "purchase_allowed": False,
        "deposit_allowed": False,
        "withdrawal_allowed": False,
        "trade_allowed": False,
        "wallet_signature_allowed": False,
        "notes": "No payment, trading, deposit, withdrawal, wallet signature, purchase, or real-money action is allowed by this queue row.",
    }
    public = {
        "post_allowed": False,
        "comment_allowed": False,
        "message_allowed": False,
        "issue_or_pr_allowed": False,
        "marketplace_listing_allowed": False,
        "submission_allowed": False,
        "notes": "No public action, external message, marketplace listing, upload, issue/PR action, or submission is allowed by this queue row.",
    }
    return credentials, account, money, public


def service_worker_data_boundary(worker_type: str) -> dict[str, Any]:
    allowed_hosts: list[str] = []
    starting_urls: list[str] = []
    if worker_type == "browser_read_only":
        allowed_hosts = ["scope_defined_in_source_packet"]
        starting_urls = ["scope_defined_in_source_packet"]
    elif worker_type == "browser_signed_in_read_only":
        allowed_hosts = ["x.com", "grok.com", "scope_defined_in_source_packet"]
        starting_urls = ["approved_signed_in_research_surface_required_before_execution"]
    return {
        "allowed_hosts": allowed_hosts,
        "starting_urls": starting_urls,
        "allowed_data_types": [
            "local artifact references",
            "public source URLs",
            "page titles",
            "short factual excerpts within copyright limits",
            "local notes",
            "approval and risk metadata",
        ],
        "disallowed_data_types": [
            "credentials",
            "OTP",
            "payment details",
            "tax/KYC data",
            "wallet data",
            "private files",
            "non-public account data",
            "unapproved signed-in content",
        ],
    }


def service_worker_expected_output(row: dict[str, Any], worker_type: str) -> dict[str, Any]:
    kind_by_type = {
        "browser_read_only": "browser_readonly_capture",
        "browser_signed_in_read_only": "signed_in_readonly_research_capture",
        "legal_kyc_tax_payment_review": "legal_payment_review_packet",
        "public_submission": "submission_route_review_packet",
        "model_api_execution": "model_api_scope_review_packet",
        "local_runtime_adapter": "lifecycle_audit_note",
    }
    return {
        "kind": kind_by_type.get(worker_type, "service_worker_result_placeholder"),
        "path": str(REPORTS_DIR / "service-worker-requests" / f"{row['request_id']}-result-placeholder.md"),
        "required": row["status"] not in {"rejected", "complete"},
    }
