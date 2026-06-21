# Egress Route Signed Decision Intake Contract v1

Generated UTC: 2026-06-21T15:44:10Z
Source gateway docket: `E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-20260618.json`
Report JSON: `E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Contract status: `report_only_intake_contract_ready`
- Route templates: `8` / `8`
- Fixture results: `3` accepted, `27` rejected
- Gateway registration allowed: `0`
- Gateway starts: `0`
- Live egress events: `0`
- Worker starts: `0`
- Runtime starts: `0`
- Browser sessions started: `0`
- Model/API calls: `False`
- MCP tool calls: `False`
- External side effects: `False`

## Templates

| Route | Egress Type | Allowed Decisions | Required Gates |
| --- | --- | --- | --- |
| `local_agent_to_agent_report_only` | `agent_to_agent` | `deny`, `approve_route_preflight_only` | `agent_egress_event_ledger_v1`, `local_runtime_adapter_pool_identity_envelope_v1` |
| `browser_read_only_gateway` | `browser_read_only` | `deny`, `approve_route_preflight_only` | `browser_read_only_worker_policy_v1`, `browser_worker_adapter_contract_v1`, `browser_read_only_signed_approval_guard_v1`, `browser_read_only_apply_preflight_blocker_v1`, `browser_read_only_apply_command_contract_v1`, `agent_egress_event_ledger_v1` |
| `mcp_tool_gateway` | `mcp_tool` | `deny`, `approve_route_preflight_only` | `mcp_tool_registry_gate_v1`, `agent_egress_event_ledger_v1`, `local_runtime_adapter_pool_identity_envelope_v1`, `signed_operator_decision_required` |
| `model_api_gateway` | `model_api` | `deny`, `approve_route_preflight_only` | `model_api_execution_gate`, `secrets_credentials_handling_gate`, `agent_egress_event_ledger_v1`, `cost_budget_signed_decision` |
| `runtime_process_gateway` | `runtime_start` | `deny`, `approve_route_preflight_only` | `runtime_start_preflight_v1`, `runtime_start_signed_decision_guard_v1`, `runtime_start_apply_preflight_blocker_v1`, `runtime_dependency_install_preflight_v1`, `agent_egress_event_ledger_v1` |
| `public_action_gateway` | `public_submission` | `deny`, `approve_route_preflight_only` | `public_action_execution_gate`, `reputation_review_worker`, `agent_egress_event_ledger_v1`, `exact_action_body_approval` |
| `account_wallet_payment_gateway` | `account_wallet_payment` | `deny`, `approve_route_preflight_only` | `account_registration_intake`, `wallet_setup_packet`, `wallet_public_address_response`, `legal_kyc_tax_payment_gate`, `agent_egress_event_ledger_v1` |
| `telemetry_export_gateway` | `telemetry_export` | `deny`, `approve_route_preflight_only` | `telemetry_privacy_export_gate_v1`, `agent_egress_event_ledger_v1`, `secrets_credentials_handling_gate` |

## Fixture Validation

| Fixture | Expected | Accepted | Errors |
| --- | --- | --- | ---: |
| `positive_deny_browser_route` | `accepted` | `True` | `0` |
| `positive_browser_route_preflight_only` | `accepted` | `True` | `0` |
| `positive_mcp_route_preflight_only` | `accepted` | `True` | `0` |
| `negative_missing_operator` | `rejected` | `False` | `1` |
| `negative_missing_attestation` | `rejected` | `False` | `2` |
| `negative_wrong_attestation` | `rejected` | `False` | `1` |
| `negative_expired_decision` | `rejected` | `False` | `2` |
| `negative_unknown_route` | `rejected` | `False` | `9` |
| `negative_egress_type_mismatch` | `rejected` | `False` | `1` |
| `negative_missing_docket` | `rejected` | `False` | `1` |
| `negative_outside_docket` | `rejected` | `False` | `1` |
| `negative_docket_hash_mismatch` | `rejected` | `False` | `1` |
| `negative_execute_scope` | `rejected` | `False` | `1` |
| `negative_missing_required_gate` | `rejected` | `False` | `1` |
| `negative_extra_unknown_gate` | `rejected` | `False` | `2` |
| `negative_approval_is_apply` | `rejected` | `False` | `1` |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `1` |
| `negative_gateway_start_allowed` | `rejected` | `False` | `1` |
| `negative_live_egress_allowed` | `rejected` | `False` | `1` |
| `negative_worker_start_allowed` | `rejected` | `False` | `1` |
| `negative_runtime_start_allowed` | `rejected` | `False` | `1` |
| `negative_browser_session_start_allowed` | `rejected` | `False` | `1` |
| `negative_service_request_assigned` | `rejected` | `False` | `1` |
| `negative_boundary_decision_applied` | `rejected` | `False` | `1` |
| `negative_boundary_gateway_started` | `rejected` | `False` | `1` |
| `negative_boundary_live_egress` | `rejected` | `False` | `1` |
| `negative_boundary_model_api` | `rejected` | `False` | `1` |
| `negative_boundary_mcp` | `rejected` | `False` | `1` |
| `negative_boundary_public_action` | `rejected` | `False` | `1` |
| `negative_boundary_external_side_effect` | `rejected` | `False` | `1` |

## Boundary

This contract only defines and validates signed-decision intake records. It does not apply decisions, write approvals, register gateways, start gateways, start workers, mutate service requests, or perform live egress.

Next action: Build egress route signed-decision guard for one exact route decision before any apply preflight, gateway registration, gateway start, or live egress.
