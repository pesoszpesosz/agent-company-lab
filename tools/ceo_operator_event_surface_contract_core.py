#!/usr/bin/env python3
"""Core helpers for report-only CEO/operator event surface contracts."""

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
SCHEMA_PATH = ARCH / "ceo-operator-event-surface-contract-v1.schema.json"
WAVE20_REPORT = REPORTS / "agent-company-operator-interface-radar-wave20-20260618.json"
WAVE20_VALIDATION = REPORTS / "agent-company-operator-interface-radar-wave20-20260618-validation.json"
CEO_REVIEW = REPORTS / "ceo-review-latest.md"
CONTROL_PLANE = REPORTS / "control-plane-status-latest.md"
TRACE_REPORT = REPORTS / "trace-events-latest.md"
ARTIFACT_REPORT = REPORTS / "artifacts-latest.md"
ROUTE_CHAIN_VALIDATION = REPORTS / "egress-route-chain-integrity-audit-v1-validation-20260618.json"
SERVICE_WORKER_CHAIN_VALIDATION = REPORTS / "service-worker-chain-integrity-validation-latest.json"
FIXTURE_DIR = REPORTS / "ceo-operator-event-surface-contract-v1-fixtures"
REPORT_JSON = REPORTS / "ceo-operator-event-surface-contract-v1-20260618.json"
VALIDATION_JSON = REPORTS / "ceo-operator-event-surface-contract-v1-validation-20260618.json"
REPORT_MD = REPORTS / "ceo-operator-event-surface-contract-v1-20260618.md"

NEXT_ACTION = (
    "Use this report-only event surface to design local CEO/manager inbox packets; do not enable SSE, WebSockets, "
    "browser sessions, worker starts, service-request mutation, model/MCP calls, public actions, or external side effects."
)

EVENT_TYPES = [
    ("ceo_review_snapshot", "CEO review snapshot", "ceo", "all_managers"),
    ("manager_status_update", "Manager status update", "lane_manager", "ceo"),
    ("worker_capability_signal", "Worker capability signal", "service_worker_registry", "lane_manager"),
    ("service_request_gate_ping", "Service request gate ping", "service_bureau", "requesting_manager"),
    ("tool_auth_request_proposed", "Tool/auth request proposed", "lane_manager", "chief_risk_officer"),
    ("approval_decision_needed", "Approval decision needed", "gate_validator", "human_operator"),
    ("route_blocker_changed", "Route blocker changed", "egress_gateway", "ceo"),
    ("artifact_evidence_attached", "Artifact evidence attached", "agent_worker", "lane_manager"),
    ("outcome_realization_recorded", "Outcome realization recorded", "lane_manager", "ceo"),
    ("trace_replay_pointer", "Trace replay pointer", "observability_worker", "ceo"),
    ("human_operator_note", "Human operator note", "human_operator", "lane_manager"),
    ("dispatch_next_action", "Dispatch next action", "ceo", "lane_manager"),
]

ZERO_BOUNDARY = {
    "report_only": True,
    "event_transports_started": 0,
    "operator_events_emitted": 0,
    "operator_events_persisted": 0,
    "approval_rows_written": 0,
    "decisions_applied": 0,
    "tasks_created": 0,
    "tasks_updated": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "runtime_starts": 0,
    "dependency_installs": 0,
    "sse_connections_opened": 0,
    "websocket_connections_opened": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "security_testing_actions": False,
    "external_side_effects": False,
}

