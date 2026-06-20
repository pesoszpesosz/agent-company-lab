# Agent Company Deep Research Wave 13 - Current Control Plane, Sandbox, and Governance Signals

Generated UTC: 2026-06-17T19:02:00Z

Lane: platform_engineering

Task: task-agent-company-deep-research-wave13-20260617

## Executive Takeaway

The strongest current signal is not "pick one agent framework." The market is separating into layers:

1. Agent control planes for identity, policy, audit, observability, evals, and deployment.
2. Computer/browser-use sandboxes for agents that interact with UIs, terminals, files, and desktops.
3. Workflow runtimes that can pause for human approval and resume.
4. AI gateways and semantic traffic controls that govern LLM, MCP, tool, and API traffic.
5. Visual workflow/app-builder surfaces that are useful for product UX but dangerous if treated as the source of truth for autonomous money-making work.

The existing agent-company lab is aligned with this direction: SQLite ledger, service catalog, approval gates, trace events, chain integrity, and report-only preflights. The gap is execution: before registering worker pools or starting any external action, the lab needs a signed operator decision contract, per-agent identity scope, credential boundaries, and a runtime policy envelope that can be verified independently.

## Fresh GitHub Metadata Snapshot

Collected from the GitHub API on 2026-06-17. Counts are point-in-time and should be refreshed before any dependency commitment.

| Repository | Stars | Forks | Language | Last pushed UTC | Why it matters |
| --- | ---: | ---: | --- | --- | --- |
| n8n-io/n8n | 192943 | 58628 | TypeScript | 2026-06-17T18:53:22Z | High-adoption workflow automation and integration surface; useful for service-worker recipe UI patterns, but high credential/public-action risk. |
| langflow-ai/langflow | 149793 | 9289 | Python | 2026-06-17T18:55:42Z | Very large visual agent/workflow builder; useful for product-studio UX patterns. |
| langgenius/dify | 145620 | 22907 | TypeScript | 2026-06-17T18:21:48Z | Production-oriented app/agent workflow platform; useful as a productization reference. |
| browser-use/browser-use | 99299 | 11086 | Python | 2026-06-15T08:24:43Z | Browser agent layer with a new native/Rust-core browser harness direction. |
| OpenHands/OpenHands | 77541 | 9855 | Python | 2026-06-17T18:46:34Z | Coding-agent harness pattern for future code-worker lanes; must be sandboxed and approval-gated. |
| crewAIInc/crewAI | 53806 | 7527 | Python | 2026-06-17T18:41:44Z | Multi-agent orchestration plus commercial control-plane language: tracing, unified management, security. |
| FlowiseAI/Flowise | 53687 | 24530 | TypeScript | 2026-06-16T11:05:50Z | Visual AI-agent builder; useful for low-code UI comparison, not core ledger authority. |
| agno-agi/agno | 40749 | 5531 | Python | 2026-06-17T18:52:11Z | Agent platform explicitly framed around building, running, and managing agent platforms. |
| microsoft/semantic-kernel | 28153 | 4651 | C# | 2026-06-17T13:33:59Z | Mature orchestration concepts, including group chat and human-in-the-loop patterns. |
| activepieces/activepieces | 22801 | 3810 | TypeScript | 2026-06-17T18:53:59Z | Workflow automation with AI agents and MCP server ecosystem; high integration risk. |
| trycua/cua | 18402 | 1189 | HTML | 2026-06-17T18:19:01Z | Open-source computer-use infrastructure for desktop sandboxes, SDKs, and benchmarks. |
| e2b-dev/E2B | 12632 | 933 | Python | 2026-06-17T18:54:18Z | Secure tool environment for agents; strong future sandbox candidate. |
| microsoft/agent-framework | 11428 | 1919 | Python | 2026-06-17T18:03:37Z | Multi-agent workflow framework with human approval/resume discussion. |
| VoltAgent/voltagent | 9661 | 999 | TypeScript | 2026-06-08T20:06:55Z | TypeScript agent engineering platform with guardrails, workflow, MCP, observability, evals, and ops console. |
| ai-boost/awesome-harness-engineering | 1900 | 195 | Python | 2026-06-17T15:35:58Z | Curated harness-engineering landscape covering evals, memory, MCP, permissions, observability, and orchestration. |
| agentcontrol/agent-control | 260 | 39 | Python | 2026-06-17T15:57:54Z | Directly relevant runtime guardrail/control-plane concept: centralized controls across frameworks. |

