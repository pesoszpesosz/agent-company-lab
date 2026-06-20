# Agent Company Migration Decision Parser Write Approval Response Application Packet Runner

Generated UTC: 2026-06-16T19:40:09Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-packet-runner-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-response-application-packet-runner-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_response_application_packet_runner_ready_for_report_only_review`

Evaluated the saved report-only approval response application packet fixtures without applying approval, writing parser files, importing a parser, parsing live decisions, or mutating service requests.

## Runner Results

- Fixtures evaluated: 10
- Accepted results: 1
- Rejected results: 9
- Passed fixtures: 10
- Failed fixtures: 0

| Fixture | Expected | Actual | Passed | Reasons |
| --- | --- | --- | --- | --- |
| `positive_valid_review_only_application_packet` | `packet_valid_for_separate_application_review` | `packet_valid_for_separate_application_review` | `True` | none |
| `missing_application_packet_id` | `guard_required_fields_present` | `reject` | `True` | guard_required_fields_present |
| `nonlocal_signed_response_artifact` | `guard_signed_response_artifact_local` | `reject` | `True` | guard_signed_response_artifact_local |
| `source_preflight_changed` | `guard_source_preflight_matches_contract` | `reject` | `True` | guard_source_preflight_matches_contract |
| `source_runner_review_changed` | `guard_source_runner_review_matches_contract` | `reject` | `True` | guard_source_runner_review_matches_contract |
| `target_path_changed` | `guard_target_path_matches_request` | `reject` | `True` | guard_target_path_matches_request |
| `source_artifact_changed` | `guard_source_artifact_matches_request` | `reject` | `True` | guard_source_artifact_matches_request |
| `application_scope_too_broad` | `guard_application_scope_review_only` | `reject` | `True` | guard_application_scope_review_only |
| `expired_packet` | `guard_not_expired` | `reject` | `True` | guard_not_expired |
| `bundled_import_sql_or_service_action` | `guard_no_import_live_parse_sql_service_or_external_action` | `reject` | `True` | guard_no_import_live_parse_sql_service_or_external_action |

## Boundary

This runner evaluates saved synthetic application packet fixture data only. It does not apply approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Review the report-only application packet runner results before any approval application or parser write request.

