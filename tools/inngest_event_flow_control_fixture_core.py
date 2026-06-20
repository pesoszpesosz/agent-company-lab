#!/usr/bin/env python3
"""Validate Inngest event naming and flow-control fixtures without using Inngest."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DURABLE_REPORTS = ROOT / "reports" / "durable-orchestration"
DEFAULT_FIXTURE = DURABLE_REPORTS / "inngest-event-flow-control-fixture-v1-20260617.json"
DEFAULT_SCHEMA = ROOT / "architecture" / "inngest-event-flow-control-fixture-v1.schema.json"
DEFAULT_JSON_OUT = DURABLE_REPORTS / "inngest-event-flow-control-fixture-v1-validation-20260617.json"
DEFAULT_MD_OUT = DURABLE_REPORTS / "inngest-event-flow-control-fixture-v1-20260617.md"

MESSAGE_TYPE_TO_EVENT = {
    "artifact_notice": "agent_company/outbox.artifact_notice",
    "gate_request": "agent_company/outbox.gate_request",
    "dispatch": "agent_company/outbox.dispatch",
}

ALLOWED_RUNTIME_DISPOSITIONS = {
    "local_preview_only",
    "park_awaiting_human_review",
}

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "inngest_client_created": False,
    "inngest_functions_registered": 0,
    "inngest_events_sent": 0,
    "inngest_step_events_sent": 0,
    "inngest_server_started": False,
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


def validate_event(
    event: dict[str, Any],
    fixture: dict[str, Any],
    outbox_messages: dict[str, dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    event_name = event.get("event_name")
    data = event.get("data") or {}
    flow = event.get("flow_control") or {}
    allowed_event_names = set(fixture["allowed_event_names"])

    if not isinstance(event_name, str) or not re.fullmatch(r"agent_company/[a-z0-9_.-]+", event_name):
        failures.append("event_name_invalid_format")
    if event_name not in allowed_event_names:
        failures.append("event_name_not_allowed")

    source_message_id = event.get("source_message_id")
    source_message = outbox_messages.get(str(source_message_id))
    if not source_message:
        failures.append("source_message_missing")
    else:
        expected_event_name = MESSAGE_TYPE_TO_EVENT.get(source_message.get("message_type"))
        if event_name != expected_event_name:
            failures.append("event_name_not_allowed_for_outbox_message_type")
        mirrored_fields = [
            "message_id",
            "lane_id",
            "recipient_id",
            "recipient_type",
            "message_type",
            "approval_posture",
            "replay_status",
        ]
        for field in mirrored_fields:
            if data.get(field) != source_message.get(field):
                failures.append(f"data_mismatch:{field}")
        if data.get("service_request_id") != source_message.get("service_request_id"):
            failures.append("data_mismatch:service_request_id")

    idempotency_key = str(data.get("idempotency_key", ""))
    idempotency_has_message = data.get("message_id") in idempotency_key
    idempotency_has_event = event_name in idempotency_key
    idempotency_has_replay = data.get("replay_status") in idempotency_key
    if not (idempotency_has_message and idempotency_has_event and idempotency_has_replay):
        failures.append("idempotency_key_missing_message_event_or_replay_status")

    if flow.get("concurrency_key") != data.get("lane_id"):
        failures.append("concurrency_key_must_equal_lane_id")
    if flow.get("throttle_key") != data.get("recipient_id"):
        failures.append("throttle_key_must_equal_recipient_id")
    expected_rate_key = data.get("service_request_id") or "none"
    if flow.get("rate_limit_key") != expected_rate_key:
        failures.append("rate_limit_key_must_equal_service_request_id_or_none")

    if data.get("approval_posture") == "needs_human_review" and flow.get("skip_allowed") is not False:
        failures.append("gate_request_skip_must_be_false")
    if data.get("allowed_runtime_disposition") not in ALLOWED_RUNTIME_DISPOSITIONS:
        failures.append("runtime_disposition_not_allowed")
    parks_for_review = data.get("allowed_runtime_disposition") == "park_awaiting_human_review"
    needs_review = data.get("approval_posture") == "needs_human_review"
    if parks_for_review and not needs_review:
        failures.append("park_disposition_requires_human_review")

    return sorted(set(failures))




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
    outbox_doc: dict[str, Any] | None = None,
    temporal_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.inngest_event_flow_control_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-inngest-event-flow-control-fixture-v1-20260617":
        top_failures.append("task_id mismatch")

    runtime_boundary = fixture.get("runtime_boundary") or {}
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if runtime_boundary.get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    outbox_path = Path(fixture.get("source_outbox_path", ""))
    outbox_messages: dict[str, dict[str, Any]] = {}
    if not outbox_path.exists():
        top_failures.append("source outbox path is missing")
    else:
        if outbox_doc is None:
            outbox_doc = load_json(outbox_path)
        outbox_messages = {msg["message_id"]: msg for msg in outbox_doc.get("messages", [])}

    temporal_path = Path(fixture.get("source_temporal_signal_fixture_path", ""))
    if not temporal_path.exists():
        top_failures.append("source temporal signal fixture path is missing")
    else:
        if temporal_doc is None:
            temporal_doc = load_json(temporal_path)
        next_test = "inngest_event_name_and_flow_control_fixture_against_central_outbox_history_v1"
        if temporal_doc.get("next_local_test") != next_test:
            top_failures.append("source temporal fixture does not point to this Inngest event/flow-control test")

    seen_event_ids: set[str] = set()
    seen_idempotency: set[str] = set()
    rows = []
    for event in fixture.get("events", []):
        failures = validate_event(event, fixture, outbox_messages)
        event_id = event.get("event_id")
        idem = (event.get("data") or {}).get("idempotency_key")
        if event_id in seen_event_ids:
            failures.append("duplicate_event_id")
        seen_event_ids.add(event_id)
        if idem in seen_idempotency:
            failures.append("duplicate_idempotency_key")
        seen_idempotency.add(idem)
        expected_failures = sorted(event.get("expected_failures") or [])
        matches_expected = sorted(failures) == expected_failures
        rows.append(
            {
                "event_id": event_id,
                "source_message_id": event.get("source_message_id"),
                "event_name": event.get("event_name"),
                "expected_decision": event.get("expected_decision"),
                "actual_failures": sorted(failures),
                "expected_failures": expected_failures,
                "matches_expected": matches_expected,
            }
        )

    failed_rows = [row for row in rows if not row["matches_expected"]]
    failed_count = len(failed_rows) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.inngest_event_flow_control_fixture_validation.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "events_checked": len(rows),
        "passed_count": len(rows) - len(failed_rows),
        "failed_count": failed_count,
        "top_level_failures": top_failures,
        "runtime_boundary": runtime_boundary,
        "rows": rows,
        "next_local_test": fixture.get("next_local_test"),
    }
