# Agent Company Migration Decision Intake Contract

Generated UTC: 2026-06-16T11:48:35Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-intake-contract-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-intake-contract-validation-latest.json`

## Decision

`agent_company_migration_decision_intake_contract_ready_for_report_only_fixture_suite`

Recommended default: `build_report_only_fixture_suite_next_without_applying_operator_decision`

Prepared a report-only signed-decision intake contract for the migration operator review, including accepted decision types, required fields, fixtures, parser guards, and output states.

## Accepted Decision Types

- `hold`
- `approve_sandbox_dry_run_only`
- `request_rework`
- `reject_migration_path`

## Required Fields

- `decision_id`
- `operator_name`
- `decision_type`
- `scope`
- `artifact_paths`
- `expires_at`
- `risk_acknowledgement`
- `signed_utc`

## Parser Guards

- `parse_json_only_no_freeform_commands`
- `require_all_fields_present`
- `reject_unknown_decision_type`
- `reject_live_apply_scope`
- `reject_external_or_gated_action_requests`
- `require_artifact_paths_match_operator_review_packet`
- `require_expiration_and_signed_timestamp`
- `emit_report_only_routing_result`
- `never_apply_decision_inside_parser`

## Positive Fixtures

- `positive_hold` -> `accepted_for_report_only_routing`
- `positive_approve_sandbox_dry_run_only` -> `accepted_for_sandbox_dry_run_preparation_only`
- `positive_request_rework` -> `accepted_for_report_only_routing`
- `positive_reject_migration_path` -> `accepted_for_report_only_routing`

## Negative Fixtures

- `missing_decision_id`: decision_id is required
- `unknown_decision_type`: decision_type must be one of the review options
- `live_apply_scope`: live migration SQL apply is outside this contract
- `missing_artifact_paths`: artifact_paths must include review and validation artifacts
- `expired_decision`: expires_at must be in the future at parse time
- `unsigned_decision`: operator signature fields are required
- `gated_action_bundle`: browser/account/wallet/payment/public/security actions are forbidden
- `service_request_mutation`: service request mutation is forbidden by this intake

## Output States

- `accepted_hold`
- `accepted_sandbox_dry_run_preparation_only`
- `accepted_rework_request`
- `accepted_rejection_closeout`

## Boundary

This contract is report-only. It does not parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build the report-only fixture suite next; do not parse or apply live operator decisions yet.

