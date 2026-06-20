# Agent Company Deep Research Wave 7 - 2026-06-15

Generated at: 2026-06-14T21:51:53Z

Scope: current open-source infrastructure for scaling an agent company: CEO/control plane, lane managers, seeker agents, gated service workers, browser workers, durable queues, human approval UI, and observability. All evidence below came from read-only GitHub metadata lookups. No account, browser, payment, wallet, legal, KYC, public submission, or real-money action was performed.

## Executive Decision

Do not make a single agent framework the company. The company is the control plane: lanes, ownership, tasks, service requests, artifacts, outcomes, and traces. Frameworks belong behind adapters. The current SQLite ledger should remain the CEO system until worker volume forces Postgres/durable queues.

The strongest Wave 7 architecture is:

1. CEO/control plane: existing SQLite ledger and generated dashboards.
2. Department managers: lane-specific threads that create typed work packets and service requests.
3. Seeker agents: framework adapters, chosen per lane, that research money paths and produce evidence artifacts.
4. Service desks: gated workers for browser sessions, registrations, wallets, legal/KYC/tax/payment, public submissions, and model/API cost-bearing calls.
5. Durable execution: DBOS first, Hatchet second, Temporal only when local queues are no longer enough.
6. Human-in-the-loop UI: AG-UI/CopilotKit-style event stream for approvals, blockers, trace review, and queue triage.
7. Observability/evals: local trace_events first, OpenInference-shaped export later, Langfuse/Phoenix as optional viewers.

## Why This Matters For Money Paths

The money system cannot safely scale by giving every lane agent direct browser, wallet, account, or submission powers. The profitable shape is a company: seekers find opportunities, managers rank them, service desks handle high-risk capabilities under explicit approval, and the CEO ledger proves what happened. This lets us run many investigations while keeping real-money and public-action gates intact.

## Current Source Findings

