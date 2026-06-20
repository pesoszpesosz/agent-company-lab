# Temporal/Inngest Adapter Runtime Readiness

Generated: 2026-06-15T15:35:56Z

## Decision

External runtime implementation is not ready to start. Local report-only contract work is ready.

The preflight command `write-durable-adapter-service-worker-integration` passed with 14 reducer rows and 0 failures. Chain integrity is currently 18 layers checked with 0 failures. That proves the local reducer and service-worker refresh boundary is coherent, but it does not approve Temporal/Inngest dependency installs, runtime starts, event emissions, workflow starts, worker assignments, model API calls, or external actions.

## Allowed Next Slice

Write a local-only durable adapter runtime interface contract:

- workflow ID and event-name mapping
- idempotency-key contract
- reducer-state to service-worker refresh disposition mapping
- negative validation checks for imports, starts, emissions, activities, and service-request mutations

## Still Blocked

- Installing Temporal or Inngest packages.
- Importing runtime clients in production path.
- Starting servers, workers, workflows, activities, events, or functions.
- Assigning or starting service workers.
- Processing the parked model/API request.

## Boundary

No dependency installs, imports, approvals, assignments, worker starts, API calls, service-request updates, Temporal/Inngest starts, events, activities, or external effects occurred.
