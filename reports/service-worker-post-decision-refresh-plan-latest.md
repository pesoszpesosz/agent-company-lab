# Service Worker Post-Decision Refresh Plan

Generated UTC: 2026-06-15T11:22:43Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-post-decision-refresh-plan-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-post-decision-refresh-plan-validation-latest.json`

## Operating Rule

This report tells the CEO/CRO which local reports to refresh after a human manually approves or rejects a service-worker decision packet. It does not run those commands, approve or reject requests, register pools, assign requests, update service requests, start workers, call APIs, browse, post, submit, pay, trade, or contact anyone.

- Refresh plans: `11`
- Approval sequences: `11`
- Rejection sequences: `11`
- Command previews: `99`
- Validation failures: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Refresh Rows

| Request | Approval Refresh Commands | Rejection Refresh Commands | Start Gate |
| --- | --- | --- | --- |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-test-browser-readonly-complete-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-wave4-digital-products-browser-readonly-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-grok-research-worker-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-next-wave-digital-legal-payment-review-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-next-wave-security-report-route-review-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |
| `req-pydantic-ai-model-backed-adapter-20260614` | write-service-worker-scope-diff, write-service-worker-gate-map, write-service-worker-pool-registry, write-service-worker-pool-registration-plan, write-service-worker-assignment-plan, write-service-worker-execution-readiness, write-service-worker-chain-integrit | write-service-worker-gate-map, write-service-worker-chain-integrity | `separate_worker_start_required` |

## Next Action

After any manual approve/reject command is run by a human/CRO, refresh the listed local reports and re-run chain integrity before assigning a service request or starting a worker. This plan itself is only a checklist.

