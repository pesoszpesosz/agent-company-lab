# Agent Company Stack Wave 5

Generated: 2026-06-14
Lane owner: `platform_engineering`
Scope: source-backed platform scan for the next infrastructure layer of the agent-company lab.

This report is local-only. It performs no account registration, browser automation, model/API execution, wallet action, trade, public post, PR, bounty claim, or submission.

## Executive Recommendation

Keep `E:\agent-company-lab` as a control-plane-first system:

1. Preserve SQLite as the source of truth for lanes, tasks, service requests, approvals, artifacts, outcomes, and traces.
2. Add frameworks as adapters around the control plane, not as the control plane.
3. Prioritize local evaluability over autonomy: every runtime must prove it can consume a lane packet, respect stop gates, emit structured artifacts, and refuse side effects without approved service requests.
4. Treat browser agents, model-backed agents, public actions, wallets, payment setup, and external submissions as service departments behind review packets.
5. Use MCP as the first tool/service boundary; defer A2A until we have multiple independently-running agent applications that need cross-runtime negotiation.

## Fresh Source Scan

| Project | Current signal observed 2026-06-14 | What it is best for | Adoption / recency signal |
| --- | --- | --- | --- |
| OpenAI Agents SDK | Lightweight framework for multi-agent workflows, with agents, handoffs/tools, guardrails, human-in-the-loop, sessions, tracing, and sandbox agents. | Future model-backed runtime adapter and sandboxed workspace workers. | GitHub shows 27.1k stars, latest release `v0.17.5` on 2026-06-11. Source: https://github.com/openai/openai-agents-python |
| Pydantic AI | Type-safe Python agent framework with model-agnostic providers, evals, observability hooks, structured outputs, MCP/A2A/UI references, human-in-the-loop tool approval, and durable execution claims. | Best immediate fit for our already-Pydantic local worker runtime and service-request schema validation. | GitHub shows 17.7k stars, latest release `v1.107.0` on 2026-06-10. Source: https://github.com/pydantic/pydantic-ai |
| LangGraph | Resilient agent graphs inspired by Pregel and Apache Beam; can be used without LangChain. | Explicit graph/workflow plans for seekers, managers, reviewers, and escalation paths. | GitHub shows 34.7k stars, latest `langgraph==1.2.5` on 2026-06-12. Source: https://github.com/langchain-ai/langgraph |
| CrewAI | Role/task-oriented multi-agent crews with YAML-like agent/task configuration and sequential processes. | Useful mental model for role registry and manager packets; less attractive as the core ledger. | GitHub shows 53.5k stars, latest `1.14.7` on 2026-06-11. Source: https://github.com/crewAIInc/crewAI |
| Microsoft AutoGen | Mature multi-agent framework; README points new projects toward Microsoft Agent Framework for long-term support. | Reference for agent-to-agent orchestration patterns and MCP warning discipline; not the first new implementation target. | GitHub shows 58.9k stars, latest Python release `python-v0.7.5` on 2025-09-30. Source: https://github.com/microsoft/autogen |
| Google ADK Python | Code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents; current 2.x line has breaking changes from 1.x. | Watchlist for Google/Gemini-heavy agents and eval/deploy patterns; avoid immediate adoption until API churn is digested. | GitHub shows 20.1k stars, latest `v2.2.0` on 2026-06-04. Source: https://github.com/google/adk-python |
| LlamaIndex | Document agent and OCR platform; strong for document/RAG/indexing-heavy workloads. | Specialized research-memory and source-indexing department, not general company orchestration. | GitHub shows 50.1k stars, latest `v0.14.22` on 2026-05-14. Source: https://github.com/run-llama/llama_index |
| Strands Agents / Harness SDK | Production agent harness in Python/TypeScript, any model/cloud. | Watchlist for harness patterns; not yet better than our current local packet contract. | GitHub shows 6.1k stars, latest `typescript/v1.5.0` on 2026-06-12. Source: https://github.com/strands-agents/harness-sdk |
| MCP | Specification, schema, and docs for the Model Context Protocol. | First-class boundary between company agents and tools/services. | GitHub shows 8.4k stars, latest spec release `2025-11-25`. Source: https://github.com/modelcontextprotocol/modelcontextprotocol |
| A2A | Open protocol for communication and interoperability between opaque agentic applications; supports discovery, modality negotiation, long-running tasks, and collaboration without exposing internal state/tools. | Later inter-company/inter-runtime federation layer. | GitHub shows 24.3k stars, latest `v1.0.1` on 2026-05-28. Source: https://github.com/a2aproject/A2A |
| Temporal | Durable workflow service and orchestration engine. | Production-grade service workflow engine once service requests become long-running and failure-prone. | GitHub shows 21k stars, latest `v1.29.7` on 2026-06-12. Source: https://github.com/temporalio/temporal |
| DBOS Transact Python | Database-backed durable Python workflows. | Smaller Python-native durable step before Temporal if we want durability without a large service deployment. | GitHub shows 1.4k stars, latest `2.23.0` on 2026-06-01. Source: https://github.com/dbos-inc/dbos-transact-py |
| Browser Use | Browser automation for AI agents; current README highlights Rust core/browser harness, persistent tools, and recovery loops. | Gated browser worker implementation candidate for read-only market/source checks. | GitHub shows 98.8k stars, latest `0.13.2` on 2026-06-12. Source: https://github.com/browser-use/browser-use |
| Langfuse | Open-source LLM engineering platform with observability, prompt management, evals, datasets, playground, API, and integrations. | Best self-hostable candidate for trace/eval/prompt operations after local traces prove value. | GitHub shows 29.1k stars, latest `v3.185.0` on 2026-06-12. Source: https://github.com/langfuse/langfuse |
| Phoenix | AI observability and evaluation platform. | Alternative observability/evals candidate; license posture requires review before embedding deeply. | GitHub shows 10.1k stars, latest `arize-phoenix v17.5.0` on 2026-06-12. Source: https://github.com/Arize-ai/phoenix |
| HumanLayer / CodeLayer | Open-source IDE/workflow system for orchestrating coding agents on complex codebases. | Useful reference for multi-agent coding workspace UX, but not directly a money-lane control plane. | GitHub shows 11k stars, latest `codelayer-0.20.0` on 2025-12-23. Source: https://github.com/humanlayer/humanlayer |

