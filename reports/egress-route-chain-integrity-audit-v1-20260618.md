# Egress Route Chain Integrity Audit v1

Generated UTC: 2026-06-21T15:49:37Z
Gateway docket: `E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-20260618.json`
Report JSON: `E:\agent-company-lab\reports\egress-route-chain-integrity-audit-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\egress-route-chain-integrity-audit-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Routes audited: `8`
- Full report-only chains: `8`
- Partial shared chains: `0`
- Recommended next route: ``
- Recommended next layer: ``
- Live egress allowed: `False`
- External side effects: `False`

## Route Coverage

| Route | Egress Type | Status | Present Layers | Missing Layers |
| --- | --- | --- | --- | --- |
| `local_agent_to_agent_report_only` | `agent_to_agent` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract`, `apply_command_guard` | `none` |
| `browser_read_only_gateway` | `browser_read_only` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract` | `none` |
| `mcp_tool_gateway` | `mcp_tool` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_guard` | `none` |
| `model_api_gateway` | `model_api` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract` | `none` |
| `runtime_process_gateway` | `runtime_start` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract` | `none` |
| `public_action_gateway` | `public_submission` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract` | `none` |
| `account_wallet_payment_gateway` | `account_wallet_payment` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract` | `none` |
| `telemetry_export_gateway` | `telemetry_export` | `full_report_only_chain` | `unified_gateway_docket`, `signed_decision_intake_contract`, `signed_decision_guard`, `apply_preflight_blocker`, `apply_command_contract` | `none` |

## Boundary

This audit is report-only. It does not register gateways, start gateways, start workers, open browser sessions, mutate service requests, call MCP/model APIs, or perform live egress.

Next action: All report-only egress route chains have their required non-live guard layers; continue only after a real signed operator decision and route-specific approval evidence exists.
