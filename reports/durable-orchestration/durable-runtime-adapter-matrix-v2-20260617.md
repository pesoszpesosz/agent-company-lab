# Durable Runtime Adapter Matrix v2

Generated UTC: 2026-06-20T12:35:28Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\durable-runtime-adapter-matrix-v2-20260617.json`
Schema: `E:\agent-company-lab\architecture\durable-runtime-adapter-matrix-v2.schema.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\durable-runtime-adapter-matrix-v2-validation-20260617.json`

## Summary

- Runtime rows checked: `7`
- Passed: `7`
- Failed: `0`
- Required runtimes present: `true`
- Dependency installs: `false`
- Dependency imports: `false`
- Runtime starts: `0`
- Queue enqueues: `0`
- Service request mutations: `0`
- API calls: `false`
- External side effects: `false`

## Matrix

| Runtime | Category | Safe Now | Score | Decision | Status |
| --- | --- | ---: | ---: | --- | --- |
| `sqlite_control_plane` | `local_control_plane` | `true` | `91` | keep_as_source_of_truth_now | `pass` |
| `temporal_python` | `durable_workflow_engine` | `false` | `83` | hold_for_local_reducer_fixture_then_human_runtime_approval | `pass` |
| `inngest` | `event_driven_durable_functions` | `false` | `78` | candidate_after_local_outbox_event_contract | `pass` |
| `dbos_python` | `database_backed_durable_workflows` | `false` | `76` | candidate_after_sqlite_to_postgres_state_boundary_review | `pass` |
| `pydantic_ai_durable_execution` | `agent_integration_layer` | `false` | `75` | use_as_reference_only_until_model_api_gate_is_approved | `pass` |
| `prefect` | `python_workflow_orchestrator` | `false` | `66` | watchlist_for_source_refresh_and_eval_flows | `pass` |
| `restate` | `durable_agent_runtime` | `false` | `70` | watchlist_after_outbox_and_browser_safety_contracts | `pass` |

## Recommended Next Local Tests

- `durable_runtime_adapter_matrix_v2_to_service_worker_reducer_fixture`
- `temporal_signal_shape_fixture_against_service_worker_request_v1`
- `inngest_event_name_and_flow_control_fixture_against_central_outbox_history_v1`
- `dbos_workflow_step_boundary_fixture_for_service_worker_request_v1`

## Decision

Keep SQLite as the active source of truth. Promote Temporal and Inngest as the next comparison candidates only through local fixtures. Hold DBOS, Prefect, Restate, and Pydantic durable execution integrations until dependency, runtime, model/API, credential, and service-worker approvals exist.

## Boundary

- No dependency install was performed.
- No durable runtime package was imported.
- No runtime was started.
- No queue event was enqueued.
- No service request was mutated.
- No browser session was opened.
- No model/API call was made.
- No external side effect was performed.
