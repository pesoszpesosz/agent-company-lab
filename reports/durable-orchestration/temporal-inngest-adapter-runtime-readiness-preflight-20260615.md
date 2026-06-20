# Durable Adapter To Service-Worker Refresh Integration

Generated UTC: 2026-06-15T15:35:49Z
JSON mirror: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-runtime-readiness-preflight-20260615.json`
Validation: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-runtime-readiness-preflight-validation-20260615.json`

## Scope

This report maps the hardened durable reducer dry-run output to existing service-worker packet refresh commands. It is local-only and report-only.

## Current Counts

- Reducer rows: `14`
- Parked rows: `11`
- Terminal completed rows: `1`
- Terminal rejected rows: `2`
- Human decision packets: `11`
- Post-decision refresh plans: `11`
- Decision preflight rows: `11`
- Chain integrity currently passing: `True`

## Mapping

| Reducer State | Rows | Disposition |
| --- | ---: | --- |
| `parked.awaiting_human_review` | `11` | `refresh_local_review_packets_only` |
| `terminal.completed_from_ledger_snapshot` | `1` | `terminal_no_refresh_start_or_replay` |
| `terminal.rejected_from_ledger_snapshot` | `2` | `terminal_rejected_no_revive_or_replay` |

## Boundary

- SQLite `service_requests` remains the authority.
- Reducer output is a deterministic preview.
- `resume_requirements` order is semantic for review packet display.
- Model/API execution remains parked until provider, model, cost, credential route, artifact scope, and worker pool are approved.
- Temporal/Inngest integration remains manifest/report-only until an explicit runtime approval exists.

## Runtime Effects

- Approvals granted: `False`
- Service requests assigned: `0`
- Service requests updated: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Next Action

Add generated durable integration validation to the refreshed chain-integrity report, then use the report-only integration command before any future orchestration adapter work.

