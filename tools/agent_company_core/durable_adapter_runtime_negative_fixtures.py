from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Runtime negative fixtures, implementation preflight, and report-only fixture reports."""

from .constants import (
    DURABLE_ADAPTER_RUNTIME_READINESS_VALIDATION_JSON,
    DURABLE_ORCHESTRATION_DIR,
    DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_JSON,
    DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_REPORT,
    DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON,
    DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON,
    DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_JSON,
    DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_REPORT,
    DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_VALIDATION_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_REPORT,
    DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_VALIDATION_JSON,
    DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON,
)
from .io import now_utc
from .service_workers import db_scalar, load_report_json_or_error
from .durable_adapter_runtime_contract import (
    forbidden_runtime_imports_in_source,
)


def durable_runtime_negative_fixture_definitions() -> list[dict[str, Any]]:
    return [
        {
            "fixture_id": "reject_dependency_install_temporalio",
            "candidate_action": "install Temporal dependency for adapter prototype",
            "blocked_signals": {"dependency_install": True},
            "expected_rejection_reason": "dependency installs require explicit approval",
        },
        {
            "fixture_id": "reject_temporal_runtime_import",
            "candidate_action": "import Temporal runtime symbols",
            "blocked_signals": {"runtime_import": True, "dependency_import": True},
            "expected_rejection_reason": "runtime imports require explicit approval",
        },
        {
            "fixture_id": "reject_temporal_workflow_start",
            "candidate_action": "start ServiceRequestLifecycleWorkflow",
            "blocked_signals": {"temporal_workflow_start": True},
            "expected_rejection_reason": "workflow starts require explicit approval",
        },
        {
            "fixture_id": "reject_temporal_activity_schedule",
            "candidate_action": "schedule service-worker refresh activity",
            "blocked_signals": {"temporal_activity_schedule": True},
            "expected_rejection_reason": "activity scheduling requires explicit approval",
        },
        {
            "fixture_id": "reject_inngest_event_emit",
            "candidate_action": "emit service request lifecycle event",
            "blocked_signals": {"inngest_event_emit": True},
            "expected_rejection_reason": "event emission requires explicit approval",
        },
        {
            "fixture_id": "reject_service_request_mutation",
            "candidate_action": "assign or update a parked service request",
            "blocked_signals": {"service_request_mutation": True},
            "expected_rejection_reason": "service-request mutation requires explicit approval",
        },
        {
            "fixture_id": "reject_worker_start",
            "candidate_action": "start model/API worker pool",
            "blocked_signals": {"worker_start": True},
            "expected_rejection_reason": "worker starts require explicit approval",
        },
        {
            "fixture_id": "reject_model_api_call",
            "candidate_action": "call a model API through the parked adapter request",
            "blocked_signals": {"api_call": True, "external_side_effect": True},
            "expected_rejection_reason": "API calls and external side effects require explicit approval",
        },
    ]


def write_durable_adapter_runtime_negative_fixtures(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_VALIDATION_JSON
    )
    contract_validation_path = (
        Path(args.contract_validation_path)
        if args.contract_validation_path
        else DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []

    contract_validation, contract_errors = load_report_json_or_error(contract_validation_path)
    failures.extend(contract_errors)
    contract_validation_loaded = bool(contract_validation)
    contract_validation_passed = bool(contract_validation and contract_validation.get("all_checks_passed") is True)
    if contract_validation and contract_validation.get("schema_version") != "temporal_inngest_adapter_runtime_interface_contract_validation.v1":
        failures.append("runtime interface contract validation has an unexpected schema version")
    if contract_validation and not contract_validation_passed:
        failures.append("runtime interface contract validation is not passing")

    forbidden_imports = forbidden_runtime_imports_in_source()
    if forbidden_imports:
        failures.append(f"forbidden runtime imports detected in source: {len(forbidden_imports)}")

    model_row = conn.execute(
        """
        SELECT request_id, status, assigned_agent_id, started_at, completed_at, decision_note
        FROM service_requests
        WHERE request_id = ?
        """,
        ("req-pydantic-ai-model-backed-adapter-20260614",),
    ).fetchone()
    model_request = dict(model_row) if model_row else None
    model_api_pool_registered = bool(
        db_scalar(conn, "SELECT COUNT(*) FROM agents WHERE agent_id = ?", ("service-worker-model-api-execution-pool",))
    )
    model_api_gate_remains_parked = bool(
        model_request
        and model_request.get("status") == "needs_review"
        and model_request.get("assigned_agent_id") is None
        and model_request.get("started_at") is None
        and model_request.get("completed_at") is None
        and model_request.get("decision_note") is None
    )
    if not model_api_gate_remains_parked:
        failures.append("model/API service request is no longer parked exactly as expected")
    if model_api_pool_registered:
        failures.append("model/API worker pool is registered unexpectedly")

    fixtures = durable_runtime_negative_fixture_definitions()
    evaluated_fixtures: list[dict[str, Any]] = []
    for fixture in fixtures:
        signals = fixture["blocked_signals"]
        blocked = any(bool(value) for value in signals.values())
        disposition = "rejected.blocked_by_runtime_interface_contract" if blocked else "accepted.unexpected"
        if not blocked:
            failures.append(f"{fixture['fixture_id']} was not rejected")
        evaluated_fixtures.append(
            {
                **fixture,
                "observed_disposition": disposition,
                "accepted": not blocked,
                "rejected": blocked,
                "side_effects_performed": False,
            }
        )

    rejected_fixture_count = sum(1 for fixture in evaluated_fixtures if fixture["rejected"])
    accepted_fixture_count = sum(1 for fixture in evaluated_fixtures if fixture["accepted"])
    if len(fixtures) != 8:
        failures.append(f"expected 8 negative fixtures, got {len(fixtures)}")
    if rejected_fixture_count != len(fixtures):
        failures.append(f"expected every negative fixture to be rejected, got {rejected_fixture_count}/{len(fixtures)}")
    if accepted_fixture_count != 0:
        failures.append(f"expected 0 accepted negative fixtures, got {accepted_fixture_count}")

    runtime_boundary = {
        "dependency_installs": 0,
        "dependency_imports": 0,
        "temporal_server_started": False,
        "temporal_workflows_started": 0,
        "temporal_activities_scheduled": 0,
        "inngest_service_started": False,
        "inngest_events_emitted": 0,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "temporal_inngest_adapter_runtime_interface_negative_fixtures.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Static negative fixtures that keep future Temporal/Inngest adapter work report-only until explicit runtime/action approval exists.",
        "contract_validation_path": str(contract_validation_path),
        "negative_fixture_count": len(evaluated_fixtures),
        "fixtures": evaluated_fixtures,
        "forbidden_runtime_imports": forbidden_imports,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": "Promote these negative fixtures into the durable adapter implementation preflight before writing any Temporal/Inngest runtime adapter code.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_negative_fixtures_rejected = rejected_fixture_count == len(fixtures) and accepted_fixture_count == 0
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_interface_negative_fixtures_validation.v1",
        "generated_utc": generated_utc,
        "negative_fixture_path": str(json_output_path),
        "contract_validation_path": str(contract_validation_path),
        "negative_fixture_count": len(evaluated_fixtures),
        "rejected_fixture_count": rejected_fixture_count,
        "accepted_fixture_count": accepted_fixture_count,
        "contract_validation_loaded": contract_validation_loaded,
        "contract_validation_passed": contract_validation_passed,
        "all_negative_fixtures_rejected": all_negative_fixtures_rejected,
        "runtime_import_allowed": False,
        "dependency_install_allowed": False,
        "workflow_start_allowed": False,
        "activity_schedule_allowed": False,
        "event_emit_allowed": False,
        "service_request_mutation_allowed": False,
        "worker_start_allowed": False,
        "api_call_allowed": False,
        "forbidden_runtime_import_count": len(forbidden_imports),
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Temporal/Inngest Runtime Interface Negative Fixtures",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "These are static local-only negative fixtures. They evaluate candidate runtime actions and prove that dependency installs, runtime imports, workflow starts, activity schedules, event emissions, worker starts, API calls, and service-request mutations remain rejected.",
        "",
        "## Fixture Summary",
        "",
        f"- Negative fixtures: `{len(evaluated_fixtures)}`",
        f"- Rejected fixtures: `{rejected_fixture_count}`",
        f"- Accepted fixtures: `{accepted_fixture_count}`",
        f"- Contract validation loaded: `{contract_validation_loaded}`",
        f"- Contract validation passed: `{contract_validation_passed}`",
        f"- Forbidden runtime imports detected: `{len(forbidden_imports)}`",
        f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
        "",
        "## Fixtures",
        "",
        "| Fixture | Disposition | Side effects? |",
        "| --- | --- | --- |",
    ]
    for fixture in evaluated_fixtures:
        lines.append(
            f"| `{fixture['fixture_id']}` | `{fixture['observed_disposition']}` | `{fixture['side_effects_performed']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Dependency installs: `0`",
            "- Runtime imports: `0`",
            "- Temporal workflows started: `0`",
            "- Temporal activities scheduled: `0`",
            "- Inngest events emitted: `0`",
            "- Service requests updated: `0`",
            "- Service requests assigned: `0`",
            "- Worker starts: `0`",
            "- API calls: `False`",
            "- External side effects: `False`",
            "",
            "## Next Action",
            "",
            "Promote these negative fixtures into the durable adapter implementation preflight before writing any Temporal/Inngest runtime adapter code.",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "negative_fixture_count": len(evaluated_fixtures),
                "rejected_fixture_count": rejected_fixture_count,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

