# Manager Packet - local_trading_strategy_research

Generated UTC: 2026-06-21T14:12:23Z
Department: Quant Research
Lane status: active
Current owner: `lane-manager-local_trading_strategy_research-019ec613`

## Manager Directive

Own only the `local_trading_strategy_research` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Inventory local backtest artifacts and define a paper-only evidence standard; no broker/API/trade action.

## CEO Recommendation

Use only local backtests and paper evidence. Real-money execution needs broker, treasury, and kill-switch gates.

## Allowed Worker Types

- strategy_miner
- backtest_runner
- data_quality_auditor
- risk_reviewer

## Example Work

- existing v2/v3 backtests
- MT5 systems
- OpenClaw trading infra

## Promotion Gates

- out-of-sample proof
- cost/slippage included
- drawdown acceptable
- no real-money execution without gate

## Required Service Workers

- broker_eligibility_worker
- treasury_risk_worker

## Service Bureau Catalog

Use these request types when this lane needs registration, browser, wallet, public action, outreach, trading, model/API, data/API, security-report, payment/legal, or credential support. The catalog defines intake and hard stops; it does not approve the action.

| Status | Type | Service | Owner Role | Purpose |
| --- | --- | --- | --- | --- |
| available | account_registration | `account_registration_intake` | `account_registration_worker` | Prepare a local registration packet for a venue without creating the account or accepting terms. |
| available | browser_research | `browser_read_only_session` | `browser_action_worker` | Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings. |
| available | data_purchase_api_access | `data_purchase_api_access_gate` | `chief_risk_officer` | Review paid APIs, premium data, scraped data, or restricted sources before a lane depends on them. |
| gated | github_public_action | `github_public_action_gate` | `reputation_review_worker` | Review PRs, issue comments, bounty claims, advisory comments, and maintainer-facing GitHub actions before public execution. |
| available | legal_kyc_tax_payment | `legal_kyc_tax_payment_gate` | `chief_risk_officer` | Summarize legal, KYC, tax, billing, payment, and account-contract obligations before the user decides. |
| available | model_api_execution | `model_api_execution_gate` | `observability_worker` | Approve and observe real model/API executions after dry-runs pass and cost/data scope is explicit. |
| available | outreach_delivery | `outreach_delivery_gate` | `reputation_review_worker` | Review and gate outbound email, DM, proposal, marketplace, or form-contact actions for non-spam and brand safety. |
| gated | public_action_execution | `public_action_execution` | `browser_action_worker` | Execute one exact approved public action, such as a reply, post, PR comment, bounty claim, proposal submission, or form submission. |
| available | real_money_trade | `real_money_trade_gate` | `chief_risk_officer` | Evaluate whether a paper-only market or trading hypothesis is even eligible for real-money consideration. |
| available | secrets_credentials_handling | `secrets_credentials_handling_gate` | `chief_risk_officer` | Define how a task can use credentials, tokens, API keys, private files, cookies, or session state without leaking or storing sensitive data. |
| available | security_report_submission | `security_report_submission_gate` | `chief_risk_officer` | Gate private vulnerability reports, advisory submissions, and program contacts after local-only proof work. |
| gated | wallet_public_address_or_payment_reply | `wallet_public_address_response` | `wallet_ops_worker` | Prepare or verify the exact public payment-address response for payout collection after user approval. |
| available | wallet_setup | `wallet_setup_packet` | `wallet_ops_worker` | Prepare wallet requirements, network/token details, custody choices, and user action checklist without controlling keys or funds. |

## Forbidden Direct Side Effects

