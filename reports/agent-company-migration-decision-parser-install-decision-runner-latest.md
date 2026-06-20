# Agent Company Migration Decision Parser Install Decision Runner

Generated UTC: 2026-06-16T12:58:55Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-runner-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-runner-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_install_decision_runner_ready_for_report_only_parser_static_review`

Evaluated the saved report-only install-decision fixture data without importing a parser, writing parser files, parsing live decisions, or applying an install decision.

## Runner Results

- Fixtures evaluated: 11
- Accepted results: 4
- Rejected results: 7
- Passed fixtures: 11
- Failed fixtures: 0

| Fixture | Expected | Actual | Passed | Reasons |
| --- | --- | --- | --- | --- |
| `positive_hold` | `accepted_hold` | `accepted_hold` | `True` | none |
| `positive_approve_one_file_write_only` | `accepted_one_file_write_only` | `accepted_one_file_write_only` | `True` | none |
| `positive_request_preflight_rework` | `accepted_preflight_rework` | `accepted_preflight_rework` | `True` | none |
| `positive_reject_parser_install` | `accepted_install_rejection` | `accepted_install_rejection` | `True` | none |
| `missing_decision_id` | `guard_required_fields_present` | `reject` | `True` | guard_required_fields_present |
| `unknown_decision_type` | `guard_known_install_decision_type` | `reject` | `True` | guard_known_install_decision_type |
| `target_path_changed` | `guard_target_path_matches_preflight` | `reject` | `True` | guard_target_path_matches_preflight |
| `missing_source_artifact` | `guard_source_artifact_matches_preflight` | `reject` | `True` | guard_required_fields_present, guard_source_artifact_matches_preflight |
| `expired_decision` | `guard_not_expired` | `reject` | `True` | guard_not_expired |
| `unsigned_decision` | `guard_signed_timestamp_present` | `reject` | `True` | guard_required_fields_present, guard_signed_timestamp_present |
| `bundled_live_parse_permission` | `guard_no_import_or_live_parse_permission` | `reject` | `True` | guard_no_import_or_live_parse_permission |

## Boundary

This runner evaluates saved synthetic fixture data only. It does not import a parser, write a parser module, parse live decisions, apply an install decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Review the report-only runner results before any parser file write or import request.

