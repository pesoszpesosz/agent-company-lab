# Agent Company Migration Decision Parser Write Decision Runner Review

Generated UTC: 2026-06-16T13:29:16Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-runner-review-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-decision-runner-review-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_decision_runner_review_ready_for_signed_parser_write_or_hold`

Recommended default: `hold_without_signed_one_file_parser_write_approval`

Reviewed the report-only parser-write runner results and prepared an operator-facing hold-or-one-file-write boundary without granting approval or changing parser state.

## Runner Result Checks

- `runner_validation_clean`
- `all_parser_write_fixture_results_passed`
- `positive_fixture_accept_count_is_4`
- `negative_fixture_reject_count_is_8`
- `no_parser_file_write_or_import`
- `no_service_request_or_external_side_effect`

## Approval Conditions

- signed operator parser-write decision id is present
- decision references this parser-write runner review artifact
- permission is limited to one local parser module file write
- target path matches the parser install preflight path
- post-write static review and fixture rerun remain required before import
- approval excludes live parsing, SQL, service-request mutation, and external actions

## Hold Conditions

- signed one-file parser-write approval is absent
- approval changes target path source artifact or runner review path
- approval bundles parser import or live decision parsing
- approval bundles SQL migration or service request mutation
- runner validation or fixture results are stale
- approval attempts browser account wallet payment public or security side effects

## Operator Instructions

- Default to hold unless a narrow one-file parser-write approval is explicitly signed.
- Do not approve parser import or live decision parsing from this review.
- If approving, reference the exact runner review artifact and target path.
- Limit approval to one local parser module file write attempt only.
- Require post-write static review and fixture rerun before any import request.
- Reject any bundled external, service-request, payment, wallet, account, public, or security action.

## Boundary

This is a report-only parser-write runner review packet. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Hold for a signed one-file parser-write approval, or continue with report-only review artifacts; do not write or import the parser without approval.

