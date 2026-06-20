from __future__ import annotations

from typing import Any


def build_ceo_apply_readiness_operator_approval_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_runner_validation_path: str,
    lane_id: str,
    packet_task_id: str,
    packet_evidence_id: str,
    source_runner_task_id: str,
    source_runner_evidence_id: str,
    readiness_packet: dict[str, Any],
    target_service_request_count: int,
    target_status_before: Any,
    target_status_after: Any,
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_operator_approval_packet_ready_no_request"
    recommended_default = "wait_for_explicit_operator_apply_approval"
    operator_approval_packet_count = 1
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0

    target_request_id = readiness_packet.get("target_request_id")
    planned_updates = readiness_packet.get("planned_field_updates", {})
    if not isinstance(planned_updates, dict):
        planned_updates = {}
    rollback_checks = readiness_packet.get("rollback_checks") or []
    if not isinstance(rollback_checks, list):
        rollback_checks = []
    operator_approvals = readiness_packet.get("required_operator_approvals") or []
    if not isinstance(operator_approvals, list):
        operator_approvals = []

    approval_statements = [
        f"Approve exact target request id: {target_request_id}",
        f"Approve approval_scope field update: {planned_updates.get('approval_scope')}",
        f"Approve decision_note field update: {planned_updates.get('decision_note')}",
        "Confirm no browser/api/worker/account/payment/public/security/real-money action is authorized by this packet.",
        "Confirm rollback snapshot must be captured immediately before any future apply command.",
    ]
    operator_approval_packet = {
        "packet_id": "ceo-decision-parser-apply-readiness-operator-approval-packet-20260616",
        "target_request_id": target_request_id,
        "planned_field_updates": planned_updates,
        "rollback_snapshot": readiness_packet.get("rollback_snapshot", {}),
        "rollback_checks": rollback_checks,
        "required_operator_approvals": operator_approvals,
        "approval_statements": approval_statements,
        "approval_request_emitted": False,
        "apply_command_enabled": False,
    }
    packet_summary = (
        "Prepared a local operator-approval packet for the apply-readiness field update. The packet records the exact target, field updates, rollback checks, and approval statements without emitting an approval request or enabling apply."
    )
    packet_next_action = (
        "Wait for explicit operator approval of this exact packet before adding or running any command that mutates the target service request."
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_operator_approval_packet.v1",
        "generated_utc": generated_utc,
        "packet_lane_id": lane_id,
        "packet_task_id": packet_task_id,
        "packet_evidence_id": packet_evidence_id,
        "source_runner_task_id": source_runner_task_id,
        "source_runner_evidence_id": source_runner_evidence_id,
        "source_runner_validation_path": source_runner_validation_path,
        "operator_approval_packet_count": operator_approval_packet_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": len(planned_updates),
        "rollback_check_count": len(rollback_checks),
        "required_operator_approval_count": len(operator_approvals),
        "approval_statement_count": len(approval_statements),
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "operator_approval_packet": operator_approval_packet,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": packet_summary,
        "next_action": packet_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Operator Approval Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        packet_summary,
        "",
        "## Approval Statements",
        "",
    ]
    for statement in approval_statements:
        md_lines.append(f"- {statement}")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is a local artifact only. It emits no approval request, applies no mutation, updates no service request, starts no worker, calls no API, opens no browser, and performs no account, wallet, payment, public, security-testing, external, or real-money action.",
            "",
            "## Next Action",
            "",
            packet_next_action,
            "",
        ]
    )
    return {
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "operator_approval_packet_count": operator_approval_packet_count,
        "target_service_request_count": target_service_request_count,
        "planned_field_update_count": len(planned_updates),
        "rollback_check_count": len(rollback_checks),
        "required_operator_approval_count": len(operator_approvals),
        "approval_statement_count": len(approval_statements),
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "approval_statements": approval_statements,
        "operator_approval_packet": operator_approval_packet,
        "summary": packet_summary,
        "next_action": packet_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = ["build_ceo_apply_readiness_operator_approval_content"]
