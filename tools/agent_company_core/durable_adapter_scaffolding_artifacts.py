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
from .durable_adapter_scaffolding_artifact_content import (
    materialized_scaffolding_artifact_content,
    scaffolding_artifact_filename,
)
from .durable_adapter_runtime_contract import (
    forbidden_runtime_imports_in_source,
)


def write_durable_adapter_runtime_report_only_scaffolding_artifacts(
    conn: sqlite3.Connection, args: argparse.Namespace
) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_VALIDATION_JSON
    )
    artifact_dir = (
        Path(args.artifact_dir)
        if args.artifact_dir
        else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACT_DIR
    )
    packet_path = Path(args.packet_path) if args.packet_path else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_JSON
    packet_validation_path = (
        Path(args.packet_validation_path)
        if args.packet_validation_path
        else DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_VALIDATION_JSON
    )
    chain_validation_path = (
        Path(args.chain_validation_path)
        if args.chain_validation_path
        else SERVICE_WORKER_CHAIN_INTEGRITY_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []
    artifact_dir.mkdir(parents=True, exist_ok=True)

    packet_payload, packet_errors = load_report_json_or_error(packet_path)
    packet_validation, packet_validation_errors = load_report_json_or_error(packet_validation_path)
    chain_validation, chain_errors = load_report_json_or_error(chain_validation_path)
    failures.extend(packet_errors + packet_validation_errors + chain_errors)

    packet_validation_loaded = bool(packet_validation)
    packet_validation_passed = bool(
        packet_validation
        and packet_validation.get("schema_version")
        == "temporal_inngest_adapter_runtime_report_only_scaffolding_packet_validation.v1"
        and packet_validation.get("all_checks_passed") is True
        and packet_validation.get("failure_count") == 0
    )
    if packet_validation and not packet_validation_passed:
        failures.append("report-only scaffolding packet validation is not passing")
    if chain_validation and chain_validation.get("all_checks_passed") is not True:
        failures.append("service-worker chain integrity validation is not passing")

    packet_components = packet_payload.get("packet_components", []) if packet_payload else []
    if packet_payload and not isinstance(packet_components, list):
        failures.append("packet payload field packet_components is not a list")
        packet_components = []
    packet_component_count = packet_validation.get("packet_component_count") if packet_validation else None
    runtime_implementation_allowed = bool(
        packet_validation and packet_validation.get("runtime_implementation_allowed") is True
    )
    runtime_code_write_allowed = bool(packet_validation and packet_validation.get("runtime_code_write_allowed") is True)
    report_only_scaffolding_allowed = bool(
        packet_validation and packet_validation.get("report_only_scaffolding_allowed") is True
    )
    if runtime_implementation_allowed:
        failures.append("runtime implementation is unexpectedly allowed")
    if runtime_code_write_allowed:
        failures.append("runtime code writing is unexpectedly allowed")
    if not report_only_scaffolding_allowed:
        failures.append("report-only scaffolding is not allowed by packet validation")

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

    materialized_artifacts: list[dict[str, Any]] = []
    for component in packet_components:
        report_only = bool(
            component.get("report_only") is True
            and component.get("executable_code") is False
            and component.get("runtime_component") is False
            and component.get("runtime_side_effect_component") is False
            and component.get("side_effects_performed") is False
        )
        if not report_only:
            failures.append(f"{component.get('component_id')} is not report-only")
        artifact_kind = str(component.get("artifact_kind"))
        artifact_path = artifact_dir / scaffolding_artifact_filename(str(component.get("component_id")), artifact_kind)
        content = materialized_scaffolding_artifact_content(component, generated_utc, packet_path, chain_validation_path)
        artifact_path.write_text(content, encoding="utf-8")
        sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest().upper()
        materialized_artifacts.append(
            {
                "component_id": component.get("component_id"),
                "source_fixture_id": component.get("source_fixture_id"),
                "artifact_kind": artifact_kind,
                "path": str(artifact_path),
                "sha256": sha256,
                "report_only": report_only,
                "executable_code": False,
                "runtime_artifact": False,
                "runtime_side_effect_artifact": False,
                "side_effects_performed": False,
            }
        )

    materialized_artifact_count = len(materialized_artifacts)
    markdown_artifact_count = sum(1 for item in materialized_artifacts if item["path"].endswith(".md"))
    json_artifact_count = sum(1 for item in materialized_artifacts if item["path"].endswith(".json"))
    json_artifacts_parse = True
    for item in materialized_artifacts:
        if item["path"].endswith(".json"):
            try:
                load_json(Path(item["path"]))
            except Exception as exc:
                json_artifacts_parse = False
                failures.append(f"materialized JSON artifact does not parse: {item['path']}: {exc}")
    executable_artifact_count = sum(1 for item in materialized_artifacts if item["executable_code"])
    runtime_artifact_count = sum(1 for item in materialized_artifacts if item["runtime_artifact"])
    runtime_side_effect_artifact_count = sum(
        1 for item in materialized_artifacts if item["runtime_side_effect_artifact"]
    )
    all_materialized_artifacts_report_only = bool(
        materialized_artifact_count == 5 and all(item["report_only"] for item in materialized_artifacts)
    )
    if materialized_artifact_count != 5:
        failures.append(f"expected 5 materialized artifacts, got {materialized_artifact_count}")
    if packet_component_count != 5:
        failures.append(f"expected packet component count 5, got {packet_component_count}")
    if markdown_artifact_count != 3:
        failures.append(f"expected 3 markdown artifacts, got {markdown_artifact_count}")
    if json_artifact_count != 2:
        failures.append(f"expected 2 JSON artifacts, got {json_artifact_count}")
    if not all_materialized_artifacts_report_only:
        failures.append("not all materialized artifacts are report-only")
    if executable_artifact_count != 0:
        failures.append(f"expected 0 executable artifacts, got {executable_artifact_count}")
    if runtime_artifact_count != 0:
        failures.append(f"expected 0 runtime artifacts, got {runtime_artifact_count}")
    if runtime_side_effect_artifact_count != 0:
        failures.append(f"expected 0 runtime side-effect artifacts, got {runtime_side_effect_artifact_count}")

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
        "schema_version": "temporal_inngest_adapter_runtime_report_only_scaffolding_artifacts.v1",
        "generated_utc": generated_utc,
        "lane_id": "platform_engineering",
        "purpose": "Materialized local markdown/JSON artifacts from the report-only scaffolding packet.",
        "artifact_dir": str(artifact_dir),
        "packet_path": str(packet_path),
        "packet_validation_path": str(packet_validation_path),
        "chain_validation_path": str(chain_validation_path),
        "materialized_artifact_count": materialized_artifact_count,
        "materialized_artifacts": materialized_artifacts,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
        "forbidden_runtime_imports": forbidden_imports,
        "model_api_request": model_request,
        "model_api_pool_registered": model_api_pool_registered,
        "runtime_boundary": runtime_boundary,
        "next_action": "Add these materialized report-only scaffolding artifacts to artifact traceability and prepare a human-readable runtime adapter approval packet, still with runtime code blocked.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "temporal_inngest_adapter_runtime_report_only_scaffolding_artifacts_validation.v1",
        "generated_utc": generated_utc,
        "manifest_path": str(json_output_path),
        "artifact_dir": str(artifact_dir),
        "materialized_artifact_count": materialized_artifact_count,
        "packet_component_count": packet_component_count,
        "packet_validation_loaded": packet_validation_loaded,
        "packet_validation_passed": packet_validation_passed,
        "all_materialized_artifacts_report_only": all_materialized_artifacts_report_only,
        "markdown_artifact_count": markdown_artifact_count,
        "json_artifact_count": json_artifact_count,
        "json_artifacts_parse": json_artifacts_parse,
        "executable_artifact_count": executable_artifact_count,
        "runtime_artifact_count": runtime_artifact_count,
        "runtime_side_effect_artifact_count": runtime_side_effect_artifact_count,
        "runtime_implementation_allowed": runtime_implementation_allowed,
        "runtime_code_write_allowed": runtime_code_write_allowed,
        "report_only_scaffolding_allowed": report_only_scaffolding_allowed,
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
        "# Temporal/Inngest Runtime Report-Only Scaffolding Artifacts",
        "",
        f"Generated UTC: {generated_utc}",
        f"Artifact directory: `{artifact_dir}`",
        f"JSON manifest: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        "The scaffolding packet has been materialized as local markdown/JSON planning artifacts only. No executable runtime adapter code was generated.",
        "",
        "## Summary",
        "",
        f"- Materialized artifacts: `{materialized_artifact_count}`",
        f"- Markdown artifacts: `{markdown_artifact_count}`",
        f"- JSON artifacts: `{json_artifact_count}`",
        f"- JSON artifacts parse: `{json_artifacts_parse}`",
        f"- All artifacts report-only: `{all_materialized_artifacts_report_only}`",
        f"- Runtime artifacts: `{runtime_artifact_count}`",
        f"- Runtime side-effect artifacts: `{runtime_side_effect_artifact_count}`",
        f"- Executable artifacts: `{executable_artifact_count}`",
        f"- Runtime implementation allowed: `{runtime_implementation_allowed}`",
        f"- Runtime code write allowed: `{runtime_code_write_allowed}`",
        f"- Report-only scaffolding allowed: `{report_only_scaffolding_allowed}`",
        f"- Forbidden runtime imports detected: `{len(forbidden_imports)}`",
        f"- Model/API gate remains parked: `{model_api_gate_remains_parked}`",
        "",
        "## Artifacts",
        "",
        "| Component | Kind | Path | Report-only |",
        "| --- | --- | --- | --- |",
    ]
    for item in materialized_artifacts:
        lines.append(
            f"| `{item['component_id']}` | `{item['artifact_kind']}` | `{item['path']}` | `{item['report_only']}` |"
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
            "Add these materialized report-only scaffolding artifacts to artifact traceability and prepare a human-readable runtime adapter approval packet, still with runtime code blocked.",
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
                "artifact_dir": str(artifact_dir),
                "materialized_artifact_count": materialized_artifact_count,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

