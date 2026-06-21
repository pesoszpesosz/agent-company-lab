# Runtime Start Signed Decision Guard v1

Generated UTC: 2026-06-21T15:44:19Z
Source runtime-start preflight: `E:\agent-company-lab\reports\runtime-start-preflight-v1-validation-20260617.json`
Guard report JSON: `E:\agent-company-lab\reports\runtime-start-signed-decision-guard-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\runtime-start-signed-decision-guard-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `17`
- Runtime start allowed: `False`
- Worker start allowed: `False`
- Decisions applied: `0`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_all` | `accepted` | `True` | `True` |  |
| `positive_preflight_only` | `accepted` | `True` | `True` |  |
| `negative_missing_operator` | `rejected` | `False` | `True` | operator_id_missing |
| `negative_missing_attestation` | `rejected` | `False` | `True` | operator_attestation_missing, preflight_only_attestation_mismatch |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_unknown_pool` | `rejected` | `False` | `True` | worker_pool_id_must_match_local_runtime_adapter_pool |
| `negative_missing_preflight` | `rejected` | `False` | `True` | source_runtime_start_preflight_path_missing |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_runtime_start_preflight_only |
| `negative_runtime_start_allowed` | `rejected` | `False` | `True` | runtime_start_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_wildcard_command_hash` | `rejected` | `False` | `True` | allowed_command_preview_sha256_mismatch |
| `negative_missing_output_artifact` | `rejected` | `False` | `True` | allowed_output_artifact_path_missing |
| `negative_outside_output_artifact` | `rejected` | `False` | `True` | allowed_output_artifact_path_must_stay_inside_lab |
| `negative_missing_trace` | `rejected` | `False` | `True` | allowed_trace_id_missing |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_runtime_process_started` | `rejected` | `False` | `True` | runtime_boundary_runtime_processes_started_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Accepted decisions are accepted only for later preflight.
- This guard applies no approval rows and starts no runtime or worker.
- Actual process execution remains blocked until a separate apply preflight exists and passes.
