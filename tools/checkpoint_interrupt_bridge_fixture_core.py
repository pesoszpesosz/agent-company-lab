#!/usr/bin/env python3
"""Validate local checkpoint interrupt bridge fixtures without importing LangGraph."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "checkpoint-interrupt-bridge-fixture-v1.schema.json"
SCORECARD = REPORTS / "adapter-candidate-scorecard-v1-20260617.json"
SCORECARD_VALIDATION = REPORTS / "adapter-candidate-scorecard-v1-validation-20260617.json"
CHECKPOINT_VALIDATION = REPORTS / "checkpoint-interrupt-contract-v1-validation-20260617.json"
FIXTURE_DIR = REPORTS / "checkpoint-interrupt-bridge-fixture-v1-fixtures"
REPORT_JSON = REPORTS / "checkpoint-interrupt-bridge-fixture-v1-20260617.json"
VALIDATION_JSON = REPORTS / "checkpoint-interrupt-bridge-fixture-v1-validation-20260617.json"
REPORT_MD = REPORTS / "checkpoint-interrupt-bridge-fixture-v1-20260617.md"

RECOMMENDED_NEXT_ACTION = (
    "Use this bridge as report-only scaffolding for future checkpoint/resume UI "
    "or lane-manager handoff fixtures; do not install LangGraph."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "external_framework_imports": 0,
    "dependency_installs": 0,
    "runtime_starts": 0,
    "graph_nodes_executed": 0,
    "checkpoint_resumes": 0,
    "resume_commands_written": 0,
    "resume_commands_executed": 0,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "model_api_calls": False,
    "mcp_tool_calls": False,
    "public_actions": False,
    "payment_actions": False,
    "wallet_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_inside_root(value: str) -> bool:
    return value.startswith(str(ROOT)) and ".." not in value


def base_bridge(bridge_id: str = "checkpoint-bridge-langgraph-pattern-local") -> dict[str, Any]:
    return {
        "bridge_id": bridge_id,
        "schema_version": "agent_company.checkpoint_interrupt_bridge_fixture.v1",
        "source_candidate": "langchain-ai/langgraph",
        "source_candidate_rank": 1,
        "source_candidate_url": "https://github.com/langchain-ai/langgraph",
        "bridge_mode": "local_fixture_only",
        "local_adapter_kind": "checkpoint_interrupt_bridge_fixture",
        "checkpoint_contract_validation_path": str(CHECKPOINT_VALIDATION),
        "scorecard_validation_path": str(SCORECARD_VALIDATION),
        "maps_to_checkpoint_interrupt_contract": True,
        "mapped_concepts": {
            "graph_node": "lane_task_or_service_worker_step",
            "interrupt": "checkpoint_interrupt_contract_v1",
            "checkpoint_state": "sqlite_task_artifact_outcome_trace_rows",
            "resume": "blocked_until_signed_operator_decision_and_apply_preflight",
        },
        "required_followup_gates": [
            "checkpoint_interrupt_contract_v1",
            "runtime_start_preflight",
            "signed_operator_runtime_decision",
            "model_api_execution_gate",
            "dependency_install_gate",
        ],
        "runtime_adoption_allowed": False,
        "dependency_install_allowed": False,
        "dependency_import_allowed": False,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_langgraph_checkpoint_bridge_fixture",
            "expected": "accepted",
            "bridge": base_bridge(),
        }
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        bridge = base_bridge(f"checkpoint-bridge-negative-{name}")
        mutate(bridge)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "bridge": bridge})

    negative("wrong_candidate", lambda b: b.update({"source_candidate": "temporalio/temporal"}))
    negative("wrong_rank", lambda b: b.update({"source_candidate_rank": 2}))
    negative("runtime_mode_live", lambda b: b.update({"bridge_mode": "runtime_adapter"}))
    negative("not_mapped_to_checkpoint", lambda b: b.update({"maps_to_checkpoint_interrupt_contract": False}))
    negative("runtime_adoption_allowed", lambda b: b.update({"runtime_adoption_allowed": True}))
    negative("dependency_install_allowed", lambda b: b.update({"dependency_install_allowed": True}))
    negative("dependency_import_allowed", lambda b: b.update({"dependency_import_allowed": True}))
    negative("resume_allowed", lambda b: b.update({"resume_allowed": True}))
    negative("apply_allowed", lambda b: b.update({"apply_allowed": True}))
    negative("worker_start_allowed", lambda b: b.update({"worker_start_allowed": True}))
    negative("missing_checkpoint_validation", lambda b: b.update({"checkpoint_contract_validation_path": ""}))
    negative(
        "outside_scorecard_validation",
        lambda b: b.update({"scorecard_validation_path": r"C:\Temp\scorecard.json"}),
    )
    negative("external_framework_import", lambda b: b["runtime_boundary"].update({"external_framework_imports": 1}))
    negative("runtime_started", lambda b: b["runtime_boundary"].update({"runtime_starts": 1}))
    negative("graph_node_executed", lambda b: b["runtime_boundary"].update({"graph_nodes_executed": 1}))
    negative("checkpoint_resumed", lambda b: b["runtime_boundary"].update({"checkpoint_resumes": 1}))
    negative("model_api_called", lambda b: b["runtime_boundary"].update({"model_api_calls": True}))
    negative("service_request_updated", lambda b: b["runtime_boundary"].update({"service_requests_updated": 1}))
    negative("external_side_effect", lambda b: b["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validation_ready(path: Path) -> bool:
    if not path.exists():
        return False
    data = load_json(path)
    return data.get("all_checks_passed") is True and data.get("failure_count") == 0


def top_candidate_is_langgraph() -> bool:
    if not SCORECARD.exists():
        return False
    rows = load_json(SCORECARD).get("candidate_rows", [])
    return bool(
        rows
        and rows[0].get("repo") == "langchain-ai/langgraph"
        and rows[0].get("first_local_adapter") == "checkpoint_interrupt_bridge_fixture"
    )


def validate_bridge(bridge: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if schema.get("properties", {}).get("source_candidate", {}).get("const") != "langchain-ai/langgraph":
        errors.append("schema_must_pin_langgraph_candidate")
    if bridge.get("schema_version") != "agent_company.checkpoint_interrupt_bridge_fixture.v1":
        errors.append("schema_version_mismatch")
    if bridge.get("source_candidate") != "langchain-ai/langgraph":
        errors.append("source_candidate_must_be_langgraph")
    if bridge.get("source_candidate_rank") != 1:
        errors.append("source_candidate_rank_must_be_1")
    if bridge.get("bridge_mode") != "local_fixture_only":
        errors.append("bridge_mode_must_be_local_fixture_only")
    if bridge.get("local_adapter_kind") != "checkpoint_interrupt_bridge_fixture":
        errors.append("local_adapter_kind_mismatch")
    if bridge.get("maps_to_checkpoint_interrupt_contract") is not True:
        errors.append("maps_to_checkpoint_interrupt_contract_must_be_true")

    for key in ["checkpoint_contract_validation_path", "scorecard_validation_path"]:
        value = str(bridge.get(key, ""))
        if not value:
            errors.append(f"{key}_missing")
        elif not path_inside_root(value):
            errors.append(f"{key}_must_stay_inside_lab")
        elif not validation_ready(Path(value)):
            errors.append(f"{key}_not_ready")

    if not top_candidate_is_langgraph():
        errors.append("scorecard_top_candidate_not_langgraph_checkpoint_bridge")
    if bridge.get("runtime_adoption_allowed") is not False:
        errors.append("runtime_adoption_allowed_must_be_false")
    if bridge.get("dependency_install_allowed") is not False:
        errors.append("dependency_install_allowed_must_be_false")
    if bridge.get("dependency_import_allowed") is not False:
        errors.append("dependency_import_allowed_must_be_false")
    if bridge.get("resume_allowed") is not False:
        errors.append("resume_allowed_must_be_false")
    if bridge.get("apply_allowed") is not False:
        errors.append("apply_allowed_must_be_false")
    if bridge.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")
    if "checkpoint_interrupt_contract_v1" not in bridge.get("required_followup_gates", []):
        errors.append("required_followup_gates_must_include_checkpoint_interrupt_contract_v1")

    boundary = bridge.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in ZERO_BOUNDARY.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    accepted = not errors
    return {
        "bridge_id": bridge.get("bridge_id"),
        "source_candidate": bridge.get("source_candidate"),
        "accepted_for_local_bridge_fixture": accepted,
        "rejected": not accepted,
        "errors": errors,
        "runtime_adoption_allowed": False,
        "dependency_install_allowed": False,
        "dependency_import_allowed": False,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    failures: list[str] = []
    results = []
    for fixture in fixtures:
        bridge = (
            copy.deepcopy(fixture["bridge"])
            if "bridge" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_bridge(bridge, schema)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_local_bridge_fixture"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})
    accepted = sum(1 for item in results if item["result"]["accepted_for_local_bridge_fixture"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    source_state = {
        "scorecard_validation_ready": validation_ready(SCORECARD_VALIDATION),
        "checkpoint_validation_ready": validation_ready(CHECKPOINT_VALIDATION),
        "scorecard_top_candidate_langgraph": top_candidate_is_langgraph(),
    }
    if not all(source_state.values()):
        failures.append("one_or_more_source_preconditions_not_ready")
    report = {
        "schema_version": "agent_company.checkpoint_interrupt_bridge_fixture_report.v1",
        "generated_utc": generated,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_scorecard_path": str(SCORECARD),
        "source_scorecard_validation_path": str(SCORECARD_VALIDATION),
        "source_checkpoint_validation_path": str(CHECKPOINT_VALIDATION),
        "source_state": source_state,
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "results": results,
        "recommended_next_action": RECOMMENDED_NEXT_ACTION,
        "runtime_adoption_allowed": False,
        "dependency_install_allowed": False,
        "dependency_import_allowed": False,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }
    validation = {
        "schema_version": "agent_company.checkpoint_interrupt_bridge_fixture_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "runtime_adoption_allowed": False,
        "dependency_install_allowed": False,
        "dependency_import_allowed": False,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


