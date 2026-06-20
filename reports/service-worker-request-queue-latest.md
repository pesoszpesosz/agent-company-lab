# Service Worker Request Queue

Generated UTC: 2026-06-19T14:16:55Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-worker-request-queue-latest.json`
Validation: `E:\agent-company-lab\reports\service-worker-request-queue-validation-latest.json`

## Operating Rule

This report is read-only queue infrastructure. It does not approve, assign, start, browse, register, trade, spend, post, submit, call external APIs, or contact anyone.

- Worker requests in report: `16`
- By worker type: `{"browser_read_only": 9, "browser_signed_in_read_only": 1, "legal_kyc_tax_payment_review": 1, "local_runtime_adapter": 2, "model_api_execution": 1, "other_gated_worker": 1, "public_submission": 1}`
- By status: `{"complete": 1, "needs_review": 13, "rejected": 2}`

## Queue By Worker Type

### browser_read_only (9)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `needs_review` | `req-algora-opik-readonly-refresh-20260618` | `paid_code_bounties` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-algora-opik-readonly-refresh-20260618\service-worker-request-v1.json` |
| `needs_review` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `digital_products_templates_plugins` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-next-wave-digital-marketplace-browser-readonly-20260614\service-worker-request-v1.json` |
| `needs_review` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `paid_code_bounties` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614\service-worker-request-v1.json` |
| `needs_review` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `security_bounty_private_reports` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-next-wave-security-google-oss-vrp-browser-readonly-20260614\service-worker-request-v1.json` |
| `needs_review` | `req-promptbase-guideline-readonly-review-20260618` | `digital_products_templates_plugins` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-promptbase-guideline-readonly-review-20260618\service-worker-request-v1.json` |
| `needs_review` | `req-test-browser-readonly-complete-20260614` | `content_and_social_growth` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614\service-worker-request-v1.json` |
| `needs_review` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `ai_ml_competitions` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-wave4-ai-ml-competitions-browser-readonly-20260614\service-worker-request-v1.json` |
| `needs_review` | `req-wave4-digital-products-browser-readonly-20260614` | `digital_products_templates_plugins` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-wave4-digital-products-browser-readonly-20260614\service-worker-request-v1.json` |
| `needs_review` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `money_source_discovery` | catalog_required_approval_no_external_action | `E:\agent-company-lab\requests\service-requests\req-wave4-money-source-discovery-browser-readonly-20260614\service-worker-request-v1.json` |

### browser_signed_in_read_only (1)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `needs_review` | `req-grok-research-worker-20260614` | `platform_engineering` | browser_grok_or_x_requires_signed_in_browser_and_no_public_actions | `E:\agent-company-lab\requests\service-requests\req-grok-research-worker-20260614\service-worker-request-v1.json` |

### legal_kyc_tax_payment_review (1)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `needs_review` | `req-next-wave-digital-legal-payment-review-20260614` | `digital_products_templates_plugins` | legal_kyc_tax_payment_requires_user_decision_no_commitment | `E:\agent-company-lab\requests\service-requests\req-next-wave-digital-legal-payment-review-20260614\service-worker-request-v1.json` |

### local_runtime_adapter (2)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `complete` | `req-test-lifecycle-approve-20260614` | `platform_engineering` | test_no_external_action | `E:\agent-company-lab\requests\service-requests\req-test-lifecycle-approve-20260614\service-worker-request-v1.json` |
| `rejected` | `req-test-lifecycle-reject-20260614` | `platform_engineering` | test_no_external_action | `E:\agent-company-lab\requests\service-requests\req-test-lifecycle-reject-20260614\service-worker-request-v1.json` |

### model_api_execution (1)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `needs_review` | `req-pydantic-ai-model-backed-adapter-20260614` | `platform_engineering` | model_api_call_requires_provider_model_cost_lane_and_artifact_scope | `E:\agent-company-lab\requests\service-requests\req-pydantic-ai-model-backed-adapter-20260614\service-worker-request-v1.json` |

### other_gated_worker (1)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `rejected` | `req-test-service-intake-valid-20260614` | `platform_engineering` | test_validator_no_external_action | `E:\agent-company-lab\requests\service-requests\req-test-service-intake-valid-20260614\service-worker-request-v1.json` |

### public_submission (1)

| Status | Source Request | Lane | Risk Gate | Packet |
| --- | --- | --- | --- | --- |
| `needs_review` | `req-next-wave-security-report-route-review-20260614` | `security_bounty_private_reports` | security_report_submission_requires_user_and_cro_approval_no_submission | `E:\agent-company-lab\requests\service-requests\req-next-wave-security-report-route-review-20260614\service-worker-request-v1.json` |

## Next Action

Use this command as the first-class queue surface, then test DBOS/Hatchet durable queue adapter manifests against these packets with no external actions.

