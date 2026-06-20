# Service Worker Dequeue Plan

Generated UTC: 2026-06-19T14:16:55Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-dequeue-plan-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-dequeue-plan-validation-latest.json`
Result directory: `E:\agent-company-lab\reports\service-worker-dequeue-results`

## Operating Rule

This command is a local deterministic dequeue dry-run. It writes local result placeholders only. It does not approve, assign, start, complete, browse, register, trade, spend, post, submit, call external APIs, enqueue external jobs, or contact anyone.

- Worker requests evaluated: `16`
- Result files written: `32`
- Route counts: `{"hold_for_approval_no_worker_start": 13, "terminal_complete_no_worker_start": 1, "terminal_rejected_no_worker_start": 2}`
- By status: `{"complete": 1, "needs_review": 13, "rejected": 2}`
- By worker type: `{"browser_read_only": 9, "browser_signed_in_read_only": 1, "legal_kyc_tax_payment_review": 1, "local_runtime_adapter": 2, "model_api_execution": 1, "other_gated_worker": 1, "public_submission": 1}`
- Worker starts: `0`
- Service requests updated: `0`
- API calls: `False`
- External side effects: `False`

## Results

| Status | Route | Source Request | Lane | Worker Type | Result |
| --- | --- | --- | --- | --- | --- |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-algora-opik-readonly-refresh-20260618` | `paid_code_bounties` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-algora-opik-readonly-refresh-20260618-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-grok-research-worker-20260614` | `platform_engineering` | `browser_signed_in_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-grok-research-worker-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-next-wave-digital-legal-payment-review-20260614` | `digital_products_templates_plugins` | `legal_kyc_tax_payment_review` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-next-wave-digital-legal-payment-review-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `digital_products_templates_plugins` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-next-wave-digital-marketplace-browser-readonly-20260615-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `paid_code_bounties` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-next-wave-paid-code-algora-archestra-browser-readonly-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `security_bounty_private_reports` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-next-wave-security-google-oss-vrp-browser-readonly-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-next-wave-security-report-route-review-20260614` | `security_bounty_private_reports` | `public_submission` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-next-wave-security-report-route-review-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-promptbase-guideline-readonly-review-20260618` | `digital_products_templates_plugins` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-promptbase-guideline-readonly-review-20260618-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-pydantic-ai-model-backed-adapter-20260614` | `platform_engineering` | `model_api_execution` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-pydantic-ai-model-backed-adapter-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-test-browser-readonly-complete-20260614` | `content_and_social_growth` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-test-browser-readonly-complete-20260614-dequeue-result.md` |
| `complete` | `terminal_complete_no_worker_start` | `req-test-lifecycle-approve-20260614` | `platform_engineering` | `local_runtime_adapter` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-test-lifecycle-approve-20260614-dequeue-result.md` |
| `rejected` | `terminal_rejected_no_worker_start` | `req-test-lifecycle-reject-20260614` | `platform_engineering` | `local_runtime_adapter` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-test-lifecycle-reject-20260614-dequeue-result.md` |
| `rejected` | `terminal_rejected_no_worker_start` | `req-test-service-intake-valid-20260614` | `platform_engineering` | `other_gated_worker` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-test-service-intake-valid-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `ai_ml_competitions` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-wave4-ai-ml-competitions-browser-readonly-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-wave4-digital-products-browser-readonly-20260614` | `digital_products_templates_plugins` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-wave4-digital-products-browser-readonly-20260614-dequeue-result.md` |
| `needs_review` | `hold_for_approval_no_worker_start` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `money_source_discovery` | `browser_read_only` | `E:\agent-company-lab\reports\service-worker-dequeue-results\swr-wave4-money-source-discovery-browser-readonly-20260614-dequeue-result.md` |

## Next Action

Promote the SQLite path only after adding a worker lease check and exact approval-scope verifier. Keep DBOS, Hatchet, and Temporal at manifest-only status until this local dry-run contract is boring and repeatable.

