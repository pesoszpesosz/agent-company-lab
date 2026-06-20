# CEO Decision Parser Apply Readiness Signed Decision Negative Fixtures

Generated UTC: 2026-06-16T09:42:36Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-negative-fixtures-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-negative-fixtures-validation-latest.json`

## Decision

`ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures_ready`

Created six local negative signed-decision fixtures for the apply-readiness approval gate. Each fixture changes one required decision field and should be rejected by the future signed-decision guard.

## Fixtures

| Fixture | Expected Rule |
| --- | --- |
| `missing-operator-signature` | `reject_missing_operator_signature` |
| `wrong-target-request-id` | `reject_target_request_id_mismatch` |
| `edited-approval-scope-text` | `reject_approval_scope_text_mismatch` |
| `stale-rollback-snapshot` | `reject_rollback_snapshot_mismatch` |
| `missing-scope-expiration` | `reject_missing_scope_expiration` |
| `side-effect-confirmation-drift` | `reject_side_effect_confirmation_drift` |

## Boundary

These fixtures are local test data only. They grant no approval, enable no apply command, update no service request, emit no approval request, start no worker, call no API, open no browser, and perform no account, wallet, payment, public, security-testing, external, or real-money action.

## Next Action

Run a report-only signed-decision guard against these fixtures before adding any mutating apply command.

