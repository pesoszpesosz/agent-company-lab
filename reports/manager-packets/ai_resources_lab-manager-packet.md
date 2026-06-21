# Manager Packet - ai_resources_lab

Generated UTC: 2026-06-21T14:28:26Z
Department: Artificial Resources
Lane status: active
Current owner: `lane-manager-ai_resources_lab-20260620`

## Manager Directive

Own only the `ai_resources_lab` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Create one narrow task with evidence requirements, duplicate key, owner, and stop gates before launching seekers.

## CEO Recommendation

Create one narrow manager task with evidence requirements before launching seekers.

## Allowed Worker Types

- ai_resources_manager
- ai_resource_evaluator
- goal_evolver_agent
- capability_overlap_mapper

## Example Work

- agent frameworks
- research infrastructures
- money-making tools
- GitHub projects
- YouTube production tooling
- Kaggle baselines
- bounty scanners
- market research systems

## Promotion Gates

- local fixture proof
- clear capability gap
- lower overlap than existing tools
- risk and license reviewed
- time-to-proof under two focused work blocks

## Required Service Workers

- observability_worker
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
- local file writes
- local SQLite records
- local fixture runs
- report-only adoption packets

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
| 96 | in_progress | `task-lane-manager-ai_resources_lab-20260620-active-goal-20260621` - Active goal for lane-manager-ai_resources_lab-20260620 | lane-manager-ai_resources_lab-20260620 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Lead the AI Resources operating cell: hire, evolve, park, or retire agents only after capability-overlap review and local evidence. |
| 90 | in_progress | `task-capability-overlap-mapper-20260621-active-goal-20260621` - Active goal for capability-overlap-mapper-20260621 | capability-overlap-mapper-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Maintain the capability overlap map so new AI hires happen only when existing owners cannot evolve to cover the need. |
| 90 | in_progress | `task-candidate-registry-curator-20260621-active-goal-20260621` - Active goal for candidate-registry-curator-20260621 | candidate-registry-curator-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Curate external AI worker frameworks and money-making agent candidates into a local candidate registry with source evidence. |
| 90 | in_progress | `task-local-evaluation-harness-builder-20260621-active-goal-20260621` - Active goal for local-evaluation-harness-builder-20260621 | local-evaluation-harness-builder-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Build local-only eval packets that prove whether candidate agents or tools improve the company before adoption. |
| 90 | in_progress | `task-adoption-retirement-reviewer-20260621-active-goal-20260621` - Active goal for adoption-retirement-reviewer-20260621 | adoption-retirement-reviewer-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Recommend evolve, watch, reject, merge, or retire decisions for stale, overlapping, or under-specified agents. |
| 90 | in_progress | `task-continuity-watchdog-worker-20260621-active-goal-20260621` - Active goal for continuity-watchdog-worker-20260621 | continuity-watchdog-worker-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Run the continuity loop: check active lanes for stale, offline, ownerless, overlapping, or goal-less work and write restore packets. |
| 90 | in_progress | `task-premium-customer-context-router-20260621-active-goal-20260621` - Active goal for premium-customer-context-router-20260621 | premium-customer-context-router-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Accept premium customer input, preserve raw material outside CEO context, route compact capsules to lanes, and update the customer. |
| 90 | in_progress | `task-browser-account-ops-worker-20260621-active-goal-20260621` - Active goal for browser-account-ops-worker-20260621 | browser-account-ops-worker-20260621 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Prepare browser/account operation packets and surface exact human KYC, tax, billing, terms, or legal gates without taking side effects. |
| 120 | complete | `task-ceo-operating-goal-v1-20260620` - Install CEO operating goal and AI Resources bootstrap | lane-manager-ai_resources_lab-20260620 |  | CEO operating goal Markdown/JSON, goal-evolver charter, registry/taxonomy updates, install report, trace event | Create ai_resources_candidate_registry_v1, human_action_feed_v1, ceo_state_packet_v1, and youtube_lane_scout_packet as local report-only packets. |
| 118 | complete | `task-ceo-first-state-packets-v1-20260620` - Install first CEO state packets and YouTube lane scout | lane-manager-ai_resources_lab-20260620 |  | AI Resources candidate registry, human-action feed, CEO state packet, YouTube lane scout, YouTube registry/taxonomy updates, trace event | Create youtube_no_post_content_batch_v1 and control_plane_capacity_benchmark_packet_v1 as local report-only proofs. |
| 99 | complete | `task-ceo-worker-bootstrap-v1-20260621` - Bootstrap CEO worker constellation | lane-manager-ai_resources_lab-20260620 |  | E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md | Run continuity watchdog snapshots on cadence, then route restore packets to AI Resources or CEO decision batch. |
| 98 | complete | `task-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621` - Park submitted payout lane as external-owned read-only | lane-manager-ai_resources_lab-20260620 |  | E:\agent-company-lab\reports\submitted-bounty-payouts-external-owned-parking-decision-v1-20260621.md | Reopen only if the user explicitly reassigns payout monitoring into this lab, supplies the live parallel worker thread id, or asks AR to replace the external payout worker. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| lane_next_monitor_recorded | ai_resources_lane_next_monitor | `outcome-ai-resources-lane-next-monitor-v1-20260621` | 0.0 | E:\agent-company-lab\reports\ai-resources-lane-next-monitor-v1-20260621.md | Create or continue lane-next evidence watch through existing owners; do not recreate acknowledgement dispatches or create duplicate workers without overlap proof. |
| repaired_existing_seed_evidence | continuity_lane_next_task_seed | `outcome-continuity-lane-next-task-seed-20260621` | 0.0 | E:\agent-company-lab\reports\continuity-lane-next-task-seed-v1-20260621.md | Regenerate continuity watchdog, manager packets, CEO state, and lane thread manifest. |
| completed_local_followup_routing | ai_resources_direct_followup_routing | `outcome-ai-resources-direct-followup-routing-v1-20260621` | 0.0 | E:\agent-company-lab\reports\ai-resources-customer-followup-routing-v1-20260621.md | Use post-acknowledgement AR queue coordination task to track remaining local AR work and service gates. |
| completed_local_followup_routing | ai_resources_customer_followup_routing | `outcome-ai-resources-customer-followup-routing-v1-20260621` | 0.0 | E:\agent-company-lab\reports\ai-resources-customer-followup-routing-v1-20260621.md | Continue remaining AR queue through existing AR workers; no acknowledgement redispatch needed. |
| no_dispatch_needed | ai_resources_owner_acknowledgement_dispatch | `outcome-ai-resources-owner-acknowledgement-dispatch-all` | 0.0 | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-dispatch-v1-20260621.md | No stale owner acknowledgements require dispatch; continue monitoring. |
| clear | ai_resources_owner_acknowledgement_monitor | `outcome-ai-resources-owner-acknowledgement-monitor-all` | 0.0 | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-monitor-v1-20260621.md | No acknowledgement escalation required; continue monitoring owner responses. |
| closure_applied | ai_resources_owner_acknowledgement_closure | `outcome-ai-resources-owner-acknowledgement-closure-all` | 0.0 | E:\agent-company-lab\reports\ai-resources-owner-acknowledgement-closure-v1-20260621.md | Regenerate owner acknowledgement monitor, CEO state, and continuity watchdog reports. |
| completed_local_acknowledgement_evidence | owner_acknowledgement_evidence | `outcome-ai-resources-owner-acknowledgement-customer-objective-20260621` | 0.0 | E:\agent-company-lab\reports\ai-resources-continuity-owner-acknowledgement-evidence-v1-20260621.md | Continue direct AI Resources follow-up and stale follow-up triage through existing AR workers and stop gates. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id ai_resources_lab
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id ai_resources_lab --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `ai_resources_lab` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