REQUIRED_SOURCE_PATHS = [
    str(WAVE20_REPORT),
    str(WAVE20_VALIDATION),
    str(CEO_REVIEW),
    str(CONTROL_PLANE),
    str(TRACE_REPORT),
    str(ARTIFACT_REPORT),
    str(ROUTE_CHAIN_VALIDATION),
    str(SERVICE_WORKER_CHAIN_VALIDATION),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    try:
        return Path(value).resolve().is_relative_to(ROOT.resolve())
    except Exception:
        return False


def validation_ready(path: Path) -> bool:
    if not path.exists():
        return False
    data = load_json(path)
    return data.get("all_checks_passed") is True and data.get("failure_count") == 0


def source_summary() -> dict[str, Any]:
    wave20 = load_json(WAVE20_REPORT)
    wave20_validation = load_json(WAVE20_VALIDATION)
    route_validation = load_json(ROUTE_CHAIN_VALIDATION)
    service_validation = load_json(SERVICE_WORKER_CHAIN_VALIDATION)
    return {
        "wave20_report_path": str(WAVE20_REPORT),
        "wave20_validation_path": str(WAVE20_VALIDATION),
        "wave20_next_build": wave20.get("recommended_next_sequence", [""])[0],
        "wave20_all_checks_passed": wave20_validation.get("all_checks_passed"),
        "route_chain_validation_path": str(ROUTE_CHAIN_VALIDATION),
        "route_chain_all_checks_passed": route_validation.get("all_checks_passed"),
        "route_chain_full_count": route_validation.get("full_chain_route_count"),
        "service_worker_chain_validation_path": str(SERVICE_WORKER_CHAIN_VALIDATION),
        "service_worker_chain_all_checks_passed": service_validation.get("all_checks_passed"),
        "service_worker_checked_report_count": service_validation.get("checked_report_count"),
    }


def base_event(event_type: str, label: str, producer: str, consumer: str) -> dict[str, Any]:
    return {
        "schema_version": "agent_company.ceo_operator_event_surface_contract.v1",
        "event_surface_status": "report_only_contract",
        "event_type": event_type,
        "event_label": label,
        "producer_role": producer,
        "consumer_role": consumer,
        "source_artifact_paths": copy.deepcopy(REQUIRED_SOURCE_PATHS),
        "payload_contract": {
            "required_fields": [
                "event_id",
                "event_type",
                "lane_id",
                "task_id",
                "agent_id",
                "summary",
                "source_artifact_path",
                "created_utc",
            ],
            "optional_fields": [
                "service_request_id",
                "gate_id",
                "route_id",
                "artifact_id",
                "outcome_id",
                "trace_id",
                "human_note",
                "next_action",
            ],
        },
        "required_gate_ids": [
            "agent_egress_event_ledger_v1",
            "service_worker_chain_integrity_v1",
            "unified_agent_egress_gateway_docket_v1",
        ],
        "approval_granted_by_event": False,
        "event_transport_enabled": False,
        "sse_enabled": False,
        "websocket_enabled": False,
        "worker_start_allowed": False,
        "service_request_mutation_allowed": False,
        "model_api_call_allowed": False,
        "mcp_tool_call_allowed": False,
        "public_action_allowed": False,
        "external_side_effects": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": f"positive_{event_type}",
            "expected": "accepted",
            "event": base_event(event_type, label, producer, consumer),
        }
        for event_type, label, producer, consumer in EVENT_TYPES
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        event = base_event(*EVENT_TYPES[0])
        mutate(event)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "event": event})

    for field, value in [
        ("event_surface_status", "live_transport_enabled"),
        ("event_type", "unknown_event_type"),
        ("producer_role", ""),
        ("consumer_role", ""),
        ("approval_granted_by_event", True),
        ("event_transport_enabled", True),
        ("sse_enabled", True),
        ("websocket_enabled", True),
        ("worker_start_allowed", True),
        ("service_request_mutation_allowed", True),
        ("model_api_call_allowed", True),
        ("mcp_tool_call_allowed", True),
        ("public_action_allowed", True),
        ("external_side_effects", True),
    ]:
        negative(field, lambda e, f=field, v=value: e.update({f: v}))
    negative("missing_source_paths", lambda e: e.update({"source_artifact_paths": []}))
    negative("outside_source_path", lambda e: e.update({"source_artifact_paths": [r"C:\Temp\ceo-review.md"]}))
    negative("missing_payload_required_field", lambda e: e["payload_contract"].update({"required_fields": ["event_id"]}))
    negative("missing_gate", lambda e: e.update({"required_gate_ids": []}))
    for key, value in [
        ("event_transports_started", 1),
        ("operator_events_emitted", 1),
        ("operator_events_persisted", 1),
        ("approval_rows_written", 1),
        ("decisions_applied", 1),
        ("tasks_created", 1),
        ("tasks_updated", 1),
        ("service_requests_assigned", 1),
        ("service_requests_updated", 1),
        ("worker_starts", 1),
        ("browser_sessions_started", 1),
        ("runtime_starts", 1),
        ("dependency_installs", 1),
        ("sse_connections_opened", 1),
        ("websocket_connections_opened", 1),
        ("mcp_tool_calls", True),
        ("model_api_calls", True),
        ("public_actions", True),
        ("external_side_effects", True),
    ]:
        negative(f"boundary_{key}", lambda e, k=key, v=value: e["runtime_boundary"].update({k: v}))
    return fixtures


