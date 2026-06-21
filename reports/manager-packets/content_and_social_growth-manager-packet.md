# Manager Packet - content_and_social_growth

Generated UTC: 2026-06-21T12:10:01Z
Department: Audience/Distribution
Lane status: active
Current owner: `lane-manager-content_and_social_growth-019ec613`

## Manager Directive

Own only the `content_and_social_growth` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Prepare a read-only Grok/X research packet through the existing service request; no posts, replies, likes, follows, or settings changes.

## CEO Recommendation

Use X/Grok/Radar as read-only discovery until a human-reviewed public-action workflow is assigned.

## Allowed Worker Types

- trend_scout
- draft_writer
- reply_selector
- analytics_reviewer

## Example Work

- X account manager
- Grok/Radar scouts
- AI-builder audience

## Promotion Gates

- human-sounding draft
- topic fit
- no private data
- no spam pattern

## Required Service Workers

- x_action_executor
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
- post
- reply
- follow
- repost

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `content_grok_x_read_only_research` - Grok/X Read-Only Research | browser_or_api_research | service_request_only | no_public_x_action_no_like_follow_reply_post_no_account_setting_change | Use grok-x-research skill only after service request approval; save prompt/output/verification artifacts. | E:\agent-company-lab\data\x-grok-research\; service_requests |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| local_content_social_x_ai_builder_monetization_source_refresh_complete | `content-social-x-ai-builder-monetization-source-refresh-20260616` - Content/social X AI-builder monetization source refresh | E:\agent-company-lab\reports\content-and-social-growth\x-ai-builder-monetization-source-refresh-20260616.md | Create ai-builder-reply-target-shortlist work packet after parked browser/Grok/X service request review. | Local evidence only; no X public action, login, account setting, ad, payment, KYC, or external side effect. |
| local_seed_evidence | `first-local-evidence-content_and_social_growth-20260615` - First local evidence packet for content_and_social_growth | E:\agent-company-lab\reports\first-local-evidence-packets\content_and_social_growth-first-local-evidence-20260615.md | Refresh the parked browser-readonly service request or create a local prompt/evidence template; no posts, replies, likes, follows, or settings changes. | Generated by platform_engineering as local first-evidence bootstrap; lane manager owns follow-up. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 86 | new | `task-continuity-owner-response-task-lane_goal_response_required-content_and_social_growth` - Submit continuity lane goal response for content_and_social_growth | lane-manager-content_and_social_growth-019ec613 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-008-continuity-restore-response-v1-008-continuity-restore-v1-008-request_lane_goal- | Owner `lane-manager-content_and_social_growth-019ec613` should submit the lane goal artifact for `content_and_social_growth`. |
| 88 | complete | `task-agent-company-atlas-signal-harvest-v1-20260617` - Add custom Signal Harvest Atlas minigame | recovered-profitable-edge-infra |  | Generated signal garden texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Regenerate the Atlas snapshot and verify the Signal Harvest minigame in browser. |
| 84 | complete | `task-fiverr-trends-no-post-review-packet-v1-20260618` - Create Fiverr trends no-post review packet | lane-manager-content_and_social_growth-019ec613 |  | E:\agent-company-lab\reports\content-and-social-growth\fiverr-trends-no-post-review-packet-v1-validation-20260618.json | If the operator approves, create exact public-copy drafts for these three entries as local files only. Do not post, reply, DM, follow, quote, tag, create a Fiverr gig/listing, contact clients, use private data, or run mo |
| 73 | complete | `task-lane-scout-fiverr_2026_trends-20260618` - Lane scout local proof: fiverr 2026 trends | lane-manager-content_and_social_growth-019ec613 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\fiverr-trends-no-post-content-calendar-local-proof-validation.json | Create a no-post draft review packet for the first three calendar entries with tone checks, source links, forbidden claims, and exact approval gates before any X/Fiverr/public action. |
| 70 | complete | `task-content_and_social_growth-startup-20260614` - Lane startup: read packet, choose first proof task, write local plan | lane-manager-content_and_social_growth-019ec613 |  | Local startup memo, source list, gates, and one next proof artifact | Create the first local trend-candidate template from non-account public sources only; X/Grok/Radar remains service-request gated. |
| 65 | complete | `task-content-social-readonly-capture-template-20260614` - Local proof: content/social read-only capture template | lane-manager-content_and_social_growth-019ec613 |  | Capture template and local fixture rows for traction/source candidates, with X/Grok/Radar fields marked awaiting service approval. | Run a future non-account public-source capture using the template; X/Grok/Radar remain gated until exact service-request approval. |
| 30 | complete | `task-content-social-x-ai-builder-monetization-source-refresh-20260616` - Refresh X AI-builder monetization and growth source map | lane-manager-content_and_social_growth-019ec613 |  | E:\agent-company-lab\reports\content-and-social-growth\x-ai-builder-monetization-source-refresh-20260616.md | Create ai-builder-reply-target-shortlist work packet after parked browser/Grok/X service request review. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| needs_review | browser_read_only_session | browser_research | `req-test-browser-readonly-complete-20260614` |  | catalog_required_approval_no_external_action | Generate complete read-only browser service packet acceptance test; no browser opened. | E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614\packet.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| fiverr_trends_no_post_review_packet_ready_local_only | no_post_review_packet | `outcome-fiverr-trends-no-post-review-packet-v1-20260618` | 0.0 | E:\agent-company-lab\reports\content-and-social-growth\fiverr-trends-no-post-review-packet-v1-validation-20260618.json | If the operator approves, create exact public-copy drafts for these three entries as local files only. Do not post, reply, DM, follow, quote, tag, create a Fiverr gig/listing, contact clients, use private data, or run mo |
| fiverr_trends_content_calendar_ready_local_only | local_proof | `outcome-fiverr-trends-no-post-content-calendar-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\fiverr-trends-no-post-content-calendar-local-proof-validation.json | Create a no-post draft review packet for the first three calendar entries with tone checks, source links, forbidden claims, and exact approval gates before any X/Fiverr/public action. |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-signal-harvest-v1-20260617` | 0.0 | reports/agent-company-atlas-signal-harvest-trace-metadata-20260617.json | Browser-verify the Signal Harvest route, animation layer, step controls, generated texture loading, and responsive layout. |
| complete_readonly_fixture | local_proof | `outcome-content-social-readonly-capture-template-20260614` | 0.0 | E:\agent-company-lab\reports\content-and-social-growth\readonly-capture-template-20260614.md | Use the template for non-account public-source captures only; keep X/Grok/Radar awaiting exact service-request approval. |
| planned_next_proof | lane_startup | `outcome-content_and_social_growth-startup-20260614` | 0.0 | E:\agent-company-lab\reports\lane-startup\content_and_social_growth-startup-20260614.md | Create a local read-only trend candidate template from non-account public sources; keep X/Grok/Radar awaiting exact service-request approval. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id content_and_social_growth
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id content_and_social_growth --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `content_and_social_growth` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

