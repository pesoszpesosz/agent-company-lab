# Manager Packet - paid_code_bounties

Generated UTC: 2026-06-21T12:53:22Z
Department: Cashflow Engineering
Lane status: active
Current owner: `lane-manager-paid_code_bounties-019ec612`

## Manager Directive

Own only the `paid_code_bounties` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Use imported rejected/parked rows as negative samples, then scout fresh explicit-payout issues with duplicate checks before any PR work.

## CEO Recommendation

Use imported rows as negative samples. Launch a fresh-source scout, not a PR worker, until a clean unclaimed bounty is found.

## Allowed Worker Types

- source_scout
- repo_triager
- patch_worker
- submission_packet_writer

## Example Work

- Algora
- Opire
- BountyHub
- Gibwork
- Gitpay
- GitHub explicit bounty issues

## Promotion Gates

- clear payout path
- low competition
- no active linked PR
- testable patch under 4 hours

## Required Service Workers

- github_identity_worker
- reputation_review_worker

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
- fork
- branch
- PR
- bounty comment

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `paid_code_profit_edge_scan_import` - Paid Code Scan Import | local_reports | lane_owner_on_demand | read_only_until_claim_rules_duplicate_checks_and_public_action_approval | Run only from paid_code_bounties lane owner after claim: E:\profit-edge-lab scanner scripts listed in README. | lane_evidence; paid_code_bounties manager packet |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| park_existing_submission_amount_false_positive_owner_hold | `pe-ledger-fuzoe-pd-hunter-18-org-list-expansion-4db3aa286661` - FuZoe/PD-Hunter #18 org-list expansion | https://github.com/FuZoe/PD-Hunter/issues/18 | Do not work #18 unless owner reopens to new contributors with clean payout terms. | Read-only ledger import for future lane managers. |
| imported | `pe-report-unitone-skill-bounty-scan-c0c428cbab57` - UnitOne Skill Bounty Scan | E:\profit-edge-lab\reports\unitone-skill-bounty-scan-latest.md | next: Build a local skill artifact, validate it, and package submission text; no public claim or PR without user approval. | Read-only evidence for future paid-code workers; this thread is not submitting PRs. |
| imported | `pe-report-projectdiscovery-bounty-scan-76f48603a8ed` - ProjectDiscovery Bounty Scan | E:\profit-edge-lab\reports\projectdiscovery-bounty-scan-latest.md |  | Read-only evidence for future paid-code workers; this thread is not submitting PRs. |
| local_parser_checker_complete | `evidence-algora-candidate-refresh-fixture-check-20260616` - Algora candidate refresh fixture check | E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-check-20260616.json | Use checker before any approved read-only live Algora refresh; do not claim/comment/PR/pay without separate public-action gate. | Executable local proof artifact produced by current platform thread; no external side effects. |
| local_parser_fixture_complete | `evidence-algora-candidate-refresh-fixture-20260616` - Algora candidate refresh parser fixture | E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-20260616.json | Implement parser checks against fixture before any approved live read-only refresh. | Local-only artifact produced by current platform thread; no external side effects. |
| local_algora_live_candidate_refresh_packet_complete | `algora-live-candidate-refresh-20260616` - Algora live-candidate refresh scanner packet | E:\agent-company-lab\reports\paid-code-bounties\algora-live-candidate-refresh-20260616.md | Implement algora-candidate-refresh-fixture-20260616.json with configured public URLs and no-network parser fixture. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_algora_explicit_payout_worksheet_complete | `algora-explicit-payout-worksheet-20260616` - Algora explicit-payout issue worksheet | E:\agent-company-lab\reports\paid-code-bounties\algora-explicit-payout-issue-worksheet-20260616.md | Create a local algora-live-candidate-refresh read-only packet or scanner. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_answers_complete | `paid-code-local-worksheet-answers-20260615` - Paid-code local worksheet answers | E:\agent-company-lab\reports\paid-code-local-worksheet-answers-latest.md | Paid-code lane manager should request a browser_read_only_session only if they want to refresh one candidate live; public claim, PR, payout, or security-sensitive steps remain separately gated. | Generated by platform_engineering from the paid-code duplicate-check worksheet; paid-code lane manager owns any gated refresh request. |
| local_worksheet_complete | `paid-code-duplicate-check-worksheet-20260615` - Paid-code duplicate-check worksheet | E:\agent-company-lab\reports\paid-code-duplicate-check-worksheet-latest.md | Paid-code lane manager should complete the six local-only worksheet items first; any live issue refresh, claim, PR, payout, or security-sensitive step must go through service requests. | Generated by platform_engineering from the completed first ranked paid-code proof; paid-code lane manager owns local worksheet completion. |
| local_proof_complete | `first-ranked-local-proof-paid_code_bounties-20260615` - First ranked local paid-code duplicate-check proof | E:\agent-company-lab\reports\first-ranked-manager-proof-latest.md | Have the paid-code lane manager use this proof to draft a local duplicate-check worksheet for the ranked bounty target; request browser or public claim work only through the parked service request gate. | Generated by platform_engineering from the ranked manager proof queue; paid-code lane manager owns follow-up. |
| park_lead_only_aggregator_noise | `pe-ledger-relayhop-sn-monetization-runtime-radar-sn-open-bou-1e3f46935568` - relayhop/sn-monetization-runtime [radar] SN open bounty cluster | https://github.com/relayhop/sn-monetization-runtime/issues/90 | Ignore relayhop/sn-monetization-runtime radar rows unless the upstream Stacker News bounty source is separately verified with clear payout and acceptance terms. | Read-only ledger import for future lane managers. |
| park_other_contributor_payment_attribution_gate | `pe-ledger-unitoneai-securityskills-2423-signed-build-manifes-362aaadf1098` - UnitOneAI/SecuritySkills #2423 signed-build-manifest-review | https://github.com/UnitOneAI/SecuritySkills/issues/2423 | Do not build #2423 unless a maintainer explicitly requests alternate implementations and attribution is clean for the user. | Read-only ledger import for future lane managers. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 92 | new | `task-continuity-owner-response-task-acknowledgement_response_required-task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-paid_code_bounties` - Handle continuity owner acknowledgement response for task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-paid_code_bounties | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-004-continuity-restore-response-v1-004-continuity-restore-v1-004-dispatch_stale_own | Existing owner `lane-manager-paid_code_bounties-019ec612` should handle the acknowledgement for `paid_code_bounties` locally and report evidence; no duplicate owner or worker should be created. |
| 90 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-paid_code_bounties` - Acknowledge customer follow-up triage for paid_code_bounties | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-requests-v1-20260621.md | Write one local acknowledgement artifact before starting workers or creating overlapping agents. |
| 76 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-paid_code_bounties` - Follow up customer input for paid_code_bounties | lane-manager-paid_code_bounties-019ec612 |  | intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.json | Create a local no-egress bounty scout packet or decide the existing paid-code lane already covers it. |
| 91 | complete | `task-algora-opik-readonly-refresh-service-request-20260618` - Create Algora Opik read-only refresh service request | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\requests\service-requests\req-algora-opik-readonly-refresh-20260618\validation.json | Leave this request in needs_review. Do not assign, start, approve, or execute it until a later exact signed decision permits a public read-only Opik/Algora refresh. |
| 88 | complete | `task-lane-scout-algora_comet_opik-20260618` - Lane scout local proof: algora comet opik | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\algora-comet-opik-claim-readiness-local-proof-validation.json | Park external Algora/Comet claim work until the Opik bounty program is verified active by an approved read-only refresh; then re-run duplicate/claim/payout checks before any public claim, comment, PR, account, CLA, or pa |
| 86 | complete | `task-paid_code_bounties-first-local-proof-20260615` - Prepare first local paid-code bounty duplicate-check proof packet | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\first-ranked-manager-proof-latest.md | Have the paid-code lane manager use this proof to draft a local duplicate-check worksheet for the ranked bounty target; request browser or public claim work only through the parked service request gate. |
| 85 | complete | `task-opire-saved-card-parser-checker-v1-20260618` - Create Opire saved-card parser checker | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\paid-code-bounties\opire-saved-card-parser-checker-v1-validation-20260618.json | Promote only candidate_needs_readonly_refresh rows into exact read-only refresh packets. Do not run /try, /claim, GitHub comments, PRs, account login, Stripe, payout, workers, model/API calls, or public actions. |
| 85 | complete | `task-paid-code-duplicate-check-worksheet-20260615` - Draft paid-code duplicate-check worksheet from first local proof | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\paid-code-duplicate-check-worksheet-latest.md | Paid-code lane manager should complete the six local-only worksheet items first; any live issue refresh, claim, PR, payout, or security-sensitive step must go through service requests. |
| 84 | complete | `task-paid-code-local-worksheet-answers-20260615` - Answer paid-code duplicate-check worksheet local items | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\paid-code-local-worksheet-answers-latest.md | Paid-code lane manager should request a browser_read_only_session only if they want to refresh one candidate live; public claim, PR, payout, or security-sensitive steps remain separately gated. |
| 82 | complete | `task-agent-company-atlas-claim-scout-texture-v1-20260617` - Add generated Claim Scout bounty-forge texture | recovered-profitable-edge-infra |  | Generated texture, texture wiring, upgraded Claim Scout styling, trace metadata, regenerated snapshot, and browser verification. | Regenerate the Atlas snapshot and browser-verify the Claim Scout game view. |
| 74 | complete | `task-lane-scout-opire_paid_oss-20260618` - Lane scout local proof: opire paid oss | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\opire-source-spec-parser-plan-local-proof-validation.json | Create a deterministic parser against saved/public Opire card snapshots extracting amount, owner, repo, title, language, command availability, solver count, URL/date fields, risk flags, and next local action; prove zero |
| 70 | complete | `task-algora-explicit-payout-worksheet-20260616` - Create Algora explicit-payout issue worksheet | lane-manager-paid_code_bounties-019ec612 |  | E:\agent-company-lab\reports\paid-code-bounties\algora-explicit-payout-issue-worksheet-20260616.md | Create a local algora-live-candidate-refresh read-only packet or scanner. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| needs_review | browser_read_only_session | browser_research | `req-algora-opik-readonly-refresh-20260618` |  | catalog_required_approval_no_external_action | Read public Comet/Opik, Algora, and GitHub status for Opik bounty reopening; no claim, PR, account, CLA, payout, or public action. | E:\agent-company-lab\requests\service-requests\req-algora-opik-readonly-refresh-20260618\packet.md |  |
| needs_review | browser_read_only_session | browser_research | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` |  | catalog_required_approval_no_external_action | Read public Algora/GitHub issue state for archestra-ai/archestra#3218; no GitHub public action. | E:\agent-company-lab\requests\service-requests\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614\packet.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| opire_saved_card_parser_checker_complete_local_only | saved_card_parser_checker | `outcome-opire-saved-card-parser-checker-v1-20260618` | 0.0 | E:\agent-company-lab\reports\paid-code-bounties\opire-saved-card-parser-checker-v1-validation-20260618.json | Promote only candidate_needs_readonly_refresh rows into exact read-only refresh packets. Do not run /try, /claim, GitHub comments, PRs, account login, Stripe, payout, workers, model/API calls, or public actions. |
| algora_opik_readonly_refresh_request_ready_needs_review | service_request_packet | `outcome-algora-opik-readonly-refresh-service-request-20260618` | 0.0 | E:\agent-company-lab\requests\service-requests\req-algora-opik-readonly-refresh-20260618\validation.json | Leave this request in needs_review. Do not assign, start, approve, or execute it until a later exact signed decision permits a public read-only Opik/Algora refresh. |
| opire_source_spec_parser_plan_ready_local_only | local_proof | `outcome-opire-source-spec-parser-plan-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\opire-source-spec-parser-plan-local-proof-validation.json | Create a deterministic parser against saved/public Opire card snapshots extracting amount, owner, repo, title, language, command availability, solver count, URL/date fields, risk flags, and next local action; prove zero |
| algora_comet_opik_claim_readiness_ready_but_parked_program_paused | local_claim_readiness | `outcome-algora-comet-opik-claim-readiness-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\algora-comet-opik-claim-readiness-local-proof-validation.json | Park external Algora/Comet claim work until the Opik bounty program is verified active by an approved read-only refresh; then re-run duplicate/claim/payout checks before any public claim, comment, PR, account, CLA, or pa |
| complete | atlas_lane_texture_visual_upgrade | `outcome-agent-company-atlas-claim-scout-texture-v1-20260617` | 0.0 | reports/agent-company-atlas-claim-scout-texture-trace-metadata-20260617.json | Browser-verify Claim Scout on mobile and desktop; all current lane-specific minigames now have generated textures. |
| local_parser_checker_complete | executable_local_proof | `outcome-algora-candidate-refresh-fixture-check-20260616` | 0.0 | E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-check-20260616.json | Use checker before any approved read-only live Algora refresh; do not claim/comment/PR/pay without separate public-action gate. |
| local_parser_fixture_complete | local_proof_artifact | `outcome-algora-candidate-refresh-fixture-20260616` | 0.0 | E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-20260616.json | Implement parser checks against fixture before any approved live read-only refresh. |
| complete | local_paid_code_scanner_packet | `outcome-algora-live-candidate-refresh-20260616` | 0.0 | E:\agent-company-lab\reports\paid-code-bounties\algora-live-candidate-refresh-20260616.md | Implement algora-candidate-refresh-fixture-20260616.json with configured public URLs and no-network parser fixture. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id paid_code_bounties
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id paid_code_bounties --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `paid_code_bounties` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

