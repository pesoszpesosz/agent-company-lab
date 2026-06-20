# CEO Decision Parser Apply Readiness Signed Decision Guard Runner

Generated UTC: 2026-06-19T21:03:22Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-guard-runner-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-guard-runner-validation-latest.json`

## Decision

`ceo_decision_parser_apply_readiness_signed_decision_guard_runner_passed_no_mutations`

Ran a local report-only signed-decision guard against six negative fixtures. The guard rejected every malformed signed decision with the expected rule and performed no mutation.

## Guard Results

| Fixture | Expected Rule | Actual Rule | Match |
| --- | --- | --- | ---: |
| `missing-operator-signature` | `reject_missing_operator_signature` | `reject_missing_operator_signature` | `True` |
| `wrong-target-request-id` | `reject_target_request_id_mismatch` | `reject_target_request_id_mismatch` | `True` |
| `edited-approval-scope-text` | `reject_approval_scope_text_mismatch` | `reject_approval_scope_text_mismatch` | `True` |
| `stale-rollback-snapshot` | `reject_rollback_snapshot_mismatch` | `reject_rollback_snapshot_mismatch` | `True` |
| `missing-scope-expiration` | `reject_missing_scope_expiration` | `reject_missing_scope_expiration` | `True` |
| `side-effect-confirmation-drift` | `reject_side_effect_confirmation_drift` | `reject_side_effect_confirmation_drift` | `True` |

## Boundary

This runner is report-only. It evaluates local signed-decision fixtures and writes local artifacts only; it does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.

## Next Action

Create a positive signed-decision fixture next; keep apply disabled until that fixture passes and the user explicitly approves a real apply command.

