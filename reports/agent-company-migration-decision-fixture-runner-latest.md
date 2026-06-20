# Agent Company Migration Decision Fixture Runner

Generated UTC: 2026-06-16T12:00:38Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-fixture-runner-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-fixture-runner-validation-latest.json`

## Decision

`agent_company_migration_decision_fixture_runner_ready_for_report_only_parser_scaffold`

Evaluated the migration decision fixture suite with a deterministic report-only runner; all 12 synthetic fixtures matched expected accept/reject outcomes.

## Runner Results

- Fixtures evaluated: 12
- Accepted results: 4
- Rejected results: 8
- Passed fixtures: 12
- Failed fixtures: 0

| Fixture | Expected | Actual | Passed | Reasons |
| --- | --- | --- | --- | --- |
| `positive_hold` | `accept` | `accept` | `True` | none |
| `positive_approve_sandbox_dry_run_only` | `accept` | `accept` | `True` | none |
| `positive_request_rework` | `accept` | `accept` | `True` | none |
| `positive_reject_migration_path` | `accept` | `accept` | `True` | none |
| `missing_decision_id` | `reject` | `reject` | `True` | missing_required_fields |
| `unknown_decision_type` | `reject` | `reject` | `True` | unknown_decision_type |
| `live_apply_scope` | `reject` | `reject` | `True` | forbidden_scope |
| `missing_artifact_paths` | `reject` | `reject` | `True` | missing_artifact_paths |
| `expired_decision` | `reject` | `reject` | `True` | expired_or_missing_expiration |
| `unsigned_decision` | `reject` | `reject` | `True` | missing_required_fields, unsigned_decision |
| `gated_action_bundle` | `reject` | `reject` | `True` | forbidden_scope |
| `service_request_mutation` | `reject` | `reject` | `True` | forbidden_scope |

## Boundary

This runner evaluates saved synthetic fixtures only. It does not parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build the report-only parser scaffold next; do not parse live decisions or apply operator decisions.

