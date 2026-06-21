# Model API Egress Signed Decision Guard v1

Generated UTC: 2026-06-21T15:44:15Z
Target route: `model_api_gateway`
Source intake contract: `E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-20260618.json`
Egress ledger validation: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json`
Identity validation: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json`
Guard report JSON: `E:\agent-company-lab\reports\model-api-egress-signed-decision-guard-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\model-api-egress-signed-decision-guard-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `50`
- Provider keys used: `False`
- Model/API call allowed: `False`
- Model/API calls: `False`
- Training data uploaded: `False`
- Max cost USD: `0`
- Gateway starts: `0`
- Live egress events: `0`
- Worker starts: `0`
- External side effects: `False`

## Required Gates

- `model_api_execution_gate`
- `secrets_credentials_handling_gate`
- `agent_egress_event_ledger_v1`
- `cost_budget_signed_decision`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_model_api_route` | `accepted` | `True` | `True` |  |
| `positive_model_api_preflight_only` | `accepted` | `True` | `True` |  |
| `negative_missing_operator` | `rejected` | `False` | `True` | operator_id_required |
| `negative_missing_attestation` | `rejected` | `False` | `True` | operator_attestation_required, operator_attestation_must_match_exact_model_api_text |
| `negative_wrong_attestation` | `rejected` | `False` | `True` | operator_attestation_must_match_exact_model_api_text |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_utc_must_be_after_signed_utc, decision_expired |
| `negative_wrong_route` | `rejected` | `False` | `True` | route_id_must_match_model_api_gateway |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | egress_type_must_be_model_api |
| `negative_missing_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_match |
| `negative_outside_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_match, source_gateway_docket_path_must_stay_inside_lab |
| `negative_docket_hash_mismatch` | `rejected` | `False` | `True` | source_gateway_docket_sha256_mismatch |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_exact_preflight_scope |
| `negative_missing_required_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_match_route_required_gates, missing_required_gate:model_api_execution_gate, missing_required_gate:secrets_credentials_handling_gate, missing_required_gate:cost_budget_signed_decision |
| `negative_extra_unknown_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_match_route_required_gates |
| `negative_approval_is_apply` | `rejected` | `False` | `True` | approval_is_not_apply_must_be_true |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_worker_registration_allowed` | `rejected` | `False` | `True` | worker_registration_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_runtime_start_allowed` | `rejected` | `False` | `True` | runtime_start_allowed_must_be_false |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_provider_key_use_allowed` | `rejected` | `False` | `True` | provider_key_use_allowed_must_be_false |
| `negative_provider_keys_used` | `rejected` | `False` | `True` | provider_keys_used_must_be_false |
| `negative_model_api_call_allowed` | `rejected` | `False` | `True` | model_api_call_allowed_must_be_false |
| `negative_model_api_called` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_training_data_upload_allowed` | `rejected` | `False` | `True` | training_data_upload_allowed_must_be_false |
| `negative_training_data_uploaded` | `rejected` | `False` | `True` | training_data_uploaded_must_be_false |
| `negative_positive_cost` | `rejected` | `False` | `True` | max_cost_usd_must_be_zero |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_external_side_effect` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_boundary_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_registered` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_boundary_gateway_started` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_provider_key_use_allowed` | `rejected` | `False` | `True` | runtime_boundary_provider_key_use_allowed_must_equal_False |
| `negative_boundary_provider_keys_used` | `rejected` | `False` | `True` | runtime_boundary_provider_keys_used_must_equal_False |
| `negative_boundary_model_api_call_allowed` | `rejected` | `False` | `True` | runtime_boundary_model_api_call_allowed_must_equal_False |
| `negative_boundary_model_api_called` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_boundary_training_upload_allowed` | `rejected` | `False` | `True` | runtime_boundary_training_data_upload_allowed_must_equal_False |
| `negative_boundary_training_uploaded` | `rejected` | `False` | `True` | runtime_boundary_training_data_uploaded_must_equal_False |
| `negative_boundary_positive_cost` | `rejected` | `False` | `True` | runtime_boundary_max_cost_usd_must_equal_0 |
| `negative_boundary_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_False |
| `negative_boundary_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_boundary_service_request_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_boundary_mcp_tool_call` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_boundary_payment_action` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_boundary_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

Accepted decisions are accepted only for a later apply-preflight blocker. This guard does not use provider keys, call models, upload data, spend money, mutate service requests, start workers, or perform live egress.

Next action: Build model API egress apply preflight blocker for the accepted model_api_gateway decision before any provider key use, model/API call, data upload, worker start, service-request mutation, or live egress.
