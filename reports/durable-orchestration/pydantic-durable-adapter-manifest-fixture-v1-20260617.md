# Pydantic Durable Adapter Manifest Fixture v1

Generated UTC: 2026-06-20T12:38:01Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\pydantic-durable-adapter-manifest-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\pydantic-durable-adapter-manifest-fixture-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\pydantic-durable-adapter-manifest-fixture-v1.schema.json`

## Summary

- Cases checked: `7`
- Passed: `7`
- Failed: `0`
- Pydantic AI imports: `0`
- Durable backend imports: `0`
- Agent runs: `0`
- Model API calls: `false`
- Model requests allowed: `false`
- MCP servers started: `0`
- Runtime starts: `0`
- External side effects: `false`

## Case Rows

| Case | Backend | Model Mode | Decision | Validation |
| --- | --- | --- | --- | --- |
| `case-valid-temporal-testmodel-static-tools` | `temporal` | `TestModel` | `valid_manifest_only_reference` | `pass` |
| `case-valid-dbos-functionmodel-static-tools` | `dbos` | `FunctionModel` | `valid_manifest_only_reference` | `pass` |
| `case-valid-prefect-testmodel-no-runtime` | `prefect` | `TestModel` | `valid_manifest_only_reference` | `pass` |
| `case-valid-restate-functionmodel-no-server` | `restate` | `FunctionModel` | `valid_manifest_only_reference` | `pass` |
| `case-invalid-real-provider-openai` | `dbos` | `openai:gpt-5.2` | `reject_real_model_without_service_request` | `pass` |
| `case-invalid-dynamic-toolset-no-id` | `temporal` | `TestModel` | `reject_durable_toolset_without_static_id` | `pass` |
| `case-invalid-runtime-and-mcp-start` | `restate` | `FunctionModel` | `reject_runtime_or_mcp_start` | `pass` |

## Decision

This manifest keeps Pydantic AI durable execution as a reference layer only. It permits TestModel and FunctionModel-shaped manifests for Temporal, DBOS, Prefect, and Restate, but blocks real providers, model requests, backend imports, runtime starts, MCP server starts, and dynamic durable toolsets without stable IDs.

## Boundary

- No Pydantic AI import.
- No durable backend import.
- No agent run, TestModel run, FunctionModel run, or model/API call.
- No MCP server, runtime, browser, worker, account, wallet, payment, public, security, or real-money action.
