# MCP Tool Registry Gate Packet v1

Generated UTC: 2026-06-17T19:11:11Z

Lane: platform_engineering

Task: task-mcp-tool-registry-gate-packet-v1-20260617

## Purpose

This packet defines the local gate required before any future agent-company worker can call an MCP server or MCP tool.

Default policy: every MCP server and tool is disabled unless registered, scoped, reviewed, and tied to an identity envelope plus egress event.

## Inputs

- Egress ledger packet: `E:\agent-company-lab\reports\agent-egress-event-ledger-packet-v1-20260617.json`
- Identity envelope matrix: `E:\agent-company-lab\reports\agent-identity-envelope-matrix-v1-20260617.json`
- Gateway matrix: `E:\agent-company-lab\reports\agent-company-gateway-candidate-matrix-v1-20260617.json`
- Current chain integrity validation: `E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json`

## Current Source Signals

Current MCP ecosystem signals point to the same pattern:

- registries are becoming the control point for server discovery, metadata, trust, and enterprise curation
- server/tool inventory must be explicit
- unknown tools should be disabled by default
- every tool call needs audit correlation
- OAuth/SSO, workload identity, DPoP, and secure credential handling are active MCP roadmap areas
- prompt/tool injection, overbroad tool access, server rug-pulls, and implicit credentials are core risks

## Fresh Repository Metadata

Collected from GitHub API on 2026-06-17.

| Repository | Stars | Forks | Language | Last pushed UTC | License | Notes |
| --- | ---: | ---: | --- | --- | --- | --- |
| `modelcontextprotocol/servers` | 87382 | 11020 | TypeScript | 2026-06-17T01:40:52Z | NOASSERTION | Large reference set of MCP servers. High surface area; not a governance control by itself. |
| `BerriAI/litellm` | 50717 | 8961 | Python | 2026-06-17T19:07:52Z | NOASSERTION | Future model/MCP gateway candidate. |
| `Kong/kong` | 43604 | 5151 | Lua | 2026-06-17T08:27:14Z | Apache-2.0 | API/AI gateway reference for mature traffic governance. |
| `github/github-mcp-server` | 30768 | 4406 | Go | 2026-06-17T16:51:35Z | MIT | Official GitHub MCP server; high value but public-action risk if write tools are enabled. |
| `modelcontextprotocol/registry` | 6936 | 869 | Go | 2026-06-10T23:33:38Z | NOASSERTION | Community-driven MCP server registry. |
| `stacklok/toolhive` | 1888 | 229 | Go | 2026-06-17T18:54:17Z | Apache-2.0 | Enterprise-grade platform for running and managing MCP servers. |
| `agentic-community/mcp-gateway-registry` | 711 | 192 | Python | 2026-06-17T13:06:48Z | Apache-2.0 | MCP gateway and registry with OAuth, dynamic discovery, and governed access. |

## Registry Entry Contract

Every MCP server entry must include:

- `mcp_registry_entry_id`
- `server_id`
- `server_name`
- `server_source_type`: `official_registry`, `github_registry`, `local_manifest`, `vendor_gateway`, `manual_review`
- `source_url`
- `package_or_endpoint`
- `publisher`
- `publisher_verification`
- `version`
- `digest_or_commit`
- `license`
- `risk_tier`: `low`, `medium`, `high`, `blocked`
- `default_status`: `disabled`
- `allowed_lanes`
- `allowed_agent_ids`
- `allowed_worker_pool_ids`
- `allowed_identity_envelope_ids`
- `allowed_tools`
- `blocked_tools`
- `credential_requirements`
- `oauth_or_auth_mode`
- `network_scope`
- `data_sensitivity_ceiling`
- `write_action_capable`
- `public_action_capable`
- `payment_or_wallet_capable`
- `file_system_capable`
- `browser_capable`
- `rate_limit_scope`
- `budget_scope`
- `logging_required`
- `recording_required`
- `redaction_required`
- `review_artifact_path`
- `approval_artifact_path`
- `egress_event_required`
- `created_utc`
- `expires_utc`
- `revocation_status`

## Tool Entry Contract

Every tool exposed by a registered server must include:

- `tool_id`
- `server_id`
- `tool_name`
- `tool_description`
- `tool_input_schema_artifact_path`
- `tool_output_schema_artifact_path`
- `tool_side_effect_class`: `read_only`, `local_mutation`, `external_read`, `external_write`, `public_action`, `payment_wallet`, `credential_access`
- `allowed_input_artifact_types`
- `required_output_artifact_type`
- `requires_operator_decision`
- `requires_identity_envelope`
- `requires_egress_event`
- `requires_post_execution_evidence`
- `default_policy_verdict`: `deny`
- `risk_reasons`

