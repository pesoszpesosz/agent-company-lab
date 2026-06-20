# Algora Live-Candidate Refresh Scanner Packet

Generated UTC: 2026-06-16T20:54:00Z
Task: `task-algora-live-candidate-refresh-20260616`
Lane: `paid_code_bounties`
Owner: `lane-manager-paid_code_bounties-019ec612`
JSON mirror: `E:\agent-company-lab\reports\paid-code-bounties\algora-live-candidate-refresh-20260616.json`

## Purpose

Specify a read-only scanner packet for finding Algora bounty candidates without claiming, commenting, forking, submitting PRs, or providing payout details.

## Scanner Inputs

| Input | Example | Required |
| --- | --- | --- |
| Algora project URL | `https://algora.io/golemcloud/home` | Yes |
| Bounty list URL | `https://algora.io/CapSoftware/bounties` | Yes |
| GitHub issue URL | Captured from Algora listing if present. | If present |
| Bounty amount | Cash amount exactly as displayed. | Yes |
| Open/completed state | Open, completed, no open bounties, unclear. | Yes |
| Visible claim/crowding signal | Claim count, awarded user, discussion volume. | If visible |
| Last visible activity | Listing age or GitHub issue update timestamp. | If visible |

## Scanner Output Schema

| Field | Type | Meaning |
| --- | --- | --- |
| `candidate_id` | string | Stable ID from project and issue. |
| `algora_url` | string | Public Algora URL. |
| `github_issue_url` | string/null | Public issue URL if visible. |
| `amount_usd` | number/null | Explicit displayed bounty amount. |
| `state` | enum | `open`, `completed`, `none_open`, `unclear`. |
| `claim_count` | number/null | Visible claim/crowding count. |
| `repo_health` | enum | `active`, `stale`, `unknown`. |
| `local_testability` | enum | `clear`, `unclear`, `blocked`. |
| `decision` | enum | `promote_local_triage`, `watchlist`, `reject`. |
| `gate` | string | Public-action/payment gate notes. |

## Rejection Rules

- Reject if amount is missing or not explicit.
- Reject if state is completed/closed.
- Reject if bounty is tiny and visibly crowded.
- Reject if local tests require credentials, paid services, private data, or account setup.
- Reject if issue acceptance is broad or subjective.
- Park if GitHub public action would be needed to clarify terms.

## Current Seed Rows

| Candidate | Public Signal | Scanner Decision |
| --- | --- | --- |
| Algora org examples | Completed bounties and bounty mechanism visible. | Reference only; no open candidate. |
| Golem Cloud | Large completed history, zero open bounties on public page. | Watchlist only. |
| CapSoftware / Cap | Open low-value bounty with many visible claims. | Reject for current sprint due to low amount/crowding. |
| Turso/Golem/TSPerf/Prettier categories | Navigation signals possible source pages. | Add to next read-only source refresh. |

## Pseudocode

```text
for each configured_algora_url:
    fetch public page text through approved read-only mechanism
    parse visible open_count, completed_count, amount, issue, claims
    if open_count == 0:
        decision = "watchlist"
    elif amount_usd is null or amount_usd < 100:
        decision = "reject"
    elif claim_count is not null and claim_count > 3:
        decision = "reject"
    elif local_testability != "clear":
        decision = "watchlist"
    else:
        decision = "promote_local_triage"
    write row to local worksheet
```

## Next Action

Implement `algora-candidate-refresh-fixture-20260616.json` with 5-10 configured public URLs and a no-network parser fixture before any live refresh.

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- GitHub actions: `false`
- Security testing actions: `false`
- Real-money actions: `false`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
