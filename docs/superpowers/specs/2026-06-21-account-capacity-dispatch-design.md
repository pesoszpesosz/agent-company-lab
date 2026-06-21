# Account Capacity Dispatch Design

Date: 2026-06-21

## Context

The company has Codex goal threads and lane tasks, but shared account/session limits can make several workers appear unavailable at once. Treating that as ordinary worker failure creates noisy restore loops. The prior policy packet established the rule: capacity state is separate from worker/thread health.

## Design

Add a local-only account capacity dispatch planner. It reads a non-secret capacity snapshot, persists current session state, reads queued local tasks, and writes a dispatch plan that says which tasks can be leased when capacity is available.

Capacity sessions have:

- `session_id`
- `surface`
- `account_label`
- `status`: `available`, `cooling_down`, `needs_restore`, or `retired_or_parked`
- `concurrency_limit`
- `active_lease_count`
- `resume_after_utc`
- `last_refresh_utc`
- `last_error`
- `notes`

The planner never stores refresh tokens or credentials. It does not send Codex thread messages, open browsers, start workers, approve service requests, or mutate task leases. It is a deterministic local report and DB ledger update only.

## Dispatch Rules

1. Available capacity equals the sum of `max(0, concurrency_limit - active_lease_count)` for `available` sessions.
2. Cooling sessions do not dispatch until `resume_after_utc` or a later snapshot marks them `available`.
3. Candidate tasks are local DB tasks with `status = new`, ordered by priority descending and creation time ascending.
4. Recommendations are capped by available capacity and `--max-tasks`.
5. The report includes a next wakeup time when all usable sessions are cooling down.

## Outputs

- JSON report: `reports/account-capacity-dispatch-plan-v1-YYYYMMDD.json`
- Markdown report: `reports/account-capacity-dispatch-plan-v1-YYYYMMDD.md`
- SQLite rows in `account_capacity_sessions`
- Audit task/artifact rows unless `--no-db-record` is used

## Verification

Tests cover:

- available sessions produce bounded recommendations without mutating task leases
- cooling-only sessions produce no recommendations and expose the earliest resume time
- CLI parser registration

## Boundary

This design is local control-plane coordination only. It does not create accounts, store credentials, bypass usage limits, start external worker runtimes, call APIs, approve service requests, open browsers, publish, submit, spend, trade, or contact anyone.
