# Manager Packet - web3_airdrops_grants_hackathons

Generated UTC: 2026-06-21T14:12:23Z
Department: Venture/Hackathon Desk
Lane status: active
Current owner: `lane-manager-web3_airdrops_grants_hackathons-019ec613`

## Manager Directive

Own only the `web3_airdrops_grants_hackathons` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Scout terms, deadlines, eligibility, and required account/wallet actions; stop before registration, wallet, deployment, or transaction work.

## CEO Recommendation

Keep as gated venture lane. Launch terms/deadline scouting only; no wallet, deployment, or registration without approval.

## Allowed Worker Types

- program_scout
- terms_reader
- prototype_planner
- submission_packet_writer

## Example Work

- Gitcoin
- Arbitrum/HackQuest
- ecosystem grants
- testnet campaigns

## Promotion Gates

- terms clear
- deadline feasible
- expected value beats code bounties
- account/wallet route approved

## Required Service Workers

- account_registration_worker
- wallet_ops_worker
- legal_terms_worker

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
- registration
- wallet transaction
- deployment
- submission

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `web3_profit_edge_terms_import` - Web3 Terms and Target Import | local_reports | lane_owner_on_demand | no_wallet_registration_deployment_transaction_or_submission_without_user_approval | Run only from web3 lane owner after claim; terms and deadline scouting only. | lane_evidence; web3 manager packet |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| submission_ready | `pe-report-web3-public-code-target-shortlist-a43435a36e55` - Web3 Public Code Target Shortlist | E:\profit-edge-lab\reports\web3-public-code-target-shortlist-latest.md | next: Preserve the v3.0.2 packet, but treat expected value as downgraded by public Consensys 7.27 collision. Submit only once as an explicitly disclosed distinct-impact extension if the Immunefi account path is clean; ot | Read-only venture/security source evidence; wallet, account, and submission gates remain separate. |
| readonly_ingestion_packet_complete | `evidence-ef-esp-readonly-ingestion-packet-20260616` - EF ESP read-only ingestion packet | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-readonly-ingestion-packet-20260616.md | Route to browser_read_only_session service request only after human approval. | Local-only artifact produced by current platform thread; no external side effects. |
| local_ef_esp_classifier_prototype_complete | `ef-esp-wishlist-rfp-classifier-prototype-20260616` - EF ESP Wishlist/RFP classifier prototype | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-wishlist-rfp-classifier-prototype-20260616.md | Create live-read-only Wishlist/RFP ingestion packet only if browser/read-only refresh is approved. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_ef_esp_fit_memo_complete | `ef-esp-fit-memo-20260616` - EF ESP Wishlist/RFP fit memo | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-fit-memo-20260616.md | Create ef-esp-wishlist-rfp-classifier-prototype-20260616.md/json. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_web3_grants_hackathons_bounties_source_refresh_complete | `web3-grants-hackathons-bounties-source-refresh-20260616` - Web3 grants hackathons bounties and airdrop-adjacent source refresh | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\web3-grants-hackathons-bounties-source-refresh-20260616.md | Create web3-opportunity-calendar markdown/json starting with EF ESP Wishlist/RFP and ETHGlobal Lisbon 2026. | Local evidence only; no account, wallet, signature, transaction, deployment, submission, public action, security testing, or real-money side effect. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 72 | new | `task-continuity-lane-next-task-20260621-web3_airdrops_grants_hackathons-006` - Continue proof-derived local next step for web3_airdrops_grants_hackathons | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\proof-derived-continuation-v1-20260621-005.md | Read the evidence artifact for this task, extract exactly one concrete next local step or explicit park/revisit condition from it, and write a compact continuation packet with evidence, gate status, owner, expected next |
| 86 | complete | `task-continuity-owner-response-task-lane_goal_response_required-web3_airdrops_grants_hackathons` - Submit continuity lane goal response for web3_airdrops_grants_hackathons | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-007-continuity-restore-response-v1-007-continuity-restore-v1-007-request_lane_goal- | Owner `lane-manager-web3_airdrops_grants_hackathons-019ec613` should submit the lane goal artifact for `web3_airdrops_grants_hackathons`. |
| 84 | complete | `task-agent-company-atlas-grant-expedition-v1-20260617` - Add custom Grant Expedition Atlas minigame | recovered-profitable-edge-infra |  | Generated grant expedition texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Use browser verification results to tune the Grant Expedition responsive layout, then continue adding lane-specific minigames. |
| 79 | complete | `task-gitcoin-no-submit-grant-fit-memo-v1-20260618` - Create Gitcoin no-submit grant-fit memo | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\gitcoin-no-submit-grant-fit-memo-v1-validation-20260618.json | Prepare sanitized public-good repo outline and exact application draft fields as local files only. Do not log in, use GitHub OAuth, start KYC/Passport, connect wallets, create Allo profiles/pools, submit grants/tag reque |
| 78 | complete | `task-dorahacks-public-directory-fixture-parser-v1-20260618` - Create DoraHacks public-directory fixture parser | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\dorahacks-public-directory-fixture-parser-v1-validation-20260618.json | For local_scout_candidate rows, prepare only sanitized local project-fit writeups, repo/demo outlines, rules checklists, and approval packets. Do not log in, connect wallets, create profiles/BUIDLs/teams, join or registe |
| 76 | complete | `task-continuity-lane-next-task-20260621-web3_airdrops_grants_hackathons-001` - Continue local Web3 opportunity proof | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\manager-packets\web3_airdrops_grants_hackathons-manager-packet.md | Local Web3 opportunity proof packet complete. Next local validation step: create gitcoin-local-application-readiness-checklist-v1-20260621.md with sanitized application fields, evidence citations, gate blockers, expected |
| 74 | complete | `task-continuity-lane-next-task-20260621-web3_airdrops_grants_hackathons-002` - Continue local Gitcoin application readiness checklist | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\web3-local-opportunity-proof-v1-20260621.md | Gitcoin local readiness checklist complete. Next allowed step is a human-approved scoped browser_read_only_session request packet for current round/domain/deadline/rules verification, or park the route; no browsing, wall |
| 72 | complete | `task-continuity-lane-next-task-20260621-web3_airdrops_grants_hackathons-005` - Continue proof-derived local next step for web3_airdrops_grants_hackathons | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\proof-derived-continuation-v1-20260621-004.md | Continuation packet 005 complete. Next expected artifact is gitcoin-readonly-refresh-request-draft-v1-20260621.md beginning with a local evidence header and allowed read-only questions table; stop before agents, ownershi |
| 72 | complete | `task-continuity-lane-next-task-20260621-web3_airdrops_grants_hackathons-004` - Continue proof-derived local next step for web3_airdrops_grants_hackathons | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\proof-derived-continuation-v1-20260621-003.md | Continuation packet 004 complete. Next expected artifact is gitcoin-readonly-refresh-request-draft-v1-20260621.md as a local draft/intake artifact only; stop before agents, ownership mutation, workers, service approval/s |
| 72 | complete | `task-continuity-lane-next-task-20260621-web3_airdrops_grants_hackathons-003` - Continue proof-derived local next step for web3_airdrops_grants_hackathons | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\gitcoin-local-application-readiness-checklist-v1-20260621.md | Continuation packet complete. Next expected artifact is gitcoin-readonly-refresh-request-draft-v1-20260621.md as a local draft only; stop before agents, workers, ownership mutation, service approval/start, browser, walle |
| 70 | complete | `task-ef-esp-fit-memo-20260616` - Create EF ESP Wishlist/RFP fit memo | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-fit-memo-20260616.md | Create ef-esp-wishlist-rfp-classifier-prototype-20260616.md/json. |
| 70 | complete | `task-web3_airdrops_grants_hackathons-startup-20260614` - Lane startup: read packet, choose first proof task, write local plan | lane-manager-web3_airdrops_grants_hackathons-019ec613 |  | Local startup memo, source list, gates, and one next proof artifact | Create one narrow local-only proof task to draft an EF ESP Glamsterdam or Neutral DeFi Risk Intelligence grant proposal packet; no account, wallet, public action, or submission without an approved service request for tha |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| continuation_packet_complete_local_only | proof_derived_continuation | `outcome-proof-derived-continuation-v1-20260621-005` | 0.0 | E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\proof-derived-continuation-v1-20260621-005.md | Next expected artifact: E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\gitcoin-readonly-refresh-request-draft-v1-20260621.md, beginning with a local evidence header and allowed read-only questions table. No |
| continuation_packet_complete_local_only | proof_derived_continuation | `outcome-proof-derived-continuation-v1-20260621-004` | 0.0 | E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\proof-derived-continuation-v1-20260621-004.md | Next expected artifact: E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\gitcoin-readonly-refresh-request-draft-v1-20260621.md. Draft/intake only; no agents, ownership mutation, workers, service approval/star |
| continuation_packet_complete_local_only | proof_derived_continuation | `outcome-proof-derived-continuation-v1-20260621-003` | 0.0 | E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\proof-derived-continuation-v1-20260621-003.md | Next expected artifact: E:\agent-company-lab\reports\web3_airdrops_grants_hackathons\gitcoin-readonly-refresh-request-draft-v1-20260621.md. Draft only; no agents, workers, ownership mutation, service approval/start, brow |
| gitcoin_readiness_checklist_complete_local_only | gitcoin_readiness_checklist | `outcome-gitcoin-local-application-readiness-checklist-v1-20260621` | 0.0 | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\gitcoin-local-application-readiness-checklist-v1-20260621.md | Recommendation: request a future scoped browser_read_only_session only after human approval to verify current Gitcoin round/domain/deadline/rules; do not approve/start account, legal, wallet, public-action, submission, A |
| web3_local_opportunity_packet_complete | local_opportunity_proof | `outcome-web3-local-opportunity-proof-v1-20260621` | 0.0 | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\web3-local-opportunity-proof-v1-20260621.md | Create gitcoin-local-application-readiness-checklist-v1-20260621.md locally; do not open browsers, create accounts, connect wallets, sign messages, submit forms, spend gas, call APIs, approve/start service requests, or m |
| dorahacks_public_directory_fixture_parser_ready_local_only | public_directory_fixture_parser | `outcome-dorahacks-public-directory-fixture-parser-v1-20260618` | 0.0 | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\dorahacks-public-directory-fixture-parser-v1-validation-20260618.json | For local_scout_candidate rows, prepare only sanitized local project-fit writeups, repo/demo outlines, rules checklists, and approval packets. Do not log in, connect wallets, create profiles/BUIDLs/teams, join or registe |
| gitcoin_no_submit_grant_fit_memo_ready_local_only | no_submit_grant_fit_memo | `outcome-gitcoin-no-submit-grant-fit-memo-v1-20260618` | 0.0 | E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\gitcoin-no-submit-grant-fit-memo-v1-validation-20260618.json | Prepare sanitized public-good repo outline and exact application draft fields as local files only. Do not log in, use GitHub OAuth, start KYC/Passport, connect wallets, create Allo profiles/pools, submit grants/tag reque |
| dorahacks_scout_template_ready_local_only | local_proof | `outcome-dorahacks-scout-template-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\dorahacks-scout-template-local-proof-validation.json | Create a DoraHacks public-directory fixture parser from manually saved hackathon/grant/BUIDL rows. Emit local scout rows with status, deadline, theme fit, funding/prize clarity, rules, deliverables, wallet/payment gates, |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id web3_airdrops_grants_hackathons
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id web3_airdrops_grants_hackathons --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `web3_airdrops_grants_hackathons` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

