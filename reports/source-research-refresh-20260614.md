# Agent Company Source Research Refresh

Generated UTC: 2026-06-14T11:13:00Z

Purpose: extend the infrastructure research with current official docs, GitHub metadata, and implementation decisions for the agent-company system. This report is platform-engineering research only; it does not assign or execute any money lane.

## New Data Artifacts

- `E:\agent-company-lab\data\curated-infra-repos-refresh-20260614.json`
- `E:\agent-company-lab\data\curated-infra-repos-refresh-20260614.csv`

## Current GitHub Metadata Snapshot

Captured with `gh repo view` on 2026-06-14.

| Repo | Stars | Forks | Latest Release | Updated UTC | Role In This System |
| --- | ---: | ---: | --- | --- | --- |
| `ray-project/ray` | 42,867 | 7,683 | `ray-2.55.1`, 2026-04-22 | 2026-06-14T11:09:36Z | Distributed compute later, not Phase 0. |
| `vercel-labs/agent-browser` | 36,024 | 2,275 | `v0.27.3`, 2026-06-12 | 2026-06-14T11:07:39Z | Candidate browser service worker. |
| `langfuse/langfuse` | 29,040 | 3,010 | `v3.185.0`, 2026-06-12 | 2026-06-14T10:43:09Z | Candidate LLM observability, prompts, evals, cost. |
| `PrefectHQ/prefect` | 22,602 | 2,335 | `3.7.4`, 2026-06-05 | 2026-06-14T08:01:18Z | Candidate Python dynamic workflow engine. |
| `pydantic/pydantic-ai` | 17,747 | 2,215 | `v1.107.0`, 2026-06-10 | 2026-06-14T10:50:18Z | Candidate typed Python agent layer. |
| `dagster-io/dagster` | 15,682 | 2,160 | `1.13.9`, 2026-06-11 | 2026-06-14T09:01:22Z | Candidate data asset orchestration later. |
| `microsoft/agent-framework` | 11,324 | 1,900 | `dotnet-1.10.0`, 2026-06-10 | 2026-06-14T10:50:44Z | Candidate enterprise agent/workflow layer. |
| `Arize-ai/phoenix` | 10,130 | 922 | `arize-phoenix-v17.5.0`, 2026-06-12 | 2026-06-14T10:08:23Z | Candidate OTel/OpenInference observability. |
| `vercel-labs/open-agents` | 5,635 | 737 | none | 2026-06-14T08:32:57Z | Cloud-agent template reference only. |
| `Arize-ai/openinference` | 1,024 | 258 | `python-openinference-instrumentation-strands-agents-v0.1.3`, 2026-06-11 | 2026-06-14T09:52:59Z | Trace semantic conventions/instrumentation. |

## Source Findings

### Microsoft Agent Framework

Microsoft Agent Framework is worth tracking because it explicitly merges the AutoGen/Semantic Kernel lineage into a production-focused .NET/Python framework. The official overview describes two categories: agents, and graph workflows that connect agents/functions with type-safe routing, checkpointing, and human-in-the-loop support. The same page says Agent Framework is the direct successor to AutoGen and Semantic Kernel concepts and adds workflow control plus long-running state management.

Implication: do not start new greenfield platform work on old AutoGen unless compatibility with existing AutoGen code is required. If the user later wants a Microsoft/Azure-shaped production path, evaluate Agent Framework as a typed orchestration layer. For the current local lab, keep the control plane framework-neutral so Agent Framework can be a worker runtime, not the system of record.

Sources:

- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://github.com/microsoft/agent-framework

### Pydantic AI

Pydantic AI is one of the strongest Python candidates for our future worker runtime because its docs emphasize type safety, dependency injection, model/provider flexibility, MCP/A2A/UI standards, human-in-the-loop tool approval, durable execution, streamed structured outputs, and graph support. Its Temporal integration docs also show the right separation: deterministic workflows for replayable control flow and non-deterministic activities for I/O/tool/model work.

Implication: if we build actual worker agents inside this lab, Pydantic AI fits the current Python/SQLite system better than most role-play frameworks. Use it for typed agent wrappers, approval-gated tools, and structured outputs. Do not let it replace the lane registry or artifact ledger.

Sources:

- https://pydantic.dev/docs/ai/overview/
- https://pydantic.dev/docs/ai/integrations/durable_execution/temporal/
- https://github.com/pydantic/pydantic-ai

### CrewAI

CrewAI remains useful as a role/crew/flow framework. Its docs emphasize agents with tools, memory, knowledge, structured outputs, flows that manage state/persistence/resume, and processes with guardrails, callbacks, and human-in-the-loop triggers.

Implication: CrewAI may be a fast prototyping layer for department-style roles, but it should not be the first platform control plane. Our needs are stricter: lane ownership, service gates, read-only imports, artifacts, and anti-duplication matter more than agent persona composition.

Sources:

