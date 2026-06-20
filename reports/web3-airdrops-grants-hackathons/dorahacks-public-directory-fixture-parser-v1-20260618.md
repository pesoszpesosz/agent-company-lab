# DoraHacks Public-Directory Fixture Parser

- Generated: `2026-06-18T09:31:31Z`
- Task: `task-dorahacks-public-directory-fixture-parser-v1-20260618`
- Status: `dorahacks_public_directory_fixture_parser_ready_local_only`
- Decision: `saved_public_rows_scored_local_scout_only_no_account_no_wallet_no_submit_no_public_action`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\dorahacks-public-directory-fixture-parser-v1-fixture-20260618.json`
- Results: `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\dorahacks-public-directory-fixture-parser-v1-results-20260618.json`

## Summary

- `row_count`: `4`
- `candidate_count`: `1`
- `kill_or_wait_count`: `3`
- `submission_ready_count`: `0`
- `source_acceptance_checks`: `7`

## Parsed Opportunity Rows

| Opportunity | Type | Status | Class | Score | Submission Ready | Kill Reasons |
| --- | --- | --- | --- | ---: | --- | --- |
| `Example AI Agent Public Goods Hackathon saved row` | `hackathon` | `ongoing` | `local_scout_candidate` | 90 | `False` | `duplicate_or_crowded_project_space` |
| `Example quadratic funding grant round saved row` | `grant` | `ongoing` | `kill_or_wait` | 85 | `False` | `requires_public_post_message_demo_or_campaign_before_approval`, `requires_wallet_connection_vote_donation_or_transaction` |
| `Example BUIDL showcase page saved row` | `buidl` | `open_ended` | `kill_or_wait` | 30 | `False` | `duplicate_or_crowded_project_space`, `eligibility_or_judging_rules_unclear`, `local_repo_demo_or_writeup_cannot_be_prepared`, `no_clear_prize_grant_or_funding_route`, `requires_account_profile_buidl_creation_or_team_join_before_review`, `requires_public_post_message_demo_or_campaign_before_approval` |
| `Example closed bounty saved row` | `bug_bounty` | `closed` | `kill_or_wait` | 25 | `False` | `closed_or_deadline_too_close`, `domain_theme_mismatch`, `local_repo_demo_or_writeup_cannot_be_prepared`, `no_clear_prize_grant_or_funding_route` |

## Required Gates Before Any DoraHacks Action

- `dorahacks_account_profile_login_approval`
- `terms_privacy_legal_review`
- `specific_hackathon_grant_or_bounty_rules_review`
- `team_join_registration_or_participation_approval`
- `buidl_profile_creation_or_project_submission_approval`
- `wallet_vote_donation_transaction_approval`
- `prize_payment_tax_or_kyc_review`
- `public_post_message_demo_or_campaign_approval`
- `buidl_ai_organizer_tool_or_runtime_approval`
- `github_issue_pr_comment_or_public_repo_action_approval`

## Boundary

- `saved_opportunity_rows_created`: `4`
- `scored_rows`: `4`
- `local_scout_candidates`: `1`
- `submission_ready_count`: `0`
- `browser_sessions_started`: `0`
- `dorahacks_account_or_login`: `False`
- `wallet_connected_or_transaction_signed`: `False`
- `profiles_buidls_or_teams_created`: `0`
- `hackathons_joined_or_registrations`: `0`
- `buidls_or_applications_submitted`: `0`
- `votes_donations_prize_claims_or_payments`: `0`
- `messages_comments_or_public_posts`: `0`
- `buidl_ai_or_organizer_tools_used`: `0`
- `github_public_actions`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Next Local Action

For local_scout_candidate rows, prepare only sanitized local project-fit writeups, repo/demo outlines, rules checklists, and approval packets. Do not log in, connect wallets, create profiles/BUIDLs/teams, join or register, submit, vote, donate, claim prizes, configure payment/tax, message or post publicly, use BUIDL AI, start workers/runtimes, or call model/MCP/external APIs from this packet alone.
