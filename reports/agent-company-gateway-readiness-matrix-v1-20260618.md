# Agent Company Gateway Readiness Matrix v1

Generated UTC: 2026-06-17T21:24:00Z
Task: `task-agent-company-gateway-readiness-matrix-v1-20260618`
Source wave: `E:\agent-company-lab\reports\agent-company-operational-infra-radar-wave16-20260618.json`
Validation: `E:\agent-company-lab\reports\agent-company-gateway-readiness-matrix-v1-validation-20260618.json`

## Purpose

Wave 16 showed that gateway layers are now central to serious agent infrastructure: LLM/model gateways, MCP registries, A2A gateways, browser/computer-use workers, and observability consoles. This matrix converts that research into local adoption criteria for the agent company. It does not install, start, route, call, assign, approve, or mutate anything.

## Summary

- Gateway domains assessed: `7`
- Ready for local-only design work: `3`
- Blocked until a real signed decision exists: `2`
- Not ready for local activation: `2`
- Highest-priority next build: `checkpoint_resume_ui_packet_design_v1`

## Readiness Matrix

| Domain | Candidate Sources | Readiness | Score | Missing Prerequisites | Next Local Build |
| --- | --- | --- | ---: | --- | --- |
| `llm_model_api_gateway` | agentgateway, plano, Pydantic AI, Cloudflare Agents | `blocked_requires_signed_decision` | `5` | signed provider/model/cost/lane/credential decision; model-call ledger; CEO budget policy | `model_api_gateway_decision_packet_v1` |
| `mcp_tool_gateway` | agentgateway, ContextForge, AIO Sandbox, Cloudflare Agents | `ready_local_only` | `7` | approved server rows; per-tool allowlist; signed tool-call scope | `mcp_gateway_registry_packet_v1` |
| `a2a_agent_to_agent_gateway` | agentgateway, ContextForge, Cloudflare Agents, AutoGen | `ready_local_only` | `6` | message envelope schema; reply/ack timeout; identity envelope | `agent_to_agent_message_envelope_v1` |
| `browser_worker_gateway` | Browser Use, Agent Browser, Cloudflare Agents | `blocked_requires_signed_decision` | `6` | real browser approval; domain allowlist; state capture path; public-action hard stop | `browser_checkpoint_resume_packet_v1` |
| `computer_use_sandbox_gateway` | CUA, AIO Sandbox | `not_ready` | `3` | worker class matrix; VM/container preflight; filesystem/network policy; secrets/private file boundary | `browser_computer_use_worker_class_matrix_v1` |
| `observability_gateway` | VoltAgent, agentgateway, ContextForge | `ready_local_only` | `8` | checkpoint/resume UI packets; trace replay grouping; manager health rollups | `checkpoint_resume_ui_packet_design_v1` |
| `cloud_durable_agent_gateway` | Cloudflare Agents, Azure Durable Agents samples | `not_ready` | `2` | cloud/billing approval; deployment boundary; secrets route; retention policy; rollback/cost kill switch | `local_to_cloud_deployment_gate_matrix_v1` |

## Adoption Rules

1. Model/API traffic stays blocked until a signed decision names provider, model, budget, lane scope, credential route, artifact path, and kill switch.
2. MCP registry design can proceed locally, but live MCP calls stay blocked until server/tool allowlists and signed scope exist.
3. A2A should start as local message envelopes between lane managers, service workers, and CEO review, not as an external gateway.
4. Browser worker activation requires signed browser read-only approval and apply preflight before any session starts.
5. Computer-use sandboxes require a separate worker-class matrix before any VM, Docker, desktop, shell, file, or MCP-capable runtime starts.
6. Observability is the safest next local build: turn trace events, outcomes, artifacts, service requests, and checkpoint handoffs into replayable CEO/Atlas packets.
7. Cloud durable-agent platforms remain references until local checkpoint/resume and signed approval loops are proven.

## Boundary

- Dependency installs: `0`
- Gateway process starts: `0`
- Runtime starts: `0`
- Worker starts: `0`
- Browser sessions started: `0`
- Service requests assigned/updated: `0` / `0`
- Model/API calls: `False`
- MCP tool calls: `False`
- Public/payment/wallet actions: `False` / `False` / `False`
- External side effects: `False`