- https://docs.crewai.com/
- https://github.com/crewAIInc/crewAI

### Workflow Engines

Temporal is the strongest candidate for durable side-effect workflows once the schema stabilizes. Pydantic's Temporal docs make the key design boundary explicit: workflow code is deterministic and replayable; activity code is where I/O, model calls, API calls, and other non-deterministic work belongs.

Prefect is a good candidate for dynamic Python-first state machines. Its agent page argues that agents do not follow fixed DAGs, and that Prefect follows Python control flow, including loops, runtime branching, and human approvals.

Dagster is a better fit for source-ingestion/data-asset reliability than for agent reasoning. Its docs frame it around assets, lineage, observability, declarative programming, and testability.

Ray is not a control plane. It becomes relevant only when many workers need distributed compute, batch inference, or large parallel source ingestion.

Implication: keep SQLite for Phase 0. Add Prefect first if we need dynamic local workflows. Add Temporal when approval wait/resume, account-service requests, browser-service jobs, and payout/service workflows need durable retry/resume. Use Dagster for data ingestion once lane sources become data assets. Use Ray only after local concurrency becomes the bottleneck.

Sources:

- https://temporal.io/
- https://pydantic.dev/docs/ai/integrations/durable_execution/temporal/
- https://www.prefect.io/solutions/agents
- https://docs.dagster.io/
- https://www.ray.io/
- https://github.com/ray-project/ray

### Browser Workers

Browser automation must stay a service department, not a general seeker tool. `agent-browser` is attractive because it is a Rust CLI with compact text output, accessibility-tree refs for deterministic selection, sessions/profiles/auth state, screenshots, network/storage/files/tabs/frame commands, video/debug/profiler/diffing, and cross-platform binaries. Browser-use remains a high-visibility candidate and now markets a Python API backed by Rust core/browser harness.

Implication: implement browser work as service requests with exact URL, intended action, allowed selectors, stop conditions, screenshot/DOM proof, and side-effect classification. For logged-in X/Grok, account registration, wallet, or bounty submission flows, the browser worker must stop before public actions or account/legal/payment gates unless the user has explicitly approved that exact action.

Sources:

- https://agent-browser.dev/
- https://github.com/vercel-labs/agent-browser
- https://browser-use.com/
- https://github.com/browser-use/browser-use

### Observability

Langfuse is the stronger product-like observability candidate if we want LLM-native traces, sessions, environments, cost/token tracking, prompt management, experiments, datasets, and self-hosting. Phoenix/OpenInference is the stronger OpenTelemetry-first path; Phoenix docs show helper abstractions for instrumenting functions, chains, agents, tools, and LLMs with OpenInference/OpenTelemetry.

Implication: Phase 0 can stay with SQLite events and artifacts. Phase 1 should add a local `trace_events` table compatible with OpenTelemetry-ish fields. If the lab needs UI/debugging quickly, try Phoenix first. If prompt/version/eval/cost operations dominate, try Langfuse.

Sources:

- https://langfuse.com/docs/observability/overview
- https://langfuse.com/docs
- https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/instrument
- https://github.com/Arize-ai/phoenix
- https://github.com/Arize-ai/openinference

## Architecture Decision Update

Recommended stack order for `E:\agent-company-lab`:

1. Keep the existing SQLite control plane as the durable source of truth.
2. Add service-request lifecycle commands before adding any agent framework.
3. Add source-ingestion specs per lane so refreshers cannot cross ownership boundaries.
4. Add a local trace/event table before adding Langfuse or Phoenix.
5. Add Pydantic AI as the first Python worker runtime candidate for typed agents and approval-gated tools.
6. Add Prefect or Temporal only when workflows need durable waiting, retries, or human approval beyond what simple CLI commands handle.
7. Keep `agent-browser`/browser-use behind a browser service worker with explicit gate rules.
8. Treat Agent Framework, CrewAI, Ray, Dagster, and low-code platforms as specialized runtimes or references, not the control plane itself.

## Concrete Next Build Items

1. `service-request` lifecycle: approve, reject, start, attach artifact, complete.
2. `source-spec` registry: per-lane source definitions, refresh cadence, required gates, output paths.
3. `write-manager-packets`: one packet per department using evidence and CEO review, with claim/acquire instructions.
4. `trace_events` table: agent_id, task_id, lane_id, span_kind, tool_name, model, token/cost fields, artifact link, timestamps.
5. `browser_action_packet` schema: exact URL, action, account context, public side-effect class, proof requirements, stop condition.

## Current Non-Use Of Grok/X

No Grok/X browser prompt was run in this refresh. The local skill exists, but environment keys were missing earlier (`XAI_API_KEY=missing`, `X_BEARER_TOKEN=missing`), and browser-Grok is a service-request-gated path because it touches a logged-in web account. Keep `req-grok-research-worker-20260614` as a queued read-only research request until the browser route is explicitly scheduled.
