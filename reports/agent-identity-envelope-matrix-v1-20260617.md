# Agent Identity Envelope Matrix v1

Generated UTC: 2026-06-17T19:22:00Z

Lane: platform_engineering

Task: task-agent-identity-envelope-matrix-v1-20260617

## Executive Takeaway

The agent-company lab should treat every future worker as a non-human principal with a short-lived, scoped identity envelope. The identity envelope should exist before any worker pool registration, service-request assignment, gateway egress, browser session, model call, MCP tool call, account action, wallet action, or public submission.

The correct near-term move is not to install SPIRE, OpenFGA, OPA, or an enterprise agent gateway. The correct near-term move is to define a local report-only `agent_identity_envelope_v1` that can later map to those systems.

## Why This Layer Matters

The current lab has service requests, worker-pool review packets, gateway research, and chain integrity. It does not yet have a formal identity record that says:

- who the worker is
- what role it is allowed to play
- what lane/department owns it
- which service request types it can touch
- which tools, browser scopes, MCP servers, APIs, accounts, models, and wallets it can access
- whose authority it is acting under, if any
- when that authority expires
- where the approval artifact lives
- how a later audit can prove the action was allowed

Without that envelope, worker registration risks creating powerful generic agents. With it, worker registration becomes an auditable act of least-privilege provisioning.

## Candidate Matrix

| Candidate | Current signal | Best use for this lab | Risk if adopted too early | Recommended posture |
| --- | --- | --- | --- | --- |
| Local SQLite identity envelope | Directly matches current CEO ledger and artifact model | Immediate source of truth for worker identity, scopes, expiry, and approval evidence | Does not cryptographically attest runtime by itself | Build as report-only contract first |
| SPIFFE/SPIRE | Workload identity standard; SPIRE attests workloads and issues SPIFFE IDs/SVIDs | Future cryptographic identity for long-running workers or sandbox runtimes | Operational complexity; not enough alone for authorization, credential brokering, or policy | Pattern now; install only after runtime approval |
| OpenFGA | Current docs include authorization patterns for agents and modeling agents as principals | Fine-grained relation/task authorization for agent actions | Requires careful resource modeling; not a complete egress or credential system | Strong future mapping target |
| OPA/Rego | General-purpose policy engine widely used for infrastructure and app decisions | Deny/allow/pause policy decisions over identity envelopes and egress events | Policy sprawl if used without a simple local data model | Pattern for policy evaluator |
| Cedar | Application authorization policy language; useful for structured permissions | Candidate for readable policy over actions/resources/context | Needs integration surface and policy tooling | Secondary policy-language candidate |
| SpiceDB / Zanzibar-style FGA | Scalable fine-grained authz store | Alternative to OpenFGA for relation-based permissions | Overkill until the lab has many real resources and workers | Watch as future scale path |
| Casbin | Mature authorization library supporting RBAC/ABAC-style models | Lightweight local policy checks for prototypes | Library-level enforcement can drift from the ledger if not carefully tied to artifacts | Pattern only |
| OPAL | Policy/data distribution layer for OPA/Cedar-style systems | Future policy distribution if multiple workers run | Too much infrastructure before live worker fleet | Later-stage reference |
| MCP identity broker / inventory controls | Palo Alto/TrueFoundry/Strata-style pattern: register MCP servers, disable by default, audit every tool call | Required pattern for future MCP access | Vendor/platform scope; live integrations touch credentials | Implement locally as registry rules first |
| CoSAI Agentic IAM framework | March 2026 identity/access-management framework for agentic systems | High-level requirements checklist for lifecycle, delegation, auditing, and risk-based controls | Framework is guidance, not a drop-in implementation | Use as completion rubric |

## Fresh Repository Metadata

Collected from the GitHub API on 2026-06-17.

