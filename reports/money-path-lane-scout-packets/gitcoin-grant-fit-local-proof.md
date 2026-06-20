# Gitcoin Grant Fit Local Proof

- Generated: `2026-06-18T07:37:06Z`
- Task: `task-lane-scout-gitcoin_grants-20260618`
- Lane: `web3_airdrops_grants_hackathons`
- Status: `gitcoin_grant_fit_ready_local_only`
- Decision: `grant_fit_only_no_account_no_wallet_no_payment_no_submission_no_public_action`
- Validation: `True` with `0` failures

## Summary

Gitcoin is a plausible Web3 grant lane for public-good developer tooling, but only after the project, round domain, grant rules, approval flow, KYC, anti-Sybil, Passport, wallet, and public-promotion gates are separated. This packet creates a local grant-fit worksheet and scorer; it does not log in, connect a wallet, submit an application, start KYC, solicit contributions, create Allo profiles/pools, transact, or publish anything.

## Grant Route Disambiguation

Gitcoin can mean a current Grants round, Grants Stack tooling, Allo protocol allocation infrastructure, Passport/Human anti-Sybil identity, or legacy cGrants. This lane is grant-fit only: it can produce a local project fit memo and application checklist, but GitHub login, grant creation, KYC, Passport/stamps, wallet connection, onchain profile creation, donations, matching claims, public promotion, and payment/payout activity are all separate approval gates.

## Sources

- `https://grants.gitcoin.co/` (official_current_grants_round_page): The current Gitcoin grants page is titled Gitcoin Grants 24: Fund What Matters. It says applications and donations are open and describes domains such as Developer Tooling and Infrastructure. The page exposes apply/info routes, but this packet does not click through, log in, connect wallets, or submit anything.
- `https://support.gitcoin.co/gitcoin-knowledge-base/llms.txt` (official_support_index): Gitcoin support exposes a machine-readable markdown index with grants, Grants Stack, KYC, rules, and policy pages. Use this as the current source map for later read-only grant documentation refreshes.
- `https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants/what-is-a-grant.md` (official_grants_program_docs): Gitcoin Grants is a quarterly program using quadratic funding to support web3 and digital public goods. The program routes funding through community contributions and matching mechanisms, so proof of public-good fit matters.
- `https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants/tips-for-grant-success.md` (official_grant_success_docs): Gitcoin advises grantees to upload early, ideally 15 days before the round starts, so approval and tag review have time. It recommends a clear TLDR, spending plan, justification, relevance to the round, impact metrics, roadmap, and public credibility.
- `https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants/general-questions/are-there-any-grant-rules-i-need-to-follow.md` (official_round_rules_docs): Round rules discuss contribution matching, unique contributor identity, anti-Sybil assumptions, and collusion constraints. Grant promotion or contribution farming can create compliance risk; this packet creates no public campaign or contribution request.
- `https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants/gitcoins-kyc.md` (official_kyc_docs): Gitcoin says KYC means Know Your Customer and is used to verify identity, prevent fraud, and satisfy matching partner concerns. Grantees may need KYC, so identity, legal, tax, and payout review remain explicit human gates.
- `https://support.gitcoin.co/gitcoin-knowledge-base/about-gitcoin/policy/grant-participation-policy/the-grant-approval-process.md` (official_grant_approval_docs): Gitcoin says a logged-in user using GitHub credentials can create a new grant, but it is not active in a round or eligible for matching until reviewed. The Anti-Fraud and Collusion workstream reviews grants for approval or denial. This makes application submission and approval a platform/account gate, not an automatic money path.
- `https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants/general-questions/how-do-you-prevent-sybil-attacks.md` (official_anti_sybil_docs): Gitcoin documents anti-Sybil controls such as aged GitHub accounts, SMS verification, BrightID, undisclosed vectors, and DID-style signals. Any grant route must avoid collusion, fake contributors, sybil behavior, and contribution incentives.
- `https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants-program/what-is-gitcoin-grants-stack.md` (official_grants_stack_docs): Gitcoin Grants Stack connects grants program managers, project owners, and community members. It covers program setup, application management, funds allocation, checkout, discovery, and application workflows.
- `https://docs-gitcoino.vercel.app/allo` (official_allo_docs): Allo is the smart-contract allocation protocol behind pools, strategies, roles, fees, and flow of funds. Creating/funding pools or interacting with allocation contracts is not needed for a local grant-fit proof and remains wallet/transaction gated.
- `https://docs-gitcoino.vercel.app/project-registry/create-profile` (official_allo_project_registry_docs): Allo project registry profile creation is an onchain-style contract interface involving owner and member addresses. Profile creation is a wallet/transaction route and is blocked here.
- `https://support.passport.human.tech/common-questions/how-score-calculated` (official_passport_score_docs): Human Passport documents score calculation and proof-of-humanity surfaces. Passport scoring can affect eligibility and anti-Sybil posture, but connecting wallets, stamps, or identity proofs is gated.
- `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-fit-memo-20260616.md` (local_prior_grant_fit_packet): Prior EF ESP grant work used a local-only fit memo, deliverable mapping, and submission gates. Reuse the same local proposal-fit posture for Gitcoin: source-backed fit first, no public submission.

