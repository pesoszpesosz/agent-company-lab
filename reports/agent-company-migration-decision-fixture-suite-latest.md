# Agent Company Migration Decision Fixture Suite

Generated UTC: 2026-06-16T11:54:28Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-fixture-suite-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-fixture-suite-validation-latest.json`

## Decision

`agent_company_migration_decision_fixture_suite_ready_for_report_only_runner`

Prepared a report-only fixture suite for the migration decision intake contract, with positive and negative submitted-intake cases and expected parser outcomes.

## Fixture Counts

- Positive fixtures: 4
- Negative fixtures: 8
- Expected accepts: 4
- Expected rejects: 8

## Fixtures

| Fixture | Expected | State/Reason |
| --- | --- | --- |
| `positive_hold` | `accept` | accepted_for_report_only_routing |
| `positive_approve_sandbox_dry_run_only` | `accept` | accepted_for_sandbox_dry_run_preparation_only |
| `positive_request_rework` | `accept` | accepted_for_report_only_routing |
| `positive_reject_migration_path` | `accept` | accepted_for_report_only_routing |
| `missing_decision_id` | `reject` | decision_id is required |
| `unknown_decision_type` | `reject` | decision_type must be one of the review options |
| `live_apply_scope` | `reject` | live migration SQL apply is outside this contract |
| `missing_artifact_paths` | `reject` | artifact_paths must include review and validation artifacts |
| `expired_decision` | `reject` | expires_at must be in the future at parse time |
| `unsigned_decision` | `reject` | operator signature fields are required |
| `gated_action_bundle` | `reject` | browser/account/wallet/payment/public/security actions are forbidden |
| `service_request_mutation` | `reject` | service request mutation is forbidden by this intake |

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

## Boundary

This suite is report-only. It does not execute fixtures, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Build the report-only fixture runner next; do not parse live decisions or apply operator decisions.

