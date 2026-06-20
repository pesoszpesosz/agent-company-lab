"""Pure content builders for CEO decision packet drafts."""

from __future__ import annotations

from typing import Any

LOCAL_DECISION = "ceo_decision_packet_drafts_ready_not_submitted"
RECOMMENDED_DEFAULT = "hold_all_gated_work_until_explicit_approval"


def build_ceo_decision_packet_drafts_content(
    *,
    generated_utc: str,
    json_output_path: object,
    validation_path: object,
    source_triage_validation_path: object,
    lane_id: str,
    draft_task_id: str,
    draft_evidence_id: str,
    source_triage_task_id: str,
    source_triage_evidence_id: str,
    triage_batches: list[dict[str, Any]],
    source_active_blocker_count: int,
    source_triage_batch_count: int,
    source_high_leverage_batch_count: int,
) -> dict[str, Any]:
    approval_request_count = 0
    runnable_without_approval_count = 0
    high_leverage_batches = [batch for batch in triage_batches if batch.get("leverage") == "high"]
    packet_drafts: list[dict[str, object]] = []
    for batch in high_leverage_batches:
        packet_drafts.append(
            {
                "packet_id": f"decision-packet-{batch['batch_id']}",
                "source_batch_id": batch["batch_id"],
                "priority": batch["priority"],
                "lane_focus": batch["lane_focus"],
                "covered_blocker_ids": batch["blocker_ids"],
                "default_recommendation": "hold",
                "decision_options": [
                    {
                        "option_id": "approve_bounded_readonly_scope",
                        "status": "draft_only_not_requested",
                        "meaning": "Approve only the bounded read-only or review scope named in this packet, with no public, account, payment, wallet, or submission side effects.",
                    },
                    {
                        "option_id": "keep_held",
                        "status": "draft_only_not_requested",
                        "meaning": "Keep every blocker in this batch held and require a fresh review later.",
                    },
                    {
                        "option_id": "reject_or_park_batch",
                        "status": "draft_only_not_requested",
                        "meaning": "Reject or park the batch so lane managers stop waiting on it and continue other local proof work.",
                    },
                ],
                "human_prompt": batch["decision_needed"],
                "why_it_matters": batch["why_it_matters"],
                "non_authority_notice": "This packet is a draft. Selecting text from it in a future message is not approval unless the user explicitly grants the exact scope.",
            }
        )
    packet_draft_count = len(packet_drafts)
    decision_option_count = sum(len(packet["decision_options"]) for packet in packet_drafts)
    draft_summary = (
        "Drafted local CEO decision packets for the three high-leverage blocker batches. The packets present approve/hold/reject options but request or execute nothing."
    )
    draft_next_action = (
        "CEO/operator can review these packet drafts and later issue an explicit scoped decision; until then all blockers remain held."
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
        "schema_version": "agent_company.ceo_decision_packet_drafts.v1",
        "generated_utc": generated_utc,
        "draft_lane_id": lane_id,
        "draft_task_id": draft_task_id,
        "draft_evidence_id": draft_evidence_id,
        "source_triage_task_id": source_triage_task_id,
        "source_triage_evidence_id": source_triage_evidence_id,
        "source_triage_validation_path": str(source_triage_validation_path),
        "source_active_blocker_count": source_active_blocker_count,
        "source_triage_batch_count": source_triage_batch_count,
        "source_high_leverage_batch_count": source_high_leverage_batch_count,
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "packet_draft_count": packet_draft_count,
        "decision_option_count": decision_option_count,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "packet_drafts": packet_drafts,
        "summary": draft_summary,
        "next_action": draft_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Packet Drafts",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{LOCAL_DECISION}`",
        "",
        draft_summary,
        "",
        "## Packet Drafts",
        "",
    ]
    for packet in packet_drafts:
        md_lines.extend(
            [
                f"### {packet['packet_id']}",
                "",
                f"Source batch: `{packet['source_batch_id']}`",
                f"Priority: `{packet['priority']}`",
                f"Lane focus: `{packet['lane_focus']}`",
                f"Default recommendation: `{packet['default_recommendation']}`",
                "",
                f"Human prompt: {packet['human_prompt']}",
                "",
                f"Why it matters: {packet['why_it_matters']}",
                "",
                "Covered blockers:",
            ]
        )
        for blocker_id in packet["covered_blocker_ids"]:
            md_lines.append(f"- `{blocker_id}`")
        md_lines.extend(["", "Decision options:"])
        for option in packet["decision_options"]:
            md_lines.append(f"- `{option['option_id']}`: {option['meaning']}")
        md_lines.extend(["", packet["non_authority_notice"], ""])
    md_lines.extend(
        [
            "## Boundary",
            "",
            "These are local decision-packet drafts only. They do not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.",
            "",
            "## Next Action",
            "",
            draft_next_action,
            "",
        ]
    )
    return {
        "local_decision": LOCAL_DECISION,
        "recommended_default": RECOMMENDED_DEFAULT,
        "approval_request_count": approval_request_count,
        "runnable_without_approval_count": runnable_without_approval_count,
        "packet_drafts": packet_drafts,
        "packet_draft_count": packet_draft_count,
        "decision_option_count": decision_option_count,
        "summary": draft_summary,
        "next_action": draft_next_action,
        "runtime_boundary": runtime_boundary,
        "payload": payload,
        "markdown": "\n".join(md_lines) + "\n",
    }


__all__ = [
    "LOCAL_DECISION",
    "RECOMMENDED_DEFAULT",
    "build_ceo_decision_packet_drafts_content",
]