from __future__ import annotations

from typing import Any


def build_signed_decision_negative_fixtures_content(
    *,
    decision_fields_template: dict[str, Any],
    approval_statements: list[Any],
    target_status_before: str | None,
    generated_utc: str,
) -> dict[str, Any]:
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before

    def signed_decision_fixture(fixture_id: str, expected_rule_id: str, **overrides: object) -> dict[str, object]:
        fields = {
            **decision_fields_template,
            "operator_signature": "operator-approved-local-fixture",
            "signed_decision_utc": generated_utc,
            "approval_expires_utc": "2026-06-17T00:00:00Z",
            "confirms_no_external_side_effects": True,
            "confirms_no_worker_start": True,
            "confirms_no_account_payment_public_security_real_money_action": True,
            "rollback_plan_acknowledged": True,
        }
        fields.update(overrides)
        return {
            "fixture_id": fixture_id,
            "expected_accepted": False,
            "expected_rule_id": expected_rule_id,
            "submitted_signed_decision": fields,
        }

    negative_signed_decision_fixtures = [
        signed_decision_fixture("missing-operator-signature", "reject_missing_operator_signature", operator_signature=None),
        signed_decision_fixture("wrong-target-request-id", "reject_target_request_id_mismatch", target_request_id="req-wrong-target"),
        signed_decision_fixture("edited-approval-scope-text", "reject_approval_scope_text_mismatch", approval_scope_text="mutated scope text"),
        signed_decision_fixture("stale-rollback-snapshot", "reject_rollback_snapshot_mismatch", rollback_snapshot_updated_at="2026-01-01T00:00:00Z"),
        signed_decision_fixture("missing-scope-expiration", "reject_missing_scope_expiration", approval_expires_utc=None),
        signed_decision_fixture("side-effect-confirmation-drift", "reject_side_effect_confirmation_drift", confirms_no_external_side_effects=False),
    ]
    fixture_summary = (
        "Created six local negative signed-decision fixtures for the apply-readiness approval gate. Each fixture changes one required decision field and should be rejected by the future signed-decision guard."
    )
    fixture_next_action = (
        "Run a report-only signed-decision guard against these fixtures before adding any mutating apply command."
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
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures_ready",
        "recommended_default": "run_signed_decision_guard_before_any_apply_command",
        "negative_signed_decision_fixtures": negative_signed_decision_fixtures,
        "negative_signed_decision_fixture_count": len(negative_signed_decision_fixtures),
        "expected_rejection_count": sum(1 for fixture in negative_signed_decision_fixtures if fixture.get("expected_accepted") is False),
        "decision_field_count": len(decision_fields_template),
        "approval_statement_count": len(approval_statements),
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_after": target_status_after,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_signed_decision_negative_fixtures_content"]
