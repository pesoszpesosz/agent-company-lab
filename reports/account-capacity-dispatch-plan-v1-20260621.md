# Account Capacity Dispatch Plan v1

Generated UTC: `2026-06-21T15:36:30Z`
Status: `ready_to_dispatch`
JSON mirror: `E:\agent-company-lab\reports\account-capacity-dispatch-plan-v1-20260621.json`
Capacity snapshot: `reports\ai-resources\account-capacity-snapshot-v1-20260621.json`

## Counts

| Count | Value |
| --- | ---: |
| `sessions_seen` | 2 |
| `available_sessions` | 1 |
| `cooling_down_sessions` | 1 |
| `needs_restore_sessions` | 0 |
| `retired_or_parked_sessions` | 0 |
| `available_capacity` | 1 |
| `queued_task_candidates` | 7 |
| `dispatch_recommendations` | 1 |

## Sessions

| Session | Surface | Status | Capacity | Resume | Last Refresh |
| --- | --- | --- | ---: | --- | --- |
| `codex-recovery-executor-low-concurrency` | codex | `available` | 1 |  | 2026-06-21T15:36:00Z |
| `codex-projectless-lane-manager-parallel-pool` | codex | `cooling_down` | 0 | 2026-06-21T16:00:00Z |  |

## Dispatch Recommendations

| Session | Task | Lane | Priority | Owner Thread | Action |
| --- | --- | --- | ---: | --- | --- |
| `codex-recovery-executor-low-concurrency` | `task-customer-input-ceo-operating-goal-objective-20260620-002-followup-ai_ml_competitions` | `ai_ml_competitions` | 76 | codex-thread:019eea2b-dd71-7483-ae49-22ed784dd4d2 | `lease_then_dispatch_with_capacity_guard` |

## Next Action

Lease recommended tasks through a scoped local command, then dispatch only up to available session capacity.

## Boundary

This planner records local capacity state and writes dispatch recommendations only. It does not store credentials or refresh tokens, mutate task leases, send thread messages, start workers, approve service requests, open browsers, call APIs, publish, submit, spend, trade, or contact anyone.
