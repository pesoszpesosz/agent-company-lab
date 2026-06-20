"""Shared evaluator for signed CEO apply-command fixtures."""

from __future__ import annotations

from typing import Any


def reject_signed_apply_command(rule_id: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "preview_state": None,
        "rule_id": rule_id,
        "real_mutation_allowed": False,
    }


def evaluate_signed_apply_command_negative_fixture(
    fixture: dict[str, Any],
    *,
    target_request_id: str | None,
) -> dict[str, Any]:
    overrides = fixture.get("input_overrides") or {}
    if overrides.get("operator_signature") is None and "operator_signature" in overrides:
        return reject_signed_apply_command("reject_missing_operator_signature")
    if overrides.get("approval_expires_utc") == "2026-01-01T00:00:00Z":
        return reject_signed_apply_command("reject_expired_approval")
    if overrides.get("rollback_snapshot_updated_at") == "2000-01-01T00:00:00Z":
        return reject_signed_apply_command("reject_stale_target_snapshot")
    if overrides.get("target_request_id") and overrides.get("target_request_id") != target_request_id:
        return reject_signed_apply_command("reject_wrong_target_request_id")
    if overrides.get("target_update_fields") != ["approval_scope", "decision_note"] and "target_update_fields" in overrides:
        return reject_signed_apply_command("reject_unapproved_field_set")
    if overrides.get("explicit_apply_execution_flag") is False:
        return reject_signed_apply_command("reject_missing_explicit_execution_flag")
    return {
        "accepted": True,
        "preview_state": None,
        "rule_id": None,
        "real_mutation_allowed": False,
    }


def evaluate_signed_apply_command_positive_fixture(
    fixture: dict[str, Any],
    *,
    target_request_id: str | None,
) -> dict[str, Any]:
    confirmations = fixture.get("confirmations") or {}
    required_fields = fixture.get("required_fields_present") or []
    if len(required_fields) != 8:
        return reject_signed_apply_command("reject_required_field_count_drift")
    if len(confirmations) != 6 or not all(value is True for value in confirmations.values()):
        return reject_signed_apply_command("reject_confirmation_bundle_incomplete")
    if fixture.get("operator_signature") != "LOCAL_FIXTURE_SIGNATURE_NOT_REAL_APPROVAL":
        return reject_signed_apply_command("reject_signature_not_fixture_scoped")
    if fixture.get("target_request_id") != target_request_id:
        return reject_signed_apply_command("reject_target_request_id_mismatch")
    if fixture.get("rollback_snapshot_updated_at") != "2026-06-14T14:37:52Z":
        return reject_signed_apply_command("reject_rollback_snapshot_mismatch")
    if fixture.get("target_update_fields") != ["approval_scope", "decision_note"]:
        return reject_signed_apply_command("reject_target_update_field_drift")
    if fixture.get("explicit_apply_execution_flag") is not True:
        return reject_signed_apply_command("reject_missing_explicit_execution_flag")
    if fixture.get("expected_real_mutation") is not False:
        return reject_signed_apply_command("reject_fixture_attempts_real_mutation")
    return {
        "accepted": True,
        "preview_state": "positive_apply_command_fixture_valid_apply_still_disabled",
        "rule_id": None,
        "real_mutation_allowed": False,
    }


__all__ = [
    "evaluate_signed_apply_command_negative_fixture",
    "evaluate_signed_apply_command_positive_fixture",
    "reject_signed_apply_command",
]
