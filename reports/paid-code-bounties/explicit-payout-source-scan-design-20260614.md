# Explicit-Payout Source Scan Design - paid_code_bounties

Generated UTC: 2026-06-14T12:22:00Z
Lane: paid_code_bounties
Task: task-paid_code_bounties-startup-20260614
Artifact type: source_scan_design
Status: scout/rank design only

## Objective

Find fresh paid-code opportunities with explicit payout terms, then rank them before any PR work. The scan must reject duplicates, crowded rows, closed/mismatched rows, low-trust payout paths, and anything requiring a public action or account step without an approved service request.

## Non-Negotiable Stop Line

Allowed now:

- Read local imported reports.
- Read public issue, PR, and marketplace metadata.
- Save local scan outputs, rankings, and decision notes.

Blocked without an approved service request for the exact scope:

- PR, branch, fork, issue comment, claim, marketplace submission, maintainer contact, account registration, payout onboarding, KYC/tax/billing, wallet action, live security testing, submitted_bounty_payouts monitoring, RustChain, Charles, or GitHub payout chasing.

## Ranked Source Plan

| Rank | Source | Include When | Reject/Park When | Expected Output |
| ---: | --- | --- | --- | --- |
| 1 | UnitOneAI/SecuritySkills explicit Complex ($500) skill issues | Open, unassigned, no linked development PR, local skill artifact possible, acceptance text clear | Prior contributor attribution unclear, existing PR appears, public submission required before local validation | Local artifact candidate packet; service request required before any public submission |
| 2 | Algora open bounties | Amount >= $100, claim count <= 3, issue open, low comments, clear acceptance, no active linked PR | Crowded claims, stale/no maintainer activity, security/live-target task, assignment unclear | Ranked manual-review shortlist |
| 3 | Opire open issues | Amount >= $100, competition <= 2, GitHub issue open, payer/repo credible, no linked work | Closed mismatch, low-trust fork, too small, active PR, stale reward, account/payout uncertainty | Ranked manual-review shortlist with Opire and GitHub URLs |
| 4 | GitHub direct explicit-payout search | Recent open issue, explicit material payout in title/body/labels, comments <= 5, no assignee, no linked PR | No material payout, amount false positive, reward not tied to task, likely awarded, crowded, aggregator-only row | Fresh pulse rows with duplicate-check evidence |
| 5 | BountyHub | PAID/prepaid, GitHub open, no assignment/exclusive state, comments < 15, open PRs = 0 | PROMISED only, assigned, closed mismatch, open PRs, many prior PR hits, specialist-heavy setup | Park/consider list with payment state and GitHub state |
| 6 | BOSS | Open issue, explicit amount, no existing submission/PR | Existing submission/PR, demo row, closed/not open | Usually park unless clean open row appears |
| 7 | Gitpay | Amount >= $100, assignment state clear and open | Assignment/assignee present or unclear | Park until assignment state is verified |
| 8 | Gibwork | Code-focused, open, remaining amount > 0, low submissions, no account-only route | Closed/expired, completed, crowded, no remaining amount, non-code/social, verified submission/account gate | Park by default; require service request before platform action |
| 9 | ProjectDiscovery OSS bounty labels | Open amount-label rows | No open rows | No-op unless source changes |

## Negative Sample Filters

Reject before scoring if any condition is true:

- Issue is closed, marketplace state conflicts with GitHub state, or bounty is completed/expired.
- Payout amount is missing, below $100, non-material, not attached to the task, or likely parsed from unrelated text.
- Existing linked PR, open PR, claim, submission, maintainer review, or likely-awarded thread is present.
- Assignment, exclusive assignee, required claim, verified submission, or payout setup is needed before local evaluation.
- Comments > 15 or platform claim/submission count > 5, unless maintainer explicitly asks for new alternatives.
- Source is an aggregator that does not directly prove the upstream payout terms.
- The work requires public disclosure of session, prompt, private artifact, credentials, or account material.
- The work is security testing/submission rather than local code review or artifact creation.
- The source overlaps submitted_bounty_payouts, RustChain, Charles, or GitHub payout chasing.

