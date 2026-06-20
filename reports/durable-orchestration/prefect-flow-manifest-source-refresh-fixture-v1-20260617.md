# Prefect Source-Refresh Flow Manifest Fixture v1

Generated UTC: 2026-06-20T12:08:44Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\prefect-flow-manifest-source-refresh-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\prefect-flow-manifest-source-refresh-fixture-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\prefect-flow-manifest-source-refresh-fixture-v1.schema.json`

## Summary

- Cases checked: `6`
- Passed: `6`
- Failed: `0`
- Prefect imports: `0`
- Flow runs: `0`
- Task runs: `0`
- Deployments created: `0`
- Schedules created: `0`
- Workers started: `0`
- Test harness starts: `0`
- API calls: `false`
- External side effects: `false`

## Case Rows

| Case | Source | Mode | Decision | Validation |
| --- | --- | --- | --- | --- |
| `case-valid-profit-edge-local-queue-planning` | `profit_edge_daily_queue_snapshot` | `local_planning_only` | `valid_manifest_only_local_planning` | `pass` |
| `case-valid-prediction-local-file-read` | `prediction_market_data_sources` | `local_file_read` | `valid_manifest_only_local_file_read` | `pass` |
| `case-valid-platform-github-metadata-preview` | `platform_infra_repo_metadata` | `read_only_github_metadata` | `valid_manifest_only_github_metadata_preview` | `pass` |
| `case-invalid-browser-service-request-source` | `digital_marketplace_terms` | `service_request_only` | `reject_service_request_only_browser_refresh` | `pass` |
| `case-invalid-prefect-deployment-and-worker` | `paid_code_readonly_bounty_sources` | `service_request_only` | `reject_prefect_runtime_and_live_source_refresh` | `pass` |
| `case-invalid-test-harness-and-service-mutation` | `security_scope_rules` | `service_request_only` | `reject_test_harness_and_service_mutation` | `pass` |

## Decision

This manifest treats Prefect as a future flow-orchestration adapter for source refreshes, not as an active runtime. It allows only local-file, local-planning, and read-only GitHub metadata preview manifests. Browser, service-request-only, API, public-action, security, wallet, payment, model/API, deployment, schedule, work-pool, worker, server/cloud, and test-harness execution paths are rejected.

## Boundary

- No Prefect package import.
- No `@flow` or `@task` decoration.
- No flow run, task run, deployment, schedule, work pool, worker, test harness, server, cloud, or API call.
- No service-request mutation, browser session, public action, account action, wallet/payment action, security test, model/API call, real-money action, or external side effect.
