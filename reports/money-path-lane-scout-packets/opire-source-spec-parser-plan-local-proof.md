# Opire Source-Spec Parser Plan Local Proof

- Generated: `2026-06-18T06:54:05Z`
- Task: `task-lane-scout-opire_paid_oss-20260618`
- Lane: `paid_code_bounties`
- Status: `opire_source_spec_parser_plan_ready_local_only`
- Decision: `local_parser_plan_only_no_claim_no_account_no_public_action`
- Validation: `True` with `0` failures

## Summary

Opire is viable as a public paid-OSS discovery source, but the first profitable step is a saved-fixture parser and scorer. Claiming, trying, commenting, PRs, account login, Stripe, and payout work remain gated.

## Source Observations

- `https://opire.dev/home` (official_home): Opire positions itself as a bounty platform for open-source issues. Featured bounties are public and include amount, title, language, and app links. Pricing copy says the bounty creator pays Opire and Stripe fees, while developers receive the bounty amount.
- `https://app.opire.dev/home` (public_app_listing): Public listing exposes aggregate paid/available/open-value metrics. Cards expose owner, repo, date, title, language tags, command availability, amount, and solver count. Sorting by price makes it suitable for a saved-fixture parser before any login or claim action.
- `https://docs.opire.dev/overview/introduction` (official_docs): Opire consists of a GitHub bot and a web platform. The web platform supports search by technology and price, payment history, solved history, and profile configuration.
- `https://docs.opire.dev/overview/commands` (official_docs): Bot commands include /reward, /try, /claim, and /tip. /try and /claim are public GitHub interactions and must stay behind public-action approval.
- `https://docs.opire.dev/rewards/lifecycle` (official_docs): Reward flow begins on an issue and later requires a PR to claim. The creator reviews the PR and chooses whom to pay if multiple developers claimed. Payout capability is checked before Stripe payment.
- `https://docs.opire.dev/rewards/pricing` (official_docs): Prices are in USD. Minimum reward is $20. Opire uses Stripe and adds Stripe plus Opire fees to the creator's cost.
- `E:\profit-edge-lab\reports\opire-bounty-scan-latest.md` (local_prior_scan): Use local profit-edge scan data as a negative/parked history input when present. Do not assume any prior row is still available without a fresh read-only refresh.

## Parser Fields

- `source_url`
- `observed_utc`
- `bounty_url`
- `amount_usd`
- `owner`
- `repo`
- `issue_title`
- `language_tags`
- `posted_or_issue_date`
- `command_available`
- `solver_count`
- `claimed_or_trying_status`
- `public_issue_url_if_available`
- `risk_flags`
- `gate_flags`
- `next_local_action`

## Sample Fixture Rows

| Owner | Repo | Amount | Solvers | Action | Route |
|---|---|---:|---:|---|---|
| rodrigompy | bugb | $5522 | 0 | inspect_public_repo_and_issue_if_url_available | high_amount_low_solver_but_requires_issue_url_and_scope_check |
| godotengine | godot | $2780 | 8 | reject_or_deprioritize | many_solvers_and_large_complex_project |
| hexgrad | kokoro | $1640 | 6 | deprioritize_until_scope_clear | funding_or_donation_shape_unclear_deliverable |
| FalkorDB | FalkorDB | $900 | 14 | reject_or_deprioritize | security_or_crash_scope_and_many_solvers |
| typeorm | typeorm | $590 | 23 | reject_or_deprioritize | high_competition_and_old_issue |
| autokey | autokey | $390 | 12 | reject_or_deprioritize | large_platform_feature_many_solvers |
| zed-industries | zed | $345 | 5 | deprioritize_until_duplicate_pr_scan | nonzero_solver_count_and_large_codebase |
| qtop | qtop | $220 | 4 | inspect_as_possible_local_proof_fixture | language_fit_but_solver_count_requires_duplicate_check |
| keycloak | keycloak | $200 | 1 | inspect_only_if_language_fit_worker_available | low_solver_count_but_language_mismatch |
| flowese | UdioWrapper | $80 | 11 | hard_reject | captcha_or_abuse_bypass_risk |

## Rejection Rules

- `reject_if_login_required_to_inspect_basic_issue`
- `reject_if_claim_requires_public_comment_before_duplicate_and_scope_checks`
- `reject_if_no_public_issue_url`
- `reject_if_solver_count_greater_than_two_for_first_pass`
- `reject_if_repo_not_publicly_inspectable`
- `reject_if_language_or_stack_mismatch`
- `reject_if_bounty_under_threshold_after_expected_hours`
- `reject_if_captcha_abuse_bypass_spam_or_policy_evasion`
- `reject_if_acceptance_criteria_unclear`
- `reject_if_issue_old_stale_or_crowded_without_recent_maintainer_signal`
- `reject_if_payment_or_stripe_gate_needed_before_local_proof`

## Acceptance Checks

- Saved public listing fixture has at least owner, repo, title, amount, solver count, and language fields.
- Parser emits hard gate flags separately from scoring notes.
- Candidate promotion requires public issue URL, duplicate PR scan, maintainer activity check, and local build/test feasibility.
- No /try, /claim, GitHub comment, PR, account, Stripe, or dashboard action is allowed in parser mode.
- Every candidate gets a next local action or a kill reason.
- Captcha/abuse-bypass rows are hard rejected even if the amount is nonzero.

## Boundary

- `browser_sessions_started`: `0`
- `opire_account_or_login`: `False`
- `github_comments_or_prs`: `0`
- `try_claim_reward_commands`: `0`
- `proposals_or_submissions`: `0`
- `payments`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a deterministic parser against saved/public Opire card snapshots extracting amount, owner, repo, title, language, command availability, solver count, URL/date fields, risk flags, and next local action; prove zero public actions and hard-reject captcha/abuse rows.
