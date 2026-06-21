# Manager Packet - prediction_market_research

Generated UTC: 2026-06-21T13:06:50Z
Department: Markets Research
Lane status: active
Current owner: `lane-manager-prediction_market_research-relaunch-20260614`

## Manager Directive

Own only the `prediction_market_research` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Create a paper-only replay task for one imported market edge and define the data source of truth, fees, settlement timing, and no-trade gate.

## CEO Recommendation

Launch a data/replay manager only. Keep Polymarket data-only and all real-money trading behind eligibility and treasury gates.

## Allowed Worker Types

- market_scout
- rules_parser
- source_of_truth_monitor
- paper_trader

## Example Work

- Kalshi source latency
- Polymarket data-only
- cross-venue semantic matching
- sports/crypto/weather close-window scans

## Promotion Gates

- venue eligibility verified
- rules verified
- spread/depth/fees captured
- paper evidence threshold met

## Required Service Workers

- market_eligibility_worker
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
- paper trade
- real-money trade

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `prediction_profit_edge_scan_import` - Prediction Market Research Import | local_reports | lane_owner_on_demand_or_scheduled_capture | data_only_until_venue_eligibility_fees_treasury_and_real_money_gate_clear | Run only from prediction_market_research lane owner after claim; use paper/data-only mode. | lane_evidence; prediction manager packet; paper/replay artifact |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| watch_only | `pe-report-cross-venue-next-team-scan-35be3fc7745a` - Cross-Venue Next-Team Scan | E:\profit-edge-lab\reports\cross-venue-next-team-latest.md | next: Watch only; no clean cross-venue trade from current public data. | Read-only market research; no real-money trading from this infrastructure thread. |
| watch_only | `pe-report-polymarket-tennis-edge-packet-68be67f48831` - Polymarket Tennis Edge Packet | E:\profit-edge-lab\reports\polymarket-tennis-edge-packet-latest.md |  | Read-only market research; Polymarket remains data-only unless eligibility is explicitly verified. |
| watch_only | `pe-report-kalshi-btc-range-edge-e654ec4ccb73` - Kalshi BTC Range Edge | E:\profit-edge-lab\reports\kalshi-btc-range-edge-latest.md |  | Read-only market research; no real-money trading from this infrastructure thread. |
| imported | `pe-report-prediction-market-scan-feb389566f62` - Prediction Market Scan | E:\profit-edge-lab\reports\prediction-market-scan-latest.md |  | Read-only market research; no real-money trading from this infrastructure thread. |
| imported | `pe-report-kalshi-btc-settlement-lag-daa29bc18301` - Kalshi BTC Settlement Lag | E:\profit-edge-lab\reports\kalshi-btc-settlement-lag-latest.md |  | Read-only market research; no real-money trading from this infrastructure thread. |
| imported | `pe-report-kalshi-crypto-settlement-lag-7d155d530ac1` - Kalshi Crypto Settlement Lag | E:\profit-edge-lab\reports\kalshi-crypto-settlement-lag-latest.md |  | Read-only market research; no real-money trading from this infrastructure thread. |
| imported | `pe-report-kalshi-generic-settlement-lag-898b589d490d` - Kalshi Generic Settlement Lag | E:\profit-edge-lab\reports\kalshi-settlement-lag-latest.md |  | Read-only market research; no real-money trading from this infrastructure thread. |
| kalshi_crypto_close_window_evidence | `pe-ledger-kalshi_crypto_close_window_evidence-9ed635b33ebd` - kalshi_crypto_close_window_evidence | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Rerun with a wider lookahead or explicit -Ticker/-EventTicker. | Read-only ledger import for future lane managers. |
| kalshi_crypto_close_window_evidence | `pe-ledger-kalshi_crypto_close_window_evidence-ad4f34dc3a36` - kalshi_crypto_close_window_evidence | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Rerun from T-3m to T+7m around the next crypto close; use authenticated CF feed if account/API entitlement is available. | Read-only ledger import for future lane managers. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 90 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-prediction_market_research` - Acknowledge customer follow-up triage for prediction_market_research | lane-manager-prediction_market_research-relaunch-20260614 |  | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-requests-v1-20260621.md | Write one local acknowledgement artifact before starting workers or creating overlapping agents. |
| 76 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-prediction_market_research` - Follow up customer input for prediction_market_research | lane-manager-prediction_market_research-relaunch-20260614 |  | intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.json | Create a local market-angle packet with data needs, venue gates, and no-trade boundary. |
| 92 | complete | `task-continuity-owner-response-task-acknowledgement_response_required-task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-prediction_market_res` - Handle continuity owner acknowledgement response for task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-prediction_market_resea | lane-manager-prediction_market_research-relaunch-20260614 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-004-continuity-restore-response-v1-004-continuity-restore-v1-004-dispatch_stale_own | Existing owner `lane-manager-prediction_market_research-relaunch-20260614` should handle the acknowledgement for `prediction_market_research` locally and report evidence; no duplicate owner or worker should be created. |
| 86 | complete | `task-kalshi-public-data-paper-signal-checker-v1-20260618` - Create Kalshi public-data paper signal checker | lane-manager-prediction_market_research-relaunch-20260614 |  | E:\agent-company-lab\reports\prediction-market-research\kalshi-public-data-paper-signal-checker-v1-validation-20260618.json | Add a historical-settled replay fixture with verified settlement values and keep the checker pessimistic until fees, depth, eligibility, official source, and max-loss fields are proven. Keep account, API keys, signed req |
| 85 | complete | `task-agent-company-atlas-settlement-replay-v1-20260617` - Add custom Settlement Replay Atlas minigame | recovered-profitable-edge-infra |  | Generated settlement replay texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Use browser verification results to tune the Settlement Replay responsive layout, then continue adding lane-specific minigames. |
| 80 | complete | `task-polymarket-saved-market-fixture-checker-v1-20260618` - Create Polymarket saved-market fixture checker | lane-manager-prediction_market_research-relaunch-20260614 |  | E:\agent-company-lab\reports\prediction-market-research\polymarket-saved-market-fixture-checker-v1-validation-20260618.json | Add more manually saved market/event snippets only, or create an exact-scope public-market-data service request. Do not call live APIs, log in, connect/create wallets, use private keys/session signers/API credentials, br |
| 76 | complete | `task-lane-scout-kalshi_public_market_data-20260618` - Lane scout local proof: kalshi public market data | lane-manager-prediction_market_research-relaunch-20260614 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\kalshi-public-data-paper-signal-local-proof-validation.json | Create a local Kalshi fixture parser/checker that consumes saved market/trade/candle-like rows, emits paper-only signal rows with kill reasons, and proves zero promotable candidates on the existing settlement-lag replay; |
| 70 | complete | `task-prediction_market_research-startup-20260614` - Lane startup: read packet, choose first proof task, write local plan | lane-manager-prediction_market_research-relaunch-20260614 |  | Local startup memo, source list, gates, and one next proof artifact | Create one paper-only Kalshi crypto settlement-lag replay task from the startup memo; no accounts, KYC, orders, trades, deposits, withdrawals, wallet actions, broker/API keys, or real-money execution. |
| 67 | complete | `task-prediction-kalshi-crypto-settlement-lag-replay-20260614` - Local proof: Kalshi crypto settlement-lag paper replay | lane-manager-prediction_market_research-relaunch-20260614 |  | Paper-only replay artifact using imported/local packets, deterministic criteria, false-positive notes, and realized_usd=0. | Keep prediction_market_research in data/paper-only mode; optional next proof is reusable local parser/checker against archived packets; no accounts, credentials, orders, trading APIs, deposits, withdrawals, or real-money |
| 62 | complete | `task-lane-scout-polymarket_docs_research-20260618` - Lane scout local proof: polymarket docs research | lane-manager-prediction_market_research-relaunch-20260614 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\polymarket-route-gate-local-proof-validation.json | Create a Polymarket saved-market fixture parser/checker from manually saved docs/API examples only; emit paper-only rows with spread, fee, liquidity, resolution, jurisdiction, wallet, and max-loss kill reasons. Keep live |
| 60 | complete | `task-prediction-archived-packet-parser-checker-20260614` - Next local proof: archived packet parser/checker | lane-manager-prediction_market_research-relaunch-20260614 |  | Reusable local parser/checker against archived close-window packets that reproduces zero actionable candidates on the killed replay set. | Run archived_packet_checker_20260614.py only on future local archived packets; no live venue calls, accounts, credentials, APIs, orders, deposits, withdrawals, or real-money trades. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| polymarket_saved_market_fixture_checker_ready_paper_only | saved_market_fixture_checker | `outcome-polymarket-saved-market-fixture-checker-v1-20260618` | 0.0 | E:\agent-company-lab\reports\prediction-market-research\polymarket-saved-market-fixture-checker-v1-validation-20260618.json | Add more manually saved market/event snippets only, or create an exact-scope public-market-data service request. Do not call live APIs, log in, connect/create wallets, use private keys/session signers/API credentials, br |
| kalshi_public_data_paper_signal_checker_complete_local_only | paper_signal_checker | `outcome-kalshi-public-data-paper-signal-checker-v1-20260618` | 0.0 | E:\agent-company-lab\reports\prediction-market-research\kalshi-public-data-paper-signal-checker-v1-validation-20260618.json | Add a historical-settled replay fixture with verified settlement values and keep the checker pessimistic until fees, depth, eligibility, official source, and max-loss fields are proven. Keep account, API keys, signed req |
| polymarket_route_gate_ready_local_only | local_proof | `outcome-polymarket-route-gate-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\polymarket-route-gate-local-proof-validation.json | Create a Polymarket saved-market fixture parser/checker from manually saved docs/API examples only; emit paper-only rows with spread, fee, liquidity, resolution, jurisdiction, wallet, and max-loss kill reasons. Keep live |
| kalshi_public_data_paper_signal_ready_local_only | local_paper_signal_packet | `outcome-kalshi-public-data-paper-signal-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\kalshi-public-data-paper-signal-local-proof-validation.json | Create a local Kalshi fixture parser/checker that consumes saved market/trade/candle-like rows, emits paper-only signal rows with kill reasons, and proves zero promotable candidates on the existing settlement-lag replay; |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-settlement-replay-v1-20260617` | 0.0 | reports/agent-company-atlas-settlement-replay-trace-metadata-20260617.json | Browser-verify the Settlement Replay module across mobile, docked desktop, and stacked desktop layouts. |
| reproduced_zero_actionable_candidates | local_parser_checker | `outcome-prediction-archived-packet-parser-checker-20260614` | 0.0 | E:\agent-company-lab\reports\prediction-market-research\archived-packet-parser-checker-proof-20260614.md | Use archived_packet_checker_20260614.py on future archived close-window packets only; remain data/paper-only unless gates are explicitly approved. |
| no_trade_no_candidate | paper_replay | `outcome-prediction-kalshi-crypto-settlement-lag-replay-20260614` | 0.0 | E:\agent-company-lab\reports\prediction-market-research\kalshi-crypto-settlement-lag-paper-replay-20260614.md | Keep data/paper-only; optionally implement reusable local parser/checker against archived packets; no accounts, credentials, orders, trading APIs, deposits, withdrawals, or real-money trades. |
| planned_next_proof | lane_startup | `outcome-prediction_market_research-startup-20260614` | 0.0 | E:\agent-company-lab\reports\lane-startup\prediction_market_research-startup-20260614.md | Create one paper-only Kalshi crypto settlement-lag replay task; keep default no-trade gate. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id prediction_market_research
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id prediction_market_research --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `prediction_market_research` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

