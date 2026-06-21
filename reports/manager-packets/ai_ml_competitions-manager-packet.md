# Manager Packet - ai_ml_competitions

Generated UTC: 2026-06-21T14:30:21Z
Department: Competition Lab
Lane status: active
Current owner: `lane-manager-ai_ml_competitions-019ec69a`

## Manager Directive

Own only the `ai_ml_competitions` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Use the starter browser-read-only service request to shortlist AI/ML competitions with prize route, deadline, dataset gate, baseline feasibility, and submission/account blockers.

## CEO Recommendation

Resolve service requests before assigning more workers.

## Allowed Worker Types

- competition_scout
- dataset_reader
- baseline_builder
- submission_packet_writer

## Example Work

- Kaggle
- DrivenData
- ML Contests
- lablab.ai
- ETHGlobal AI tracks

## Promotion Gates

- rules and prize route clear
- dataset access legal
- deadline feasible
- baseline can be built locally
- submission/account gates approved

## Required Service Workers

- account_registration_worker
- data_access_worker
- legal_terms_worker
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
- account registration
- dataset download
- competition submission

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `ai_ml_competitions_public_prize_source_seed` - AI/ML Competition Public Prize Source Seed | public_competition_registry | lane_owner_on_demand_or_weekly | read_only_public_research_no_account_submission_dataset_download_or_terms_acceptance | Prepare a read-only public listing scan only after lane manager claim; save results to a dated local shortlist artifact. | E:\agent-company-lab\reports\ai-ml-competitions\public-prize-source-refresh-YYYYMMDD.md; lane_evidence; service_request_candidates |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| watchlist_fit_gate_complete | `evidence-gemini-xprize-agent-company-fit-gate-20260616` - Gemini XPRIZE Agent Company fit gate | E:\agent-company-lab\reports\ai-ml-competitions\gemini-xprize-agent-company-fit-gate-20260616.md | Create local business model canvas only if user explicitly promotes contest venture sprint. | Local-only artifact produced by current platform thread; no external side effects. |
| local_toy_harness_runner_complete | `evidence-arc-toy-harness-run-20260616` - ARC toy harness run | E:\agent-company-lab\reports\ai-ml-competitions\arc-toy-harness-run-20260616.json | Extend synthetic family coverage or keep ARC lane parked until competition rules/data gates are approved. | Executable local proof artifact produced by current platform thread; no external side effects. |
| local_toy_fixture_complete | `evidence-arc-toy-harness-fixture-20260616` - ARC toy harness synthetic fixture | E:\agent-company-lab\reports\ai-ml-competitions\arc-toy-harness-fixture-20260616.json | Write standard-library local harness only if AI/ML lane keeps ARC prototype prioritized. | Local-only artifact produced by current platform thread; no external side effects. |
| local_arc_toy_harness_plan_complete | `arc-local-toy-harness-plan-20260616` - ARC local toy harness plan | E:\agent-company-lab\reports\ai-ml-competitions\arc-local-toy-harness-plan-20260616.md | Create arc-toy-harness-fixture-20260616.json and local-only harness draft. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_devpost_gemini_xprize_rules_packet_complete | `devpost-gemini-xprize-rules-packet-20260616` - Devpost Build with Gemini XPRIZE rules packet | E:\agent-company-lab\reports\ai-ml-competitions\devpost-rules-packet-build-with-gemini-xprize-20260616.md | Create gemini-xprize-agent-company-fit-gate-20260616.md. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_arc_prize_feasibility_memo_complete | `arc-prize-feasibility-memo-20260616` - ARC Prize 2026 feasibility memo | E:\agent-company-lab\reports\ai-ml-competitions\arc-prize-feasibility-memo-20260616.md | Create arc-local-toy-harness-plan-20260616.md. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_devpost_prize_calendar_complete | `devpost-prize-calendar-20260616` - Devpost weekly prize calendar | E:\agent-company-lab\reports\ai-ml-competitions\devpost-prize-calendar-20260616.md | Create devpost-rules-packet-build-with-gemini-xprize-20260616.md after read-only rules refresh confirms eligibility and terms. | Local proof artifact only. No account, browser session, wallet, payment, public action, security testing, service-request mutation, worker start, API call, or real-money action occurred. |
| local_ai_ml_competitions_public_prize_source_refresh_complete | `ai-ml-competitions-public-prize-source-refresh-20260616` - AI/ML competitions public prize source refresh | E:\agent-company-lab\reports\ai-ml-competitions\public-prize-source-refresh-20260616.md | Create public-prize-shortlist work packet focused on ARC Prize 2026 and AIcrowd WhestBench local feasibility. | Local evidence only; no account, rules acceptance, dataset download, submission, paid compute, or external side effect. |
| local_seed_evidence | `first-local-evidence-ai_ml_competitions-20260615` - First local evidence packet for ai_ml_competitions | E:\agent-company-lab\reports\first-local-evidence-packets\ai_ml_competitions-first-local-evidence-20260615.md | Create a local shortlist template from approved public sources; stop before account, terms, dataset, compute spend, or submission. | Generated by platform_engineering as local first-evidence bootstrap; lane manager owns follow-up. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 76 | new | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-ai_ml_competitions` - Follow up customer input for ai_ml_competitions | lane-manager-ai_ml_competitions-019ec69a |  | intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.json | Create a competition feasibility packet with account/dataset/compute gates and local proof path. |
| 92 | complete | `task-continuity-owner-response-task-acknowledgement_response_required-task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-ai_ml_competitions` - Handle continuity owner acknowledgement response for task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-ai_ml_competitions | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\continuity-owner-response-v1-001-continuity-restore-response-v1-001-continuity-restore-v1-001-dispatch_stale_own | Existing owner `lane-manager-ai_ml_competitions-019ec69a` should handle the acknowledgement for `ai_ml_competitions` locally and report evidence; no duplicate owner or worker should be created. |
| 90 | complete | `task-customer-input-ceo-operating-goal-objective-20260620-002-owner-acknowledgement-ai_ml_competitions` - Acknowledge customer follow-up triage for ai_ml_competitions | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-requests-v1-20260621.md | Owner acknowledgement evidence linked at E:\agent-company-lab\reports\ai-ml-competitions-continuity-acknowledgement-next-action-v1-20260621.md; continue the lane follow-up locally with existing owner and no duplicate wor |
| 89 | complete | `task-arc-agi-3-micro-env-replay-baseline-v1-20260618` - Create ARC-AGI-3 micro-environment replay baseline | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-micro-env-replay-baseline-v1-validation-20260618.json | Extend the synthetic micro-environment suite with distractors and a tiny planner that infers prerequisite graphs from replay history. Keep Kaggle account/rules, official data, ARC toolkit/API keys, scorecards, submission |
| 88 | complete | `task-agent-company-atlas-baseline-climb-v1-20260617` - Add custom Baseline Climb Atlas minigame | recovered-profitable-edge-infra |  | Generated benchmark arena texture, custom frontend minigame renderer, trace metadata, regenerated snapshot, and browser validation | Regenerate the Atlas snapshot and verify the Baseline Climb minigame in browser. |
| 87 | complete | `task-arc-agi-3-prereq-planner-baseline-v1-20260618` - Create ARC-AGI-3 prerequisite planner baseline | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-prereq-planner-baseline-v1-validation-20260618.json | Add hidden-prerequisite environments where the planner must infer edges from blocked actions and failed attempts, then compare learned-edge planning against the visible-edge planner. Keep Kaggle account/rules, official d |
| 84 | complete | `task-kaggle-no-login-competition-fixture-scorer-v1-20260618` - Create Kaggle no-login competition fixture scorer | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\ai-ml-competitions\kaggle-no-login-competition-fixture-scorer-v1-validation-20260618.json | For local_baseline_only rows, create offline stub baselines using synthetic/public-open data only. Do not log in, create API tokens, accept competition rules, download Kaggle data, run Kaggle notebooks, submit, pay, post |
| 82 | complete | `task-lane-scout-arc_prize_2026-20260618` - Lane scout local proof: arc prize 2026 | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\arc-prize-2026-baseline-local-proof-validation.json | Create the ARC-AGI-3 micro-environment replay baseline locally; keep Kaggle account/rules, official data, submission, paper/public action, paid compute/API, worker/runtime, and external side effects blocked until human a |
| 77 | complete | `task-lane-scout-arc_agi_3-20260618` - Lane scout local proof: arc agi 3 | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\arc-agi-3-rules-gate-local-proof-validation.json | Implement the standard-library ARC-AGI-3 micro-environment replay baseline locally; do not install the official toolkit, create/use API keys, log in, download official/gated data, open scorecards, submit to Kaggle, publi |
| 72 | complete | `task-lane-scout-kaggle_money_competitions-20260618` - Lane scout local proof: kaggle money competitions | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\money-path-lane-scout-packets\kaggle-money-competition-scout-worksheet-local-proof-validation.json | Create a no-login Kaggle competition row fixture from manually saved public listing/rules snippets, then run the worksheet scorer and prove all rows either have a next local baseline action or a kill reason. Keep Kaggle |
| 70 | complete | `task-devpost-prize-calendar-20260616` - Create Devpost weekly prize calendar | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\ai-ml-competitions\devpost-prize-calendar-20260616.md | Create devpost-rules-packet-build-with-gemini-xprize-20260616.md after read-only rules refresh confirms eligibility and terms. |
| 70 | complete | `task-arc-prize-feasibility-memo-20260616` - Create ARC Prize 2026 feasibility memo | lane-manager-ai_ml_competitions-019ec69a |  | E:\agent-company-lab\reports\ai-ml-competitions\arc-prize-feasibility-memo-20260616.md | Create arc-local-toy-harness-plan-20260616.md. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| needs_review | browser_read_only_session | browser_research | `req-wave4-ai-ml-competitions-browser-readonly-20260614` |  | catalog_required_approval_no_external_action | Read public AI/ML competition listings and capture rules/prize/dataset gates; no browser side effects. | E:\agent-company-lab\requests\service-requests\req-wave4-ai-ml-competitions-browser-readonly-20260614\packet.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| kaggle_no_login_fixture_scorer_ready_local_only | no_login_competition_fixture_scorer | `outcome-kaggle-no-login-competition-fixture-scorer-v1-20260618` | 0.0 | E:\agent-company-lab\reports\ai-ml-competitions\kaggle-no-login-competition-fixture-scorer-v1-validation-20260618.json | For local_baseline_only rows, create offline stub baselines using synthetic/public-open data only. Do not log in, create API tokens, accept competition rules, download Kaggle data, run Kaggle notebooks, submit, pay, post |
| arc_agi_3_prereq_planner_baseline_complete_local_only | local_competition_baseline | `outcome-arc-agi-3-prereq-planner-baseline-v1-20260618` | 0.0 | E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-prereq-planner-baseline-v1-validation-20260618.json | Add hidden-prerequisite environments where the planner must infer edges from blocked actions and failed attempts, then compare learned-edge planning against the visible-edge planner. Keep Kaggle account/rules, official d |
| arc_agi_3_micro_env_replay_baseline_complete_local_only | local_competition_baseline | `outcome-arc-agi-3-micro-env-replay-baseline-v1-20260618` | 0.0 | E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-micro-env-replay-baseline-v1-validation-20260618.json | Extend the synthetic micro-environment suite with distractors and a tiny planner that infers prerequisite graphs from replay history. Keep Kaggle account/rules, official data, ARC toolkit/API keys, scorecards, submission |
| kaggle_money_competition_scout_worksheet_ready_local_only | local_proof | `outcome-kaggle-money-competition-scout-worksheet-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\kaggle-money-competition-scout-worksheet-local-proof-validation.json | Create a no-login Kaggle competition row fixture from manually saved public listing/rules snippets, then run the worksheet scorer and prove all rows either have a next local baseline action or a kill reason. Keep Kaggle |
| arc_agi_3_rules_gate_ready_local_only | local_rules_gate_packet | `outcome-arc-agi-3-rules-gate-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\arc-agi-3-rules-gate-local-proof-validation.json | Implement the standard-library ARC-AGI-3 micro-environment replay baseline locally; do not install the official toolkit, create/use API keys, log in, download official/gated data, open scorecards, submit to Kaggle, publi |
| arc_prize_2026_baseline_ready_local_only | local_competition_baseline | `outcome-arc-prize-2026-baseline-local-proof-20260618` | 0.0 | E:\agent-company-lab\reports\money-path-lane-scout-packets\arc-prize-2026-baseline-local-proof-validation.json | Create the ARC-AGI-3 micro-environment replay baseline locally; keep Kaggle account/rules, official data, submission, paper/public action, paid compute/API, worker/runtime, and external side effects blocked until human a |
| complete | atlas_lane_minigame_visual_upgrade | `outcome-agent-company-atlas-baseline-climb-v1-20260617` | 0.0 | reports/agent-company-atlas-baseline-climb-trace-metadata-20260617.json | Browser-verify the Baseline Climb route, animation layer, step controls, generated texture loading, and responsive layout. |
| local_toy_harness_runner_complete | executable_local_proof | `outcome-arc-toy-harness-run-20260616` | 0.0 | E:\agent-company-lab\reports\ai-ml-competitions\arc-toy-harness-run-20260616.json | Extend synthetic family coverage or keep ARC lane parked until competition rules/data gates are approved. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id ai_ml_competitions
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id ai_ml_competitions --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `ai_ml_competitions` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

