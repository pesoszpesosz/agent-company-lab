"""Shared evaluator for CEO apply-readiness signed decisions."""

from __future__ import annotations

from typing import Any


def evaluate_ceo_signed_decision(
    decision: dict[str, Any],
    decision_fields_template: dict[str, Any],
    *,
    include_preview_state: bool = False,
) -> dict[str, Any]:
    def rejected(rule_id: str) -> dict[str, Any]:
        return {
            "accepted_signed_decision": False,
            "rule_id": rule_id,
            "preview_state": None,
            "real_mutation_allowed": False,
        }

    if not decision.get("operator_signature"):
        return rejected("reject_missing_operator_signature")
    if decision.get("target_request_id") != decision_fields_template.get("target_request_id"):
        return rejected("reject_target_request_id_mismatch")
    if decision.get("approval_scope_text") != decision_fields_template.get("approval_scope_text"):
        return rejected("reject_approval_scope_text_mismatch")
    if decision.get("decision_note_text") != decision_fields_template.get("decision_note_text"):
        return rejected("reject_decision_note_text_mismatch")
    if decision.get("rollback_snapshot_updated_at") != decision_fields_template.get("rollback_snapshot_updated_at"):
        return rejected("reject_rollback_snapshot_mismatch")
    if not decision.get("approval_expires_utc"):
        return rejected("reject_missing_scope_expiration")
    if (
        decision.get("confirms_no_external_side_effects") is not True
        or decision.get("confirms_no_worker_start") is not True
        or decision.get("confirms_no_account_payment_public_security_real_money_action") is not True
    ):
        return rejected("reject_side_effect_confirmation_drift")
    if decision.get("rollback_plan_acknowledged") is not True:
        return rejected("reject_rollback_plan_not_acknowledged")
    return {
        "accepted_signed_decision": True,
        "rule_id": None,
        "preview_state": "signed_decision_valid_apply_still_disabled" if include_preview_state else None,
        "real_mutation_allowed": False,
    }


__all__ = ["evaluate_ceo_signed_decision"]
