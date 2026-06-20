"""Pure result builders for the CEO apply-readiness positive runner."""

from __future__ import annotations

from typing import Any

from .ceo_decision_apply_readiness_evaluator import evaluate_ceo_apply_readiness_packet


def build_positive_readiness_runner_content(
    positive_readiness_fixture: dict[str, Any],
    readiness_packet: dict[str, Any],
) -> dict[str, Any]:
    result = evaluate_ceo_apply_readiness_packet(readiness_packet, require_preview_apply_boundary=True)
    readiness_guard_results = [
        {
            "fixture_id": positive_readiness_fixture.get("fixture_id"),
            "expected_accepted": positive_readiness_fixture.get("expected_accepted"),
            "actual_accepted": result.get("accepted_readiness"),
            "expected_preview_state": positive_readiness_fixture.get("expected_preview_state"),
            "actual_preview_state": result.get("preview_state"),
            "expected_real_mutation": positive_readiness_fixture.get("expected_real_mutation"),
            "actual_real_mutation_allowed": result.get("real_mutation_allowed"),
            "actual_rule_id": result.get("rule_id"),
            "matched_expected": (
                positive_readiness_fixture.get("expected_accepted") is True
                and result.get("accepted_readiness") is True
                and positive_readiness_fixture.get("expected_preview_state") == result.get("preview_state")
                and positive_readiness_fixture.get("expected_real_mutation") is False
                and result.get("real_mutation_allowed") is False
            ),
        }
    ]
    runner_summary = (
        "Ran the local report-only apply-readiness positive runner against one valid readiness packet. The packet passed the guard into preview-only state while real mutation stayed disabled."
    )
    runner_next_action = (
        "Keep real apply disabled; only a separate explicit operator apply approval may authorize the service-request field update command."
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
        "local_decision": "ceo_decision_parser_apply_readiness_positive_runner_passed_preview_only",
        "recommended_default": "positive_runner_still_requires_separate_operator_apply_approval",
        "mutation_applied_count": 0,
        "queue_mutation_count": 0,
        "approval_request_count": 0,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
        "readiness_guard_results": readiness_guard_results,
        "readiness_guard_execution_count": len(readiness_guard_results),
        "accepted_readiness_count": sum(1 for item in readiness_guard_results if item.get("actual_accepted") is True),
        "rejected_readiness_count": sum(1 for item in readiness_guard_results if item.get("actual_accepted") is False),
        "expected_acceptance_match_count": sum(1 for item in readiness_guard_results if item.get("matched_expected") is True),
        "preview_state_match_count": sum(
            1
            for item in readiness_guard_results
            if item.get("expected_preview_state") == item.get("actual_preview_state")
        ),
        "real_mutation_allowed_count": sum(
            1 for item in readiness_guard_results if item.get("actual_real_mutation_allowed") is True
        ),
    }



def build_positive_readiness_runner_artifacts(
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
    positive_readiness_fixture_count: int,
    target_service_request_count: int,
    planned_field_update_count: int,
    rollback_check_count: int,
    required_operator_approval_count: int,
    target_status_before: Any,
    target_status_after: Any,
    runner_content: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_positive_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixture_task_id": source_fixture_task_id,
        "source_fixture_evidence_id": source_fixture_evidence_id,
        "source_fixture_validation_path": source_fixture_validation_path,
        "positive_readiness_fixture_count": positive_readiness_fixture_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": planned_field_update_count,
        "rollback_check_count": rollback_check_count,
        "required_operator_approval_count": required_operator_approval_count,
        "readiness_guard_execution_count": runner_content["readiness_guard_execution_count"],
        "accepted_readiness_count": runner_content["accepted_readiness_count"],
        "rejected_readiness_count": runner_content["rejected_readiness_count"],
        "expected_acceptance_match_count": runner_content["expected_acceptance_match_count"],
        "preview_state_match_count": runner_content["preview_state_match_count"],
        "real_mutation_allowed_count": runner_content["real_mutation_allowed_count"],
        "mutation_applied_count": runner_content["mutation_applied_count"],
        "queue_mutation_count": runner_content["queue_mutation_count"],
        "approval_request_count": runner_content["approval_request_count"],
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "readiness_guard_results": runner_content["readiness_guard_results"],
        "local_decision": runner_content["local_decision"],
        "recommended_default": runner_content["recommended_default"],
        "summary": runner_content["summary"],
        "next_action": runner_content["next_action"],
        "runtime_boundary": runner_content["runtime_boundary"],
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Positive Runner",
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
        "## Guard Result",
        "",
        "| Fixture | Accepted | Preview State | Real Mutation Allowed | Match |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for item in runner_content["readiness_guard_results"]:
        md_lines.append(
            f"| `{item.get('fixture_id')}` | `{item.get('actual_accepted')}` | `{item.get('actual_preview_state')}` | `{item.get('actual_real_mutation_allowed')}` | `{item.get('matched_expected')}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner is report-only. It evaluated a local positive readiness fixture and wrote local artifacts only; it did not mutate service requests, assign work, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            str(runner_content["next_action"]),
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_positive_readiness_runner_artifacts", "build_positive_readiness_runner_content"]


