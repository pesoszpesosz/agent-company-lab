"""Pure content builders for signed apply-command closeout reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REMAINING_APPLY_COMMAND_CLOSEOUT_GATES = [
    "real_operator_signature_not_fixture_placeholder",
    "operator_approval_expiration_and_scope_review",
    "explicit_permission_to_mutate_service_request_fields",
    "fresh_target_updated_at_snapshot_at_apply_time",
    "separate_mutation_implementation_and_rollback_review",
]


def build_signed_apply_command_closeout_content(source_validations: list[dict[str, Any]]) -> dict[str, Any]:
    source_validation_results = []
    for item in source_validations:
        data = item["validation"]
        source_validation_results.append(
            {
                "id": item["id"],
                "task_id": item["task_id"],
                "path": str(item["path"]),
                "schema_version": data.get("schema_version"),
                "all_checks_passed": data.get("all_checks_passed"),
                "failure_count": data.get("failure_count"),
                "apply_command_enabled": data.get("apply_command_enabled"),
                "apply_execution_allowed": data.get("apply_execution_allowed"),
                "service_requests_updated": data.get("service_requests_updated"),
                "service_requests_assigned": data.get("service_requests_assigned"),
            }
        )
    passed_source_validation_count = sum(
        1
        for item in source_validation_results
        if item.get("all_checks_passed") is True
        and item.get("failure_count") == 0
        and item.get("apply_command_enabled") is False
        and item.get("apply_execution_allowed") is False
    )
    closeout_summary = (
        "Closed out the local signed-decision apply-command readiness ladder. Contract, negative fixtures, guard runner, and positive runner all pass locally, but real mutation remains parked behind explicit operator approval."
    )
    closeout_next_action = (
        "Do not implement or run a mutating apply command until a real operator approval replaces fixture data and the remaining gates are reviewed."
    )
    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    return {
        "apply_command_closeout_count": 1,
        "source_validation_results": source_validation_results,
        "source_validation_count": len(source_validation_results),
        "passed_source_validation_count": passed_source_validation_count,
        "remaining_gates": REMAINING_APPLY_COMMAND_CLOSEOUT_GATES,
        "remaining_gate_count": len(REMAINING_APPLY_COMMAND_CLOSEOUT_GATES),
        "ready_for_real_mutation": False,
        "approval_granted_by_closeout": False,
        "explicit_operator_apply_approval_present": False,
        "apply_command_enabled": False,
        "apply_execution_allowed": False,
        "mutation_applied_count": 0,
        "queue_mutation_count": 0,
        "approval_request_count": 0,
        "summary": closeout_summary,
        "next_action": closeout_next_action,
        "runtime_boundary": runtime_boundary,
    }


def build_signed_apply_command_closeout_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    closeout_task_id: str,
    closeout_evidence_id: str,
    source_positive_runner_task_id: str,
    source_positive_runner_evidence_id: str,
    target_request_id: str,
    target_status_before: str | None,
    target_status_after: str | None,
    closeout_content: dict[str, Any],
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout_parked_waiting_for_real_operator_approval"
    recommended_default = "do_not_implement_or_run_mutating_apply_until_real_operator_approval_is_supplied"
    closeout_summary = closeout_content["summary"]
    closeout_next_action = closeout_content["next_action"]
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout.v1",
        "generated_utc": generated_utc,
        "closeout_lane_id": lane_id,
        "closeout_task_id": closeout_task_id,
        "closeout_evidence_id": closeout_evidence_id,
        "source_positive_runner_task_id": source_positive_runner_task_id,
        "source_positive_runner_evidence_id": source_positive_runner_evidence_id,
        "apply_command_closeout_count": closeout_content["apply_command_closeout_count"],
        "source_validation_count": closeout_content["source_validation_count"],
        "passed_source_validation_count": closeout_content["passed_source_validation_count"],
        "source_validation_results": closeout_content["source_validation_results"],
        "remaining_gate_count": closeout_content["remaining_gate_count"],
        "remaining_gates": closeout_content["remaining_gates"],
        "ready_for_real_mutation": closeout_content["ready_for_real_mutation"],
        "approval_granted_by_closeout": closeout_content["approval_granted_by_closeout"],
        "explicit_operator_apply_approval_present": closeout_content["explicit_operator_apply_approval_present"],
        "apply_command_enabled": closeout_content["apply_command_enabled"],
        "apply_execution_allowed": closeout_content["apply_execution_allowed"],
        "mutation_applied_count": closeout_content["mutation_applied_count"],
        "queue_mutation_count": closeout_content["queue_mutation_count"],
        "approval_request_count": closeout_content["approval_request_count"],
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": closeout_summary,
        "next_action": closeout_next_action,
        "runtime_boundary": closeout_content["runtime_boundary"],
    }

    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Closeout",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        closeout_summary,
        "",
        "## Source Validations",
        "",
        "| Source | Passed | Failure Count | Apply Enabled | Execution Allowed |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for item in closeout_content["source_validation_results"]:
        md_lines.append(
            f"| `{item['id']}` | `{item['all_checks_passed']}` | `{item['failure_count']}` | `{item['apply_command_enabled']}` | `{item['apply_execution_allowed']}` |"
        )
    md_lines.extend(["", "## Remaining Gates", ""])
    md_lines.extend(f"- `{gate}`" for gate in closeout_content["remaining_gates"])
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This closeout is local-only. It does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            closeout_next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "REMAINING_APPLY_COMMAND_CLOSEOUT_GATES",
    "build_signed_apply_command_closeout_artifacts",
    "build_signed_apply_command_closeout_content",
]
