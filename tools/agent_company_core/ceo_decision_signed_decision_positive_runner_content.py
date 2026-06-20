from __future__ import annotations

from typing import Any

from .ceo_decision_signed_decision_evaluator import evaluate_ceo_signed_decision


def build_signed_decision_positive_runner_content(
    *,
    positive_fixture: dict[str, Any],
    decision_fields_template: dict[str, Any],
    target_status_before: str | None,
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_signed_decision_positive_runner_passed_preview_only"
    recommended_default = "positive_signed_decision_runner_still_requires_separate_operator_apply_approval"
    apply_command_enabled = False
    approval_granted_by_runner = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before
    positive_signed_decision_fixture_count = 1 if positive_fixture else 0
    submitted_signed_decision = positive_fixture.get("submitted_signed_decision", {})

    result = evaluate_ceo_signed_decision(
        submitted_signed_decision,
        decision_fields_template,
        include_preview_state=True,
    )
    signed_decision_positive_results = [
        {
            "fixture_id": positive_fixture.get("fixture_id"),
            "expected_accepted": positive_fixture.get("expected_accepted"),
            "actual_accepted": result.get("accepted_signed_decision"),
            "expected_preview_state": positive_fixture.get("expected_preview_state"),
            "actual_preview_state": result.get("preview_state"),
            "expected_real_mutation": positive_fixture.get("expected_real_mutation"),
            "actual_real_mutation_allowed": result.get("real_mutation_allowed"),
            "actual_rule_id": result.get("rule_id"),
            "matched_expected": (
                positive_fixture.get("expected_accepted") is True
                and result.get("accepted_signed_decision") is True
                and positive_fixture.get("expected_preview_state") == result.get("preview_state")
                and positive_fixture.get("expected_real_mutation") is False
                and result.get("real_mutation_allowed") is False
            ),
        }
    ]
    runner_summary = (
        "Ran the local report-only positive signed-decision runner against one valid signed-decision fixture. The fixture passed into preview-only state while apply stayed disabled and no real approval was granted."
    )
    runner_next_action = (
        "Keep real apply disabled; only a separate explicit operator approval may authorize any service-request field update command."
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
        "positive_signed_decision_fixture_count": positive_signed_decision_fixture_count,
        "signed_decision_positive_results": signed_decision_positive_results,
        "signed_decision_positive_execution_count": len(signed_decision_positive_results),
        "accepted_signed_decision_count": sum(1 for item in signed_decision_positive_results if item.get("actual_accepted") is True),
        "rejected_signed_decision_count": sum(1 for item in signed_decision_positive_results if item.get("actual_accepted") is False),
        "expected_acceptance_match_count": sum(1 for item in signed_decision_positive_results if item.get("matched_expected") is True),
        "preview_state_match_count": sum(1 for item in signed_decision_positive_results if item.get("expected_preview_state") == item.get("actual_preview_state")),
        "real_mutation_allowed_count": sum(1 for item in signed_decision_positive_results if item.get("actual_real_mutation_allowed") is True),
        "apply_command_enabled": apply_command_enabled,
        "approval_granted_by_runner": approval_granted_by_runner,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }



def build_signed_decision_positive_runner_artifacts(
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
    runner_content: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_positive_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixture_task_id": source_fixture_task_id,
        "source_fixture_evidence_id": source_fixture_evidence_id,
        "source_fixture_validation_path": source_fixture_validation_path,
        "positive_signed_decision_fixture_count": runner_content["positive_signed_decision_fixture_count"],
        "signed_decision_positive_execution_count": runner_content["signed_decision_positive_execution_count"],
        "accepted_signed_decision_count": runner_content["accepted_signed_decision_count"],
        "rejected_signed_decision_count": runner_content["rejected_signed_decision_count"],
        "expected_acceptance_match_count": runner_content["expected_acceptance_match_count"],
        "preview_state_match_count": runner_content["preview_state_match_count"],
        "real_mutation_allowed_count": runner_content["real_mutation_allowed_count"],
        "apply_command_enabled": runner_content["apply_command_enabled"],
        "approval_granted_by_runner": runner_content["approval_granted_by_runner"],
        "mutation_applied_count": runner_content["mutation_applied_count"],
        "queue_mutation_count": runner_content["queue_mutation_count"],
        "approval_request_count": runner_content["approval_request_count"],
        "target_status_before": runner_content["target_status_before"],
        "target_status_after": runner_content["target_status_after"],
        "signed_decision_positive_results": runner_content["signed_decision_positive_results"],
        "local_decision": runner_content["local_decision"],
        "recommended_default": runner_content["recommended_default"],
        "summary": runner_content["summary"],
        "next_action": runner_content["next_action"],
        "runtime_boundary": runner_content["runtime_boundary"],
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Positive Runner",
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
    for item in runner_content["signed_decision_positive_results"]:
        md_lines.append(
            f"| `{item.get('fixture_id')}` | `{item.get('actual_accepted')}` | `{item.get('actual_preview_state')}` | `{item.get('actual_real_mutation_allowed')}` | `{item.get('matched_expected')}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner is report-only. It evaluates one local positive signed-decision fixture and writes local artifacts only; it does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            str(runner_content["next_action"]),
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_signed_decision_positive_runner_artifacts", "build_signed_decision_positive_runner_content"]

