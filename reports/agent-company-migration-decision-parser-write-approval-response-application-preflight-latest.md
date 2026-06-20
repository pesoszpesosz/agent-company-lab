# Agent Company Migration Decision Parser Write Approval Response Application Preflight

Generated UTC: 2026-06-16T19:27:56Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-preflight-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-preflight-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_application_preflight_blocked_without_signed_response`

Recommended default: `keep_hold_until_signed_approval_response_application_packet_exists`

Prepared a report-only application preflight for parser-write approval responses and kept application blocked because no signed response artifact is present.

## Prerequisite Checks

- `source_runner_review_validation_clean`
- `source_runner_review_default_is_hold`
- `runner_review_confirms_all_13_fixtures_passed`
- `approval_response_intake_contract_exists`
- `approval_request_packet_exists`
- `no_signed_response_artifact_supplied`
- `no_parser_write_or_import_allowed_from_preflight`

## Required Signed Response Fields

- `decision_id`
- `operator_name`
- `response_type`
- `target_path`
- `source_artifact_path`
- `source_request_path`
- `approval_scope`
- `signed_utc`

## Blocked Actions

- apply approval response
- write parser module file
- import parser module
- parse live decisions
- execute migration SQL
- enable apply command
- create database tables
- start workers
- assign or update service requests
- open browser or use accounts
- touch wallets payments or real money
- post publicly or run security testing

## Hold Conditions

- signed response artifact is absent
- response artifact fails intake contract validation
- response path or source artifact differs from approval request
- response bundles import live parsing SQL service-request or external action
- runner review or fixture evidence is stale
- operator approval scope is broader than one local parser file write

## Boundary

This is a report-only application preflight. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Keep hold until a signed approval response application packet exists and validates; do not write or import the parser from this preflight.

