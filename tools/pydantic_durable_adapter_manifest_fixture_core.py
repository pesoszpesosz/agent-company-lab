#!/usr/bin/env python3
"""Validate Pydantic durable adapter manifest fixtures without importing Pydantic AI."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DURABLE_REPORTS = ROOT / "reports" / "durable-orchestration"
DEFAULT_FIXTURE = DURABLE_REPORTS / "pydantic-durable-adapter-manifest-fixture-v1-20260617.json"
DEFAULT_SCHEMA = ROOT / "architecture" / "pydantic-durable-adapter-manifest-fixture-v1.schema.json"
DEFAULT_JSON_OUT = DURABLE_REPORTS / "pydantic-durable-adapter-manifest-fixture-v1-validation-20260617.json"
DEFAULT_MD_OUT = DURABLE_REPORTS / "pydantic-durable-adapter-manifest-fixture-v1-20260617.md"

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "pydantic_ai_imports": 0,
    "durable_backend_imports": 0,
    "agent_runs": 0,
    "test_model_runs": 0,
    "function_model_runs": 0,
    "model_api_calls": False,
    "model_requests_allowed": False,
    "mcp_servers_started": 0,
    "runtime_starts": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_case(case: dict[str, Any], fixture: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    policy = fixture["adapter_policy"]
    backend = case.get("backend")
    model_mode = str(case.get("model_mode", ""))

    if backend not in policy["supported_reference_backends"]:
        failures.append("backend_not_supported")
    if model_mode not in policy["allowed_model_modes"]:
        failures.append("model_mode_not_allowed")
    if case.get("allow_model_requests") is not False:
        failures.append("model_requests_not_blocked")
    if case.get("model_api_call_requested") is not False:
        failures.append("model_api_call_requested")
    if case.get("durable_backend_imported") is not False:
        failures.append("durable_backend_imported")
    if case.get("runtime_started") is not False:
        failures.append("runtime_started")
    if case.get("mcp_server_started") is not False:
        failures.append("mcp_server_started")

    for toolset in case.get("toolsets", []):
        toolset_id = str(toolset.get("toolset_id") or "")
        if policy.get("require_static_toolset_ids_for_durable_backends") and not toolset_id:
            failures.append("toolset_id_missing")
        if toolset.get("registration") == "dynamic" and toolset.get("uses_get_toolset") is True:
            failures.append("dynamic_toolset_with_get_toolset_not_supported")

    return sorted(set(failures))




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
    dbos_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.pydantic_durable_adapter_manifest_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-pydantic-durable-adapter-manifest-fixture-v1-20260617":
        top_failures.append("task_id mismatch")
    if not schema_path.exists():
        top_failures.append("schema path is missing")

    for source_field in ["source_dbos_boundary_validation_path", "source_pydantic_local_manifest_path"]:
        source_path = Path(fixture.get(source_field, ""))
        if not source_path.exists():
            top_failures.append(f"{source_field} is missing")

    dbos_path = Path(fixture.get("source_dbos_boundary_validation_path", ""))
    if dbos_doc is None and dbos_path.exists():
        dbos_doc = load_json(dbos_path)
    if dbos_doc is not None:
        next_test = "pydantic_durable_adapter_manifest_fixture_without_model_api_calls"
        if dbos_doc.get("next_local_test") != next_test:
            top_failures.append("source DBOS validation does not point to this Pydantic manifest test")
        if dbos_doc.get("failed_count") != 0:
            top_failures.append("source DBOS validation has failures")

    runtime_boundary = fixture.get("runtime_boundary") or {}
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if runtime_boundary.get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    rows = []
    seen_cases: set[str] = set()
    for case in fixture.get("manifest_cases", []):
        failures = validate_case(case, fixture)
        case_id = str(case.get("case_id"))
        if case_id in seen_cases:
            failures.append("duplicate_case_id")
        seen_cases.add(case_id)
        expected_failures = sorted(case.get("expected_failures") or [])
        matches_expected = sorted(failures) == expected_failures
        rows.append(
            {
                "case_id": case_id,
                "backend": case.get("backend"),
                "model_mode": case.get("model_mode"),
                "expected_decision": case.get("expected_decision"),
                "actual_failures": sorted(failures),
                "expected_failures": expected_failures,
                "matches_expected": matches_expected,
            }
        )

    failed_rows = [row for row in rows if not row["matches_expected"]]
    failed_count = len(failed_rows) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.pydantic_durable_adapter_manifest_fixture_validation.v1",
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
