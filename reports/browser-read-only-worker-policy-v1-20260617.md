# Browser Read-Only Worker Policy v1 Validation

Generated UTC: 2026-06-21T15:44:06Z
Validation JSON: `E:\agent-company-lab\reports\browser-read-only-worker-policy-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\browser-read-only-worker-policy-v1-20260617.json`
Schema: `E:\agent-company-lab\architecture\browser-read-only-worker-policy-v1.schema.json`

## Summary

- All checks passed: `True`
- Policy verdict: `public_read_only_plan_valid_start_blocked`
- Browser session start allowed: `False`
- Worker start allowed: `False`
- Fixtures: `29`
- Accepted: `1`
- Rejected: `28`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_public_read_only_plan_start_blocked` | `accepted` | `True` | `True` |  |
| `negative_missing_service_request` | `rejected` | `False` | `True` | service_request_not_found |
| `negative_wrong_service_id` | `rejected` | `False` | `True` | service_id_must_be_browser_read_only_session |
| `negative_signed_in_session` | `rejected` | `False` | `True` | session_mode_must_be_public_read_only_no_login |
| `negative_unknown_session` | `rejected` | `False` | `True` | session_mode_must_be_public_read_only_no_login |
| `negative_missing_allowlist` | `rejected` | `False` | `True` | allowed_domains_must_be_nonempty, target_url_host_must_be_in_allowed_domains |
| `negative_wildcard_domain` | `rejected` | `False` | `True` | allowed_domains_must_not_use_wildcards, target_url_host_must_be_in_allowed_domains |
| `negative_unbounded_navigation` | `rejected` | `False` | `True` | navigation_scope_must_be_explicit_allowlist_only |
| `negative_target_outside_allowlist` | `rejected` | `False` | `True` | target_url_host_must_be_in_allowed_domains |
| `negative_http_url` | `rejected` | `False` | `True` | target_urls_must_be_https |
| `negative_login_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_login |
| `negative_form_submit_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_form_submit_actions |
| `negative_public_action_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_public_actions |
| `negative_account_action_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_account_actions |
| `negative_wallet_action_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_wallet_actions |
| `negative_payment_action_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_payment_actions |
| `negative_security_testing_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_security_testing_actions |
| `negative_file_upload_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_file_transfer_actions |
| `negative_file_download_allowed` | `rejected` | `False` | `True` | allowed_actions_include_prohibited_file_transfer_actions |
| `negative_missing_capture_log` | `rejected` | `False` | `True` | declared_capture_log_path_missing |
| `negative_missing_output_artifact` | `rejected` | `False` | `True` | evidence_output_artifact_path_missing |
| `negative_teardown_not_required` | `rejected` | `False` | `True` | teardown_required_must_be_true |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_service_request_mutated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_mutated_must_equal_0 |
| `negative_mcp_tool_called` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Passing this validator accepts only a browser research plan shape.
- Passing this validator does not open an in-app browser, Browser Use session, Playwright session, or signed-in browser.
- Passing this validator does not assign or mutate service requests.
- Login, form submit, account, wallet, payment, public, security testing, file transfer, MCP tool, model/API, credential, and external side-effect actions remain blocked.
