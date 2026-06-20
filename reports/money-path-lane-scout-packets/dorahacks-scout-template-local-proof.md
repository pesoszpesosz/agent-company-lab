# DoraHacks Scout Template Local Proof

- Generated: `2026-06-18T07:44:12Z`
- Task: `task-lane-scout-dorahacks_hackathons_grants-20260618`
- Lane: `web3_airdrops_grants_hackathons`
- Status: `dorahacks_scout_template_ready_local_only`
- Decision: `scout_template_only_no_account_no_wallet_no_payment_no_submission_no_public_action_no_runtime`
- Validation: `True` with `0` failures

## Summary

DoraHacks is a broad Web3/frontier-tech opportunity surface, but the safe first step is a local scout template. This packet defines opportunity fields, route stages, scoring, and kill reasons for hackathons, grants, BUIDLs, and bounties without account login, wallet connection, submission, payment, public action, worker/runtime, or model/MCP calls.

## Route Disambiguation

DoraHacks mixes BUIDL profiles, hackathon participation, grant rounds, quadratic voting/funding, organizer tools, bug bounties, BUIDL AI, messaging, and chain-specific pages. This lane is a scout-template route only: it can classify opportunities and draft local project-fit notes, but account login, BUIDL creation, hackathon registration, grant application, wallet connection, vote/donation, prize/payment handling, public posts/messages, and worker/runtime use are all separate gates.

## Sources

- `https://dorahacks.io/` (official_home_page): DoraHacks positions itself as an open-source incentive and hackathon community platform. The page references hackathon organizer tooling, BUIDL AI, BUIDLs, grants, premium organizer tooling, and wallet/login surfaces.
- `https://dorahacks.io/hackathon` (official_hackathon_page): The hackathon page says participants can learn, team up, build, participate in hackathons, or create hackathons. It exposes filters for ongoing/upcoming/closed status, virtual/IRL location, region, and tags such as AI, Quantum, Crypto/PQC, Biohack, and Student. Creating or participating in a hackathon is not performed by this packet.
- `https://dorahacks.io/grant` (official_grant_page): The grant page presents quadratic funding and MACI/aMACI style grant rounds. It reports public aggregate stats on total rounds, votes, and funded amount, and exposes filters for ongoing/upcoming/closed rounds, ecosystem, and voting method. Voting, donating, grant participation, or wallet actions are blocked here.
- `https://dorahacks.io/buidl` (official_buidl_page): The BUIDL page describes DoraHacks as a home for BUIDLs and says users can create projects and accelerate ventures. It exposes technology/category/chain filters and public aggregate counts for BUIDLs, funded amount, and active builders. Creating a BUIDL, updating milestones, or joining a campaign is gated.
- `https://dorahacks.io/sitemap.xml` (official_sitemap): The sitemap was reachable and fresh with 2026-06-17 timestamps. It lists routes for BUIDL, grant, bounty, faucet, search, message, BUIDL AI, hackathon, bug bounty, legal terms, cookie policy, and chain-specific BUIDL pages. Use sitemap routes as a public discovery map, not as permission to interact.
- `https://dorahacks.io/legal/terms` (official_terms_page): Terms of Use were reachable and last updated 5 May 2026. Terms identify Hackerlink Limited and affiliated companies, create a legally binding agreement, and mention arbitration and dispute provisions. Account, organizer, submission, legal, payment, or prize participation requires human review.
- `https://dorahacks.io/legal/privacy` (official_privacy_page): Privacy Policy was reachable and last updated 26 November 2025. It covers personal data, usage data, cookies, transfers, rights, retention, and jurisdiction-specific notices. Any account, profile, KYC-like, contact, or project submission route must treat personal-data processing as gated.
- `https://dorahacks.io/bugbounty` (official_bug_bounty_page): Bug bounty page was reachable, but public text showed no ongoing bounties and seven outdated bounties at capture time. Bug bounty work should not be conflated with grants/hackathons and should remain monitor-only unless a live scoped program appears.
- `https://github.com/dorahacksglobal` (official_github_org): The public GitHub organization is reachable and can support read-only source discovery or duplicate checks. GitHub issues, PRs, comments, forks, and public actions remain gated.
- `E:\agent-company-lab\reports\money-path-lane-scout-packets\gitcoin-grant-fit-local-proof.md` (local_prior_grant_packet): The Gitcoin packet established grant-lane controls around fit, rules, identity, wallet, submission, public action, and payout gates. Reuse the same no-submit local-fit posture for DoraHacks.
- `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\web3-grants-hackathons-bounties-source-refresh-20260616.md` (local_prior_web3_source_refresh): Prior Web3 lane refresh already separated grant, hackathon, bounty, wallet, and submission surfaces. DoraHacks should enter the queue as a scout template before any project creation or submission.

## Opportunity Fields