## Status Model

Allowed registry statuses:

- `disabled`
- `under_review`
- `approved_report_only`
- `approved_preflight_only`
- `approved_live_read_only`
- `blocked`
- `revoked`

No status in this packet approves live write/public/payment/account/credential actions.

## Validation Rules

An MCP tool call may be considered only if:

1. The MCP server is registered.
2. The MCP tool is registered.
3. The server status is not `disabled`, `blocked`, or `revoked`.
4. The tool default policy does not exceed the server status.
5. The agent has a valid identity envelope.
6. The identity envelope allows this server and tool.
7. The egress event references the server and tool.
8. The operator decision allows the exact next action.
9. Credentials are explicit and not inferred.
10. Input and output artifact paths are declared.
11. Any public/write/payment/account/credential action pauses for review or remains denied.
12. Tool call audit must include a correlation id spanning agent, egress event, server, tool, and output artifact.

## Negative Fixtures

Future validators must reject:

| Fixture id | Reason |
| --- | --- |
| `unknown_server` | Server not in registry. |
| `unknown_tool` | Tool not in server entry. |
| `disabled_server_call` | Server disabled by default. |
| `revoked_server_call` | Server explicitly revoked. |
| `implicit_credentials` | Credential authority is vague or inherited. |
| `missing_identity_envelope` | Tool call has no principal scope. |
| `identity_scope_mismatch` | Identity envelope does not allow server/tool. |
| `missing_egress_event` | No egress evidence row. |
| `missing_operator_decision` | Required approval artifact absent. |
| `write_tool_as_read_only` | Tool with side effects mislabeled read-only. |
| `public_action_without_cro` | Public tool call lacks CRO/reputation gate. |
| `wallet_payment_tool_non_deny` | Wallet/payment tool not denied. |
| `missing_schema_artifacts` | Tool schema not captured. |
| `missing_output_artifact` | Output evidence path absent. |
| `unbounded_rate_or_budget` | Rate/cost scope missing. |

## Candidate First Registry Entries

These are candidate review entries only, not approvals:

| Candidate | Proposed status | Rationale | Required blocker |
| --- | --- | --- | --- |
| `local-report-only-fixture-mcp` | `approved_report_only` | Safe local fixture for validating registry schema with no server start. | Contract validator required |
| `github-mcp-server-read-only-subset` | `under_review` | High utility for paid-code/bounty work, but write/public tools are dangerous. | Explicit tool allowlist and public-action block |
| `browser-automation-mcp-read-only` | `under_review` | Useful for research workers, but browser session boundaries must be explicit. | Browser scope, recording, teardown policy |
| `unknown-public-registry-server` | `disabled` | Default posture for any discovered but unreviewed server. | Manual review required |

## Runtime Boundary

This packet:

- starts no MCP server
- installs no MCP server
- enables no MCP server
- calls no MCP tools
- creates no OAuth app, API key, token, or credential
- performs no registry publication
- changes no GitHub, marketplace, account, wallet, payment, or public state
- opens no browser session
- starts no worker
- assigns no service request
- changes no external state

## Sources

- GitHub MCP Registry: https://github.com/mcp
- Official MCP Registry: https://registry.modelcontextprotocol.io/
- Model Context Protocol roadmap: https://modelcontextprotocol.io/development/roadmap
- GitHub MCP Registry blog: https://github.blog/ai-and-ml/generative-ai/how-to-find-install-and-manage-mcp-servers-with-the-github-mcp-registry/
- OWASP MCP Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html
- Microsoft MCP security/governance: https://www.microsoft.com/insidetrack/blog/protecting-ai-conversations-at-microsoft-with-model-context-protocol-security-and-governance/
- Palo Alto MCP controls: https://www.paloaltonetworks.com/blog/identity-security/secure-ai-agents-controls-visibility-mcp-data-access/
- agentic-community MCP Gateway Registry: https://github.com/agentic-community/mcp-gateway-registry
- Stacklok ToolHive: https://github.com/stacklok/toolhive
- Kong MCP Registry: https://konghq.com/products/mcp-registry

## Decision

Recommended next report-only build: `mcp_tool_registry_gate_contract_v1` schema, fixture set, and validator design after implementation-design approval.

