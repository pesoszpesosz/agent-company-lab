from __future__ import annotations
def money_path_lane_assignment(lane_id: str) -> dict[str, str]:
    assignments = {
        "ai_ml_competitions": {
            "agent": "competition_scout",
            "first_task": "Build a public prize-competition shortlist with prize route, deadline, account gate, dataset gate, baseline feasibility, and no-submission stop.",
            "proof": "Dated shortlist plus one baseline-feasibility memo.",
        },
        "content_and_social_growth": {
            "agent": "trend_scout",
            "first_task": "Use read-only X/Grok/Radar-style research to identify high-traction AI-builder posts and reply gaps; stop before any public action.",
            "proof": "Reply-target shortlist with exact URL, traction signal, suggested angle, and reputation risk note.",
        },
        "lead_generation_and_sales": {
            "agent": "offer_builder",
            "first_task": "Draft one non-spam offer packet for a narrow buyer segment with targeting rules, proof asset, and opt-out/reputation constraints.",
            "proof": "Offer packet and lead-filter rubric; no outreach sent.",
        },
        "local_trading_strategy_research": {
            "agent": "strategy_miner",
            "first_task": "Inventory local backtest/trading workspaces and define one paper-only replay standard with fees, slippage, and kill criteria.",
            "proof": "Local artifact inventory plus paper-only evidence checklist.",
        },
        "money_source_discovery": {
            "agent": "source_mapper",
            "first_task": "Create a public venue registry scan for monetizable sources, payout route, account gate, first proof artifact, and freshness cadence.",
            "proof": "Ranked venue registry with gate and first-action column.",
        },
        "web3_airdrops_grants_hackathons": {
            "agent": "program_scout",
            "first_task": "Scout grants, hackathons, and airdrop/task programs for deadlines, wallet/account requirements, eligibility, and local prototype proof options.",
            "proof": "Terms/deadline shortlist; no wallet, registration, deployment, or transaction.",
        },
        "digital_products_templates_plugins": {
            "agent": "market_gap_scout",
            "first_task": "Refresh marketplace demand evidence and choose one locally buildable product packet before listing or payment work.",
            "proof": "Demand memo, asset draft, and gated listing/payment decision packet.",
        },
        "paid_code_bounties": {
            "agent": "repo_triager",
            "first_task": "Scout explicit payout issues with duplicate checks, ownership checks, and testability under four hours before any PR/comment.",
            "proof": "Ranked issue worksheet with duplicate and payout-route evidence.",
        },
        "security_bounty_private_reports": {
            "agent": "program_rules_reader",
            "first_task": "Rank allowed public-code static review targets by scope clarity, private report route, and reproducible local proof path.",
            "proof": "Scope-safe target sheet and private-report route memo.",
        },
        "prediction_market_research": {
            "agent": "market_scout",
            "first_task": "Create one paper-only market replay with source-of-truth, fees, liquidity, settlement, and no-trade gate.",
            "proof": "Paper replay record; no account, deposit, or trade.",
        },
        "platform_engineering": {
            "agent": "control_plane_builder",
            "first_task": "Keep the ledger, validation chain, dashboard, and service gates healthy while money lanes produce evidence.",
            "proof": "Passing chain integrity and refreshed control-plane status.",
        },
        "submitted_bounty_payouts": {
            "agent": "payout_monitor",
            "first_task": "Read-only visibility only from this thread; do not duplicate the external payout worker.",
            "proof": "Boundary note only.",
        },
    }
    return assignments.get(
        lane_id,
        {
            "agent": "seeker_agent",
            "first_task": "Create a narrow local proof task with evidence, duplicate key, and explicit stop gates.",
            "proof": "Local proof packet.",
        },
    )
