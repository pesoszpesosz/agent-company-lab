# Durable Runtime Comparison Decision Packet v1

Generated UTC: 2026-06-20T12:40:47Z
Packet: `E:\agent-company-lab\reports\durable-orchestration\durable-runtime-comparison-decision-packet-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\durable-runtime-comparison-decision-packet-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\durable-runtime-comparison-decision-packet-v1.schema.json`

## Summary

- Source validations checked: `8`
- Runtime recommendations checked: `7`
- Failed: `0`
- Primary recommendation: Implement the next executable layer as a local SQLite/outbox service-worker queue runner, not as Temporal, Inngest, DBOS, Pydantic durable execution, Prefect, or Restate.
- External side effects: `false`

## Runtime Ranking

| Rank | Runtime | Decision | Score |
| ---: | --- | --- | ---: |
| 1 | `sqlite_control_plane` | `promote_now_local_only` | 94 |
| 2 | `temporal_python` | `hold_for_human_runtime_approval_after_local_runner` | 83 |
| 3 | `inngest` | `hold_for_event_adapter_approval_after_local_outbox_ack` | 78 |
| 4 | `dbos_python` | `hold_for_database_provisioning_review` | 76 |
| 5 | `pydantic_ai_durable_execution` | `reference_only_until_model_api_gate` | 75 |
| 6 | `restate` | `watchlist_after_local_outbox_service_boundaries` | 70 |
| 7 | `prefect` | `watchlist_for_source_refresh_after_local_runner` | 66 |

## Implementation Sequence

| Step | Build | Status |
| ---: | --- | --- |
| 1 | `sqlite_outbox_acknowledgement_runner_v1` | `recommended_next_local_build` |
| 2 | `local_service_worker_request_state_machine_runner_v1` | `recommended_after_ack_preview` |
| 3 | `runtime_implementation_human_approval_packet_v2` | `recommended_before_any_external_runtime` |

## Decision

Promote the local SQLite/outbox runner path first. Hold Temporal, Inngest, DBOS, Pydantic durable execution, Prefect, and Restate behind explicit dependency/runtime/model/API/server/cloud/database/service-worker approval gates.

## Boundary

- No dependency install, import, runtime start, queue enqueue, workflow start, event send, server start, database provisioning, service-request mutation, worker start, browser session, API/model call, public action, or external side effect.
