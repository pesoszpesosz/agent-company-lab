# HackerOne Rules Route Readiness Local Proof

- Generated: `2026-06-18T07:15:32Z`
- Task: `task-lane-scout-hackerone_program_rules-20260618`
- Lane: `security_bounty_private_reports`
- Status: `hackerone_rules_route_readiness_ready_local_only`
- Decision: `rules_readiness_only_no_account_no_testing_no_submission_no_payment_no_public_action`
- Validation: `True` with `0` failures

## Summary

HackerOne is a viable security-bounty research lane only after each candidate program is classified by program type, bounty eligibility, scope, safe harbor, exclusions, duplicate risk, report route, and payment gates. This packet builds the local rules-readiness worksheet and scorer inputs; it does not create an account, open a browser session, test any target, submit a report, contact a program, configure payouts, or disclose anything.

## Cash Route Disambiguation

HackerOne discovery mixes cash BBP opportunities, VDP-only disclosure routes, pentest engagements, and private/invite-only work. This lane is cash-first: VDP-only rows are useful for practice, disclosure process learning, or reputation, but they must not be promoted as bounty-cash candidates unless the specific program or asset exposes bounty eligibility.

## Sources

- `https://www.hackerone.com/product/bug-bounty-platform` (official_bbp_product_page): HackerOne describes H1 Bounty as continuous researcher-led testing by a global community. The page says programs expose bounty tables, disclosure guidelines, safe harbor statements, payments, researcher controls, report lifecycle management, triage, and response data. This supports a rules-first cash route, but not direct target testing without a specific program policy and explicit operator approval.
- `https://www.hackerone.com/hackers` (official_hacker_page): The hacker page separates bug bounty programs, HackerOne Clear, pentest engagements, and Vulnerability Disclosure Programs. It states that researchers can use VDPs to submit vulnerabilities to organizations that welcome reports and commit to safe harbor. It also says bounty payment identity may be required, so payment and tax handling remain gated.
- `https://www.hackerone.com/terms/disclosure-guidelines` (official_disclosure_guidelines): Guidelines tell finders to respect program rules, privacy, patience, and do no harm. They say each program publishes a policy for the specific service or product and that the program policy supersedes general guidelines when conflicts exist. Submission guidance requires detailed vulnerability descriptions, reproducible steps, and proof-of-concept detail. Bounty payments are discretionary, subject to eligibility restrictions, paid in USD, and tax consequences remain the researcher's responsibility.
- `https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq` (official_safe_harbor_docs): HackerOne says safe harbor is a clear statement that good-faith security research is authorized and protected from organization legal action. The January 2026 article says scope definitions remain based on explicitly included assets, even when safe harbor is enabled. It recommends clarification before borderline conduct and says bad-faith conduct is not covered.
- `https://docs.hackerone.com/en/articles/8494552-defining-scope` (official_scope_docs): HackerOne scope assets have types, identifiers, eligibility for submission, eligibility for bounty, environmental scoring, labels, and instructions. Assets can be ineligible for submission or bounty, and HackerOne exposes warnings when a selected asset is not paid or reportable. This makes asset-level scope and bounty eligibility required fields before any cash-route work.
- `https://docs.hackerone.com/en/articles/8369900-opportunity-discovery` (official_opportunity_discovery_docs): Opportunity Discovery centralizes bounty programs, VDPs, pentests, and future earning openings. Program cards include program features, asset types, minimum and maximum bounty, response standards, and status tags. Filtering by program type, asset type, industry, and sort order is a read-only discovery route, but live page interaction is still gated in this lab.
- `https://docs.hackerone.com/en/articles/8410373-directory` (official_directory_docs): The Directory documents organization security contacts, disclosure policies, and associated bug bounty programs. It exposes program data such as launch date, reports resolved, minimum and average bounty, managed labels, active-program labels, and bounty availability filters. Directory pages can include organizations that do not use HackerOne, so report route and bounty eligibility must be verified per program.
- `https://docs.hackerone.com/en/articles/8410358-hacktivity` (official_hacktivity_docs): Hacktivity is a learning signal showing community activity, disclosed reports, and bounty-awarded activity. Disclosed reports can inform duplicate-risk and report-quality checks, but they are not permission to test a target.
- `https://docs.hackerone.com/en/articles/8473994-submitting-reports` (official_submission_docs): Submitting a report requires using a program security page, selecting asset and weakness fields, writing proof of concept, impact, and reproduction steps, then submitting. The final submit action cannot be undone for report details and therefore remains blocked without exact approval.
- `https://docs.hackerone.com/en/articles/8475116-quality-reports` (official_report_quality_docs): High-quality reports should outline the bug, reproduce it, assess coverage, and include relevant logs or supporting material. Before submitting, researchers should verify that the issue is in scope and not already reported. Report quality requirements favor local/static proof preparation before any platform submission.
- `https://docs.hackerone.com/en/articles/8399426-payment-faqs` (official_payment_docs): Payment FAQ mentions PayPal, Coinbase, and Currencycloud as payout providers. Payments can take time after award and require a valid tax form and selected payout method. Payment preferences, tax forms, identity, and payout setup remain human-gated.
- `E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md` (local_prior_security_scan): The prior local security scan ranked rules-first bounty discovery as high upside but required a rules-first gate before any target work. It favored static source review and exact scope review over active testing.
- `E:\profit-edge-lab\reports\issuehunt-security-program-scan-latest.md` (local_prior_alternative_scan): The IssueHunt scan demonstrates the same pattern: public program rows can be scored, but account setup, testing, and reporting require approval. It supplies a reusable rules-first scoring discipline for the HackerOne lane.

