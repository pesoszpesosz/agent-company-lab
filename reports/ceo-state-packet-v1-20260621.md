# CEO State Packet V1

Generated UTC: 2026-06-21T13:10:31Z
Status: `current_local_state_packet`
Packet id: `ceo-state-packet-v1-20260621`
JSON mirror: `E:\agent-company-lab\reports\ceo-state-packet-v1-20260621.json`

## Company Counts

| Table | Count |
| --- | ---: |
| lanes | 15 |
| departments | 24 |
| roles | 25 |
| agents | 23 |
| tasks | 650 |
| artifacts | 2636 |
| outcomes | 462 |
| trace_events | 575 |
| service_requests | 16 |

## Active Blockers And Gates

- Service requests needing review: `13`
- Blocked tasks: `0`
- Stale owner acknowledgements: `0`

## Current Decision Batch

- `owner_acknowledgement_pressure`
- `goal_evolver_review`
- `ceo_state_packet`
- `human_action_feed`
- `manager_dispatch_queue`

## Next Dispatch Queue

| Kind | Task | Lane | Next Action |
| --- | --- | --- | --- |
| open_task | `task-lane-manager-ai_resources_lab-20260620-active-goal-20260621` | `ai_resources_lab` | Lead the AI Resources operating cell: hire, evolve, park, or retire agents only after capability-overlap review and local evidence. |
| open_task | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-escalation-ai_resources_lab` | `ai_resources_lab` | AI Resources should triage stale customer follow-ups and either evolve/reuse one existing worker, park with revisit condition, or draft a CEO decision-batch item. |
| open_task | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-ai_resources_lab` | `ai_resources_lab` | Evaluate required worker/resource capability and propose one non-overlapping upgrade or reuse path. |
| open_task | `task-capability-overlap-mapper-20260621-active-goal-20260621` | `ai_resources_lab` | Maintain the capability overlap map so new AI hires happen only when existing owners cannot evolve to cover the need. |
| open_task | `task-candidate-registry-curator-20260621-active-goal-20260621` | `ai_resources_lab` | Curate external AI worker frameworks and money-making agent candidates into a local candidate registry with source evidence. |
| open_task | `task-local-evaluation-harness-builder-20260621-active-goal-20260621` | `ai_resources_lab` | Build local-only eval packets that prove whether candidate agents or tools improve the company before adoption. |
| open_task | `task-adoption-retirement-reviewer-20260621-active-goal-20260621` | `ai_resources_lab` | Recommend evolve, watch, reject, merge, or retire decisions for stale, overlapping, or under-specified agents. |
| open_task | `task-continuity-watchdog-worker-20260621-active-goal-20260621` | `ai_resources_lab` | Run the continuity loop: check active lanes for stale, offline, ownerless, overlapping, or goal-less work and write restore packets. |
| open_task | `task-premium-customer-context-router-20260621-active-goal-20260621` | `ai_resources_lab` | Accept premium customer input, preserve raw material outside CEO context, route compact capsules to lanes, and update the customer. |
| open_task | `task-browser-account-ops-worker-20260621-active-goal-20260621` | `ai_resources_lab` | Prepare browser/account operation packets and surface exact human KYC, tax, billing, terms, or legal gates without taking side effects. |

## Boundary

This packet is a compact local state summary only. It does not approve service requests, start workers, call models/APIs, open browsers, create accounts, publish, submit, trade, spend, or perform security testing.
