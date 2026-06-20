# Agent Company Migration Decision Parser Install Decision Intake Contract

Generated UTC: 2026-06-16T12:48:34Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-intake-contract-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-intake-contract-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_install_decision_intake_contract_ready_for_report_only_fixture_suite`

Recommended default: `build_report_only_install_decision_fixture_suite_next_without_applying_install_decision`

Defined the report-only signed install-decision intake contract for the parser install review, including required fields, fixtures, parser guards, and output states.

## Required Fields

- `decision_id`
- `operator_name`
- `decision_type`
- `target_path`
- `source_artifact_path`
- `expires_at`
- `risk_acknowledgement`
- `signed_utc`

## Accepted Install Decisions

- `hold`
- `approve_one_file_write_only`
- `request_preflight_rework`
- `reject_parser_install`

## Positive Fixtures

- `positive_hold` -> `accepted_hold`
- `positive_approve_one_file_write_only` -> `accepted_one_file_write_only`
- `positive_request_preflight_rework` -> `accepted_preflight_rework`
- `positive_reject_parser_install` -> `accepted_install_rejection`

## Negative Fixtures

- `missing_decision_id`
- `unknown_decision_type`
- `target_path_changed`
- `missing_source_artifact`
- `expired_decision`
- `unsigned_decision`
- `bundled_live_parse_permission`

## Parser Guards

- `guard_json_object_only`
- `guard_required_fields_present`
- `guard_known_install_decision_type`
- `guard_target_path_matches_preflight`
- `guard_source_artifact_matches_preflight`
- `guard_not_expired`
- `guard_signed_timestamp_present`
- `guard_no_import_or_live_parse_permission`

## Boundary

This is a report-only intake contract. It does not apply an install decision, write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only install-decision fixture suite next; do not apply an install decision or write/import a parser module.

