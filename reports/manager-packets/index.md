# Agent Company Manager Packets

Generated UTC: 2026-06-21T14:12:23Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`

## Boundary

- A manager packet is an instruction and evidence view, not permission to perform gated side effects.
- Each future manager should register an agent, claim an unowned lane, acquire one task, write artifacts, and record outcomes.
- `submitted_bounty_payouts` is read-only in this thread and remains assigned to the parallel payout worker.

## Index

| Lane | Department | Owner | Evidence | Open Tasks | Open Service Requests | Packet | Recommendation |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `ai_ml_competitions` | Competition Lab | lane-manager-ai_ml_competitions-019ec69a | 9 | 1 | 1 | `E:\agent-company-lab\reports\manager-packets\ai_ml_competitions-manager-packet.md` | Resolve service requests before assigning more workers. |
| `ai_resources_lab` | Artificial Resources | lane-manager-ai_resources_lab-20260620 | 0 | 8 | 0 | `E:\agent-company-lab\reports\manager-packets\ai_resources_lab-manager-packet.md` | Create one narrow manager task with evidence requirements before launching seekers. |
| `content_and_social_growth` | Audience/Distribution | lane-manager-content_and_social_growth-019ec613 | 2 | 1 | 1 | `E:\agent-company-lab\reports\manager-packets\content_and_social_growth-manager-packet.md` | Use X/Grok/Radar as read-only discovery until a human-reviewed public-action workflow is assigned. |
| `digital_products_templates_plugins` | Product Studio | lane-manager-digital_products_templates_plugins-019ec69a | 22 | 1 | 4 | `E:\agent-company-lab\reports\manager-packets\digital_products_templates_plugins-manager-packet.md` | Resolve service requests before assigning more workers. |
| `lead_generation_and_sales` | Growth/Sales | lane-manager-lead_generation_and_sales-019ec613 | 5 | 1 | 0 | `E:\agent-company-lab\reports\manager-packets\lead_generation_and_sales-manager-packet.md` | Design non-spam offer and CRM rules before any email, DM, marketplace, or account action. |
| `local_trading_strategy_research` | Quant Research | lane-manager-local_trading_strategy_research-019ec613 | 2 | 1 | 0 | `E:\agent-company-lab\reports\manager-packets\local_trading_strategy_research-manager-packet.md` | Use only local backtests and paper evidence. Real-money execution needs broker, treasury, and kill-switch gates. |
| `money_source_discovery` | Strategic Research | lane-manager-money_source_discovery-019ec699 | 7 | 1 | 1 | `E:\agent-company-lab\reports\manager-packets\money_source_discovery-manager-packet.md` | Resolve service requests before assigning more workers. |
| `paid_code_bounties` | Cashflow Engineering | lane-manager-paid_code_bounties-019ec612 | 22 | 1 | 2 | `E:\agent-company-lab\reports\manager-packets\paid_code_bounties-manager-packet.md` | Use imported rows as negative samples. Launch a fresh-source scout, not a PR worker, until a clean unclaimed bounty is found. |
| `platform_engineering` | Platform Engineering | recovered-profitable-edge-infra | 95 | 2 | 4 | `E:\agent-company-lab\reports\manager-packets\platform_engineering-manager-packet.md` | Finish active platform task, then promote separate lane-manager launches from manager packets. |
| `prediction_market_research` | Markets Research | lane-manager-prediction_market_research-relaunch-20260614 | 9 | 1 | 0 | `E:\agent-company-lab\reports\manager-packets\prediction_market_research-manager-packet.md` | Launch a data/replay manager only. Keep Polymarket data-only and all real-money trading behind eligibility and treasury gates. |
| `premium_customer_intake` | Customer/Operator Success | premium-customer-intake-agent-20260620 | 0 | 1 | 0 | `E:\agent-company-lab\reports\manager-packets\premium_customer_intake-manager-packet.md` | Create one narrow manager task with evidence requirements before launching seekers. |
| `security_bounty_private_reports` | Security Research | lane-manager-security_bounty_private_reports-019ec612 | 20 | 1 | 2 | `E:\agent-company-lab\reports\manager-packets\security_bounty_private_reports-manager-packet.md` | Launch a security manager to rank private-report drafts, rules gates, and proof gaps. No submissions without approval. |
| `submitted_bounty_payouts` | Revenue Collection | external:parallel-payout-worker | 21 | 0 | 0 | `E:\agent-company-lab\reports\manager-packets\submitted_bounty_payouts-manager-packet.md` | Read-only visibility only. Parallel payout worker owns monitoring and GitHub follow-up. |
| `web3_airdrops_grants_hackathons` | Venture/Hackathon Desk | lane-manager-web3_airdrops_grants_hackathons-019ec613 | 5 | 1 | 0 | `E:\agent-company-lab\reports\manager-packets\web3_airdrops_grants_hackathons-manager-packet.md` | Keep as gated venture lane. Launch terms/deadline scouting only; no wallet, deployment, or registration without approval. |
| `youtube_content_channels` | Audience/Distribution | lane-manager-youtube_content_channels-20260620 | 0 | 1 | 0 | `E:\agent-company-lab\reports\manager-packets\youtube_content_channels-manager-packet.md` | Create one narrow manager task with evidence requirements before launching seekers. |
