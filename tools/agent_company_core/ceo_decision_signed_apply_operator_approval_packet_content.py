from __future__ import annotations

from typing import Any


def build_signed_apply_operator_approval_packet_content(
    *,
    decision_fields_template: dict[str, Any],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    approval_granted_by_packet = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    required_approval_fields = [
        "target_request_id",
        "approval_scope_text",
        "decision_note_text",
        "operator_signature",
        "approval_expires_utc",
        "rollback_snapshot_updated_at",
        "apply_command_name",
        "confirmation_statement",
    ]
    required_confirmations = [
        "confirm_target_request_matches_snapshot",
        "confirm_no_browser_account_wallet_payment_public_security_real_money_action",
        "confirm_apply_updates_only_approval_scope_and_decision_note",
        "confirm_no_worker_start_or_assignment",
        "confirm_rollback_plan_accepted",
        "confirm_operator_understands_packet_does_not_apply_itself",
    ]
    operator_apply_approval_packet = {
        "packet_id": "signed-decision-operator-apply-approval-packet-20260616",
        "target_request_id": target_request_id,
        "target_status": target_status_before,
        "approval_scope_text": decision_fields_template.get("approval_scope_text"),
        "decision_note_text": decision_fields_template.get("decision_note_text"),
        "rollback_snapshot_updated_at": decision_fields_template.get("rollback_snapshot_updated_at"),
        "apply_command_name": "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command",
        "required_approval_fields": required_approval_fields,
        "required_confirmations": required_confirmations,
        "operator_instruction": (
            "This packet is a draft only. A separate explicit operator apply approval must provide every required field and confirmation before any mutation command can be enabled."
        ),
        "approval_granted_by_packet": approval_granted_by_packet,
        "apply_command_enabled": apply_command_enabled,
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
    packet_summary = (
        "Drafted the local signed-decision operator apply approval packet. The packet names the exact fields and confirmations required, but it does not grant approval or enable apply."
    )
    packet_next_action = (
        "Use this packet as the human gate template; do not mutate the target service request until the operator explicitly supplies the required approval."
    )

    return {
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet_ready_no_mutation",
        "recommended_default": "operator_must_explicitly_approve_before_apply_command_is_enabled",
        "operator_apply_approval_packet_count": 1,
        "approval_granted_by_packet": approval_granted_by_packet,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "required_approval_fields": required_approval_fields,
        "required_confirmations": required_confirmations,
        "required_approval_field_count": len(required_approval_fields),
        "required_confirmation_count": len(required_confirmations),
        "operator_apply_approval_packet": operator_apply_approval_packet,
        "summary": packet_summary,
        "next_action": packet_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_signed_apply_operator_approval_packet_content"]
