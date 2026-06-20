# Agent Company Migration Decision Parser Write Approval Response Application Packet Contract

Generated UTC: 2026-06-16T19:31:50Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-packet-contract-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-packet-contract-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_application_packet_contract_ready_for_signed_packet_or_hold`

Recommended default: `wait_for_signed_approval_response_application_packet_without_applying`

Defined the report-only signed application packet contract for parser-write approval responses, keeping application blocked until a separate signed packet exists and validates.

## Application Fields

- `application_packet_id`
- `operator_name`
- `signed_response_artifact_path`
- `source_preflight_path`
- `source_runner_review_path`
- `target_path`
- `source_artifact_path`
- `application_scope`
- `expires_at`
- `signed_utc`

## Eligibility Rules

- source preflight validation is clean
- source preflight keeps application_allowed false until packet review
- signed response artifact path is present and local
- source preflight path matches this contract source
- target path matches parser write approval request
- application scope equals one_local_parser_file_write_application_review_only
- packet excludes parser import live parsing SQL service request and external actions
- packet expires after current validation timestamp and has signed_utc

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

- application packet is absent
- signed response artifact path is missing or non-local
- packet target or source artifact differs from the approval request
- packet scope is broader than one local parser file write application review
- packet bundles import live parsing SQL service-request or external action
- source preflight validation is stale or failing

## Boundary

This is a report-only application packet contract. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Wait for a signed approval-response application packet; do not write or import the parser from this contract.

