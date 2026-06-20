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


def durable_runtime_report_only_fixture_definitions() -> list[dict[str, Any]]:
    return [
        {
            "fixture_id": "allow_contract_summary_markdown",
            "candidate_action": "render a markdown summary of the runtime interface contract",
            "artifact_kind": "report_markdown",
            "allowed_scope": "local_report_only",
        },
        {
            "fixture_id": "allow_negative_fixture_matrix_json",
            "candidate_action": "render a JSON matrix of rejected runtime-side-effect candidates",
            "artifact_kind": "report_json",
            "allowed_scope": "local_report_only",
        },
        {
            "fixture_id": "allow_preflight_gate_snapshot",
            "candidate_action": "render a preflight gate snapshot for human review",
            "artifact_kind": "validation_json",
            "allowed_scope": "local_report_only",
        },
        {
            "fixture_id": "allow_chain_readiness_pointer",
            "candidate_action": "render a pointer to the latest chain-integrity validation",
            "artifact_kind": "report_markdown",
            "allowed_scope": "local_report_only",
        },
        {
            "fixture_id": "allow_adapter_todo_packet",
            "candidate_action": "render a todo packet for future explicitly-approved runtime adapter work",
            "artifact_kind": "planning_markdown",
            "allowed_scope": "local_report_only",
        },
    ]


