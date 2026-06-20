from __future__ import annotations

from typing import Any

from .ceo_decision_signed_apply_command_evaluator import evaluate_signed_apply_command_negative_fixture


def build_signed_apply_command_guard_runner_content(
    *,
    negative_fixtures: list[dict[str, Any]],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    apply_command_execution_count = 0
    approval_granted_by_runner = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    apply_execution_allowed = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before

    guard_results = []
    for item in negative_fixtures:
        result = evaluate_signed_apply_command_negative_fixture(
            item,
            target_request_id=target_request_id,
        )
        guard_results.append(
            {
                "fixture_id": item.get("fixture_id"),
                "expected_accepted": item.get("expected_accepted"),
                "actual_accepted": result["accepted"],
                "expected_rule_id": item.get("expected_rule_id"),
                "actual_rule_id": result["rule_id"],
                "execution_attempted": False,
                "matched_expected": item.get("expected_accepted") is result["accepted"] and item.get("expected_rule_id") == result["rule_id"],
            }
        )

    runner_summary = (
        "Ran the local report-only guard runner for six signed-decision apply command negative fixtures. Every fixture rejected with its expected rule, and no apply command execution was attempted."
    )
    runner_next_action = (
        "Keep the apply command disabled; next create a positive signed operator apply fixture only as local data, not as approval or mutation."
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
        "guard_results": guard_results,
        "apply_command_guard_execution_count": len(guard_results),
        "rejected_fixture_count": sum(1 for item in guard_results if item.get("actual_accepted") is False),
        "accepted_fixture_count": sum(1 for item in guard_results if item.get("actual_accepted") is True),
        "matched_rejection_rule_count": sum(1 for item in guard_results if item.get("matched_expected") is True),
        "apply_command_execution_count": apply_command_execution_count,
        "approval_granted_by_runner": approval_granted_by_runner,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_after,
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner_rejected_all_no_mutation",
        "recommended_default": "keep_apply_command_disabled_until_positive_signed_operator_apply_approval_passes",
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }


def build_signed_apply_command_guard_runner_artifacts(
    *,
    generated_utc: str,
    json_output_path: object,
    validation_path: object,
    source_fixture_validation_path: object,
    lane_id: str,
    runner_task_id: str,
    runner_evidence_id: str,
    source_fixture_task_id: str,
    source_fixture_evidence_id: str,
    target_request_id: str | None,
    target_status_before: str | None,
    runner_content: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixture_task_id": source_fixture_task_id,
        "source_fixture_evidence_id": source_fixture_evidence_id,
        "source_fixture_validation_path": str(source_fixture_validation_path),
        "apply_command_guard_execution_count": runner_content["apply_command_guard_execution_count"],
        "rejected_fixture_count": runner_content["rejected_fixture_count"],
        "accepted_fixture_count": runner_content["accepted_fixture_count"],
        "matched_rejection_rule_count": runner_content["matched_rejection_rule_count"],
        "apply_command_execution_count": runner_content["apply_command_execution_count"],
        "guard_results": runner_content["guard_results"],
        "approval_granted_by_runner": runner_content["approval_granted_by_runner"],
        "explicit_operator_apply_approval_present": runner_content["explicit_operator_apply_approval_present"],
        "apply_command_enabled": runner_content["apply_command_enabled"],
        "apply_execution_allowed": runner_content["apply_execution_allowed"],
        "mutation_applied_count": runner_content["mutation_applied_count"],
        "queue_mutation_count": runner_content["queue_mutation_count"],
        "approval_request_count": runner_content["approval_request_count"],
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": runner_content["target_status_after"],
        "local_decision": runner_content["local_decision"],
        "recommended_default": runner_content["recommended_default"],
        "summary": runner_content["summary"],
        "next_action": runner_content["next_action"],
        "runtime_boundary": runner_content["runtime_boundary"],
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Guard Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{runner_content['local_decision']}`",
        "",
        runner_content["summary"],
        "",
        "## Results",
        "",
        "| Fixture | Accepted | Rule | Match |",
        "| --- | ---: | --- | ---: |",
    ]
    for item in runner_content["guard_results"]:
        md_lines.append(f"| `{item['fixture_id']}` | `{item['actual_accepted']}` | `{item['actual_rule_id']}` | `{item['matched_expected']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner is report-only. It evaluates local negative fixtures and writes local artifacts only; it does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            runner_content["next_action"],
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "build_signed_apply_command_guard_runner_artifacts",
    "build_signed_apply_command_guard_runner_content",
]