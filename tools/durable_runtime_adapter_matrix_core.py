#!/usr/bin/env python3
"""Validate the durable runtime adapter matrix without installing or starting runtimes."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DURABLE_REPORTS = ROOT / "reports" / "durable-orchestration"
DEFAULT_FIXTURE = DURABLE_REPORTS / "durable-runtime-adapter-matrix-v2-20260617.json"
DEFAULT_SCHEMA = ROOT / "architecture" / "durable-runtime-adapter-matrix-v2.schema.json"
DEFAULT_JSON_OUT = DURABLE_REPORTS / "durable-runtime-adapter-matrix-v2-validation-20260617.json"
DEFAULT_MD_OUT = DURABLE_REPORTS / "durable-runtime-adapter-matrix-v2-20260617.md"

REQUIRED_RUNTIMES = {
    "sqlite_control_plane",
    "temporal_python",
    "inngest",
    "dbos_python",
    "pydantic_ai_durable_execution",
    "prefect",
    "restate",
}

ZERO_ACTION_FIELDS = {
    "dependency_installs": False,
    "dependency_imports": False,
    "runtime_starts": 0,
    "queue_enqueues": 0,
    "service_request_mutations": 0,
    "api_calls": False,
    "model_api_calls": False,
    "browser_sessions_started": 0,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def zero_action_failures(actions: dict[str, Any], prefix: str) -> list[str]:
    failures: list[str] = []
    for field, expected in ZERO_ACTION_FIELDS.items():
        if actions.get(field) != expected:
            failures.append(f"{prefix}.{field} must be {expected!r}")
    return failures


def validate_row(row: dict[str, Any], seen: set[str]) -> list[str]:
    failures: list[str] = []
    runtime_id = row.get("runtime_id")
    if not runtime_id:
        failures.append("runtime_id is required")
        return failures
    if runtime_id in seen:
        failures.append(f"duplicate runtime_id: {runtime_id}")
    seen.add(runtime_id)
    failures.extend(zero_action_failures(row.get("artifact_actions") or {}, f"matrix[{runtime_id}].artifact_actions"))
    if not row.get("source_urls"):
        failures.append("source_urls must not be empty")
    if not isinstance(row.get("score"), int) or not 0 <= row["score"] <= 100:
        failures.append("score must be an integer from 0 to 100")
    if len(row.get("first_local_test") or "") < 10:
        failures.append("first_local_test must be a concrete local fixture name")
    if not row.get("stop_conditions"):
        failures.append("stop_conditions must not be empty")
    if runtime_id == "sqlite_control_plane":
        if row.get("safe_now") is not True:
            failures.append("sqlite_control_plane must be the only safe_now runtime")
        if row.get("promotion_decision") != "keep_as_source_of_truth_now":
            failures.append("sqlite_control_plane promotion decision must keep it as source of truth")
    else:
        if row.get("safe_now") is not False:
            failures.append("non-sqlite runtime must not be safe_now")
        if not row.get("approval_dependencies"):
            failures.append("non-sqlite runtime must name approval dependencies")
        if len(row.get("stop_conditions") or []) < 2:
            failures.append("non-sqlite runtime must include at least two stop conditions")
        decision = (row.get("promotion_decision") or "").lower()
        if "adopt_now" in decision or decision == "keep_as_source_of_truth_now":
            failures.append("non-sqlite runtime cannot be adopted now")
    return failures




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
) -> dict[str, Any]:
    top_failures = []
    if fixture.get("schema_version") != "agent_company.durable_runtime_adapter_matrix.v2":
        top_failures.append("schema_version mismatch")
    if fixture.get("task_id") != "task-durable-runtime-adapter-matrix-v2-20260617":
        top_failures.append("task_id mismatch")
    top_failures.extend(zero_action_failures(fixture.get("artifact_actions") or {}, "artifact_actions"))

    rows = []
    seen: set[str] = set()
    for row in fixture.get("matrix", []):
        failures = validate_row(row, seen)
        rows.append(
            {
                "runtime_id": row.get("runtime_id"),
                "display_name": row.get("display_name"),
                "category": row.get("category"),
                "safe_now": row.get("safe_now"),
                "fits_existing_gates": row.get("fits_existing_gates"),
                "score": row.get("score"),
                "promotion_decision": row.get("promotion_decision"),
                "first_local_test": row.get("first_local_test"),
                "failures": failures,
            }
        )

    missing = sorted(REQUIRED_RUNTIMES - seen)
    unexpected = sorted(seen - REQUIRED_RUNTIMES)
    if missing:
        top_failures.append(f"missing required runtimes: {', '.join(missing)}")
    if unexpected:
        top_failures.append(f"unexpected runtime rows: {', '.join(unexpected)}")
    next_tests = fixture.get("recommended_next_local_tests") or []
    if "durable_runtime_adapter_matrix_v2_to_service_worker_reducer_fixture" not in next_tests:
        top_failures.append("recommended reducer fixture is required")
    safe_now_rows = sorted(row["runtime_id"] for row in fixture.get("matrix", []) if row.get("safe_now") is True)
    if safe_now_rows != ["sqlite_control_plane"]:
        top_failures.append("sqlite_control_plane must be the only safe_now row")

    row_failed_count = sum(1 for row in rows if row["failures"])
    failed_count = row_failed_count + (1 if top_failures else 0)
    return {
        "schema_version": "agent_company.durable_runtime_adapter_matrix_validation.v2",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "rows_checked": len(rows),
        "passed_count": len(rows) - row_failed_count,
        "failed_count": failed_count,
        "top_level_failures": top_failures,
        "required_runtimes_present": not missing,
        "artifact_actions": fixture.get("artifact_actions") or {},
        "recommended_next_local_tests": next_tests,
        "decision": fixture.get("decision"),
        "rows": rows,
    }
