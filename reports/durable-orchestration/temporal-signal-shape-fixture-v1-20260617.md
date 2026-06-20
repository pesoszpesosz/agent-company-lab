# Temporal Signal Shape Fixture v1

Generated UTC: 2026-06-20T12:13:23Z
Fixture: `E:\agent-company-lab\reports\durable-orchestration\temporal-signal-shape-fixture-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-signal-shape-fixture-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\temporal-signal-shape-fixture-v1.schema.json`

## Summary

- Signal cases checked: `6`
- Passed: `6`
- Failed: `0`
- Temporal imports: `0`
- Temporal client connections: `0`
- Temporal workflows started: `0`
- Temporal signals sent: `0`
- Service requests updated: `0`
- External side effects: `false`

## Signal Cases

| Case | Signal | Request Status | Shape Valid | Disposition | Validation |
| --- | --- | --- | ---: | --- | --- |
| `case-valid-needs-review-approval-shape-parked` | `human_review_decision` | `needs_review` | `true` | `shape_valid_but_parked_no_mutation` | `pass` |
| `case-valid-needs-review-reject-shape-terminal-preview` | `human_review_decision` | `needs_review` | `true` | `shape_valid_reject_preview_no_mutation` | `pass` |
| `case-invalid-public-action-without-authority` | `human_review_decision` | `needs_review` | `false` | `reject_shape_public_action_not_authorized` | `pass` |
| `case-invalid-sensitive-payload` | `human_review_decision` | `needs_review` | `false` | `reject_shape_sensitive_field_present` | `pass` |
| `case-terminal-complete-no-replay-start` | `terminal_snapshot_notice` | `complete` | `true` | `terminal_notice_no_replay_start` | `pass` |
| `case-terminal-rejected-no-revive` | `terminal_snapshot_notice` | `rejected` | `true` | `terminal_notice_no_revive` | `pass` |

## Decision

Temporal remains a contract-preview target only. These payloads define what a future signal handler may accept or reject, but this artifact does not register handlers, connect a client, start a Workflow, send a Signal, execute a Query or Update, schedule an Activity, or mutate service requests.

## Boundary

- No Temporal package import.
- No Temporal client connection.
- No Temporal server, Worker, Workflow, Signal, Query, Update, or Activity.
- No service request mutation.
- No browser, model/API, public, account, wallet, payment, security, or real-money action.
