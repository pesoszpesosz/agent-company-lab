#!/usr/bin/env python3
"""Validate Restate agent-service boundary fixtures without importing Restate."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DURABLE_REPORTS = ROOT / "reports" / "durable-orchestration"
DEFAULT_FIXTURE = DURABLE_REPORTS / "restate-agent-service-boundary-fixture-v1-20260617.json"
DEFAULT_SCHEMA = ROOT / "architecture" / "restate-agent-service-boundary-fixture-v1.schema.json"
DEFAULT_JSON_OUT = DURABLE_REPORTS / "restate-agent-service-boundary-fixture-v1-validation-20260617.json"
DEFAULT_MD_OUT = DURABLE_REPORTS / "restate-agent-service-boundary-fixture-v1-20260617.md"

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "restate_imports": 0,
    "restate_server_starts": 0,
    "services_registered": 0,
    "handlers_invoked": 0,
    "service_calls_or_sends": 0,
    "object_calls_or_sends": 0,
    "workflow_calls_or_sends": 0,
    "journal_writes": 0,
    "state_mutations": 0,
    "llm_calls": 0,
    "tool_executions": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "external_side_effects": False,
}

RESTATE_EDGE_TO_FAILURE = {
    "package_imported": "restate_runtime_edge:package_imported",
    "server_started": "restate_runtime_edge:server_started",
    "service_registered": "restate_runtime_edge:service_registered",
    "handler_invoked": "restate_runtime_edge:handler_invoked",
    "service_call_or_send": "restate_runtime_edge:service_call_or_send",
    "object_call_or_send": "restate_runtime_edge:object_call_or_send",
    "workflow_call_or_send": "restate_runtime_edge:workflow_call_or_send",
    "journal_write": "restate_runtime_edge:journal_write",
    "state_mutation": "restate_runtime_edge:state_mutation",
    "llm_call": "restate_runtime_edge:llm_call",
    "tool_execution": "restate_runtime_edge:tool_execution",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_case(case: dict[str, Any], fixture: dict[str, Any], messages: dict[str, dict[str, Any]]) -> list[str]:
    failures: list[str] = []
    policy = fixture["service_boundary_policy"]
    message = messages.get(str(case.get("source_message_id")))
    if not message:
        failures.append("source_message_missing")
    else:
        parks_for_review = case.get("outbox_disposition") == "park_awaiting_human_review"
        needs_review = message.get("approval_posture") == "needs_human_review"
        if parks_for_review and not needs_review:
            failures.append("park_disposition_requires_human_review_message")
        is_gate_request = message.get("message_type") == "gate_request"
        if is_gate_request and not parks_for_review:
            failures.append("gate_request_must_park")
        if message.get("external_side_effects") is not False:
            failures.append("source_message_has_external_side_effects")

    if case.get("service_shape") not in policy["allowed_service_shapes"]:
        failures.append("service_shape_not_allowed")
    if case.get("outbox_disposition") not in policy["allowed_outbox_dispositions"]:
        failures.append("outbox_disposition_forbidden")

    restate_edges = case.get("restate_edges") or {}
    for edge, failure in RESTATE_EDGE_TO_FAILURE.items():
        if restate_edges.get(edge) is not False:
            failures.append(failure)

    side_effects = case.get("side_effects") or {}
    if side_effects.get("service_request_mutation") is not False:
        failures.append("service_request_mutation_requested")
    if side_effects.get("worker_start") is not False:
        failures.append("worker_start_requested")
    if side_effects.get("browser_session") is not False:
        failures.append("browser_session_requested")
    if side_effects.get("api_call") is not False:
        failures.append("api_call_requested")
    if side_effects.get("model_api_call") is not False:
        failures.append("model_api_call_requested")
    if side_effects.get("public_action") is not False:
        failures.append("public_action_requested")
    if side_effects.get("external_side_effect") is not False:
        failures.append("external_side_effect_requested")

    return sorted(set(failures))




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
    prefect_doc: dict[str, Any] | None = None,
    outbox_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.restate_agent_service_boundary_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-restate-agent-service-boundary-fixture-v1-20260617":
        top_failures.append("task_id mismatch")
    if not schema_path.exists():
        top_failures.append("schema path is missing")

    for source_field in ["source_prefect_validation_path", "source_outbox_history_path"]:
        source_path = Path(fixture.get(source_field, ""))
        if not source_path.exists():
            top_failures.append(f"{source_field} is missing")

    prefect_path = Path(fixture.get("source_prefect_validation_path", ""))
    if prefect_doc is None and prefect_path.exists():
        prefect_doc = load_json(prefect_path)
    if prefect_doc is not None:
        next_test = "restate_agent_service_boundary_fixture_against_central_outbox_history_v1"
        if prefect_doc.get("next_local_test") != next_test:
            top_failures.append("source Prefect validation does not point to this Restate boundary test")
        if prefect_doc.get("failed_count") != 0:
            top_failures.append("source Prefect validation has failures")

    runtime_boundary = fixture.get("runtime_boundary") or {}
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if runtime_boundary.get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    messages: dict[str, dict[str, Any]] = {}
    outbox_path = Path(fixture.get("source_outbox_history_path", ""))
    if outbox_doc is None and outbox_path.exists():
        outbox_doc = load_json(outbox_path)
    if outbox_doc is not None:
        messages = {row["message_id"]: row for row in outbox_doc.get("messages", [])}

    rows = []
    seen_cases: set[str] = set()
    for case in fixture.get("agent_service_cases", []):
        failures = validate_case(case, fixture, messages)
        case_id = str(case.get("case_id"))
        if case_id in seen_cases:
            failures.append("duplicate_case_id")
        seen_cases.add(case_id)
        expected_failures = sorted(case.get("expected_failures") or [])
        matches_expected = sorted(failures) == expected_failures
        rows.append(
            {
                "case_id": case_id,
                "source_message_id": case.get("source_message_id"),
                "service_shape": case.get("service_shape"),
                "outbox_disposition": case.get("outbox_disposition"),
                "expected_decision": case.get("expected_decision"),
                "actual_failures": sorted(failures),
                "expected_failures": expected_failures,
                "matches_expected": matches_expected,
            }
        )

    failed_rows = [row for row in rows if not row["matches_expected"]]
    failed_count = len(failed_rows) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.restate_agent_service_boundary_fixture_validation.v1",
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
