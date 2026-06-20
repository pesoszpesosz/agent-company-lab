from __future__ import annotations

from typing import Any

"""Money-path coverage audit scoring and lane model helpers."""

from .money_path_lane_assignment import money_path_lane_assignment


def money_path_runtime_boundary() -> dict[str, Any]:
    return {
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


def money_path_no_action_lanes() -> list[dict[str, str]]:
    return [
        {
            "lane_id": "platform_engineering",
            "reason": "Platform should support money-lane evidence production rather than absorb the next work wave.",
        },
        {
            "lane_id": "submitted_bounty_payouts",
            "reason": "Read-only boundary is owned by another payout worker unless explicitly reassigned.",
        },
    ]


def build_money_path_coverage_model(
    lanes: list[dict[str, Any]],
    evidence_counts: dict[str, int],
    task_counts: dict[str, int],
    source_spec_counts: dict[str, int],
    parked_request_counts: dict[str, int],
    trace_counts: dict[str, int],
    thin_evidence_threshold: int = 1,
) -> dict[str, Any]:
    active_lanes = [lane for lane in lanes if lane["status"] == "active"]
    owned_active_lanes = [
        lane
        for lane in active_lanes
        if lane["owner_agent_id"] and lane["lane_id"] != "submitted_bounty_payouts"
    ]
    actionable_lanes = [
        lane
        for lane in active_lanes
        if lane["lane_id"] not in ("platform_engineering", "submitted_bounty_payouts")
    ]
    read_only_boundary_preserved = [
        lane["lane_id"]
        for lane in active_lanes
        if lane["lane_id"] == "submitted_bounty_payouts" and lane["owner_agent_id"] is None
    ] == ["submitted_bounty_payouts"]

    lane_rows: list[dict[str, Any]] = []
    for lane in active_lanes:
        lane_id = lane["lane_id"]
        assignment = money_path_lane_assignment(lane_id)
        evidence_count = evidence_counts.get(lane_id, 0)
        source_count = source_spec_counts.get(lane_id, 0)
        parked_count = parked_request_counts.get(lane_id, 0)
        trace_count = trace_counts.get(lane_id, 0)
        is_actionable_money_lane = lane in actionable_lanes
        thin_evidence = is_actionable_money_lane and evidence_count <= thin_evidence_threshold
        gated = parked_count > 0
        coverage_score = (
            min(evidence_count, 10) * 2
            + min(source_count, 3) * 3
            + min(trace_count, 5)
            - (3 if thin_evidence else 0)
            - (1 if gated else 0)
        )
        urgency_score = (
            (10 if thin_evidence else 0)
            + (4 if source_count == 0 and is_actionable_money_lane else 0)
            + (3 if gated else 0)
            + (2 if task_counts.get(lane_id, 0) <= 3 and is_actionable_money_lane else 0)
        )
        if lane_id in ("money_source_discovery", "ai_ml_competitions", "web3_airdrops_grants_hackathons"):
            urgency_score += 2
        lane_rows.append(
            {
                "lane_id": lane_id,
                "department": lane["department"],
                "owner_agent_id": lane["owner_agent_id"],
                "owner_thread_id": lane["owner_thread_id"],
                "source_spec_count": source_count,
                "evidence_count": evidence_count,
                "task_count": task_counts.get(lane_id, 0),
                "parked_service_request_count": parked_count,
                "trace_event_count": trace_count,
                "coverage_score": coverage_score,
                "urgency_score": urgency_score,
                "thin_evidence": thin_evidence,
                "blocked_by_service_gate": gated,
                "recommended_agent_type": assignment["agent"],
                "recommended_first_task": assignment["first_task"],
                "required_proof_artifact": assignment["proof"],
                "allowed_scope": "local_or_read_only_research_only",
            }
        )

    thin_evidence_rows = [row for row in lane_rows if row["thin_evidence"]]
    recommended_next_lanes = sorted(
        thin_evidence_rows,
        key=lambda row: (-row["urgency_score"], row["evidence_count"], row["lane_id"]),
    )
    recommended_lane_ids = [row["lane_id"] for row in recommended_next_lanes]
    return {
        "active_lanes": active_lanes,
        "owned_active_lanes": owned_active_lanes,
        "actionable_lanes": actionable_lanes,
        "read_only_boundary_preserved": read_only_boundary_preserved,
        "thin_evidence_threshold": thin_evidence_threshold,
        "lane_rows": lane_rows,
        "thin_evidence_rows": thin_evidence_rows,
        "recommended_next_lanes": recommended_next_lanes,
        "recommended_lane_ids": recommended_lane_ids,
        "no_action_lanes": money_path_no_action_lanes(),
        "runtime_boundary": money_path_runtime_boundary(),
    }


__all__ = [
    "build_money_path_coverage_model",
    "money_path_no_action_lanes",
    "money_path_runtime_boundary",
]