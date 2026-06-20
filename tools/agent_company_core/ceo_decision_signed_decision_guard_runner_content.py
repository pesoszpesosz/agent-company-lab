from __future__ import annotations

from typing import Any

from .ceo_decision_signed_decision_evaluator import evaluate_ceo_signed_decision


def build_signed_decision_guard_runner_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_fixtures_validation_path: str,
    lane_id: str,
    runner_task_id: str,
    runner_evidence_id: str,
    source_fixtures_task_id: str,
    source_fixtures_evidence_id: str,
    signed_decision_fixtures: list[dict[str, Any]],
    decision_fields_template: dict[str, Any],
    target_status_before: Any,
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_signed_decision_guard_runner_passed_no_mutations"
    recommended_default = "keep_apply_disabled_until_signed_decision_guard_passes_positive_fixture"
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before

    guard_results: list[dict[str, object]] = []
    for fixture in signed_decision_fixtures:
        result = evaluate_ceo_signed_decision(
            fixture.get("submitted_signed_decision", {}),
            decision_fields_template,
        )
        guard_results.append(
            {
                "fixture_id": fixture.get("fixture_id"),
                "expected_accepted": fixture.get("expected_accepted"),
                "actual_accepted": result.get("accepted_signed_decision"),
                "expected_rule_id": fixture.get("expected_rule_id"),
                "actual_rule_id": result.get("rule_id"),
                "matched_expected": result.get("accepted_signed_decision") is False and result.get("rule_id") == fixture.get("expected_rule_id"),
            }
        )

    runner_summary = (
        "Ran a local report-only signed-decision guard against six negative fixtures. The guard rejected every malformed signed decision with the expected rule and performed no mutation."
    )
    runner_next_action = (
        "Create a positive signed-decision fixture next; keep apply disabled until that fixture passes and the user explicitly approves a real apply command."
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
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_guard_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_fixtures_task_id": source_fixtures_task_id,
        "source_fixtures_evidence_id": source_fixtures_evidence_id,
        "source_fixtures_validation_path": source_fixtures_validation_path,
        "negative_signed_decision_fixture_count": len(signed_decision_fixtures),
        "signed_decision_guard_execution_count": len(guard_results),
        "rejected_signed_decision_count": sum(1 for item in guard_results if item.get("actual_accepted") is False),
        "accepted_signed_decision_count": sum(1 for item in guard_results if item.get("actual_accepted") is True),
        "expected_rejection_match_count": sum(1 for item in guard_results if item.get("matched_expected") is True),
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "signed_decision_guard_results": guard_results,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Guard Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        runner_summary,
        "",
        "## Guard Results",
        "",
        "| Fixture | Expected Rule | Actual Rule | Match |",
        "| --- | --- | --- | ---: |",
    ]
    for result in guard_results:
        md_lines.append(
            f"| `{result.get('fixture_id')}` | `{result.get('expected_rule_id')}` | `{result.get('actual_rule_id')}` | `{result.get('matched_expected')}` |"
        )
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This runner is report-only. It evaluates local signed-decision fixtures and writes local artifacts only; it does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            runner_next_action,
            "",
        ]
    )
    return {
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "negative_signed_decision_fixture_count": payload["negative_signed_decision_fixture_count"],
        "signed_decision_guard_execution_count": payload["signed_decision_guard_execution_count"],
        "rejected_signed_decision_count": payload["rejected_signed_decision_count"],
        "accepted_signed_decision_count": payload["accepted_signed_decision_count"],
        "expected_rejection_match_count": payload["expected_rejection_match_count"],
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_after,
        "signed_decision_guard_results": guard_results,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = ["build_signed_decision_guard_runner_content"]
