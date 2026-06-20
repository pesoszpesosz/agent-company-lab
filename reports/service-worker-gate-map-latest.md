# Service Worker Gate Map

Generated UTC: 2026-06-19T21:38:45Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-gate-map-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-gate-map-validation-latest.json`

## Operating Rule

This report maps each service-worker request to its current blocking gate. It grants no approval and does not register pools, assign, start, complete, enqueue, update, browse, call APIs, post, submit, register accounts, trade, spend, or contact anyone.

- Requests mapped: `16`
- Ready for assignment: `0`
- Gate counts: `{"human_cro_approval_required": 13, "terminal_no_execution": 3}`
- Pool status counts: `{"missing_service_worker_pool": 16}`
- Pools registered by gate map: `0`
- Service requests assigned by gate map: `0`
- Worker starts: `0`
- API calls: `False`
- External side effects: `False`

## Request Gates

| Status | Blocking Gate | Request | Worker Type | Pool | Pool Status | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| `needs_review` | `human_cro_approval_required` | `req-algora-opik-readonly-refresh-20260618` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-grok-research-worker-20260614` | `browser_signed_in_read_only` | `service-worker-signed-in-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-next-wave-digital-legal-payment-review-20260614` | `legal_kyc_tax_payment_review` | `service-worker-legal-kyc-payment-review-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-next-wave-security-report-route-review-20260614` | `public_submission` | `service-worker-public-submission-review-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-promptbase-guideline-readonly-review-20260618` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-pydantic-ai-model-backed-adapter-20260614` | `model_api_execution` | `service-worker-model-api-execution-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-test-browser-readonly-complete-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `complete` | `terminal_no_execution` | `req-test-lifecycle-approve-20260614` | `local_runtime_adapter` | `service-worker-local-runtime-adapter-pool` | `missing_service_worker_pool` | Do not execute terminal requests; keep audit evidence or create a fresh scoped request. |
| `rejected` | `terminal_no_execution` | `req-test-lifecycle-reject-20260614` | `local_runtime_adapter` | `service-worker-local-runtime-adapter-pool` | `missing_service_worker_pool` | Do not execute terminal requests; keep audit evidence or create a fresh scoped request. |
| `rejected` | `terminal_no_execution` | `req-test-service-intake-valid-20260614` | `other_gated_worker` | `service-worker-other-gated-work-pool` | `missing_service_worker_pool` | Do not execute terminal requests; keep audit evidence or create a fresh scoped request. |
| `needs_review` | `human_cro_approval_required` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-wave4-digital-products-browser-readonly-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |
| `needs_review` | `human_cro_approval_required` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `browser_read_only` | `service-worker-browser-read-only-pool` | `missing_service_worker_pool` | Use the CRO review queue for a separate manual approve/reject decision. |

## Gate Order

1. Packet must be valid.
2. Human/CRO review must be ready.
3. Service request must be separately approved or assigned.
4. Exact approval scope must be compatible with the packet.
5. Required service-worker pool must be registered.
6. Execution-readiness verifier must pass.
7. Assignment must still be a separate manual action.

## Next Action

Use this gate map as the CEO/CRO board for deciding which local preparation step comes next. Current requests should not be assigned or started until every prior gate is explicitly satisfied in the generated reports.

