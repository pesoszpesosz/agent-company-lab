# Telemetry Export Egress Signed Decision Guard v1

Generated UTC: 2026-06-21T15:49:47Z
Target route: `telemetry_export_gateway`
Guard report JSON: `E:\agent-company-lab\reports\telemetry-export-egress-signed-decision-guard-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\telemetry-export-egress-signed-decision-guard-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `68`
- Telemetry exports: `0`
- External trace exports: `0`
- Private prompts uploaded: `0`
- Credentials exported: `0`
- Unredacted logs synced: `0`
- Worker starts: `0`
- External side effects: `False`

## Required Gates

- `telemetry_privacy_export_gate_v1`
- `agent_egress_event_ledger_v1`
- `secrets_credentials_handling_gate`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_telemetry_export_route` | `accepted` | `True` | `True` |  |
| `positive_telemetry_export_preflight_only` | `accepted` | `True` | `True` |  |
| `negative_operator_id` | `rejected` | `False` | `True` | operator_id_required |
| `negative_operator_attestation` | `rejected` | `False` | `True` | operator_attestation_must_match_exact_telemetry_text |
| `negative_expires_utc` | `rejected` | `False` | `True` | expires_utc_must_be_after_signed_utc, decision_expired |
| `negative_route_id` | `rejected` | `False` | `True` | route_id_must_match_telemetry_export_gateway |
| `negative_egress_type` | `rejected` | `False` | `True` | egress_type_must_be_telemetry_export |
| `negative_source_gateway_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_match |
| `negative_source_gateway_docket_sha256` | `rejected` | `False` | `True` | source_gateway_docket_sha256_mismatch |
| `negative_allowed_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_exact_preflight_scope |
| `negative_allowed_gate_ids` | `rejected` | `False` | `True` | allowed_gate_ids_must_match_route_required_gates, missing_required_gate:telemetry_privacy_export_gate_v1, missing_required_gate:secrets_credentials_handling_gate |
| `negative_approval_is_not_apply` | `rejected` | `False` | `True` | approval_is_not_apply_must_be_true |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_telemetry_export_allowed` | `rejected` | `False` | `True` | telemetry_export_allowed_must_be_false |
| `negative_external_trace_export_allowed` | `rejected` | `False` | `True` | external_trace_export_allowed_must_be_false |
| `negative_private_prompt_upload_allowed` | `rejected` | `False` | `True` | private_prompt_upload_allowed_must_be_false |
| `negative_credential_export_allowed` | `rejected` | `False` | `True` | credential_export_allowed_must_be_false |
| `negative_unredacted_log_sync_allowed` | `rejected` | `False` | `True` | unredacted_log_sync_allowed_must_be_false |
| `negative_redaction_policy_approved` | `rejected` | `False` | `True` | redaction_policy_approved_must_be_false |
| `negative_destination_scope_approved` | `rejected` | `False` | `True` | destination_scope_approved_must_be_false |
| `negative_retention_policy_approved` | `rejected` | `False` | `True` | retention_policy_approved_must_be_false |
| `negative_sample_trace_artifact_approved` | `rejected` | `False` | `True` | sample_trace_artifact_approved_must_be_false |
| `negative_worker_registration_allowed` | `rejected` | `False` | `True` | worker_registration_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_runtime_start_allowed` | `rejected` | `False` | `True` | runtime_start_allowed_must_be_false |
| `negative_browser_session_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_service_requests_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_requests_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_mcp_tool_calls` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_model_api_calls` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_public_actions` | `rejected` | `False` | `True` | public_actions_must_be_false |
| `negative_account_actions` | `rejected` | `False` | `True` | account_actions_must_be_false |
| `negative_wallet_actions` | `rejected` | `False` | `True` | wallet_actions_must_be_false |
| `negative_payment_actions` | `rejected` | `False` | `True` | payment_actions_must_be_false |
| `negative_external_side_effects` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_outside_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_match, source_gateway_docket_path_must_stay_inside_lab |
| `negative_extra_unknown_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_match_route_required_gates |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_boundary_decisions_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_rows_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_registrations` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_boundary_gateway_starts` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress_events` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_telemetry_export_allowed` | `rejected` | `False` | `True` | runtime_boundary_telemetry_export_allowed_must_equal_False |
| `negative_boundary_telemetry_exports` | `rejected` | `False` | `True` | runtime_boundary_telemetry_exports_must_equal_0 |
| `negative_boundary_external_trace_export_allowed` | `rejected` | `False` | `True` | runtime_boundary_external_trace_export_allowed_must_equal_False |
| `negative_boundary_external_trace_exports` | `rejected` | `False` | `True` | runtime_boundary_external_trace_exports_must_equal_0 |
| `negative_boundary_private_prompt_upload_allowed` | `rejected` | `False` | `True` | runtime_boundary_private_prompt_upload_allowed_must_equal_False |
| `negative_boundary_private_prompts_uploaded` | `rejected` | `False` | `True` | runtime_boundary_private_prompts_uploaded_must_equal_0 |
| `negative_boundary_credential_export_allowed` | `rejected` | `False` | `True` | runtime_boundary_credential_export_allowed_must_equal_False |
| `negative_boundary_credentials_exported` | `rejected` | `False` | `True` | runtime_boundary_credentials_exported_must_equal_0 |
| `negative_boundary_unredacted_log_sync_allowed` | `rejected` | `False` | `True` | runtime_boundary_unredacted_log_sync_allowed_must_equal_False |
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
| `negative_boundary_public_actions` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_boundary_account_actions` | `rejected` | `False` | `True` | runtime_boundary_account_actions_must_equal_False |
| `negative_boundary_wallet_actions` | `rejected` | `False` | `True` | runtime_boundary_wallet_actions_must_equal_False |
| `negative_boundary_payment_actions` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_boundary_external_side_effects` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

Accepted decisions are accepted only for a later apply-preflight blocker. This guard does not export traces, upload prompts, export credentials, sync logs, mutate service requests, start workers, call models/MCP tools, or perform live egress.

Next action: Build telemetry_export_gateway apply preflight blocker before any external trace export, private prompt upload, credential export, unredacted log sync, service-request mutation, worker start, model/MCP call, live egress, or external side effect.
