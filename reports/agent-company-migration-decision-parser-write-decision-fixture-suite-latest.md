# Agent Company Migration Decision Parser Write Decision Fixture Suite

Generated UTC: 2026-06-19T23:22:29Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-fixture-suite-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-fixture-suite-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_decision_fixture_suite_ready_for_report_only_runner`

Recommended default: `build_report_only_parser_write_decision_runner_next_without_writing_parser`

Materialized the report-only parser-write decision fixture suite from the intake contract, covering accepted write decisions, rejection cases, and parser-write guards.

## Fixture Counts

- Positive fixtures: 4
- Negative fixtures: 8
- Assertions: 12

## Fixtures

- `positive_hold` (positive): accepted_hold
- `positive_approve_one_parser_file_write_only` (positive): accepted_one_parser_file_write_only
- `positive_request_runner_review_rework` (positive): accepted_runner_review_rework
- `positive_reject_parser_write` (positive): accepted_parser_write_rejection
- `missing_decision_id` (negative): guard_required_fields_present
- `unknown_decision_type` (negative): guard_known_parser_write_decision_type
- `target_path_changed` (negative): guard_target_path_matches_preflight
- `source_artifact_path_changed` (negative): guard_source_artifact_matches_preflight
- `source_review_path_changed` (negative): guard_source_review_matches_runner_review
- `expired_decision` (negative): guard_not_expired
- `unsigned_decision` (negative): guard_signed_timestamp_present
- `bundled_import_or_live_parse_permission` (negative): guard_no_import_or_live_parse_permission

## Boundary

This is a report-only parser-write decision fixture suite. It does not execute fixtures, apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only parser-write decision runner next; do not execute a parser write or import the parser.

