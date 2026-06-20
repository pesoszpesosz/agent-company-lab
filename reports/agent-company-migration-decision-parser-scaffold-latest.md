# Agent Company Migration Decision Parser Scaffold

Generated UTC: 2026-06-19T22:14:53Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-scaffold-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-scaffold-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_scaffold_ready_for_report_only_parser_module`

Prepared a report-only parser scaffold for migration operator decisions, grounded in the passing fixture runner and explicit guard/result schemas.

## Parser Stages

1. `load_json_object`
2. `require_exact_field_set`
3. `validate_decision_type`
4. `validate_scope_boundaries`
5. `validate_artifact_paths`
6. `validate_expiration_and_signature`
7. `emit_report_only_result`

## Guard Functions

- `guard_json_object_only`
- `guard_required_fields_present`
- `guard_known_decision_type`
- `guard_no_live_apply_scope`
- `guard_no_external_or_gated_action_scope`
- `guard_artifact_paths_match_review_packet`
- `guard_not_expired`
- `guard_signed_timestamp_present`
- `guard_result_is_report_only`

## Result Fields

- `accepted`
- `decision_type`
- `result_state`
- `refusal_reasons`
- `artifact_paths`
- `expires_at`
- `signed_utc`
- `report_only`

## Refusal Reasons

- `missing_required_fields`
- `unknown_decision_type`
- `forbidden_scope`
- `missing_artifact_paths`
- `expired_or_missing_expiration`
- `unsigned_decision`
- `artifact_path_mismatch`
- `not_json_object`

## Boundary

This scaffold is report-only. It does not write a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Draft the report-only parser module next; do not parse live decisions or apply operator decisions.