- openai/openai-agents-python (agent_runtime): 27144 stars, 4190 forks, Python, license MIT, latest release v0.17.5 published 2026-06-11T04:11:51Z; pushed 2026-06-13T06:18:40Z. Role: reference Python runtime adapter for seekers/managers; useful for handoffs, tools, tracing-shaped local manifests. Source: https://github.com/openai/openai-agents-python
- langchain-ai/langgraph (agent_runtime): 34725 stars, 5826 forks, Python, license MIT, latest release 1.2.5 published 2026-06-12T20:31:14Z; pushed 2026-06-14T01:19:32Z. Role: stateful graph runtime for resilient manager/seeker flows and long-running review loops. Source: https://github.com/langchain-ai/langgraph
- pydantic/pydantic-ai (agent_runtime): 17753 stars, 2213 forks, Python, license MIT, latest release v1.107.0 published 2026-06-10T14:40:24Z; pushed 2026-06-14T18:19:40Z. Role: typed agent contracts, schemas, eval/test-model path for safe local workers. Source: https://github.com/pydantic/pydantic-ai
- microsoft/agent-framework (agent_runtime): 11335 stars, 1905 forks, Python, license MIT, latest release dotnet-1.10.0 published 2026-06-10T17:50:17Z; pushed 2026-06-14T06:27:56Z. Role: enterprise-style Python/.NET multi-agent workflows; useful signal for cross-language department workers. Source: https://github.com/microsoft/agent-framework
- microsoft/autogen (agent_runtime): 58948 stars, 8895 forks, Python, license CC-BY-4.0, latest release python-v0.7.5 published 2025-09-30T06:18:26Z; pushed 2026-04-15T11:59:09Z. Role: established multi-agent conversation framework; useful for research comparison, less favored for new control-plane dependency. Source: https://github.com/microsoft/autogen
- google/adk-python (agent_runtime): 20106 stars, 3563 forks, Python, license Apache-2.0, latest release v2.2.0 published 2026-06-04T22:13:43Z; pushed 2026-06-14T18:44:17Z. Role: code-first agent toolkit with evaluation/deployment framing; useful for manager and service-worker design patterns. Source: https://github.com/google/adk-python
- strands-agents/harness-sdk (agent_runtime): 6132 stars, 881 forks, Python, license Apache-2.0, latest release typescript/v1.5.0 published 2026-06-12T14:37:27Z; pushed 2026-06-13T00:14:58Z. Role: production harness framing; useful signal for end-to-end worker control, model/cloud portability, MCP integration. Source: https://github.com/strands-agents/harness-sdk
- run-llama/llama_index (agent_runtime_data): 50122 stars, 7560 forks, Python, license MIT, latest release v0.14.22 published 2026-05-14T20:22:24Z; pushed 2026-06-12T19:29:18Z. Role: document/data agent layer for research ingestion, source memory, RAG over ledgers and reports. Source: https://github.com/run-llama/llama_index
- crewAIInc/crewAI (agent_runtime): 53545 stars, 7498 forks, Python, license MIT, latest release 1.14.7 published 2026-06-11T17:13:46Z; pushed 2026-06-14T07:19:50Z. Role: role-playing collaborative agents; useful for department metaphors, less central than our ledger for governance. Source: https://github.com/crewAIInc/crewAI
- agno-agi/agno (agent_platform): 40681 stars, 5521 forks, Python, license Apache-2.0, latest release v2.6.14 published 2026-06-12T16:38:25Z; pushed 2026-06-14T18:50:45Z. Role: agent platform management framing; useful as product inspiration for agent registries and runtime surfaces. Source: https://github.com/agno-agi/agno
- mastra-ai/mastra (agent_runtime_ts): 25064 stars, 2229 forks, TypeScript, license Other, latest release @mastra/core@1.42.0 published 2026-06-12T14:48:23Z; pushed 2026-06-14T20:35:27Z. Role: TypeScript agent/workflow/eval stack; useful if browser/product workers move to Node services. Source: https://github.com/mastra-ai/mastra
- CopilotKit/CopilotKit (human_ui): 35080 stars, 4363 forks, TypeScript, license MIT, latest release v1.60.1 published 2026-06-12T13:48:02Z; pushed 2026-06-13T15:26:24Z. Role: frontend stack for human-in-the-loop agent operations and AG-UI-adjacent control room patterns. Source: https://github.com/CopilotKit/CopilotKit
- ag-ui-protocol/ag-ui (human_ui_protocol): 14261 stars, 1286 forks, Python, license MIT, latest release release/2026-06-12 published 2026-06-12T08:20:59Z; pushed 2026-06-13T18:00:52Z. Role: Agent-User Interaction protocol for streaming state/tool/human approval events into a control room. Source: https://github.com/ag-ui-protocol/ag-ui
- modelcontextprotocol/modelcontextprotocol (tool_protocol): 8399 stars, 1589 forks, TypeScript, license Other, latest release 2025-11-25 published 2025-11-25T21:17:42Z; pushed 2026-06-13T22:17:38Z. Role: tool/resource protocol; service desk adapters should expose approved local tools through MCP-like contracts. Source: https://github.com/modelcontextprotocol/modelcontextprotocol
- a2aproject/A2A (agent_protocol): 24283 stars, 2465 forks, Shell, license Apache-2.0, latest release v1.0.1 published 2026-05-28T11:34:36Z; pushed 2026-06-12T10:40:26Z. Role: agent-to-agent interoperability protocol; useful later for cross-thread/opaque worker contracts. Source: https://github.com/a2aproject/A2A
- browser-use/browser-use (browser_worker): 98813 stars, 11027 forks, Python, license MIT, latest release 0.13.2 published 2026-06-12T22:45:04Z; pushed 2026-06-13T21:08:02Z. Role: high-velocity browser automation worker candidate; must remain behind browser_read_only/service gates. Source: https://github.com/browser-use/browser-use
- Skyvern-AI/skyvern (browser_worker): 21908 stars, 2038 forks, Python, license AGPL-3.0, latest release v1.0.41 published 2026-06-11T21:37:23Z; pushed 2026-06-14T20:10:30Z. Role: workflow/RPA-style browser worker candidate; AGPL license requires care before embedding. Source: https://github.com/Skyvern-AI/skyvern
- microsoft/playwright-mcp (browser_worker_protocol): 33906 stars, 2804 forks, TypeScript, license Apache-2.0, latest release v0.0.76 published 2026-06-10T00:14:20Z; pushed 2026-06-10T00:14:20Z. Role: MCP server for browser operations; useful for read-only browser desk after explicit approval. Source: https://github.com/microsoft/playwright-mcp
- temporalio/temporal (durable_execution): 20967 stars, 1655 forks, Go, license MIT, latest release v1.29.7 published 2026-06-12T16:51:23Z; pushed 2026-06-14T12:46:42Z. Role: heavyweight durable workflow backbone when local SQLite/CLI needs distributed retries and worker fleets. Source: https://github.com/temporalio/temporal
- dbos-inc/dbos-transact-py (durable_execution): 1420 stars, 71 forks, Python, license MIT, latest release 2.23.0 published 2026-06-01T21:34:11Z; pushed 2026-06-13T03:14:55Z. Role: best near-term fit for Python/SQLite/Postgres durable workflows; aligns with current ledger-first architecture. Source: https://github.com/dbos-inc/dbos-transact-py
- hatchet-dev/hatchet (durable_execution_queue): 7345 stars, 416 forks, Go, license MIT, latest release v0.89.0 published 2026-06-10T11:07:59Z; pushed 2026-06-13T20:15:44Z. Role: background tasks, durable workflows, concurrency controls for service desks and lane worker queues. Source: https://github.com/hatchet-dev/hatchet
- inngest/inngest (durable_execution_evented): 5491 stars, 318 forks, Go, license Other, latest release v1.27.0 published 2026-06-09T23:22:48Z; pushed 2026-06-14T10:27:42Z. Role: stateful event functions; useful if we shift from CLI queue to event-driven service request handling. Source: https://github.com/inngest/inngest
- triggerdotdev/trigger.dev (durable_execution_ts): 15344 stars, 1303 forks, TypeScript, license Apache-2.0, latest release v4.4.6 published 2026-05-12T10:38:39Z; pushed 2026-06-14T20:07:13Z. Role: managed/self-hosted AI workflow pattern for productized workers; less immediate than DBOS/Hatchet for local lab. Source: https://github.com/triggerdotdev/trigger.dev
- PrefectHQ/prefect (workflow_data_ops): 22607 stars, 2335 forks, Python, license Apache-2.0, latest release 3.7.4 published 2026-06-05T17:23:31Z; pushed 2026-06-14T17:57:09Z. Role: data/research pipeline orchestrator; useful for source freshness and recurring scouts, not agent runtime. Source: https://github.com/PrefectHQ/prefect
- dagster-io/dagster (workflow_data_assets): 15685 stars, 2161 forks, Python, license Apache-2.0, latest release 1.13.9 published 2026-06-11T19:16:52Z; pushed 2026-06-12T19:19:16Z. Role: asset lineage/data pipeline option for research corpora and generated datasets. Source: https://github.com/dagster-io/dagster
- nats-io/nats-server (messaging): 20023 stars, 1836 forks, Go, license Apache-2.0, latest release v2.14.2 published 2026-06-02T16:02:48Z; pushed 2026-06-12T16:08:38Z. Role: later-stage event bus for many workers; not needed before DB queue saturation. Source: https://github.com/nats-io/nats-server
- langfuse/langfuse (observability_eval): 29065 stars, 3011 forks, TypeScript, license Other, latest release v3.185.0 published 2026-06-12T11:48:13Z; pushed 2026-06-13T21:33:32Z. Role: LLM observability, evals, prompt management; useful as external reference while local trace_events remains source of truth. Source: https://github.com/langfuse/langfuse
- Arize-ai/phoenix (observability_eval): 10131 stars, 923 forks, Python, license Other, latest release arize-phoenix-v17.5.0 published 2026-06-12T21:52:28Z; pushed 2026-06-14T20:56:21Z. Role: AI observability/evaluation workbench; good candidate for trace/eval export target. Source: https://github.com/Arize-ai/phoenix
- Arize-ai/openinference (observability_protocol): 1024 stars, 258 forks, Python, license Apache-2.0, latest release python-openinference-instrumentation-strands-agents-v0.1.3 published 2026-06-11T17:12:19Z; pushed 2026-06-11T18:03:18Z. Role: OpenTelemetry instrumentation vocabulary for agent/tool/model spans; should shape local trace schema exports. Source: https://github.com/Arize-ai/openinference

