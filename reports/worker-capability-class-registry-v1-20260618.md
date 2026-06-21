# Worker Capability Class Registry v1

Generated UTC: 2026-06-21T15:49:47Z
Source docket: `E:\agent-company-lab\reports\agent-company-runtime-adoption-docket-v1-20260618.json`
Report JSON: `E:\agent-company-lab\reports\worker-capability-class-registry-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\worker-capability-class-registry-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Source docket items: `27`
- Capability classes: `10`
- Unmapped docket items: `0`
- Worker registration allowed: `False`
- Worker start allowed: `False`
- Runtime start allowed: `False`
- External side effects: `False`

## Capability Classes

| Class | Repos | Required Gates |
| --- | ---: | --- |
| `agent_framework` | `4` | `runtime_dependency_install_preflight_v1`; `model_api_execution_gate`; `runtime_start_preflight_v1` |
| `browser_worker` | `4` | `browser_read_only_worker_policy_v1`; `browser_worker_adapter_contract_v1`; `browser_read_only_signed_approval_guard_v1`; `browser_read_only_apply_preflight_blocker_v1`; `browser_read_only_apply_command_contract_v1` |
| `durable_runtime` | `2` | `runtime_start_preflight_v1`; `runtime_start_signed_decision_guard_v1`; `runtime_start_apply_preflight_blocker_v1`; `runtime_dependency_install_preflight_v1` |
| `durable_workflow` | `1` | `runtime_start_preflight_v1`; `runtime_dependency_install_preflight_v1`; `queue_mutation_guard_v1` |
| `gateway_or_mcp` | `3` | `mcp_tool_registry_gate_v1`; `agent_egress_event_ledger_v1`; `unified_agent_egress_gateway_docket_v1` |
| `model_backed_agent_framework` | `3` | `model_api_execution_gate`; `secrets_credentials_handling_gate`; `runtime_dependency_install_preflight_v1`; `runtime_start_preflight_v1` |
| `observability` | `4` | `telemetry_privacy_export_gate_v1`; `runtime_dependency_install_preflight_v1`; `agent_egress_event_ledger_v1` |
| `platform_runtime` | `1` | `runtime_start_preflight_v1`; `legal_kyc_tax_payment_gate`; `secrets_credentials_handling_gate`; `public_action_execution_gate` |
| `unknown_or_mixed` | `1` | `manual_architecture_review_required`; `chief_risk_officer_review` |
| `workflow_platform` | `4` | `runtime_start_preflight_v1`; `runtime_dependency_install_preflight_v1`; `service_request_queue_mutation_guard_v1`; `secrets_credentials_handling_gate` |

## Boundary

- This registry is report-only.
- It registers no worker pool and starts no worker.
- It starts no runtime, browser session, MCP server, model/API call, telemetry export, public action, wallet/payment action, or service-request assignment.
