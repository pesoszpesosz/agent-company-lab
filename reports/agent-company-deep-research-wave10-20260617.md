# Agent Company Deep Research Wave 10

Generated UTC: 2026-06-17T00:00:00Z
Task: `task-agent-company-deep-research-wave10-20260617`
Lane: `platform_engineering`
Owner: `recovered-profitable-edge-infra`
Dataset: `E:\agent-company-lab\data\curated-infra-repos-wave10-20260617.json`
CSV: `E:\agent-company-lab\data\curated-infra-repos-wave10-20260617.csv`
Decision matrix: `E:\agent-company-lab\reports\agent-company-wave10-decision-matrix-20260617.json`

## Purpose

Refresh the Agent Company infrastructure radar with current primary-source signals from GitHub, official docs, and official project pages. This wave does not install dependencies, start runtimes, open browser sessions, call model APIs, register accounts, approve service requests, or perform external side effects.

## Source Set

Primary source URLs used:

- https://github.com/langchain-ai/langgraph
- https://docs.langchain.com/oss/python/langgraph/overview
- https://github.com/microsoft/autogen
- https://github.com/pydantic/pydantic-ai
- https://pydantic.dev/docs/ai/integrations/durable_execution/overview/
- https://developers.openai.com/api/docs/libraries#use-the-agents-sdk
- https://github.com/openai/openai-agents-python
- https://github.com/openai/openai-agents-js
- https://github.com/crewAIInc/crewAI
- https://github.com/browser-use/browser-use
- https://github.com/browser-use/browser-harness
- https://www.inngest.com/docs
- https://github.com/inngest/inngest
- https://github.com/dbos-inc/dbos-transact-py
- https://github.com/dbos-inc/dbos-transact-ts
- https://github.com/dbos-inc/dbos-openai-agents
- https://docs.temporal.io/ai-cookbook/human-in-the-loop-python
- https://github.com/temporalio/sdk-python
- https://github.com/humanlayer/humanlayer
- https://github.com/a2aproject/A2A
- https://github.com/a2aproject/a2a-python
- https://github.com/modelcontextprotocol/python-sdk
- https://github.com/langfuse/langfuse
- https://github.com/Arize-ai/phoenix

The GitHub dataset was collected through public GitHub repository metadata only. It stores star count, forks, open issue count, pushed/updated timestamps, license, language, topics, and source API URL.

## Current Signals

Top adoption and activity signals in the collected GitHub metadata:

| Repo | Category | Stars | Last Push | Local Decision |
| --- | --- | ---: | --- | --- |
| `browser-use/browser-use` | Browser worker | 99,149 | 2026-06-15 | Candidate only behind strict browser service gates. |
| `microsoft/autogen` | Agent runtime | 59,010 | 2026-04-15 | Watch/deprioritize because current public repo signal says maintenance mode. |
| `crewAIInc/crewAI` | Agent runtime | 53,717 | 2026-06-16 | Watchlist; do not expand role-play orchestration before durable gates. |
| `langchain-ai/langgraph` | Agent runtime | 34,945 | 2026-06-16 | Good adapter candidate for stateful graphs, after local outbox/history. |
| `langfuse/langfuse` | Observability | 29,213 | 2026-06-16 | Strong eval/trace candidate, but needs trace export contract first. |
| `openai/openai-agents-python` | Agent runtime | 27,198 | 2026-06-13 | Good gated adapter for tools, handoffs, guardrails, tracing. |
| `a2aproject/A2A` | Interoperability | 24,315 | 2026-06-12 | Protocol watch; useful after local agent communication contract. |
| `modelcontextprotocol/python-sdk` | Interoperability | 23,343 | 2026-06-16 | Promote as tool/context boundary, not as the whole company bus. |
| `pydantic/pydantic-ai` | Agent runtime | 17,795 | 2026-06-16 | Keep as typed local adapter and durable-exec reference. |
| `browser-use/browser-harness` | Browser worker | 14,950 | 2026-06-13 | Research candidate; isolate behind browser safety fixtures. |
| `Arize-ai/phoenix` | Observability | 10,166 | 2026-06-16 | Strong observability/eval candidate after OpenTelemetry export contract. |
| `inngest/inngest` | Durable execution | 5,499 | 2026-06-16 | Adapter candidate for durable steps, concurrency, throttling, and observability. |

## Architecture Takeaways

### 1. Durable execution is now the main missing layer

Pydantic AI's official durable execution docs list Temporal, DBOS, Prefect, and Restate as officially supported durable execution integrations. Temporal's human-in-the-loop cookbook emphasizes signal-based approval, resource-efficient waiting, durable timers, and audit trails. Inngest documents an event-driven durable platform with built-in queueing, scaling, concurrency, throttling, rate limiting, and observability.