## Architecture Implications

### 1. Runtime Layer

OpenAI Agents, LangGraph, Pydantic AI, Google ADK, Microsoft Agent Framework, Strands, CrewAI, Agno, Mastra, AutoGen, and LlamaIndex are all active enough to matter. The mistake would be choosing one as the root system. The right move is to keep work_packet.v1 and service requests as the root contract, then let each lane use the adapter that fits its work.

Near-term runtime stance:

- Keep Pydantic AI/TestModel for deterministic local contract checks.
- Keep LangGraph as the best fit for explicit state machines and resilient manager loops.
- Keep OpenAI Agents as the clean model/tool/handoff adapter when model API execution is explicitly approved.
- Keep LlamaIndex for source ingestion and local evidence memory, not as the CEO system.
- Treat CrewAI/Agno/Microsoft/Google/Strands/Mastra as pattern libraries until a specific lane proves they outperform current adapters.

### 2. Service Desk Layer

The user explicitly described workers that do registration, wallet, browser, and other risky actions for agents. That must be a typed service layer, not a hidden tool call. Browser Use, Skyvern, and Playwright MCP show that the browser-worker ecosystem is mature and moving fast, but the lab should only invoke them through approved service requests.

Required service desks:

- browser_read_only_session: public non-signed-in browsing, screenshots/evidence only.
- account_registration_gate: no signup or credentials without explicit user approval and platform terms review.
- wallet_gate: no wallet creation, import, signing, funding, transaction, or token claim without explicit approval.
- legal_kyc_tax_payment_gate: no commitments; only review packets until user decides.
- public_submission_gate: no PR comments, issue comments, marketplace listings, reports, or public posts without approval.
- model_api_execution_gate: no provider-cost or external model calls unless scoped and approved.

