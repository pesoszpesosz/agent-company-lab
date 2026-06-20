from __future__ import annotations

from typing import Any


def build_ceo_gate_blocker_board_content(
    *,
    service_request_rows: list[dict[str, Any]],
    service_request_status_counts: dict[str, int],
    hold_entries: list[dict[str, Any]],
    register_lane_id: str | None,
) -> dict[str, Any]:
    needs_review_rows = [row for row in service_request_rows if row["status"] == "needs_review"]
    service_request_blockers = [
        {
            "blocker_id": row["request_id"],
            "blocker_type": "service_request_needs_review",
            "lane_id": row["lane_id"],
            "request_type": row["request_type"],
            "risk_gate": row["risk_gate"],
            "status": row["status"],
            "requested_action": row["requested_action"],
            "assigned_agent_id": row["assigned_agent_id"],
            "updated_at": row["updated_at"],
            "resume_trigger": "Explicit user approval with exact scope, or rejection/parking by CEO/CRO.",
        }
        for row in needs_review_rows
    ]
    hold_blockers = [
        {
            "blocker_id": entry["hold_id"],
            "blocker_type": "local_gated_hold",
            "lane_id": register_lane_id,
            "risk_gate": entry["gate_required"],
            "status": entry["status"],
            "requested_action": entry["resume_command_candidate"],
            "resume_trigger": entry["resume_trigger"],
            "source_question_id": entry["source_question_id"],
        }
        for entry in hold_entries
        if entry.get("status") == "active_hold"
    ]
    active_hold_count = len(hold_blockers)
    active_blocker_lane_ids = sorted(
        {row["lane_id"] for row in needs_review_rows if row.get("lane_id")}
        | ({str(register_lane_id)} if active_hold_count and register_lane_id else set())
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
    board_summary = (
        "Created a CEO gate/blocker board that consolidates service requests needing review with local gated holds, making all blocked work visible without approving or executing it."
    )
    board_next_action = (
        "CEO/operator should review the board and explicitly approve, reject, or keep holding individual blockers; no worker may resume a blocker from this board alone."
    )

    return {
        "local_decision": "ceo_gate_blocker_board_current",
        "recommended_default": "hold_all_gated_work_until_explicit_approval",
        "service_request_total_count": len(service_request_rows),
        "service_request_needs_review_count": len(needs_review_rows),
        "service_request_rejected_count": int(service_request_status_counts.get("rejected", 0)),
        "service_request_complete_count": int(service_request_status_counts.get("complete", 0)),
        "active_hold_count": active_hold_count,
        "active_blocker_count": len(needs_review_rows) + active_hold_count,
        "active_blocker_lane_count": len(active_blocker_lane_ids),
        "active_blocker_lane_ids": active_blocker_lane_ids,
        "runnable_without_approval_count": 0,
        "approval_request_count": 0,
        "service_request_blockers": service_request_blockers,
        "hold_blockers": hold_blockers,
        "blocker_items": service_request_blockers + hold_blockers,
        "summary": board_summary,
        "next_action": board_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_ceo_gate_blocker_board_content"]
