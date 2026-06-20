# Restate Agent Service Boundary Fixture v1

Generated UTC: 2026-06-20T12:29:58Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\restate-agent-service-boundary-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\restate-agent-service-boundary-fixture-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\restate-agent-service-boundary-fixture-v1.schema.json`

## Summary

- Cases checked: `6`
- Passed: `6`
- Failed: `0`
- Restate imports: `0`
- Restate server starts: `0`
- Services registered: `0`
- Handlers invoked: `0`
- Service/object/workflow sends: `0`
- Journal writes: `0`
- State mutations: `0`
- LLM calls: `0`
- Tool executions: `0`
- External side effects: `false`

## Case Rows

| Case | Message | Shape | Disposition | Validation |
| --- | --- | --- | --- | --- |
| `case-valid-artifact-notice-ceo-preview` | `msg-wave10-central-outbox-build-20260617` | `basic_service_preview` | `local_preview_only` | `pass` |
| `case-valid-gate-request-virtual-object-parked` | `msg-paid-code-parser-followup-20260617` | `virtual_object_preview` | `park_awaiting_human_review` | `pass` |
| `case-valid-local-dispatch-workflow-preview` | `msg-ai-competition-arc-followup-20260617` | `workflow_preview` | `local_preview_only` | `pass` |
| `case-invalid-gate-request-service-send` | `msg-paid-code-parser-followup-20260617` | `virtual_object_preview` | `send_service_message` | `pass` |
| `case-invalid-local-dispatch-llm-tool-public-action` | `msg-ai-competition-arc-followup-20260617` | `workflow_preview` | `execute_tool` | `pass` |
| `case-invalid-prohibited-action-artifact-notice-state-mutation` | `msg-wave10-central-outbox-build-20260617` | `basic_service_preview` | `mutate_state` | `pass` |

## Decision

This fixture treats Restate as a future durable agent/service runtime only. It allows local preview mappings from central outbox messages to Basic Service, Virtual Object, and Workflow shapes. It rejects handler invocation, service/object/workflow calls or sends, journal writes, state mutation, LLM calls, tool execution, worker starts, browser/API/model/public actions, service-request mutation, and external side effects.

## Boundary

- No Restate package import.
- No Restate server, service registration, handler invocation, service call/send, object call/send, or workflow call/send.
- No journal write, state mutation, LLM call, or tool execution.
- No service-request mutation, worker start, browser session, API/model call, public action, account/wallet/payment action, security test, real-money action, or external side effect.
