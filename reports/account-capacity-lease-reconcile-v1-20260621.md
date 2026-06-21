# Account Capacity Lease Reconcile v1

Generated UTC: `2026-06-21T16:02:20Z`
Status: `already_consistent`
JSON mirror: `E:\agent-company-lab\reports\account-capacity-lease-reconcile-v1-20260621.json`

## Counts

| Count | Value |
| --- | ---: |
| `sessions_reconciled` | 1 |
| `sessions_changed` | 0 |
| `capacity_released` | 0 |
| `capacity_claimed` | 0 |

## Sessions

| Session | Status | Before | After | Released | Claimed |
| --- | --- | ---: | ---: | ---: | ---: |
| `codex-recovery-executor-low-concurrency` | available | 1 | 1 | 0 | 0 |

## Next Action

Capacity counters already match active runtime deliveries.

## Boundary

This reconciler updates local account capacity counters only for sessions represented in lane_runtime_thread_deliveries. It does not mutate task status, send thread messages, start workers, open browsers, approve service requests, call APIs, publish, submit, spend, trade, or contact anyone.
