# Explicit-Payout Local Scout Packet - paid_code_bounties

Generated UTC: 2026-06-14T15:18:14Z
Agent: lane-manager-paid_code_bounties-019ec612
Task: task-paid-code-explicit-payout-local-scout-20260614
Status: read-only local scout complete
Realized USD: 0

## Scope

This packet applies the saved local scan design at:

E:\agent-company-lab\reports\paid-code-bounties\explicit-payout-source-scan-design-20260614.md

Inputs were local report snapshots and paid_code_bounties control-plane evidence only. I did not open PRs, fork, branch, comment, claim bounties, contact maintainers, register accounts, submit marketplace work, monitor payout submissions, or work on submitted_bounty_payouts. I also excluded RustChain, Charles, and GitHub payout-chasing rows from the active candidate pool.

## Input Snapshots

| Source | Snapshot UTC / State | Local Path |
| --- | --- | --- |
| Paid Code Bounty Scan | 2026-06-14T15:14:15Z, 168 rows, 5 ready/manual rows | E:\profit-edge-lab\reports\bounty-scan-latest.md |
| GitHub Fresh Bounty Pulse | 2026-06-14T15:14:15Z, 123 rows, 0 ready | E:\profit-edge-lab\reports\github-fresh-bounty-pulse-latest.md |
| UnitOne Skill Bounty Scan | 2026-06-14T14:59:07Z, 12 rows | E:\profit-edge-lab\reports\unitone-skill-bounty-scan-latest.md |
| Algora Bounty Scan | 2026-06-14T14:31:52Z, 82 rows, 0 ready | E:\profit-edge-lab\reports\algora-bounty-scan-latest.md |
| Opire Bounty Scan | 2026-06-14T14:31:52Z, 46 rows, 0 ready/high-value | E:\profit-edge-lab\reports\opire-bounty-scan-latest.md |
| BountyHub Bounty Scan | 2026-06-14T14:31:26Z, 24 rows, 0 ready/manual high-value | E:\profit-edge-lab\reports\bountyhub-bounty-scan-latest.md |
| BOSS Bounty Scan | 2026-06-13T21:27:38Z, all top rows gated | E:\profit-edge-lab\reports\boss-bounty-scan-latest.md |
| Gibwork Bounty Scan | 2026-06-13T11:56:12Z, all top rows gated | E:\profit-edge-lab\reports\gibwork-bounty-scan-latest.md |
| Gitpay Task Scan | 2026-06-13T11:24:59Z, all top rows gated | E:\profit-edge-lab\reports\gitpay-task-scan-latest.md |
| ProjectDiscovery Bounty Scan | 2026-06-14T14:20:03Z, 0 rows | E:\profit-edge-lab\reports\projectdiscovery-bounty-scan-latest.md |
| Control-plane lane evidence | 15 paid_code_bounties evidence rows | E:\agent-company-lab\state\agent_company.sqlite |

## Result Summary

| Bucket | Count | Decision |
| --- | ---: | --- |
| Clean candidates | 0 | No row survived duplicate, lane-boundary, public-action, and payout-quality gates. |
| Manual-review candidates | 4 | Keep for a future read-only verification task only; no public action. |
| Parked duplicate/public-action/lane-boundary rows | 20+ | Do not work unless source state changes and a scoped approval exists. |
| Rejected source families | 5 | BountyHub, BOSS, Gibwork, Gitpay, and ProjectDiscovery currently produce no clean paid-code work. |

The important update is that the previously attractive UnitOne $500 rows now all show linked PR signals in the local report. They are no longer clean local build candidates. The paid-code GitHub scan's best rows are all Charles microbounties, which are excluded from this lane.

## Clean Candidates

None.

Reason: every row with visible payout had at least one blocker: linked PR/submission, crowding, stale/manual-review gate, low/no material payout, platform-account gate, assignment gate, closed mismatch, specialist setup, or lane exclusion.

## Manual-Review Queue

These are not approved work items. They are the least-bad read-only follow-up targets if a future task wants to verify source state. No PR work or public action is allowed from this packet.

