# Algora Explicit-Payout Issue Worksheet

Generated UTC: 2026-06-16T20:39:00Z
Task: `task-algora-explicit-payout-worksheet-20260616`
Lane: `paid_code_bounties`
Owner: `lane-manager-paid_code_bounties-019ec612`
JSON mirror: `E:\agent-company-lab\reports\paid-code-bounties\algora-explicit-payout-issue-worksheet-20260616.json`

## Purpose

Create a duplicate-aware local worksheet for Algora paid GitHub issues before any public claim, comment, fork, PR, or payout setup. The goal is to identify only explicit-payout work that has a realistic route to first money and can be proven locally.

## Source Signals

| Signal | Evidence | Routing Meaning |
| --- | --- | --- |
| Bounty mechanism is GitHub-comment based | Algora public bounty pages say bounties can be created by commenting `/bounty $1000` on GitHub issues. | Public GitHub actions are central and must stay gated. |
| Completed bounty proof exists | Algora organization pages show completed bounties with amounts and issue references. | Historical payouts prove mechanism, but not current availability. |
| Open inventory can be sparse | Some public organization pages currently show zero open bounties; one CapSoftware page surfaced an open low-value bounty with many claims. | Need freshness and crowding checks before spending coding time. |
| High-value historical events exist | Golem Cloud public page shows completed bounties with larger amounts and top earner totals. | Good source for pattern learning, not necessarily a live cash slot today. |

## Explicit-Payout Filters

| Filter | Pass Rule | Reject/Park Rule |
| --- | --- | --- |
| Amount clarity | Public issue or Algora page shows an explicit bounty amount before work starts. | Park if payout is implied, stale, private, or hidden behind login. |
| Open state | Bounty is currently open and issue is not solved/claimed/merged. | Reject if closed, completed, or clearly superseded. |
| Crowding | Claim count is low or assignment/claim rules protect effort. | Reject or deprioritize if many visible claims and no reservation. |
| Owner route | Maintainer/bounty owner has a clear review path and recent activity. | Park if repo is abandoned or payout owner is unclear. |
| Testability | Local reproduction and tests can prove completion before public action. | Reject if requires credentials, paid services, private data, or undefined acceptance. |
| Scope size | Can be completed in a bounded local sprint. | Park if it is a broad product build with unclear acceptance. |
| Public-action readiness | PR/comment/claim path can be reviewed as a service request. | Do not act directly from this worksheet. |

## Candidate Source Rows

| Candidate | Current Public Signal | Local Duplicate Check | Risk | Decision |
| --- | --- | --- | --- | --- |
| Algora organization examples | Completed page shows 25 completed bounties and the `/bounty` mechanism. | Use as format/reference only. | No current open bounty on this page. | Reference only. |
| Golem Cloud | Public page shows zero open bounties but large completed bounty history. | Monitor for future open bounties; use completed rows for acceptance-pattern study. | Currently no live open work. | Watchlist, not active sprint. |
| CapSoftware / Cap | Public page surfaced an open low-value bounty and many visible claims. | Check issue state locally/read-only before any action if promoted. | Low amount and heavy crowding. | Reject for current sprint unless no better source. |
| Turso / Golem / TSPerf / Prettier menu links | Algora navigation lists these as bounty categories. | Queue read-only source refresh if paid-code lane needs live candidates. | Requires current browser/source refresh; no public action. | Candidate source list. |
| Existing local paid-code queue | Prior lab rows include duplicate-check and browser-refresh decision packets. | Reuse negative samples to avoid stale/claimed work. | Must respect parked browser/GitHub gate. | Use as guardrail. |

## Local Triage Command Proposal

The paid-code lane should build or run a read-only scanner that records:

- Algora org/project URL.
- Open bounty count.
- Amount.
- GitHub issue URL.
- Claim count or visible competing activity.
- Last maintainer activity.
- Required stack.
- Local test command.
- Public-action gate status.

No comments, claims, PRs, forks, or payout details are allowed from the scanner.

## Score

| Metric | Score | Notes |
| --- | ---: | --- |
| Expected dollars/hour | 3 | Strong when clean bounties exist; current examples are sparse or crowded. |
| Time to first local proof | 4 | Duplicate-check worksheet and scanner can be local. |
| Gate burden | 3 | GitHub public action and payment route are gated. |
| Competition/crowding risk | 4 | Many bounty systems invite duplicated work. |
| Agent fit | 5 | Excellent fit for repo triage, tests, and duplicate checking. |

## Required Approval Gates

- `github_public_action_gate` before claim/comment/PR/fork intended for public work.
- `legal_kyc_tax_payment_gate` before payout setup or bounty terms acceptance.
- Repo-specific license/contribution review before public PR.

## Prohibited Actions

- No GitHub comments.
- No bounty claims.
- No forks/PRs for bounty work.
- No payout details.
- No account/payment setup.
- No use of credentials or private repo data.

## Next Action

Create a local `algora-live-candidate-refresh` read-only packet or scanner that compares Algora project pages and rejects rows with zero open bounties, tiny payout, heavy claim crowding, stale maintainer activity, or unclear acceptance.

## Source URLs

- https://algora.io/algora/bounties?status=completed
- https://algora.io/capgo/bounties?status=open%2F
- https://algora.io/golemcloud/home
- https://algora.io/CapSoftware/bounties

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- Security testing actions: `false`
- Real-money actions: `false`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
