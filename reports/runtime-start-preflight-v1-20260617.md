# Runtime Start Preflight v1 Validation

Generated UTC: 2026-06-20T21:07:38Z
Worker pool: `service-worker-local-runtime-adapter-pool`
Validation JSON: `E:\agent-company-lab\reports\runtime-start-preflight-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\runtime-start-preflight-v1-20260617.json`

## Summary

- All checks passed: `True`
- Runtime start verdict: `dry_run_preview_valid_start_blocked`
- Runtime start allowed: `False`
- Worker start allowed: `False`
- Runtime processes started: `0`
- Command previews executed: `0`
- External side effects: `False`

## Activation Chain

- Path: `E:\agent-company-lab\reports\worker-activation-preflight-chain-v1-validation-20260617.json`
- All checks passed: `True`
- Chain verdict: `preflight_passed_registration_blocked`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_dry_run_preview_valid_start_blocked` | `accepted` | `True` | `True` |  |
| `negative_missing_activation_chain` | `rejected` | `False` | `True` | activation_chain_validation_path_missing |
| `negative_signed_start_approval_claimed` | `rejected` | `False` | `True` | operator_decision_must_not_claim_signed_start_authority |
| `negative_runtime_start_allowed` | `rejected` | `False` | `True` | runtime_start_verdict_must_block_start, runtime_start_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_command_mode_execute` | `rejected` | `False` | `True` | command_preview_mode_must_be_preview_only |
| `negative_command_execution_allowed` | `rejected` | `False` | `True` | command_execution_allowed_must_be_false |
| `negative_command_preview_executed` | `rejected` | `False` | `True` | runtime_boundary_command_previews_executed_must_equal_0 |
| `negative_runtime_process_started` | `rejected` | `False` | `True` | runtime_boundary_runtime_processes_started_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_mcp_tool_called` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_browser_opened` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_credential_created` | `rejected` | `False` | `True` | runtime_boundary_credentials_created_must_equal_False |
| `negative_missing_trace_id` | `rejected` | `False` | `True` | trace_id_missing |
| `negative_missing_output_artifact` | `rejected` | `False` | `True` | output_artifact_path_missing |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Passing this validator does not execute a command preview.
- Passing this validator does not start any local runtime process.
- Passing this validator does not assign service requests, start workers, enable MCP tools, open browsers, or use credentials.
