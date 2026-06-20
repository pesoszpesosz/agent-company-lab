# Agent Company Trace Events

Generated UTC: 2026-06-15T14:54:07Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
Rows shown: 1

## Boundary

- Trace events are local audit records for agent/company operations.
- A trace event is not approval to perform account, wallet, browser, public, legal/KYC/billing, or real-money actions.

## Counts By Event Type

| Event Type | Count |
| --- | ---: |
| `durable_adapter_cli_dry_run_implementation` | 1 |

## Counts By Lane

| Lane | Count |
| --- | ---: |
| `platform_engineering` | 1 |

## Events

| Time | Type | Trace | Lane | Task | Agent | Event | Source | Artifact | Metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-15T14:53:49Z | durable_adapter_cli_dry_run_implementation | `trace-durable-orchestration-adapter-cli-dry-run-implementation-20260615` | `platform_engineering` | `task-temporal-inngest-adapter-cli-dry-run-implementation-20260615` | recovered-profitable-edge-infra | `trace-event-temporal-inngest-adapter-cli-dry-run-implementation-20260615` - Implemented fixture-only durable service-request reducer dry-run CLI command and verified syntax/help/fixture/result-write tests with zero service-request mutations and no external runtime/API effects. | local_cli_fixture_tests_and_sqlite_snapshot | E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-dry-run-implementation-test-20260615.md | {"all_checks_passed": true, "artifact_hashes_sha256": {"E:\\agent-company-lab\\reports\\durable-orchestration\\temporal-inngest-adapter-cli-dry-run-implementation-test-20260615.json": "D91AC5EC2B61DC3181271FEA694A472C9F5 |
