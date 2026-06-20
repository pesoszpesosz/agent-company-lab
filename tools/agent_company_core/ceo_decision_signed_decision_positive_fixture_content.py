from __future__ import annotations

from typing import Any


def build_signed_decision_positive_fixture_content(
    *,
    decision_fields_template: dict[str, Any],
    approval_statements: list[Any],
    target_status_before: str | None,
    generated_utc: str,
) -> dict[str, Any]:
    positive_signed_decision_fixture_count = 1
    expected_acceptance_count = 1
    signed_decision_preview_only = True
    apply_command_enabled = False
    approval_granted_by_fixture = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before
    signed_decision_fields = {
        **decision_fields_template,
        "operator_signature": "operator-approved-local-preview-fixture",
        "signed_decision_utc": generated_utc,
        "approval_expires_utc": "2026-06-17T00:00:00Z",
        "confirms_no_external_side_effects": True,
        "confirms_no_worker_start": True,
        "confirms_no_account_payment_public_security_real_money_action": True,
        "rollback_plan_acknowledged": True,
    }
    positive_signed_decision_fixture = {
        "fixture_id": "valid-signed-decision-preview-only",
        "expected_accepted": True,
        "expected_preview_state": "signed_decision_valid_apply_still_disabled",
        "expected_real_mutation": False,
        "submitted_signed_decision": signed_decision_fields,
    }
    fixture_summary = (
        "Created one local positive signed-decision fixture that should pass the signed-decision guard while still keeping apply disabled and granting no real approval."
    )
    fixture_next_action = (
        "Run a report-only positive signed-decision runner; do not add or run any mutating apply command without a separate explicit operator approval."
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
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_positive_fixture_ready_preview_only",
        "recommended_default": "positive_signed_decision_fixture_requires_separate_positive_runner",
        "positive_signed_decision_fixture_count": positive_signed_decision_fixture_count,
        "expected_acceptance_count": expected_acceptance_count,
        "decision_field_count": len(decision_fields_template),
        "approval_statement_count": len(approval_statements),
        "signed_decision_preview_only": signed_decision_preview_only,
        "apply_command_enabled": apply_command_enabled,
        "approval_granted_by_fixture": approval_granted_by_fixture,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_after,
        "positive_signed_decision_fixture": positive_signed_decision_fixture,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_signed_decision_positive_fixture_content"]
