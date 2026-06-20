# Agent Company Migration Decision Module Fixture Checks

Generated UTC: 2026-06-16T12:18:39Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-module-fixture-checks-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-module-fixture-checks-validation-latest.json`

## Decision

`agent_company_migration_decision_module_fixture_checks_ready_for_report_only_parser_module_file_draft`

Checked the report-only parser module draft against all 12 migration decision fixtures; every fixture has coverage, parser entry, scope guard, and result builder support.

## Check Results

- Check cases: 12
- Passed: 12
- Failed: 0

| Fixture | Expected | Covered | Entry | Scope Guard | Result Builder | Passed |
| --- | --- | --- | --- | --- | --- | --- |
| `positive_hold` | `accept` | `True` | `True` | `True` | `True` | `True` |
| `positive_approve_sandbox_dry_run_only` | `accept` | `True` | `True` | `True` | `True` | `True` |
| `positive_request_rework` | `accept` | `True` | `True` | `True` | `True` | `True` |
| `positive_reject_migration_path` | `accept` | `True` | `True` | `True` | `True` | `True` |
| `missing_decision_id` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `unknown_decision_type` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `live_apply_scope` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `missing_artifact_paths` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `expired_decision` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `unsigned_decision` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `gated_action_bundle` | `reject` | `True` | `True` | `True` | `True` | `True` |
| `service_request_mutation` | `reject` | `True` | `True` | `True` | `True` | `True` |

## Boundary

These are report-only module fixture checks. They do not write an importable parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Draft the report-only parser module file next; do not install it or parse live decisions.

