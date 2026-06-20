# Runtime Process Egress Signed Decision Guard v1

Generated UTC: 2026-06-20T21:07:37Z
Target route: `runtime_process_gateway`
Guard report JSON: `E:\agent-company-lab\reports\runtime-process-egress-signed-decision-guard-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\runtime-process-egress-signed-decision-guard-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `43`
- Runtime start allowed: `False`
- Runtime starts: `0`
- Worker starts: `0`
- Dependency installs: `0`
- External side effects: `False`

## Required Gates

- `runtime_start_preflight_v1`
- `runtime_start_signed_decision_guard_v1`
- `runtime_start_apply_preflight_blocker_v1`
- `runtime_dependency_install_preflight_v1`
- `agent_egress_event_ledger_v1`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_runtime_process_route` | `accepted` | `True` | `True` |  |
| `positive_runtime_process_preflight_only` | `accepted` | `True` | `True` |  |
| `negative_missing_operator` | `rejected` | `False` | `True` | operator_id_required |
| `negative_missing_attestation` | `rejected` | `False` | `True` | operator_attestation_required, operator_attestation_must_match_exact_runtime_process_text |
| `negative_wrong_attestation` | `rejected` | `False` | `True` | operator_attestation_must_match_exact_runtime_process_text |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_utc_must_be_after_signed_utc, decision_expired |
| `negative_wrong_route` | `rejected` | `False` | `True` | route_id_must_match_runtime_process_gateway |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | egress_type_must_be_runtime_start |
| `negative_missing_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_match |
| `negative_outside_docket_path` | `rejected` | `False` | `True` | source_gateway_docket_path_must_match, source_gateway_docket_path_must_stay_inside_lab |
| `negative_docket_hash_mismatch` | `rejected` | `False` | `True` | source_gateway_docket_sha256_mismatch |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_exact_preflight_scope |
| `negative_missing_required_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_match_route_required_gates, missing_required_gate:runtime_start_signed_decision_guard_v1, missing_required_gate:runtime_start_apply_preflight_blocker_v1, missing_required_gate:runtime_dependency_install_preflight_v1 |
| `negative_extra_unknown_gate` | `rejected` | `False` | `True` | allowed_gate_ids_must_match_route_required_gates |
| `negative_approval_is_apply` | `rejected` | `False` | `True` | approval_is_not_apply_must_be_true |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_worker_registration_allowed` | `rejected` | `False` | `True` | worker_registration_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_runtime_start_allowed` | `rejected` | `False` | `True` | runtime_start_allowed_must_be_false |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_dependency_install` | `rejected` | `False` | `True` | dependency_installs_must_be_zero |
| `negative_runtime_started` | `rejected` | `False` | `True` | runtime_starts_must_be_zero |
| `negative_worker_started` | `rejected` | `False` | `True` | worker_starts_must_be_zero |
| `negative_queue_mutation` | `rejected` | `False` | `True` | queue_mutations_must_be_zero |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_model_api_call` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_external_side_effect` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_boundary_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_started` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_dependency_install` | `rejected` | `False` | `True` | runtime_boundary_dependency_installs_must_equal_0 |
| `negative_boundary_runtime_started` | `rejected` | `False` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_boundary_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_queue_mutation` | `rejected` | `False` | `True` | runtime_boundary_queue_mutations_must_equal_0 |
| `negative_boundary_service_request_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_boundary_mcp_tool_call` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_boundary_model_api_call` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_boundary_payment_action` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_boundary_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This guard is report-only.
- Accepted decisions are accepted only for a later apply preflight.
- No dependency install, runtime process start, worker start, queue mutation, service-request mutation, MCP/model call, or live egress is allowed.

Next action: Build runtime_process_gateway apply preflight blocker before any dependency install, runtime process start, worker start, queue mutation, service-request mutation, or live egress.
