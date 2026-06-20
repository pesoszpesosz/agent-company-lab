from __future__ import annotations

from typing import Any, Callable


def build_ceo_blocker_triage_content(blocker_items: list[dict[str, Any]]) -> dict[str, Any]:
    def ids_for(predicate: Callable[[dict[str, Any]], bool]) -> list[str]:
        return [item["blocker_id"] for item in blocker_items if predicate(item)]

    triage_batches = [
        {
            "batch_id": "batch-digital-products-marketplace-validation",
            "priority": 1,
            "leverage": "high",
            "lane_focus": "digital_products_templates_plugins",
            "blocker_ids": ids_for(
                lambda item: item.get("lane_id") == "digital_products_templates_plugins"
                and item.get("risk_gate")
                in {
                    "catalog_required_approval_no_external_action",
                    "browser_read_only_session",
                    "legal_kyc_tax_payment",
                    "legal_kyc_tax_payment_requires_user_decision_no_commitment",
                    "public_action_approval",
                    "account_payment_approval",
                }
            ),
            "decision_needed": "Choose whether to approve only read-only validation/legal review, keep all holds, or reject the marketplace route.",
            "why_it_matters": "This lane has the most complete local product packet and the largest cluster of related gates.",
        },
        {
            "batch_id": "batch-security-bounty-route-readiness",
            "priority": 2,
            "leverage": "high",
            "lane_focus": "security_bounty_private_reports",
            "blocker_ids": ids_for(lambda item: item.get("lane_id") == "security_bounty_private_reports"),
            "decision_needed": "Decide whether read-only rules/scope review is worth approving before any report-route work.",
            "why_it_matters": "Security routes can become payout-relevant, but submission and testing gates must stay strict.",
        },
        {
            "batch_id": "batch-paid-code-and-ai-ml-readonly",
            "priority": 3,
            "leverage": "high",
            "lane_focus": "paid_code_bounties_ai_ml_competitions",
            "blocker_ids": ids_for(lambda item: item.get("lane_id") in {"paid_code_bounties", "ai_ml_competitions"}),
            "decision_needed": "Approve or hold read-only public page refreshes for paid-code and competition opportunities.",
            "why_it_matters": "These are low-commitment discovery gates that can refresh payout/rules evidence without public action.",
        },
        {
            "batch_id": "batch-platform-research-and-model-api",
            "priority": 4,
            "leverage": "medium",
            "lane_focus": "platform_engineering",
            "blocker_ids": ids_for(lambda item: item.get("lane_id") == "platform_engineering"),
            "decision_needed": "Separate model-cost/API approval from browser/Grok research approval; keep both held unless exact scope is approved.",
            "why_it_matters": "Platform research can improve infrastructure, but model/API and signed-in browser gates need exact cost and action boundaries.",
        },
        {
            "batch_id": "batch-source-discovery-and-social-browser",
            "priority": 5,
            "leverage": "medium",
            "lane_focus": "money_source_discovery_content_and_social_growth",
            "blocker_ids": ids_for(lambda item: item.get("lane_id") in {"money_source_discovery", "content_and_social_growth"}),
            "decision_needed": "Decide whether read-only browser discovery is useful now or should stay parked behind higher-value batches.",
            "why_it_matters": "These can add leads, but current product/security/paid-code gates look closer to actionable proof.",
        },
    ]
    covered_blocker_ids = sorted({blocker_id for batch in triage_batches for blocker_id in batch["blocker_ids"]})
    missing_blocker_ids = sorted({item["blocker_id"] for item in blocker_items} - set(covered_blocker_ids))
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
    triage_summary = (
        "Ranked the CEO blocker board into five local decision batches, highlighting three high-leverage batches while leaving every gate held."
    )
    triage_next_action = (
        "CEO/operator should review the ranked batches and explicitly approve, reject, or continue holding individual scopes; this triage does not authorize any work."
    )

    return {
        "local_decision": "ceo_blocker_triage_ready_for_human_review",
        "recommended_default": "hold_all_gated_work_until_explicit_approval",
        "approval_request_count": 0,
        "runnable_without_approval_count": 0,
        "triage_batches": triage_batches,
        "triage_batch_count": len(triage_batches),
        "high_leverage_batch_count": sum(1 for batch in triage_batches if batch["leverage"] == "high"),
        "covered_blocker_ids": covered_blocker_ids,
        "covered_blocker_count": len(covered_blocker_ids),
        "missing_blocker_ids": missing_blocker_ids,
        "summary": triage_summary,
        "next_action": triage_next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_ceo_blocker_triage_content"]
