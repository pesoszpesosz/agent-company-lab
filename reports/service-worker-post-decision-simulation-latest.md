# Service Worker Post-Decision Simulation

Generated UTC: 2026-06-15T11:06:36Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-post-decision-simulation-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-post-decision-simulation-validation-latest.json`

## Operating Rule

This report simulates what would remain after a human manually approves or rejects a decision packet. It does not run approve/reject commands, grant approvals or rejections, register pools, assign service requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.

- Simulations: `11`
- Branches: `22`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Simulation Rows

| Request | Approve Branch Remaining Gates | Reject Branch Result | Pool |
| --- | --- | --- | --- |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-test-browser-readonly-complete-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-wave4-digital-products-browser-readonly-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-browser-read-only-pool` |
| `req-grok-research-worker-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-signed-in-browser-read-only-pool` |
| `req-next-wave-digital-legal-payment-review-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-legal-kyc-payment-review-pool` |
| `req-next-wave-security-report-route-review-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-public-submission-review-pool` |
| `req-pydantic-ai-model-backed-adapter-20260614` | exact_scope_compatibility_refresh_required, service_worker_pool_registration_required, manual_assignment_required, execution_readiness_required, separate_worker_start_required | `rejected` | `service-worker-model-api-execution-pool` |

## Next Action

If a human/CRO manually approves a request later, refresh scope diff, gate map, pool registration, assignment plan, readiness, and chain integrity before any assignment or worker start. If a human/CRO manually rejects it, refresh the gate map and chain integrity to confirm terminal no-execution state.