These require a scoped service request and approval before any execution:
- paper deployment
- real-money trade

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `local_trading_research_import` - Local Trading Research Import | local_workspace | lane_owner_on_demand | paper_backtest_only_until_broker_treasury_and_real_money_gate_clear | Read-only inventory first; no broker/API/trading action. | local_trading manager packet |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| local_trading_paper_backtest_source_refresh_complete | `local-trading-paper-backtest-source-refresh-20260616` - Local trading paper-only backtest source refresh | E:\agent-company-lab\reports\local-trading-strategy-research\paper-trading-backtest-source-refresh-20260616.md | Create paper-replay-standard and local-strategy-inventory artifacts without opening credentials or broker/account files. | Local evidence only; no broker login, API key use, account inspection, balance inspection, order placement, deposit, withdrawal, transfer, subscription, financial advice, or real-money action. |
| local_seed_evidence | `first-local-evidence-local_trading_strategy_research-20260615` - First local evidence packet for local_trading_strategy_research | E:\agent-company-lab\reports\first-local-evidence-packets\local_trading_strategy_research-first-local-evidence-20260615.md | Inventory local backtest evidence standards and kill-switch fields; no broker, exchange, prediction-market, API, deposit, withdrawal, or order action. | Generated by platform_engineering as local first-evidence bootstrap; lane manager owns follow-up. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 72 | new | `task-continuity-lane-next-task-20260621-local_trading_strategy_research-006` - Continue proof-derived local next step for local_trading_strategy_research | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\local_trading_strategy_research\proof-derived-continuation-v1-20260621-005.md | Read the evidence artifact for this task, extract exactly one concrete next local step or explicit park/revisit condition from it, and write a compact continuation packet with evidence, gate status, owner, expected next |
| 86 | complete | `task-continuity-owner-response-task-lane_goal_response_required-local_trading_strategy_research` - Submit continuity lane goal response for local_trading_strategy_research | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-004-continuity-restore-response-v1-004-continuity-restore-v1-004-request_lane_goal- | Owner `lane-manager-local_trading_strategy_research-019ec613` should submit the lane goal artifact for `local_trading_strategy_research`. |
| 86 | complete | `task-agent-company-atlas-paper-trial-v1-20260617` - Add custom Paper Trial Atlas minigame | recovered-profitable-edge-infra |  | Generated paper trial texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Verify and continue expanding lane-specific minigames for remaining money paths. |
| 76 | complete | `task-continuity-lane-next-task-20260621-local_trading_strategy_research-001` - Continue local trading paper-research proof | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\manager-packets\local_trading_strategy_research-manager-packet.md | Create local-trading-replay-data-readiness-v1-20260621.md from non-sensitive local file metadata only; no broker/API/paid-data/order/trade/browser/account action. |
| 74 | complete | `task-continuity-lane-next-task-20260621-local_trading_strategy_research-002` - Continue local trading no-key replay prep | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\local-trading\local-trading-paper-research-proof-v1-20260621.md | Create local-trading-selected-dataset-readiness-v1-20260621.md by validating the selected JSON locally for schema, timestamp order, OHLC invariants, and spread availability only; no broker/API/account/paid-data/order/tra |
| 72 | complete | `task-continuity-lane-next-task-20260621-local_trading_strategy_research-005` - Continue proof-derived local next step for local_trading_strategy_research | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\local_trading_strategy_research\proof-derived-continuation-v1-20260621-004.md | Write E:\agent-company-lab\reports\local-trading\local-trading-selected-dataset-readiness-v1-20260621.md by validating the selected local JSON for readiness counts only; no replay, agent/worker creation, ownership mutati |
| 72 | complete | `task-continuity-lane-next-task-20260621-local_trading_strategy_research-004` - Continue proof-derived local next step for local_trading_strategy_research | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\local_trading_strategy_research\proof-derived-continuation-v1-20260621-003.md | Write E:\agent-company-lab\reports\local-trading\local-trading-selected-dataset-readiness-v1-20260621.md by validating the selected local JSON for readiness counts only; no replay, agent/worker creation, ownership mutati |
| 72 | complete | `task-continuity-lane-next-task-20260621-local_trading_strategy_research-003` - Continue proof-derived local next step for local_trading_strategy_research | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\local-trading\local-trading-no-key-replay-prep-v1-20260621.md | Write E:\agent-company-lab\reports\local-trading\local-trading-selected-dataset-readiness-v1-20260621.md by validating the selected local JSON for counts/schema only; no replay, agents/workers, ownership mutation, servic |
| 70 | complete | `task-local_trading_strategy_research-startup-20260614` - Lane startup: inventory local backtest artifacts and define paper-only evidence standard | lane-manager-local_trading_strategy_research-019ec613 |  | Local startup memo, local artifact inventory, paper-only evidence standard, gates, and one next proof task | Create the first narrow local proof task: XAU paper-evidence intake and closed-event-only ledger reconciliation. |
| 64 | complete | `task-local-trading-xau-paper-evidence-intake-20260614` - Local proof: XAU paper-evidence intake checklist | lane-manager-local_trading_strategy_research-019ec613 |  | Paper-evidence intake checklist/report reconciling local XAU watch artifacts against audit requirements, with no live signals or broker action. | Wait for already-local XAU platform data or approved data-refresh service request, then update only open paper-watch events; no broker/API/order/live-signal action. |
| 25 | complete | `task-local-trading-paper-backtest-source-refresh-20260616` - Refresh paper-only trading backtest and dry-run source map | lane-manager-local_trading_strategy_research-019ec613 |  | E:\agent-company-lab\reports\local-trading-strategy-research\paper-trading-backtest-source-refresh-20260616.md | Create paper-replay-standard and local-strategy-inventory artifacts without opening credentials or broker/account files. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| complete | proof_derived_continuation | `outcome-local-trading-proof-derived-continuation-v1-20260621-005` | 0.0 | E:\agent-company-lab\reports\local_trading_strategy_research\proof-derived-continuation-v1-20260621-005.md | Write the selected-dataset readiness-count artifact locally only; keep replay, agent/worker creation, ownership mutation, service approvals, browser, public action, APIs, spend, trade, brokers, paid data, and contact gat |
| complete | proof_derived_continuation | `outcome-local-trading-proof-derived-continuation-v1-20260621-004` | 0.0 | E:\agent-company-lab\reports\local_trading_strategy_research\proof-derived-continuation-v1-20260621-004.md | Write the selected-dataset readiness-count artifact locally only; keep replay, agent/worker creation, ownership mutation, service approvals, browser, public action, APIs, spend, trade, brokers, paid data, and contact gat |
| complete | proof_derived_continuation | `outcome-local-trading-proof-derived-continuation-v1-20260621-003` | 0.0 | E:\agent-company-lab\reports\local_trading_strategy_research\proof-derived-continuation-v1-20260621-003.md | Write the selected-dataset readiness-count artifact locally only; keep replay, agents/workers, ownership mutation, service approvals, browser, public action, APIs, spend, trade, brokers, paid data, and contact gates clos |
| complete | no_key_local_replay_prep | `outcome-local-trading-no-key-replay-prep-v1-20260621` | 0.0 | E:\agent-company-lab\reports\local-trading\local-trading-no-key-replay-prep-v1-20260621.md | Validate selected local JSON for readiness counts only; keep account, broker, API, paid-data, order, spend, and trading gates closed. |
| complete | local_paper_research_proof | `outcome-local-trading-paper-research-proof-v1-20260621` | 0.0 | E:\agent-company-lab\reports\local-trading\local-trading-paper-research-proof-v1-20260621.md | Create local replay data readiness packet using non-sensitive local metadata only; keep broker/API/paid-data/order/trade gates closed. |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-paper-trial-v1-20260617` | 0.0 | reports/agent-company-atlas-paper-trial-trace-metadata-20260617.json | Browser-verify the Paper Trial module across mobile, docked desktop, and stacked desktop layouts. |
| xau_paper_evidence_intake_ready_no_promotion | local_paper_proof | `outcome-local-trading-xau-paper-evidence-intake-20260614` | 0.0 | E:\agent-company-lab\reports\local-trading-strategy-research\xau-paper-evidence-intake-20260614.md | Wait for already-local XAU platform data or approved data-refresh service request; update only open watch events and keep broker/API/order/live-signal gates closed. |
| planned_next_proof | lane_startup | `outcome-local_trading_strategy_research-startup-20260614` | 0.0 | E:\agent-company-lab\reports\lane-startup\local_trading_strategy_research-startup-20260614.md | Create one local XAU paper-evidence intake task; no broker/API/order/live-signal action. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id local_trading_strategy_research
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id local_trading_strategy_research --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `local_trading_strategy_research` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

