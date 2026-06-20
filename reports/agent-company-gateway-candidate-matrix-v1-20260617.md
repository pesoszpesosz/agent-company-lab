# Agent Company Gateway Candidate Matrix v1

Generated UTC: 2026-06-17T19:12:00Z

Lane: platform_engineering

Task: task-agent-company-gateway-candidate-matrix-v1-20260617

## Executive Takeaway

The agent-company lab should not install or run a live AI gateway yet. The next correct layer is a local egress-governance contract that can later map onto LiteLLM, Portkey, Kong, TrueFoundry, Lunar/MCPX, or a custom gateway.

The near-term recommendation is:

1. Keep the SQLite CEO ledger as the source of truth.
2. Define a local `agent_egress_event_ledger_v1` before any live gateway.
3. Use LiteLLM as the most practical future local-first candidate for model and MCP gateway experiments.
4. Treat Kong, TrueFoundry, Portkey, and Lunar as architecture references until the lab has signed operator decisions, agent identity envelopes, credential policy, and replayable egress evidence.

## Why This Layer Matters

The current company can already create service requests, review gates, worker-pool review packets, trace events, and chain-integrity reports. The missing piece is a unified egress policy layer for actions that leave the local lab:

- model API calls
- MCP tool calls
- direct REST/API calls
- browser actions
- signed-in browser actions
- public submissions
- wallet/payment/account-adjacent actions
- agent-to-agent traffic

Without an egress layer, every future worker would need to reinvent policy checks. With an egress layer, every worker emits the same evidence: who requested the action, what tool/model/API/browser target was used, what policy allowed or denied it, what budget applied, and what artifact proves the result.

## Candidate Matrix

| Candidate | Current signal | Fit for this lab | Main risk | Recommended posture |
| --- | --- | --- | --- | --- |
| Local SQLite egress ledger | Already matches existing CEO ledger and chain-integrity model | Highest immediate fit | Does not perform live gateway enforcement by itself | Build first as report-only contract |
| LiteLLM | Open-source AI Gateway for 100+ LLM providers; MCP gateway controls MCP access by key/team/org | Best future local-first model/MCP gateway candidate | Governance beyond model/MCP traffic still needs our ledger | Pattern now; possible approved local experiment later |
| Portkey Gateway | Open-source gateway with routing, fallbacks, load balancing, guardrails, multimodal support | Strong routing/guardrail reference | Primarily model gateway; live deployment adds dependency and credential surface | Pattern/reference until dependency review |
| Kong AI Gateway / Agent Gateway | API + AI + MCP + A2A governance in one enterprise platform | Best enterprise architecture reference for unified traffic governance | Enterprise/platform complexity; not local-first for this lab | Reference for long-term traffic taxonomy |
| TrueFoundry AI/MCP/Agent Gateway | Unified registry, step-level observability, RBAC, policy enforcement, governed MCP access | Strong enterprise control-plane reference | Commercial/platform scope; too heavy before local contracts | Reference for agent registry and policy model |
| Lunar/MCPX-style gateway | Emphasizes governing LLM, MCP, and API traffic from a distributed control plane | Strong conceptual reference for distributed control | Source material is vendor framing; needs independent verification before adoption | Reference for distributed-control-plane requirements |
| AgentControl | Open-source runtime guardrail control plane across frameworks | Useful lightweight policy/evaluator reference | Small project and not a full egress gateway | Pattern for local deny/allow evaluator shape |

## Fresh Repository Metadata

Collected from the GitHub API on 2026-06-17.

| Repository | Stars | Forks | Language | Last pushed UTC | License | Notes |
| --- | ---: | ---: | --- | --- | --- | --- |
| BerriAI/litellm | 50717 | 8961 | Python | 2026-06-17T18:49:36Z | NOASSERTION | Python SDK and proxy server / AI gateway with cost tracking, guardrails, load balancing, and logging. |
| Kong/kong | 43604 | 5151 | Lua | 2026-06-17T08:27:14Z | Apache-2.0 | API and AI gateway; relevant as mature gateway substrate. |
| Portkey-AI/gateway | 12106 | 1134 | TypeScript | 2026-05-25T13:54:51Z | MIT | Open-source AI Gateway with integrated guardrails and model routing. |
| microsoft/agent-framework | 11428 | 1919 | Python | 2026-06-17T18:57:10Z | MIT | Relevant for workflow pause/resume and approval/event patterns. |
| agentcontrol/agent-control | 260 | 39 | Python | 2026-06-17T15:57:54Z | Apache-2.0 | Centralized runtime guardrail control plane; useful evaluator reference. |

## Source Findings

### LiteLLM

LiteLLM positions itself as an open-source AI gateway with one interface to many model providers. Its MCP documentation says the proxy can provide a fixed endpoint for MCP tools and manage MCP access by key, team, or organization.

Agent-company implication:

- Strong candidate for future local model/MCP gateway experiments.
- Should not become the policy source of truth. The lab's ledger should decide whether a model/MCP call is allowed, and LiteLLM can later enforce or route approved calls.
- Useful first mapping target for `agent_egress_event_ledger_v1`.

Sources:

- https://github.com/BerriAI/litellm
- https://docs.litellm.ai/docs/mcp

### Kong AI Gateway / Agent Gateway

Kong frames its gateway as one platform for API, LLM, MCP, and agent-to-agent traffic. Its April 2026 Agent Gateway announcement emphasizes unified observability, security, access control, audit, cost visibility, and governance across LLM, MCP, and A2A communication.

