#!/usr/bin/env python3
"""Validate Temporal signal payload shapes without importing Temporal or sending messages."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = (
    ROOT / "reports" / "durable-orchestration" / "temporal-signal-shape-fixture-v1-20260617.json"
)
DEFAULT_SCHEMA = ROOT / "architecture" / "temporal-signal-shape-fixture-v1.schema.json"
DEFAULT_JSON_OUT = (
    ROOT
    / "reports"
    / "durable-orchestration"
    / "temporal-signal-shape-fixture-v1-validation-20260617.json"
)
DEFAULT_MD_OUT = (
    ROOT / "reports" / "durable-orchestration" / "temporal-signal-shape-fixture-v1-20260617.md"
)

ALLOWED_DISPOSITIONS = {
    "approve_after_manual_review",
    "reject_after_manual_review",
    "notice_only",
}

PUBLIC_ACTION_TOKENS = [
    "comment",
    "post",
    "publish",
    "submit",
    "reply",
    "message",
    "claim",
    "apply",
    "create_account",
    "connect_wallet",
    "pay",
    "trade",
]

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "temporal_client_connections": 0,
    "temporal_server_started": False,
    "temporal_workers_started": 0,
    "temporal_workflows_started": 0,
    "temporal_signals_sent": 0,
    "temporal_queries_executed": 0,
    "temporal_updates_sent": 0,
    "temporal_activities_scheduled": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_case(case: dict[str, Any], fixture: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    payload = case.get("payload") or {}
    allowed_signal_names = set(fixture["allowed_signal_names"])
    required_payload_fields = set(fixture["required_payload_fields"])
    forbidden_payload_fields = set(fixture["forbidden_payload_fields"])

    if case.get("signal_name") not in allowed_signal_names:
        failures.append("signal_name_not_allowed")
    missing = sorted(required_payload_fields - set(payload))
    for field in missing:
        failures.append(f"required_payload_field_missing:{field}")
    for field in sorted(forbidden_payload_fields & set(payload)):
        failures.append(f"forbidden_payload_field_present:{field}")

    if payload.get("request_id") != case.get("request_id"):
        failures.append("payload_request_id_mismatch")
    if payload.get("status_snapshot") != case.get("status_snapshot"):
        failures.append("payload_status_snapshot_mismatch")
    signal_id = str(payload.get("signal_id", ""))
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{8,160}", signal_id):
        failures.append("signal_id_not_stable_slug")
    idempotency_key = str(payload.get("idempotency_key", ""))
    if case.get("request_id") not in idempotency_key or case.get("signal_name") not in idempotency_key:
        failures.append("idempotency_key_missing_request_or_signal")

    disposition = str(payload.get("requested_disposition", ""))
    if disposition not in ALLOWED_DISPOSITIONS:
        failures.append("requested_disposition_not_allowed")
    lowered_disposition = disposition.lower()
    if any(token in lowered_disposition for token in PUBLIC_ACTION_TOKENS):
        failures.append("public_action_requires_separate_gate")

    authority_route = payload.get("authority_route")
    if not isinstance(authority_route, list) or not all(isinstance(item, str) for item in authority_route):
        failures.append("authority_route_must_be_string_list")
    else:
        if case.get("status_snapshot") == "needs_review" and not (
            "human_user" in authority_route and "chief_risk_officer" in authority_route
        ):
            failures.append("authority_route_missing_required_human_or_cro")
        if case.get("status_snapshot") in {"complete", "rejected"} and disposition != "notice_only":
            failures.append("terminal_signal_must_be_notice_only")

    scope_hash = str(payload.get("scope_hash", ""))
    if not scope_hash.startswith("sha256:"):
        failures.append("scope_hash_must_be_sha256_prefixed")

    allowed_after_signal = payload.get("allowed_after_signal", [])
    disallowed_after_signal = payload.get("disallowed_after_signal", [])
    if case.get("status_snapshot") == "needs_review" and case.get("expected_shape_valid"):
        if not isinstance(allowed_after_signal, list) or "refresh local decision packets" not in allowed_after_signal:
            failures.append("valid_needs_review_signal_must_only_refresh_local_packets")
        if not isinstance(disallowed_after_signal, list) or "start worker" not in disallowed_after_signal:
            failures.append("valid_needs_review_signal_must_disallow_worker_start")

    return sorted(set(failures))


def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
    reducer_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.temporal_signal_shape_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-temporal-signal-shape-fixture-v1-20260617":
        top_failures.append("task_id mismatch")

    runtime_boundary = fixture.get("runtime_boundary") or {}
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if runtime_boundary.get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    source_reducer_path = Path(fixture.get("source_reducer_fixture_path", ""))
    if not source_reducer_path.exists():
        top_failures.append("source reducer fixture path is missing")
    else:
        if reducer_doc is None:
            reducer_doc = load_json(source_reducer_path)
        if reducer_doc.get("next_local_test") != "temporal_signal_shape_fixture_against_service_worker_request_v1":
            top_failures.append("source reducer fixture does not point to this Temporal signal-shape test")

    rows = []
    for case in fixture.get("signal_cases", []):
        actual_failures = validate_case(case, fixture)
        expected_failures = sorted(case.get("expected_failures") or [])
        actual_shape_valid = not actual_failures
        matches_expected = (
            actual_shape_valid == case.get("expected_shape_valid")
            and sorted(actual_failures) == expected_failures
        )
        rows.append(
            {
                "case_id": case.get("case_id"),
                "request_id": case.get("request_id"),
                "status_snapshot": case.get("status_snapshot"),
                "signal_name": case.get("signal_name"),
                "actual_shape_valid": actual_shape_valid,
                "expected_shape_valid": case.get("expected_shape_valid"),
                "expected_disposition": case.get("expected_disposition"),
                "expected_reducer_state": case.get("expected_reducer_state"),
                "actual_failures": actual_failures,
                "expected_failures": expected_failures,
                "matches_expected": matches_expected,
            }
        )

    failed_rows = [row for row in rows if not row["matches_expected"]]
    failed_count = len(failed_rows) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.temporal_signal_shape_fixture_validation.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "cases_checked": len(rows),
        "passed_count": len(rows) - len(failed_rows),
        "failed_count": failed_count,
        "top_level_failures": top_failures,
        "runtime_boundary": runtime_boundary,
        "rows": rows,
        "next_local_test": fixture.get("next_local_test"),
    }
