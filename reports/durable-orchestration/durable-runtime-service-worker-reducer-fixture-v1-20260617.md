# Durable Runtime Service-Worker Reducer Fixture v1

Generated UTC: 2026-06-20T12:16:56Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\durable-runtime-service-worker-reducer-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\durable-runtime-service-worker-reducer-fixture-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\durable-runtime-service-worker-reducer-fixture-v1.schema.json`

## Summary

- Runtime profiles: `7`
- Service status cases: `3`
- Expanded reducer checks: `21`
- Failed: `0`
- Required runtimes present: `true`
- Required statuses present: `true`
- Dependency installs: `0`
- Dependency imports: `0`
- Runtime starts: `0`
- Queue enqueues: `0`
- Service request mutations: `0`
- API calls: `false`
- External side effects: `false`

## Expanded Reducer Checks

| Runtime | Status | Output State | Mode | Status |
| --- | --- | --- | --- | --- |
| `sqlite_control_plane` | `needs_review` | `parked.awaiting_human_review` | `local_sqlite_dry_run_only` | `pass` |
| `sqlite_control_plane` | `complete` | `terminal.completed_from_ledger_snapshot` | `local_sqlite_dry_run_only` | `pass` |
| `sqlite_control_plane` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `local_sqlite_dry_run_only` | `pass` |
| `temporal_python` | `needs_review` | `parked.awaiting_human_review` | `runtime_contract_preview_only` | `pass` |
| `temporal_python` | `complete` | `terminal.completed_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `temporal_python` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `inngest` | `needs_review` | `parked.awaiting_human_review` | `runtime_contract_preview_only` | `pass` |
| `inngest` | `complete` | `terminal.completed_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `inngest` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `dbos_python` | `needs_review` | `parked.awaiting_human_review` | `runtime_contract_preview_only` | `pass` |
| `dbos_python` | `complete` | `terminal.completed_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `dbos_python` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `pydantic_ai_durable_execution` | `needs_review` | `parked.awaiting_human_review` | `runtime_contract_preview_only` | `pass` |
| `pydantic_ai_durable_execution` | `complete` | `terminal.completed_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `pydantic_ai_durable_execution` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `prefect` | `needs_review` | `parked.awaiting_human_review` | `runtime_contract_preview_only` | `pass` |
| `prefect` | `complete` | `terminal.completed_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `prefect` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `restate` | `needs_review` | `parked.awaiting_human_review` | `runtime_contract_preview_only` | `pass` |
| `restate` | `complete` | `terminal.completed_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |
| `restate` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `runtime_contract_preview_only` | `pass` |

## Decision

The reducer contract permits local previews only. SQLite remains the active source of truth; external durable runtimes may consume this fixture as a contract reference only after their own dependency, runtime, service-worker, credential, and approval gates are cleared.

## Boundary

- No dependency install was performed.
- No durable runtime package was imported.
- No runtime was started.
- No queue event was enqueued.
- No service request was mutated.
- No browser session was opened.
- No model/API call was made.
- No external side effect was performed.
