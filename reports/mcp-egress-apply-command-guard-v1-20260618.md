# MCP Egress Apply Command Guard v1

Generated UTC: 2026-06-20T21:07:34Z
Target route: `mcp_tool_gateway`
Apply preflight validation: `E:\agent-company-lab\reports\mcp-egress-apply-preflight-blocker-v1-validation-20260618.json`
MCP registry validation: `E:\agent-company-lab\reports\mcp-tool-registry-gate-v1-validation-20260617.json`
Egress ledger validation: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json`
Identity validation: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\mcp-egress-apply-command-guard-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\mcp-egress-apply-command-guard-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `49`
- Apply command allowed: `False`
- Apply allowed: `False`
- Gateway start allowed: `False`
- Live egress allowed: `False`
- MCP server enable allowed: `False`
- MCP tool call allowed: `False`
- MCP servers started: `0`
- MCP servers enabled: `0`
- Credentials created: `False`
- Worker start allowed: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_guard` | `accepted` | `True` | `True` |  |
| `negative_wrong_route` | `rejected` | `False` | `True` | target_route_id_must_match_mcp_tool_gateway |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | target_egress_type_must_match_mcp_tool |
| `negative_missing_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_missing |
| `negative_outside_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_wrong_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_validation |
| `negative_wrong_guard_validation` | `rejected` | `False` | `True` | source_guard_validation_path_must_match_current_source |
| `negative_wrong_intake_validation` | `rejected` | `False` | `True` | source_intake_validation_path_must_match_current_source |
| `negative_wrong_gateway_validation` | `rejected` | `False` | `True` | source_gateway_docket_validation_path_must_match_current_source |
| `negative_wrong_expected_status` | `rejected` | `False` | `True` | expected_source_apply_preflight_status_must_match_source |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_present_must_be_false, real_signed_decision_path_must_be_empty_for_guard_only |
| `negative_execute_command_type` | `rejected` | `False` | `True` | command_type_invalid |
| `negative_execute_scope` | `rejected` | `False` | `True` | report_only_guard_scope_must_match |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty_without_real_signed_decision |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_mcp_server_enable_allowed` | `rejected` | `False` | `True` | mcp_server_enable_allowed_must_be_false |
| `negative_mcp_tool_call_allowed` | `rejected` | `False` | `True` | mcp_tool_call_allowed_must_be_false |
| `negative_mcp_server_started` | `rejected` | `False` | `True` | mcp_servers_started_must_be_zero |
| `negative_mcp_server_enabled` | `rejected` | `False` | `True` | mcp_servers_enabled_must_be_zero |
| `negative_credentials_created` | `rejected` | `False` | `True` | credentials_created_must_be_false |
| `negative_credential_access_allowed` | `rejected` | `False` | `True` | credential_access_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_model_api_call` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_external_side_effect_top_level` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_command_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_command_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_approval_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_gateway_registered` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_gateway_started` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_live_egress` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_mcp_server_enable_allowed` | `rejected` | `False` | `True` | runtime_boundary_mcp_server_enable_allowed_must_equal_False |
| `negative_boundary_mcp_tool_call_allowed` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_call_allowed_must_equal_False |
| `negative_boundary_mcp_server_started` | `rejected` | `False` | `True` | runtime_boundary_mcp_servers_started_must_equal_0 |
| `negative_boundary_mcp_server_enabled` | `rejected` | `False` | `True` | runtime_boundary_mcp_servers_enabled_must_equal_0 |
| `negative_boundary_credentials_created` | `rejected` | `False` | `True` | runtime_boundary_credentials_created_must_equal_False |
| `negative_boundary_credential_access_allowed` | `rejected` | `False` | `True` | runtime_boundary_credential_access_allowed_must_equal_False |
| `negative_registry_publication` | `rejected` | `False` | `True` | runtime_boundary_registry_publications_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_service_request_boundary` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_public_action` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_external_side_effect_boundary` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

This guard validates report-only MCP command shapes. It writes no command, executes no command, registers no gateway, enables or starts no MCP server, calls no MCP tool, accesses no credentials, starts no worker, mutates no service request, and performs no live egress.

Next action: Keep MCP egress blocked until a real signed operator MCP egress decision and exact command preview exist; then build an execution guard before any MCP server enable/start, MCP tool call, credential access, worker start, or live egress.
