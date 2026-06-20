#!/usr/bin/env python3
"""Validate DBOS workflow/step boundary fixtures without importing DBOS."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = (
    ROOT / "reports" / "durable-orchestration" / "dbos-workflow-step-boundary-fixture-v1-20260617.json"
)
DEFAULT_SCHEMA = ROOT / "architecture" / "dbos-workflow-step-boundary-fixture-v1.schema.json"
DEFAULT_JSON_OUT = (
    ROOT
    / "reports"
    / "durable-orchestration"
    / "dbos-workflow-step-boundary-fixture-v1-validation-20260617.json"
)
DEFAULT_MD_OUT = (
    ROOT / "reports" / "durable-orchestration" / "dbos-workflow-step-boundary-fixture-v1-20260617.md"
)

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "dbos_package_imported": False,
    "dbos_launch_called": False,
    "database_connections": 0,
    "database_provisioning": False,
    "queues_registered": 0,
    "workflows_started": 0,
    "workflows_enqueued": 0,
    "steps_executed": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "external_side_effects": False,
}

FORBIDDEN_RUNTIME_EDGES = [
    "launch_requested",
    "database_provision_requested",
    "queue_registration_requested",
    "workflow_start_requested",
    "workflow_enqueue_requested",
]

EXPECTED_STATE_BY_STATUS = {
    "needs_review": "parked.awaiting_human_review",
    "complete": "terminal.completed_from_ledger_snapshot",
    "rejected": "terminal.rejected_from_ledger_snapshot",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def request_ids_from_queue(queue_doc: dict[str, Any]) -> set[str]:
    raw = json.dumps(queue_doc)
    ids: set[str] = set()
    marker = "req-"
    start = 0
    while True:
        index = raw.find(marker, start)
        if index < 0:
            break
        end = index
        while end < len(raw) and raw[end] not in {'"', "'", "\\", " ", ",", "]", "}", "\n", "\r", "\t"}:
            end += 1
        ids.add(raw[index:end])
        start = end
    return ids


def validate_case(case: dict[str, Any], fixture: dict[str, Any], known_request_ids: set[str]) -> list[str]:
    failures: list[str] = []
    policy = fixture["step_boundary_policy"]
    request_id = case.get("service_request_id")
    status = case.get("status_snapshot")
    workflow_id = case.get("workflow_id", "")
    workflow_options = case.get("workflow_options") or {}
    runtime_edges = case.get("dbos_runtime_edges") or {}

    if request_id not in known_request_ids:
        failures.append("service_request_id_not_found_in_queue_snapshot")
    if request_id not in workflow_id:
        failures.append("workflow_id_missing_service_request_id")
    if not str(workflow_id).startswith("agent-company/dbos/service-request/"):
        failures.append("workflow_id_prefix_invalid")

    expected_state = EXPECTED_STATE_BY_STATUS.get(str(status))
    if case.get("expected_state") != expected_state:
        failures.append("expected_state_does_not_match_status")
    actual_terminal = status in {"complete", "rejected"}
    if case.get("expected_terminal") is not actual_terminal:
        failures.append("expected_terminal_does_not_match_status")

    dedupe = str(workflow_options.get("deduplication_id", ""))
    if not dedupe.startswith(f"service-request:{request_id}"):
        failures.append("deduplication_id_missing_service_request")
    if not workflow_options.get("queue_name"):
        failures.append("queue_name_missing")
    if not workflow_options.get("queue_partition_key"):
        failures.append("queue_partition_key_missing")

    for edge_name in FORBIDDEN_RUNTIME_EDGES:
        if runtime_edges.get(edge_name) is not False:
            failures.append(f"forbidden_runtime_edge:{edge_name}")

    allowed_steps = set(policy["allowed_step_kinds"])
    forbidden_steps = set(policy["forbidden_step_kinds"])
    for step in case.get("planned_steps", []):
        step_id = str(step.get("step_id", "unknown_step"))
        step_kind = step.get("step_kind")
        if step_kind in forbidden_steps:
            failures.append(f"forbidden_step_kind:{step_kind}")
        if step_kind not in allowed_steps and step_kind not in forbidden_steps:
            failures.append(f"unknown_step_kind:{step_kind}")
        if step.get("executes_now") is not False:
            failures.append(f"planned_step_executes_now:{step_id}")
        if step.get("mutates_service_request") is not False:
            failures.append(f"step_mutates_service_request:{step_id}")
        if step.get("external_side_effect") is not False:
            failures.append(f"step_external_side_effect:{step_id}")

    return sorted(set(failures))


def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
    known_request_ids: set[str] | None = None,
    source_inngest_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.dbos_workflow_step_boundary_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-dbos-workflow-step-boundary-fixture-v1-20260617":
        top_failures.append("task_id mismatch")

    if not schema_path.exists():
        top_failures.append("schema path is missing")

    contract = fixture.get("workflow_contract") or {}
    for field in [
        "defined_not_decorated",
        "steps_defined_not_decorated",
        "ceo_ledger_remains_source_of_truth",
    ]:
        if contract.get(field) is not True:
            top_failures.append(f"workflow_contract.{field} must be true")
    for field in [
        "dbos_package_imported",
        "dbos_launch_called",
        "database_provisioned",
        "queue_registered",
        "workflow_started",
        "workflow_enqueued",
        "step_executed",
    ]:
        if contract.get(field) is not False:
            top_failures.append(f"workflow_contract.{field} must be false")

    runtime_boundary = fixture.get("runtime_boundary") or {}
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if runtime_boundary.get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    for source_field in [
        "source_service_worker_schema_path",
        "source_service_worker_queue_path",
        "source_inngest_fixture_path",
    ]:
        source_path = Path(fixture.get(source_field, ""))
        if not source_path.exists():
            top_failures.append(f"{source_field} is missing")

    queue_path = Path(fixture.get("source_service_worker_queue_path", ""))
    if known_request_ids is None:
        known_request_ids = set()
        if queue_path.exists():
            known_request_ids = request_ids_from_queue(load_json(queue_path))

    inngest_path = Path(fixture.get("source_inngest_fixture_path", ""))
    if source_inngest_doc is None and inngest_path.exists():
        source_inngest_doc = load_json(inngest_path)
    if source_inngest_doc is not None:
        expected_next = "dbos_workflow_step_boundary_fixture_for_service_worker_request_v1"
        if source_inngest_doc.get("next_local_test") != expected_next:
            top_failures.append("source Inngest fixture does not point to this DBOS boundary test")

    rows = []
    seen_cases: set[str] = set()
    for case in fixture.get("cases", []):
        failures = validate_case(case, fixture, known_request_ids)
        case_id = case.get("case_id")
        if case_id in seen_cases:
            failures.append("duplicate_case_id")
        seen_cases.add(str(case_id))
        expected_failures = sorted(case.get("expected_failures") or [])
        matches_expected = sorted(failures) == expected_failures
        rows.append(
            {
                "case_id": case_id,
                "service_request_id": case.get("service_request_id"),
                "status_snapshot": case.get("status_snapshot"),
                "expected_state": case.get("expected_state"),
                "expected_terminal": case.get("expected_terminal"),
                "actual_failures": sorted(failures),
                "expected_failures": expected_failures,
                "matches_expected": matches_expected,
            }
        )

    failed_rows = [row for row in rows if not row["matches_expected"]]
    failed_count = len(failed_rows) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.dbos_workflow_step_boundary_fixture_validation.v1",
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
