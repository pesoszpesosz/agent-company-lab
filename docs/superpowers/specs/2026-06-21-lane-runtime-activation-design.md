# Lane Runtime Activation Design

## Problem

The control plane needs to answer two separate questions:

1. Should this lane be active right now?
2. Is there account/session capacity to run it right now?

Treating those as one question causes bad restores. When a shared account is exhausted, every thread looks offline, so the watchdog can spam restore attempts instead of recognizing a capacity cooldown. When a lane is only supposed to run after customer input, it can also be mistaken for a failed always-on worker.

## Design

Add a `lane_runtime_policies` table and a local planner:

- `always_on`: kept warm every continuity cycle. If no task exists, the right action is seed or monitor. If tasks exist and capacity exists, dispatch. If tasks exist and capacity is exhausted, mark pending capacity.
- `on_demand`: idle until a trigger creates queued work, such as customer material, a service request, a source packet, or a lane-specific intake file.
- `scheduled`: eligible on a cadence. The current slice treats queued scheduled work as eligible and leaves actual clock expansion to later cadence runners.
- `parked`: no dispatch, even if tasks exist. This is for external-owned or intentionally suspended lanes.

The planner joins that policy layer with `account_capacity_sessions`. It recommends dispatch only when both the lane policy and capacity state allow it.

## Queue Semantics

The queue is still the existing `tasks` table. A task becomes runnable only if:

- `tasks.status = 'new'`
- `tasks.lease_owner_agent_id IS NULL`
- the lane has a runtime policy that permits activation
- at least one account/session slot is available

The planner is advisory. It writes JSON/Markdown state and DB audit records, but does not mutate leases, send thread messages, start browsers, approve service requests, publish, trade, submit, or contact anyone.

## Capacity Exhaustion Behavior

Capacity statuses stay separate from worker health:

- `available`: dispatch up to `concurrency_limit - active_lease_count`
- `cooling_down`: do not restore-spam; record next wakeup and wait
- `needs_restore`: restore the account/session, not every lane thread
- `retired_or_parked`: keep it out of capacity math

If eligible work exists but no slot exists, the lane state is `pending_capacity`, not `offline` or `broken`.

## Result

The watchdog can report three distinct states:

- worker/thread health
- lane activation state
- account/session capacity state

That gives the CEO layer an abstract control surface: activate lanes by policy, queue work by task priority and lane class, and resume fast when a refreshed session appears.

## Drain Execution

The drain executor consumes `lane_runtime_activation_plan.v1` recommendations after the planner has selected capacity-eligible tasks. It re-checks the task row and account/session row before leasing so stale recommendations cannot consume a full session or overwrite an active task lease.

The executor is still local-only:

- it sets local task leases and `in_progress` status
- it increments `account_capacity_sessions.active_lease_count`
- it writes dispatch packets for the owner thread adapter
- it does not send messages, start workers, open browsers, call APIs, approve service requests, publish, submit, spend, trade, or contact anyone

After a successful drain, rerunning the activation planner should normally move remaining eligible lanes to `pending_capacity` until a session refresh makes slots available again.
