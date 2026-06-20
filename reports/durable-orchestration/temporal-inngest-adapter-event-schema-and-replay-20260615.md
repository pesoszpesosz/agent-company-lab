# Temporal/Inngest Adapter Event Schema and Replay Validation

Generated UTC: 2026-06-15T14:33:09Z

This is a local proof artifact only. It defines event payloads and replay checks, but emits no Inngest events, starts no Temporal workflows, schedules no activities, and changes no service requests.

## Contract

- Event payload schema: `agent_company.service_request_event.v1`
- Adapter event schema: `temporal_inngest_adapter_event_schema.v1`
- Replay validation: `temporal_inngest_adapter_replay_validation.v1`
- Idempotency format: `service-request-event:{request_id}:{event_name}:{status_snapshot}:{risk_gate}`

## Runtime Boundary

- `dependency_installs`: `0`
- `dependency_imports`: `0`
- `temporal_server_started`: `False`
- `inngest_service_started`: `False`
- `temporal_workflows_started`: `0`
- `temporal_activities_scheduled`: `0`
- `inngest_functions_registered`: `0`
- `inngest_events_emitted`: `0`
- `worker_starts`: `0`
- `service_requests_updated`: `0`
- `service_requests_assigned`: `0`
- `approvals_granted`: `0`
- `api_calls`: `False`
- `external_side_effects`: `False`

## Replay Summary

- Preview events built: `14`
- Unique idempotency keys: `14`
- Status counts: `{'complete': 1, 'needs_review': 11, 'rejected': 2}`
- Event counts: `{'agent_company/service_request.completed': 1, 'agent_company/service_request.needs_review': 11, 'agent_company/service_request.rejected': 2}`
- Worker counts: `{'browser_read_only': 7, 'browser_signed_in_read_only': 1, 'legal_kyc_tax_payment_review': 1, 'local_runtime_adapter': 2, 'model_api_execution': 1, 'other_gated_worker': 1, 'public_submission': 1}`
- Failure count: `0`
- All checks passed: `True`

## Blocked Transitions

- needs_review -> assigned without explicit approval
- needs_review -> started without approval, assignment, and readiness
- rejected -> assigned by replay
- rejected -> started by replay
- complete -> started by replay
- any -> model_api_execution without provider/model/max_cost/credential/output-scope approval
- any -> browser/account/payment/wallet/public/security-test/legal commitment without separate approval

## Preview Events

| # | Request | Event | Status | Temporal State | Mutates? | Starts? |
|---:|---|---|---|---|---:|---:|
| 1 | `req-grok-research-worker-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 2 | `req-next-wave-digital-legal-payment-review-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 3 | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 4 | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 5 | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 6 | `req-next-wave-security-report-route-review-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 7 | `req-pydantic-ai-model-backed-adapter-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 8 | `req-test-browser-readonly-complete-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 9 | `req-test-lifecycle-approve-20260614` | `agent_company/service_request.completed` | `complete` | `completed_no_action_or_verified` | `False` | `False` |
| 10 | `req-test-lifecycle-reject-20260614` | `agent_company/service_request.rejected` | `rejected` | `terminal_rejected` | `False` | `False` |
| 11 | `req-test-service-intake-valid-20260614` | `agent_company/service_request.rejected` | `rejected` | `terminal_rejected` | `False` | `False` |
| 12 | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 13 | `req-wave4-digital-products-browser-readonly-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |
| 14 | `req-wave4-money-source-discovery-browser-readonly-20260614` | `agent_company/service_request.needs_review` | `needs_review` | `awaiting_human_review` | `False` | `False` |

## Files

- Schema JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-event-schema-20260615.json`
- Replay validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-replay-validation-20260615.json`
- Source manifest: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-service-request-adapter-manifest-20260615.json`