## Duplicate Check Pipeline

1. Normalize identifiers:
   - canonical_issue_url
   - repo_full_name
   - issue_number
   - marketplace_name
   - marketplace_bounty_id
   - normalized_title_slug
   - payout_amount_usd

2. Local duplicate check:
   - Compare canonical_issue_url and repo#issue against paid_code_bounties lane_evidence.
   - Compare against imported source paths and E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl for paid-code rows only.
   - Mark rows as imported_duplicate, prior_rejected, prior_parked, or new_candidate.

3. Public duplicate check, read-only:
   - Fetch issue metadata: state, assignees, labels, comments count, updated_at.
   - Search PRs in the same repo for issue number, exact title phrases, and closing keywords.
   - Inspect linked PR metadata when visible from issue HTML/API.
   - Scan comments for claim, attempt, assigned, submitted, PR opened, under review, awarded, paid, or maintainer rejection signals.
   - Cross-check marketplace listing against GitHub issue state and open PR state.

4. Cross-source duplicate check:
   - Collapse rows when Algora, Opire, BountyHub, Gitpay, BOSS, or GitHub direct point to the same repo#issue.
   - Keep the source with the clearest payout mechanics and preserve all source URLs in evidence.

5. Decision gate:
   - new_clean_candidate: passes all checks, still no public action.
   - manual_review: needs human/source inspection but no public action.
   - parked_duplicate: existing PR/claim/submission or prior evidence.
   - rejected: no material payout, closed mismatch, unsafe requirement, account/payout gate, or wrong lane.

## Scoring Model

Start at 0.

Positive weights:

- +40 explicit payout >= $500
- +25 explicit payout $100-$499
- +20 open issue with no assignee and no linked PR
- +15 comments <= 3 or marketplace claims <= 2
- +15 local-artifact possible before public action
- +10 active maintainer/recent update within 14 days
- +10 tests or validation path can be assessed locally under 4 hours

Negative weights:

- -100 closed, completed, expired, or GitHub/marketplace mismatch
- -80 active linked PR, likely awarded, or existing submission
- -60 assignment/exclusive/claim required before local work
- -50 account registration, payout onboarding, wallet, KYC, or marketplace submission needed before evaluation
- -45 crowded comments/claims/submissions
- -40 low-trust fork, ambiguous payer, or unsupported payout route
- -35 security/live target testing or public disclosure requirement
- -30 no material payout or amount false positive risk
- -25 specialist environment likely over 4 hours

Rank buckets:

- 70+: clean scout candidate, still service-request gated before public action
- 40-69: manual-review candidate
- 1-39: watch or park
- <=0: reject/park with blocker

## Output Schema For The Fresh Scan

Each row should include:

- candidate_id
- status
- source_name
- source_url
- canonical_issue_url
- repo_full_name
- issue_number
- title
- payout_amount_usd
- payout_terms_text_evidence
- marketplace_state
- github_state
- assignees
- comments_count
- claim_count
- linked_pr_count
- open_pr_urls
- duplicate_status
- negative_sample_match
- score
- rank_bucket
- blockers
- allowed_next_action
- service_request_needed
- evidence_paths
- checked_at_utc

## First Execution Recommendation

Run sources in this order:

1. UnitOneAI/SecuritySkills Complex ($500) rows from the imported report, then refresh only by read-only GitHub issue metadata.
2. Algora open bounties filtered to amount >= $100, claims <= 3, no active linked PR, and non-security/local-code tasks.
3. Opire rows filtered to amount >= $100, competition <= 2, GitHub open, and no linked work.
4. GitHub direct search for recent explicit payout issues with amount >= $100 and comments <= 5.
5. BountyHub PAID rows only after GitHub open/no-PR/no-assignment checks.

Do not run PR, claim, comment, marketplace submit, or maintainer-contact steps from the scanner. A clean candidate should produce a local action packet plus a pending service-request recommendation, not an external action.
