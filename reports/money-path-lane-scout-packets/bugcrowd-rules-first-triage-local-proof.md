# Bugcrowd Rules First-Triage Local Proof

- Generated: `2026-06-18T07:19:52Z`
- Task: `task-lane-scout-bugcrowd_program_rules-20260618`
- Lane: `security_bounty_private_reports`
- Status: `bugcrowd_rules_first_triage_ready_local_only`
- Decision: `rules_first_triage_only_no_account_no_testing_no_submission_no_payment_no_public_action`
- Validation: `True` with `0` failures

## Summary

Bugcrowd is a viable security-bounty lane only when a candidate is classified from the bounty brief first: program type, reward route, in-scope target group, out-of-scope target group, VRT mapping, safe harbor, disclosure terms, known issue/duplicate risk, and payment gates. This packet creates the local triage worksheet and scorer; it does not create an account, open a browser session, follow a program, test any target, save or submit a report, contact support, configure payment/tax, or disclose anything.

## Reward Route Disambiguation

Bugcrowd discovery mixes Reward programs, VDP programs, private invite-only engagements, pentests, charity programs, and community-curated listings. This lane is cash-first: VDP rows, charity rows, private invite rows, and non-cash recognition rows are not promoted as cash candidates unless a specific bounty brief exposes reward ranges for the in-scope target.

## Sources

- `https://www.bugcrowd.com/bug-bounty-list/` (official_public_program_list): Bugcrowd describes the public list as a comprehensive list of bug bounty and vulnerability disclosure programs curated by the hacker community. The list is discovery-only; individual program briefs still control scope, rules, rewards, and disclosure.
- `https://www.bugcrowd.com/hackers/` (official_hacker_page): Bugcrowd positions the hacker route as a way to report vulnerabilities ethically and earn rewards. The page advertises public engagements, triage, standardized VRT, program variety, and payments to hackers. This supports a rules-first bounty lane but not account setup, testing, submission, or payment setup.
- `https://docs.bugcrowd.com/researchers/participating-in-program/finding-program/` (official_program_discovery_docs): Public programs are open to researchers, while private programs require invitations and may have geographic, identity, trust, or skill restrictions. The docs say each program brief includes specific disclosure policy and rules that researchers must follow. Preset filters separate Reward, Vulnerability Disclosure, Charity, participating, invite, and hidden program categories.
- `https://docs.bugcrowd.com/researchers/participating-in-program/reviewing-bounty-briefs/` (official_bounty_brief_docs): Bugcrowd says the bounty brief contains targets, goals, scope, out-of-scope areas, additional rules, rewards, and expected review timing. It says to review the complete brief before beginning testing. It states out-of-scope testing can lead to out-of-scope results, point penalties, platform escalation, or bans. It notes VDP programs no longer offer point rewards, which reinforces reward-route separation.
- `https://docs.bugcrowd.com/researchers/disclosure/disclose-io-and-safe-harbor/` (official_safe_harbor_docs): Bugcrowd describes disclose.io as a vendor-agnostic framework for safe harbor in bug bounty and vulnerability disclosure programs. Program owners should provide in-scope properties, rewards, official communication channels, and disclosure policy. Bugcrowd distinguishes full safe harbor from partial safe harbor, so the triage packet must capture the safe harbor status.
- `https://docs.bugcrowd.com/researchers/reporting-managing-submissions/reporting-a-bug/` (official_reporting_docs): Bugcrowd says vulnerability reports should explain where the bug was found, who it affects, reproduction, affected parameters, and proof-of-concept support. Required report fields include summary title, target, technical severity/VRT, vulnerability details, and attachments. Submissions cannot be edited after being reported, making the submit action an explicit approval gate.
- `https://docs.bugcrowd.com/researchers/receiving-rewards/getting-rewarded/` (official_reward_docs): Cash rewards require a program that offers cash, an in-scope valid bug, reproducibility by triage or the program owner, and first-reporter status. Reward amount is set by the program owner with Bugcrowd input and varies by program, priority, and business impact. Duplicate and known issues can block cash reward eligibility.
- `https://bugcrowd.com/vulnerability-rating-taxonomy/` (official_vrt_source): Bugcrowd VRT is the baseline priority-rating resource for common vulnerabilities. The public page exposes a downloadable JSON VRT 1.18 and a GitHub conversation route for taxonomy changes. VRT priority is necessary but not sufficient for cash: program scope, impact, duplicates, and owner decision still matter.
- `E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md` (local_prior_security_scan): The prior security scan recommended rules-first security bounty work and static review before any target activity. It ranked Bugcrowd-like program rule review as high-upside only after scope and authorization are clear.
- `E:\agent-company-lab\reports\money-path-lane-scout-packets\hackerone-rules-route-readiness-local-proof.md` (local_prior_rules_packet): The HackerOne packet established the reusable security-bounty pattern: classify reward route, scope, safe harbor, duplicate risk, reporting route, and payment gates before any testing. Bugcrowd uses a distinct vocabulary around bounty briefs, VRT, CrowdStream, and safe harbor icons, so it gets its own packet.

