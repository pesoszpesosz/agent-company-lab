# MCP Egress Apply Preflight Blocker v1

Generated UTC: 2026-06-20T21:07:34Z
Target route: `mcp_tool_gateway`
Guard validation: `E:\agent-company-lab\reports\mcp-egress-signed-decision-guard-v1-validation-20260618.json`
MCP registry validation: `E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-validation-20260617.json`
Egress ledger validation: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json`
Identity validation: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\mcp-egress-apply-preflight-blocker-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\mcp-egress-apply-preflight-blocker-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Apply preflight status: `blocked_no_real_signed_decision`
- Blocker reason: `no_real_signed_operator_mcp_egress_decision_artifact`
- Real signed decision present: `False`
- MCP apply guard present: `True`
- Apply allowed: `False`
- Gateway registration allowed: `False`
- Gateway start allowed: `False`
- Live egress allowed: `False`
- MCP server enable allowed: `False`
- MCP tool call allowed: `False`
- MCP servers started: `0`
- MCP servers enabled: `0`
- Credentials created: `False`
- Worker start allowed: `False`
- External side effects: `False`

## Checks

| Check | Passed | Detail |
| --- | --- | --- |
| `gateway_docket_validation_passes` | `True` | E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-validation-20260618.json |
| `signed_decision_intake_validation_passes` | `True` | E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-validation-20260618.json |
| `mcp_signed_decision_guard_passes_for_target_route` | `True` | E:\agent-company-lab\reports\mcp-egress-signed-decision-guard-v1-validation-20260618.json |
| `mcp_registry_gate_validation_passes` | `True` | E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-validation-20260617.json |
| `agent_egress_event_ledger_validation_passes` | `True` | E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json |
| `identity_envelope_validation_passes` | `True` | E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json |
| `real_signed_decision_absent` | `True` | No real signed operator egress-route decision artifact was supplied. |
| `mcp_apply_guard_missing_without_apply` | `True` | E:\agent-company-lab\reports\mcp-egress-apply-command-guard-v1-validation-20260618.json |

## Boundary

This blocker writes reports only. It writes no apply command, executes no command, registers no gateway, enables or starts no MCP server, calls no MCP tool, accesses no credentials, starts no worker, mutates no service request, and performs no live egress.

Next action: Provide a real signed operator MCP egress-route decision artifact, then build an MCP apply-command guard before any gateway registration, MCP server enable/start, MCP tool call, credential access, worker start, or live egress can be considered.
