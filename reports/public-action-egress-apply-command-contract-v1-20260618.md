# Public Action Egress Apply Command Contract v1

Generated UTC: 2026-06-20T21:07:36Z
Target route: `public_action_gateway`
Report JSON: `E:\agent-company-lab\reports\public-action-egress-apply-command-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\public-action-egress-apply-command-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `49`
- Apply command allowed: `False`
- Public action allowed: `False`
- Public actions: `False`
- Posts created: `0`
- Forms submitted: `0`
- PRs opened: `0`
- Bounty claims: `0`
- Messages sent: `0`
- Browser sessions started: `0`
- Account actions: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_contract` | `accepted` | `True` | `True` |  |
| `negative_wrong_route` | `rejected` | `False` | `True` | target_route_id_must_match_public_action_gateway |
| `negative_wrong_egress_type` | `rejected` | `False` | `True` | target_egress_type_must_be_public_submission |
| `negative_missing_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_outside_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_wrong_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source |
| `negative_wrong_guard_validation` | `rejected` | `False` | `True` | source_guard_validation_path_must_match_current_source |
| `negative_wrong_intake_validation` | `rejected` | `False` | `True` | source_intake_validation_path_must_match_current_source |
| `negative_wrong_gateway_validation` | `rejected` | `False` | `True` | source_gateway_docket_validation_path_must_match_current_source |
| `negative_wrong_egress_ledger_validation` | `rejected` | `False` | `True` | source_egress_ledger_validation_path_must_match_current_source |
| `negative_wrong_expected_status` | `rejected` | `False` | `True` | expected_source_apply_preflight_status_must_match |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_must_be_absent |
| `negative_exact_action_body_approval_present` | `rejected` | `False` | `True` | exact_action_body_approval_must_be_absent, immutable_action_body_sha256_must_be_empty_without_approval |
| `negative_execute_command_type` | `rejected` | `False` | `True` | command_type_must_be_deny_or_report_only_contract |
| `negative_execute_scope` | `rejected` | `False` | `True` | allowed_scope_must_match_command_type |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty |
| `negative_immutable_body_hash_present` | `rejected` | `False` | `True` | immutable_action_body_sha256_must_be_empty_without_approval |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_public_action_allowed` | `rejected` | `False` | `True` | public_action_allowed_must_be_false |
| `negative_public_actions` | `rejected` | `False` | `True` | public_actions_must_be_false |
| `negative_browser_session_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_account_action` | `rejected` | `False` | `True` | account_actions_must_be_false |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_request_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_mcp_tool_call` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_model_api_call` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_external_side_effect_top_level` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_boundary_apply_commands_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_boundary_apply_commands_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_boundary_decisions_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_rows_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_registrations` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_boundary_gateway_starts` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress_events` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_posts_created` | `rejected` | `False` | `True` | runtime_boundary_posts_created_must_equal_0 |
| `negative_boundary_forms_submitted` | `rejected` | `False` | `True` | runtime_boundary_forms_submitted_must_equal_0 |
| `negative_boundary_prs_opened` | `rejected` | `False` | `True` | runtime_boundary_prs_opened_must_equal_0 |
| `negative_boundary_bounty_claims` | `rejected` | `False` | `True` | runtime_boundary_bounty_claims_must_equal_0 |
| `negative_boundary_messages_sent` | `rejected` | `False` | `True` | runtime_boundary_messages_sent_must_equal_0 |
| `negative_boundary_browser_sessions_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_boundary_account_actions` | `rejected` | `False` | `True` | runtime_boundary_account_actions_must_equal_False |
| `negative_boundary_worker_starts` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_service_requests_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_boundary_payment_actions` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_boundary_external_side_effects` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This contract is report-only and writes no apply command.
- Public action execution remains blocked until a real signed decision, exact action-body approval, and executable command preview exist.
- No post, form submission, PR, bounty claim, message send, browser mutation, account action, service-request mutation, worker start, or live egress is allowed.

Next action: Build public action egress apply-command guard v1 only after a real signed operator decision, exact action-body approval, and executable command preview exist; until then, keep public egress blocked.
