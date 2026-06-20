# Temporal/Inngest Runtime Interface Contract

Generated UTC: 2026-06-15T15:42:52Z
JSON mirror: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-runtime-interface-contract-latest.json`
Validation: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-runtime-interface-contract-validation-latest.json`

## Decision

This is a local-only interface contract. It defines identifiers and mappings for future adapter work, but it does not import Temporal/Inngest, start runtimes, emit events, schedule activities, or mutate service requests.

## Contract Summary

- Interface contracts: `4`
- Reducer rows: `14`
- Parked rows: `11`
- Terminal rows: `3`
- Forbidden runtime imports detected: `0`
- Model/API gate remains parked: `True`

## Contracts

| Contract | Runtime | Executed? |
| --- | --- | --- |
| `temporal_workflow_identity_preview` | `temporal` | `False` |
| `inngest_event_identity_preview` | `inngest` | `False` |
| `reducer_to_service_worker_refresh_disposition` | `local_report_only` | `False` |
| `runtime_gate_enforcement` | `local_report_only` | `False` |

## Boundary

- Dependency installs: `0`
- Runtime imports: `0`
- Temporal workflows started: `0`
- Temporal activities scheduled: `0`
- Inngest events emitted: `0`
- Service requests updated: `0`
- Service requests assigned: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Next Action

Implement static interface-contract negative fixtures and add this generated contract validation to the orchestration readiness chain before any runtime adapter code.

