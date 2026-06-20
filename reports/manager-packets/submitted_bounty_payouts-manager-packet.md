# Manager Packet - submitted_bounty_payouts

Generated UTC: 2026-06-20T22:49:40Z
Department: Revenue Collection
Lane status: active
Current owner: `other Find profitable edge worker, not this recovered infrastructure thread`

## Manager Directive

Own only the `submitted_bounty_payouts` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

**Read-only boundary:** This lane is read-only in this workspace. Do not monitor, comment, submit, claim, or chase payouts from this thread.

## Recommended Next Task

Read-only here. Do not assign work from this thread; coordinate with the parallel payout worker if the user explicitly reassigns ownership.

## CEO Recommendation

Read-only visibility only. Parallel payout worker owns monitoring and GitHub follow-up.

## Allowed Worker Types

- payout_monitor
- rules_reader
- response_drafter

## Example Work

- RustChain
- Charles microbounties
- existing merged PRs

## Promotion Gates

- owner selection
- explicit payout instruction
- payment transaction evidence

## Required Service Workers

- wallet_public_address_worker
- user_approval_worker

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
- wallet address comment
- payment detail reply

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| promote | `pe-ledger-profit_edge_cycle_1152_rustchain_14015_293_28rtc_s-db270a691c29` - profit_edge_cycle_1152_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1203_rustchain_14015_293_28rtc_s-73fd884af219` - profit_edge_cycle_1203_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1219_rustchain_14015_293_28rtc_s-88b8f05144fd` - profit_edge_cycle_1219_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1548_rustchain_14015_293_28rtc_s-eb0e8f2c75ae` - profit_edge_cycle_1548_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1620_rustchain_14015_293_28rtc_s-d1ae6ef96865` - profit_edge_cycle_1620_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1637_rustchain_14015_293_28rtc_s-60d9e5ab1103` - profit_edge_cycle_1637_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1644_rustchain_14015_293_28rtc_s-785ff4060339` - profit_edge_cycle_1644_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_1653_rustchain_14015_293_28rtc_s-44d10af617c5` - profit_edge_cycle_1653_rustchain_14015_293_28rtc_still_promoted | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Monitor RustChain #14015 and #293 for owner award comments, payment transactions, or explicit request for payout details tied to PRs #25/#27/#28/#24. Do not post wallet/payment details unless explicitly requested through | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-rustchain_payout_routing_followup_promoted_2026061-719f2c9ac48b` - rustchain_payout_routing_followup_promoted_20260613_215135 | https://github.com/Scottcjn/rustchain-bounties/issues/14058 | Watch RustChain wallet registration #14058 and payout follow-up comments on #293/#14015/#14037; if the owner requests clarification, reply with the public RTC wallet name pesoszpesosz and no private seed/key/address mate | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_2156_rustchain_payout_followup_p-f8a98e61a367` - profit_edge_cycle_2156_rustchain_payout_followup_promoted | https://github.com/Scottcjn/rustchain-bounties/issues/14058 | Monitor RustChain wallet registration #14058, payout follow-up comments on #293/#14015/#14037, and Bottube PR #1413 for owner award/payment replies or explicit payout clarification requests; if needed, reply only with pu | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_20260614_104715_rustchain_293_14-26e2ac2a5afb` - profit_edge_cycle_20260614_104715_rustchain_293_14015_payout_monitor_promoted | https://github.com/Scottcjn/rustchain-bounties/issues/14058 | Monitor RustChain wallet registration #14058 and payout follow-up threads #293/#14015 for owner award/payment replies or explicit payout clarification requests tied to PR #24 and PRs #25/#27/#28; if needed, reply only wi | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |
| promote | `pe-ledger-profit_edge_cycle_20260614_105648_rtk_patch_candid-482f7d02a348` - profit_edge_cycle_20260614_105648_rtk_patch_candidate_rustchain_still_promoted | https://github.com/Scottcjn/rustchain-bounties/issues/14058 | Monitor RustChain wallet registration #14058 and payout follow-up threads #293/#14015 for owner award/payment replies or explicit payout clarification requests tied to PR #24 and PRs #25/#27/#28; if needed, reply only wi | Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 83 | complete | `task-agent-company-atlas-payout-vault-v1-20260617` - Add custom Payout Vault Atlas minigame | recovered-profitable-edge-infra |  | Generated texture, custom renderer, responsive styling, trace metadata, and browser verification. | Regenerate the Atlas snapshot and browser-verify the Payout Vault game view. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-payout-vault-v1-20260617` | 0.0 | reports/agent-company-atlas-payout-vault-trace-metadata-20260617.json | Browser-verify the Payout Vault minigame on mobile and desktop and keep monitoring owner-selection/payment-evidence signals. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id submitted_bounty_payouts
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id submitted_bounty_payouts --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `submitted_bounty_payouts` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