Agent-company implication:

- Excellent taxonomy reference: `llm`, `mcp`, `api`, `event`, and `agent_to_agent` should be separate egress classes.
- Strong evidence that the lab should not treat "model call" as the only external action class.
- Too heavyweight for the next local step.

Sources:

- https://konghq.com/products/kong-ai-gateway
- https://www.prnewswire.com/news-releases/kong-ai-gateway-now-supports-agent-to-agent-traffic-becoming-the-most-comprehensive-ai-gateway-for-the-agentic-era-302741741.html
- https://github.com/Kong/kong

### Portkey Gateway

Portkey says it has open-sourced its AI Gateway, with unified access, fallbacks, load balancing, retries, guardrails, and production use at very high token volume. Its gateway repository describes integrated guardrails, broad model routing, multimodal support, and agentic workflow integrations.

Agent-company implication:

- Useful for guardrail placement: input/output guardrails should be attached to the gateway decision, not buried inside worker prompts.
- Useful for routing/fallback concepts.
- Needs dependency/security review before any local run.

Sources:

- https://portkey.ai/docs/product/open-source
- https://github.com/portkey-ai/gateway
- https://portkey.ai/blog/bringing-guardrails-on-the-gateway/

### TrueFoundry

TrueFoundry presents a combined AI Gateway, MCP Gateway, Agent Gateway, prompt management, and agent skills registry. Its June 2026 Agent Gateway launch emphasizes a unified agent registry, step-level observability, RBAC, policy enforcement, governed MCP tool access, retries, timeouts, and fallbacks.

Agent-company implication:

- Strong reference for the future "agent identity envelope": registry, role-based access, per-step observability, and policy enforcement.
- Too broad/commercial for near-term local implementation.
- Use as enterprise benchmark for our local ledger design.

Sources:

- https://www.truefoundry.com/
- https://www.businesswire.com/news/home/20260602233322/en/TrueFoundry-Launches-Agent-Gateway-to-Close-the-Enterprise-AI-Governance-Gap

### Lunar / MCPX Direction

Lunar's 2026 gateway comparison argues that AI gateways now need to govern the full interaction, not only model traffic: LLMs, MCP, and API traffic. It ranks Lunar, Portkey, Kong, LiteLLM, and TrueFoundry as the five gateways enterprises are evaluating.

Agent-company implication:

- Validates a distributed-control-plane requirement.
- Reinforces that the company needs one policy language for model, tool, and API egress.
- Treat as architecture reference, not as an adoption decision.

Source:

- https://www.lunar.dev/post/top-5-ai-gateways-in-2026

### AgentControl

AgentControl is a smaller open-source project focused on centralized runtime guardrails across agent frameworks. It supports configurable evaluators and framework integration rather than acting as a full egress gateway.

Agent-company implication:

- Useful for local evaluator shape: regex/list/JSON/SQL/custom checks.
- Could inspire the deny/allow verdict schema for our egress ledger.

Source:

- https://github.com/agentcontrol/agent-control

## Recommended Local Contract Before Any Live Gateway

`agent_egress_event_ledger_v1` should require:

- `event_id`
- `request_id`
- `task_id`
- `lane_id`
- `agent_id`
- `worker_pool_id`
- `egress_type`: `model_api`, `mcp_tool`, `direct_api`, `browser_read_only`, `browser_signed_in`, `public_submission`, `wallet_payment`, `agent_to_agent`
- `target`: provider, domain, MCP server, API host, browser URL, or agent id
- `tool_or_model`
- `input_artifact_path`
- `output_artifact_path`
- `credential_scope`
- `budget_scope`
- `approval_artifact_path`
- `policy_verdict`: `allow`, `deny`, `pause_for_review`
- `policy_reasons`
- `redaction_required`
- `recording_required`
- `created_utc`
- `expires_utc`
- `runtime_boundary`

Default policy should be deny. No live egress should occur unless:

1. The service request is approved.
2. The worker pool exists and has an identity envelope.
3. The egress event passes policy validation.
4. The operator decision scope matches the requested action.
5. The output artifact path is declared before execution.

## Phased Adoption Plan

### Phase 0: Now

Build only report-only contracts:

- `agent_egress_event_ledger_v1`
- `agent_identity_envelope_v1`
- `worker_pool_operator_decision_contract_v1`
- gateway negative fixtures

### Phase 1: First Approved Local Experiment

If approved later, create a LiteLLM configuration draft for local model/MCP routing, but do not run it until dependency, key, cost, and network boundaries are approved.

### Phase 2: Policy Mapping

Map local egress verdicts to LiteLLM callbacks/teams/keys, Portkey guardrails, Kong routes/plugins, or TrueFoundry registries. Keep the local ledger authoritative.

### Phase 3: Worker Runtime Integration

Workers must call the local policy layer before any external call. Browser/computer-use workers require separate recording and teardown evidence.

## Validation Boundary

This matrix:

- started no gateway
- installed no gateway
- created no API keys
- called no model APIs
- called no MCP tools
- opened no browser sessions
- assigned no service requests
- started no workers
- changed no external account, wallet, payment, public, GitHub, X, or marketplace state

## Decision

Recommended next build: `agent_egress_event_ledger_v1` as a report-only schema/fixture packet, after explicit implementation-design approval if code changes are required.

