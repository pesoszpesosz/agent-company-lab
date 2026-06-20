# Worker Activation Preflight Chain v1 Validation

Generated UTC: 2026-06-20T21:07:40Z
Worker pool: `service-worker-local-runtime-adapter-pool`
Validation JSON: `E:\agent-company-lab\reports\worker-activation-preflight-chain-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\worker-activation-preflight-chain-v1-20260617.json`

## Summary

- All checks passed: `True`
- Chain verdict: `preflight_passed_registration_blocked`
- Registration allowed: `False`
- Worker start allowed: `False`
- MCP tool call allowed: `False`
- External side effects: `False`

## Composed Validators

| Validator | All Checks Passed | Accepted | Rejected |
| --- | --- | ---: | ---: |
| `identity` | `True` | `1` | `25` |
| `egress` | `True` | `1` | `23` |
| `mcp_registry` | `True` | `1` | `21` |

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_preflight_passed_registration_blocked` | `accepted` | `True` | `True` |  |
| `negative_missing_identity_validator` | `rejected` | `False` | `True` | identity_validation_path_missing |
| `negative_missing_egress_validator` | `rejected` | `False` | `True` | egress_validation_path_missing |
| `negative_missing_mcp_registry_validator` | `rejected` | `False` | `True` | mcp_registry_validation_path_missing |
| `negative_signed_approval_claimed` | `rejected` | `False` | `True` | operator_decision_must_remain_report_only |
| `negative_registration_allowed` | `rejected` | `False` | `True` | chain_verdict_must_block_registration, registration_allowed_must_be_false |
| `negative_worker_start_allowed` | `rejected` | `False` | `True` | worker_start_allowed_must_be_false |
| `negative_mcp_tool_call_allowed` | `rejected` | `False` | `True` | mcp_tool_call_allowed_must_be_false |
| `negative_worker_registered_side_effect` | `rejected` | `False` | `True` | runtime_boundary_worker_pools_registered_must_equal_0 |
| `negative_service_request_assigned_side_effect` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_external_side_effect` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- Passing this chain does not register a worker pool.
- Passing this chain does not assign service requests.
- Passing this chain does not start workers or enable MCP tool calls.
