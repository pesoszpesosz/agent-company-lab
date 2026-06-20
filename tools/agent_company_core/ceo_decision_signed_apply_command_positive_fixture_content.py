from __future__ import annotations

from typing import Any


def build_signed_apply_command_positive_fixture_content(
    *,
    operator_packet: dict[str, Any],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    approval_granted_by_fixture = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    apply_execution_allowed = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before
    target_update_fields = ["approval_scope", "decision_note"]
    required_fields = operator_packet.get("required_approval_fields") or []
    required_confirmations = operator_packet.get("required_confirmations") or []
    signed_operator_apply_fixture = {
        "fixture_id": "signed-operator-apply-command-positive-fixture-20260616",
        "target_request_id": target_request_id,
        "approval_scope_text": operator_packet.get("approval_scope_text"),
        "decision_note_text": operator_packet.get("decision_note_text"),
        "operator_signature": "LOCAL_FIXTURE_SIGNATURE_NOT_REAL_APPROVAL",
        "approval_expires_utc": "2026-12-31T23:59:59Z",
        "rollback_snapshot_updated_at": operator_packet.get("rollback_snapshot_updated_at"),
        "apply_command_name": operator_packet.get("apply_command_name"),
        "confirmation_statement": "LOCAL FIXTURE ONLY - does not authorize mutation.",
        "required_fields_present": required_fields,
        "confirmations": {key: True for key in required_confirmations},
        "target_update_fields": target_update_fields,
        "explicit_apply_execution_flag": True,
        "expected_accepted": True,
        "expected_preview_state": "positive_apply_command_fixture_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }
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
    fixture_summary = (
        "Created one local positive signed operator apply command fixture. It has the expected approval-shape fields and confirmations, but it is fixture data only and does not grant approval or enable apply."
    )
    fixture_next_action = (
        "Run a report-only positive fixture runner that accepts this local fixture into preview state while keeping real mutation disabled."
    )

    return {
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture_ready_preview_only",
        "recommended_default": "positive_apply_command_fixture_requires_report_only_runner_before_any_apply_implementation",
        "positive_apply_command_fixture_count": 1,
        "required_field_count": len(required_fields),
        "confirmation_count": len(required_confirmations),
        "target_update_field_count": len(target_update_fields),
        "signed_operator_apply_fixture": signed_operator_apply_fixture,
        "approval_granted_by_fixture": approval_granted_by_fixture,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "target_update_fields": target_update_fields,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_signed_apply_command_positive_fixture_content"]
