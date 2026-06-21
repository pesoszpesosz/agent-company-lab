# Lane Runtime Dispatch Drain v1

Generated UTC: `2026-06-21T16:02:00Z`
Status: `dispatch_packets_ready`
Dry run: `False`
Activation plan: `reports\lane-runtime-activation-plan-v1-20260621.json`
JSON mirror: `E:\agent-company-lab\reports\lane-runtime-dispatch-drain-v1-20260621.json`
Packet dir: `E:\agent-company-lab\reports\lane-runtime-dispatch-packets-v1-20260621`

## Counts

| Count | Value |
| --- | ---: |
| `recommendations_seen` | 1 |
| `leased_dispatches` | 1 |
| `skipped_dispatches` | 0 |
| `packets_written` | 1 |
| `sessions_touched` | 1 |

## Leased Dispatches

| Session | Task | Lane | Lease Owner | Expires | Packet |
| --- | --- | --- | --- | --- | --- |
| `codex-recovery-executor-low-concurrency` | `task-continuity-lane-next-task-20260621-premium_customer_intake-009` | `premium_customer_intake` | `premium-customer-intake-agent-20260620` | `2026-06-21T18:02:00Z` | E:\agent-company-lab\reports\lane-runtime-dispatch-packets-v1-20260621\lane-runtime-dispatch-task-continuity-lane-next-t |

## Skipped Dispatches

| Reason | Session | Task | Lane |
| --- | --- | --- | --- |
| none |  |  |  |

## Next Action

Deliver the dispatch packets to the leased owner threads through the next approved local worker adapter.

## Boundary

This drain only writes local packets and, when not in dry-run mode, mutates local task leases and account capacity counters. It does not send thread messages, start workers, open browsers, approve service requests, publish, submit, spend, trade, call APIs, or contact anyone.
