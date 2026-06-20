from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Report-only scaffolding packet and materialized artifact reports."""

from .constants import (
    DURABLE_ORCHESTRATION_DIR,
    DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_VALIDATION_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACT_DIR,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_REPORT,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_VALIDATION_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_JSON,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_REPORT,
    DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_VALIDATION_JSON,
    SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .service_workers import db_scalar, load_report_json_or_error
from .utils import safe_id_fragment
from .durable_adapter_runtime_contract import (
    forbidden_runtime_imports_in_source,
)


def write_durable_adapter_runtime_report_only_scaffolding_packet(
    conn: sqlite3.Connection, args: argparse.Namespace
) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_VALIDATION_JSON
    )
    fixtures_validation_path = (
        Path(args.fixtures_validation_path)
        if args.fixtures_validation_path
        else DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_VALIDATION_JSON
    )
    fixtures_path = Path(args.fixtures_path) if args.fixtures_path else DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_JSON
    preflight_validation_path = (
        Path(args.preflight_validation_path)
        if args.preflight_validation_path
        else DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []

    fixtures_validation, fixtures_validation_errors = load_report_json_or_error(fixtures_validation_path)
    fixtures_payload, fixtures_errors = load_report_json_or_error(fixtures_path)
    preflight_validation, preflight_errors = load_report_json_or_error(preflight_validation_path)
    failures.extend(fixtures_validation_errors + fixtures_errors + preflight_errors)

    fixtures_validation_loaded = bool(fixtures_validation)
    fixtures_validation_passed = bool(
        fixtures_validation
        and fixtures_validation.get("schema_version") == "temporal_inngest_adapter_runtime_report_only_fixtures_validation.v1"
        and fixtures_validation.get("all_checks_passed") is True
        and fixtures_validation.get("failure_count") == 0
    )
    if fixtures_validation and not fixtures_validation_passed:
        failures.append("report-only fixtures validation is not passing")

    preflight_validation_loaded = bool(preflight_validation)
    preflight_validation_passed = bool(
        preflight_validation
        and preflight_validation.get("schema_version") == "temporal_inngest_adapter_runtime_implementation_preflight_validation.v1"
        and preflight_validation.get("all_checks_passed") is True
        and preflight_validation.get("failure_count") == 0
    )
    if preflight_validation and not preflight_validation_passed:
        failures.append("runtime implementation preflight validation is not passing")

    fixtures = fixtures_payload.get("fixtures", []) if fixtures_payload else []
    if fixtures_payload and not isinstance(fixtures, list):
        failures.append("report-only fixtures payload field fixtures is not a list")
        fixtures = []

    source_report_only_fixture_count = (
        fixtures_validation.get("report_only_fixture_count") if fixtures_validation else None
    )
    source_accepted_report_only_fixture_count = (
        fixtures_validation.get("accepted_report_only_fixture_count") if fixtures_validation else None
    )
    runtime_implementation_allowed = bool(
        preflight_validation and preflight_validation.get("runtime_implementation_allowed") is True
    )
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

    packet_components: list[dict[str, Any]] = []
    for fixture in fixtures:
        component_id = str(fixture.get("fixture_id", "unknown")).replace("allow_", "packet_")
        report_only = bool(
            fixture.get("accepted") is True
            and fixture.get("allowed_scope") == "local_report_only"
            and fixture.get("runtime_fixture") is False
            and fixture.get("runtime_side_effect_fixture") is False
            and fixture.get("side_effects_performed") is False
        )
        if not report_only:
            failures.append(f"{fixture.get('fixture_id')} is not a clean report-only fixture")
        packet_components.append(
            {
                "component_id": component_id,
                "source_fixture_id": fixture.get("fixture_id"),
                "artifact_kind": fixture.get("artifact_kind"),
                "title": fixture.get("candidate_action"),
                "report_only": report_only,
                "executable_code": False,
                "runtime_component": False,
                "runtime_side_effect_component": False,
                "side_effects_performed": False,
                "implementation_note": "Generate local markdown/JSON planning content only; do not import Temporal/Inngest or start runtimes.",
            }
        )

    packet_component_count = len(packet_components)
    runtime_component_count = sum(1 for component in packet_components if component["runtime_component"])
    runtime_side_effect_component_count = sum(
        1 for component in packet_components if component["runtime_side_effect_component"]
    )
    executable_code_component_count = sum(1 for component in packet_components if component["executable_code"])
    all_packet_components_report_only = bool(
        packet_component_count == 5 and all(component["report_only"] for component in packet_components)
    )
    if packet_component_count != 5:
        failures.append(f"expected 5 packet components, got {packet_component_count}")
    if not all_packet_components_report_only:
        failures.append("not all packet components are report-only")
    if source_report_only_fixture_count != 5:
        failures.append(f"expected source report-only fixture count 5, got {source_report_only_fixture_count}")
    if source_accepted_report_only_fixture_count != 5:
        failures.append(
            f"expected source accepted report-only fixture count 5, got {source_accepted_report_only_fixture_count}"
        )
    if runtime_component_count != 0:
        failures.append(f"expected 0 runtime components, got {runtime_component_count}")
    if runtime_side_effect_component_count != 0:
        failures.append(f"expected 0 runtime side-effect components, got {runtime_side_effect_component_count}")
    if executable_code_component_count != 0:
        failures.append(f"expected 0 executable code components, got {executable_code_component_count}")

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
        "schema_version": "temporal_inngest_adapter_runtime_report_only_scaffolding_packet.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Package the currently permitted local report-only adapter scaffolding artifacts without producing executable runtime adapter code.",
        "fixtures_path": str(fixtures_path),
        "fixtures_validation_path": str(fixtures_validation_path),
        "preflight_validation_path": str(preflight_validation_path),
        "packet_component_count": packet_component_count,
        "packet_components": packet_components,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "forbidden_runtime_imports": forbidden_imports,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": "Materialize the packet components as local markdown/JSON scaffolding artifacts, still without executable runtime adapter code.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_report_only_scaffolding_packet_validation.v1",
        "generated_utc": generated_utc,
        "packet_path": str(json_output_path),
        "packet_component_count": packet_component_count,
        "source_report_only_fixture_count": source_report_only_fixture_count,
        "source_accepted_report_only_fixture_count": source_accepted_report_only_fixture_count,
        "fixtures_validation_loaded": fixtures_validation_loaded,
        "fixtures_validation_passed": fixtures_validation_passed,
        "preflight_validation_loaded": preflight_validation_loaded,
        "preflight_validation_passed": preflight_validation_passed,
        "all_packet_components_report_only": all_packet_components_report_only,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "runtime_component_count": runtime_component_count,
        "runtime_side_effect_component_count": runtime_side_effect_component_count,
        "executable_code_component_count": executable_code_component_count,
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
        "# Temporal/Inngest Runtime Report-Only Scaffolding Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "This packet is local report-only scaffolding. It contains planning and summary components, not executable Temporal/Inngest adapter code.",
        "",
        "## Packet Summary",
        "",
        f"- Packet components: `{packet_component_count}`",
        f"- Source report-only fixtures: `{source_report_only_fixture_count}`",
        f"- Accepted source fixtures: `{source_accepted_report_only_fixture_count}`",
        f"- All components report-only: `{all_packet_components_report_only}`",
        f"- Runtime implementation allowed: `{runtime_implementation_allowed}`",
        f"- Runtime code write allowed: `{runtime_code_write_allowed}`",
        f"- Report-only scaffolding allowed: `{report_only_scaffolding_allowed}`",
        f"- Runtime components: `{runtime_component_count}`",
        f"- Runtime side-effect components: `{runtime_side_effect_component_count}`",
        f"- Executable code components: `{executable_code_component_count}`",
        f"- Forbidden runtime imports detected: `{len(forbidden_imports)}`",
        f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
        "",
        "## Components",
        "",
        "| Component | Artifact kind | Report-only | Executable? |",
        "| --- | --- | --- | --- |",
    ]
    for component in packet_components:
        lines.append(
            f"| `{component['component_id']}` | `{component['artifact_kind']}` | `{component['report_only']}` | `{component['executable_code']}` |"
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
            "Materialize the packet components as local markdown/JSON scaffolding artifacts, still without executable runtime adapter code.",
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
                "packet_component_count": packet_component_count,
                "runtime_component_count": runtime_component_count,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

