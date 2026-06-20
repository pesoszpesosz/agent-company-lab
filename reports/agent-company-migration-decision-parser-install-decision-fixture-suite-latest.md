# Agent Company Migration Decision Parser Install Decision Fixture Suite

Generated UTC: 2026-06-16T12:54:23Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-fixture-suite-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-fixture-suite-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_install_decision_fixture_suite_ready_for_report_only_runner`

Recommended default: `build_report_only_install_decision_runner_next_without_applying_install_decision`

Materialized the report-only install-decision fixture suite from the intake contract, covering accepted decisions, rejection cases, and parser guard assertions.

## Fixture Counts

- Positive fixtures: 4
- Negative fixtures: 7
- Assertions: 11

## Fixtures

- `positive_hold` (positive): accepted_hold
- `positive_approve_one_file_write_only` (positive): accepted_one_file_write_only
- `positive_request_preflight_rework` (positive): accepted_preflight_rework
- `positive_reject_parser_install` (positive): accepted_install_rejection
- `missing_decision_id` (negative): guard_required_fields_present
- `unknown_decision_type` (negative): guard_known_install_decision_type
- `target_path_changed` (negative): guard_target_path_matches_preflight
- `missing_source_artifact` (negative): guard_source_artifact_matches_preflight
- `expired_decision` (negative): guard_not_expired
- `unsigned_decision` (negative): guard_signed_timestamp_present
- `bundled_live_parse_permission` (negative): guard_no_import_or_live_parse_permission

## Boundary

This is a report-only fixture suite. It does not execute fixtures, apply an install decision, write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only install-decision runner next; do not execute fixtures through an importable parser or apply an install decision.

