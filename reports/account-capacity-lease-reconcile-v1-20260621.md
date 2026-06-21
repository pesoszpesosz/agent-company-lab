# Account Capacity Lease Reconcile v1

Generated UTC: `2026-06-21T16:40:00Z`
Status: `capacity_released`
JSON mirror: `E:\agent-company-lab\reports\account-capacity-lease-reconcile-v1-20260621.json`

## Counts

| Count | Value |
| --- | ---: |
| `sessions_reconciled` | 1 |
| `sessions_changed` | 1 |
| `capacity_released` | 1 |
| `capacity_claimed` | 0 |

## Sessions

| Session | Status | Before | After | Released | Claimed |
| --- | --- | ---: | ---: | ---: | ---: |
| `codex-recovery-executor-low-concurrency` | available | 1 | 0 | 1 | 0 |

## Next Action

Rerun lane runtime activation planning; newly freed capacity may drain the next queued lane.

## Boundary

This reconciler updates local account capacity counters only for sessions represented in lane_runtime_thread_deliveries. It does not mutate task status, send thread messages, start workers, open browsers, approve service requests, call APIs, publish, submit, spend, trade, or contact anyone.