| Rank | Candidate | Source | Payout | Local Gate | Duplicate / Public-Action Gate | Allowed Next Action |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | archestra-ai/archestra#3218 - Auto sync permissions ACL support for Jira + Confluence connectors | Algora | 150 | manual_review, claims=3 | Need read-only issue, PR, claim-history, and acceptance check; no claim/comment | Read-only verification only |
| 2 | aueangpanit/electron-template#1 - Tray icon orange dot indicator | Opire | 100 | manual_review, competition=2, issue_check_failed | Need GitHub state and reward-state reconciliation; no claim/comment | Read-only verification only |
| 3 | Permify/permify-cli#2 - Endpoint, Token, Cert Path, and Cert Key Storage | Algora | 200 | stale_manual_review, claims=3 | Need maintainer/reward freshness check; no claim/comment | Read-only verification only |
| 4 | rustdesk/rustdesk#3762 - Add asio support | Algora | 100 | stale_manual_review, claims=0 | Need bounty still-honored check and feasibility check; no claim/comment | Read-only verification only |

## Parked High-Signal Rows

| Candidate / Family | Why It Looked Interesting | Park Reason |
| --- | --- | --- |
| UnitOneAI/SecuritySkills#2428-#2439 | 12 visible Complex ($500) rows | Every row now has `park_linked_pr_signal` with linked PR ids. Do not duplicate unless rejected or explicitly reopened. |
| charles-openclaw/charles-microbounties#1182/#1183/#1184/#1185/#1188 | Paid Code Bounty Scan says `pursue_if_unclaimed`, score 73 | Lane exclusion: Charles/RustChain/GitHub payout-chasing work is not this lane. Also would require public PR path. |
| matty33/eps-dapp#145/#148 | Large visible amounts, fresh GitHub pulse | Parked existing submissions / active linked PR search hits / likely in review or awarded. |
| SecureBananaLabs/bug-bounty#76/#80 | Visible bounty amounts | Very crowded: hundreds of comments; low payout probability. |
| Scottcjn/rustchain-bounties#731/#747 | Bounty labels and reward language | RustChain lane exclusion and crowded comment history. |
| BountyHub microg/GmsCore#2994 | $14,999 PAID listing | Crowded existing PRs: 554 comments, 6 open PRs, 25 PR hits, specialist setup. |
| BountyHub microg/GmsCore#2843 | $2,340 PAID listing | Crowded existing PRs: 135 comments, 7 open PRs, 31 PR hits, specialist setup. |
| Gibwork landing-page task | $350 remaining, USDC | 108 submissions, verified-submission/account gate, stale platform status. |
| Gitpay top task | $380 listed | Assignment/assignee gate plus PR signal; do not implement until assignment state is clear. |
| BOSS top rows | $250-$1,050 listed | Existing submission/PR or closed/not-open gates. |
| ProjectDiscovery | Official program source | No open rows in local scan. |

## Rejected Pattern Notes

- Visible amount alone is not enough. The row must have an explicit payout path and task-specific acceptance route.
- A linked PR signal is a hard duplicate gate, even when the issue remains open.
- Crowded bounty threads with hundreds of comments or many PR hits are bad cashflow candidates.
- Platform rows requiring claims, accounts, verified submissions, payout onboarding, or assignment state are service-request gated.
- Charles, RustChain, submitted_bounty_payouts, and GitHub payout-chasing rows are out of lane even when scanners rank them highly.

## Duplicate Checks Applied Locally

- Compared candidate URLs and source families against paid_code_bounties lane evidence.
- Used local report duplicate signals: linked PR ids, PR hit counts, active linked PR search hits, comments counts, claim counts, competition counts, closed mismatch flags, assignment gates, and platform submission counts.
- Collapsed source-family decisions where multiple reports pointed to the same blocker pattern.
- Did not perform a new browser or GitHub public action from this lane.

## Public-Action Gates

All candidate rows are still blocked from public action. A future service request would be required before any of the following:

- GitHub comment, PR, fork, branch, or bounty claim.
- Marketplace submission or account action.
- Maintainer contact.
- Payout onboarding, KYC, tax, billing, wallet, or payment setup.
- Work on submitted_bounty_payouts, RustChain, Charles, or payout-chasing lanes.

## Recommended Next Task

Create a new scoped read-only verification task only if the lane wants to continue. The best next verification target is Algora archestra-ai/archestra#3218, because it has the clearest non-excluded payout signal among the manual-review rows: $150, claims=3, not currently flagged as crowded in the local report. The verification should only check issue state, linked PRs, comments/claim history, repo health, and acceptance terms. It should end in either a parked blocker or a service-request recommendation; no public action.