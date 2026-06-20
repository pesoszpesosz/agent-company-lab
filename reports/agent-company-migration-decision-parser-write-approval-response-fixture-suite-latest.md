# Agent Company Migration Decision Parser Write Approval Response Fixture Suite

Generated UTC: 2026-06-19T23:31:07Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-fixture-suite-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-fixture-suite-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_fixture_suite_ready_for_report_only_runner`

Recommended default: `build_report_only_parser_write_approval_response_runner_next_without_applying_approval`

Materialized the report-only parser-write approval response fixture suite from the intake contract, covering accepted responses, rejection cases, and response guards.

## Fixture Counts

- Positive fixtures: 4
- Negative fixtures: 9
- Assertions: 13

## Fixtures

- `positive_hold` (positive): accepted_hold
- `positive_approve_one_parser_file_write_only` (positive): accepted_one_parser_file_write_only
- `positive_request_approval_request_rework` (positive): accepted_approval_request_rework
- `positive_reject_parser_write_request` (positive): accepted_parser_write_request_rejection
- `missing_decision_id` (negative): guard_required_fields_present
- `unknown_response_type` (negative): guard_known_response_type
- `target_path_changed` (negative): guard_target_path_matches_request
- `source_artifact_path_changed` (negative): guard_source_artifact_matches_request
- `source_request_path_changed` (negative): guard_source_request_matches_packet
- `approval_scope_too_broad` (negative): guard_approval_scope_one_file_only
- `expired_response` (negative): guard_not_expired
- `unsigned_response` (negative): guard_signed_timestamp_present
- `bundled_import_or_live_parse_permission` (negative): guard_no_import_or_live_parse_permission

## Boundary

This is a report-only approval response fixture suite. It does not execute fixtures, apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only parser-write approval response runner next; do not apply approval or write the parser.

