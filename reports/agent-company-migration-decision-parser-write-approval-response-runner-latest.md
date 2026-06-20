# Agent Company Migration Decision Parser Write Approval Response Runner

Generated UTC: 2026-06-16T13:50:30Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-runner-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-runner-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_runner_ready_for_report_only_review`

Evaluated the saved report-only parser-write approval response fixture data without applying approval, writing parser files, importing a parser, parsing live decisions, or mutating service requests.

## Runner Results

- Fixtures evaluated: 13
- Accepted results: 4
- Rejected results: 9
- Passed fixtures: 13
- Failed fixtures: 0

| Fixture | Expected | Actual | Passed | Reasons |
| --- | --- | --- | --- | --- |
| `positive_hold` | `accepted_hold` | `accepted_hold` | `True` | none |
| `positive_approve_one_parser_file_write_only` | `accepted_one_parser_file_write_only` | `accepted_one_parser_file_write_only` | `True` | none |
| `positive_request_approval_request_rework` | `accepted_approval_request_rework` | `accepted_approval_request_rework` | `True` | none |
| `positive_reject_parser_write_request` | `accepted_parser_write_request_rejection` | `accepted_parser_write_request_rejection` | `True` | none |
| `missing_decision_id` | `guard_required_fields_present` | `reject` | `True` | guard_required_fields_present |
| `unknown_response_type` | `guard_known_response_type` | `reject` | `True` | guard_known_response_type |
| `target_path_changed` | `guard_target_path_matches_request` | `reject` | `True` | guard_target_path_matches_request |
| `source_artifact_path_changed` | `guard_source_artifact_matches_request` | `reject` | `True` | guard_source_artifact_matches_request |
| `source_request_path_changed` | `guard_source_request_matches_packet` | `reject` | `True` | guard_source_request_matches_packet |
| `approval_scope_too_broad` | `guard_approval_scope_one_file_only` | `reject` | `True` | guard_approval_scope_one_file_only |
| `expired_response` | `guard_not_expired` | `reject` | `True` | guard_not_expired |
| `unsigned_response` | `guard_signed_timestamp_present` | `reject` | `True` | guard_required_fields_present, guard_signed_timestamp_present |
| `bundled_import_or_live_parse_permission` | `guard_no_import_or_live_parse_permission` | `reject` | `True` | guard_no_import_or_live_parse_permission |

## Boundary

This runner evaluates saved synthetic approval response fixture data only. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Review the report-only parser-write approval response runner results before any parser write approval application request.

