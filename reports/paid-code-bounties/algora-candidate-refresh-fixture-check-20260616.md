# Algora Candidate Refresh Fixture Check

Generated UTC: 2026-06-16T20:58:48Z
Fixture: `E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-20260616.json`
JSON mirror: `E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-check-20260616.json`

## Summary

- Fixtures checked: `6`
- Passed: `6`
- Failed: `0`
- Network calls: `false`
- External side effects: `false`

## Rows

| Fixture | Decision | Status | Notes |
| --- | --- | --- | --- |
| `algora_org_examples_reference_only` | `reference_only` | `pass` | No candidate issue; use only to verify parser shape. |
| `golemcloud_zero_open_watchlist` | `watchlist` | `pass` | Wait for an explicit open bounty before local triage. |
| `capsoftware_low_amount_crowded_reject` | `reject` | `pass` | Do not spend sprint time on low-value crowded bounty. |
| `turso_unclear_amount_watchlist` | `watchlist` | `pass` | Read-only refresh required for explicit amount and acceptance state. |
| `prettier_clear_local_triage_candidate` | `promote_local_triage` | `pass` | Local triage only; no claim, comment, PR, or payout details without GitHub/public-action approval. |
| `tsperf_subjective_acceptance_reject` | `reject` | `pass` | Reject until measurable acceptance target exists. |

## Boundary

- Live Algora fetch: `false`
- Live GitHub fetch: `false`
- GitHub comments/claims/PRs: `false`
- Account/payment/public actions: `false`
- External side effects: `false`
