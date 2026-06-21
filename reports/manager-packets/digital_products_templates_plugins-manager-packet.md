# Manager Packet - digital_products_templates_plugins

Generated UTC: 2026-06-21T14:37:35Z
Department: Product Studio
Lane status: active
Current owner: `lane-manager-digital_products_templates_plugins-019ec69a`

## Manager Directive

Own only the `digital_products_templates_plugins` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Use the starter browser-read-only service request to shortlist sellable template/plugin/product ideas with buyer problem, build artifact, marketplace fees, and payment/listing gates.

## CEO Recommendation

Resolve service requests before assigning more workers.

## Allowed Worker Types

- market_gap_scout
- template_builder
- plugin_packager
- listing_packet_writer

## Example Work

- Gumroad
- Lemon Squeezy
- PromptBase
- Notion Marketplace
- Shopify app/plugin marketplaces

## Promotion Gates

- buyer problem explicit
- asset can be built locally
- marketplace fees and terms clear
- listing and payment gates approved

## Required Service Workers

- account_registration_worker
- legal_terms_worker
- payment_review_worker
- public_action_worker

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
- marketplace account
- product listing
- payment setup
- public promotion

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `digital_products_marketplace_demand_source_seed` - Digital Product Marketplace Demand Source Seed | public_marketplace_research | lane_owner_on_demand_or_weekly | read_only_market_research_no_listing_account_payment_or_public_submission | Prepare a read-only demand and fee scan only after lane manager claim; no listing, account, checkout, or payment action. | E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-demand-refresh-YYYYMMDD.md; lane_evidence; legal_kyc_tax_payment_gate_candidates |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| local_gated_hold_register_complete | `digital-products-local-gated-hold-register-20260616` - Digital products local gated hold register | E:\agent-company-lab\reports\digital-products-local-gated-hold-register-latest.md | Keep all four holds active until explicit user approval is given for a specific gate; after approval, resume only the matching bounded task packet. | Generated by platform_engineering from the post-approval simulation plan; all holds remain active until explicit user approval. |
| local_post_approval_simulation_plan_complete | `digital-products-local-post-approval-simulation-plan-20260616` - Digital products local post-approval simulation plan | E:\agent-company-lab\reports\digital-products-local-post-approval-simulation-plan-latest.md | Keep the digital-products lane on hold until explicit user approval is given for a listed decision item; after approval, run only the matching bounded scenario. | Generated by platform_engineering from the operator approval brief; no scenario may execute without explicit user approval. |
| local_operator_approval_brief_complete | `digital-products-local-operator-approval-brief-20260616` - Digital products local operator approval brief | E:\agent-company-lab\reports\digital-products-local-operator-approval-brief-latest.md | User/operator must explicitly approve one or both decision items before any browser validation or legal/payment review; otherwise hold the lane locally. | Generated by platform_engineering from approval-request drafts; user/operator owns any explicit approval decision. |
| local_approval_request_drafts_complete | `digital-products-local-approval-request-drafts-20260616` - Digital products local approval request drafts | E:\agent-company-lab\reports\digital-products-local-approval-request-drafts-latest.md | Review these local drafts and decide whether to explicitly request browser or legal/payment approval; do not browse, submit, accept terms, create accounts, or configure payouts. | Generated by platform_engineering from post-polish readiness; digital-products lane manager owns any explicit future approval request. |
| local_post_polish_readiness_complete | `digital-products-local-post-polish-readiness-20260616` - Digital products local post-polish readiness | E:\agent-company-lab\reports\digital-products-local-post-polish-readiness-latest.md | Draft separate local approval-request packets for read-only browser validation and legal/payment review; do not submit, browse, accept terms, create accounts, or configure payouts. | Generated by platform_engineering from the local copy-polish pass; digital-products lane manager owns future approval-request packet drafts. |
| local_copy_polish_complete | `digital-products-local-copy-polish-20260616` - Digital products local copy polish | E:\agent-company-lab\reports\digital-products-local-copy-polish-latest.md | Run a local post-polish readiness check and decide whether to continue locally or draft separate future approval-request packets; do not exercise any gate. | Generated by platform_engineering from the local gate choice; digital-products lane manager owns local readiness follow-up. |
| local_gate_choice_complete | `digital-products-local-gate-choice-20260616` - Digital products local gate choice | E:\agent-company-lab\reports\digital-products-local-gate-choice-latest.md | Run a local copy-polish pass on the revised package and optionally draft separate future approval-request packets without exercising any gate. | Generated by platform_engineering from the local gate-decision packet; digital-products lane manager owns local follow-up. |
| local_gate_decision_packet_complete | `digital-products-local-gate-decision-packet-20260616` - Digital products local gate-decision packet | E:\agent-company-lab\reports\digital-products-local-gate-decision-packet-latest.md | Choose whether to continue local refinement, request read-only browser approval, request legal/payment review, or pause; no gate is requested or exercised by this packet. | Generated by platform_engineering from revised local completeness; digital-products lane manager owns any explicit future gate request. |
| local_revised_completeness_complete | `digital-products-local-revised-completeness-20260616` - Digital products local revised completeness check | E:\agent-company-lab\reports\digital-products-local-revised-completeness-latest.md | Prepare a local gate-decision packet that compares continue-local, request read-only browser approval, request legal/payment review, or pause; do not perform any external validation. | Generated by platform_engineering from the local revision pass; digital-products lane manager owns the next gate-decision packet. |
| local_revision_pass_complete | `digital-products-local-revision-pass-20260616` - Digital products local revision pass | E:\agent-company-lab\reports\digital-products-local-revision-pass-latest.md | Run a local revised-package completeness check against these six files; do not browse, publish, list, price, create accounts, configure payouts, or request external validation. | Generated by platform_engineering from the private-review decision; digital-products lane manager owns the local completeness follow-up. |
| local_private_review_decision_complete | `digital-products-local-private-review-decision-20260616` - Digital products local private review decision | E:\agent-company-lab\reports\digital-products-local-private-review-decision-latest.md | Draft the local revision pass from the six-item queue, then rerun local package completeness; do not browse, publish, list, price, create accounts, or configure payouts. | Generated by platform_engineering from local private-review packet; digital-products lane manager owns local revision follow-up. |
| local_private_review_packet_complete | `digital-products-local-private-review-packet-20260616` - Digital products local private review packet | E:\agent-company-lab\reports\digital-products-local-private-review-packet-latest.md | Have the digital-products lane manager review the packet locally and choose continue-local, request browser gate, request legal/payment gate, or pause-candidate. | Generated by platform_engineering from local completeness check; digital-products lane manager owns local decision follow-up. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 72 | new | `task-continuity-lane-next-task-20260621-digital_products_templates_plugins-007` - Continue proof-derived local next step for digital_products_templates_plugins | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\digital_products_templates_plugins\proof-derived-continuation-v1-20260621-006.md | Read the evidence artifact for this task, extract exactly one concrete next local step or explicit park/revisit condition from it, and write a compact continuation packet with evidence, gate status, owner, expected next |
| 92 | complete | `task-fiverr-no-publish-approval-request-packet-20260618` - Create no-publish Fiverr approval request packet | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\digital-products\fiverr-no-publish-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for one Fiverr account/gig copy review. Do not log in, create or edit a seller profile, create/edit/publish a gig, message buyers, accept orders |
| 92 | complete | `task-promptbase-guideline-readonly-service-request-20260618` - Create PromptBase read-only guideline review service request | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\requests\service-requests\req-promptbase-guideline-readonly-review-20260618\validation.json | Leave the request in needs_review. Do not assign, start, approve, or execute it until a later exact signed decision permits a read-only PromptBase browser session. |
| 89 | complete | `task-lane-scout-promptbase_agent_skill_route-20260618` - Lane scout local proof: promptbase agent skill route | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\promptbase-approval-rubric-local-proof-validation.json | If the operator wants to proceed, review only the read-only guideline approval first and convert it into one exact-scope service request; keep account, payment, package build, listing, upload, submission, worker/runtime, |
| 88 | complete | `task-gumroad-no-publish-approval-request-packet-20260618` - Create no-publish Gumroad approval request packet | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\digital-products\gumroad-no-publish-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for Gumroad account/listing copy and package-manifest review. Do not log in, create/edit a seller profile, accept terms, create/upload/edit a pr |
| 86 | complete | `task-continuity-owner-response-task-lane_goal_response_required-digital_products_templates_plugins` - Submit continuity lane goal response for digital_products_templates_plugins | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-002-continuity-restore-response-v1-002-continuity-restore-v1-002-request_lane_goal- | Owner `lane-manager-digital_products_templates_plugins-019ec69a` should submit the lane goal artifact for `digital_products_templates_plugins`. |
| 86 | complete | `task-lane-scout-fiverr_ai_services-20260618` - Lane scout local proof: fiverr ai services | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\fiverr-ai-service-bundles-local-proof-validation.json | Create a no-publish Fiverr approval request packet for the recommended first bundle only after human review; keep Fiverr account, gig/listing, seller terms, payout, client data, credentials, public action, worker/runtime |
| 86 | complete | `task-digital-products-marketplace-route-eligibility-wave24-20260618` - Prepare digital-products marketplace route eligibility wave 24 | recovered-profitable-edge-infra |  | Route eligibility dataset, report, validation mirror, and trace metadata. | Prepare PromptBase-specific local listing and eligibility checklist from existing package files only; keep browser validation, seller terms, account setup, payout setup, zip/public upload, listing, and submission behind |
| 86 | complete | `task-digital_products_templates_plugins-first-local-proof-20260615` - Prepare first local marketplace demand proof packet | lane-manager-digital_products_templates_plugins-019ec69a |  | E:\agent-company-lab\reports\digital-products-local-demand-proof-latest.md | Digital-products lane manager should draft a local demand memo and only request marketplace/browser or legal/payment gates if they want live demand validation. |
| 85 | complete | `task-digital-products-promptbase-do-not-run-submission-packet-wave27-20260618` - Prepare PromptBase do-not-run submission approval packet wave 27 | recovered-profitable-edge-infra |  | E:\agent-company-lab\reports\digital-products-promptbase-do-not-run-submission-packet-wave27-20260618-validation.json | Ask the operator to review the six exact approval packets; if approved later, create one narrow service request at a time, beginning with read-only PromptBase guideline review. Keep browser, account, legal/payment, zip, |
| 85 | complete | `task-digital-products-promptbase-route-readiness-wave25-20260618` - Prepare digital-products PromptBase route readiness wave 25 | recovered-profitable-edge-infra |  | PromptBase route readiness dataset, report, validation mirror, and trace metadata. | Create a local PromptBase use-case and reproducibility checklist from existing package files only; do not write final listing copy, browse marketplace pages in a lab browser, create accounts, accept terms, configure payo |
| 84 | complete | `task-digital-products-promptbase-use-case-repro-checklist-wave26-20260618` - Prepare digital-products PromptBase use-case reproducibility checklist wave 26 | recovered-profitable-edge-infra |  | Local use-case/reproducibility dataset, report, validation mirror, and trace metadata. | Create a do-not-run PromptBase submission packet that lists exact later approvals and command-free review steps; keep final listing copy, browser validation, seller terms, account setup, payout setup, zip/public upload, |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| needs_review | browser_read_only_session | browser_research | `req-promptbase-guideline-readonly-review-20260618` |  | catalog_required_approval_no_external_action | Review public PromptBase guideline/seller pages for Agent Skill Starter Kit v0; no browser side effects. | E:\agent-company-lab\requests\service-requests\req-promptbase-guideline-readonly-review-20260618\packet.md |  |
| needs_review | legal_kyc_tax_payment_gate | legal_kyc_tax_payment | `req-next-wave-digital-legal-payment-review-20260614` |  | legal_kyc_tax_payment_requires_user_decision_no_commitment | Review legal/KYC/tax/payment/payout/account-contract gates for Agent Skill Starter Kit marketplace route; no commitments. | E:\agent-company-lab\requests\service-requests\req-next-wave-digital-legal-payment-review-20260614\packet.md |  |
| needs_review | browser_read_only_session | browser_research | `req-next-wave-digital-marketplace-browser-readonly-20260614` |  | catalog_required_approval_no_external_action | Read public digital marketplace terms/fees/listing requirements for Agent Skill Starter Kit route; no browser side effects. | E:\agent-company-lab\requests\service-requests\req-next-wave-digital-marketplace-browser-readonly-20260614\packet.md |  |
| needs_review | browser_read_only_session | browser_research | `req-wave4-digital-products-browser-readonly-20260614` |  | catalog_required_approval_no_external_action | Read public digital-product marketplace pages and capture product opportunity signals; no browser side effects. | E:\agent-company-lab\requests\service-requests\req-wave4-digital-products-browser-readonly-20260614\packet.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| parked_loop_next_artifact_known_local_only | proof_derived_continuation | `outcome-digital-products-proof-derived-continuation-v1-20260621-006` | 0.0 | E:\agent-company-lab\reports\digital_products_templates_plugins\proof-derived-continuation-v1-20260621-006.md | Assign or explicitly request E:\agent-company-lab\reports\digital_products_templates_plugins\gumroad-direct-download-human-decision-intake-v1-20260621.md; keep proof-derived continuation loop parked until then. |
| lemon_squeezy_no_publish_launch_approval_packet_ready_local_only | launch_approval_packet | `outcome-lemon-squeezy-no-publish-launch-approval-packet-v1-20260618` | 0.0 | E:\agent-company-lab\reports\digital-products\lemon-squeezy-no-publish-launch-approval-packet-v1-validation-20260618.json | If the operator approves, create exact local listing copy, refund/support text, screenshot checklist, and deterministic zip manifest files. Do not log in, accept terms, create a storefront/product, upload files, create c |
| gumroad_no_publish_approval_packet_ready_local_only | approval_packet | `outcome-gumroad-no-publish-approval-request-packet-20260618` | 0.0 | E:\agent-company-lab\reports\digital-products\gumroad-no-publish-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for Gumroad account/listing copy and package-manifest review. Do not log in, create/edit a seller profile, accept terms, create/upload/edit a pr |
| fiverr_no_publish_approval_packet_ready_local_only | approval_packet | `outcome-fiverr-no-publish-approval-request-packet-20260618` | 0.0 | E:\agent-company-lab\reports\digital-products\fiverr-no-publish-approval-request-packet-validation-20260618.json | If the operator approves this packet, create an exact-scope service request for one Fiverr account/gig copy review. Do not log in, create or edit a seller profile, create/edit/publish a gig, message buyers, accept orders |
| promptbase_guideline_readonly_request_ready_needs_review | service_request_packet | `outcome-promptbase-guideline-readonly-service-request-20260618` | 0.0 | E:\agent-company-lab\requests\service-requests\req-promptbase-guideline-readonly-review-20260618\validation.json | Leave the request in needs_review. Do not assign, start, approve, or execute it until a later exact signed decision permits a read-only PromptBase browser session. |
| lemon_squeezy_route_decision_ready_local_only | local_proof | `outcome-lemon-squeezy-route-decision-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\lemon-squeezy-route-decision-local-proof-validation.json | Create a Lemon Squeezy launch approval packet for Agent Skill Starter Kit v0 or a narrower AI workflow audit template pack, including product IP/license review, refund/support terms, forbidden claims, pricing margin scen |
| gumroad_direct_download_packet_ready_local_only | local_direct_download_packet | `outcome-gumroad-direct-download-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\gumroad-direct-download-local-proof-validation.json | Create a no-publish Gumroad approval request packet for Agent Skill Starter Kit v0; include seller terms/prohibited-products review, IP/license review, price/refund/copy review, zip checksum plan, payout/tax/payment gate |
| fiverr_ai_service_bundles_ready_local_only | local_service_bundles | `outcome-fiverr-ai-service-bundles-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\fiverr-ai-service-bundles-local-proof-validation.json | Create a no-publish Fiverr approval request packet for the recommended first bundle only after human review; keep Fiverr account, gig/listing, seller terms, payout, client data, credentials, public action, worker/runtime |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id digital_products_templates_plugins
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id digital_products_templates_plugins --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `digital_products_templates_plugins` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

