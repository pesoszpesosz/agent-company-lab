# Agent Company Operational Infra Radar Wave 16

Generated UTC: 2026-06-17T21:11:59Z
Task: `task-agent-company-operational-infra-radar-wave16-20260618`
Dataset: `E:\agent-company-lab\data\agent-company-operational-infra-radar-wave16-20260618.json`
CSV: `E:\agent-company-lab\data\agent-company-operational-infra-radar-wave16-20260618.csv`
Validation: `E:\agent-company-lab\reports\agent-company-operational-infra-radar-wave16-validation-20260618.json`

## Purpose

Wave 16 extends the agent-company research map into operational infrastructure: browser workers, computer-use sandboxes, MCP/A2A gateways, AI gateways, cloud durable agents, and observability/control planes. This wave is read-only and does not install dependencies, start runtimes, assign service requests, start workers, open a local browser session, call models, call MCP tools, post publicly, touch wallets, or move money.

## Source Boundary

- Repository metadata rows captured: `14`
- Primary-source README/docs rows mapped: `10`
- Metadata method: authenticated `gh repo view`
- Initial unauthenticated GitHub REST attempt: rate-limited, not used as evidence
- Validation failures: `0`
- External side effects: `False`

## Ranked Operational Signals

| Fit | Stars | Last Push | Category | Repo | Local Decision | Gate |
| ---: | ---: | --- | --- | --- | --- | --- |
| `12` | `99307` | `2026-06-15T08:24:43Z` | `browser_worker_runtime` | [browser-use/browser-use](https://github.com/browser-use/browser-use) | Reference browser worker UX, domain allowlists, persistent browser state, and recovery loop patterns. | `browser_read_only_worker_policy plus signed approval before any browser session` |
| `12` | `18403` | `2026-06-17T20:44:46Z` | `computer_use_sandbox` | [trycua/cua](https://github.com/trycua/cua) | Reference desktop sandbox/benchmark boundaries for future local worker pools. | `sandbox execution gate plus worker-pool registration approval required` |
| `12` | `5165` | `2026-06-15T08:45:43Z` | `all_in_one_agent_sandbox` | [agent-infra/sandbox](https://github.com/agent-infra/sandbox) | Reference unified workspace isolation and file/browser/shell/MCP boundaries. | `sandbox execution, MCP registry, secrets, and worker activation gates required` |
| `12` | `3916` | `2026-06-17T18:53:19Z` | `mcp_a2a_registry_gateway` | [IBM/mcp-context-forge](https://github.com/IBM/mcp-context-forge) | Reference tool registry, plugin, observability, and gateway federation design. | `MCP tool registry gate and no live tool calls until approval` |
| `12` | `3338` | `2026-06-17T19:56:52Z` | `agentic_proxy_mcp_a2a_llm_gateway` | [agentgateway/agentgateway](https://github.com/agentgateway/agentgateway) | Reference unified LLM/MCP/A2A gateway policy, RBAC, spend control, and observability patterns. | `no gateway process, Kubernetes, model traffic, or tool traffic without signed operator approval` |
| `11` | `17819` | `2026-06-17T09:44:19Z` | `typed_agent_framework` | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Reference typed outputs, evals, and durable agent semantics. | `model API, dependency install, and runtime start approval required` |
| `11` | `6593` | `2026-06-17T18:26:24Z` | `ai_gateway_data_plane` | [katanemo/plano](https://github.com/katanemo/plano) | Reference LLM routing, safety, observability, and policy data-plane concepts. | `no proxy/runtime start; all model traffic remains blocked` |
| `11` | `5124` | `2026-06-17T11:55:36Z` | `durable_edge_agent_platform` | [cloudflare/agents](https://github.com/cloudflare/agents) | Reference durable objects, scheduling, MCP, workflows, approvals, and browser agents. | `cloud account, billing, deployment, and runtime gates required` |
| `10` | `36307` | `2026-06-16T18:02:29Z` | `browser_cli_worker` | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Study as a possible fast local browser command surface. | `browser install/start remains blocked` |
| `10` | `11012` | `2026-03-07T22:34:40Z` | `human_approval_for_coding_agents` | [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) | Reference approval UX and decision routing for coding-agent work. | `public-action and secrets gates required` |
| `10` | `9661` | `2026-06-08T20:06:55Z` | `agent_observability_platform` | [VoltAgent/voltagent](https://github.com/VoltAgent/voltagent) | Reference production traces, logs, dashboards, and agent metrics. | `no SaaS console, dependency install, or telemetry export without approval` |
| `9` | `59040` | `2026-04-15T11:59:09Z` | `multi_agent_programming_framework` | [microsoft/autogen](https://github.com/microsoft/autogen) | Keep as a conversational multi-agent reference, not the local lane authority. | `dependency install, model API, and runtime start approval required` |
| `9` | `6` | `2026-06-10T19:30:03Z` | `durable_agent_samples` | [Azure-Samples/durable-task-extension-for-agent-framework](https://github.com/Azure-Samples/durable-task-extension-for-agent-framework) | Reference Durable Task extension shape only. | `Azure account, billing, deployment, and runtime gates required` |
| `7` | `11024` | `2026-06-17T18:12:47Z` | `realtime_voice_agent_runtime` | [livekit/agents](https://github.com/livekit/agents) | Park as a future operator surface reference. | `model, audio, network, privacy, and runtime gates required` |

## Primary-Source Takeaways

| Source | Takeaway | Local Mapping |
| --- | --- | --- |
| [agentgateway](https://github.com/agentgateway/agentgateway) | Combines LLM, MCP, and A2A gateway roles with security, spend controls, RBAC, rate limits, and OpenTelemetry. | Unify local model/API, MCP, and agent-to-agent egress ledgers before adopting a live gateway. |
| [Cloudflare Agents](https://github.com/cloudflare/agents) | Includes state, scheduling, MCP, workflows, approvals, browser agents, email, and resumable streaming. | Use as future deployment reference after local checkpoint/resume packets and approval gates mature. |
| [Browser Use](https://github.com/browser-use/browser-use) | Adds a Rust-core beta agent with browser harness, persistent tools, and recovery loops. | Treat browser workers as stateful, policy-bound workers with domain allowlists and lifecycle records. |
| [CUA](https://github.com/trycua/cua) | Focuses on sandboxes, SDKs, and benchmarks for agents controlling full desktops across operating systems. | Separate desktop/computer-use worker pools from browser-only workers. |
| [ContextForge](https://github.com/IBM/mcp-context-forge) | Federates MCP, A2A, REST, and gRPC with governance, discovery, observability, plugins, auth, retries, and tracing. | Extend the service catalog toward a registry/proxy model while preserving deny-by-default tool calls. |
| [Agent Browser](https://github.com/vercel-labs/agent-browser) | Provides a native Rust browser automation CLI for AI agents. | Useful as a command-surface pattern, but browser install/start must remain gated. |
| [AIO Sandbox](https://github.com/agent-infra/sandbox) | Combines browser, shell, file, MCP, and VSCode Server in a Docker environment. | Future worker sandboxes need capability-scoped identity envelopes and per-channel egress records. |
| [VoltAgent](https://github.com/VoltAgent/voltagent) | Emphasizes production observability with execution traces, performance metrics, dashboards, and logs. | Promote trace_events/outcomes/artifacts into richer CEO/Atlas health and replay views. |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Lists durable execution for progress preservation across API failures, app errors, restarts, and HITL workflows. | Keep typed local validators as the boundary before model-backed or durable runtime adapters. |
| [Azure durable agents samples](https://github.com/Azure-Samples/durable-task-extension-for-agent-framework) | Organizes durable AI agent quickstarts and apps around Microsoft Agent Framework plus Durable Task. | Use as a durable-agent sample reference only; Azure deployment and billing are gated. |

## Architecture Decisions

1. `agent_gateway_is_now_a_first_class_layer`
   Decision: promote the local egress ledger plus service catalog toward a future gateway-facing registry before live MCP/model/tool traffic.
   Next build: `agent_company_gateway_readiness_matrix_v1`

2. `browser_and_computer_use_need_separate_worker_classes`
   Decision: keep browser-only workers, computer-use sandboxes, and all-in-one sandboxes as separate activation paths.
   Next build: `browser_computer_use_worker_class_matrix_v1`

3. `observability_must_be_productized_for_the_ceo_layer`
   Decision: convert trace events, artifacts, outcomes, and service requests into replayable health packets for CEO/Atlas views.
   Next build: `checkpoint_resume_ui_packet_design_v1`

4. `cloud_deployment_is_powerful_but_not_the_next_step`
   Decision: study cloud durable-agent platforms as deployment references only; local checkpoint/resume and signed approval must come first.
   Next build: `local_to_cloud_deployment_gate_matrix_v1`

## Recommended Next Sequence

1. `checkpoint_resume_ui_packet_design_v1`
2. `agent_company_gateway_readiness_matrix_v1`
3. `browser_computer_use_worker_class_matrix_v1`
4. `local_to_cloud_deployment_gate_matrix_v1`

## Boundary

- Dependency installs: `0`
- Runtime starts: `0`
- Worker starts: `0`
- Browser sessions started: `0`
- Service requests assigned/updated: `0` / `0`
- Model/API calls: `False`
- MCP tool calls: `False`
- Public/payment/wallet actions: `False` / `False` / `False`
- External side effects: `False`

