from __future__ import annotations

from typing import Any


def build_signed_apply_preflight_content(
    *,
    runner_validation: dict[str, Any],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    apply_preflight_check_count = 1
    apply_blocked_count = 1
    explicit_operator_apply_approval_present = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    accepted_signed_decision_count = runner_validation.get("accepted_signed_decision_count")
    apply_command_enabled = runner_validation.get("apply_command_enabled")
    approval_granted_by_runner = runner_validation.get("approval_granted_by_runner")
    real_mutation_allowed_count = runner_validation.get("real_mutation_allowed_count")
    target_status_after = target_status_before
    blocked_reasons = [
        {
            "reason_id": "positive_runner_preview_only",
            "detail": "The valid signed decision was accepted only into preview state.",
        },
        {
            "reason_id": "apply_command_disabled",
            "detail": "The runner validation keeps apply_command_enabled false.",
        },
        {
            "reason_id": "runner_did_not_grant_approval",
            "detail": "The runner validation keeps approval_granted_by_runner false.",
        },
        {
            "reason_id": "missing_explicit_operator_apply_approval",
            "detail": "No separate operator apply approval artifact is present for mutation.",
        },
        {
            "reason_id": "real_mutation_allowance_zero",
            "detail": "The runner validation reports zero real mutation allowances.",
        },
    ]
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
    preflight_summary = (
        "Checked the accepted signed-decision positive runner as an apply preflight. Apply remains blocked because the runner is preview-only and no separate explicit operator apply approval exists."
    )
    preflight_next_action = (
        "Wait for explicit operator apply approval before enabling any command that mutates the target service request."
    )

    return {
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_apply_preflight_blocked_no_mutation",
        "recommended_default": "wait_for_explicit_operator_apply_approval_before_mutating_service_request",
        "apply_preflight_check_count": apply_preflight_check_count,
        "apply_blocked_count": apply_blocked_count,
        "accepted_signed_decision_count": accepted_signed_decision_count,
        "apply_command_enabled": apply_command_enabled,
        "approval_granted_by_runner": approval_granted_by_runner,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "real_mutation_allowed_count": real_mutation_allowed_count,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "blocked_reasons": blocked_reasons,
        "blocked_reason_count": len(blocked_reasons),
        "summary": preflight_summary,
        "next_action": preflight_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_signed_apply_preflight_content"]