## Source Findings

### 1. Browser and computer-use execution needs a separate sandbox class

Browser Use 0.13 describes a beta agent with a Rust core and browser harness, giving models a browser/computer action space, persistent tools, and recovery loops. That is relevant to the lab's browser-read-only pool, but it also confirms the risk: browser workers are no longer simple page fetchers; they are runtime actors that need session boundaries, recovery-loop limits, recording, and replay.

Source: https://github.com/browser-use/browser-use

trycua/cua describes open-source infrastructure for computer-use agents, including sandboxes, SDKs, and benchmarks for full desktop control across macOS, Linux, and Windows. This supports a separate "computer_use_sandbox_worker" concept instead of merging desktop automation into the same pool as browser read-only research.

Source: https://github.com/trycua/cua

Implication for this lab:

- Keep browser-read-only, signed-in-browser-read-only, and desktop/computer-use workers as separate pool types.
- Every pool should require a session artifact, allowed domains/apps, credential policy, recording policy, and teardown evidence.
- Browser/computer-use should stay blocked until the signed decision and pool registration gates exist.

### 2. Enterprise control-plane language now matches the lab's direction

CrewAI's public repository describes its control plane as covering tracing, observability, centralized management, integrations, security, analytics, and on-prem/cloud deployment options. Activant's agent-control-plane analysis frames the problem as AI sprawl: overlapping agents, shadow keys, brittle automations, and untraceable spend. It recommends a unified studio/marketplace model with per-agent identity, policy-as-code, signed/rate-limited tools, versioned flows, evals, and economics.

Sources:

- https://github.com/crewaiinc/crewai
- https://activantcapital.com/research/the-agent-control-plane

Implication for this lab:

- The SQLite CEO ledger is the right local source of truth for now.
- The next control-plane layer should not be a visual flow builder first. It should be an operator decision ledger and signed action contract.
- Visual dashboards are useful as views over the ledger, not as the ledger itself.

### 3. Agent security is moving toward identity, policy, traffic control, and audit

Tigera Lynx, announced June 17, 2026, is positioned as a unified control plane for Kubernetes-native AI agents. The reported capabilities map directly to the lab's gaps: find every agent, assign sandboxes, give each agent a cryptographic identity, enforce policy on every action, audit agent activity, and detect anomalous behavior.

Agent Control presents a smaller open-source signal: centralized runtime guardrails that can apply across LangChain, CrewAI, Google ADK, AWS Strands, and similar frameworks, with configurable evaluators.

SemaMesh's CNCF sandbox proposal frames the "semantic blind spot" as the gap between ordinary network controls and what autonomous agents actually do. Its direction: identity-aware traffic interception, semantic policy, quotas, forensics, cost metrics, and Prometheus-style telemetry.

Sources:

- https://www.helpnetsecurity.com/2026/06/17/tigera-lynx/
- https://github.com/agentcontrol/agent-control
- https://github.com/cncf/sandbox/issues/455

Implication for this lab:

- Add a future "agent identity envelope" to every worker registration: agent id, department, role, allowed request types, tool scopes, credential scope, network/browser scope, budget scope, and expiry.
- Add "policy evidence" as a first-class artifact type: why an action was allowed or denied.
- Treat gateway/traffic policy as a separate department primitive, not as an afterthought inside each worker.

### 4. Human approval/resume is a first-class workflow primitive

The Microsoft Agent Framework discussion notes that workflows can emit a request-info event to pause execution, wait for human approval or input, and resume. Semantic Kernel discussions also point to multiple orchestration modes, including sequential, concurrent, group chat, and human-in-the-loop patterns.

Sources:

- https://github.com/microsoft/agent-framework/discussions/2753
- https://github.com/microsoft/semantic-kernel/discussions/12270

Implication for this lab:

- The existing service request `needs_review` state is correct but too coarse for live execution.
- The next contract should distinguish: request created, request reviewed, operator decision received, pool registered, request assigned, worker started, worker paused, approval requested, approval received, worker resumed, worker completed, evidence sealed.
- The system should never jump from "decision packet exists" to "action happened" without an intermediate signed decision and preflight pass.

### 5. AI gateways are becoming agent gateways

