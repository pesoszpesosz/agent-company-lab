# Service Worker Request v1

Generated UTC: 2026-06-14T21:59:06Z

- Worker request ID: `swr-pydantic-ai-model-backed-adapter-20260614`
- Source service request: `req-pydantic-ai-model-backed-adapter-20260614`
- Worker type: `model_api_execution`
- Lane: `platform_engineering`
- Status: `needs_review`
- Risk gate: `model_api_call_requires_provider_model_cost_lane_and_artifact_scope`

## Non-Approval Notice

This backfill artifact grants no approval and performs no execution. It only converts the current service request row into the service_worker_request.v1 contract.

## Objective

Review a cost-bearing model/API execution request for req-pydantic-ai-model-backed-adapter-20260614; do not call external providers until provider, model, max cost, and artifact scope are explicitly approved.

## Allowed Actions

- prepare local cost/scope review
- identify provider, model, max cost, input/output artifact scope, and data sensitivity
- wait for explicit approval before any API call

## Prohibited Actions

- execute without explicit approval
- login unless explicitly approved
- signup or account creation
- accept terms or legal agreements
- enter credentials, OTPs, personal data, private files, payment details, tax/KYC data, or wallet information
- submit forms
- publish, post, reply, comment, message, list, upload, or contact external parties
- purchase, deposit, withdraw, trade, connect wallet, sign wallet messages, or perform real-money actions
- change account settings
- bypass paywalls, rate limits, access controls, or platform rules
