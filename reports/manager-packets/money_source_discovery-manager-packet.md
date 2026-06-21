# Manager Packet - money_source_discovery

Generated UTC: 2026-06-21T13:40:01Z
Department: Strategic Research
Lane status: active
Current owner: `lane-manager-money_source_discovery-019ec699`

## Manager Directive

Own only the `money_source_discovery` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Use the starter browser-read-only service request to build a source registry of monetizable venues, payout routes, account gates, and first proof tasks.

## CEO Recommendation

Resolve service requests before assigning more workers.

## Allowed Worker Types

- source_mapper
- venue_rules_reader
- expected_value_ranker
- lane_launcher

## Example Work

- new bounty sources
- AI competitions
- marketplace opportunities
- grant and affiliate source registries

## Promotion Gates

- source is current
- payout or monetization path explicit
- account and legal gates identified
- first proof artifact feasible under 2 hours

## Required Service Workers

- browser_action_worker
- account_registration_worker
- chief_risk_officer

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
- browser read-only research
- account registration packet
- data/API access review

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `money_source_discovery_public_venue_source_seed` - Money Source Discovery Public Venue Source Seed | public_venue_registry | lane_owner_on_demand_or_weekly | read_only_discovery_no_registration_outreach_wallet_payment_or_submission | Prepare a read-only source registry scan only after lane manager claim; classify venue, payout route, account gate, and proof artifact. | E:\agent-company-lab\reports\money-source-discovery\public-venue-source-refresh-YYYYMMDD.md; lane_evidence; service_request_candidates |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| local_profile_packet_draft_complete | `evidence-ai-training-profile-packet-draft-20260616` - AI training profile packet draft | E:\agent-company-lab\reports\money-source-discovery\ai-training-profile-packet-draft-20260616.md | Create platform-specific gate matrix only after read-only platform source refresh is approved. | Local-only artifact produced by current platform thread; no external side effects. |
| local_ai_training_sample_pack_complete | `ai-training-sample-pack-20260616` - AI training sample pack | E:\agent-company-lab\reports\money-source-discovery\ai-training-sample-pack-20260616.md | Create ai-training-profile-packet-draft-20260616.md with do-not-submit status. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_opentrain_role_feed_worksheet_complete | `opentrain-role-feed-worksheet-20260616` - OpenTrain AI role-feed worksheet | E:\agent-company-lab\reports\money-source-discovery\opentrain-role-feed-worksheet-20260616.md | Create a local ai-training-sample-pack task for math reasoning, code QA, and RLHF samples. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_top_registry_work_packets_complete | `money-source-top-registry-work-packets-20260616` - Top public venue registry work packets | E:\agent-company-lab\reports\money-source-discovery\top-registry-work-packets-20260616.md | Execute the six promoted local proof tasks in lane order, starting with OpenTrain role-feed worksheet and Algora explicit-payout worksheet. | Local task-promotion only. No browser session, account, wallet, payment, public action, security testing, worker start, API call, or real-money action occurred. |
| local_money_source_public_venue_registry_complete | `money-source-public-venue-registry-20260616` - Money source public venue registry | E:\agent-company-lab\reports\money-source-discovery\public-venue-registry-20260616.md | Promote top registry rows into lane-specific work packets: OpenTrain role-feed worksheet, Algora explicit-payout issue worksheet, EF ESP fit memo, Devpost prize calendar, ARC Prize feasibility memo, and Upwork AI workflo | Local report-only registry. No account, payment, wallet, public action, browser session, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_money_source_public_venue_source_refresh_complete | `money-source-public-venue-source-refresh-20260616` - Money source public venue source refresh | E:\agent-company-lab\reports\money-source-discovery\public-venue-source-refresh-20260616.md | Create public-venue-registry markdown/json with at least 20 scored venue rows and route each row to a lane. | Local evidence only; no signup, login, payment, wallet, public action, security testing, submission, or real-money side effect. |
| local_seed_evidence | `first-local-evidence-money_source_discovery-20260615` - First local evidence packet for money_source_discovery | E:\agent-company-lab\reports\first-local-evidence-packets\money_source_discovery-first-local-evidence-20260615.md | Create a local venue-registry template with payout route, proof artifact, account gate, and first safe task; no registration, outreach, wallet, payment, or submission. | Generated by platform_engineering as local first-evidence bootstrap; lane manager owns follow-up. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 76 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-money_source_discovery` - Follow up customer input for money_source_discovery | lane-manager-money_source_discovery-019ec699 |  | intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.json | Decide whether this implies a new money path, an existing lane update, or a watch-list revisit trigger. |
| 92 | complete | `task-continuity-owner-response-task-acknowledgement_response_required-task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-money_source_discover` - Handle continuity owner acknowledgement response for task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-money_source_discovery | lane-manager-money_source_discovery-019ec699 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-002-continuity-restore-response-v1-002-continuity-restore-v1-002-dispatch_stale_own | Existing owner `lane-manager-money_source_discovery-019ec699` should handle the acknowledgement for `money_source_discovery` locally and report evidence; no duplicate owner or worker should be created. |
| 92 | complete | `task-money-path-graduation-action-queue-v1-20260618` - Money path graduation action queue v1 | recovered-profitable-edge-infra |  | E:\agent-company-lab\reports\money-path-graduation-action-queue-v1-validation-20260618.json | Have lane managers claim the top ranked queue item and create only the named local artifact/parser/checker/draft. If the next action needs account, wallet, payment, trade, submission, public action, worker/runtime, model |
| 90 | complete | `task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-money_source_discovery` - Acknowledge customer follow-up triage for money_source_discovery | lane-manager-money_source_discovery-019ec699 |  | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-requests-v1-20260621.md | Owner acknowledgement evidence linked at E:\agent-company-lab\reports\money-source-discovery-continuity-live-handoff-acknowledgement-v1-20260621.md; continue the lane follow-up locally with existing owner and no duplicat |
| 90 | complete | `task-money-path-lane-scout-packet-v1-20260618` - Build money_path_lane_scout_packet_v1 from refreshed current money paths | recovered-profitable-edge-infra |  | E:\agent-company-lab\reports\money-path-lane-scout-packet-v1-validation-20260618.json | Have lane managers execute the highest-priority local proof tasks one at a time, starting with Upwork AI offer matrix, PromptBase approval rubric, Algora claim-readiness checklist, and ARC baseline packet. Keep every acc |
| 88 | complete | `task-money-path-expansion-radar-wave17-20260618` - Run money-path expansion radar wave 17 | recovered-profitable-edge-infra |  | E:\agent-company-lab\reports\money-path-expansion-radar-wave17-validation-20260618.json | Use wave 17 to create the top four local proof packets without account registration, public actions, security testing, trades, wallets, or payment setup. |
| 88 | complete | `task-agent-company-atlas-venue-mapper-v1-20260617` - Add custom Venue Mapper Atlas minigame | recovered-profitable-edge-infra |  | Generated venue mapper texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Verify and keep evolving lane-specific minigames for the next expandable money path. |
| 72 | complete | `task-msd-001-local-routing-decision-20260614` - Route MSD-001 as local money-source control row | recovered-profitable-edge-infra |  | Local routing report proving MSD-001 is the only unblocked queue item and MSD-002 through MSD-016 remain blocked. | Generate a machine-readable blocked-row action queue for MSD-002 through MSD-016; no browser/current-source verification until service request approval. |
| 71 | complete | `task-money-source-blocked-row-action-queue-20260614` - Generate blocked-row action queue for MSD-002 through MSD-016 | recovered-profitable-edge-infra |  | Machine-readable queue listing each blocked MSD row, first required gate, prohibited actions, and safe local next action. | Package the highest-leverage local proof template among MSD-003 through MSD-016; browser/current-source verification remains blocked until service approval. |
| 70 | complete | `task-opentrain-role-feed-worksheet-20260616` - Create OpenTrain AI role-feed worksheet | lane-manager-money_source_discovery-019ec699 |  | E:\agent-company-lab\reports\money-source-discovery\opentrain-role-feed-worksheet-20260616.md | Create a local ai-training-sample-pack task for math reasoning, code QA, and RLHF samples. |
| 70 | complete | `task-money_source_discovery-startup-20260614` - Lane startup: read packet, choose first proof task, write local plan | lane-manager-money_source_discovery-019ec699 |  | Local startup memo, source list, gates, and one next proof artifact | Run money_source_weekly_delta_local_dry_run from local Wave-4 files only; browser capture remains blocked until req-wave4-money-source-discovery-browser-readonly-20260614 is approved. |
| 69 | complete | `task-money-source-weekly-delta-local-dry-run-20260614` - Local proof: money source weekly delta dry run | lane-manager-money_source_discovery-019ec699 |  | Local weekly delta table with at least ten candidate rows, owner lanes, gates, and proof artifact paths; realized_usd=0. | Use the local 16-row weekly delta as a proof queue; browser/current-source verification remains blocked until req-wave4-money-source-discovery-browser-readonly-20260614 is approved. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| needs_review | browser_read_only_session | browser_research | `req-wave4-money-source-discovery-browser-readonly-20260614` |  | catalog_required_approval_no_external_action | Read public opportunity-source directories and capture monetizable source candidates; no browser side effects. | E:\agent-company-lab\requests\service-requests\req-wave4-money-source-discovery-browser-readonly-20260614\packet.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| money_path_graduation_queue_ready_local_only | local_queue | `outcome-money-path-graduation-action-queue-v1-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-graduation-action-queue-v1-validation-20260618.json | Have lane managers claim the top ranked queue item and create only the named local artifact/parser/checker/draft. If the next action needs account, wallet, payment, trade, submission, public action, worker/runtime, model |
| money_path_lane_scout_packet_ready_local_only | local_scout_packet | `outcome-money-path-lane-scout-packet-v1-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packet-v1-validation-20260618.json | Have lane managers execute the highest-priority local proof tasks one at a time, starting with Upwork AI offer matrix, PromptBase approval rubric, Algora claim-readiness checklist, and ARC baseline packet. Keep every acc |
| complete_read_only_money_path_map_ready | money_path_expansion_research | `outcome-money-path-expansion-radar-wave17-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-expansion-radar-wave17-validation-20260618.json | Create local proof packets for security rules ranking, AI automation offer, paid-code fresh bounty scorecard, and AI training platform gate matrix; do not register accounts, submit, trade, post, test security targets, or |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-venue-mapper-v1-20260617` | 0.0 | reports/agent-company-atlas-venue-mapper-trace-metadata-20260617.json | Browser-verify the Venue Mapper module across mobile, docked desktop, and stacked desktop layouts. |
| local_profile_packet_draft_complete | local_proof_artifact | `outcome-ai-training-profile-packet-draft-20260616` | 0.0 | E:\agent-company-lab\reports\money-source-discovery\ai-training-profile-packet-draft-20260616.md | Create platform-specific gate matrix only after read-only platform source refresh is approved. |
| complete | local_ai_training_sample_pack | `outcome-ai-training-sample-pack-20260616` | 0.0 | E:\agent-company-lab\reports\money-source-discovery\ai-training-sample-pack-20260616.md | Create ai-training-profile-packet-draft-20260616.md with do-not-submit status. |
| complete | local_ai_training_role_feed_worksheet | `outcome-opentrain-role-feed-worksheet-20260616` | 0.0 | E:\agent-company-lab\reports\money-source-discovery\opentrain-role-feed-worksheet-20260616.md | Create a local ai-training-sample-pack task for math reasoning, code QA, and RLHF samples. |
| complete | local_registry_task_promotion | `outcome-money-source-top-registry-work-packets-20260616` | 0.0 | E:\agent-company-lab\reports\money-source-discovery\top-registry-work-packets-20260616.md | Execute six promoted local proof tasks without external side effects. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id money_source_discovery
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id money_source_discovery --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `money_source_discovery` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

