from __future__ import annotations

from typing import Any

from .ceo_decision_signed_apply_command_evaluator import evaluate_signed_apply_command_positive_fixture


def build_signed_apply_command_positive_runner_content(
    *,
    signed_fixture: dict[str, Any],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner_accepted_preview_only_no_mutation"
    recommended_default = "positive_apply_runner_still_requires_explicit_real_operator_approval_before_mutation"
    approval_granted_by_runner = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    apply_execution_allowed = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before

    result = evaluate_signed_apply_command_positive_fixture(
        signed_fixture,
        target_request_id=target_request_id,
    )
    positive_results = [
        {
            "fixture_id": signed_fixture.get("fixture_id"),
            "expected_accepted": signed_fixture.get("expected_accepted"),
            "actual_accepted": result["accepted"],
            "expected_preview_state": signed_fixture.get("expected_preview_state"),
            "actual_preview_state": result["preview_state"],
            "expected_real_mutation": signed_fixture.get("expected_real_mutation"),
            "actual_real_mutation_allowed": result["real_mutation_allowed"],
            "actual_rule_id": result["rule_id"],
            "matched_expected": (
                signed_fixture.get("expected_accepted") is True
                and result["accepted"] is True
                and signed_fixture.get("expected_preview_state") == result["preview_state"]
                and signed_fixture.get("expected_real_mutation") is False
                and result["real_mutation_allowed"] is False
            ),
        }
    ]
    runner_summary = (
        "Ran the local report-only positive runner for one signed operator apply command fixture. The fixture accepted into preview-only state while real mutation, approval, and apply execution stayed disabled."
    )
    runner_next_action = (
        "Keep real apply disabled; next produce an apply readiness closeout that lists the remaining explicit operator approval requirement before mutation can exist."
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
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "positive_results": positive_results,
        "positive_apply_command_execution_count": len(positive_results),
        "accepted_apply_fixture_count": sum(1 for item in positive_results if item.get("actual_accepted") is True),
        "rejected_apply_fixture_count": sum(1 for item in positive_results if item.get("actual_accepted") is False),
        "preview_state_match_count": sum(1 for item in positive_results if item.get("expected_preview_state") == item.get("actual_preview_state")),
        "real_mutation_allowed_count": sum(1 for item in positive_results if item.get("actual_real_mutation_allowed") is True),
        "approval_granted_by_runner": approval_granted_by_runner,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_after,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }



def build_signed_apply_command_positive_runner_artifacts(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_fixture_validation_path: str,
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixture_task_id": source_fixture_task_id,
        "source_fixture_evidence_id": source_fixture_evidence_id,
        "source_fixture_validation_path": source_fixture_validation_path,
        "positive_apply_command_execution_count": runner_content["positive_apply_command_execution_count"],
        "accepted_apply_fixture_count": runner_content["accepted_apply_fixture_count"],
        "rejected_apply_fixture_count": runner_content["rejected_apply_fixture_count"],
        "preview_state_match_count": runner_content["preview_state_match_count"],
        "real_mutation_allowed_count": runner_content["real_mutation_allowed_count"],
        "positive_results": runner_content["positive_results"],
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
        "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Positive Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{runner_content['local_decision']}`",
        "",
        str(runner_content["summary"]),
        "",
        "## Result",
        "",
        "| Fixture | Accepted | Preview State | Real Mutation Allowed | Match |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for item in runner_content["positive_results"]:
        md_lines.append(
            f"| `{item.get('fixture_id')}` | `{item.get('actual_accepted')}` | `{item.get('actual_preview_state')}` | `{item.get('actual_real_mutation_allowed')}` | `{item.get('matched_expected')}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner is report-only. It evaluates one local positive fixture and writes local artifacts only; it does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            str(runner_content["next_action"]),
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_signed_apply_command_positive_runner_artifacts", "build_signed_apply_command_positive_runner_content"]