## Architecture Implications

The winning design is not "pick one agent framework." It is a layered company architecture:

1. Company ledger
   - Current: SQLite tables in `state/agent_company.sqlite`.
   - Later: Postgres if concurrency grows beyond local Codex-thread coordination.
   - Non-negotiable contract: every task, approval, service request, artifact, outcome, and trace lands in the ledger.

2. Work packet format
   - Current: manager packets, service-request packet factory, local proof tasks, outcome rows.
   - Next: define a runtime-agnostic `work_packet.v1` JSON schema for lane task execution.
   - Why: Pydantic AI, OpenAI Agents SDK, LangGraph, CrewAI, ADK, and future A2A agents should consume the same packet contract.

3. Runtime adapters
   - Immediate local runtime: Pydantic-only typed worker plus Pydantic AI dry-run/test model.
   - Next local adapter: OpenAI Agents SDK adapter in dry-run/sandbox-manifest mode, but no model/API run until `model_api_execution` service approval.
   - Graph adapter: LangGraph only after we have a repeated workflow that actually needs graph semantics.
   - Role/crew adapter: CrewAI as a config-template reference, not a source of truth.

4. Durable service workflows
   - Current: service requests are DB rows with manual state changes.
   - Next small step: implement idempotent state-transition checks and retry-safe service request packets locally.
   - Later: DBOS for Python-native durable workflow experiments or Temporal for production-grade, cross-language service workflows.