Decision: do not import any durable runtime yet. Build a local adapter comparison matrix and a replayable outbox/history model first, then test one runtime behind the existing service-worker gates.

### 2. Browser workers are high-value and high-risk

Browser Use has the strongest adoption signal in this scan, and Browser Harness is a fresh low-level browser-control candidate. But browser workers are exactly where accounts, public actions, private sessions, and reputation risk can leak.

Decision: create a local browser-worker safety fixture before any browser worker route. The fixture should classify actions as public read-only, signed-in read-only, public-action, account/profile, payment, credential, or prohibited.

### 3. Agent runtime wrappers are not the bottleneck

LangGraph, Pydantic AI, OpenAI Agents SDK, CrewAI, and AutoGen all offer useful agent abstractions. OpenAI's docs position the Agents SDK for code-first orchestration with agents, tools, handoffs, guardrails, tracing, and sandbox execution. LangGraph's docs position it as a low-level runtime for long-running, stateful agents. CrewAI has large community attention. AutoGen has a large historical signal but is no longer the preferred foundation for new core work because of its maintenance-mode signal.

Decision: treat frameworks as adapters, not the company brain. The company brain remains the SQLite control plane, task/evidence ledger, service-worker gate map, and future outbox/history.

### 4. Interoperability should stay tool-first before agent-to-agent endpoints

A2A is the right protocol watch for independent agent systems communicating across vendors/frameworks. MCP remains the more immediate tool/context boundary for local and external capabilities.

Decision: continue using MCP-style boundaries for tools and service workers. Add A2A only after local agent communication messages are stable and replayable.

### 5. Observability needs an export contract first

Langfuse and Phoenix are both strong observability candidates. The lab already has trace events, artifacts, outcomes, and OpenInference-style metadata conventions. The missing piece is an export contract that says exactly which local spans/events become external traces and which fields are redacted.

Decision: build `trace_export_contract_v1` locally before trying Langfuse, Phoenix, OpenTelemetry, or any hosted trace backend.

## Updated Stack Decision

Keep:

- SQLite as the CEO ledger and source of truth.
- Local artifacts as durable proof.
- Service-worker request packets as the hard boundary for account, wallet, public, browser, legal, payment, model/API, security-report, and real-money actions.
- Python standard-library proof tools for first-pass local validation.

Add next:

1. Central outbox/history schema for agent communication.
2. Trace export contract for Langfuse/Phoenix/OpenTelemetry candidates.
3. Durable runtime adapter matrix v2 covering Temporal, Inngest, DBOS, Pydantic durable execution, Prefect, and Restate.
4. Browser worker safety fixture for Browser Use / Browser Harness style agents.

Hold:

- Live model/API-backed OpenAI Agents SDK work until the model/API service request is approved.
- Browser Use or Browser Harness execution until browser worker safety fixtures and exact read-only/public-action approvals exist.
- Temporal/Inngest/DBOS runtime imports until local adapter matrix v2 is written.
- A2A endpoint work until local outbox/history is stable.

## Follow-Up Task Candidates

| Candidate | Lane | Proof Artifact | Side-Effect Boundary |
| --- | --- | --- | --- |
| `task-agent-company-central-outbox-history-v1-20260617` | `platform_engineering` | `reports/agent-company-central-outbox-history-v1-20260617.md/json` | Local schema and fixture only. |
| `task-trace-export-contract-v1-20260617` | `platform_engineering` | `reports/trace-export-contract-v1-20260617.md/json` | No external trace backend or API calls. |
| `task-durable-runtime-adapter-matrix-v2-20260617` | `platform_engineering` | `reports/durable-orchestration/durable-runtime-adapter-matrix-v2-20260617.md/json` | No dependency install, import, runtime start, queue enqueue, or service update. |
| `task-browser-worker-safety-fixture-v1-20260617` | `platform_engineering` | `reports/browser-worker-safety-fixture-v1-20260617.md/json` | No browser opened, no account, no public action. |

## Decision

Wave 10 reinforces the current architectural direction: the lab should not jump straight to a bigger agent framework. It should first make agent communication replayable, make traces exportable, compare durable execution adapters against the existing service gates, and add browser-worker safety fixtures.

The next local build should be `central_outbox_history_v1`, because agent managers and service workers need a replayable communication surface before external orchestration frameworks can safely take over scheduling.

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- Security testing actions: `false`
- Real-money actions: `false`
- Model/API calls: `false`
- Dependency installs/imports: `false`
- Runtime starts: `0`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
