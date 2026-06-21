# Account Churn Restoration Status v1

Generated UTC: `2026-06-21T16:05:00Z`
Status: `better_but_needs_refresh_detector`

## Answer

The queue/capacity restructuring is working better: exhausted capacity now becomes pending_capacity, and one bounded dispatch was delivered without blasting all lane threads. It is not complete because refresh detection still does not automatically flip the cooling-down pool back to available.

## Current Readout

- The low-concurrency executor accepted exactly one dispatch and is now occupied by premium_customer_intake-009.
- The owner-thread delivery ledger shows the 009 prompt delivered once, so it will not resend by accident.
- The activation planner now reports pending_capacity rather than restore/broken for the remaining queued lanes.
- The watchdog remains clear: no ownerless lanes, missing owner threads, expired leases, duplicate active keys, or lanes without open tasks.

## Remaining Gaps

- The projectless parallel pool is still cooling_down even though its resume_after_utc has passed; the system needs a real refresh detector, not just a time hint.
- There is no single command yet that runs reconcile -> seed -> plan -> drain -> outbox -> delivery receipt -> reconcile as one durable cycle.
- Capacity release still depends on task completion being observed and reconciled after the owner thread finishes.

## Next Evolution

- Add a refresh-signal intake that can mark sessions available only when a new usable account/session/refresh token is actually detected.
- Add a single continuity-cycle command that drains one or N tasks according to capacity and writes an auditable summary.
- Add stale in_progress lease escalation so a delivered task that does not complete becomes needs_restore instead of silently holding capacity.

## Evidence Counts

| Signal | Value |
| --- | ---: |
| `available_capacity` | 0 |
| `dispatch_recommendations` | 0 |
| `eligible_task_candidates` | 12 |
| `lanes_pending_capacity` | 12 |
| `watchdog_ownerless_active_lanes` | 0 |
| `watchdog_agents_missing_threads` | 0 |
| `watchdog_expired_leases` | 0 |
| `watchdog_lanes_without_open_tasks` | 0 |

## Boundary

This status packet is local evidence only. It did not start browsers, change accounts, approve service requests, publish, submit, spend, trade, or contact anyone.
