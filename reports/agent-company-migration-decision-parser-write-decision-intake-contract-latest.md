# Agent Company Migration Decision Parser Write Decision Intake Contract

Generated UTC: 2026-06-19T21:06:39Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-intake-contract-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-intake-contract-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_decision_intake_contract_ready_for_report_only_fixture_suite`

Recommended default: `build_report_only_parser_write_decision_fixture_suite_next_without_writing_parser`

Defined the report-only parser-write decision intake contract for a future signed one-file parser write approval, with hold as the default and no parser state changes.

## Required Fields

- `decision_id`
- `operator_name`
- `decision_type`
- `target_path`
- `source_artifact_path`
- `source_review_path`
- `expires_at`
- `risk_acknowledgement`
- `signed_utc`

## Accepted Parser Write Decisions

- `hold`
- `approve_one_parser_file_write_only`
- `request_runner_review_rework`
- `reject_parser_write`

## Parser Guards

- `guard_json_object_only`
- `guard_required_fields_present`
- `guard_known_parser_write_decision_type`
- `guard_target_path_matches_preflight`
- `guard_source_artifact_matches_preflight`
- `guard_source_review_matches_runner_review`
- `guard_not_expired`
- `guard_signed_timestamp_present`
- `guard_no_import_or_live_parse_permission`

## Negative Fixtures

- `missing_decision_id`
- `unknown_decision_type`
- `target_path_changed`
- `source_artifact_path_changed`
- `source_review_path_changed`
- `expired_decision`
- `unsigned_decision`
- `bundled_import_or_live_parse_permission`

## Boundary

This is a report-only parser-write decision intake contract. It does not apply an approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only parser-write decision fixture suite next; do not write or import the parser.

