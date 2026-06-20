# Agent Company Migration Decision Parser Install Decision Runner Review

Generated UTC: 2026-06-16T13:06:38Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-runner-review-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-decision-runner-review-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_install_decision_runner_review_ready_for_operator_parser_write_decision_or_hold`

Recommended default: `hold_without_signed_operator_parser_write_approval`

Reviewed the report-only install-decision runner results and prepared an operator-facing hold-or-parser-write boundary without granting approval or changing parser state.

## Runner Result Checks

- `runner_validation_clean`
- `all_fixture_results_passed`
- `positive_fixture_accept_count_is_4`
- `negative_fixture_reject_count_is_7`
- `no_parser_file_write_or_import`
- `no_service_request_or_external_side_effect`

## Approval Conditions

- signed operator decision id is present
- decision references this runner review artifact
- permission is limited to one parser module file write
- target path matches the parser install preflight path
- post-write static review remains required before import
- approval excludes live decision parsing and service-request mutation

## Hold Conditions

- signed operator approval is absent
- approval changes target path or source artifact
- approval bundles parser import or live parsing
- approval bundles SQL migration or service request mutation
- runner validation or fixture results are stale
- approval attempts browser account wallet payment public or security side effects

## Operator Instructions

- Default to hold unless a narrow parser-write approval is explicitly signed.
- Do not approve parser import or live decision parsing from this review.
- If approving, reference the exact runner review artifact and target path.
- Limit approval to one local parser module file write only.
- Require post-write static review and fixture rerun before any import request.
- Reject any bundled external, service-request, payment, wallet, account, public, or security action.

## Boundary

This is a report-only runner review packet. It does not apply an install decision, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Hold for a signed one-file parser-write approval, or continue with report-only review artifacts; do not write or import the parser without approval.