5. Tool and agent interoperability
   - MCP first: clean boundary for read-only GitHub, web search, browser, local DB, report writer, and future registered services.
   - A2A later: only once we have distinct agent applications that need discovery and long-running cross-agent collaboration.

6. Browser/action bureau
   - Browser Use is the strongest current open-source signal for browser agents by stars and release activity.
   - It must remain behind `browser_read_only_session` or stricter service requests.
   - Required controls: allowed domains, headless/visible mode choice, no login/OTP/account setting changes, no form submission unless request type explicitly allows it.

7. Observability/evals
   - Current: local `trace_events`, prompt eval registry, artifacts report.
   - Near-term: extend local trace metadata to map cleanly onto OpenTelemetry-style fields.
   - Later: self-host Langfuse before Phoenix if we want prompt/dataset/eval/tracing all in one open-source stack; run Phoenix as an alternative only after license review.

## Stack Shortlist For This Lab

### Tier 0: Keep Already Working

- SQLite control plane.
- `agent_company.py` CLI.
- Manager packets.
- Service-request packet factory.
- Local proof tasks and proof monitors.
- Trace/artifact/outcome reports.

Reason: this already gave us 10 lane managers, 14 service requests, 61 completed tasks, 144 artifacts, and 77 trace events without accidentally doing external actions.

### Tier 1: Build Next

- `work_packet.v1` schema.
- `runtime_adapter_results` table or artifact type.
- Adapter comparison harness that runs the same synthetic packet through:
  - current typed worker runtime,
  - Pydantic AI TestModel/dry-run,
  - OpenAI Agents SDK no-model/sandbox-adapter stub,
  - LangGraph static graph stub.
- Score every adapter on:
  - gate compliance,
  - schema validity,
  - artifact quality,
  - trace completeness,
  - local determinism,
  - effort to integrate.

### Tier 2: Add After Local Harness Passes

- DBOS or Temporal experiment for service-request lifecycle durability.
- MCP server around read-only lab commands and source registry.
- Browser Use read-only worker behind an approved service request.
- Langfuse self-host or local OpenTelemetry export after traces become too hard to inspect in Markdown.

### Tier 3: Watchlist

- A2A federation for independently-running agent apps.
- Google ADK for Google-native manager experiments.
- CrewAI role/task config generator if we want import/export compatibility with crew-like agent teams.
- LlamaIndex for source memory, document extraction, and lane evidence retrieval.
- Strands/Harness SDK for production agent harness ideas.
- HumanLayer/CodeLayer for multi-agent coding UX ideas.

## Safety Gates For Every Candidate

Every new framework adapter must prove these before it can touch a real online money lane:

1. Can run a synthetic task without network/model/API/browser/account side effects.
2. Can refuse a packet that requests real-money action without approval.
3. Can preserve lane ownership and avoid `submitted_bounty_payouts`.
4. Can emit a complete artifact path, outcome status, realized USD, and trace event.
5. Can distinguish "prepared" from "submitted" or "paid".
6. Can fail closed if credentials, wallet, KYC, legal, payment, or public-action scopes appear.

## Concrete Next Local Task

Create `task-work-packet-runtime-adapter-harness-20260614`:

- Write `architecture/work-packet-v1.schema.json`.
- Write `tools/runtime_adapter_harness.py`.
- Include four local adapters:
  - `typed_worker_runtime_stub`
  - `pydantic_ai_testmodel_stub`
  - `openai_agents_sandbox_stub`
  - `langgraph_static_stub`
- Run three synthetic packets:
  - safe local research synthesis,
  - browser-read-only request that must stop without approved service request,
  - real-money/public-action request that must refuse.
- Output:
  - `reports/runtime-adapter-harness-20260614.md`
  - `reports/runtime-adapter-harness-20260614.json`
- Record artifact/outcome/trace rows.

This is materially different from the parallel GitHub payout lane. It improves the agent-company operating system that will later assign separate workers to many money paths.
