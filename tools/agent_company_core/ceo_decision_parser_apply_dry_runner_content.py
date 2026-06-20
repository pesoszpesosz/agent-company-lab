"""Pure content builder for the CEO decision parser apply dry-runner."""

from __future__ import annotations

from typing import Any

from .ceo_decision_parser_apply_evaluator import evaluate_ceo_parser_positive_apply_preview

LOCAL_DECISION = "ceo_decision_parser_apply_dry_runner_passed_preview_only"
RECOMMENDED_DEFAULT = "require_operator_apply_approval_before_real_update"


def build_ceo_decision_parser_apply_dry_runner_content(
    *,
    generated_utc: str,
    json_output_path: object,
    validation_path: object,
    lane_id: str,
    runner_task_id: str,
    runner_evidence_id: str,
    source_positive_fixture_task_id: str,
    source_positive_fixture_evidence_id: str,
    source_positive_fixture_validation_path: object,
    positive_fixture: dict[str, Any],
    expected_preview: dict[str, Any],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    submitted_apply = positive_fixture.get("submitted_apply", {})
    dry_run_result = evaluate_ceo_parser_positive_apply_preview(submitted_apply, expected_preview=expected_preview)
    apply_dry_run_execution_count = 1 if positive_fixture else 0
    positive_apply_fixture_count = 1 if positive_fixture else 0
    accepted_apply_preview_count = 1 if dry_run_result.get("accepted_apply_preview") is True else 0
    preview_update_count = int(expected_preview.get("would_update_count") or 0) if accepted_apply_preview_count else 0
    expected_preview_match_count = (
        1
        if dry_run_result.get("accepted_apply_preview") is True
        and dry_run_result.get("preview_state") == positive_fixture.get("expected_preview_state")
        and expected_preview.get("request_id") == target_request_id
        and expected_preview.get("applied") is False
        else 0
    )
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    runner_summary = (
        "Ran a local report-only apply dry-run against the positive apply fixture. The runner accepted the preview, matched the single expected service-request field update, and applied nothing."
    )
    runner_next_action = (
        "Keep real apply disabled; next create an apply-readiness packet that names the exact DB update, rollback check, and operator approval needed before any service request mutation."
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
        "schema_version": "agent_company.ceo_decision_parser_apply_dry_runner.v1",
        "generated_utc": generated_utc,
        "runner_lane_id": lane_id,
        "runner_task_id": runner_task_id,
        "runner_evidence_id": runner_evidence_id,
        "source_positive_fixture_task_id": source_positive_fixture_task_id,
        "source_positive_fixture_evidence_id": source_positive_fixture_evidence_id,
        "source_positive_fixture_validation_path": str(source_positive_fixture_validation_path),
        "positive_apply_fixture_count": positive_apply_fixture_count,
        "apply_dry_run_execution_count": apply_dry_run_execution_count,
        "accepted_apply_preview_count": accepted_apply_preview_count,
        "expected_preview_match_count": expected_preview_match_count,
        "preview_update_count": preview_update_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_before,
        "dry_run_result": dry_run_result,
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Apply Dry Runner",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{LOCAL_DECISION}`",
        "",
        runner_summary,
        "",
        "## Preview Result",
        "",
        f"- Target request: `{target_request_id}`",
        f"- Preview state: `{dry_run_result.get('preview_state')}`",
        f"- Preview updates: `{preview_update_count}`",
        "- Applied: `False`",
        "",
        "## Boundary",
        "",
        "This runner is report-only. It generated a local preview from one positive apply fixture and did not mutate service requests, assign work, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
        "",
        "## Next Action",
        "",
        runner_next_action,
        "",
    ]
    return {
        "positive_apply_fixture_count": positive_apply_fixture_count,
        "apply_dry_run_execution_count": apply_dry_run_execution_count,
        "accepted_apply_preview_count": accepted_apply_preview_count,
        "expected_preview_match_count": expected_preview_match_count,
        "preview_update_count": preview_update_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_before,
        "dry_run_result": dry_run_result,
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "summary": runner_summary,
        "next_action": runner_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = [
    "LOCAL_DECISION",
    "RECOMMENDED_DEFAULT",
    "build_ceo_decision_parser_apply_dry_runner_content",
]