# CEO Decision Parser Apply Negative Fixtures

Generated UTC: 2026-06-15T23:51:48Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-negative-fixtures-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-negative-fixtures-validation-latest.json`

## Decision

`ceo_decision_parser_apply_negative_fixtures_ready`

Created local negative fixtures for the future CEO decision parser apply path, covering missing mutation approval, read-only-only approval, missing targets, excessive update count, forbidden action conflict, and missing status snapshot.

## Fixtures

| Fixture | Expected Rule |
| --- | --- |
| `missing-explicit-mutation-approval` | `reject_missing_explicit_mutation_approval` |
| `readonly-approval-not-mutation-approval` | `reject_readonly_scope_not_mutation_approval` |
| `missing-target-service-request-ids` | `reject_missing_target_service_request_ids` |
| `unbounded-update-count` | `reject_unbounded_or_excessive_update_count` |
| `forbidden-action-requested` | `reject_forbidden_action_requested` |
| `missing-status-snapshot` | `reject_missing_service_request_status_snapshot` |

## Boundary

These are local negative fixtures only. They apply no mutation, update no service request, request no approval, start no worker, call no API, open no browser, and perform no account, wallet, payment, public, security-testing, external, or real-money action.

## Next Action

Use these fixtures before building any apply path; every unauthorized or underspecified apply attempt must be rejected before service request mutations are allowed.

