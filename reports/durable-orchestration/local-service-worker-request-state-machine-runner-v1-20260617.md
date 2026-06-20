# Local Service-Worker Request State-Machine Runner Preview v1

Generated UTC: 2026-06-17T17:47:35Z
Preview JSON: `E:\agent-company-lab\reports\durable-orchestration\local-service-worker-request-state-machine-runner-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\local-service-worker-request-state-machine-runner-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\local-service-worker-request-state-machine-runner-v1.schema.json`

## Summary

- Transitions checked: `14`
- Policy probes checked: `5`
- Failed: `0`
- DB counts changed: `false`
- Service requests updated: `0`
- Service requests assigned: `0`
- Worker starts: `0`
- Browser sessions: `0`
- External side effects: `false`

## Transition Preview

| Worker Request | Status | Disposition | Assignment Preview | Start Preview | Command |
| --- | --- | --- | --- | --- | --- |
| `swr-grok-research-worker-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-next-wave-digital-legal-payment-review-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-next-wave-digital-marketplace-browser-readonly-20260615` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-next-wave-security-report-route-review-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-pydantic-ai-model-backed-adapter-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-test-browser-readonly-complete-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-test-lifecycle-approve-20260614` | `complete` | `terminal_noop` | `false` | `false` | `no_op_terminal_state` |
| `swr-test-lifecycle-reject-20260614` | `rejected` | `terminal_noop` | `false` | `false` | `no_op_terminal_state` |
| `swr-test-service-intake-valid-20260614` | `rejected` | `terminal_noop` | `false` | `false` | `no_op_terminal_state` |
| `swr-wave4-ai-ml-competitions-browser-readonly-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-wave4-digital-products-browser-readonly-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |
| `swr-wave4-money-source-discovery-browser-readonly-20260614` | `needs_review` | `parked_awaiting_human_review` | `false` | `false` | `keep_parked` |

## Policy Probes

| Probe | Status | Expected Disposition | Expected Command |
| --- | --- | --- | --- |
| `probe-approved-readonly-preview-only` | `approved` | `preview_assignment_or_start_only` | `preview_assign_worker` |
| `probe-needs-review-cannot-start` | `needs_review` | `parked_awaiting_human_review` | `keep_parked` |
| `probe-complete-never-revives` | `complete` | `terminal_noop` | `no_op_terminal_state` |
| `probe-rejected-never-revives` | `rejected` | `terminal_noop` | `no_op_terminal_state` |
| `probe-approved-public-action-without-scope-stays-parked` | `approved` | `park_until_scope_fixed` | `park_until_scope_fixed` |

## Decision

This preview proves the local state-machine semantics before any service-worker execution exists. Current queue rows remain parked or terminal. A future approved row may preview assignment/start commands, but this runner still does not write back to the database or start a worker.

## Boundary

- No service-request update, assignment, start, completion, or rejection.
- No worker start, browser session, queue enqueue, outbox update, dependency import/install, runtime start, API/model call, public/account/wallet/payment/security/real-money action, or external side effect.