### 3. Durable Execution Layer

The current CLI plus SQLite queue is still the right Phase 0/1 control plane. The next upgrade should not be Kubernetes-shaped complexity. It should be a narrow durable adapter spike: run one existing local work_packet.v1 through DBOS and Hatchet-shaped manifests, compare retries, idempotency, result artifacts, and failure records. Temporal is excellent but should wait until we have true distributed worker pressure.

### 4. Human Control Room

AG-UI and CopilotKit point to the missing product surface: a control room that streams what agents are doing, which tools they requested, what approvals are blocked, what evidence was produced, and which lane is closest to money. The current markdown dashboards are good audit artifacts; the UI should eventually be event-driven and approval-first.

### 5. Observability

Langfuse, Phoenix, and OpenInference suggest that traces should be model/tool/span-shaped. The lab already has trace_events. The next step is not sending telemetry externally; it is a local mapping: trace_id, event_id, lane_id, task_id, agent_id, service_request_id, tool_name, input_artifact, output_artifact, external_side_effects, risk_gate, approval_id, status, cost_usd, realized_usd.

## Ranking For Our Lab

| Rank | Component | Promote Now? | Reason |
|---:|---|---|---|
| 1 | service_worker_request.v1 | Yes | Directly implements the user-requested company service-worker model and closes safety gaps. |
| 2 | OpenInference trace export plan | Yes | Makes current traces interoperable without external telemetry. |
| 3 | DBOS durable adapter spike | Yes | Best near-term match for Python/database-backed durable local work. |
| 4 | Hatchet queue comparison | Yes, after DBOS | Better service desk queue/concurrency model, but more moving parts. |
| 5 | AG-UI/CopilotKit control-room prototype | Soon | Needed for human approvals once service requests grow. |
| 6 | Temporal | Later | Strong, but heavy before distributed production worker fleets. |
| 7 | NATS | Later | Useful event bus only after DB queue pressure appears. |

## Next Concrete Build

Build service_worker_request.v1 as the next local artifact. It should include: request_id, requesting_lane_id, requesting_agent_id, worker_type, service_id, risk_gate, approval_scope, prohibited_actions, allowed_actions, credentials_boundary, account_boundary, money_boundary, external_side_effects_allowed, max_cost_usd, input_artifacts, expected_output_artifacts, execution_plan_path, result_artifact_path, status, created_at, decided_at, started_at, completed_at, and replay_policy.

Then backfill the existing browser/legal/model service requests into that format so lane managers can ask for service workers without receiving direct unsafe powers.

## Sources

- openai/openai-agents-python: https://github.com/openai/openai-agents-python
- langchain-ai/langgraph: https://github.com/langchain-ai/langgraph
- pydantic/pydantic-ai: https://github.com/pydantic/pydantic-ai
- microsoft/agent-framework: https://github.com/microsoft/agent-framework
- microsoft/autogen: https://github.com/microsoft/autogen
- google/adk-python: https://github.com/google/adk-python
- strands-agents/harness-sdk: https://github.com/strands-agents/harness-sdk
- run-llama/llama_index: https://github.com/run-llama/llama_index
- crewAIInc/crewAI: https://github.com/crewAIInc/crewAI
- agno-agi/agno: https://github.com/agno-agi/agno
- mastra-ai/mastra: https://github.com/mastra-ai/mastra
- CopilotKit/CopilotKit: https://github.com/CopilotKit/CopilotKit
- ag-ui-protocol/ag-ui: https://github.com/ag-ui-protocol/ag-ui
- modelcontextprotocol/modelcontextprotocol: https://github.com/modelcontextprotocol/modelcontextprotocol
- a2aproject/A2A: https://github.com/a2aproject/A2A
- browser-use/browser-use: https://github.com/browser-use/browser-use
- Skyvern-AI/skyvern: https://github.com/Skyvern-AI/skyvern
- microsoft/playwright-mcp: https://github.com/microsoft/playwright-mcp
- temporalio/temporal: https://github.com/temporalio/temporal
- dbos-inc/dbos-transact-py: https://github.com/dbos-inc/dbos-transact-py
- hatchet-dev/hatchet: https://github.com/hatchet-dev/hatchet
- inngest/inngest: https://github.com/inngest/inngest
- triggerdotdev/trigger.dev: https://github.com/triggerdotdev/trigger.dev
- PrefectHQ/prefect: https://github.com/PrefectHQ/prefect
- dagster-io/dagster: https://github.com/dagster-io/dagster
- nats-io/nats-server: https://github.com/nats-io/nats-server
- langfuse/langfuse: https://github.com/langfuse/langfuse
- Arize-ai/phoenix: https://github.com/Arize-ai/phoenix
- Arize-ai/openinference: https://github.com/Arize-ai/openinference
