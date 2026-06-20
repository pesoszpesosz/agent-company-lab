# Agent Company Migration Decision Parser Write Decision Runner

Generated UTC: 2026-06-19T22:21:21Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-runner-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-runner-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_decision_runner_ready_for_report_only_parser_write_review`

Evaluated the saved report-only parser-write decision fixture data without writing parser files, importing a parser, parsing live decisions, or applying approval.

## Runner Results

- Fixtures evaluated: 12
- Accepted results: 4
- Rejected results: 8
- Passed fixtures: 12
- Failed fixtures: 0

| Fixture | Expected | Actual | Passed | Reasons |
| --- | --- | --- | --- | --- |
| `positive_hold` | `accepted_hold` | `accepted_hold` | `True` | none |
| `positive_approve_one_parser_file_write_only` | `accepted_one_parser_file_write_only` | `accepted_one_parser_file_write_only` | `True` | none |
| `positive_request_runner_review_rework` | `accepted_runner_review_rework` | `accepted_runner_review_rework` | `True` | none |
| `positive_reject_parser_write` | `accepted_parser_write_rejection` | `accepted_parser_write_rejection` | `True` | none |
| `missing_decision_id` | `guard_required_fields_present` | `reject` | `True` | guard_required_fields_present |
| `unknown_decision_type` | `guard_known_parser_write_decision_type` | `reject` | `True` | guard_known_parser_write_decision_type |
| `target_path_changed` | `guard_target_path_matches_preflight` | `reject` | `True` | guard_target_path_matches_preflight |
| `source_artifact_path_changed` | `guard_source_artifact_matches_preflight` | `reject` | `True` | guard_source_artifact_matches_preflight |
| `source_review_path_changed` | `guard_source_review_matches_runner_review` | `reject` | `True` | guard_source_review_matches_runner_review |
| `expired_decision` | `guard_not_expired` | `reject` | `True` | guard_not_expired |
| `unsigned_decision` | `guard_signed_timestamp_present` | `reject` | `True` | guard_required_fields_present, guard_signed_timestamp_present |
| `bundled_import_or_live_parse_permission` | `guard_no_import_or_live_parse_permission` | `reject` | `True` | guard_no_import_or_live_parse_permission |

## Boundary

This runner evaluates saved synthetic fixture data only. It does not write or import a parser module, parse live decisions, apply approval, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Review the report-only parser-write runner results before any parser file write or import request.