Lunar.dev's 2026 AI gateway comparison argues that agent infrastructure now needs governance beyond model-provider routing: agents invoke tools, MCP servers, and downstream APIs with credentials. The key architecture claim is a distributed control plane that can govern LLM, MCP, and API traffic.

Source: https://www.lunar.dev/post/top-5-ai-gateways-in-2026

Implication for this lab:

- Model API execution is only one slice. The future gateway needs to govern model calls, MCP calls, browser actions, API calls, and public submissions.
- For now, the local lab should model this as a "gateway decision packet" and "egress event ledger" before any live gateway deployment.

### 6. Visual app/workflow builders are useful references but risky execution authorities

n8n, Activepieces, Langflow, Dify, and Flowise have massive adoption and useful UI patterns. They are valuable references for workflow recipes, integrations, and visual state inspection. They are not good first sources of authority for this lab because they naturally pull the system toward credentials, integrations, public actions, and live workflow execution.

Implication for this lab:

- Use these systems as UX and connector pattern references.
- Keep the local control plane, approvals, and evidence ledger authoritative.
- Do not run external workflow platforms until credential isolation, per-action approval, and replayable audit are implemented.

## Architecture Delta For Agent Company Lab

The next infrastructure layer should be:

1. Worker-pool operator decision contract.
   - Inputs: review packet id, target pool id, decision, scope, expiry, approver, rationale.
   - Decisions: register_later, hold, reject, request_more_evidence.
   - Output: signed decision artifact only. No registration side effect.

2. Agent identity envelope.
   - Captures role, department, allowed service request types, tool scope, browser/network scope, credential policy, budget policy, and expiry.
   - Required before any worker pool can be registered.

3. Egress event ledger.
   - Local schema for future model/API/browser/MCP/public-action egress events.
   - First implementation should be report-only fixtures with deny-by-default policy.

4. Worker lifecycle state machine v2.
   - Expands current request states into explicit pause/resume/approval/evidence-seal states.
   - Keeps human approval as a durable transition, not a comment in a report.

5. Gateway candidate matrix.
   - Compare LiteLLM, Kong AI Gateway, Lunar/MCPX, Portkey, and TrueFoundry-style approaches for local-first governance.
   - Treat this as pattern research until install/deployment approval exists.

## Recommended Next Concrete Builds

No external action should be taken yet. The next safe builds are local/report-only:

1. `worker_pool_operator_decision_contract_v1`
   - Convert the 7 review packets into a signed-decision intake format.
   - Validate negative fixtures: missing approver, expired decision, scope mismatch, command preview tampering, non-approved pool id, public-action escalation.

2. `agent_identity_envelope_v1`
   - Define the identity envelope every worker pool will need before registration.
   - Include credentials, network/browser, budget, and expiry scopes.

3. `agent_egress_event_ledger_v1`
   - Model future LLM/API/MCP/browser/public-action traffic as ledger rows.
   - Keep every probe deny-by-default until explicit operator approval exists.

4. `gateway_candidate_matrix_v1`
   - Research and compare gateway options for governing model, MCP, and API traffic.
   - Keep as report-only; no installs, keys, containers, or runtime starts.

## Runtime Boundary

This research wave:

- started no browser sessions
- registered no worker pools
- assigned no service requests
- started no workers
- installed no dependencies
- imported no new runtime packages
- called no model APIs
- used no credentials
- touched no wallets, accounts, payments, trades, public posts, or bounty submissions
- changed no external state

## Sources

- Browser Use: https://github.com/browser-use/browser-use
- CUA: https://github.com/trycua/cua
- CrewAI: https://github.com/crewaiinc/crewai
- VoltAgent: https://github.com/VoltAgent/voltagent
- Agent Control: https://github.com/agentcontrol/agent-control
- Microsoft Agent Framework discussion: https://github.com/microsoft/agent-framework/discussions/2753
- Semantic Kernel discussion: https://github.com/microsoft/semantic-kernel/discussions/12270
- SemaMesh CNCF issue: https://github.com/cncf/sandbox/issues/455
- Tigera Lynx report: https://www.helpnetsecurity.com/2026/06/17/tigera-lynx/
- Lunar.dev AI gateway comparison: https://www.lunar.dev/post/top-5-ai-gateways-in-2026
- Activant Agent Control Plane: https://activantcapital.com/research/the-agent-control-plane
