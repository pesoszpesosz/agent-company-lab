# Durable Adapter To Service-Worker Refresh Integration

Generated: 2026-06-15T15:21:46Z

## Scope

This report maps the hardened durable reducer dry-run output to existing service-worker packet refresh commands. It is local-only and report-only. It does not approve, reject, assign, start, complete, emit, schedule, call APIs, or start Temporal/Inngest.

## Current Counts

- Reducer rows: 14.
- Parked rows: 11.
- Terminal completed rows: 1.
- Terminal rejected rows: 2.
- Human decision packets: 11.
- Post-decision refresh plans: 11.
- Decision preflight rows: 11.
- Chain integrity: 17 checked, 0 failures.

## Mapping

Rows with `parked.awaiting_human_review` may refresh local review artifacts only:

- `write-service-worker-gate-map`
- `write-service-worker-human-decision-packets`
- `write-service-worker-post-decision-simulation`
- `write-service-worker-post-decision-refresh-plan`
- `write-service-worker-decision-preflight`
- `write-service-worker-chain-integrity`

Rows with `terminal.completed_from_ledger_snapshot` or `terminal.rejected_from_ledger_snapshot` stay terminal. They may be included in integrity evidence but must not be replay-started, revived, assigned, or converted back into active review work.

## Boundary

- SQLite `service_requests` remains the authority.
- Reducer output is a deterministic preview.
- `resume_requirements` order is semantic for review packet display.
- Model/API execution remains parked until provider, model, cost, credential route, artifact scope, and worker pool are approved.
- Temporal/Inngest integration remains manifest/report-only until an explicit runtime approval exists.

## Next Action

Implement a report-only CLI command that materializes this integration map from current reducer and service-worker artifacts, then add it to chain-integrity validation.
