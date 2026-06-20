# Agent Company Trace Events

Generated UTC: 2026-06-15T14:23:04Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
Rows shown: 1

## Boundary

- Trace events are local audit records for agent/company operations.
- A trace event is not approval to perform account, wallet, browser, public, legal/KYC/billing, or real-money actions.

## Counts By Event Type

| Event Type | Count |
| --- | ---: |
| `platform_research` | 1 |

## Counts By Lane

| Lane | Count |
| --- | ---: |
| `platform_engineering` | 1 |

## Events

| Time | Type | Trace | Lane | Task | Agent | Event | Source | Artifact | Metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-15T14:22:43Z | platform_research | `trace-agent-company-deep-research-wave9-20260615` | `platform_engineering` | `task-agent-company-deep-research-wave9-20260615` | recovered-profitable-edge-infra | `trace-event-agent-company-deep-research-wave9-20260615` - Completed Wave 9 durable orchestration/HITL research; recommends SQLite authority plus Temporal/Inngest adapter manifests, OpenAI Agents behind model/API gate, Prefect/Dagster operational references, and 12-factor agent | codex-web-primary-sources | E:\agent-company-lab\reports\agent-company-deep-research-wave9-20260615.json | {"api_calls": false, "approvals_granted": 0, "authoritative_ledger": "current_sqlite_control_plane", "dependency_imports": 0, "dependency_installs": 0, "external_side_effects": false, "first_durable_candidates": ["tempor |
