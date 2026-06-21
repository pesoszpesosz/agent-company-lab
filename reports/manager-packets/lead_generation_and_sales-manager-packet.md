# Manager Packet - lead_generation_and_sales

Generated UTC: 2026-06-21T13:06:50Z
Department: Growth/Sales
Lane status: active
Current owner: `lane-manager-lead_generation_and_sales-019ec613`

## Manager Directive

Own only the `lead_generation_and_sales` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Draft non-spam offer rules, target filters, proof artifacts, and review gates before any outreach account or message action.

## CEO Recommendation

Design non-spam offer and CRM rules before any email, DM, marketplace, or account action.

## Allowed Worker Types

- lead_scout
- offer_builder
- outreach_drafter
- crm_worker

## Example Work

- AI automation service leads
- small-business website fixes
- security hardening offers
- freelance marketplaces

## Promotion Gates

- legal outreach route
- clear offer
- non-spam targeting
- tracking and opt-out

## Required Service Workers

- outreach_policy_worker
- account_identity_worker

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
- email
- DM
- proposal submission

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `lead_generation_policy_sources` - Lead Generation Policy and Offer Sources | policy_and_crm_design | lane_owner_on_demand | no_spam_no_outreach_no_account_action_without_service_request_and_policy_review | Draft policy and offer packets only; no email, DM, marketplace, or CRM action. | lead generation manager packet |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| local_profile_proposal_draft_complete | `evidence-upwork-profile-and-proposal-draft-20260616` - Upwork profile and proposal local draft | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-profile-and-proposal-draft-20260616.md | Create marketplace approval request packet before any Upwork account/profile/proposal action. | Local-only artifact produced by current platform thread; no external side effects. |
| local_ai_workflow_audit_proof_asset_complete | `ai-workflow-audit-proof-asset-agency-reporting-20260616` - AI workflow audit proof asset for agency reporting | E:\agent-company-lab\reports\lead-generation-and-sales\ai-workflow-audit-proof-asset-agency-reporting-20260616.md | Create upwork-profile-and-proposal-draft-20260616.md only as a local draft. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_upwork_ai_workflow_audit_offer_complete | `upwork-ai-workflow-audit-offer-20260616` - Upwork AI workflow audit offer packet | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-ai-workflow-audit-offer-20260616.md | Create ai-workflow-audit-proof-asset-agency-reporting-20260616.md/json using synthetic data only. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_leadgen_ai_service_source_refresh_complete | `leadgen-ai-service-source-refresh-20260616` - Lead generation AI service source refresh | E:\agent-company-lab\reports\lead-generation-and-sales\ai-service-leadgen-source-refresh-20260616.md | Create ai-workflow-audit-offer-packet markdown/json with ICP, proof asset, and outreach compliance gate. | Local evidence only; no scraping, account signup, CRM import, email, DM, call, InMail, ad, proposal, public action, or customer-data processing. |
| local_seed_evidence | `first-local-evidence-lead_generation_and_sales-20260615` - First local evidence packet for lead_generation_and_sales | E:\agent-company-lab\reports\first-local-evidence-packets\lead_generation_and_sales-first-local-evidence-20260615.md | Draft a local offer and source-category rubric; no scraping, CRM upload, email, DM, marketplace proposal, or contact form action. | Generated by platform_engineering as local first-evidence bootstrap; lane manager owns follow-up. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 93 | complete | `task-upwork-no-send-approval-request-packet-20260618` - Create no-send Upwork approval request packet | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-no-send-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for one Upwork account/profile/proposal review. Do not log in, create or edit a profile, select a live job, send a proposal, message a client, a |
| 91 | complete | `task-lane-scout-upwork_ai_freelance_work-20260618` - Lane scout local proof: upwork ai freelance work | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\upwork-ai-offer-matrix-local-proof-validation.json | Create a no-send Upwork approval request packet for the recommended first offer only after human review; keep account, proposal, payment, client data, credentials, public action, worker/runtime, model/MCP, and external s |
| 90 | complete | `task-upwork-ai-skills-no-send-approval-request-packet-20260618` - Create Upwork AI-skills-demand no-send approval request packet | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-ai-skills-no-send-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for one Upwork AI Integration Workflow Audit account/profile/proposal review. Do not log in, create/edit a profile or portfolio, choose a live j |
| 87 | complete | `task-agent-company-atlas-offer-route-v1-20260617` - Add custom Offer Route Atlas minigame | recovered-profitable-edge-infra |  | Generated offer route texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Verify and continue expanding lane-specific minigames for remaining money paths. |
| 86 | complete | `task-continuity-owner-response-task-lane_goal_response_required-lead_generation_and_sales` - Submit continuity lane goal response for lead_generation_and_sales | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-008-continuity-restore-response-v1-008-continuity-restore-v1-008-request_lane_goal- | Owner `lane-manager-lead_generation_and_sales-019ec613` should submit the lane goal artifact for `lead_generation_and_sales`. |
| 84 | complete | `task-lane-scout-upwork_2026_ai_skills_demand-20260618` - Lane scout local proof: upwork 2026 ai skills demand | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\upwork-ai-skills-fit-score-local-proof-validation.json | Create a no-send Upwork approval request packet for the recommended AI Integration Workflow Audit only after human review; keep account, profile, proposal, client data, credentials, payment, public action, worker/runtime |
| 70 | complete | `task-upwork-ai-workflow-audit-offer-20260616` - Create Upwork AI workflow audit offer packet | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-ai-workflow-audit-offer-20260616.md | Create ai-workflow-audit-proof-asset-agency-reporting-20260616.md/json using synthetic data only. |
| 70 | complete | `task-lead_generation_and_sales-startup-20260614` - Lane startup: read packet, choose first proof task, write local plan | lane-manager-lead_generation_and_sales-019ec613 |  | Local startup memo, source list, gates, and one next proof artifact | Create local-only proof artifact: website intake audit rubric and fictional sample packet; do not identify or contact real leads. |
| 68 | complete | `task-ai-workflow-audit-proof-asset-agency-reporting-20260616` - Create AI workflow audit proof asset for agency reporting | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\lead-generation-and-sales\ai-workflow-audit-proof-asset-agency-reporting-20260616.md | Create upwork-profile-and-proposal-draft-20260616.md only as a local draft. |
| 66 | complete | `task-upwork-profile-and-proposal-draft-20260616` - Create Upwork profile and proposal local draft | lane-manager-lead_generation_and_sales-019ec613 |  | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-profile-and-proposal-draft-20260616.md | Create marketplace approval request packet before any Upwork account/profile/proposal action. |
| 64 | complete | `task-leadgen-fictional-audit-rubric-packet-20260614` - Local proof: fictional lead-audit rubric packet | lane-manager-lead_generation_and_sales-019ec613 |  | Local-only audit rubric and fictional sample proof packet with pass/fail criteria, exclusions, review gates, and no real prospect data. | If the lane continues, create a separate source-category policy review task only; do not identify real leads without an approved service request. |
| 61 | complete | `task-leadgen-source-category-policy-review-20260614` - Next local proof: source-category policy review | lane-manager-lead_generation_and_sales-019ec613 |  | Local policy review of allowed/prohibited source categories for future lead discovery, with data handling gates and no real leads. | If the lane continues, draft a service-request template for a future tiny manual source-category review; keep real prospect data blocked unless explicitly approved. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| upwork_ai_skills_no_send_approval_packet_ready_local_only | approval_packet | `outcome-upwork-ai-skills-no-send-approval-request-packet-20260618` | 0.0 | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-ai-skills-no-send-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for one Upwork AI Integration Workflow Audit account/profile/proposal review. Do not log in, create/edit a profile or portfolio, choose a live j |
| upwork_no_send_approval_packet_ready_local_only | approval_packet | `outcome-upwork-no-send-approval-request-packet-20260618` | 0.0 | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-no-send-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for one Upwork account/profile/proposal review. Do not log in, create or edit a profile, select a live job, send a proposal, message a client, a |
| upwork_ai_skills_fit_score_ready_local_only | local_offer_fit_score | `outcome-upwork-ai-skills-fit-score-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\upwork-ai-skills-fit-score-local-proof-validation.json | Create a no-send Upwork approval request packet for the recommended AI Integration Workflow Audit only after human review; keep account, profile, proposal, client data, credentials, payment, public action, worker/runtime |
| upwork_ai_offer_matrix_ready_local_only | local_offer_matrix | `outcome-upwork-ai-offer-matrix-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\upwork-ai-offer-matrix-local-proof-validation.json | Create a no-send Upwork approval request packet for the recommended first offer only after human review; keep account, proposal, payment, client data, credentials, public action, worker/runtime, model/MCP, and external s |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-offer-route-v1-20260617` | 0.0 | reports/agent-company-atlas-offer-route-trace-metadata-20260617.json | Browser-verify the Offer Route module across mobile, docked desktop, and stacked desktop layouts. |
| local_profile_proposal_draft_complete | local_proof_artifact | `outcome-upwork-profile-and-proposal-draft-20260616` | 0.0 | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-profile-and-proposal-draft-20260616.md | Create marketplace approval request packet before any Upwork account/profile/proposal action. |
| complete | local_service_proof_asset | `outcome-ai-workflow-audit-proof-asset-agency-reporting-20260616` | 0.0 | E:\agent-company-lab\reports\lead-generation-and-sales\ai-workflow-audit-proof-asset-agency-reporting-20260616.md | Create upwork-profile-and-proposal-draft-20260616.md only as a local draft. |
| complete | local_service_offer_packet | `outcome-upwork-ai-workflow-audit-offer-20260616` | 0.0 | E:\agent-company-lab\reports\lead-generation-and-sales\upwork-ai-workflow-audit-offer-20260616.md | Create ai-workflow-audit-proof-asset-agency-reporting-20260616.md/json using synthetic data only. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id lead_generation_and_sales
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id lead_generation_and_sales --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `lead_generation_and_sales` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

