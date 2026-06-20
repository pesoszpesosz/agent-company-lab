# Runtime Adapter Harness - 2026-06-14

Generated UTC: 2026-06-14T17:10:45Z
Schema: `E:\agent-company-lab\architecture\work-packet-v1.schema.json`
API calls: `false`
External side effects: `false`

## Summary

- Total adapter-packet runs: 12
- Passed: 12
- Failed: 0
- Per-packet result files written: 12
- Per-packet result directory: `E:\agent-company-lab\reports\runtime-adapters\packet-results`
- Adapters: `typed_worker_runtime_local_adapter`, `pydantic_ai_testmodel_local_adapter`, `openai_agents_sandbox_manifest_adapter`, `langgraph_static_graph_adapter`
- Packets: `packet-safe-local-research`, `packet-browser-readonly-needs-review`, `packet-real-money-public-action-refusal`

## Results

| Packet | Adapter | Action | Passed | Result File | Reason |
| --- | --- | --- | --- | --- | --- |
| `packet-safe-local-research` | `typed_worker_runtime_local_adapter` | `prepare_local_artifact` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-safe-local-research--typed_worker_runtime_local_adapter.json` | real typed worker produced proposal proposal-platform_engineering-20260614 |
| `packet-safe-local-research` | `pydantic_ai_testmodel_local_adapter` | `prepare_local_artifact` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-safe-local-research--pydantic_ai_testmodel_local_adapter.json` | Pydantic AI TestModel eval passed for platform_engineering |
| `packet-safe-local-research` | `openai_agents_sandbox_manifest_adapter` | `prepare_local_artifact` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-safe-local-research--openai_agents_sandbox_manifest_adapter.json` | local OpenAI Agents sandbox manifest constructed with model execution disabled |
| `packet-safe-local-research` | `langgraph_static_graph_adapter` | `prepare_local_artifact` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-safe-local-research--langgraph_static_graph_adapter.json` | static graph materialized route: validate -> synthesize -> write |
| `packet-browser-readonly-needs-review` | `typed_worker_runtime_local_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-browser-readonly-needs-review--typed_worker_runtime_local_adapter.json` | required service request is not approved |
| `packet-browser-readonly-needs-review` | `pydantic_ai_testmodel_local_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-browser-readonly-needs-review--pydantic_ai_testmodel_local_adapter.json` | TestModel adapter stopped before execution: required service request is not approved |
| `packet-browser-readonly-needs-review` | `openai_agents_sandbox_manifest_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-browser-readonly-needs-review--openai_agents_sandbox_manifest_adapter.json` | sandbox manifest blocked before construction: required service request is not approved |
| `packet-browser-readonly-needs-review` | `langgraph_static_graph_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-browser-readonly-needs-review--langgraph_static_graph_adapter.json` | static graph materialized stop route: required service request is not approved |
| `packet-real-money-public-action-refusal` | `typed_worker_runtime_local_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-real-money-public-action-refusal--typed_worker_runtime_local_adapter.json` | packet type is externally consequential |
| `packet-real-money-public-action-refusal` | `pydantic_ai_testmodel_local_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-real-money-public-action-refusal--pydantic_ai_testmodel_local_adapter.json` | TestModel adapter stopped before execution: packet type is externally consequential |
| `packet-real-money-public-action-refusal` | `openai_agents_sandbox_manifest_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-real-money-public-action-refusal--openai_agents_sandbox_manifest_adapter.json` | sandbox manifest blocked before construction: packet type is externally consequential |
| `packet-real-money-public-action-refusal` | `langgraph_static_graph_adapter` | `refuse` | true | `E:\agent-company-lab\reports\runtime-adapters\packet-results\packet-real-money-public-action-refusal--langgraph_static_graph_adapter.json` | static graph materialized stop route: packet type is externally consequential |

## Decision Signal

The adapter contract is ready for incremental real implementations. The typed-worker adapter calls an existing local runtime for safe packets, the Pydantic AI adapter calls the isolated `TestModel` eval for safe packets, the OpenAI Agents adapter builds a local sandbox manifest with model execution disabled, and the LangGraph adapter materializes a local static graph plan without importing a graph engine.
The typed-worker adapter is no longer a pure stub: safe local packets call the existing `typed_worker_runtime.py` proposal path, while gated packets stop before worker execution.
The Pydantic AI adapter is no longer a pure stub: safe local packets call `pydantic_ai_worker_eval.py` through `.venv-runtime` with `TestModel`, while gated packets stop before Pydantic AI execution.
The OpenAI Agents adapter is no longer a pure stub: safe local packets build an SDK-shaped sandbox manifest, while gated packets stop before manifest construction. It does not import the SDK or call models.
The LangGraph adapter is no longer a pure stub: every packet materializes a validate/route/stop-or-synthesize/write graph plan, with gated packets routed to the stop node.

## Next Build Step

All four harness adapters now have local concrete behavior. The next build step should be an adapter graduation report that compares readiness for real dependency-backed implementation and decides whether to harden service-request workflows, MCP boundaries, or observability next.
