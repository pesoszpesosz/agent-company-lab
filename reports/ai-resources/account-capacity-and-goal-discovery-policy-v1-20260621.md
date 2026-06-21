# Account Capacity and Goal Discovery Policy v1

Generated UTC: `2026-06-21T15:08:00Z`

Status: `adopt`

## Decision

The company must stop treating every non-responsive worker as a broken worker. Worker dispatch now separates thread health from account/session capacity:

1. `available`: a session can accept work now.
2. `cooling_down`: a session hit usage/rate limits and has a `resume_after_utc` or refresh-detected condition.
3. `needs_restore`: a thread or worker has no owner, no goal, repeated system errors, missing evidence, or a failed handoff route.
4. `retired_or_parked`: a worker is deliberately inactive and should not be rediscovered as a crisis.

## Refresh Behavior

When a new usable session or usage refresh is detected, AR should mark the corresponding capacity record `available`, then the dispatcher should immediately lease queued tasks in priority order up to the concurrency cap. No worker should be spammed during cooldown. The watchdog should report the cooldown once, then stay quiet until either `resume_after_utc` arrives, a refresh event is recorded, or the thread changes state.

Do not store refresh tokens or credentials in the company repo. Store only non-secret capacity state such as session alias, state, provider/surface, concurrency cap, `resume_after_utc`, last failure summary, and last successful dispatch.

## Dynamic Goal Discovery

The continuity loop must treat Codex app threads as a discovery source, not only the SQLite roster. Each heartbeat should:

1. Snapshot recent Codex threads.
2. Detect goal signals from `/goal`, `Active goal`, `Current goal`, or `Goal:`.
3. Compare goal threads against registered `agents.thread_id` and `lanes.owner_thread_id`.
4. Flag unregistered goal threads for AR registration.
5. Flag `systemError` goal threads for restore.
6. Flag non-repo-backed goal threads for migration or absolute-path executor handling.

This prevents new Codex conversations with active goals from becoming invisible.

## Dispatch Shape

Use a central queue instead of direct multi-thread blasting. The default mode during shared-account pressure is sequential or very low concurrency. If a session refresh arrives, the queue drains immediately without human prompting; if capacity drops again, the dispatcher parks remaining work rather than creating duplicate workers.

## Immediate Application

The dynamic inventory command is now `python tools\agent_company.py write-codex-thread-goal-inventory --thread-snapshot <snapshot.json>`.

The recovery executor thread `019eeaaa-ccf5-7d51-9274-e000a7b96ccd` proved the bounded absolute-path recovery pattern by completing the seven stuck `007` lane-next tasks without mutating lane ownership.

## Boundary

This policy is local coordination only. It does not create accounts, store credentials, bypass usage limits, start external worker runtimes, call APIs, approve service requests, open browsers, publish, submit, spend, trade, or contact anyone.
