from __future__ import annotations

from typing import Any


def build_ceo_apply_readiness_no_approval_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_packet_validation_path: str,
    lane_id: str,
    blocker_task_id: str,
    blocker_evidence_id: str,
    source_packet_task_id: str,
    source_packet_evidence_id: str,
    operator_approval_packet: dict[str, Any],
    target_service_request_count: int,
    target_status_before: Any,
    target_status_after: Any,
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_no_approval_blocked_no_mutation"
    recommended_default = "do_not_add_apply_command_until_explicit_operator_approval_exists"
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    explicit_operator_approval_present = False
    blocked_apply_attempt_count = 1

    target_request_id = operator_approval_packet.get("target_request_id")
    planned_updates = operator_approval_packet.get("planned_field_updates", {})
    if not isinstance(planned_updates, dict):
        planned_updates = {}
    approval_statements = operator_approval_packet.get("approval_statements") or []
    if not isinstance(approval_statements, list):
        approval_statements = []
    apply_command_enabled = operator_approval_packet.get("apply_command_enabled")
    approval_request_emitted = operator_approval_packet.get("approval_request_emitted")
    operator_approval_packet_count = 1 if operator_approval_packet else 0
    planned_field_update_count = len(planned_updates)
    approval_statement_count = len(approval_statements)
    blocked_reasons = [
        "operator approval packet has not emitted an approval request",
        "apply command is disabled in the packet",
        "explicit operator approval is absent",
        "target service request must remain unchanged until approval is recorded",
    ]
    simulated_apply_attempt = {
        "attempt_id": "no-approval-apply-attempt-20260616",
        "target_request_id": target_request_id,
        "requested_field_updates": planned_updates,
        "blocked": True,
        "blocked_reasons": blocked_reasons,
        "mutation_applied": False,
        "approval_request_emitted": False,
        "apply_command_enabled": False,
    }
    blocker_summary = (
        "Ran a local no-approval blocker against the apply-readiness approval packet. The simulated apply attempt was blocked because no explicit operator approval exists and the packet keeps apply disabled."
    )
    blocker_next_action = (
        "Do not add or run a mutating apply command until a separate explicit operator approval artifact exists for this exact target and field update."
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_no_approval_blocker.v1",
        "generated_utc": generated_utc,
        "blocker_lane_id": lane_id,
        "blocker_task_id": blocker_task_id,
        "blocker_evidence_id": blocker_evidence_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "source_packet_validation_path": source_packet_validation_path,
        "blocked_apply_attempt_count": blocked_apply_attempt_count,
        "blocked_reason_count": len(blocked_reasons),
        "operator_approval_packet_count": operator_approval_packet_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": planned_field_update_count,
        "approval_statement_count": approval_statement_count,
        "apply_command_enabled": apply_command_enabled,
        "approval_request_emitted": approval_request_emitted,
        "explicit_operator_approval_present": explicit_operator_approval_present,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "simulated_apply_attempt": simulated_apply_attempt,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": blocker_summary,
        "next_action": blocker_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness No Approval Blocker",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        blocker_summary,
        "",
        "## Blocked Reasons",
        "",
    ]
    for reason in blocked_reasons:
        md_lines.append(f"- {reason}")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This blocker is a local report-only simulation. It emits no approval request, applies no mutation, updates no service request, starts no worker, calls no API, opens no browser, and performs no account, wallet, payment, public, security-testing, external, or real-money action.",
            "",
            "## Next Action",
            "",
            blocker_next_action,
            "",
        ]
    )
    return {
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "explicit_operator_approval_present": explicit_operator_approval_present,
        "blocked_apply_attempt_count": blocked_apply_attempt_count,
        "operator_approval_packet_count": operator_approval_packet_count,
        "planned_field_update_count": planned_field_update_count,
        "approval_statement_count": approval_statement_count,
        "blocked_reasons": blocked_reasons,
        "blocked_reason_count": len(blocked_reasons),
        "simulated_apply_attempt": simulated_apply_attempt,
        "summary": blocker_summary,
        "next_action": blocker_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
        "apply_command_enabled": apply_command_enabled,
        "approval_request_emitted": approval_request_emitted,
    }


__all__ = ["build_ceo_apply_readiness_no_approval_content"]