## Grant Fields

- `round_url`
- `observed_utc`
- `round_name`
- `round_status`
- `domain_or_collection`
- `grant_program_type`
- `application_open`
- `donations_open`
- `application_deadline`
- `approval_timeline`
- `project_name`
- `project_owner`
- `project_public_good_fit`
- `target_domain_fit`
- `problem_statement`
- `deliverables`
- `roadmap`
- `impact_metrics`
- `budget_or_use_of_funds`
- `matching_mechanism`
- `eligibility_requirements`
- `grant_rules`
- `anti_sybil_requirements`
- `passport_or_identity_requirements`
- `kyc_requirements`
- `wallet_or_transaction_requirements`
- `github_or_account_requirements`
- `application_fields`
- `tag_request_requirements`
- `approval_or_review_body`
- `collusion_or_quo_policy_risk`
- `public_promotion_plan_local_only`
- `duplicate_or_prior_funding_signal`
- `evidence_links`
- `score`
- `kill_reasons`
- `next_local_action`

## Route Stages

- `public_round_discovery`: Record public round/domain text, deadlines, domains, and apply/info links into a local fixture. Gate `public_read_only`. Allowed now `True`.
- `grant_fit_memo`: Map one local project or product idea to public-good fit, domain fit, deliverables, budget, impact metrics, and evidence. Gate `local_only`. Allowed now `True`.
- `application_draft`: Create a private draft of fields likely needed for a grant application, without logging in or submitting. Gate `local_draft_only`. Allowed now `True`.
- `account_github_kyc_passport_gate`: GitHub login, Gitcoin account, KYC, Passport score/stamps, identity verification, or anti-Sybil proof. Gate `explicit_account_identity_approval_required`. Allowed now `False`.
- `wallet_allo_transaction_gate`: Wallet connection, onchain profile creation, pool interaction, donation, checkout, matching claim, payout, or transaction signing. Gate `explicit_wallet_payment_approval_required`. Allowed now `False`.
- `submission_gate`: Create grant, tag project for a round, submit application, upload public profile, or request approval. Gate `explicit_submission_approval_required`. Allowed now `False`.
- `public_promotion_gate`: Post, solicit contributions, coordinate donors, offer quid pro quo, or publish campaign materials. Gate `explicit_public_action_approval_required`. Allowed now `False`.

## Fit Rubric

- `round_domain_fit` (20 pts): project clearly maps to an open Gitcoin domain such as developer tooling or public goods
- `public_good_credibility` (15 pts): work is open, non-extractive, and useful to a broader ecosystem
- `deliverable_clarity` (15 pts): milestones, artifacts, and acceptance evidence are concrete
- `impact_metrics` (10 pts): usage, adoption, developer impact, or maintenance metrics are measurable
- `budget_reasonableness` (10 pts): use of funds is specific and proportional
- `approval_readiness` (10 pts): rules, tags, and review requirements are addressed before submission
- `identity_gate_clarity` (10 pts): KYC, GitHub, Passport, and anti-Sybil gates are known and not bypassed
- `no_collusion_risk` (10 pts): no quid pro quo, fake contributors, donation incentives, or coordinated Sybil behavior

## Hard Kill Reasons

- `round_not_open_or_domain_mismatch`
- `project_not_a_public_good_or_value_claim_unclear`
- `grant_rules_or_participation_policy_unreviewed`
- `requires_gitcoin_or_github_login_without_approval`
- `requires_kyc_passport_identity_or_personhood_verification_without_approval`
- `requires_wallet_connection_transaction_signature_or_onchain_profile`
- `requires_payment_donation_checkout_matching_claim_or_payout`
- `requires_public_submission_upload_or_tag_request_without_approval`
- `requires_public_campaign_contribution_solicitation_or_quid_pro_quo`
- `collusion_sybil_or_fake_contributor_risk`
- `budget_deliverables_or_impact_metrics_too_vague`
- `duplicate_prior_funding_or_eligibility_conflict_unresolved`
- `local_draft_cannot_produce_required_evidence`

## Boundary

- `browser_sessions_started`: `0`
- `gitcoin_account_or_login`: `False`
- `github_oauth_or_credentials_used`: `False`
- `kyc_or_identity_verification_started`: `False`
- `passport_or_stamps_connected`: `False`
- `wallet_connected_or_transaction_signed`: `False`
- `allo_profile_or_pool_created`: `False`
- `donations_checkouts_matching_claims_or_payouts`: `0`
- `grant_applications_submitted`: `0`
- `tag_requests_or_round_applications`: `0`
- `public_posts_or_contribution_solicitation`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a Gitcoin grant-fit memo for one candidate local product or open-source artifact, likely developer tooling or agent-company public-good infrastructure. Include round/domain fit, deliverables, budget/use of funds, impact metrics, prior work evidence, duplicate/funding sweep, rules checklist, KYC/Passport/GitHub/wallet gates, and an explicit no-submit approval packet. Keep account/login, GitHub OAuth, KYC, Passport/stamps, wallet/transaction, Allo profile/pool, donation/checkout/payout, grant submission/tag request, public campaign, worker/runtime, and model/MCP calls blocked.
