# Agent Company Deep Research Wave 14

Generated UTC: 2026-06-17T19:58:00Z

Purpose: refresh the agent-company infrastructure map after the local identity, egress, MCP registry, and worker activation preflight validators landed. This wave focuses on current open-source/public architecture signals for durable agents, MCP/tool governance, browser workers, and scalable per-agent state.

Boundary: research and local planning only. No accounts, registrations, browser sessions, API calls, MCP server starts, tool calls, payments, wallet actions, public actions, or external side effects.

## Current-source Signals

| Source | Current signal | Lab implication |
| --- | --- | --- |
| LangGraph (`langchain-ai/langgraph`) | LangGraph positions itself as low-level infrastructure for long-running, stateful agents, with durable execution, human-in-the-loop state inspection/modification, memory, debugging, and deployment. It had a latest release visible as `langgraph-cli==0.4.30` on 2026-06-16 during this scan. Source: https://github.com/langchain-ai/langgraph | Treat graph runtimes as the right abstraction for manager/worker state machines, but keep the lab's SQLite task/outcome/trace ledger as the source of authority until a migration preflight proves equivalence. |
| Dapr Agents (`dapr/dapr-agents`) | Dapr Agents emphasizes resilient, observable AI agents with workflow orchestration, statefulness, telemetry, pub/sub, service invocation, state stores, durable workflows, and virtual actors. Source: https://github.com/dapr/dapr-agents | Strong reference for a future distributed worker bureau: actors map cleanly to service-worker pools, pub/sub maps to task assignment, and workflows map to approval waits. Do not adopt until local adapter contracts exist. |
| Cloudflare Agents (`cloudflare/agents`) | Cloudflare Agents are persistent, stateful execution environments backed by Durable Objects, with lifecycle, storage, scheduling, AI model calls, MCP, workflows, and idle hibernation. Source: https://github.com/cloudflare/agents | Confirms that one-agent-per-session/user/lane is a mainstream scaling pattern. The lab should model each lane manager and service worker as a durable identity with explicit wake/sleep, lease, and replay semantics. |
| Microsoft Durable Task extension for Agent Framework | Microsoft docs describe persistent sessions, automatic checkpointing, multi-agent orchestration, human approval waits, timed waits, crash/restart survival, and serverless scaling. Source: https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/durable-task/sdks/durable-agents-microsoft-agent-framework.md | Supports the lab's current insistence on signed operator decisions and durable wait states before worker registration or execution. Also validates the need for a runtime-start preflight separate from registration preflight. |
| `lastmile-ai/mcp-agent` | `mcp-agent` treats MCP servers as composable tool surfaces and provides workflow decorators that can run via asyncio or Temporal. It also documents MCP server aggregation and secrets configuration. Source: https://github.com/lastmile-ai/mcp-agent | The lab's MCP registry gate is directionally correct: tool aggregation must be explicit, secrets must stay outside source control, and durable execution should be separable from MCP server connection mechanics. |
| `browser-use/browser-use` | Browser Use 0.13 introduces a beta agent with a Rust core, browser harness, persistent tools, and recovery loops for frontier models. Source: https://github.com/browser-use/browser-use | Browser workers are maturing toward native harnesses. The lab should keep browser service requests parked until domain/session/recording/teardown policy exists, then evaluate Browser Use as a local read-only harness candidate. |
| `vercel-labs/agent-browser` | Agent Browser is a browser automation CLI for AI agents, implemented as a native Rust CLI/daemon using direct CDP, with cross-platform binaries including Windows x64. Source: https://github.com/vercel-labs/agent-browser | This is a concrete candidate for a future browser-read-only worker, but it downloads/controls Chrome and must remain gated behind browser service approval, recording, teardown, and public-action denial. |

## Architecture Synthesis

The current ecosystem is converging on five primitives:

1. Durable state per agent or workflow.
2. Human approval waits that can pause for long periods without losing context.
3. Tool and MCP registries that make external capability explicit instead of implicit.
4. Browser/computer-use harnesses with native runtimes and recovery loops.
5. Observability traces that tie decisions, tool calls, artifacts, and outcomes together.

The lab already has local equivalents for several of these:

- durable state: `state/agent_company.sqlite`
- human gates: service requests, decision packets, signed-decision guard patterns
- MCP/tool registry: `mcp-tool-registry-gate-v1`
- identity and egress: local identity-envelope and egress-ledger validators
- traceability: `trace_events`, artifact hashes, validation reports

