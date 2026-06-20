# Temporal/Inngest Adapter Reducer State Machine

Generated UTC: 2026-06-15T14:36:50Z

This reducer spec consumes local preview events only. It does not invoke Temporal, Inngest, model APIs, browsers, workers, or ledger mutations.

## State Machine

| Input status | Output state | Terminal | Parked | Mutates ledger | Assigns | Starts worker |
|---|---|---:|---:|---:|---:|---:|
| `needs_review` | `parked.awaiting_human_review` | `False` | `True` | `False` | `False` | `False` |
| `complete` | `terminal.completed_from_ledger_snapshot` | `True` | `False` | `False` | `False` | `False` |
| `rejected` | `terminal.rejected_from_ledger_snapshot` | `True` | `False` | `False` | `False` | `False` |

## Replay Validation

- Events reduced: `14`
- Output states: `{'parked.awaiting_human_review': 11, 'terminal.completed_from_ledger_snapshot': 1, 'terminal.rejected_from_ledger_snapshot': 2}`
- Duplicate replay checks: `28`
- Failure count: `0`
- All checks passed: `True`

## Runtime Boundary

- `dependency_installs`: `0`
- `dependency_imports`: `0`
- `temporal_server_started`: `False`
- `inngest_service_started`: `False`
- `temporal_workflows_started`: `0`
- `temporal_activities_scheduled`: `0`
- `inngest_functions_registered`: `0`
- `inngest_events_emitted`: `0`
- `reducer_invocations_against_live_runtime`: `0`
- `worker_starts`: `0`
- `service_requests_updated`: `0`
- `service_requests_assigned`: `0`
- `approvals_granted`: `0`
- `api_calls`: `False`
- `external_side_effects`: `False`

## Reducer Outputs

| Request | Input | Output | Worker | Mutates? | Emits? | Required gates |
|---|---|---|---|---:|---:|---|
| `req-grok-research-worker-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_signed_in_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; signed-in browser approval; read-only prompt scope; no post/reply/like/follow/message/settings changes |
| `req-next-wave-digital-legal-payment-review-20260614` | `needs_review` | `parked.awaiting_human_review` | `legal_kyc_tax_payment_review` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; user legal/payment decision; no KYC/tax/payment entry by automation; no contract acceptance by replay |
| `req-next-wave-digital-marketplace-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |
| `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |
| `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |
| `req-next-wave-security-report-route-review-20260614` | `needs_review` | `parked.awaiting_human_review` | `public_submission` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; user approval; CRO approval; program scope verified; submission route verified; no automatic submission |
| `req-pydantic-ai-model-backed-adapter-20260614` | `needs_review` | `parked.awaiting_human_review` | `model_api_execution` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; provider selected; model selected; max cost set; credential route approved; lane/output artifact scope approved |
| `req-test-browser-readonly-complete-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |
| `req-test-lifecycle-approve-20260614` | `complete` | `terminal.completed_from_ledger_snapshot` | `local_runtime_adapter` | `False` | `False` | new explicit task or service request; do not replay-start terminal rows; explicit approval for risk gate |
| `req-test-lifecycle-reject-20260614` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `local_runtime_adapter` | `False` | `False` | new explicit request; do not revive rejected rows by replay; explicit approval for risk gate |
| `req-test-service-intake-valid-20260614` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `other_gated_worker` | `False` | `False` | new explicit request; do not revive rejected rows by replay; explicit approval for risk gate |
| `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |
| `req-wave4-digital-products-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |
| `req-wave4-money-source-discovery-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `False` | `False` | human approval packet; CRO/CEO approval if risk gate requires it; exact request scope match; eligible worker pool registered; artifact output path approved; catalog approval; public read-only scope; no login/signup/form/public/payment action |

## Files

- Reducer spec JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-reducer-state-machine-20260615.json`
- Reducer validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-reducer-validation-20260615.json`
- Source replay validation: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-replay-validation-20260615.json`
