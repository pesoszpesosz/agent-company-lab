#!/usr/bin/env python3
"""Validate durable-runtime reducer fixtures without importing or starting runtimes."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = (
    ROOT
    / "reports"
    / "durable-orchestration"
    / "durable-runtime-service-worker-reducer-fixture-v1-20260617.json"
)
DEFAULT_SCHEMA = ROOT / "architecture" / "durable-runtime-service-worker-reducer-fixture-v1.schema.json"
DEFAULT_JSON_OUT = (
    ROOT
    / "reports"
    / "durable-orchestration"
    / "durable-runtime-service-worker-reducer-fixture-v1-validation-20260617.json"
)
DEFAULT_MD_OUT = (
    ROOT
    / "reports"
    / "durable-orchestration"
    / "durable-runtime-service-worker-reducer-fixture-v1-20260617.md"
)

REQUIRED_RUNTIMES = {
    "sqlite_control_plane",
    "temporal_python",
    "inngest",
    "dbos_python",
    "pydantic_ai_durable_execution",
    "prefect",
    "restate",
}

REQUIRED_STATUSES = {
    "needs_review",
    "complete",
    "rejected",
}

ZERO_PROFILE_FIELDS = {
    "dependency_installs": False,
    "dependency_imports": False,
    "runtime_starts": 0,
    "queue_enqueues": 0,
    "api_calls": False,
    "external_side_effects": False,
}

ZERO_ACTION_FLAGS = {
    "ledger_mutation_allowed": False,
    "approval_granted": False,
    "assign_worker": False,
    "start_worker": False,
    "emit_followup_event": False,
    "schedule_activity": False,
    "call_api": False,
    "browser_session_started": False,
    "model_api_call": False,
    "queue_enqueue": False,
    "external_side_effects_allowed": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_zero_fields(source: dict[str, Any], expected: dict[str, Any], prefix: str) -> list[str]:
    failures: list[str] = []
    for field, expected_value in expected.items():
        if source.get(field) != expected_value:
            failures.append(f"{prefix}.{field} must be {expected_value!r}; got {source.get(field)!r}")
    return failures


def status_output(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "output_state": case["expected_output_state"],
        "parked": case["parked"],
        "terminal": case["terminal"],
        "resume_requirements": case["resume_requirements"],
    }


def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
) -> dict[str, Any]:
    top_failures: list[str] = []
    if fixture.get("schema_version") != "agent_company.durable_runtime_service_worker_reducer_fixture.v1":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-durable-runtime-service-worker-reducer-fixture-v1-20260617":
        top_failures.append("task_id mismatch")

    profiles = fixture.get("runtime_profiles") or []
    cases = fixture.get("service_status_cases") or []
    profile_ids = {row.get("runtime_id") for row in profiles}
    statuses = {row.get("status_snapshot") for row in cases}
    missing_runtimes = sorted(REQUIRED_RUNTIMES - profile_ids)
    unexpected_runtimes = sorted(profile_ids - REQUIRED_RUNTIMES)
    missing_statuses = sorted(REQUIRED_STATUSES - statuses)
    if missing_runtimes:
        top_failures.append(f"missing runtime profiles: {', '.join(missing_runtimes)}")
    if unexpected_runtimes:
        top_failures.append(f"unexpected runtime profiles: {', '.join(unexpected_runtimes)}")
    if missing_statuses:
        top_failures.append(f"missing status cases: {', '.join(missing_statuses)}")

    expected_flags = fixture.get("expected_action_flags") or {}
    top_failures.extend(check_zero_fields(expected_flags, ZERO_ACTION_FLAGS, "expected_action_flags"))
    queue_snapshot = fixture.get("queue_snapshot") or {}
    if queue_snapshot.get("service_request_count") != sum(queue_snapshot.get("status_counts", {}).values()):
        top_failures.append("queue_snapshot service_request_count must equal status_counts total")
    if queue_snapshot.get("needs_review_count", 0) <= 0:
        top_failures.append("queue_snapshot must include parked needs_review requests")

    expanded_checks: list[dict[str, Any]] = []
    for profile in profiles:
        runtime_id = profile.get("runtime_id")
        profile_failures = check_zero_fields(profile, ZERO_PROFILE_FIELDS, f"runtime_profiles[{runtime_id}]")
        if runtime_id == "sqlite_control_plane":
            if profile.get("safe_now") is not True:
                profile_failures.append("sqlite_control_plane must be safe_now")
            if profile.get("allowed_reducer_mode") != "local_sqlite_dry_run_only":
                profile_failures.append("sqlite_control_plane must use local_sqlite_dry_run_only")
        else:
            if profile.get("safe_now") is not False:
                profile_failures.append("non-sqlite runtime must not be safe_now")
            if profile.get("allowed_reducer_mode") != "runtime_contract_preview_only":
                profile_failures.append("non-sqlite runtime must use runtime_contract_preview_only")
        for case in cases:
            row_failures = list(profile_failures)
            output = status_output(case)
            if case["status_snapshot"] == "needs_review":
                needs_review_not_parked = (
                    output["output_state"] != "parked.awaiting_human_review"
                    or not output["parked"]
                    or output["terminal"]
                )
                if needs_review_not_parked:
                    row_failures.append("needs_review must park awaiting human review")
                if len(output["resume_requirements"]) < 5:
                    row_failures.append(
                        "needs_review must name the full approval/scope/pool/artifact resume requirements"
                    )
            if case["status_snapshot"] in {"complete", "rejected"}:
                if not output["terminal"] or output["parked"]:
                    row_failures.append("terminal status must remain terminal and not parked")
            expanded_checks.append(
                {
                    "runtime_id": runtime_id,
                    "status_snapshot": case["status_snapshot"],
                    "event_name": case["event_name"],
                    "output_state": output["output_state"],
                    "parked": output["parked"],
                    "terminal": output["terminal"],
                    "allowed_reducer_mode": profile.get("allowed_reducer_mode"),
                    "action_flags": expected_flags,
                    "failures": sorted(set(row_failures)),
                }
            )

    failed_count = sum(1 for row in expanded_checks if row["failures"]) + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.durable_runtime_service_worker_reducer_fixture_validation.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "runtime_profile_count": len(profiles),
        "status_case_count": len(cases),
        "expanded_check_count": len(expanded_checks),
        "failed_count": failed_count,
        "top_level_failures": top_failures,
        "required_runtimes_present": not missing_runtimes,
        "required_statuses_present": not missing_statuses,
        "runtime_boundary": {
            "dependency_installs": 0,
            "dependency_imports": 0,
            "runtime_starts": 0,
            "queue_enqueues": 0,
            "service_request_mutations": 0,
            "worker_starts": 0,
            "browser_sessions_started": 0,
            "api_calls": False,
            "model_api_calls": False,
            "external_side_effects": False,
        },
        "queue_snapshot": queue_snapshot,
        "expanded_checks": expanded_checks,
        "next_local_test": fixture.get("next_local_test"),
    }