| Repository | Stars | Forks | Language | Last pushed UTC | License | Notes |
| --- | ---: | ---: | --- | --- | --- | --- |
| apache/casbin | 20190 | 1743 | Go | 2026-06-16T13:54:37Z | Apache-2.0 | Mature authorization library for ACL/RBAC/ABAC-style access-control models. |
| open-policy-agent/opa | 11867 | 1593 | Go | 2026-06-17T10:37:23Z | Apache-2.0 | General-purpose policy engine. |
| authzed/spicedb | 6782 | 399 | Go | 2026-06-16T20:16:39Z | Apache-2.0 | Zanzibar-inspired fine-grained authorization database. |
| permitio/opal | 5470 | 285 | Python | 2026-06-14T14:28:52Z | Apache-2.0 | Policy and data distribution for OPA, Cedar, and related policy agents. |
| ory/keto | 5355 | 384 | Go | 2026-06-17T03:42:35Z | Apache-2.0 | Zanzibar-style permission server. |
| openfga/openfga | 5310 | 421 | Go | 2026-06-17T18:56:40Z | Apache-2.0 | Flexible authorization engine inspired by Zanzibar. |
| spiffe/spire | 2400 | 623 | Go | 2026-06-17T16:03:20Z | Apache-2.0 | SPIFFE Runtime Environment. |
| cedar-policy/cedar | 1552 | 156 | Rust | 2026-06-17T18:18:07Z | Apache-2.0 | Cedar policy language implementation. |
| agentcontrol/agent-control | 260 | 39 | Python | 2026-06-17T15:57:54Z | Apache-2.0 | Centralized agent runtime guardrail reference. |

## Source Findings

### SPIFFE/SPIRE

SPIRE is the SPIFFE Runtime Environment. It performs node and workload attestation and issues SVIDs to workloads. The SPIRE GitHub description emphasizes the Workload API, SPIFFE IDs, SVID issuance, and workload-to-workload trust via mTLS or JWT verification.

Agent-company implication:

- SPIFFE/SPIRE is the right conceptual model for cryptographic non-human identity.
- It should not be the first local implementation step because our workers are not yet live runtimes.
- The local identity envelope should reserve fields for future `spiffe_id`, `svid_type`, `attestation_method`, and `trust_domain`.

Sources:

- https://github.com/spiffe/spire
- https://spiffe.io/docs/latest/spire-about/spire-concepts/
- https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md

### OpenFGA and relationship-based authorization

OpenFGA's current agent authorization docs explicitly discuss AI agents and automated processes. They distinguish agents acting on behalf of users, agents acting with their own identity, and third-party-service access. The key problem described is broad credentials; the proposed pattern is scoping permissions precisely.

Agent-company implication:

- Model agents as principals, not just as tools.
- Add task-scoped permission fields to the identity envelope.
- Later, map `agent_id`, `request_id`, `lane_id`, `resource`, and `action` to a relation-based authorization engine.

Sources:

- https://openfga.dev/docs/modeling/agents
- https://openfga.dev/docs/modeling/agents/agents-as-principals
- https://github.com/openfga/openfga

### OPA, Cedar, and policy engines

OPA is a general-purpose policy engine. Cedar is a structured policy language implementation. OPAL distributes policy and policy data to policy agents such as OPA and Cedar. These are useful as eventual policy-evaluation layers over the local identity envelope and egress ledger.

Agent-company implication:

- Keep the first policy language simple: local JSON validation and deny-by-default verdicts.
- Later, translate stable policies into OPA/Rego or Cedar if the worker fleet grows.
- Avoid installing a policy engine before the local data model is stable.

Sources:

- https://github.com/open-policy-agent/opa
- https://github.com/cedar-policy/cedar
- https://github.com/permitio/opal

### MCP identity and tool inventory

Palo Alto's MCP security article describes a centralized control point for MCP access: register agents and MCP servers, inventory usage, audit tool invocation, and keep newly registered MCP servers disabled until explicitly enabled by security review. TrueFoundry's gateway material similarly emphasizes agent registry, MCP gateway, access control, policy enforcement, and step-level observability.

Agent-company implication:

- The lab needs an MCP/tool registry before any worker can call tools.
- Unknown MCP servers must default to disabled.
- Every MCP tool call should require an egress ledger event and an identity envelope.

Sources:

