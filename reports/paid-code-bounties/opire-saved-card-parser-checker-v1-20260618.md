# Opire Saved-Card Parser Checker

- Generated: `2026-06-18T08:49:08Z`
- Task: `task-opire-saved-card-parser-checker-v1-20260618`
- Status: `opire_saved_card_parser_checker_complete_local_only`
- Decision: `local_parser_only_no_claim_no_public_action`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\paid-code-bounties\opire-saved-card-parser-checker-v1-fixture-20260618.json`
- Results: `E:\agent-company-lab\reports\paid-code-bounties\opire-saved-card-parser-checker-v1-results-20260618.json`

## Summary

- `row_count`: `10`
- `candidate_count`: `0`
- `hard_reject_count`: `1`
- `parked_count`: `9`
- `rejected_or_deprioritized_count`: `0`

## Parsed Rows

| Row | Amount | Repo | Solvers | Score | Decision | Risk Flags |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `opire_fixture_row_01` | 5522 | `rodrigompy/bugb` | 0 | 45 | `park_until_issue_url` | `missing_public_issue_url` |
| `opire_fixture_row_02` | 2780 | `godotengine/godot` | 8 | 14 | `park_until_issue_url` | `crowded_solver_count`, `language_or_stack_mismatch`, `missing_public_issue_url` |
| `opire_fixture_row_03` | 1640 | `hexgrad/kokoro` | 6 | 15 | `park_until_issue_url` | `crowded_solver_count`, `funding_or_donation_shape_unclear`, `missing_public_issue_url` |
| `opire_fixture_row_04` | 900 | `FalkorDB/FalkorDB` | 14 | 0 | `park_until_issue_url` | `crowded_solver_count`, `language_or_stack_mismatch`, `missing_public_issue_url`, `security_or_crash_scope_requires_extra_review` |
| `opire_fixture_row_05` | 590 | `typeorm/typeorm` | 23 | 0 | `park_until_issue_url` | `crowded_solver_count`, `missing_public_issue_url` |
| `opire_fixture_row_06` | 390 | `autokey/autokey` | 12 | 0 | `park_until_issue_url` | `command_unavailable_or_unknown`, `crowded_solver_count`, `missing_public_issue_url` |
| `opire_fixture_row_07` | 345 | `zed-industries/zed` | 5 | 3 | `park_until_issue_url` | `crowded_solver_count`, `missing_public_issue_url` |
| `opire_fixture_row_08` | 220 | `qtop/qtop` | 4 | 3 | `park_until_issue_url` | `crowded_solver_count`, `missing_public_issue_url` |
| `opire_fixture_row_09` | 200 | `keycloak/keycloak` | 1 | 17 | `park_until_issue_url` | `language_or_stack_mismatch`, `missing_public_issue_url` |
| `opire_fixture_row_10` | 80 | `flowese/UdioWrapper` | 11 | 0 | `hard_reject` | `amount_below_first_pass_threshold`, `captcha_abuse_bypass_spam_or_policy_evasion`, `command_unavailable_or_unknown`, `crowded_solver_count`, `missing_public_issue_url` |

## Aggregate Gate Flags

- `duplicate_pr_scan_required`
- `local_build_test_feasibility_required`
- `maintainer_activity_check_required`
- `no_try_claim_without_public_action_approval`
- `public_issue_url_required`

## Boundary

- `fixture_rows_created`: `10`
- `parsed_rows_emitted`: `10`
- `candidate_rows`: `0`
- `hard_reject_rows`: `1`
- `browser_sessions_started`: `0`
- `opire_account_or_login`: `False`
- `try_claim_reward_commands`: `0`
- `github_comments_or_prs`: `0`
- `proposals_or_submissions`: `0`
- `payments`: `0`
- `public_actions`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Next Local Action

Promote only candidate_needs_readonly_refresh rows into exact read-only refresh packets. Do not run /try, /claim, GitHub comments, PRs, account login, Stripe, payout, workers, model/API calls, or public actions.
