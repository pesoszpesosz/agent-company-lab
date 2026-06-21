# Manager Packet - security_bounty_private_reports

Generated UTC: 2026-06-21T14:07:11Z
Department: Security Research
Lane status: active
Current owner: `lane-manager-security_bounty_private_reports-019ec612`

## Manager Directive

Own only the `security_bounty_private_reports` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Rank imported private-report and static-review sources by program scope, evidence quality, payout path, and disclosure route.

## CEO Recommendation

Launch a security manager to rank private-report drafts, rules gates, and proof gaps. No submissions without approval.

## Allowed Worker Types

- program_rules_reader
- static_reviewer
- proof_builder
- report_writer

## Example Work

- Google OSS VRP style review
- IssueHunt security programs
- HackerOne/Bugcrowd public programs
- Web3 bounty programs

## Promotion Gates

- program scope verified
- allowed testing only
- minimal reproducible proof
- private report route clear

## Required Service Workers

- scope_approval_worker
- report_submission_worker

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
- security advisory
- private report submission

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `security_profit_edge_scan_import` - Security Bounty and Private Report Import | local_reports | lane_owner_on_demand | read_only_static_review_until_program_scope_user_approval_and_private_route_clear | Run only from security_bounty_private_reports lane owner after claim and scope rules review. | lane_evidence; security manager packet |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| draft_hypothesis_not_submission_ready | `pe-ledger-google-certificate-transparency-go-get-entries-ove-7f64f49eed42` - google/certificate-transparency-go get-entries overcount validation gap | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Build a clean local regression patch for GetRawEntries range-count validation plus scanner-level no-skip test; do not submit Bug Hunters report or upstream PR without explicit approval. | Read-only ledger import for future lane managers. |
| draft_hypothesis_not_submission_ready | `pe-ledger-bazelbuild-buildtools-buildozer-label-traversal-wo-e0e7682d2503` - bazelbuild/buildtools buildozer label traversal workspace escape | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Build a local patch candidate rejecting package path traversal in InterpretLabelForWorkspaceLocation/targetExpressionToBuildFiles and search for first-party automation that processes untrusted buildozer labels. | Read-only ledger import for future lane managers. |
| draft_hypothesis_not_submission_ready | `pe-ledger-bazelbuild_rules_android_aar_resource_zip_slip_sta-b2eae39b165b` - bazelbuild_rules_android_aar_resource_zip_slip_static_review_20260613_1620 | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Build a real-rule Windows Bazel reproduction, verify sandbox/execroot containment, and prepare a patch rejecting absolute or dot-dot escaping AAR entries before any external submission. | Read-only ledger import for future lane managers. |
| submission_rules_gate_not_cleared | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-28880407640f` - bazelbuild/rules_android Windows AAR resource path traversal | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Before submission, user must approve rendered rules review / Bug Hunters account route and current scope validation. | Read-only ledger import for future lane managers. |
| partial_verified_patch_candidate_unsubmitted | `pe-ledger-bazelbuild-rules_android-aar-resource-zip-slip-win-de60afb752e0` - bazelbuild/rules_android AAR resource zip-slip Windows extraction | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Complete helper hardening for absolute, drive-qualified, backslash, empty, dot, and dot-dot segments; rerun tests/proof; no external submission without explicit approval. | Read-only ledger import for future lane managers. |
| verified_patch_candidate_unsubmitted | `pe-ledger-google-certificate-transparency-go-get-entries-res-29e093c10c2a` - google/certificate-transparency-go get-entries response cardinality validation | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Choose private Google OSS VRP report vs public upstream PR/hardening issue, or continue to a stronger bounty lane. Do not submit externally without explicit user approval. | Read-only ledger import for future lane managers. |
| verified_patch_candidate_unsubmitted | `pe-ledger-bazelbuild-buildtools-buildozer-label-traversal-wo-0426669d4438` - bazelbuild/buildtools buildozer label traversal workspace escape | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Choose private Google OSS VRP report vs public upstream hardening PR/issue, or continue to a stronger lane. No external submission without explicit user approval. | Read-only ledger import for future lane managers. |
| verified_patch_candidate_unsubmitted | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-60f499367ecf` - bazelbuild/rules_android Windows AAR resource path traversal | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Build a minimal real-rule Bazel repro for crafted AAR traversal on Windows, then choose private Google OSS VRP report vs public hardening PR. No external submission was taken. | Read-only ledger import for future lane managers. |
| fresh_lane_recorded_not_promoted | `pe-ledger-golang_crypto_static_review_scout_20260613_1548-77ce36c4f6ee` - golang_crypto_static_review_scout_20260613_1548 | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Build a local oversized-agent-frame probe and search first-party untrusted ServeAgent exposure paths; no external submission. | Read-only ledger import for future lane managers. |
| imported | `pe-report-security-bounty-source-scan-032255bc416b` - Security Bounty Source Scan | E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md | next: If switching to the security lane, read rules, clone scope, and spend one focused review block on invariants before any submission. | Read-only source evidence for future security department workers. |
| imported | `pe-report-google-oss-static-review-shortlist-dbeac8a17965` - Google OSS Static Review Shortlist | E:\profit-edge-lab\reports\google-oss-static-review-shortlist-latest.md | next: Clone read-only and review supply-chain, parser, auth, credential, build, and release-boundary logic; no live testing. | Read-only source evidence for future security department workers. |
| imported | `pe-report-issuehunt-security-program-scan-eaea569f83ac` - IssueHunt Security Program Scan | E:\profit-edge-lab\reports\issuehunt-security-program-scan-latest.md | next: Read the full program page and all scope text; draft non-invasive hypotheses only, then ask user before account setup or testing. | Read-only source evidence for future security department workers. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 72 | new | `task-continuity-lane-next-task-20260621-security_bounty_private_reports-005` - Continue proof-derived local next step for security_bounty_private_reports | lane-manager-security_bounty_private_reports-019ec612 |  | E:\agent-company-lab\reports\security_bounty_private_reports\proof-derived-continuation-v1-20260621-004.md | Read the evidence artifact for this task, extract exactly one concrete next local step or explicit park/revisit condition from it, and write a compact continuation packet with evidence, gate status, owner, expected next |
| 89 | complete | `task-security-program-rules-scope-ranker-v1-20260618` - Build security program rules and scope ranker v1 | recovered-profitable-edge-infra |  | E:\agent-company-lab\reports\security-program-rules-scope-ranker-v1-validation-20260618.json | Build Immunefi directory scope shortlist and security report quality gate before any target-specific testing or report drafting. |
| 88 | complete | `task-immunefi-directory-scope-shortlist-v1-20260618` - Build Immunefi directory scope shortlist v1 | recovered-profitable-edge-infra |  | Ranked Immunefi directory scope shortlist with source URLs, local next-proof actions, and zero-side-effect validation. | Build optimism_scope_rules_extraction_packet_v1 and security_report_quality_gate_v1 before any target-specific testing or report drafting. |
| 87 | complete | `task-optimism-scope-rules-extraction-packet-v1-20260618` - Build Optimism scope rules extraction packet v1 | recovered-profitable-edge-infra |  | Optimism Immunefi rules/scope extraction packet with asset examples, impact matrix, out-of-scope controls, service gates, and zero-side-effect validation. | Build optimism_asset_scope_table_v1 and security_report_quality_gate_v1; keep runtime/testing/submission blocked. |
| 86 | complete | `task-continuity-owner-response-task-lane_goal_response_required-security_bounty_private_reports` - Submit continuity lane goal response for security_bounty_private_reports | lane-manager-security_bounty_private_reports-019ec612 |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-006-continuity-restore-response-v1-006-continuity-restore-v1-006-request_lane_goal- | Owner `lane-manager-security_bounty_private_reports-019ec612` should submit the lane goal artifact for `security_bounty_private_reports`. |
| 86 | complete | `task-optimism-asset-scope-table-v1-20260618` - Build Optimism asset scope table v1 | recovered-profitable-edge-infra |  | Full observed Optimism Immunefi asset table with 33 rows, category counts, duplicate-risk notes, and zero external side effects. | Build optimism_known_issue_duplicate_matrix_v1 and security_report_quality_gate_v1 before any target-specific code review. |
| 85 | complete | `task-optimism-known-issue-duplicate-matrix-v1-20260618` - Build Optimism known-issue duplicate matrix v1 | recovered-profitable-edge-infra |  | Optimism known-issue and duplicate-control matrix with 21 controls, hard stops, source routes, and zero-side-effect validation. | Build security_report_quality_gate_v1 before target-specific code review. |
| 84 | complete | `task-security-report-quality-gate-v1-20260618` - Build security report quality gate v1 | recovered-profitable-edge-infra |  | Report-only security report quality gate with scope, duplicate, PoC, impact, severity, publication, approval, and side-effect controls. | Build optimism_local_review_candidate_filter_v1 before target-specific code review. |
| 84 | complete | `task-agent-company-atlas-scope-run-v1-20260617` - Add custom Scope Run Atlas minigame | recovered-profitable-edge-infra |  | Generated scope run texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Return to local_service_worker_request_state_machine_runner_v1_without_worker_start as the next executable-control-plane preview. |
| 83 | complete | `task-optimism-local-review-candidate-filter-v1-20260618` - Build Optimism local review candidate filter v1 | recovered-profitable-edge-infra |  | Report-only Optimism candidate filter routing local review, hard stops, upstream checks, duplicate controls, and quality-gate requirements. | Create exactly one optimism_single_asset_candidate_packet_v1 from olf-001 or olf-009 before target-specific review. |
| 82 | complete | `task-hackerone-no-login-public-program-fixture-scorer-v1-20260618` - Create HackerOne no-login public program fixture scorer | lane-manager-security_bounty_private_reports-019ec612 |  | E:\agent-company-lab\reports\security-bounty-private-reports\hackerone-no-login-public-program-fixture-scorer-v1-validation-20260618.json | For static_candidate_draft rows, prepare only a local public-source review checklist and report skeleton. Do not create or use a HackerOne account, open a browser session, follow/bookmark/contact programs, test targets, |
| 82 | complete | `task-optimism-single-asset-candidate-packet-v1-20260618` - Build Optimism single-asset candidate packet v1 | recovered-profitable-edge-infra |  | Report-only single-asset OptimismPortal candidate packet with source snapshot, invariant plan, duplicate controls, quality gate notes, and zero side effects. | Write optimism_portal_invariant_memo_v1 for exactly one invariant group before any proof execution. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| needs_review | browser_read_only_session | browser_research | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` |  | catalog_required_approval_no_external_action | Read public Google OSS VRP rendered rules/scope/submission route for rules_android; no account or submission action. | E:\agent-company-lab\requests\service-requests\req-next-wave-security-google-oss-vrp-browser-readonly-20260614\packet.md |  |
| needs_review | security_report_submission_gate | security_report_submission | `req-next-wave-security-report-route-review-20260614` |  | security_report_submission_requires_user_and_cro_approval_no_submission | Review security report submission route readiness for rules_android packet; no report submission. | E:\agent-company-lab\requests\service-requests\req-next-wave-security-report-route-review-20260614\packet.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| bugcrowd_no_login_public_program_fixture_scorer_ready_local_only | no_login_public_program_fixture_scorer | `outcome-bugcrowd-no-login-public-program-fixture-scorer-v1-20260618` | 0.0 | E:\agent-company-lab\reports\security-bounty-private-reports\bugcrowd-no-login-public-program-fixture-scorer-v1-validation-20260618.json | For static_candidate_draft rows, prepare only a local VRT/source-review checklist and private report skeleton. Do not create or use a Bugcrowd account, open a browser session, follow/join/contact programs, test targets, |
| hackerone_no_login_public_program_fixture_scorer_ready_local_only | no_login_public_program_fixture_scorer | `outcome-hackerone-no-login-public-program-fixture-scorer-v1-20260618` | 0.0 | E:\agent-company-lab\reports\security-bounty-private-reports\hackerone-no-login-public-program-fixture-scorer-v1-validation-20260618.json | For static_candidate_draft rows, prepare only a local public-source review checklist and report skeleton. Do not create or use a HackerOne account, open a browser session, follow/bookmark/contact programs, test targets, |
| bugcrowd_rules_first_triage_ready_local_only | local_proof | `outcome-bugcrowd-rules-first-triage-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\bugcrowd-rules-first-triage-local-proof-validation.json | Create a no-login Bugcrowd public-program fixture from manually saved program-list and bounty-brief snippets; run the first-triage scorer; emit only local/static candidate drafts with VRT, scope, safe harbor, reward, and |
| hackerone_rules_route_readiness_ready_local_only | local_proof | `outcome-hackerone-rules-route-readiness-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\hackerone-rules-route-readiness-local-proof-validation.json | Create a no-login HackerOne public program fixture from manually saved program directory, Opportunity Discovery, and program-policy snippets; run the scorer; emit only static/public-code-review candidate drafts. Keep acc |
| complete_report_only_fixture_plan_no_patch_no_testing_no_submission | optimism_portal_l2sender_fixture_plan | `outcome-optimism-portal-l2sender-fixture-plan-v1-20260618` | 0.0 | E:\agent-company-lab\reports\optimism-portal-l2sender-fixture-plan-v1-20260618-validation.json | Only after explicit approval, materialize local patch file and run local upstream tests; do not submit or test live targets. |
| complete_report_only_no_finding_no_testing_no_submission | optimism_portal_invariant_memo | `outcome-optimism-portal-invariant-memo-v1-20260618` | 0.0 | E:\agent-company-lab\reports\optimism-portal-invariant-memo-v1-validation-20260618.json | Create local fixture design or patch plan for l2Sender postcondition assertions; do not claim a vulnerability without a failing local proof. |
| complete_report_only_single_asset_packet_no_testing_no_submission | optimism_single_asset_candidate_packet | `outcome-optimism-single-asset-candidate-packet-v1-20260618` | 0.0 | E:\agent-company-lab\reports\optimism-single-asset-candidate-packet-v1-validation-20260618.json | Write optimism_portal_invariant_memo_v1 for opi-007 or opi-008; no fork execution, live target testing, browser work, or submission. |
| complete_report_only_candidate_filter_no_testing_no_submission | optimism_local_review_candidate_filter | `outcome-optimism-local-review-candidate-filter-v1-20260618` | 0.0 | E:\agent-company-lab\reports\optimism-local-review-candidate-filter-v1-validation-20260618.json | Create exactly one optimism_single_asset_candidate_packet_v1; no code execution, fork testing, browser work, target testing, or submission before gates. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id security_bounty_private_reports
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id security_bounty_private_reports --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `security_bounty_private_reports` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