- https://www.paloaltonetworks.com/blog/identity-security/secure-ai-agents-controls-visibility-mcp-data-access/
- https://www.truefoundry.com/
- https://www.businesswire.com/news/home/20260602233322/en/TrueFoundry-Launches-Agent-Gateway-to-Close-the-Enterprise-AI-Governance-Gap

### CoSAI Agentic IAM

The Coalition for Secure AI approved an Agentic Identity and Access Management paper on March 20, 2026. Related CoSAI material frames the problem as representing, authenticating, authorizing, and governing AI agents as verifiable, auditable identities with lifecycle management, context-aware controls, and risk-based enforcement.

Agent-company implication:

- Use CoSAI as a checklist: identity, authentication, authorization, delegation, lifecycle, auditability, and risk controls.
- Treat this as a completion rubric for the identity envelope rather than as a software dependency.

Sources:

- https://www.coalitionforsecureai.org/wp-content/uploads/2026/04/agentic-identity-and-access-control.pdf
- https://www.oasis-open.org/2026/05/06/coalition-for-secure-ai-unveils-new-agentic-identity-and-security-research-following-high-profile-sessions-at-rsac-2026/
- https://www.coalitionforsecureai.org/resources/

## Recommended Local Contract: `agent_identity_envelope_v1`

Minimum fields:

- `identity_envelope_id`
- `agent_id`
- `agent_type`: `lane_manager`, `worker_pool`, `service_worker`, `ceo`, `risk_reviewer`, `researcher`
- `role_id`
- `department_id`
- `lane_ids`
- `worker_pool_id`
- `owner_agent_id`
- `owner_thread_id`
- `principal_mode`: `own_identity`, `delegated_user`, `delegated_service`, `test_fixture`
- `delegation_chain`
- `approval_artifact_path`
- `allowed_service_request_types`
- `allowed_egress_types`
- `allowed_targets`
- `allowed_mcp_servers`
- `allowed_mcp_tools`
- `browser_session_policy`
- `credential_policy`
- `wallet_policy`
- `payment_policy`
- `public_action_policy`
- `data_sensitivity_ceiling`
- `budget_scope`
- `rate_limit_scope`
- `recording_required`
- `redaction_required`
- `created_utc`
- `expires_utc`
- `revocation_status`
- `revocation_reason`
- `future_spiffe_id`
- `future_trust_domain`
- `policy_verifier`
- `runtime_boundary`

Default policy:

- no credentials
- no wallets
- no payments
- no account registration
- no public actions
- no model/API/MCP/browser egress
- no service-request assignment
- no worker start
- no escalation from read-only to signed-in or public action

## Identity Envelope Gates

A worker pool may be registered only if:

1. A matching manual decision or approval artifact exists.
2. The identity envelope names the exact worker pool id.
3. The allowed service request types match the pool purpose.
4. Credential, browser, model, MCP, wallet, payment, and public-action scopes are explicit.
5. The envelope has an expiry.
6. The runtime boundary says whether it is report-only or live.
7. The chain-integrity report can count the envelope as a validation layer.

A service request may be assigned only if:

1. The request is approved.
2. The pool exists.
3. The pool has a valid identity envelope.
4. The requested action fits the envelope.
5. Any external egress has a separate egress ledger event.

## Recommended Next Report-Only Builds

1. `agent_identity_envelope_contract_v1`
   - Markdown/JSON contract and negative fixtures.
   - No registration and no live worker use.

2. `worker_pool_operator_decision_contract_v1`
   - Signed decision intake for the 7 existing worker-pool review packets.

3. `agent_egress_event_ledger_v1`
   - Deny-by-default egress event schema that references the identity envelope.

4. `mcp_tool_registry_gate_v1`
   - Local registry of allowed/disabled MCP servers and tools.

## Runtime Boundary

This matrix:

- installed no identity or policy system
- created no credentials
- issued no SPIFFE IDs or SVIDs
- registered no worker pools
- assigned no service requests
- started no workers
- called no model APIs
- called no MCP tools
- opened no browser sessions
- touched no account, wallet, payment, public, marketplace, GitHub, or X state
- changed no external state

