#!/usr/bin/env python3
"""Validate lane-manager checkpoint handoff rows without assigning work."""

from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(r"E:\agent-company-lab")
DB_PATH = ROOT / "state" / "agent_company.sqlite"
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "lane-manager-checkpoint-handoff-v1.schema.json"
BRIDGE_VALIDATION = REPORTS / "checkpoint-interrupt-bridge-fixture-v1-validation-20260617.json"
CHECKPOINT_VALIDATION = REPORTS / "checkpoint-interrupt-contract-v1-validation-20260617.json"
CEO_REVIEW = REPORTS / "ceo-review-latest.md"
FIXTURE_DIR = REPORTS / "lane-manager-checkpoint-handoff-v1-fixtures"
REPORT_JSON = REPORTS / "lane-manager-checkpoint-handoff-v1-20260618.json"
VALIDATION_JSON = REPORTS / "lane-manager-checkpoint-handoff-v1-validation-20260618.json"
REPORT_MD = REPORTS / "lane-manager-checkpoint-handoff-v1-20260618.md"

EXCLUDED_LANES = {"submitted_bounty_payouts"}

ZERO_BOUNDARY = {
    "report_only": True,
    "handoff_commands_written": 0,
    "handoff_commands_executed": 0,
    "tasks_created": 0,
    "tasks_acquired": 0,
    "tasks_updated": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "runtime_starts": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "public_actions": False,
    "payment_actions": False,
    "wallet_actions": False,
    "external_side_effects": False,
}
NEXT_ACTION = (
    "Use handoff rows to generate checkpoint/resume UI packets; do not create tasks, "
    "assign service requests, or start workers."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return value.startswith(str(ROOT)) and ".." not in value


def validation_ready(path: Path) -> bool:
    if not path.exists():
        return False
    data = load_json(path)
    return data.get("all_checks_passed") is True and data.get("failure_count") == 0


def lane_rows() -> list[dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT lane_id, department, owner_agent_id, status FROM lanes ORDER BY lane_id"
        ).fetchall()
        return [dict(row) for row in rows]


def expected_lane_ids(lanes: list[dict[str, Any]] | None = None) -> list[str]:
    rows = lanes if lanes is not None else lane_rows()
    return [
        row["lane_id"]
        for row in rows
        if row["status"] == "active"
        and row["lane_id"] not in EXCLUDED_LANES
        and row["owner_agent_id"]
    ]


def base_handoff(lane: dict[str, Any]) -> dict[str, Any]:
    lane_id = lane["lane_id"]
    return {
        "handoff_id": f"handoff-{lane_id.replace('_', '-')}-checkpoint-pause",
        "schema_version": "agent_company.lane_manager_checkpoint_handoff.v1",
        "lane_id": lane_id,
        "department": lane["department"],
        "manager_agent_id": lane["owner_agent_id"],
        "handoff_mode": "checkpoint_pause_only",
        "checkpoint_interrupt_required": True,
        "checkpoint_bridge_validation_path": str(BRIDGE_VALIDATION),
        "checkpoint_contract_validation_path": str(CHECKPOINT_VALIDATION),
        "ceo_review_path": str(CEO_REVIEW),
        "handoff_allowed": False,
        "worker_start_allowed": False,
        "service_request_mutation_allowed": False,
        "required_manager_steps": [
            "claim_lane",
            "acquire_task",
            "record_evidence",
            "request_service_worker_if_gate_needed",
            "stop_at_checkpoint_interrupt",
        ],
        "blocked_until": [
            "valid_checkpoint_interrupt_contract",
            "valid_checkpoint_interrupt_bridge_fixture",
            "explicit_task_creation_or_human_handoff",
            "service_request_gate_if_external_action_needed",
        ],
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set(lanes: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    source_lanes = copy.deepcopy(lanes) if lanes is not None else lane_rows()
    expected_ids = expected_lane_ids(source_lanes)
    fixtures = [
        {
            "name": "positive_all_owned_active_lane_handoffs",
            "expected": "accepted",
            "handoffs": [base_handoff(row) for row in source_lanes if row["lane_id"] in expected_ids],
        }
    ]

    def negative(name: str, mutate: Callable[[list[dict[str, Any]]], None]) -> None:
        rows = [base_handoff(row) for row in source_lanes if row["lane_id"] in expected_ids]
        mutate(rows)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "handoffs": rows})

    negative("missing_lane", lambda rows: rows.pop())
    negative(
        "submitted_payout_lane_included",
        lambda rows: rows.append(
            base_handoff(
                {
                    "lane_id": "submitted_bounty_payouts",
                    "department": "Revenue Collection",
                    "owner_agent_id": "other-worker",
                    "status": "active",
                }
            )
        ),
    )
    negative("missing_manager", lambda rows: rows[0].update({"manager_agent_id": ""}))
    negative("checkpoint_not_required", lambda rows: rows[0].update({"checkpoint_interrupt_required": False}))
    negative("handoff_allowed", lambda rows: rows[0].update({"handoff_allowed": True}))
    negative("worker_start_allowed", lambda rows: rows[0].update({"worker_start_allowed": True}))
    negative(
        "service_request_mutation_allowed",
        lambda rows: rows[0].update({"service_request_mutation_allowed": True}),
    )
    negative(
        "outside_bridge_validation",
        lambda rows: rows[0].update({"checkpoint_bridge_validation_path": r"C:\Temp\bridge.json"}),
    )
    negative("task_created_side_effect", lambda rows: rows[0]["runtime_boundary"].update({"tasks_created": 1}))
    negative(
        "service_request_assigned",
        lambda rows: rows[0]["runtime_boundary"].update({"service_requests_assigned": 1}),
    )
    negative("runtime_started", lambda rows: rows[0]["runtime_boundary"].update({"runtime_starts": 1}))
    negative("external_side_effect", lambda rows: rows[0]["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validate_handoff(
    row: dict[str, Any],
    schema: dict[str, Any],
    lane_map: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if schema.get("properties", {}).get("handoff_allowed", {}).get("const") is not False:
        errors.append("schema_must_force_handoff_allowed_false")
    if row.get("schema_version") != "agent_company.lane_manager_checkpoint_handoff.v1":
        errors.append("schema_version_mismatch")
    lane_id = str(row.get("lane_id", ""))
    if lane_id not in lane_map:
        errors.append("lane_id_not_found")
    if lane_id in EXCLUDED_LANES:
        errors.append("excluded_read_only_lane_must_not_be_handoff_row")
    lane = lane_map.get(lane_id, {})
    if lane and row.get("manager_agent_id") != lane.get("owner_agent_id"):
        errors.append("manager_agent_id_must_match_lane_owner")
    if not str(row.get("manager_agent_id", "")).strip():
        errors.append("manager_agent_id_missing")
    if row.get("handoff_mode") != "checkpoint_pause_only":
        errors.append("handoff_mode_must_be_checkpoint_pause_only")
    if row.get("checkpoint_interrupt_required") is not True:
        errors.append("checkpoint_interrupt_required_must_be_true")
    for key in ["checkpoint_bridge_validation_path", "checkpoint_contract_validation_path", "ceo_review_path"]:
        value = str(row.get(key, ""))
        if not value:
            errors.append(f"{key}_missing")
        elif not path_inside_root(value):
            errors.append(f"{key}_must_stay_inside_lab")
        elif not Path(value).exists():
            errors.append(f"{key}_not_found")
    if not validation_ready(Path(str(row.get("checkpoint_bridge_validation_path", "")))):
        errors.append("checkpoint_bridge_validation_not_ready")
    if not validation_ready(Path(str(row.get("checkpoint_contract_validation_path", "")))):
        errors.append("checkpoint_contract_validation_not_ready")
    if row.get("handoff_allowed") is not False:
        errors.append("handoff_allowed_must_be_false")
    if row.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")
    if row.get("service_request_mutation_allowed") is not False:
        errors.append("service_request_mutation_allowed_must_be_false")
    steps = row.get("required_manager_steps", [])
    for required in ["claim_lane", "acquire_task", "record_evidence", "stop_at_checkpoint_interrupt"]:
        if required not in steps:
            errors.append(f"required_manager_step_missing:{required}")
    boundary = row.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")
    return errors


def build_report(
    schema: dict[str, Any],
    fixtures: list[dict[str, Any]],
    *,
    lanes: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    lanes = copy.deepcopy(lanes) if lanes is not None else lane_rows()
    lane_map = {row["lane_id"]: row for row in lanes}
    expected_ids = expected_lane_ids(lanes)
    failures: list[str] = []
    results = []
    for fixture in fixtures:
        rows = (
            copy.deepcopy(fixture["handoffs"])
            if "handoffs" in fixture
            else load_json(Path(fixture["path"]))
        )
        row_errors: list[str] = []
        lane_ids = [row.get("lane_id") for row in rows]
        if sorted(lane_ids) != sorted(expected_ids):
            row_errors.append("handoff_lane_set_must_equal_owned_active_lanes_excluding_read_only_payouts")
        for row in rows:
            row_errors.extend(validate_handoff(row, schema, lane_map))
        accepted = not row_errors
        expected_accept = fixture["expected"] == "accepted"
        passed = accepted == expected_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        fixture_summary = {key: value for key, value in fixture.items() if key != "handoffs"}
        results.append(
            {
                **fixture_summary,
                "passed": passed,
                "row_count": len(rows),
                "result": {
                    "accepted_for_lane_manager_handoff": accepted,
                    "rejected": not accepted,
                    "errors": row_errors,
                },
            }
        )
    accepted_count = sum(1 for item in results if item["result"]["accepted_for_lane_manager_handoff"])
    rejected_count = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted_count != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted_count}")
    if rejected_count != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected_count}")
    if not validation_ready(BRIDGE_VALIDATION):
        failures.append("checkpoint_bridge_validation_not_ready")
    if not validation_ready(CHECKPOINT_VALIDATION):
        failures.append("checkpoint_contract_validation_not_ready")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.lane_manager_checkpoint_handoff_report.v1",
        "generated_utc": generated,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "expected_lane_count": len(expected_ids),
        "expected_lane_ids": expected_ids,
        "excluded_lanes": sorted(EXCLUDED_LANES),
        "source_bridge_validation": str(BRIDGE_VALIDATION),
        "source_checkpoint_validation": str(CHECKPOINT_VALIDATION),
        "fixture_count": len(fixtures),
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "results": results,
        "handoff_allowed": False,
        "worker_start_allowed": False,
        "service_request_mutation_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.lane_manager_checkpoint_handoff_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "expected_lane_count": len(expected_ids),
        "handoff_allowed": False,
        "worker_start_allowed": False,
        "service_request_mutation_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


