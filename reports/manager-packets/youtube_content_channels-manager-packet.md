# Manager Packet - youtube_content_channels

Generated UTC: 2026-06-21T14:24:32Z
Department: Audience/Distribution
Lane status: active
Current owner: `lane-manager-youtube_content_channels-20260620`

## Manager Directive

Own only the `youtube_content_channels` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Create one narrow task with evidence requirements, duplicate key, owner, and stop gates before launching seekers.

## CEO Recommendation

Create one narrow manager task with evidence requirements before launching seekers.

## Allowed Worker Types

- youtube_channel_manager
- youtube_script_worker
- youtube_asset_pipeline_worker
- reputation_review_worker

## Example Work

- faceless AI explainers
- tool walkthrough shorts
- agent-company build logs
- AI productivity tutorials
- competition/bounty recaps
- evergreen template demos

## Promotion Gates

- channel thesis has clear audience and monetization route
- first 10 no-post scripts pass quality review
- asset pipeline is locally reproducible
- account and public-action gates identified
- copyright and attribution risks reviewed

## Required Service Workers

- account_registration_worker
- legal_terms_worker
- public_action_worker
- brand_review_worker

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
- channel creation
- video upload
- comment reply
- thumbnail publication
- public promotion
- ad or sponsor outreach

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
| none |  |  |  |  |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 76 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-youtube_content_channels` - Follow up customer input for youtube_content_channels | lane-manager-youtube_content_channels-20260620 |  | intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.json | Create a YouTube lane work packet that turns the capsule into one script/storyboard or material-analysis task. |
| 117 | complete | `task-youtube-no-post-content-batch-v1-20260620` - Create first YouTube no-post content batch | lane-manager-youtube_content_channels-20260620 |  | No-post batch, production manifest, reputation/copyright checklist, material route template, customer update feed, trace event | Expand one brief into a full local script/storyboard or create control_plane_capacity_benchmark_packet_v1. |
| 92 | complete | `task-continuity-owner-response-task-acknowledgement_response_required-task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-youtube_content_chann` - Handle continuity owner acknowledgement response for task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-youtube_content_channel | lane-manager-youtube_content_channels-20260620 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-005-continuity-restore-response-v1-005-continuity-restore-v1-005-dispatch_stale_own | Existing owner `lane-manager-youtube_content_channels-20260620` should handle the acknowledgement for `youtube_content_channels` locally and report evidence; no duplicate owner or worker should be created. |
| 90 | complete | `task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-youtube_content_channels` - Acknowledge customer follow-up triage for youtube_content_channels | lane-manager-youtube_content_channels-20260620 |  | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-requests-v1-20260621.md | Owner acknowledgement evidence linked at E:\agent-company-lab\reports\youtube-content-channels-continuity-acknowledgement-next-action-v1-20260621.md; continue the lane follow-up locally with existing owner and no duplica |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| complete | youtube_no_post_content_batch | `outcome-youtube-no-post-content-batch-v1-20260620` | 0.0 | E:\agent-company-lab\reports\youtube-no-post-content-batch-v1-20260620.md | Expand one brief into a full local script/storyboard or create control_plane_capacity_benchmark_packet_v1. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id youtube_content_channels
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id youtube_content_channels --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `youtube_content_channels` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

