# Temporal/Inngest Service-Request Adapter Manifest

Generated UTC: 2026-06-15T14:28:46Z

This is a design manifest only. It installs no dependencies, imports no Temporal/Inngest packages, starts no servers, emits no events, assigns no workers, and changes no service-request state.

## Runtime Boundary

- `dependency_installs`: `0`
- `dependency_imports`: `0`
- `temporal_server_started`: `False`
- `inngest_service_started`: `False`
- `temporal_workflows_started`: `0`
- `inngest_functions_registered`: `0`
- `inngest_events_emitted`: `0`
- `worker_starts`: `0`
- `service_requests_updated`: `0`
- `service_requests_assigned`: `0`
- `approvals_granted`: `0`
- `api_calls`: `False`
- `external_side_effects`: `False`

## Adapter Concepts

- Temporal workflow type: `ServiceRequestLifecycleWorkflow`
- Temporal workflow ID format: `service-request/{request_id}`
- Inngest function ID format: `service-request-lifecycle-{worker_type}`
- Pause points: `needs_review`, high-risk gates, missing worker pool, exact scope mismatch, human/CRO/CEO approval required.

## Summary

- Service requests mapped: `14`
- By status: `{'complete': 1, 'needs_review': 11, 'rejected': 2}`
- By worker type: `{'browser_read_only': 7, 'browser_signed_in_read_only': 1, 'legal_kyc_tax_payment_review': 1, 'local_runtime_adapter': 2, 'model_api_execution': 1, 'other_gated_worker': 1, 'public_submission': 1}`
- By lane: `{'ai_ml_competitions': 1, 'content_and_social_growth': 1, 'digital_products_templates_plugins': 3, 'money_source_discovery': 1, 'paid_code_bounties': 1, 'platform_engineering': 5, 'security_bounty_private_reports': 2}`

## Request Mapping

| Request | Status | Worker Type | Temporal State | Event Preview | Pause Reason |
|---|---:|---|---|---|---|
| `req-grok-research-worker-20260614` | `needs_review` | `browser_signed_in_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate browser_grok_or_x_requires_signed_in_browser_and_no_public_actions; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-next-wave-digital-legal-payment-review-20260614` | `needs_review` | `legal_kyc_tax_payment_review` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate legal_kyc_tax_payment_requires_user_decision_no_commitment; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-next-wave-security-report-route-review-20260614` | `needs_review` | `public_submission` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate security_report_submission_requires_user_and_cro_approval_no_submission; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-pydantic-ai-model-backed-adapter-20260614` | `needs_review` | `model_api_execution` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate model_api_call_requires_provider_model_cost_lane_and_artifact_scope; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-test-browser-readonly-complete-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-test-lifecycle-approve-20260614` | `complete` | `local_runtime_adapter` | `completed_no_action_or_verified` | `agent_company/service_request.completed` | Terminal complete state from existing ledger; adapter must not replay execution or mutate the request. |
| `req-test-lifecycle-reject-20260614` | `rejected` | `local_runtime_adapter` | `terminal_rejected` | `agent_company/service_request.rejected` | Terminal rejected state from existing ledger; adapter must not assign, start, or revive the request. |
| `req-test-service-intake-valid-20260614` | `rejected` | `other_gated_worker` | `terminal_rejected` | `agent_company/service_request.rejected` | Terminal rejected state from existing ledger; adapter must not assign, start, or revive the request. |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-wave4-digital-products-browser-readonly-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `needs_review` | `browser_read_only` | `awaiting_human_review` | `agent_company/service_request.needs_review` | Paused at risk gate catalog_required_approval_no_external_action; explicit human/CRO/CEO approval, worker assignment, and exact scope match are missing. |

## Validation

- Manifest rows: `14`
- Needs review: `11`
- Terminal rows: `3`
- Failure count: `0`
- All no-execution checks passed: `True`

JSON manifest: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-service-request-adapter-manifest-20260615.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-service-request-adapter-manifest-validation-20260615.json`
## Artifact Integrity

Final SHA-256 values are stored in the SQLite `artifacts` table and verified after file write; self-hashes are omitted from JSON payloads to avoid recursive hash churn.
