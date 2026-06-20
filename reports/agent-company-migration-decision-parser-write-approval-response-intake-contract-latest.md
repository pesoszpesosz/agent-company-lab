# Agent Company Migration Decision Parser Write Approval Response Intake Contract

Generated UTC: 2026-06-16T13:38:25Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-intake-contract-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-intake-contract-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_intake_contract_ready_for_report_only_fixture_suite`

Recommended default: `build_report_only_parser_write_approval_response_fixture_suite_next_without_applying_approval`

Defined the report-only signed parser-write approval response intake contract, including required fields, accepted responses, guards, and fixture expectations.

## Required Fields

- `decision_id`
- `operator_name`
- `response_type`
- `target_path`
- `source_artifact_path`
- `source_request_path`
- `approval_scope`
- `risk_acknowledgement`
- `expires_at`
- `signed_utc`

## Accepted Responses

- `hold`
- `approve_one_parser_file_write_only`
- `request_approval_request_rework`
- `reject_parser_write_request`

## Response Guards

- `guard_json_object_only`
- `guard_required_fields_present`
- `guard_known_response_type`
- `guard_target_path_matches_request`
- `guard_source_artifact_matches_request`
- `guard_source_request_matches_packet`
- `guard_approval_scope_one_file_only`
- `guard_not_expired`
- `guard_signed_timestamp_present`
- `guard_no_import_or_live_parse_permission`

## Boundary

This is a report-only approval response intake contract. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build a report-only parser-write approval response fixture suite next; do not apply approval or write the parser.

