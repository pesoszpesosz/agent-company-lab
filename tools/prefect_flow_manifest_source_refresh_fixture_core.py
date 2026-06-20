#!/usr/bin/env python3
"""Validate Prefect source-refresh flow manifests without importing Prefect."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = (
    ROOT / "reports" / "durable-orchestration" / "prefect-flow-manifest-source-refresh-fixture-v1-20260617.json"
)
DEFAULT_SCHEMA = ROOT / "architecture" / "prefect-flow-manifest-source-refresh-fixture-v1.schema.json"
DEFAULT_JSON_OUT = (
    ROOT
    / "reports"
    / "durable-orchestration"
    / "prefect-flow-manifest-source-refresh-fixture-v1-validation-20260617.json"
)
DEFAULT_MD_OUT = (
    ROOT / "reports" / "durable-orchestration" / "prefect-flow-manifest-source-refresh-fixture-v1-20260617.md"
)

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "prefect_imports": 0,
    "flows_decorated": 0,
    "tasks_decorated": 0,
    "flow_runs": 0,
    "task_runs": 0,
    "deployments_created": 0,
    "schedules_created": 0,
    "work_pools_created": 0,
    "workers_started": 0,
    "prefect_test_harness_starts": 0,
    "prefect_server_starts": 0,
    "prefect_cloud_calls": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "external_side_effects": False,
}

PREFECT_RUNTIME_EDGE_FIELDS = [
    "package_imported",
    "flow_decorated",
    "task_decorated",
    "flow_run_requested",
    "task_run_requested",
    "deployment_created",
    "schedule_created",
    "work_pool_created",
    "worker_started",
    "test_harness_started",
    "server_or_cloud_used",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_modes_from_scheduler(plan: dict[str, Any]) -> dict[str, str]:
    return {row["source_id"]: row["allowed_mode"] for row in plan.get("sources", [])}


def source_lanes_from_scheduler(plan: dict[str, Any]) -> dict[str, str]:
    return {row["source_id"]: row["lane_id"] for row in plan.get("sources", [])}


def validate_case(
    case: dict[str, Any],
    fixture: dict[str, Any],
    source_modes: dict[str, str],
    source_lanes: dict[str, str],
) -> list[str]:
    failures: list[str] = []
    policy = fixture["flow_policy"]
    source_id = case.get("source_id")
    allowed_mode = case.get("allowed_mode")
    prefect_edges = case.get("prefect_edges") or {}
    side_effects = case.get("side_effects") or {}

    if source_id not in source_modes:
        failures.append("source_id_not_found_in_scheduler")
    else:
        if allowed_mode != source_modes[source_id]:
            failures.append("allowed_mode_mismatch_scheduler")
        if case.get("lane_id") != source_lanes.get(source_id):
            failures.append("lane_id_mismatch_scheduler")

    if allowed_mode in policy["blocked_modes"] or allowed_mode == "service_request_only":
        failures.append("allowed_mode_requires_service_request")
    elif allowed_mode not in policy["allowed_modes"]:
        failures.append("allowed_mode_not_allowed_for_prefect_manifest")

    flow_name = str(case.get("flow_name") or "")
    if not flow_name.startswith("agent_company_source_refresh_"):
        failures.append("flow_name_prefix_invalid")
    if not case.get("task_names"):
        failures.append("task_names_missing")

    for edge_name in PREFECT_RUNTIME_EDGE_FIELDS:
        if prefect_edges.get(edge_name) is not False:
            failures.append(f"prefect_runtime_edge:{edge_name}")

    if side_effects.get("browser_session") is not False:
        failures.append("browser_session_requested")
    if side_effects.get("api_call") is not False:
        failures.append("api_call_requested")
    if side_effects.get("service_request_mutation") is not False:
        failures.append("service_request_mutation_requested")
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
    scheduler_doc: dict[str, Any] | None = None,
    pydantic_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.prefect_flow_manifest_source_refresh_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-prefect-flow-manifest-source-refresh-fixture-v1-20260617":
        top_failures.append("task_id mismatch")
    if not schema_path.exists():
        top_failures.append("schema path is missing")

    for source_field in [
        "source_pydantic_manifest_validation_path",
        "source_freshness_scheduler_plan_path",
        "source_specs_path",
    ]:
        source_path = Path(fixture.get(source_field, ""))
        if not source_path.exists():
            top_failures.append(f"{source_field} is missing")

    pydantic_path = Path(fixture.get("source_pydantic_manifest_validation_path", ""))
    if pydantic_doc is None and pydantic_path.exists():
        pydantic_doc = load_json(pydantic_path)
    if pydantic_doc is not None:
        expected_next = "prefect_flow_manifest_for_local_source_refresh_without_runtime_start"
        if pydantic_doc.get("next_local_test") != expected_next:
            top_failures.append("source Pydantic validation does not point to this Prefect manifest test")
        if pydantic_doc.get("failed_count") != 0:
            top_failures.append("source Pydantic validation has failures")

    runtime_boundary = fixture.get("runtime_boundary") or {}
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if runtime_boundary.get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    scheduler_path = Path(fixture.get("source_freshness_scheduler_plan_path", ""))
    source_modes: dict[str, str] = {}
    source_lanes: dict[str, str] = {}
    if scheduler_doc is None and scheduler_path.exists():
        scheduler_doc = load_json(scheduler_path)
    if scheduler_doc is not None:
        source_modes = source_modes_from_scheduler(scheduler_doc)
        source_lanes = source_lanes_from_scheduler(scheduler_doc)
        meta = scheduler_doc.get("metadata") or {}
        if (
            meta.get("api_calls") is not False
            or meta.get("browser_actions") is not False
            or meta.get("external_side_effects") is not False
        ):
            top_failures.append("source freshness scheduler metadata is not zero-side-effect")

    rows = []
    seen_cases: set[str] = set()
    for case in fixture.get("flow_cases", []):
        failures = validate_case(case, fixture, source_modes, source_lanes)
        case_id = str(case.get("case_id"))
        if case_id in seen_cases:
            failures.append("duplicate_case_id")
        seen_cases.add(case_id)
        expected_failures = sorted(case.get("expected_failures") or [])
        matches_expected = sorted(failures) == expected_failures
        rows.append(
            {
                "case_id": case_id,
                "source_id": case.get("source_id"),
                "lane_id": case.get("lane_id"),
                "allowed_mode": case.get("allowed_mode"),
                "expected_decision": case.get("expected_decision"),
                "actual_failures": sorted(failures),
                "expected_failures": expected_failures,
                "matches_expected": matches_expected,
            }
        )

    failed_rows = [row for row in rows if not row["matches_expected"]]
    failed_count = len(failed_rows) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.prefect_flow_manifest_source_refresh_fixture_validation.v1",
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
