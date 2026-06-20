from __future__ import annotations

from typing import Any


def build_ceo_apply_readiness_base_content(
    *,
    target_request_id: str,
    target_request: dict[str, Any] | None,
    planned_updates: dict[str, Any],
) -> dict[str, Any]:
    target_status_before = target_request.get("status") if target_request else None
    rollback_checks = [
        "snapshot target service request before apply",
        "verify status count delta is zero except intended field update",
        "restore approval_scope and decision_note to previous values on failure",
        "write post-apply validation artifact before any worker start",
    ]
    required_operator_approvals = [
        "explicitly approve this exact target request id",
        "explicitly approve approval_scope field update text",
        "explicitly approve decision_note field update text",
        "confirm no browser/api/worker/account/payment/public/security/real-money action",
        "confirm rollback snapshot is captured before apply",
    ]
    readiness_packet = {
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_updated_at_before": target_request.get("updated_at") if target_request else None,
        "planned_field_updates": planned_updates,
        "planned_update_sql_shape": {
            "table": "service_requests",
            "where": "request_id = :target_request_id AND status = 'needs_review'",
            "set_fields": sorted(planned_updates.keys()),
            "max_rows": 1,
        },
        "rollback_snapshot": {
            "approval_scope": target_request.get("approval_scope") if target_request else None,
            "decision_note": target_request.get("decision_note") if target_request else None,
            "status": target_status_before,
            "updated_at": target_request.get("updated_at") if target_request else None,
        },
        "rollback_checks": rollback_checks,
        "required_operator_approvals": required_operator_approvals,
        "apply_boundary": {
            "apply_allowed_now": False,
            "requires_explicit_operator_apply_approval": True,
            "service_requests_updated": 0,
            "worker_starts": 0,
            "external_side_effects": False,
        },
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
    readiness_summary = (
        "Created a local apply-readiness packet for the single service-request preview, naming the exact DB update shape, rollback snapshot checks, and explicit operator approval requirements before any real mutation is allowed."
    )
    readiness_next_action = (
        "Hold real apply disabled; next create apply-readiness negative fixtures so missing approval, stale snapshots, and target drift are rejected before any update command exists."
    )

    return {
        "local_decision": "ceo_decision_parser_apply_readiness_ready_no_apply",
        "recommended_default": "hold_for_explicit_operator_apply_approval",
        "readiness_packet_count": 1,
        "mutation_applied_count": 0,
        "queue_mutation_count": 0,
        "approval_request_count": 0,
        "planned_field_update_count": len(planned_updates),
        "rollback_checks": rollback_checks,
        "required_operator_approvals": required_operator_approvals,
        "rollback_check_count": len(rollback_checks),
        "required_operator_approval_count": len(required_operator_approvals),
        "readiness_packet": readiness_packet,
        "summary": readiness_summary,
        "next_action": readiness_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_ceo_apply_readiness_base_content"]
