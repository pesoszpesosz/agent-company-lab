# CEO Decision Parser Apply Readiness Signed Decision Apply Command Guard Runner

Generated UTC: 2026-06-16T10:32:42Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-apply-command-guard-runner-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-apply-command-guard-runner-validation-latest.json`

## Decision

`ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner_rejected_all_no_mutation`

Ran the local report-only guard runner for six signed-decision apply command negative fixtures. Every fixture rejected with its expected rule, and no apply command execution was attempted.

## Results

| Fixture | Accepted | Rule | Match |
| --- | ---: | --- | ---: |
| `apply-command-reject-missing-operator-signature` | `False` | `reject_missing_operator_signature` | `True` |
| `apply-command-reject-expired-approval` | `False` | `reject_expired_approval` | `True` |
| `apply-command-reject-stale-target-snapshot` | `False` | `reject_stale_target_snapshot` | `True` |
| `apply-command-reject-wrong-target-request-id` | `False` | `reject_wrong_target_request_id` | `True` |
| `apply-command-reject-unapproved-field-set` | `False` | `reject_unapproved_field_set` | `True` |
| `apply-command-reject-missing-explicit-execution-flag` | `False` | `reject_missing_explicit_execution_flag` | `True` |

## Boundary

This runner is report-only. It evaluates local negative fixtures and writes local artifacts only; it does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.

## Next Action

Keep the apply command disabled; next create a positive signed operator apply fixture only as local data, not as approval or mutation.

