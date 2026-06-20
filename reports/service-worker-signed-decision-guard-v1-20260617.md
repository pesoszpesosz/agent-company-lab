# Service Worker Signed Decision Guard v1

Generated UTC: 2026-06-20T21:07:38Z
Guard report JSON: `E:\agent-company-lab\reports\service-worker-signed-decision-guard-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\service-worker-signed-decision-guard-v1-validation-20260617.json`
Source intake contract: `E:\agent-company-lab\reports\service-worker-signed-decision-intake-contract-v1-20260617.json`

## Summary

- All checks passed: `True`
- Guard status: `report_only_signed_decision_guard_ready`
- Accepted fixtures: `3`
- Rejected fixtures: `24`
- Apply allowed: `False`
- Decisions applied: `0`
- Service requests assigned: `0`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_browser` | `accepted` | `True` | `True` |  |
| `positive_review_legal` | `accepted` | `True` | `True` |  |
| `positive_assignment_browser` | `accepted` | `True` | `True` |  |
| `negative_missing_operator` | `rejected` | `False` | `True` | operator_id_missing |
| `negative_missing_attestation` | `rejected` | `False` | `True` | operator_attestation_missing |
| `negative_weak_attestation` | `rejected` | `False` | `True` | operator_attestation_must_include_report_only_boundary |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_expires_before_signed` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_missing_contract` | `rejected` | `False` | `True` | source_intake_contract_path_missing |
| `negative_outside_contract` | `rejected` | `False` | `True` | source_intake_contract_path_must_stay_inside_lab |
| `negative_unknown_service` | `rejected` | `False` | `True` | service_id_not_found_in_intake_contract, allowed_scope_must_start_with_service_id |
| `negative_wrong_request_type` | `rejected` | `False` | `True` | request_type_must_match_template |
| `negative_decision_not_allowed_for_service` | `rejected` | `False` | `True` | decision_not_allowed_for_service_template |
| `negative_broad_scope` | `rejected` | `False` | `True` | allowed_scope_must_be_exact_not_broad, allowed_scope_must_start_with_service_id |
| `negative_missing_request_ids_for_non_deny` | `rejected` | `False` | `True` | non_deny_decision_requires_bound_request_ids |
| `negative_unknown_request_id` | `rejected` | `False` | `True` | allowed_request_ids_unknown_for_template:req-does-not-exist |
| `negative_exact_scope_false` | `rejected` | `False` | `True` | exact_scope_required_must_be_true |
| `negative_approval_is_apply` | `rejected` | `False` | `True` | approval_is_not_apply_must_be_true |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_approval_row_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_service_request_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_False |
| `negative_api_called` | `rejected` | `False` | `True` | runtime_boundary_api_calls_must_equal_False |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Accepted decisions are accepted only for later apply preflight.
- This guard applies no approval, rejection, queue mutation, worker start, browser session, API call, or external side effect.