## Brief Fields

- `program_url`
- `observed_utc`
- `program_name`
- `program_type`
- `program_status`
- `public_or_private`
- `requires_invitation`
- `identity_or_2fa_requirement`
- `reward_program`
- `cash_reward_range`
- `kudos_or_points_only`
- `managed_by_bugcrowd`
- `safe_harbor_status`
- `disclose_io_status`
- `official_communication_channels`
- `disclosure_policy`
- `brief_last_updated`
- `target_groups`
- `in_scope_targets`
- `out_of_scope_targets`
- `target_technology`
- `reward_range_by_target`
- `vrt_priority_mapping`
- `program_rules`
- `forbidden_testing`
- `credential_or_test_account_policy`
- `rate_limit_or_automation_policy`
- `known_issues_available`
- `duplicate_risk_signal`
- `submission_limit_or_throttle`
- `report_required_fields`
- `proof_of_concept_expectations`
- `payment_method_or_tax_gate`
- `local_static_candidate_source`
- `score`
- `kill_reasons`
- `next_local_action`

## Triage Stages

- `public_program_list_fixture`: Capture public program-list rows or manually saved brief snippets into a local fixture. Gate `local_or_approved_read_only_browser`. Allowed now `True`.
- `bounty_brief_extraction`: Extract program type, reward range, scope, out-of-scope targets, rules, safe harbor, disclosure policy, and known issue gates. Gate `public_read_only_no_login_no_testing`. Allowed now `True`.
- `vrt_and_duplicate_triage`: Map the candidate weakness to VRT priority and reject known issue or likely duplicate patterns from local/public evidence. Gate `local_only_or_public_read_only`. Allowed now `True`.
- `local_static_candidate_prep`: Prepare only source-code, documentation, or fixture-based hypotheses without probing live targets. Gate `local_source_review_only`. Allowed now `True`.
- `security_testing_gate`: Any live target access, scanner, account workflow, credential use, exploit attempt, API call, or target validation. Gate `explicit_security_testing_approval_required`. Allowed now `False`.
- `submission_draft`: Write a local draft with title, target, VRT classification, reproduction, impact, evidence, and caveats. Gate `local_draft_only`. Allowed now `True`.
- `submission_payment_disclosure_gate`: Submit report, save platform draft, contact support, follow a program, configure payment/tax, disclose publicly, or interact with CrowdStream. Gate `explicit_operator_approval_required`. Allowed now `False`.

## Scoring Rubric

- `reward_clarity` (20 pts): brief shows reward ranges for the specific in-scope target
- `scope_clarity` (15 pts): in-scope and out-of-scope target groups are explicit
- `safe_harbor_clarity` (15 pts): full safe harbor or clear disclose.io terms are visible
- `vrt_fit` (10 pts): candidate weakness maps cleanly to VRT P1-P3 with realistic impact
- `local_static_proofability` (15 pts): candidate can be proven from source, docs, fixtures, or local reproduction
- `duplicate_known_issue_risk` (10 pts): known issues or public examples do not already cover the path
- `low_harm_profile` (10 pts): no out-of-scope, DoS, spam, PII, social engineering, or credential-heavy testing needed
- `payment_gate_clarity` (5 pts): reward payout method/tax steps are known and remain post-award gates

## Hard Kill Reasons

- `vdp_charity_points_only_or_no_cash_reward_for_cash_lane`
- `program_private_invite_or_membership_required`
- `brief_unreadable_without_account_or_terms_acceptance`
- `scope_or_reward_range_unclear`
- `safe_harbor_or_disclosure_terms_missing_or_partial_without_clarity`
- `requires_testing_out_of_scope_targets`
- `requires_live_security_testing_without_explicit_approval`
- `requires_credentials_pii_social_engineering_dos_spam_or_phishing`
- `known_issue_duplicate_or_first_reporter_status_unlikely`
- `vrt_priority_too_low_or_non_exploitable_for_cash_effort`
- `submission_limit_or_platform_privilege_risk_unclear`
- `cannot_produce_local_static_or_fixture_based_proof`

## Boundary

- `browser_sessions_started`: `0`
- `bugcrowd_account_or_login`: `False`
- `programs_followed_or_feedback_sent`: `0`
- `support_tickets_or_contacts`: `0`
- `programs_joined_or_invites_accepted`: `0`
- `targets_tested`: `0`
- `security_testing_performed`: `0`
- `credentials_or_private_assets_used`: `0`
- `reports_submitted_or_drafts_saved`: `0`
- `crowdstream_actions`: `0`
- `public_comments_or_disclosures`: `0`
- `payments_or_tax_forms`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a no-login Bugcrowd public-program fixture from manually saved program-list and bounty-brief snippets; run the first-triage scorer; emit only local/static candidate drafts with VRT, scope, safe harbor, reward, and known-issue gates. Keep account, browser login, program following, support tickets, target testing, report draft saving/submission, payment/tax forms, CrowdStream, public disclosure, worker/runtime, and model/MCP calls blocked.
