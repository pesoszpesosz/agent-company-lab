# Telemetry Export Egress Apply Command Contract v1

Generated UTC: 2026-06-20T21:07:39Z
Target route: `telemetry_export_gateway`
Report JSON: `E:\agent-company-lab\reports\telemetry-export-egress-apply-command-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\telemetry-export-egress-apply-command-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `69`
- Apply command allowed: `False`
- Telemetry export allowed: `False`
- External trace exports: `0`
- Private prompts uploaded: `0`
- Credentials exported: `0`
- Unredacted logs synced: `0`
- Browser sessions started: `0`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_contract` | `accepted` | `True` | `True` |  |
| `negative_target_route_id` | `rejected` | `False` | `True` | target_route_id_must_match_telemetry_export_gateway |
| `negative_target_egress_type` | `rejected` | `False` | `True` | target_egress_type_must_be_telemetry_export |
| `negative_source_apply_preflight_blocker_path` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_source_guard_validation_path` | `rejected` | `False` | `True` | source_guard_validation_path_must_match_current_source |
| `negative_source_intake_validation_path` | `rejected` | `False` | `True` | source_intake_validation_path_must_match_current_source |
| `negative_source_gateway_docket_validation_path` | `rejected` | `False` | `True` | source_gateway_docket_validation_path_must_match_current_source |
| `negative_source_egress_ledger_validation_path` | `rejected` | `False` | `True` | source_egress_ledger_validation_path_must_match_current_source |
| `negative_source_identity_validation_path` | `rejected` | `False` | `True` | source_identity_validation_path_must_match_current_source |
| `negative_expected_source_apply_preflight_status` | `rejected` | `False` | `True` | expected_source_apply_preflight_status_must_match |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_present_and_real_signed_decision_path_must_be_absent |
| `negative_redaction_policy_present` | `rejected` | `False` | `True` | redaction_policy_present_and_redaction_policy_path_must_be_absent |
| `negative_destination_scope_present` | `rejected` | `False` | `True` | destination_scope_present_and_destination_scope_path_must_be_absent |
| `negative_retention_policy_present` | `rejected` | `False` | `True` | retention_policy_present_and_retention_policy_path_must_be_absent |
| `negative_sample_trace_artifact_present` | `rejected` | `False` | `True` | sample_trace_artifact_present_and_sample_trace_artifact_path_must_be_absent |
| `negative_command_type` | `rejected` | `False` | `True` | command_type_must_be_deny_or_report_only_contract |
| `negative_allowed_scope` | `rejected` | `False` | `True` | allowed_scope_must_match_command_type |
| `negative_immutable_command_preview_sha256` | `rejected` | `False` | `True` | immutable_command_preview_sha256_must_be_empty_without_approval |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_telemetry_export_allowed` | `rejected` | `False` | `True` | telemetry_export_allowed_must_be_false |
| `negative_external_trace_export_allowed` | `rejected` | `False` | `True` | external_trace_export_allowed_must_be_false |
| `negative_private_prompt_upload_allowed` | `rejected` | `False` | `True` | private_prompt_upload_allowed_must_be_false |
| `negative_credential_export_allowed` | `rejected` | `False` | `True` | credential_export_allowed_must_be_false |
| `negative_unredacted_log_sync_allowed` | `rejected` | `False` | `True` | unredacted_log_sync_allowed_must_be_false |
| `negative_browser_session_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_mcp_tool_calls` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_model_api_calls` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_public_actions` | `rejected` | `False` | `True` | public_actions_must_be_false |
| `negative_account_actions` | `rejected` | `False` | `True` | account_actions_must_be_false |
| `negative_wallet_actions` | `rejected` | `False` | `True` | wallet_actions_must_be_false |
| `negative_payment_actions` | `rejected` | `False` | `True` | payment_actions_must_be_false |
| `negative_real_money_actions` | `rejected` | `False` | `True` | real_money_actions_must_be_false |
| `negative_service_requests_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_requests_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_external_side_effects` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_outside_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_real_signed_decision_path` | `rejected` | `False` | `True` | real_signed_decision_present_and_real_signed_decision_path_must_be_absent |
| `negative_redaction_policy_path` | `rejected` | `False` | `True` | redaction_policy_present_and_redaction_policy_path_must_be_absent |
| `negative_destination_scope_path` | `rejected` | `False` | `True` | destination_scope_present_and_destination_scope_path_must_be_absent |
| `negative_retention_policy_path` | `rejected` | `False` | `True` | retention_policy_present_and_retention_policy_path_must_be_absent |
| `negative_sample_trace_artifact_path` | `rejected` | `False` | `True` | sample_trace_artifact_present_and_sample_trace_artifact_path_must_be_absent |
| `negative_boundary_apply_commands_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_boundary_apply_commands_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_boundary_decisions_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_rows_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_registrations` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_boundary_gateway_starts` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress_events` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_telemetry_exports` | `rejected` | `False` | `True` | runtime_boundary_telemetry_exports_must_equal_0 |
| `negative_boundary_external_trace_exports` | `rejected` | `False` | `True` | runtime_boundary_external_trace_exports_must_equal_0 |
| `negative_boundary_private_prompts_uploaded` | `rejected` | `False` | `True` | runtime_boundary_private_prompts_uploaded_must_equal_0 |
| `negative_boundary_credentials_exported` | `rejected` | `False` | `True` | runtime_boundary_credentials_exported_must_equal_0 |
| `negative_boundary_unredacted_logs_synced` | `rejected` | `False` | `True` | runtime_boundary_unredacted_logs_synced_must_equal_0 |
| `negative_boundary_redaction_policy_approved` | `rejected` | `False` | `True` | runtime_boundary_redaction_policy_approved_must_equal_False |
| `negative_boundary_destination_scope_approved` | `rejected` | `False` | `True` | runtime_boundary_destination_scope_approved_must_equal_False |
| `negative_boundary_retention_policy_approved` | `rejected` | `False` | `True` | runtime_boundary_retention_policy_approved_must_equal_False |
| `negative_boundary_sample_trace_artifact_approved` | `rejected` | `False` | `True` | runtime_boundary_sample_trace_artifact_approved_must_equal_False |
| `negative_boundary_worker_starts` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_runtime_starts` | `rejected` | `False` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_boundary_browser_sessions_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_boundary_service_requests_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_boundary_mcp_tool_calls` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_boundary_model_api_calls` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_boundary_external_side_effects` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This contract is report-only and writes no apply command.
- Telemetry export execution remains blocked until a real signed decision, redaction policy, destination scope, retention policy, sample trace artifact, and immutable command preview exist.
- No external trace export, private prompt upload, credential export, unredacted log sync, service-request mutation, worker start, browser start, model/MCP call, live egress, or external side effect is allowed.

Next action: Build telemetry_export_gateway apply-command guard only after a real signed operator decision, redaction policy, destination scope, retention policy, sample trace artifact, and immutable command preview exist; until then, keep telemetry export egress blocked.
