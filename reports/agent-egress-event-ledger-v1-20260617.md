# Agent Egress Event Ledger v1 Validation

Generated UTC: 2026-06-20T21:07:28Z
Source packet: `E:\agent-company-lab\reports\agent-egress-event-ledger-packet-v1-20260617.json`
Schema: `E:\agent-company-lab\architecture\agent-egress-event-ledger-v1.schema.json`
Validation JSON: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-20260617.json`
Fixture directory: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-fixtures`

## Summary

- All checks passed: `True`
- Fixture count: `24`
- Accepted fixtures: `1`
- Rejected fixtures: `23`
- Live egress allowed: `False`
- Gateway started: `False`
- Model API calls: `False`
- MCP tool calls: `False`
- Browser sessions started: `0`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_report_only_preflight_event` | `accepted` | `True` | `True` |  |
| `negative_missing_identity_envelope` | `rejected` | `False` | `True` | identity_envelope_artifact_path_missing |
| `negative_missing_operator_decision` | `rejected` | `False` | `True` | operator_decision_artifact_path_missing |
| `negative_expired_egress_event` | `rejected` | `False` | `True` | expires_not_after_created, egress_event_expired |
| `negative_unknown_egress_type` | `rejected` | `False` | `True` | unknown_egress_type, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_implicit_credentials` | `rejected` | `False` | `True` | credential_scope_must_be_none |
| `negative_implicit_budget` | `rejected` | `False` | `True` | budget_scope_must_be_zero_or_not_applicable |
| `negative_missing_output_artifact` | `rejected` | `False` | `True` | output_artifact_path_missing |
| `negative_scope_broadened_from_identity` | `rejected` | `False` | `True` | egress_type_requires_future_gate:direct_api, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_scope_broadened_from_decision` | `rejected` | `False` | `True` | policy_verdict_not_allowed_in_local_validator:allow_after_operator_approval |
| `negative_signed_in_browser_as_read_only` | `rejected` | `False` | `True` | egress_type_requires_future_gate:browser_signed_in, browser_scope_must_be_none, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_public_action_allowed_without_cro` | `rejected` | `False` | `True` | egress_type_requires_future_gate:public_submission, public_action_scope_must_be_none, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_wallet_payment_non_deny` | `rejected` | `False` | `True` | egress_type_requires_future_gate:wallet_payment, wallet_scope_must_be_none, payment_scope_must_be_none, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_model_api_no_provider_cost` | `rejected` | `False` | `True` | egress_type_requires_future_gate:model_api, model_api_scope_must_be_none, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_mcp_server_not_registered` | `rejected` | `False` | `True` | egress_type_requires_future_gate:mcp_tool, mcp_scope_must_be_none, allow_report_only_preflight_requires_report_only_egress_type |
| `negative_external_side_effects_report_only` | `rejected` | `False` | `True` | external_side_effects_expected_must_be_false |
| `negative_gateway_started` | `rejected` | `False` | `True` | runtime_boundary_gateway_started_must_equal_False |
| `negative_api_key_created` | `rejected` | `False` | `True` | runtime_boundary_api_keys_created_must_equal_False |
| `negative_model_call_recorded` | `rejected` | `False` | `True` | runtime_boundary_model_api_calls_must_equal_False |
| `negative_mcp_call_recorded` | `rejected` | `False` | `True` | runtime_boundary_mcp_tool_calls_must_equal_False |
| `negative_browser_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_worker_started` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_service_request_assigned` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_revoked_event` | `rejected` | `False` | `True` | egress_event_not_active |

## Boundary

- This validator creates local fixture/report files only.
- It does not start a gateway, install a gateway, create API keys, record live egress, call model APIs, call MCP tools, open a browser, register pools, assign service requests, start workers, or perform credential/wallet/payment/public actions.
- A passing event is only acceptable as local report-only preflight evidence.
