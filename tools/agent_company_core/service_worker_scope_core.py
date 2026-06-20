from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

"""Scope-diff, scope-template, and approval-review reporting for service workers."""

from .constants import (
    SERVICE_WORKER_APPROVAL_REVIEW_JSON,
    SERVICE_WORKER_APPROVAL_REVIEW_REPORT,
    SERVICE_WORKER_APPROVAL_REVIEW_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_DIFF_JSON,
    SERVICE_WORKER_SCOPE_DIFF_REPORT,
    SERVICE_WORKER_SCOPE_DIFF_VALIDATION_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_JSON,
    SERVICE_WORKER_SCOPE_TEMPLATE_REPORT,
    SERVICE_WORKER_SCOPE_TEMPLATE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import compact_text, md_cell
from .service_worker_core import (
    approval_not_expired,
    latest_approval_for_request,
    service_worker_packet_path,
    synthesize_service_worker_request,
    validate_service_worker_request_object,
)


SIDE_EFFECT_SCOPE_RULES = [
    {
        "key": "credential_boundary",
        "packet_flag": None,
        "required_denial_terms": ["credential", "credentials", "otp", "private data", "private files", "secrets"],
        "conflict_terms": ["enter credentials", "use credentials", "otp", "password", "private data", "private file", "secret"],
    },
    {
        "key": "account_boundary",
        "packet_flag": "account_or_identity_action_allowed",
        "required_denial_terms": ["login", "signup", "account", "settings", "terms acceptance"],
        "conflict_terms": ["login", "log in", "sign in", "signup", "sign up", "create account", "settings", "accept terms"],
    },
    {
        "key": "money_boundary",
        "packet_flag": "real_money_allowed",
        "required_denial_terms": ["payment", "wallet", "purchase", "deposit", "withdraw", "trade", "real money"],
        "conflict_terms": ["payment", "wallet", "purchase", "deposit", "withdraw", "trade", "buy", "sell", "real money"],
    },
    {
        "key": "public_action_boundary",
        "packet_flag": "public_action_allowed",
        "required_denial_terms": ["post", "comment", "message", "submit", "publish", "listing", "upload", "public action"],
        "conflict_terms": ["post", "comment", "message", "submit", "publish", "listing", "upload", "reply", "contact"],
    },
    {
        "key": "model_or_api_cost",
        "packet_flag": "model_or_api_cost_allowed",
        "required_denial_terms": ["api", "model", "cost", "provider"],
        "conflict_terms": ["api call", "model call", "provider", "paid api", "cost"],
    },
    {
        "key": "external_side_effects",
        "packet_flag": "external_side_effects_allowed",
        "required_denial_terms": ["external action", "external side effect", "no side effect"],
        "conflict_terms": ["external action", "side effect", "start worker", "execute worker"],
    },
]


NEGATION_MARKERS = ["no", "not", "never", "without", "do not", "don't", "cannot", "may not", "must not"]


def normalized_scope_text(*values: str | None) -> str:
    return " ".join(" ".join((value or "").lower().replace("_", " ").split()) for value in values if value)


def term_present_with_negation_awareness(text: str, term: str) -> tuple[bool, bool]:
    term = term.lower()
    index = text.find(term)
    if index < 0:
        return False, False
    start = max(0, index - 40)
    prefix = text[start:index]
    negated = any(marker in prefix.split()[-8:] for marker in NEGATION_MARKERS)
    if not negated:
        negated = any(marker in prefix for marker in ["do not", "may not", "must not"])
    return True, negated


def denial_present(text: str, terms: list[str]) -> bool:
    for term in terms:
        present, negated = term_present_with_negation_awareness(text, term)
        if present and negated:
            return True
    return False


def positive_conflicts(text: str, terms: list[str]) -> list[str]:
    conflicts: list[str] = []
    for term in terms:
        present, negated = term_present_with_negation_awareness(text, term)
        if present and not negated:
            conflicts.append(term)
    return conflicts


def concrete_hosts_from_packet(packet: dict[str, Any]) -> list[str]:
    hosts = []
    for host in packet.get("data_boundary", {}).get("allowed_hosts", []):
        if host and not str(host).startswith("scope_defined") and "required" not in str(host):
            hosts.append(str(host).lower())
    return hosts


def host_scope_mentions(text: str, hosts: list[str]) -> dict[str, bool]:
    mentions: dict[str, bool] = {}
    for host in hosts:
        bare = host.removeprefix("www.")
        mentions[host] = host in text or bare in text
    return mentions

def compact_sequence(values: list[Any] | tuple[Any, ...] | None, fallback: str) -> list[str]:
    items = [compact_text(str(value), 300) or "" for value in (values or [])]
    items = [item for item in items if item]
    return items or [fallback]


def scope_template_output_paths(packet: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for item in packet.get("expected_output_artifacts", []):
        if isinstance(item, dict) and item.get("path"):
            paths.append(str(item["path"]))
    if packet.get("result_artifact_path"):
        paths.append(str(packet["result_artifact_path"]))
    deduped: list[str] = []
    for path in paths:
        if path not in deduped:
            deduped.append(path)
    return compact_sequence(deduped, "required result artifact path from the packet")


def scope_template_hosts(packet: dict[str, Any]) -> list[str]:
    boundary = packet.get("data_boundary", {})
    if not isinstance(boundary, dict):
        return ["scope defined in the source packet"]
    return compact_sequence(boundary.get("allowed_hosts", []), "scope defined in the source packet")


def scope_template_starting_urls(packet: dict[str, Any]) -> list[str]:
    boundary = packet.get("data_boundary", {})
    if not isinstance(boundary, dict):
        return ["scope defined in the source packet"]
    return compact_sequence(boundary.get("starting_urls", []), "scope defined in the source packet")


def scope_template_allowed_data(packet: dict[str, Any]) -> list[str]:
    boundary = packet.get("data_boundary", {})
    if not isinstance(boundary, dict):
        return ["only public or local data named in the packet"]
    return compact_sequence(boundary.get("allowed_data_types", []), "only public or local data named in the packet")


def scope_template_required_denials(packet: dict[str, Any]) -> list[str]:
    denials = [
        "no credentials, OTPs, secrets, private files, private data, payment details, tax/KYC data, or wallet data",
        "no login, signup, account creation, account settings changes, or terms/legal acceptance",
        "no payments, purchases, deposits, withdrawals, trades, wallet connections, wallet signatures, or real-money action",
        "no public posts, comments, replies, messages, listings, uploads, form submissions, issue/PR actions, or external contact",
        "no external side effects, API/provider/model calls, paid cost, worker start, or queue mutation unless separately approved in an exact scope",
        "no bypassing paywalls, rate limits, access controls, platform rules, or the packet stop conditions",
    ]
    for action in packet.get("prohibited_actions", []):
        text = compact_text(str(action), 220)
        if text and text.lower() not in {item.lower() for item in denials}:
            denials.append(text)
    return denials


def join_scope_items(label: str, values: list[str]) -> str:
    return f"{label}: " + "; ".join(values)

