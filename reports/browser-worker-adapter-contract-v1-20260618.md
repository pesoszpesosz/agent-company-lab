# Browser Worker Adapter Contract v1 Validation

Generated UTC: 2026-06-20T21:07:30Z
Validation JSON: `E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-validation-20260618.json`
Report JSON: `E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-20260618.json`
Schema: `E:\agent-company-lab\architecture\browser-worker-adapter-contract-v1.schema.json`

## Summary

- All checks passed: `True`
- Contract verdict: `adapter_contract_valid_start_blocked`
- Browser session start allowed: `False`
- Worker start allowed: `False`
- Fixtures: `26`
- Accepted: `1`
- Rejected: `25`
- External side effects: `False`

## Accepted Runtime Shape

The only accepted fixture is a report-only `playwright_deterministic` adapter contract tied to an existing `browser_read_only_session` service request. It allows public HTTPS navigation, visible text reading, accessibility snapshots, screenshots, and local evidence writes, but it still blocks browser and worker starts.

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_playwright_read_only_adapter_start_blocked` | `accepted` | `True` | `True` |  |
| `negative_missing_request` | `rejected` | `False` | `True` | service_request_not_found |
| `negative_wrong_service` | `rejected` | `False` | `True` | service_id_must_be_browser_read_only_session |
| `negative_stagehand_runtime_without_api_gate` | `rejected` | `False` | `True` | only_playwright_deterministic_allowed_for_contract_v1, runtime_candidate_must_be_microsoft_playwright |
| `negative_signed_in_session` | `rejected` | `False` | `True` | session_mode_must_be_public_read_only_no_login |
| `negative_approved_runtime_mode` | `rejected` | `False` | `True` | execution_mode_must_be_report_only_contract |
| `negative_unbounded_navigation` | `rejected` | `False` | `True` | navigation_scope_must_be_explicit_allowlist_only |
| `negative_wildcard_domain` | `rejected` | `False` | `True` | allowed_domains_must_not_use_wildcards, target_url_host_must_be_in_allowed_domains |
| `negative_target_outside_allowlist` | `rejected` | `False` | `True` | target_url_host_must_be_in_allowed_domains |
| `negative_non_https_target` | `rejected` | `False` | `True` | target_urls_must_be_https |
| `negative_missing_screenshot_artifact` | `rejected` | `False` | `True` | required_artifacts_missing_paths |
| `negative_artifact_outside_lab` | `rejected` | `False` | `True` | required_artifacts_capture_log_path_must_stay_inside_lab |
| `negative_missing_kill_switch` | `rejected` | `False` | `True` | lifecycle_kill_switch_required_must_be_true |
| `negative_positive_session_duration` | `rejected` | `False` | `True` | lifecycle_max_session_minutes_must_be_zero_until_approval |
| `negative_browser_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_allowed_login` | `rejected` | `False` | `True` | allowed_action_classes_include_prohibited_login_actions |
| `negative_allowed_form_submit` | `rejected` | `False` | `True` | allowed_action_classes_include_prohibited_form_submit_actions |
| `negative_allowed_public_action` | `rejected` | `False` | `True` | allowed_action_classes_include_prohibited_public_actions |
| `negative_allowed_wallet` | `rejected` | `False` | `True` | allowed_action_classes_include_prohibited_wallet_actions |
| `negative_allowed_browser_code` | `rejected` | `False` | `True` | allowed_action_classes_include_prohibited_mcp_servers_started |
| `negative_missing_denied_class` | `rejected` | `False` | `True` | denied_action_classes_missing_required_denials |
| `negative_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_workers_started_must_equal_0 |
| `negative_mcp_started` | `rejected` | `False` | `True` | runtime_boundary_mcp_servers_started_must_equal_0 |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Passing this contract does not start Playwright, Browser Use, Stagehand, Playwright MCP, agent-browser, cloud browsers, extensions, or browser forks.
- Passing this contract does not approve service requests or assign workers.
- Login, form submit, account, wallet, payment, public, security testing, file transfer, model/API, credential, MCP server, and external side-effect actions remain blocked.
