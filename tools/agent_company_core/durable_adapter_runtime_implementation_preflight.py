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
from .durable_adapter_runtime_implementation_preflight_content import build_durable_runtime_implementation_preflight_content
from .io import now_utc
from .service_workers import db_scalar, load_report_json_or_error
from .durable_adapter_runtime_contract import (
    forbidden_runtime_imports_in_source,
)


def write_durable_adapter_runtime_implementation_preflight(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    DURABLE_ORCHESTRATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_REPORT
    json_output_path = Path(args.json_path) if args.json_path else DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_JSON
    validation_path = (
        Path(args.validation_path)
        if args.validation_path
        else DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON
    )
    contract_validation_path = (
        Path(args.contract_validation_path)
        if args.contract_validation_path
        else DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON
    )
    negative_validation_path = (
        Path(args.negative_validation_path)
        if args.negative_validation_path
        else DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_VALIDATION_JSON
    )
    readiness_validation_path = (
        Path(args.readiness_validation_path)
        if args.readiness_validation_path
        else DURABLE_ADAPTER_RUNTIME_READINESS_VALIDATION_JSON
    )
    integration_validation_path = (
        Path(args.integration_validation_path)
        if args.integration_validation_path
        else DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON
    )
    generated_utc = now_utc()
    failures: list[str] = []

    upstream_specs = [
        (
            "service_worker_refresh_integration",
            integration_validation_path,
            "temporal_inngest_adapter_service_worker_refresh_integration_validation.v1",
        ),
        (
            "runtime_readiness",
            readiness_validation_path,
            "temporal_inngest_adapter_runtime_readiness_validation.v1",
        ),
        (
            "runtime_interface_contract",
            contract_validation_path,
            "temporal_inngest_adapter_runtime_interface_contract_validation.v1",
        ),
        (
            "runtime_interface_negative_fixtures",
            negative_validation_path,
            "temporal_inngest_adapter_runtime_interface_negative_fixtures_validation.v1",
        ),
    ]
    upstream_validations: list[dict[str, Any]] = []
    payload_by_id: dict[str, dict[str, Any]] = {}
    for upstream_id, path, expected_schema in upstream_specs:
        payload, load_errors = load_report_json_or_error(path)
        failures.extend(load_errors)
        loaded = payload is not None
        schema_matches = bool(payload and payload.get("schema_version") == expected_schema)
        passed = bool(payload and payload.get("all_checks_passed") is True and payload.get("failure_count") == 0)
        if loaded and not schema_matches:
            failures.append(f"{upstream_id} validation has unexpected schema version")
        if loaded and not passed:
            failures.append(f"{upstream_id} validation is not passing")
        if payload:
            payload_by_id[upstream_id] = payload
        upstream_validations.append(
            {
                "id": upstream_id,
                "path": str(path),
                "loaded": loaded,
                "schema_matches": schema_matches,
                "all_checks_passed": bool(payload and payload.get("all_checks_passed") is True),
                "failure_count": payload.get("failure_count") if payload else None,
                "passed": passed and schema_matches,
            }
        )

    readiness_checks = payload_by_id.get("runtime_readiness", {}).get("checks", {})
    negative_validation = payload_by_id.get("runtime_interface_negative_fixtures", {})
    contract_validation = payload_by_id.get("runtime_interface_contract", {})
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

    explicit_runtime_approval_present = False
    external_runtime_implementation_allowed_now = bool(
        readiness_checks.get("external_runtime_implementation_allowed_now") is True
    )
    local_report_only_implementation_allowed_now = bool(
        readiness_checks.get("local_report_only_implementation_allowed_now") is True
    )
    runtime_implementation_allowed = bool(
        explicit_runtime_approval_present and external_runtime_implementation_allowed_now
    )
    runtime_code_write_allowed = runtime_implementation_allowed
    report_only_scaffolding_allowed = local_report_only_implementation_allowed_now and not runtime_implementation_allowed
    if external_runtime_implementation_allowed_now:
        failures.append("runtime readiness unexpectedly allows external runtime implementation")
    if not local_report_only_implementation_allowed_now:
        failures.append("runtime readiness no longer allows local report-only implementation")
    if runtime_implementation_allowed:
        failures.append("runtime implementation became allowed without an explicit approval gate")

    preflight_checks = [
        {
            "check_id": "upstream_validations_loaded_and_passing",
            "passed": all(item["passed"] for item in upstream_validations),
            "actual": upstream_validations,
        },
        {
            "check_id": "runtime_readiness_blocks_external_runtime",
            "passed": external_runtime_implementation_allowed_now is False,
            "actual": external_runtime_implementation_allowed_now,
        },
        {
            "check_id": "runtime_readiness_allows_report_only_scaffolding",
            "passed": local_report_only_implementation_allowed_now is True,
            "actual": local_report_only_implementation_allowed_now,
        },
        {
            "check_id": "negative_fixtures_reject_all_runtime_candidates",
            "passed": bool(
                negative_validation.get("negative_fixture_count") == 8
                and negative_validation.get("rejected_fixture_count") == 8
                and negative_validation.get("accepted_fixture_count") == 0
                and negative_validation.get("all_negative_fixtures_rejected") is True
            ),
            "actual": {
                "negative_fixture_count": negative_validation.get("negative_fixture_count"),
                "rejected_fixture_count": negative_validation.get("rejected_fixture_count"),
                "accepted_fixture_count": negative_validation.get("accepted_fixture_count"),
                "all_negative_fixtures_rejected": negative_validation.get("all_negative_fixtures_rejected"),
            },
        },
        {
            "check_id": "runtime_contract_import_scan_clean",
            "passed": bool(
                contract_validation.get("forbidden_runtime_import_count") == 0
                and contract_validation.get("no_forbidden_runtime_imports_detected") is True
                and len(forbidden_imports) == 0
            ),
            "actual": {
                "contract_forbidden_import_count": contract_validation.get("forbidden_runtime_import_count"),
                "source_forbidden_import_count": len(forbidden_imports),
            },
        },
        {
            "check_id": "model_api_gate_still_parked",
            "passed": model_api_gate_remains_parked,
            "actual": model_request,
        },
        {
            "check_id": "model_api_pool_absent",
            "passed": not model_api_pool_registered,
            "actual": model_api_pool_registered,
        },
        {
            "check_id": "no_explicit_runtime_approval_present",
            "passed": not explicit_runtime_approval_present,
            "actual": explicit_runtime_approval_present,
        },
        {
            "check_id": "runtime_implementation_remains_blocked",
            "passed": not runtime_implementation_allowed and not runtime_code_write_allowed,
            "actual": {
                "runtime_implementation_allowed": runtime_implementation_allowed,
                "runtime_code_write_allowed": runtime_code_write_allowed,
            },
        },
    ]
    for check in preflight_checks:
        if not check["passed"]:
            failures.append(f"preflight check failed: {check['check_id']}")

    preflight_content = build_durable_runtime_implementation_preflight_content(
        generated_utc=generated_utc,
        json_output_path=str(json_output_path),
        validation_path=str(validation_path),
        upstream_validations=upstream_validations,
        preflight_checks=preflight_checks,
        runtime_implementation_allowed=runtime_implementation_allowed,
        runtime_code_write_allowed=runtime_code_write_allowed,
        report_only_scaffolding_allowed=report_only_scaffolding_allowed,
        explicit_runtime_approval_present=explicit_runtime_approval_present,
        external_runtime_implementation_allowed_now=external_runtime_implementation_allowed_now,
        local_report_only_implementation_allowed_now=local_report_only_implementation_allowed_now,
        negative_validation=negative_validation,
        forbidden_imports=forbidden_imports,
        model_request=model_request,
        model_api_gate_remains_parked=model_api_gate_remains_parked,
        model_api_pool_registered=model_api_pool_registered,
        failures=failures,
    )
    runtime_boundary = preflight_content["runtime_boundary"]
    passed_preflight_check_count = preflight_content["passed_preflight_check_count"]
    upstream_validation_passed_count = preflight_content["upstream_validation_passed_count"]
    payload = preflight_content["payload"]
    validation_payload = preflight_content["validation_payload"]
    all_checks_passed = preflight_content["all_checks_passed"]
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.write_text(preflight_content["markdown"], encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "preflight_check_count": len(preflight_checks),
                "passed_preflight_check_count": passed_preflight_check_count,
                "runtime_implementation_allowed": runtime_implementation_allowed,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

