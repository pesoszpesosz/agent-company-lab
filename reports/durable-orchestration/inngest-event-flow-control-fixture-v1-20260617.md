# Inngest Event Flow-Control Fixture v1

Generated UTC: 2026-06-20T12:32:35Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\inngest-event-flow-control-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\inngest-event-flow-control-fixture-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\inngest-event-flow-control-fixture-v1.schema.json`

## Summary

- Events checked: `4`
- Passed: `4`
- Failed: `0`
- Inngest imports: `0`
- Inngest functions registered: `0`
- Inngest events sent: `0`
- Service requests updated: `0`
- External side effects: `false`

## Event Rows

| Event | Source Message | Name | Decision | Validation |
| --- | --- | --- | --- | --- |
| `evt-msg-wave10-central-outbox-build-20260617` | `msg-wave10-central-outbox-build-20260617` | `agent_company/outbox.artifact_notice` | `valid_local_preview_event` | `pass` |
| `evt-msg-paid-code-parser-followup-20260617` | `msg-paid-code-parser-followup-20260617` | `agent_company/outbox.gate_request` | `valid_gate_request_event_parked` | `pass` |
| `evt-msg-ai-competition-arc-followup-20260617` | `msg-ai-competition-arc-followup-20260617` | `agent_company/outbox.dispatch` | `valid_local_dispatch_event` | `pass` |
| `evt-invalid-public-action-20260617` | `msg-paid-code-parser-followup-20260617` | `agent_company/outbox.invalid_public_action` | `reject_public_action_or_silent_skip` | `pass` |

## Decision

This is a static contract for future Inngest adapters. It defines event names, idempotency keys, concurrency keys, throttle keys, and rate-limit behavior from central outbox messages. It does not create an Inngest client, register functions, send events, start a server, call APIs, or mutate service requests.

## Boundary

- No Inngest package import.
- No Inngest client, function registration, server, send, or step event.
- No service request mutation.
- No browser, model/API, public, account, wallet, payment, security, or real-money action.
