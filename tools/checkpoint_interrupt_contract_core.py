#!/usr/bin/env python3
"""Validate checkpoint interrupt contracts without resuming or applying work."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from runtime_boundary_shared_core import collect_runtime_boundary_errors


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
SCHEMA_PATH = ARCH / "checkpoint-interrupt-contract-v1.schema.json"
WAVE15_VALIDATION = REPORTS / "agent-company-current-source-radar-wave15-validation-20260617.json"
DOCKET_VALIDATION = REPORTS / "service-worker-operator-decision-docket-v1-validation-20260617.json"
APPLY_PREFLIGHT_VALIDATION = (
    REPORTS / "service-worker-signed-decision-apply-preflight-blocker-v1-validation-20260617.json"
)
FIXTURE_DIR = REPORTS / "checkpoint-interrupt-contract-v1-fixtures"
REPORT_JSON = REPORTS / "checkpoint-interrupt-contract-v1-20260617.json"
VALIDATION_JSON = REPORTS / "checkpoint-interrupt-contract-v1-validation-20260617.json"
REPORT_MD = REPORTS / "checkpoint-interrupt-contract-v1-20260617.md"

NEXT_ACTION = (
    "Use checkpoint interrupts as the pause/resume contract for lane-manager handoffs "
    "and service-worker decisions before any runtime/framework adoption."
)

ZERO_BOUNDARY = {
    "report_only": True,
    "resume_commands_written": 0,
    "resume_commands_executed": 0,
    "apply_commands_written": 0,
    "apply_commands_executed": 0,
    "approval_rows_written": 0,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "worker_starts": 0,
    "runtime_starts": 0,
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


def base_checkpoint(
    checkpoint_id: str,
    source_kind: str,
    lane_id: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "checkpoint_id": checkpoint_id,
        "schema_version": "agent_company.checkpoint_interrupt_contract.v1",
        "source_kind": source_kind,
        "lane_id": lane_id,
        "task_id": (
            "task-agent-company-current-source-radar-wave15-20260617"
            if source_kind != "service_request"
            else ""
        ),
        "service_request_id": (
            "req-next-wave-security-report-route-review-20260614"
            if source_kind == "service_request"
            else ""
        ),
        "interrupt_reason": reason,
        "manual_review_required": True,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        "required_artifacts": [
            str(WAVE15_VALIDATION),
            str(DOCKET_VALIDATION),
            str(APPLY_PREFLIGHT_VALIDATION),
        ],
        "source_research_validation_path": str(WAVE15_VALIDATION),
        "operator_docket_validation_path": str(DOCKET_VALIDATION),
        "apply_preflight_validation_path": str(APPLY_PREFLIGHT_VALIDATION),
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def fixture_set() -> list[dict[str, Any]]:
    fixtures = [
        {
            "name": "positive_service_request_gate",
            "expected": "accepted",
            "checkpoint": base_checkpoint(
                "checkpoint-service-worker-review-gate",
                "service_request",
                "security_bounty_private_reports",
                "service_worker_gate",
            ),
        },
        {
            "name": "positive_runtime_adoption_gate",
            "expected": "accepted",
            "checkpoint": base_checkpoint(
                "checkpoint-runtime-framework-adoption",
                "runtime_candidate",
                "platform_engineering",
                "runtime_adoption_gate",
            ),
        },
        {
            "name": "positive_lane_task_handoff",
            "expected": "accepted",
            "checkpoint": base_checkpoint(
                "checkpoint-lane-manager-handoff",
                "lane_task",
                "platform_engineering",
                "checkpoint_resume_guard",
            ),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        checkpoint = base_checkpoint(
            f"checkpoint-negative-{name}",
            "service_request",
            "security_bounty_private_reports",
            "service_worker_gate",
        )
        mutate(checkpoint)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "checkpoint": checkpoint})

    negative("wrong_schema_version", lambda c: c.update({"schema_version": "wrong"}))
    negative("unknown_source_kind", lambda c: c.update({"source_kind": "browser_session"}))
    negative("missing_lane", lambda c: c.update({"lane_id": ""}))
    negative("service_request_without_id", lambda c: c.update({"service_request_id": ""}))
    negative("lane_task_without_task", lambda c: c.update({"source_kind": "lane_task", "task_id": ""}))
    negative("manual_review_false", lambda c: c.update({"manual_review_required": False}))
    negative("resume_allowed", lambda c: c.update({"resume_allowed": True}))
    negative("apply_allowed", lambda c: c.update({"apply_allowed": True}))
    negative("worker_start_allowed", lambda c: c.update({"worker_start_allowed": True}))
    negative("missing_required_artifacts", lambda c: c.update({"required_artifacts": []}))
    negative("outside_required_artifact", lambda c: c.update({"required_artifacts": [r"C:\Temp\outside.json"]}))
    negative("missing_source_research", lambda c: c.update({"source_research_validation_path": ""}))
    negative("resume_command_written", lambda c: c["runtime_boundary"].update({"resume_commands_written": 1}))
    negative("service_request_updated", lambda c: c["runtime_boundary"].update({"service_requests_updated": 1}))
    negative("runtime_started", lambda c: c["runtime_boundary"].update({"runtime_starts": 1}))
    negative("external_side_effect", lambda c: c["runtime_boundary"].update({"external_side_effects": True}))
    return fixtures


def validation_ready(path: Path, key: str = "all_checks_passed") -> bool:
    if not path.exists():
        return False
    data = load_json(path)
    return data.get(key) is True and data.get("failure_count") == 0


def validate_checkpoint(checkpoint: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if schema.get("properties", {}).get("source_kind", {}).get("enum", [None])[0] != "lane_task":
        errors.append("schema_source_kind_enum_must_start_lane_task")
    if checkpoint.get("schema_version") != "agent_company.checkpoint_interrupt_contract.v1":
        errors.append("schema_version_mismatch")
    if checkpoint.get("source_kind") not in {"lane_task", "service_request", "runtime_candidate"}:
        errors.append("source_kind_unknown")
    if not str(checkpoint.get("lane_id", "")).strip():
        errors.append("lane_id_missing")
    if checkpoint.get("source_kind") == "service_request" and not str(checkpoint.get("service_request_id", "")).strip():
        errors.append("service_request_id_required_for_service_request_source")
    if checkpoint.get("source_kind") in {"lane_task", "runtime_candidate"} and not str(
        checkpoint.get("task_id", "")
    ).strip():
        errors.append("task_id_required_for_lane_or_runtime_source")
    allowed_interrupt_reasons = {
        "human_review_required",
        "service_worker_gate",
        "runtime_adoption_gate",
        "checkpoint_resume_guard",
    }
    if checkpoint.get("interrupt_reason") not in allowed_interrupt_reasons:
        errors.append("interrupt_reason_unknown")
    if checkpoint.get("manual_review_required") is not True:
        errors.append("manual_review_required_must_be_true")
    if checkpoint.get("resume_allowed") is not False:
        errors.append("resume_allowed_must_be_false")
    if checkpoint.get("apply_allowed") is not False:
        errors.append("apply_allowed_must_be_false")
    if checkpoint.get("worker_start_allowed") is not False:
        errors.append("worker_start_allowed_must_be_false")

    required = checkpoint.get("required_artifacts", [])
    if not isinstance(required, list) or not required:
        errors.append("required_artifacts_must_be_non_empty_list")
        required = []
    for path_value in required:
        path = str(path_value)
        if not path_inside_root(path):
            errors.append("required_artifact_must_stay_inside_lab")
        elif not Path(path).exists():
            errors.append("required_artifact_not_found")

    source_path = str(checkpoint.get("source_research_validation_path", ""))
    if not source_path:
        errors.append("source_research_validation_path_missing")
    elif not path_inside_root(source_path) or not Path(source_path).exists():
        errors.append("source_research_validation_path_invalid")
    elif not validation_ready(Path(source_path)):
        errors.append("source_research_validation_not_ready")
    operator_docket = checkpoint.get("operator_docket_validation_path")
    if operator_docket and not validation_ready(Path(str(operator_docket))):
        errors.append("operator_docket_validation_not_ready")
    apply_preflight = checkpoint.get("apply_preflight_validation_path")
    if apply_preflight and not validation_ready(Path(str(apply_preflight))):
        errors.append("apply_preflight_validation_not_ready")

    errors.extend(collect_runtime_boundary_errors(checkpoint, ZERO_BOUNDARY))

    accepted = not errors
    return {
        "checkpoint_id": checkpoint.get("checkpoint_id"),
        "source_kind": checkpoint.get("source_kind"),
        "interrupt_reason": checkpoint.get("interrupt_reason"),
        "accepted_for_checkpoint_interrupt": accepted,
        "rejected": not accepted,
        "errors": errors,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_report(schema: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    failures: list[str] = []
    results = []
    for fixture in fixtures:
        checkpoint = (
            copy.deepcopy(fixture["checkpoint"])
            if "checkpoint" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_checkpoint(checkpoint, schema)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_checkpoint_interrupt"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})
    accepted = sum(1 for item in results if item["result"]["accepted_for_checkpoint_interrupt"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    source_state = {
        "wave15_validation_ready": validation_ready(WAVE15_VALIDATION),
        "operator_docket_validation_ready": validation_ready(DOCKET_VALIDATION),
        "apply_preflight_validation_ready": validation_ready(APPLY_PREFLIGHT_VALIDATION),
    }
    if not all(source_state.values()):
        failures.append("one_or_more_source_validations_not_ready")
    report = {
        "schema_version": "agent_company.checkpoint_interrupt_contract_report.v1",
        "generated_utc": generated,
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "source_state": source_state,
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "results": results,
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.checkpoint_interrupt_contract_validation.v1",
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
        "resume_allowed": False,
        "apply_allowed": False,
        "worker_start_allowed": False,
        **copy.deepcopy(ZERO_BOUNDARY),
        "failures": failures,
    }
    return report, validation


