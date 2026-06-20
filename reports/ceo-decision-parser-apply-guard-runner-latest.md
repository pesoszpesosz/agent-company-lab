# CEO Decision Parser Apply Guard Runner

Generated UTC: 2026-06-15T23:55:20Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-guard-runner-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-guard-runner-validation-latest.json`

## Decision

`ceo_decision_parser_apply_guard_runner_passed_no_mutations`

Ran a local report-only apply guard against six negative apply fixtures. The guard rejected every unauthorized or underspecified apply request and performed no service request mutation.

## Guard Results

| Fixture | Expected Rule | Actual Rule | Match |
| --- | --- | --- | --- |
| `missing-explicit-mutation-approval` | `reject_missing_explicit_mutation_approval` | `reject_missing_explicit_mutation_approval` | `True` |
| `readonly-approval-not-mutation-approval` | `reject_readonly_scope_not_mutation_approval` | `reject_readonly_scope_not_mutation_approval` | `True` |
| `missing-target-service-request-ids` | `reject_missing_target_service_request_ids` | `reject_missing_target_service_request_ids` | `True` |
| `unbounded-update-count` | `reject_unbounded_or_excessive_update_count` | `reject_unbounded_or_excessive_update_count` | `True` |
| `forbidden-action-requested` | `reject_forbidden_action_requested` | `reject_forbidden_action_requested` | `True` |
| `missing-status-snapshot` | `reject_missing_service_request_status_snapshot` | `reject_missing_service_request_status_snapshot` | `True` |

## Boundary

This runner is report-only. It evaluated local apply fixtures and wrote local artifacts only; it did not mutate service requests, assign work, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.

## Next Action

Keep the apply path disabled; next create a positive apply dry-run fixture that previews the exact single service-request update without applying it.

