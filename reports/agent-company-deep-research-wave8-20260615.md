# Agent Company Deep Research Wave 8

Generated UTC: 2026-06-15T12:13:03Z

## Why This Wave Exists

Wave 7 already selected service-worker request packets, approval-safe queues, and review gates. Wave 8 checks current primary sources for the next runtime decision: which frameworks should become execution substrates once the gates are ready, and which should stay as research references.

## Source Findings

### Microsoft Agent Framework

- URL: https://github.com/microsoft/agent-framework
- Evidence: Open multi-language framework for production-grade AI agents and multi-agent workflows in .NET/Python; emphasizes durability, restartability, observability, governance, human-in-the-loop control, graph workflows, MCP/A2A, and hosted/cloud patterns.

### Microsoft AutoGen

- URL: https://github.com/microsoft/autogen
- Evidence: AutoGen README now marks the project maintenance mode and points new users to Microsoft Agent Framework; keep it as legacy pattern source, not new core.

### LangGraph

- URL: https://github.com/langchain-ai/langgraph
- Evidence: Low-level infrastructure for long-running stateful workflows/agents with durable execution, human-in-the-loop, memory, and trace/debugging support.

### Pydantic AI

- URL: https://github.com/pydantic/pydantic-ai
- Evidence: Python agent framework for production-grade GenAI applications/workflows; model-agnostic provider support and OpenTelemetry/Logfire observability fit typed local workers.

### Hatchet

- URL: https://github.com/hatchet-dev/hatchet
- Evidence: Orchestration engine for background tasks, AI agents, and durable workflows; supports Python/TypeScript/Go/Ruby with queueing, retries, durability, monitoring, alerting, and logging.

### DBOS Transact Python

- URL: https://github.com/dbos-inc/dbos-transact-py
- Evidence: Postgres-backed durable Python workflows and queues; checkpointing/resume, queue concurrency/rate limits, scheduling, notifications, programmatic workflow management.

## Stack Decision

| Component | Decision | Reason |
| --- | --- | --- |
| Core control plane | Keep current SQLite task/artifact/trace/service-request spine; do not replace it with a framework runtime yet. | The lab already has gates, packet schemas, chain integrity, and review artifacts. Replacing it before worker execution starts would add migration risk without earning more money-path throughput. |
| Typed local worker runtime | Promote Pydantic AI as the first typed worker implementation path for local/non-gated model workflows. | Strong Python fit, provider-agnostic model layer, typed validation, and observability align with existing Pydantic eval artifacts. |
| Long-running manager/seekers | Evaluate LangGraph for stateful manager and seeker loops after current service-worker approval chain is stable. | Durable execution and human-in-the-loop features match manager checkpoints and reviewable state updates. |
| Production multi-agent orchestration | Track Microsoft Agent Framework as the likely cross-runtime production target; do not build on AutoGen for new core work. | MAF is the active Microsoft path with production, governance, durability, workflow, MCP/A2A, Python/.NET support; AutoGen is maintenance-mode. |
| Durable service-worker queues | Keep SQLite queue reports now; next adapter proof should compare DBOS and Hatchet against existing service-worker packet semantics. | DBOS is minimal Postgres-backed durable execution; Hatchet is stronger when queue scale, retries, monitoring, and self-hosted dashboard matter. |
| Human/account/payment gates | Keep all legal/KYC/payment/wallet/account/browser-public actions as service requests requiring human/CRO decisions. | Every external action class remains a boundary; runtime choice must not bypass approval records or exact-scope review. |

## Recommended Architecture Delta

- Keep the current SQLite CEO/control-plane ledger as the authority for task, artifact, trace, and service-request state.
- Use Pydantic AI for the first typed local worker bridge, but keep model/API calls behind service-request approval.
- Use LangGraph for future manager/seeker loops that need persistent state and human-in-the-loop checkpoints.
- Evaluate Microsoft Agent Framework as the production multi-agent target after local gates prove stable; it is now the active Microsoft successor path, while AutoGen is maintenance-mode.
- Compare DBOS and Hatchet as durable worker queue adapters; do not import either until a local adapter test proves packet compatibility and operational benefit.

## Next Actions

- Add a local runtime-bridge scorecard mapping Microsoft Agent Framework, LangGraph, Pydantic AI, DBOS, Hatchet, and current SQLite reports against the 11 pending service-worker packets.
- Build one dry-run Pydantic AI worker only for a local artifact summarization task with api_calls=false unless model/API approval is explicitly granted.
- Design a DBOS-vs-Hatchet adapter test that consumes service-worker request packets and emits local result placeholders without enqueueing external work.
- Keep AutoGen references only for migration/pattern comparison; remove it from any new-core recommendation unless MAF is unavailable.

## No-Action Statement

No worker was started, no approval was granted, no service request was updated, no account/browser/API/payment/wallet/public/security-testing action was performed, and no dependency was installed.
