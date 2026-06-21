# Model API Egress Apply Command Contract v1

Generated UTC: 2026-06-21T15:44:15Z
Target route: `model_api_gateway`
Apply preflight validation: `E:\agent-company-lab\reports\model-api-egress-apply-preflight-blocker-v1-validation-20260618.json`
Report JSON: `E:\agent-company-lab\reports\model-api-egress-apply-command-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\model-api-egress-apply-command-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `47`
- Apply command allowed: `False`
- Apply allowed: `False`
- Provider key use allowed: `False`
- Model/API call allowed: `False`
- Model/API calls: `False`
- Training data uploaded: `False`
- Max cost USD: `0`
- Worker start allowed: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_contract` | `accepted` | `True` | `True` |  |
| `negative_wrong_route` | `rejected` | `False` | `True` | target_route_id_must_match_model_api_gateway |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | target_egress_type_must_be_model_api |
| `negative_missing_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_outside_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_wrong_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source |
| `negative_wrong_guard_validation` | `rejected` | `False` | `True` | source_guard_validation_path_must_match_current_source |
| `negative_wrong_intake_validation` | `rejected` | `False` | `True` | source_intake_validation_path_must_match_current_source |
| `negative_wrong_gateway_validation` | `rejected` | `False` | `True` | source_gateway_docket_validation_path_must_match_current_source |
| `negative_wrong_egress_ledger_validation` | `rejected` | `False` | `True` | source_egress_ledger_validation_path_must_match_current_source |
| `negative_wrong_identity_validation` | `rejected` | `False` | `True` | source_identity_validation_path_must_match_current_source |
| `negative_wrong_expected_status` | `rejected` | `False` | `True` | expected_source_apply_preflight_status_must_match_source |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_present_must_be_false_for_contract_only, real_signed_decision_path_must_be_empty_for_contract_only |
| `negative_execute_command_type` | `rejected` | `False` | `True` | command_type_must_be_deny_or_report_only_contract |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_match_command_type |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_provider_key_use_allowed` | `rejected` | `False` | `True` | provider_key_use_allowed_must_be_false |
| `negative_provider_keys_used` | `rejected` | `False` | `True` | provider_keys_used_must_be_false |
| `negative_model_api_call_allowed` | `rejected` | `False` | `True` | model_api_call_allowed_must_be_false |
| `negative_model_api_called` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_training_data_upload_allowed` | `rejected` | `False` | `True` | training_data_upload_allowed_must_be_false |
| `negative_training_data_uploaded` | `rejected` | `False` | `True` | training_data_uploaded_must_be_false |
| `negative_positive_cost` | `rejected` | `False` | `True` | max_cost_usd_must_be_zero |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_browser_started` | `rejected` | `False` | `True` | browser_sessions_started_must_be_false |
| `negative_external_side_effect_top_level` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_command_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_command_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_approval_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_gateway_registered` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_provider_key_boundary` | `rejected` | `False` | `True` | runtime_boundary_provider_keys_used_must_equal_False |
| `negative_model_call_boundary` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_training_upload_boundary` | `rejected` | `False` | `True` | runtime_boundary_training_data_uploaded_must_equal_False |
| `negative_cost_boundary` | `rejected` | `False` | `True` | runtime_boundary_max_cost_usd_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_service_request_boundary` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_payment_action` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_external_side_effect_boundary` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

This contract validates report-only command shapes. It writes no command, executes no command, uses no provider key, calls no model/API, uploads no data, spends no money, starts no worker, mutates no service request, and performs no live egress.

Next action: Build model API egress apply-command guard v1 only after a real signed operator decision and executable command preview exist; until then, keep model/API egress blocked.
