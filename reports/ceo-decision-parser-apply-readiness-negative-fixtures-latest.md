# CEO Decision Parser Apply Readiness Negative Fixtures

Generated UTC: 2026-06-16T00:10:25Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-negative-fixtures-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-negative-fixtures-validation-latest.json`

## Decision

`ceo_decision_parser_apply_readiness_negative_fixtures_ready`

Created local negative fixtures for the apply-readiness gate, covering missing operator approvals, stale rollback snapshot, target status drift, planned field drift, unbounded update shape, and open side-effect boundary.

## Fixtures

| Fixture | Expected Rule |
| --- | --- |
| `missing-operator-approvals` | `reject_missing_operator_approval_bundle` |
| `stale-rollback-snapshot` | `reject_stale_rollback_snapshot` |
| `target-status-drift` | `reject_target_status_drift` |
| `planned-field-drift` | `reject_planned_field_drift` |
| `unbounded-update-shape` | `reject_unbounded_update_shape` |
| `side-effect-boundary-open` | `reject_side_effect_boundary_open` |

## Boundary

These are local negative fixtures only. They apply no mutation, update no service request, request no approval, start no worker, call no API, open no browser, and perform no account, wallet, payment, public, security-testing, external, or real-money action.

## Next Action

Use these fixtures before any apply-readiness runner or apply command; every drifted or underspecified readiness packet must be rejected before DB mutation is possible.

