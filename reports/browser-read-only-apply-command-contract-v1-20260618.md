# Browser Read-Only Apply Command Contract v1

Generated UTC: 2026-06-21T15:44:05Z
Apply preflight validation: `E:\agent-company-lab\reports\browser-read-only-apply-preflight-blocker-v1-validation-20260617.json`
Guard validation: `E:\agent-company-lab\reports\browser-read-only-signed-approval-guard-v1-validation-20260617.json`
Adapter contract validation: `E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-validation-20260618.json`
Contract report JSON: `E:\agent-company-lab\reports\browser-read-only-apply-command-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\browser-read-only-apply-command-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `27`
- Source apply preflight status: `blocked_no_real_signed_decision`
- Source guard adapter contract gate: `present_valid_start_blocked`
- Apply command allowed: `False`
- Apply allowed: `False`
- Assignment allowed: `False`
- Browser session start allowed: `False`
- Worker start allowed: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_contract` | `accepted` | `True` | `True` |  |
| `negative_missing_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab, source_apply_preflight_blocker_path_missing |
| `negative_outside_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_wrong_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_match_current_validation |
| `negative_wrong_guard_validation` | `rejected` | `False` | `True` | source_guard_validation_path_must_match_current_source, source_guard_validation_path_must_match_current_guard |
| `negative_wrong_adapter_validation` | `rejected` | `False` | `True` | source_adapter_contract_validation_path_must_match_current_source, source_adapter_contract_validation_path_must_match_current_contract |
| `negative_wrong_expected_status` | `rejected` | `False` | `True` | expected_source_apply_preflight_status_must_match_source |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_present_must_be_false, real_signed_decision_path_must_be_empty_for_contract_only |
| `negative_execute_command_type` | `rejected` | `False` | `True` | command_type_must_be_deny_or_report_only_contract, command_type_invalid |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_match_command_type, report_only_contract_scope_must_match |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty, target_request_ids_must_be_empty_without_real_signed_decision |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_assignment_allowed` | `rejected` | `False` | `True` | assignment_allowed_must_be_false |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_command_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_command_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_decision_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_service_request_mutated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_mutated_must_equal_0 |
| `negative_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_login_action` | `rejected` | `False` | `True` | runtime_boundary_login_actions_must_equal_False |
| `negative_public_action` | `rejected` | `False` | `True` | runtime_boundary_public_actions_must_equal_False |
| `negative_payment_action` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This contract validates command-shaped fixtures only.
- It writes no apply command and executes no command.
- It assigns no service requests, starts no browser sessions, and starts no workers.
- Target request IDs must remain empty until a real signed operator decision artifact and a separate apply preflight exist.
