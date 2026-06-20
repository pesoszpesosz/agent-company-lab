# Agent Company Migration Decision Parser Write Approval Response Application Packet Fixture Suite

Generated UTC: 2026-06-19T22:32:43Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite_ready_for_report_only_runner`

Recommended default: `build_report_only_approval_response_application_packet_runner_next_without_applying`

Materialized report-only approval response application packet fixtures from the contract, including one valid review-only packet and nine guard rejection cases.

## Fixture Counts

- Positive fixtures: 1
- Negative fixtures: 9
- Assertions: 10

## Fixtures

- `positive_valid_review_only_application_packet` (positive): `packet_valid_for_separate_application_review`
- `missing_application_packet_id` (negative): `guard_required_fields_present`
- `nonlocal_signed_response_artifact` (negative): `guard_signed_response_artifact_local`
- `source_preflight_changed` (negative): `guard_source_preflight_matches_contract`
- `source_runner_review_changed` (negative): `guard_source_runner_review_matches_contract`
- `target_path_changed` (negative): `guard_target_path_matches_request`
- `source_artifact_changed` (negative): `guard_source_artifact_matches_request`
- `application_scope_too_broad` (negative): `guard_application_scope_review_only`
- `expired_packet` (negative): `guard_not_expired`
- `bundled_import_sql_or_service_action` (negative): `guard_no_import_live_parse_sql_service_or_external_action`

## Boundary

This is a report-only fixture suite. It does not execute fixtures, apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only application packet runner next; do not apply approval or write/import the parser.

