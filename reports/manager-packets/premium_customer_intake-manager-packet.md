# Manager Packet - premium_customer_intake

Generated UTC: 2026-06-20T21:01:19Z
Department: Customer/Operator Success
Lane status: active
Current owner: `premium-customer-intake-agent-20260620`

## Manager Directive

Own only the `premium_customer_intake` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Create one narrow task with evidence requirements, duplicate key, owner, and stop gates before launching seekers.

## CEO Recommendation

Create one narrow manager task with evidence requirements before launching seekers.

## Allowed Worker Types

- premium_customer_intake_agent
- human_action_desk_worker
- observability_worker

## Example Work

- new customer requests
- lane-specific source material
- YouTube videos or references
- operator constraints
- human-provided account readiness notes
- new business ideas
- corrections and priority changes

## Promotion Gates

- newest request captured
- current company context checked
- route chosen or parked with reason
- CEO context capsule written
- knowledge application path assigned
- customer update emitted

## Required Service Workers

- observability_worker
- human_action_desk_worker
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
- local input packet
- local routing ledger entry
- local artifact registration
- local task proposal
- compact CEO update

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
| 119 | complete | `task-premium-customer-intake-router-v1-20260620` - Install premium customer intake router and knowledge application loop | premium-customer-intake-agent-20260620 |  | Premium customer intake role/lane/agent, router contract, intake workspace, routing ledger, route packet, knowledge application loop, customer update feed, CEO state packet v2, tra | Use premium_customer_intake for future customer requests and lane materials; create youtube_no_post_content_batch_v1 next. |
| 92 | complete | `task-premium-customer-followup-escalation-command-v1-20260620` - Executable premium customer follow-up escalation v1 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\tools\agent_company_core\premium_customer_followup_escalation.py | Next let AI Resources triage the escalation packet into a non-overlap local plan or CEO decision-batch item. |
| 92 | complete | `task-premium-customer-intake-router-command-v1-20260620` - Executable premium customer intake router v1 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\tools\agent_company_core\premium_customer_intake_router.py | Use route-premium-customer-input for new customer requests/materials; next add lane-specific follow-up task synthesis. |
| 91 | complete | `task-premium-customer-followup-synthesizer-command-v1-20260620` - Executable premium customer lane follow-up synthesizer v1 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\tools\agent_company_core\premium_customer_followup_synthesizer.py | Next add stale follow-up monitor and lane-manager acknowledgement reports. |
| 90 | complete | `task-premium-customer-followup-monitor-command-v1-20260620` - Executable premium customer follow-up monitor v1 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\tools\agent_company_core\premium_customer_followup_monitor.py | Next escalate stale unacknowledged follow-ups into AI Resources or CEO decision batch without starting workers. |
| 89 | complete | `task-customer-input-ceo-operating-goal-objective-20260620-002-lane-followup-synthesis` - Synthesize lane follow-ups for customer-input-ceo-operating-goal-objective-20260620-002 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\intake\customer\processed\customer-input-ceo-operating-goal-objective-20260620-002-lane-followups.md | Lane managers own generated local tasks; intake monitors for stale unclaimed follow-ups. |
| 88 | complete | `task-premium-customer-followup-escalation-v1-customer-input-ceo-operating-goal-objective-20260620-002` - Escalate stale premium customer follow-ups for customer-input-ceo-operating-goal-objective-20260620-002 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\reports\customer-followup-escalation-v1-20260620.md | AI Resources should triage stale customer follow-ups and either evolve/reuse one existing worker, park with revisit condition, or draft a CEO decision-batch item. |
| 88 | complete | `task-customer-input-ceo-operating-goal-objective-20260620-002` - Route premium customer input customer-input-ceo-operating-goal-objective-20260620-002 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.md | ai_resources_lab_followup_packet_or_task |
| 87 | complete | `task-premium-customer-followup-monitor-v1-customer-input-ceo-operating-goal-objective-20260620-002` - Monitor premium customer follow-ups for customer-input-ceo-operating-goal-objective-20260620-002 | premium-customer-intake-agent-20260620 |  | E:\agent-company-lab\reports\customer-followup-monitor-v1-20260620.md | Escalate ownerless, blocked, or stale follow-ups to AI Resources or the CEO decision batch. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| validated | customer_followup_escalation_capability | `outcome-premium-customer-followup-escalation-command-v1-20260620` | 0.0 | E:\agent-company-lab\tools\agent_company_core\premium_customer_followup_escalation.py | Use the escalation packet to drive AI Resources triage, then surface only CEO-grade decisions or customer updates. |
| escalation_needed | customer_followup_escalation | `outcome-premium-customer-followup-escalation-customer-input-ceo-operating-goal-objective-20260620-002` | 0.0 | E:\agent-company-lab\reports\customer-followup-escalation-v1-20260620.md | AI Resources should triage stale customer follow-ups and either evolve/reuse one existing worker, park with revisit condition, or draft a CEO decision-batch item. |
| validated | customer_followup_monitor_capability | `outcome-premium-customer-followup-monitor-command-v1-20260620` | 0.0 | E:\agent-company-lab\tools\agent_company_core\premium_customer_followup_monitor.py | Create an escalation packet for stale unacknowledged follow-ups without starting lane work. |
| attention_needed | customer_followup_monitor | `outcome-premium-customer-followup-monitor-customer-input-ceo-operating-goal-objective-20260620-002` | 0.0 | E:\agent-company-lab\reports\customer-followup-monitor-v1-20260620.md | Escalate ownerless, blocked, or stale follow-ups to AI Resources or the CEO decision batch. |
| validated | customer_followup_synthesis_capability | `outcome-premium-customer-followup-synthesizer-command-v1-20260620` | 0.0 | E:\agent-company-lab\tools\agent_company_core\premium_customer_followup_synthesizer.py | Add stale follow-up monitor and lane-manager acknowledgement reports. |
| synthesized | customer_lane_followup_synthesis | `outcome-customer-input-ceo-operating-goal-objective-20260620-002-lane-followups` | 0.0 | E:\agent-company-lab\intake\customer\processed\customer-input-ceo-operating-goal-objective-20260620-002-lane-followups.md | Monitor generated lane tasks; escalate stale or ownerless lanes to AI Resources. |
| validated | customer_intake_capability | `outcome-premium-customer-intake-router-command-v1-20260620` | 0.0 | E:\agent-company-lab\tools\agent_company_core\premium_customer_intake_router.py | Add lane-specific follow-up task synthesis from route packets so routed inputs automatically create actionable lane work. |
| routed | customer_input_routing | `outcome-customer-input-ceo-operating-goal-objective-20260620-002` | 0.0 | E:\agent-company-lab\intake\customer\routes\customer-input-ceo-operating-goal-objective-20260620-002.md | ai_resources_lab_followup_packet_or_task |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id premium_customer_intake
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id premium_customer_intake --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `premium_customer_intake` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

