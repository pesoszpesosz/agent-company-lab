# MCP Egress Signed Decision Guard v1

Generated UTC: 2026-06-20T21:07:34Z
Target route: `mcp_tool_gateway`
Source intake contract: `E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-20260618.json`
MCP registry validation: `E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-validation-20260617.json`
Egress ledger validation: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json`
Identity validation: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json`
Guard report JSON: `E:\agent-company-lab\reports\mcp-egress-signed-decision-guard-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\mcp-egress-signed-decision-guard-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `44`
- Gateway starts: `0`
- Live egress events: `0`
- MCP servers started: `0`
- MCP servers enabled: `0`
- MCP tool calls: `False`
- Credentials created: `False`
- Worker starts: `0`
- Decisions applied: `0`
- External side effects: `False`

## Required Gates

- `mcp_tool_registry_gate_v1`
- `agent_egress_event_ledger_v1`
- `local_runtime_adapter_pool_identity_envelope_v1`
- `signed_operator_decision_required`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_mcp_route` | `accepted` | `True` | `True` |  |
| `positive_mcp_preflight_only` | `accepted` | `True` | `True` |  |
| `negative_missing_operator` | `rejected` | `False` | `True` | operator_id_missing |
| `negative_missing_attestation` | `rejected` | `False` | `True` | operator_attestation_missing, preflight_only_attestation_mismatch |
| `negative_wrong_attestation` | `rejected` | `False` | `True` | preflight_only_attestation_mismatch |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_wrong_route` | `rejected` | `False` | `True` | route_id_must_match_target_route |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | egress_type_must_match_target_route |
| `negative_missing_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_missing |
| `negative_outside_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_stay_inside_lab |
| `negative_docket_hash_mismatch` | `rejected` | `False` | `True` | source_gateway_docket_sha256_mismatch |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_exact_target_route_preflight_only |
| `negative_missing_required_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_equal_target_route_required_gates, mcp_tool_registry_gate_required, identity_envelope_gate_required, signed_operator_decision_gate_required |
| `negative_extra_unknown_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_equal_target_route_required_gates, unknown_or_extra_gate:unknown_gate |
| `negative_approval_is_apply` | `rejected` | `False` | `True` | approval_is_not_apply_must_be_true |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_worker_registration_allowed` | `rejected` | `False` | `True` | worker_registration_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_runtime_start_allowed` | `rejected` | `False` | `True` | runtime_start_allowed_must_be_false |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_mcp_server_started` | `rejected` | `False` | `True` | mcp_servers_started_must_be_zero |
| `negative_mcp_server_enabled` | `rejected` | `False` | `True` | mcp_servers_enabled_must_be_zero |
| `negative_mcp_tool_call_allowed` | `rejected` | `False` | `True` | mcp_tool_call_allowed_must_be_false |
| `negative_credentials_created` | `rejected` | `False` | `True` | credentials_created_must_be_false |
| `negative_credential_access_allowed` | `rejected` | `False` | `True` | credential_access_allowed_must_be_false |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_model_api_call` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_external_side_effect` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_boundary_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_registered` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_boundary_gateway_started` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_mcp_server_started` | `rejected` | `False` | `True` | runtime_boundary_mcp_servers_started_must_equal_0 |
| `negative_boundary_mcp_server_enabled` | `rejected` | `False` | `True` | runtime_boundary_mcp_servers_enabled_must_equal_0 |
| `negative_boundary_mcp_tool_call_allowed` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_call_allowed_must_equal_False |
| `negative_boundary_credentials_created` | `rejected` | `False` | `True` | runtime_boundary_credentials_created_must_equal_False |
| `negative_boundary_credential_access_allowed` | `rejected` | `False` | `True` | runtime_boundary_credential_access_allowed_must_equal_False |
| `negative_boundary_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_boundary_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_public_action` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_boundary_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

Accepted decisions are accepted only for a later apply-preflight blocker. This guard does not write approvals, mutate service requests, register gateways, enable or start MCP servers, call MCP tools, access credentials, start workers, or perform live egress.

Next action: Build MCP egress apply preflight blocker for the accepted mcp_tool_gateway decision before any gateway registration, MCP server enable/start, MCP tool call, credential access, worker start, or live egress.