def write_durable_adapter_runtime_report_only_fixtures(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_VALIDATION_JSON
    )
    preflight_validation_path = (
        Path(args.preflight_validation_path)
        if args.preflight_validation_path
        else DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []

    preflight_validation, preflight_errors = load_report_json_or_error(preflight_validation_path)
    failures.extend(preflight_errors)
    preflight_validation_loaded = bool(preflight_validation)
    preflight_validation_passed = bool(
        preflight_validation
        and preflight_validation.get("schema_version")
        == "temporal_inngest_adapter_runtime_implementation_preflight_validation.v1"
        and preflight_validation.get("all_checks_passed") is True
        and preflight_validation.get("failure_count") == 0
    )
    if preflight_validation and not preflight_validation_passed:
        failures.append("runtime implementation preflight validation is not passing")

    runtime_implementation_allowed = bool(preflight_validation and preflight_validation.get("runtime_implementation_allowed") is True)
    runtime_code_write_allowed = bool(preflight_validation and preflight_validation.get("runtime_code_write_allowed") is True)
    report_only_scaffolding_allowed = bool(
        preflight_validation and preflight_validation.get("report_only_scaffolding_allowed") is True
    )
    if runtime_implementation_allowed:
        failures.append("runtime implementation is unexpectedly allowed")
    if runtime_code_write_allowed:
        failures.append("runtime code writing is unexpectedly allowed")
    if not report_only_scaffolding_allowed:
        failures.append("report-only scaffolding is not allowed by implementation preflight")

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

    fixtures = durable_runtime_report_only_fixture_definitions()
    evaluated_fixtures: list[dict[str, Any]] = []
    for fixture in fixtures:
        allowed = bool(report_only_scaffolding_allowed and fixture["allowed_scope"] == "local_report_only")
        if not allowed:
            failures.append(f"{fixture['fixture_id']} was not allowed as report-only scaffolding")
        evaluated_fixtures.append(
            {
                **fixture,
                "observed_disposition": "allowed.local_report_only" if allowed else "rejected.unexpected",
                "accepted": allowed,
                "rejected": not allowed,
                "runtime_fixture": False,
                "runtime_side_effect_fixture": False,
                "side_effects_performed": False,
            }
        )

    accepted_report_only_fixture_count = sum(1 for fixture in evaluated_fixtures if fixture["accepted"])
    rejected_report_only_fixture_count = sum(1 for fixture in evaluated_fixtures if fixture["rejected"])
    runtime_fixture_count = sum(1 for fixture in evaluated_fixtures if fixture["runtime_fixture"])
    runtime_side_effect_fixture_count = sum(1 for fixture in evaluated_fixtures if fixture["runtime_side_effect_fixture"])
    if len(fixtures) != 5:
        failures.append(f"expected 5 report-only fixtures, got {len(fixtures)}")
    if accepted_report_only_fixture_count != len(fixtures):
        failures.append(
            f"expected every report-only fixture to be accepted, got {accepted_report_only_fixture_count}/{len(fixtures)}"
        )
    if rejected_report_only_fixture_count != 0:
        failures.append(f"expected 0 rejected report-only fixtures, got {rejected_report_only_fixture_count}")
    if runtime_fixture_count != 0:
        failures.append(f"expected 0 runtime fixtures, got {runtime_fixture_count}")
    if runtime_side_effect_fixture_count != 0:
        failures.append(f"expected 0 runtime side-effect fixtures, got {runtime_side_effect_fixture_count}")

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
    all_report_only_fixtures_allowed = accepted_report_only_fixture_count == len(fixtures) and rejected_report_only_fixture_count == 0
    payload = {
        "schema_version": "temporal_inngest_adapter_runtime_report_only_fixtures.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Positive fixtures for the only implementation work currently allowed: local report-only scaffolding.",
        "preflight_validation_path": str(preflight_validation_path),
        "report_only_fixture_count": len(evaluated_fixtures),
        "fixtures": evaluated_fixtures,
        "forbidden_runtime_imports": forbidden_imports,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": "Create the local report-only adapter scaffolding packet from these allowed fixtures, without importing Temporal/Inngest or starting runtimes.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_report_only_fixtures_validation.v1",
        "generated_utc": generated_utc,
        "report_only_fixture_path": str(json_output_path),
        "preflight_validation_path": str(preflight_validation_path),
        "report_only_fixture_count": len(evaluated_fixtures),
        "accepted_report_only_fixture_count": accepted_report_only_fixture_count,
        "rejected_report_only_fixture_count": rejected_report_only_fixture_count,
        "runtime_fixture_count": runtime_fixture_count,
        "runtime_side_effect_fixture_count": runtime_side_effect_fixture_count,
        "preflight_validation_loaded": preflight_validation_loaded,
        "preflight_validation_passed": preflight_validation_passed,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "all_report_only_fixtures_allowed": all_report_only_fixtures_allowed,
        "forbidden_runtime_import_count": len(forbidden_imports),
        "no_forbidden_runtime_imports_detected": len(forbidden_imports) == 0,
        "model_api_gate_remains_parked": model_api_gate_remains_parked,
        "model_api_pool_registered": model_api_pool_registered,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Temporal/Inngest Runtime Report-Only Fixtures",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "Only local report-only scaffolding is allowed. These fixtures define permitted planning and summary artifacts while runtime implementation, runtime imports, worker starts, API calls, and service-request mutation remain blocked.",
        "",
        "## Fixture Summary",
        "",
        f"- Report-only fixtures: `{len(evaluated_fixtures)}`",
        f"- Accepted report-only fixtures: `{accepted_report_only_fixture_count}`",
        f"- Rejected report-only fixtures: `{rejected_report_only_fixture_count}`",
        f"- Runtime fixtures: `{runtime_fixture_count}`",
        f"- Runtime side-effect fixtures: `{runtime_side_effect_fixture_count}`",
        f"- Preflight validation passed: `{preflight_validation_passed}`",
        f"- Runtime implementation allowed: `{runtime_implementation_allowed}`",
        f"- Runtime code write allowed: `{runtime_code_write_allowed}`",
        f"- Report-only scaffolding allowed: `{report_only_scaffolding_allowed}`",
        f"- Forbidden runtime imports detected: `{len(forbidden_imports)}`",
        f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
        "",
        "## Fixtures",
        "",
        "| Fixture | Artifact kind | Disposition | Side effects? |",
        "| --- | --- | --- | --- |",
    ]
    for fixture in evaluated_fixtures:
        lines.append(
            f"| `{fixture['fixture_id']}` | `{fixture['artifact_kind']}` | `{fixture['observed_disposition']}` | `{fixture['side_effects_performed']}` |"
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
            "Create the local report-only adapter scaffolding packet from these allowed fixtures, without importing Temporal/Inngest or starting runtimes.",
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
                "report_only_fixture_count": len(evaluated_fixtures),
                "accepted_report_only_fixture_count": accepted_report_only_fixture_count,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

