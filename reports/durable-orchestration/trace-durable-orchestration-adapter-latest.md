# Agent Company Trace Events

Generated UTC: 2026-06-15T15:38:17Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
Rows shown: 1

## Boundary

- Trace events are local audit records for agent/company operations.
- A trace event is not approval to perform account, wallet, browser, public, legal/KYC/billing, or real-money actions.

## Counts By Event Type

| Event Type | Count |
| --- | ---: |
| `durable_adapter_runtime_readiness` | 1 |

## Counts By Lane

| Lane | Count |
| --- | ---: |
| `platform_engineering` | 1 |

## Events

| Time | Type | Trace | Lane | Task | Agent | Event | Source | Artifact | Metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-15T15:38:03Z | durable_adapter_runtime_readiness | `trace-durable-orchestration-adapter-runtime-readiness-20260615` | `platform_engineering` | `task-temporal-inngest-adapter-runtime-readiness-20260615` | recovered-profitable-edge-infra | `trace-event-temporal-inngest-adapter-runtime-readiness-20260615` - Used report-only durable integration preflight to decide runtime readiness: external Temporal/Inngest runtime work remains blocked, local report-only contract work is allowed, with zero service-request mutations, approva | local_report_only | E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-runtime-readiness-20260615.md | {} |