- `opportunity_url`
- `observed_utc`
- `opportunity_type`
- `name`
- `status`
- `ecosystem_or_chain`
- `region_or_location`
- `virtual_or_irl`
- `tags`
- `submission_start`
- `submission_end`
- `voting_start`
- `voting_end`
- `funding_or_prize_pool`
- `currency_or_token`
- `voting_method`
- `eligibility_rules`
- `required_deliverables`
- `judging_criteria`
- `team_requirements`
- `project_fit`
- `repo_or_demo_requirement`
- `license_or_open_source_requirement`
- `wallet_requirement`
- `account_or_profile_requirement`
- `kyc_or_tax_or_payment_requirement`
- `public_promotion_requirement`
- `submission_route`
- `duplicate_or_prior_project_signal`
- `local_artifact_to_prepare`
- `score`
- `kill_reasons`
- `next_local_action`

## Route Stages

- `public_directory_scout`: Classify public hackathon, grant, BUIDL, and bounty directory rows from saved/public text. Gate `public_read_only`. Allowed now `True`.
- `local_project_fit_template`: Draft project fit, deliverables, repo/demo plan, team assumptions, and evidence locally. Gate `local_only`. Allowed now `True`.
- `rules_and_timeline_extraction`: Extract status, deadline, eligibility, prize/funding, voting method, and submission requirements without joining. Gate `public_read_only_no_interaction`. Allowed now `True`.
- `account_profile_wallet_gate`: Log in, create profile, connect wallet, create BUIDL, join team, register, or message. Gate `explicit_account_wallet_approval_required`. Allowed now `False`.
- `submission_gate`: Submit BUIDL, grant application, hackathon project, milestone, bounty report, demo, or judging material. Gate `explicit_submission_approval_required`. Allowed now `False`.
- `payment_vote_prize_gate`: Vote, donate, claim matching, accept prize, enter tax/payment flow, or sign a transaction. Gate `explicit_payment_wallet_legal_approval_required`. Allowed now `False`.
- `public_runtime_gate`: Post updates, message organizers, launch public demo, run hosted worker/bot, or use BUIDL AI/organizer tooling. Gate `explicit_public_action_or_runtime_approval_required`. Allowed now `False`.

## Scoring Rubric

- `status_and_deadline` (15 pts): opportunity is ongoing/upcoming with enough time for local deliverable prep
- `domain_fit` (15 pts): AI, infra, Web3, public-good, or developer-tooling theme matches local assets
- `prize_or_funding_clarity` (10 pts): funding/prize pool and currency/token route are explicit
- `deliverable_feasibility` (15 pts): repo/demo/writeup can be produced locally without account or wallet
- `rules_clarity` (10 pts): eligibility, judging, team, and open-source requirements are visible
- `wallet_payment_risk` (10 pts): no wallet/payment/prize gate is needed before local proof
- `duplicate_or_crowding_risk` (10 pts): prior BUIDLs do not already saturate the idea
- `promotion_burden` (5 pts): does not require immediate public campaign or donor coordination
- `reuse_value` (10 pts): local artifact can be reused for Gitcoin, EF ESP, or DoraHacks even if not submitted

## Hard Kill Reasons

- `closed_or_deadline_too_close`
- `no_clear_prize_grant_or_funding_route`
- `domain_theme_mismatch`
- `eligibility_or_judging_rules_unclear`
- `requires_account_profile_buidl_creation_or_team_join_before_review`
- `requires_wallet_connection_vote_donation_or_transaction`
- `requires_payment_tax_kyc_or_prize_acceptance_before_local_fit`
- `requires_public_post_message_demo_or_campaign_before_approval`
- `requires_worker_runtime_hosted_bot_or_buidl_ai_use_without_approval`
- `requires_nonlocal_assets_private_data_or_third_party_credentials`
- `duplicate_or_crowded_project_space`
- `local_repo_demo_or_writeup_cannot_be_prepared`
- `legal_terms_privacy_or_country_risk_unreviewed`

## Boundary

- `browser_sessions_started`: `0`
- `dorahacks_account_or_login`: `False`
- `wallet_connected_or_transaction_signed`: `False`
- `profiles_buidls_or_teams_created`: `0`
- `buidls_or_applications_submitted`: `0`
- `hackathons_joined_or_registrations`: `0`
- `votes_donations_prize_claims_or_payments`: `0`
- `messages_comments_or_public_posts`: `0`
- `buidl_ai_or_organizer_tools_used`: `0`
- `github_public_actions`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a DoraHacks public-directory fixture parser from manually saved hackathon/grant/BUIDL rows. Emit local scout rows with status, deadline, theme fit, funding/prize clarity, rules, deliverables, wallet/payment gates, duplicate risk, and next local artifact. Keep login, wallet, profile/BUIDL creation, team join, registration, submission, voting, donation, prize/payment/tax, public posts/messages, BUIDL AI, worker/runtime, and model/MCP calls blocked.
