# Agent Company Control Plane Scaling Radar Wave 22

Generated UTC: 2026-06-18T03:11:00Z

Purpose: evaluate current durable queue, workflow, and supervisor-control systems for scaling the local Agent Company control plane without enabling live workers.

## Recommendation

Build `control_plane_scaling_decision_matrix_v1` next as a report-only matrix. Do not install Temporal, DBOS, Hatchet, Trigger.dev, LangGraph, Prefect, Dagster, or Restate yet.

The local SQLite task/outcome/artifact/trace ledgers should remain the source of truth. External durable systems should be treated as future adapters, each blocked behind signed runtime-adapter approval, dry-run fixtures, service-worker readiness, and route-specific apply-command contracts.

## Candidate Systems

| System | Current Signal | Best Agent Company Fit | Disposition |
| --- | --- | --- | --- |
| Temporal | `temporalio/temporal`: 21,032 stars, pushed 2026-06-18 | Long-lived lane and service-worker workflows with Signals/Queries/Updates. | Adapter later |
| Hatchet | `hatchet-dev/hatchet`: 7,383 stars, pushed 2026-06-17 | Worker-pool queues, concurrency caps, fairness, and AI-agent background tasks. | Adapter later |
| DBOS | `dbos-inc/dbos-transact-py`: 1,425 stars, pushed 2026-06-17 | Database-first durable workflows, closest to the current SQLite ledger posture. | Adapter later |
| Trigger.dev | `triggerdotdev/trigger.dev`: 15,380 stars, pushed 2026-06-17 | Managed AI/task workflows, waits, queue concurrency, human approval patterns. | Adapter later |
| LangGraph | `langchain-ai/langgraph`: 35,076 stars, pushed 2026-06-17 | Agent state graphs, interrupts, and future supervisor inboxes. | Adapter later |
| Restate | `restatedev/restate`: 4,021 stars, pushed 2026-06-17 | Fault-tolerant services and durable RPC patterns. | Watch later |
| Prefect | `PrefectHQ/prefect`: 22,633 stars, pushed 2026-06-18 | Source refresh and data-flow orchestration. | Watch later |
| Dagster | `dagster-io/dagster`: 15,713 stars, pushed 2026-06-17 | Data asset orchestration and observability. | Watch later |

## Primary Source Patterns

- Temporal distinguishes asynchronous write messages, read-only inspection, and tracked read/write messages. The lab should mirror that split locally before exposing live workflow messages.
- Hatchet's concurrency controls queue excess runs until resource capacity exists. That maps well to future service-worker pool caps.
- Trigger.dev queue/wait patterns show how parent work can checkpoint at waitpoints instead of occupying execution capacity.
- DBOS durable workflows and steps fit the lab's database-first worldview, especially if SQLite later becomes Postgres.

## Decision Matrix Seed

| Capability | Keep Local Now | Adapter Later | First Gate |
| --- | --- | --- | --- |
| Durable lane workflow | SQLite task/outcome/trace ledgers. | Temporal or DBOS. | Signed runtime-adapter implementation approval plus zero-side-effect dry run. |
| Service-worker pool queue | Report-only queue, assignment plan, pool registry, and gate map. | Hatchet or Trigger.dev. | Human-approved service request, worker-pool registration, readiness pass, and apply-command contract. |
| Human supervisor inbox | CEO/manager inbox packets and static dashboard views only. | LangGraph Agent Inbox or custom local dashboard. | Explicit `ceo_manager_inbox_packet_v1` design approval. |
| Source refresh jobs | Source-spec registry and report-only freshness scheduler. | Prefect or Dagster. | Per-source browser/API/public-action gate and cost/data policy. |

## Zero Side-Effect Boundary

- GitHub metadata reads: 8
- Web documentation reads: 4
- Dependency installs: 0
- Runtime starts: 0
- Workflow engines started: 0
- Queues created: 0
- Workers started: 0
- Browser sessions started: 0
- Service requests assigned or updated: 0
- Tasks created or updated by the report: 0
- MCP/model/API calls: false
- Public/account/wallet/payment actions: false
- External side effects: false

## Source URLs

- https://docs.temporal.io/encyclopedia/workflow-message-passing
- https://docs.hatchet.run/v1/concurrency
- https://trigger.dev/docs/queue-concurrency
- https://docs.dbos.dev/python/tutorials/workflow-tutorial
- https://github.com/temporalio/temporal
- https://github.com/hatchet-dev/hatchet
- https://github.com/dbos-inc/dbos-transact-py
- https://github.com/triggerdotdev/trigger.dev
- https://github.com/restatedev/restate
- https://github.com/PrefectHQ/prefect
- https://github.com/dagster-io/dagster
- https://github.com/langchain-ai/langgraph

## Next Action

Build `control_plane_scaling_decision_matrix_v1` as a report-only matrix that ranks Temporal, DBOS, Hatchet, Trigger.dev, LangGraph, Prefect, Dagster, and Restate for each Agent Company capability without installing dependencies, creating queues, starting runtimes, mutating service requests, or performing external actions.
