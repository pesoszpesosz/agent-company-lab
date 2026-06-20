# Browser Read-Only Signed Approval Guard v1

Generated UTC: 2026-06-20T21:07:29Z
Source assignment preflight: `E:\agent-company-lab\reports\browser-read-only-assignment-preflight-v1-validation-20260617.json`
Guard report JSON: `E:\agent-company-lab\reports\browser-read-only-signed-approval-guard-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\browser-read-only-signed-approval-guard-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `26`
- Assignment allowed: `False`
- Browser session start allowed: `False`
- Worker start allowed: `False`
- Adapter contract gate: `present_valid_start_blocked`
- Adapter contract validation: `E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-validation-20260618.json`
- Decisions applied: `0`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_all` | `accepted` | `True` | `True` |  |
| `positive_preflight_only` | `accepted` | `True` | `True` |  |
| `negative_missing_operator` | `rejected` | `False` | `True` | operator_id_missing |
| `negative_missing_attestation` | `rejected` | `False` | `True` | operator_attestation_missing, preflight_only_attestation_mismatch |
| `negative_wrong_attestation` | `rejected` | `False` | `True` | preflight_only_attestation_mismatch |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_expires_before_signed` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_missing_preflight` | `rejected` | `False` | `True` | source_assignment_preflight_path_missing |
| `negative_outside_preflight` | `rejected` | `False` | `True` | source_assignment_preflight_path_must_stay_inside_lab |
| `negative_missing_adapter_contract_path` | `rejected` | `False` | `True` | source_adapter_contract_validation_path_missing |
| `negative_wrong_adapter_contract_path` | `rejected` | `False` | `True` | source_adapter_contract_validation_path_must_stay_inside_lab |
| `negative_stale_adapter_contract_path` | `rejected` | `False` | `True` | source_adapter_contract_validation_path_must_match_source_preflight |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_browser_read_only_assignment_preflight_only |
| `negative_assignment_allowed` | `rejected` | `False` | `True` | assignment_allowed_must_be_false |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_missing_candidate_ids` | `rejected` | `False` | `True` | allowed_candidate_request_ids_missing, allowed_candidate_request_ids_must_match_current_candidates |
| `negative_unknown_candidate_id` | `rejected` | `False` | `True` | allowed_candidate_request_ids_unknown:req-unknown-browser, allowed_candidate_request_ids_must_match_current_candidates |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_approval_row_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_service_request_mutated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_mutated_must_equal_0 |
| `negative_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_login_action` | `rejected` | `False` | `True` | runtime_boundary_login_actions_must_equal_False |
| `negative_public_action` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_payment_action` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Accepted decisions are accepted only for later assignment preflight.
- This guard applies no approval rows, assigns no service requests, starts no workers, and opens no browsers.
- Any future apply command must re-check exact candidate IDs, operator authority, queue state, and zero side effects.
