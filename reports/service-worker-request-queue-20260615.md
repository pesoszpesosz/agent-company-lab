# Service Worker Request Queue - 2026-06-15

Generated UTC: 2026-06-14T21:59:06Z

Total worker requests: 14

No service request was approved, assigned, started, or executed by this backfill. All external side-effect flags remain false.

## By Worker Type

### browser_read_only (7)

- `req-next-wave-digital-marketplace-browser-readonly-20260614` lane=`digital_products_templates_plugins` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-next-wave-digital-marketplace-browser-readonly-20260614\service-worker-request-v1.json`
- `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` lane=`paid_code_bounties` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614\service-worker-request-v1.json`
- `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` lane=`security_bounty_private_reports` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-next-wave-security-google-oss-vrp-browser-readonly-20260614\service-worker-request-v1.json`
- `req-test-browser-readonly-complete-20260614` lane=`content_and_social_growth` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614\service-worker-request-v1.json`
- `req-wave4-ai-ml-competitions-browser-readonly-20260614` lane=`ai_ml_competitions` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-wave4-ai-ml-competitions-browser-readonly-20260614\service-worker-request-v1.json`
- `req-wave4-digital-products-browser-readonly-20260614` lane=`digital_products_templates_plugins` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-wave4-digital-products-browser-readonly-20260614\service-worker-request-v1.json`
- `req-wave4-money-source-discovery-browser-readonly-20260614` lane=`money_source_discovery` status=`needs_review` risk_gate=`catalog_required_approval_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-wave4-money-source-discovery-browser-readonly-20260614\service-worker-request-v1.json`

### browser_signed_in_read_only (1)

- `req-grok-research-worker-20260614` lane=`platform_engineering` status=`needs_review` risk_gate=`browser_grok_or_x_requires_signed_in_browser_and_no_public_actions` -> `E:\agent-company-lab\requests\service-requests\req-grok-research-worker-20260614\service-worker-request-v1.json`

### legal_kyc_tax_payment_review (1)

- `req-next-wave-digital-legal-payment-review-20260614` lane=`digital_products_templates_plugins` status=`needs_review` risk_gate=`legal_kyc_tax_payment_requires_user_decision_no_commitment` -> `E:\agent-company-lab\requests\service-requests\req-next-wave-digital-legal-payment-review-20260614\service-worker-request-v1.json`

### local_runtime_adapter (2)

- `req-test-lifecycle-approve-20260614` lane=`platform_engineering` status=`complete` risk_gate=`test_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-test-lifecycle-approve-20260614\service-worker-request-v1.json`
- `req-test-lifecycle-reject-20260614` lane=`platform_engineering` status=`rejected` risk_gate=`test_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-test-lifecycle-reject-20260614\service-worker-request-v1.json`

### model_api_execution (1)

- `req-pydantic-ai-model-backed-adapter-20260614` lane=`platform_engineering` status=`needs_review` risk_gate=`model_api_call_requires_provider_model_cost_lane_and_artifact_scope` -> `E:\agent-company-lab\requests\service-requests\req-pydantic-ai-model-backed-adapter-20260614\service-worker-request-v1.json`

### other_gated_worker (1)

- `req-test-service-intake-valid-20260614` lane=`platform_engineering` status=`rejected` risk_gate=`test_validator_no_external_action` -> `E:\agent-company-lab\requests\service-requests\req-test-service-intake-valid-20260614\service-worker-request-v1.json`

### public_submission (1)

- `req-next-wave-security-report-route-review-20260614` lane=`security_bounty_private_reports` status=`needs_review` risk_gate=`security_report_submission_requires_user_and_cro_approval_no_submission` -> `E:\agent-company-lab\requests\service-requests\req-next-wave-security-report-route-review-20260614\service-worker-request-v1.json`

## By Risk Gate

### browser_grok_or_x_requires_signed_in_browser_and_no_public_actions (1)

- `req-grok-research-worker-20260614` worker_type=`browser_signed_in_read_only` status=`needs_review`

### catalog_required_approval_no_external_action (7)

- `req-next-wave-digital-marketplace-browser-readonly-20260614` worker_type=`browser_read_only` status=`needs_review`
- `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` worker_type=`browser_read_only` status=`needs_review`
- `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` worker_type=`browser_read_only` status=`needs_review`
- `req-test-browser-readonly-complete-20260614` worker_type=`browser_read_only` status=`needs_review`
- `req-wave4-ai-ml-competitions-browser-readonly-20260614` worker_type=`browser_read_only` status=`needs_review`
- `req-wave4-digital-products-browser-readonly-20260614` worker_type=`browser_read_only` status=`needs_review`
- `req-wave4-money-source-discovery-browser-readonly-20260614` worker_type=`browser_read_only` status=`needs_review`

### legal_kyc_tax_payment_requires_user_decision_no_commitment (1)

- `req-next-wave-digital-legal-payment-review-20260614` worker_type=`legal_kyc_tax_payment_review` status=`needs_review`

### model_api_call_requires_provider_model_cost_lane_and_artifact_scope (1)

- `req-pydantic-ai-model-backed-adapter-20260614` worker_type=`model_api_execution` status=`needs_review`

### security_report_submission_requires_user_and_cro_approval_no_submission (1)

- `req-next-wave-security-report-route-review-20260614` worker_type=`public_submission` status=`needs_review`

### test_no_external_action (2)

- `req-test-lifecycle-approve-20260614` worker_type=`local_runtime_adapter` status=`complete`
- `req-test-lifecycle-reject-20260614` worker_type=`local_runtime_adapter` status=`rejected`

### test_validator_no_external_action (1)

- `req-test-service-intake-valid-20260614` worker_type=`other_gated_worker` status=`rejected`

## Next Action

Add a first-class service-worker queue report command or DB table, then test DBOS/Hatchet as durable queue adapters against this queue with no external actions.