The remaining gap is not another broad framework scan. The next high-value build is an activation/runtime boundary that proves a worker can be started in a dry-run harness without mutating service requests, invoking tools, creating credentials, or touching external systems.

## Candidate Stack Decisions

| Candidate | Decision | Reason |
| --- | --- | --- |
| LangGraph | Keep as conceptual reference and possible future graph adapter. | Strong fit for stateful manager workflows and human intervention, but not needed before local runtime-start preflight. |
| Dapr Agents | Keep as distributed-worker reference. | Strong actor/workflow/pubsub model, but heavier than the current SQLite lab. Revisit after local adapter proofs. |
| Cloudflare Agents | Keep as per-agent persistent-state reference. | Good architecture match for one lane/worker per durable object, but migration would require deployment and account decisions. |
| Microsoft Agent Framework + Durable Task | Keep as enterprise durable-agent reference. | Good evidence for checkpointing and human approval waits, but adopting Azure infrastructure is gated by account/billing decisions. |
| mcp-agent | Promote to MCP adapter candidate after registry gate hardening. | It directly maps MCP aggregation to durable workflows, but live MCP server connection remains blocked. |
| Browser Use | Promote to browser-read-only harness candidate after browser policy. | Useful for public research lanes, but it is a browser execution system and must stay behind approval gates. |
| Agent Browser | Add to browser-worker candidate list. | Native Rust/CDP path is attractive for reliability, but installing Chrome/daemon behavior requires explicit gate checks. |

## Money-path Execution Implications

For paid code, security bounties, prediction markets, digital products, content growth, and lead-gen lanes, the infrastructure should follow one policy:

1. Seekers can produce local evidence and ranked candidates.
2. Managers can request service-worker help through cataloged service requests.
3. Service workers cannot execute until identity, egress, MCP/tool, approval, and runtime-start gates pass.
4. External action remains narrow: one approved action, one exact artifact, one trace, one post-action evidence seal.

This is slower than uncontrolled automation, but it prevents fake progress, accidental public actions, and account/payment/legal mistakes. For money-making work, the practical edge is not "more autonomy"; it is higher throughput of safe local proof packets and faster promotion of only the few candidates that deserve human approval.

## Recommended Next Builds

1. `runtime_start_preflight_validator_v1`
   - Inputs: worker activation preflight chain, signed operator decision status, service request scope, runtime command preview, output path, trace id.
   - Positive result: dry-run runtime start is coherent but still not executed.
   - Negative cases: command executes, process starts, service request assigned, browser opens, MCP server starts, credential touched, missing output artifact, missing trace id.

2. `browser_read_only_worker_policy_v1`
   - Inputs: service request, domain allowlist, session mode, recording path, teardown policy, disallowed actions.
   - Positive result: browser read-only plan is valid as a plan, not as execution authority.
   - Negative cases: login, form submit, comment/post, payment, wallet, settings changes, unrecorded session.

3. `mcp_adapter_candidate_matrix_v1`
   - Inputs: mcp-agent, official MCP registry candidates, local fixture server, schema drift policy, secret handling.
   - Positive result: rank adapter candidates for report-only/lab-only usage.
   - Negative cases: implicit secrets, remote endpoint without allowlist, untyped schema drift, write-capable tool default enabled.

4. `lane_manager_workflow_runtime_map_v1`
   - Inputs: current lane taxonomy, manager prompts, task DAG, trace conventions.
   - Positive result: map each lane to a durable workflow shape without adopting a framework yet.
   - Negative cases: lane workflow requires account/payment/public action by default.

## Immediate Recommendation

Build `runtime_start_preflight_validator_v1` next. The lab has already reached `preflight_passed_registration_blocked`; the missing piece is a separate validator that says exactly what would have to be true before any local runtime process can start. This keeps the system moving toward real worker activation while preserving the hard boundary against premature external execution.

## Source URLs

- https://github.com/langchain-ai/langgraph
- https://github.com/dapr/dapr-agents
- https://github.com/cloudflare/agents
- https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/durable-task/sdks/durable-agents-microsoft-agent-framework.md
- https://github.com/lastmile-ai/mcp-agent
- https://github.com/browser-use/browser-use
- https://github.com/vercel-labs/agent-browser
