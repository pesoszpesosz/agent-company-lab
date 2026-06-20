# Unified Agent Egress Gateway Docket v1

Generated UTC: 2026-06-20T21:07:40Z
Source capability registry: `E:\agent-company-lab\reports\worker-capability-class-registry-v1-20260618.json`
Report JSON: `E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Capability classes: `10`
- Gateway routes: `8`
- Required gates indexed: `24`
- Gateway registration allowed: `False`
- Gateway start allowed: `False`
- Live egress allowed: `False`
- Worker starts: `False`
- Runtime starts: `False`
- Browser session starts: `False`
- Model/API calls: `False`
- MCP tool calls: `False`
- External side effects: `False`

## Route Table

| Route | Egress Type | Capability Classes | Required Gates | Blocked Actions |
| --- | --- | --- | --- | --- |
| `local_agent_to_agent_report_only` | `agent_to_agent` | `agent_framework`, `browser_worker`, `durable_runtime`, `durable_workflow`, `gateway_or_mcp`, `model_backed_agent_framework`, `observability`, `platform_runtime`, `unknown_or_mixed`, `workflow_platform` | `agent_egress_event_ledger_v1`, `local_runtime_adapter_pool_identity_envelope_v1` | `live_gateway_start`, `external_api_call`, `service_request_mutation` |
| `browser_read_only_gateway` | `browser_read_only` | `browser_worker` | `browser_read_only_worker_policy_v1`, `browser_worker_adapter_contract_v1`, `browser_read_only_signed_approval_guard_v1`, `browser_read_only_apply_preflight_blocker_v1`, `browser_read_only_apply_command_contract_v1`, `agent_egress_event_ledger_v1` | `browser_session_start`, `signed_in_state_change`, `form_submit`, `download_private_file` |
| `mcp_tool_gateway` | `mcp_tool` | `gateway_or_mcp` | `mcp_tool_registry_gate_v1`, `agent_egress_event_ledger_v1`, `local_runtime_adapter_pool_identity_envelope_v1`, `signed_operator_decision_required` | `mcp_server_start`, `mcp_tool_call`, `credential_read`, `network_write` |
| `model_api_gateway` | `model_api` | `agent_framework`, `model_backed_agent_framework` | `model_api_execution_gate`, `secrets_credentials_handling_gate`, `agent_egress_event_ledger_v1`, `cost_budget_signed_decision` | `model_api_call`, `provider_key_use`, `training_data_upload`, `unbounded_cost` |
| `runtime_process_gateway` | `runtime_start` | `durable_runtime`, `durable_workflow`, `workflow_platform`, `platform_runtime` | `runtime_start_preflight_v1`, `runtime_start_signed_decision_guard_v1`, `runtime_start_apply_preflight_blocker_v1`, `runtime_dependency_install_preflight_v1`, `agent_egress_event_ledger_v1` | `dependency_install`, `runtime_process_start`, `queue_mutation`, `worker_start` |
| `public_action_gateway` | `public_submission` | `browser_worker`, `gateway_or_mcp`, `platform_runtime` | `public_action_execution_gate`, `reputation_review_worker`, `agent_egress_event_ledger_v1`, `exact_action_body_approval` | `post_comment`, `submit_form`, `open_pr`, `claim_bounty`, `send_message` |
| `account_wallet_payment_gateway` | `account_wallet_payment` | `platform_runtime`, `browser_worker` | `account_registration_intake`, `wallet_setup_packet`, `wallet_public_address_response`, `legal_kyc_tax_payment_gate`, `agent_egress_event_ledger_v1` | `accept_terms`, `create_account`, `control_private_key`, `send_funds`, `publish_payment_address` |
| `telemetry_export_gateway` | `telemetry_export` | `observability`, `gateway_or_mcp` | `telemetry_privacy_export_gate_v1`, `agent_egress_event_ledger_v1`, `secrets_credentials_handling_gate` | `external_trace_export`, `private_prompt_upload`, `credential_export`, `unredacted_log_sync` |

## Gateway Decisions

- `all_live_egress_routes_remain_report_only`
- `agent_egress_event_ledger_is_required_for_every_route`
- `route_specific_gates_must_pass_before_signed_operator_decision_intake`
- `gateway_start_is_not_registration_and_neither_is_allowed_here`
- `public_account_wallet_payment_model_mcp_browser_and_runtime_paths_are_separate_routes`

## Boundary

This docket does not register, start, or configure an egress gateway. It is a route map and gate index for future signed operator decisions.

Next action: Build signed operator decision intake for one exact egress route before any gateway registration, gateway start, or live egress.
