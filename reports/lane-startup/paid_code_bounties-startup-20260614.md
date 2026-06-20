# Paid Code Bounties Startup Memo

Generated UTC: 2026-06-14T12:22:00Z
Agent: lane-manager-paid_code_bounties-019ec612
Thread: 019ec612-d317-71f1-b02f-c85f2295e320
Lane: paid_code_bounties
Department: Cashflow Engineering
Task: task-paid_code_bounties-startup-20260614

## Startup State

- Registered as department_manager for cashflow_engineering.
- Claimed paid_code_bounties after live status showed the lane was unowned.
- Created and acquired exactly one startup task: task-paid_code_bounties-startup-20260614.
- No service request exists for public action in this lane.
- Scope remains scout/rank only. No PR, issue comment, bounty claim, marketplace submission, maintainer contact, account registration, payout onboarding, or submitted_bounty_payouts work was performed.

## Source Material Read

- E:\agent-company-lab\README.md
- E:\agent-company-lab\reports\manager-packets\paid_code_bounties-manager-packet.md
- E:\agent-company-lab\reports\lane-manager-thread-launch-manifest-latest.md
- E:\agent-company-lab\reports\prompt-eval-review-latest.md
- E:\agent-company-lab\evals\manager-prompt-stop-gates-20260614.json
- Paid-code imported report set from E:\profit-edge-lab\reports: bounty-scan, github-fresh-bounty-pulse, algora, opire, bountyhub, boss, gibwork, gitpay, unitone, and projectdiscovery.

## Prompt Safety Gates Applied

Default stop gates from the prompt/eval registry:

- account_registration
- wallet_action
- browser_public_action
- legal_kyc_tax_billing
- security_testing_or_submission
- real_money_trade
- public_pr_comment_or_bounty_submission
- submitted_bounty_payout_lane

For this lane, the practical gate is stricter: local read-only scouting and ranking only until an approved service request names the exact public action and scope.

## What The Imported Rows Teach

The imported rows are mostly negative samples, not work orders. The recurring reject/park reasons are:

| Pattern | Examples | Why It Blocks Work |
| --- | --- | --- |
| Existing submission or active PR | FuZoe/PD-Hunter#18, matty33/eps-dapp#145/#148, BOSS rows, several Warpspeed/Spectral rows | High duplicate risk; do not duplicate unless existing work is rejected and the maintainer requests alternatives. |
| Crowded bounty or claims | BountyHub microg/GmsCore#2994, UnsafeLabs Algora rows, Gibwork landing-page task | Low payout probability and high time sink even when amount is visible. |
| No material payout or amount false positive | GitHub Fresh Pulse low/no amount rows, FuZoe amount false positive | Visible numbers are not enough; payout must be real, material, and attached to this task. |
| Assignment or attribution gate | Gitpay assignment rows, UnitOneAI/SecuritySkills#2423, BountyHub assigned/exclusive rows | Cannot safely work without clear assignment or clean attribution. |
| Closed or platform mismatch | BountyHub closed GitHub issues, Opire closed mismatch rows | Marketplace and GitHub state must agree before ranking. |
| Unclean public artifact requirement | UnsafeLabs/Bounty-Hunters#515 | Public disclosure of session/system material is not acceptable. |
| Account, claim, or submission route needed | Gibwork, BountyHub/Gitpay assignment flows, marketplace claims | Requires a scoped approved service request before any external action. |
| Aggregator or lead-only noise | relayhop/sn-monetization-runtime radar row | Upstream bounty source must be verified directly. |

## Source Posture

- UnitOne Skill Bounty: strongest local-artifact source. The report contains 12 open unassigned Complex ($500) rows with no development PRs, but any public submission remains gated.
- Algora: useful only after claim-count and stale/crowding filters. Current report has 82 rows, 0 ready rows, and 21 manual-review rows.
- Opire: potentially useful for explicit reward discovery, but payer/repo credibility, competition, GitHub state, and linked work must be checked before ranking.
- GitHub direct explicit-payout search: useful only with strict amount, recency, comments, linked-PR, and duplicate filters.
- BountyHub: prioritize only PAID rows with open GitHub issues, no assignment/exclusive state, low comments, and no open PRs. Current imported rows are mostly crowded or mismatched.
- Gibwork: park by default because many rows require account/submission routes, have crowded submissions, closed status, or no remaining amount.
- Gitpay: park until assignment/assignee state is clear.
- BOSS: park current rows because existing PR/submission or demo/closed gates dominate.
- ProjectDiscovery: no open bounty-label/amount-label rows in the imported scan.

## First Proof Artifact

The first proof artifact is the scan design at:

E:\agent-company-lab\reports\paid-code-bounties\explicit-payout-source-scan-design-20260614.md

It defines the fresh explicit-payout source scan, source order, duplicate checks, scoring model, and output schema. It deliberately stops before PR work.

## Next Action

Run a read-only local scout using the scan design and write a ranked candidate packet under E:\agent-company-lab\reports\paid-code-bounties\. The packet should include only local evidence and should end with either clean candidates that require a service request for public action, or a killed/parked list with exact blockers.

No money is realized from this startup task. Realized USD: 0.
