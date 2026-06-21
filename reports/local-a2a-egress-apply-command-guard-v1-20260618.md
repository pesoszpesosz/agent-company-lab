# Local A2A Egress Apply Command Guard v1

Generated UTC: 2026-06-21T15:44:12Z
Target route: `local_agent_to_agent_report_only`
Apply command contract validation: `E:\agent-company-lab\reports\local-a2a-egress-apply-command-contract-v1-validation-20260618.json`
Report JSON: `E:\agent-company-lab\reports\local-a2a-egress-apply-command-guard-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\local-a2a-egress-apply-command-guard-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `39`
- Apply command allowed: `False`
- Apply allowed: `False`
- Gateway start allowed: `False`
- Live egress allowed: `False`
- Agent message send allowed: `False`
- Agent messages sent: `0`
- Worker start allowed: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_guard` | `accepted` | `True` | `True` |  |
| `negative_wrong_route` | `rejected` | `False` | `True` | target_route_id_must_match_local_agent_to_agent_report_only |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | target_egress_type_must_be_agent_to_agent |
| `negative_missing_contract_source` | `rejected` | `False` | `True` | source_apply_command_contract_path_missing |
| `negative_outside_contract_source` | `rejected` | `False` | `True` | source_apply_command_contract_path_must_stay_inside_lab |
| `negative_wrong_contract_source` | `rejected` | `False` | `True` | source_apply_command_contract_path_must_match_current_source |
| `negative_wrong_preflight_source` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source |
| `negative_wrong_signed_guard_source` | `rejected` | `False` | `True` | source_signed_guard_validation_path_must_match_current_source |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_present_must_be_false_for_guard_only, real_signed_decision_path_must_be_empty_for_guard_only |
| `negative_execute_command_type` | `rejected` | `False` | `True` | command_type_invalid |
| `negative_execute_scope` | `rejected` | `False` | `True` | report_only_guard_scope_must_match |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty_without_real_signed_decision |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_agent_message_send_allowed` | `rejected` | `False` | `True` | agent_message_send_allowed_must_be_false |
| `negative_agent_messages_sent` | `rejected` | `False` | `True` | agent_messages_sent_must_be_zero |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_model_api_call` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_browser_started` | `rejected` | `False` | `True` | browser_sessions_started_must_be_zero |
| `negative_external_side_effect_top_level` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_command_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_command_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_approval_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_gateway_registered` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_gateway_started` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_live_egress` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_agent_message_boundary_allowed` | `rejected` | `False` | `True` | runtime_boundary_agent_message_send_allowed_must_equal_False |
| `negative_agent_message_boundary_sent` | `rejected` | `False` | `True` | runtime_boundary_agent_messages_sent_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_service_request_boundary` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_public_action` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_external_side_effect_boundary` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

This guard validates report-only local A2A command guard shapes. It writes no command, executes no command, registers no gateway, starts no gateway, sends no agent message, starts no worker, mutates no service request, calls no model/API or MCP tool, opens no browser, and performs no live egress.

Next action: Keep local A2A egress blocked until a real signed operator local A2A egress decision and exact command preview exist; no agent message send, service-request mutation, worker start, or live egress is permitted by this guard.
