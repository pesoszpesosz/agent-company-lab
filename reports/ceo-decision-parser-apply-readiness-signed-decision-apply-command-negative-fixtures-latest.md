# CEO Decision Parser Apply Readiness Signed Decision Apply Command Negative Fixtures

Generated UTC: 2026-06-19T22:10:26Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures-validation-latest.json`

## Decision

`ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures_ready_no_mutation`

Created six local negative fixtures for the signed-decision apply command contract. Each fixture must be rejected before any future apply executor can mutate the target service request.

## Fixtures

| Fixture | Expected Rule | Execution Attempted |
| --- | --- | ---: |
| `apply-command-reject-missing-operator-signature` | `reject_missing_operator_signature` | `False` |
| `apply-command-reject-expired-approval` | `reject_expired_approval` | `False` |
| `apply-command-reject-stale-target-snapshot` | `reject_stale_target_snapshot` | `False` |
| `apply-command-reject-wrong-target-request-id` | `reject_wrong_target_request_id` | `False` |
| `apply-command-reject-unapproved-field-set` | `reject_unapproved_field_set` | `False` |
| `apply-command-reject-missing-explicit-execution-flag` | `reject_missing_explicit_execution_flag` | `False` |

## Boundary

These are local rejection fixtures only. They do not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.

## Next Action

Build a report-only guard runner for these negative fixtures before implementing or enabling any apply command execution path.