## Program Fields

- `program_url`
- `observed_utc`
- `program_name`
- `program_type`
- `program_status`
- `bounty_available`
- `minimum_bounty`
- `maximum_bounty`
- `average_bounty`
- `managed_by_hackerone`
- `response_standards`
- `asset_types`
- `scope_assets`
- `out_of_scope_assets`
- `asset_eligibility_for_submission`
- `asset_eligibility_for_bounty`
- `safe_harbor_present`
- `safe_harbor_variant`
- `program_policy_url`
- `testing_permissions`
- `forbidden_testing`
- `rate_limits`
- `credential_policy`
- `privacy_data_policy`
- `disclosure_policy`
- `duplicate_policy`
- `minimum_severity`
- `report_template_fields`
- `proof_of_concept_expectations`
- `payment_tax_identity_requirements`
- `country_or_sanctions_eligibility`
- `public_activity_signal`
- `hactivity_duplicate_signal`
- `local_candidate_source`
- `score`
- `kill_reasons`
- `next_local_action`

## Route Stages

- `public_discovery_fixture`: Capture public program/opportunity/directory card text into a local fixture. Gate `local_or_approved_read_only_browser`. Allowed now `True`.
- `program_rules_extraction`: Extract program type, bounty eligibility, scope, safe harbor, exclusions, response standards, disclosure, and payout gates. Gate `public_read_only_no_login_no_testing`. Allowed now `True`.
- `local_static_candidate_prep`: For source-code or OSS-like assets only, prepare local/static hypotheses without touching live targets. Gate `local_source_review_only`. Allowed now `True`.
- `hacktivity_duplicate_review`: Use public disclosed report patterns only to reject duplicates and improve report structure. Gate `public_read_only_no_upvote_no_follow_no_comment`. Allowed now `False`.
- `security_testing_gate`: Any live target probing, credential use, scanner, API call, rate-limit interaction, exploit check, or account workflow. Gate `explicit_security_testing_approval_required`. Allowed now `False`.
- `private_report_draft`: Write a report draft with title, scope proof, impact, local reproduction, caveats, and screenshots/logs if locally generated. Gate `local_draft_only`. Allowed now `True`.
- `submission_payment_public_disclosure_gate`: Submit report, set payout/tax preferences, request disclosure, contact program, or publish anything. Gate `explicit_operator_approval_required`. Allowed now `False`.

## Scoring Rubric

- `cash_bounty_clarity` (20 pts): specific program and asset expose bounty eligibility and min/max reward
- `scope_clarity` (15 pts): in-scope and out-of-scope assets are explicit and narrow
- `safe_harbor_clarity` (15 pts): program includes clear safe harbor for good-faith work
- `local_static_proofability` (15 pts): issue can be researched from public source or local fixtures without live testing
- `low_harm_profile` (10 pts): no need for credentials, PII, production mutation, scanning, or sensitive data
- `duplicate_risk` (10 pts): Hacktivity/public reports do not show the same weakness path
- `payout_tax_route_clarity` (5 pts): eligibility and payout/tax gates are known before submission
- `report_effort_fit` (10 pts): proof can be written with clear reproduction, impact, and remediation within one focused sprint

## Hard Kill Reasons

- `vdp_only_or_no_cash_bounty_for_cash_lane`
- `program_or_asset_not_accepting_submissions`
- `scope_or_bounty_eligibility_unclear`
- `safe_harbor_or_authorization_unclear`
- `requires_active_testing_without_explicit_approval`
- `requires_login_credentials_pii_social_engineering_dos_spam_or_phishing`
- `requires_touching_sensitive_or_production_only_data_without_safe_test_path`
- `duplicate_or_publicly_known_issue_likely`
- `payment_tax_identity_country_or_sanctions_eligibility_unclear`
- `private_program_invite_nda_or_clear_membership_required`
- `report_route_not_private_or_not_on_approved_platform`
- `local_static_or_fixture_proof_cannot_be_produced`

## Boundary

- `browser_sessions_started`: `0`
- `hackerone_account_or_login`: `False`
- `programs_contacted`: `0`
- `programs_bookmarked_or_followed`: `0`
- `directory_edits_or_feedback`: `0`
- `hactivity_votes_or_follows`: `0`
- `targets_tested`: `0`
- `security_testing_performed`: `0`
- `credentials_or_private_assets_used`: `0`
- `reports_submitted`: `0`
- `public_comments_or_disclosures`: `0`
- `payments_or_tax_forms`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a no-login HackerOne public program fixture from manually saved program directory, Opportunity Discovery, and program-policy snippets; run the scorer; emit only static/public-code-review candidate drafts. Keep account, browser login, target testing, report submission, payment/tax forms, public disclosure, worker/runtime, and model/MCP calls blocked.