def validate_event(event: dict[str, Any], schema: dict[str, Any], sources: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("properties", {}).get("event_surface_status", {}).get("const") != "report_only_contract":
        errors.append("schema_event_surface_status_must_be_report_only_contract")
    for prop in ["event_transport_enabled", "sse_enabled", "websocket_enabled", "approval_granted_by_event"]:
        if schema.get("properties", {}).get(prop, {}).get("const") is not False:
            errors.append(f"schema_{prop}_must_be_false")
    if event.get("schema_version") != "agent_company.ceo_operator_event_surface_contract.v1":
        errors.append("schema_version_mismatch")
    if event.get("event_surface_status") != "report_only_contract":
        errors.append("event_surface_status_must_be_report_only_contract")
    if event.get("event_type") not in {item[0] for item in EVENT_TYPES}:
        errors.append("event_type_not_in_contract")
    if not str(event.get("producer_role", "")).strip():
        errors.append("producer_role_missing")
    if not str(event.get("consumer_role", "")).strip():
        errors.append("consumer_role_missing")
    source_paths = event.get("source_artifact_paths", [])
    if not isinstance(source_paths, list) or len(source_paths) < 4:
        errors.append("source_artifact_paths_must_include_current_operator_sources")
    for value in source_paths:
        if not path_inside_root(str(value)):
            errors.append("source_artifact_path_must_stay_inside_lab")
        elif not Path(str(value)).exists():
            errors.append("source_artifact_path_not_found")
    payload = event.get("payload_contract", {})
    required_fields = set(payload.get("required_fields", [])) if isinstance(payload, dict) else set()
    for required in ["event_id", "event_type", "lane_id", "task_id", "agent_id", "summary", "source_artifact_path", "created_utc"]:
        if required not in required_fields:
            errors.append(f"payload_required_field_missing:{required}")
    gates = set(event.get("required_gate_ids", []))
    for gate in ["agent_egress_event_ledger_v1", "service_worker_chain_integrity_v1", "unified_agent_egress_gateway_docket_v1"]:
        if gate not in gates:
            errors.append(f"required_gate_missing:{gate}")
    for key in [
        "approval_granted_by_event",
        "event_transport_enabled",
        "sse_enabled",
        "websocket_enabled",
        "worker_start_allowed",
        "service_request_mutation_allowed",
        "model_api_call_allowed",
        "mcp_tool_call_allowed",
        "public_action_allowed",
        "external_side_effects",
    ]:
        if event.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    if sources.get("wave20_next_build") != "ceo_operator_event_surface_contract_v1":
        errors.append("source_wave20_must_recommend_event_surface_contract")
    if sources.get("wave20_all_checks_passed") is not True:
        errors.append("source_wave20_validation_not_passing")
    if sources.get("route_chain_all_checks_passed") is not True or sources.get("route_chain_full_count") != 8:
        errors.append("route_chain_must_be_ready")
    if sources.get("service_worker_chain_all_checks_passed") is not True:
        errors.append("service_worker_chain_must_be_ready")
    if not validation_ready(WAVE20_VALIDATION):
        errors.append("wave20_validation_not_ready")
    if not validation_ready(ROUTE_CHAIN_VALIDATION):
        errors.append("route_chain_validation_not_ready")
    if not validation_ready(SERVICE_WORKER_CHAIN_VALIDATION):
        errors.append("service_worker_chain_validation_not_ready")
    boundary = event.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")
    return errors


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = source_summary()
    failures: list[str] = []
    results = []
    for fixture in fixtures:
        event = (
            copy.deepcopy(fixture["event"])
            if "event" in fixture
            else load_json(Path(fixture["path"]))
        )
        errors = validate_event(event, schema, sources)
        accepted = not errors
        expected_accept = fixture["expected"] == "accepted"
        passed = accepted == expected_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({
            **fixture,
            "passed": passed,
            "event_type": event.get("event_type"),
            "result": {
                "accepted_for_contract_only": accepted,
                "rejected": not accepted,
                "errors": errors,
                "event_transport_enabled": False,
                "approval_granted_by_event": False,
                "external_side_effects": False,
            },
        })
    accepted_count = sum(1 for item in results if item["result"]["accepted_for_contract_only"])
    rejected_count = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted_count != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted_count}")
    if rejected_count != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected_count}")
    generated = utc_now()
    event_type_ids = [item[0] for item in EVENT_TYPES]
    report = {
        "schema_version": "agent_company.ceo_operator_event_surface_contract_report.v1",
        "generated_utc": generated,
        "contract_status": "report_only_event_surface_ready",
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_summary": sources,
        "event_type_count": len(EVENT_TYPES),
        "event_type_ids": event_type_ids,
        "fixture_count": len(fixtures),
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "results": results,
        "next_action": NEXT_ACTION,
        **copy.deepcopy(ZERO_BOUNDARY),
        "event_transport_enabled": False,
        "sse_enabled": False,
        "websocket_enabled": False,
        "approval_granted_by_event": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.ceo_operator_event_surface_contract_validation.v1",
        "generated_utc": generated,
        "contract_status": "report_only_event_surface_ready",
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "source_wave20_next_build": sources["wave20_next_build"],
        "event_type_count": len(EVENT_TYPES),
        "fixture_count": len(fixtures),
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "fixture_expectation_mismatch_count": len(failures),
        "event_transport_enabled": False,
        "sse_enabled": False,
        "websocket_enabled": False,
        "approval_granted_by_event": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    return report, validation


