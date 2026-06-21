# Agent Company Runtime Adoption Docket v1

Generated UTC: 2026-06-21T15:49:31Z
Source radar dataset: `E:\agent-company-lab\data\agent-company-open-source-stack-radar-wave19-20260618.json`
Report JSON: `E:\agent-company-lab\reports\agent-company-runtime-adoption-docket-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\agent-company-runtime-adoption-docket-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Source candidates: `27`
- Docket items: `27`
- Reference only: `11`
- Adapter candidates: `4`
- Future runtime candidates: `3`
- Blocked dependencies: `9`
- Adoption allowed: `False`
- Runtime starts: `0`
- External side effects: `False`

## Top Adapter Candidates

- `browser-use/browser-use`
- `microsoft/playwright`
- `browserbase/stagehand`
- `microsoft/playwright-mcp`

## Future Runtime Candidates

- `temporalio/temporal`
- `restatedev/restate`
- `dbos-inc/dbos-transact-py`

## Docket

| Rank | Repo | Disposition | Worker Class | Risk | Next Gate |
| ---: | --- | --- | --- | --- | --- |
| `1` | `browser-use/browser-use` | `adapter_candidate` | `browser_worker` | `medium` | `browser_worker_adapter_contract_plus_signed_approval_plus_apply_preflight` |
| `2` | `microsoft/playwright` | `adapter_candidate` | `browser_worker` | `medium` | `browser_worker_adapter_contract_plus_signed_approval_plus_apply_preflight` |
| `3` | `langchain-ai/langgraph` | `reference_only` | `agent_framework` | `medium` | `model_api_dependency_install_runtime_start_and_secrets_gates` |
| `4` | `temporalio/temporal` | `future_runtime_candidate` | `durable_runtime` | `medium` | `runtime_start_preflight_signed_decision_and_dependency_install_gate` |
| `5` | `microsoft/agent-framework` | `blocked_dependency` | `model_backed_agent_framework` | `high` | `model_api_provider_cost_dependency_install_runtime_start_and_secrets_gates` |
| `6` | `crewAIInc/crewAI` | `reference_only` | `agent_framework` | `medium` | `model_api_dependency_install_runtime_start_and_secrets_gates` |
| `7` | `IBM/mcp-context-forge` | `reference_only` | `gateway_or_mcp` | `medium` | `mcp_registry_egress_gateway_and_signed_operator_decision` |
| `8` | `agentgateway/agentgateway` | `reference_only` | `gateway_or_mcp` | `medium` | `mcp_registry_egress_gateway_and_signed_operator_decision` |
| `9` | `openai/openai-agents-python` | `blocked_dependency` | `model_backed_agent_framework` | `medium` | `model_api_provider_cost_dependency_install_runtime_start_and_secrets_gates` |
| `10` | `browserbase/stagehand` | `adapter_candidate` | `browser_worker` | `high` | `browser_worker_adapter_contract_plus_signed_approval_plus_apply_preflight` |
| `11` | `pydantic/pydantic-ai` | `reference_only` | `agent_framework` | `medium` | `model_api_dependency_install_runtime_start_and_secrets_gates` |
| `12` | `restatedev/restate` | `future_runtime_candidate` | `durable_runtime` | `high` | `runtime_start_preflight_signed_decision_and_dependency_install_gate` |
| `13` | `microsoft/autogen` | `reference_only` | `agent_framework` | `medium` | `model_api_dependency_install_runtime_start_and_secrets_gates` |
| `14` | `microsoft/playwright-mcp` | `adapter_candidate` | `browser_worker` | `medium` | `browser_worker_adapter_contract_plus_signed_approval_plus_apply_preflight` |
| `15` | `langfuse/langfuse` | `reference_only` | `observability` | `high` | `telemetry_privacy_dependency_install_and_export_gate` |
| `16` | `modelcontextprotocol/python-sdk` | `reference_only` | `gateway_or_mcp` | `medium` | `mcp_registry_egress_gateway_and_signed_operator_decision` |
| `17` | `google/adk-python` | `blocked_dependency` | `model_backed_agent_framework` | `high` | `model_api_provider_cost_dependency_install_runtime_start_and_secrets_gates` |
| `18` | `Arize-ai/phoenix` | `reference_only` | `observability` | `medium` | `telemetry_privacy_dependency_install_and_export_gate` |
| `19` | `hatchet-dev/hatchet` | `blocked_dependency` | `workflow_platform` | `medium` | `runtime_start_preflight_dependency_install_gate_queue_mutation_guard_and_signed_operator_decision` |
| `20` | `inngest/inngest` | `blocked_dependency` | `workflow_platform` | `high` | `runtime_start_preflight_dependency_install_gate_queue_mutation_guard_and_signed_operator_decision` |
| `21` | `dbos-inc/dbos-transact-py` | `future_runtime_candidate` | `durable_workflow` | `medium` | `runtime_start_preflight_dependency_install_gate_and_queue_mutation_guard` |
| `22` | `PrefectHQ/prefect` | `blocked_dependency` | `workflow_platform` | `high` | `runtime_start_preflight_dependency_install_gate_queue_mutation_guard_and_signed_operator_decision` |
| `23` | `n8n-io/n8n` | `blocked_dependency` | `workflow_platform` | `high` | `runtime_start_preflight_dependency_install_gate_queue_mutation_guard_and_signed_operator_decision` |
| `24` | `langgenius/dify` | `blocked_dependency` | `platform_runtime` | `high` | `docker_cloud_account_credentials_plugin_and_public_action_gates` |
| `25` | `humanlayer/humanlayer` | `blocked_dependency` | `unknown_or_mixed` | `medium` | `manual_architecture_review_required` |
| `26` | `VoltAgent/voltagent` | `reference_only` | `observability` | `medium` | `telemetry_privacy_dependency_install_and_export_gate` |
| `27` | `openlit/openlit` | `reference_only` | `observability` | `medium` | `telemetry_privacy_dependency_install_and_export_gate` |

## Boundary

- This docket is report-only.
- No dependency is installed or imported.
- No runtime, worker, browser, MCP server, model/API call, telemetry export, service request assignment, public action, wallet/payment action, or external side effect is allowed.
