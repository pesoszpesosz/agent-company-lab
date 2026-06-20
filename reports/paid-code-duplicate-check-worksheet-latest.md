# Paid-Code Duplicate-Check Worksheet

Generated UTC: 2026-06-15T20:44:26Z
JSON mirror: `E:\agent-company-lab\reports\paid-code-duplicate-check-worksheet-latest.json`
Validation: `E:\agent-company-lab\reports\paid-code-duplicate-check-worksheet-validation-latest.json`
Source proof: `E:\agent-company-lab\reports\first-ranked-manager-proof-latest.json`

## Summary

Built a paid-code duplicate-check worksheet from the completed first ranked proof. It separates six local-only checks from six gated checks that require explicit browser, legal/payment, public-action, or security approval.

## Worksheet

| Item | Mode | Gate | Question |
| --- | --- | --- | --- |
| `local-evidence-normalization` | `local_only` | `` | Summarize the imported evidence row in one sentence and identify why it was parked, rejected, or still candidate-worthy. |
| `candidate-status-from-import` | `local_only` | `` | Classify the candidate as rejected, parked, or needs fresh triage using only local imported status and next_action fields. |
| `duplicate-risk-from-import` | `local_only` | `` | Extract known duplicate signals such as active PRs, many comments, existing claims, owner hold, or rewarded duplicate work. |
| `payout-trust-from-import` | `local_only` | `` | Record any local evidence about escrow, paid state, bounty amount confidence, attribution, or payment gate risk. |
| `effort-shape-from-import` | `local_only` | `` | Infer repo/language/test/build effort only from local scan summaries; mark unknowns instead of browsing. |
| `local-go-no-go-note` | `local_only` | `` | Write a no-browser go/no-go note and the exact gate that would be needed before refreshing the candidate live. |
| `live-open-state-check` | `blocked_by_gate` | `browser_read_only_session` | Verify whether the issue is still open and the bounty still accepts new work. |
| `live-pr-claim-check` | `blocked_by_gate` | `browser_read_only_session` | Check live PRs, comments, claims, and maintainer signals for duplicate or stale work. |
| `terms-and-payout-check` | `blocked_by_gate` | `legal_kyc_tax_payment` | Confirm current bounty terms, payout route, attribution, and any account or payment requirements. |
| `repo-build-feasibility-check` | `blocked_by_gate` | `browser_read_only_session` | Inspect repo setup, tests, language/tooling, and likely implementation surface. |
| `public-claim-or-pr-action` | `blocked_by_gate` | `public_action_approval` | Comment, claim, submit PR, or otherwise make a public action. |
| `security-sensitive-review` | `blocked_by_gate` | `security_testing_approval` | Run exploit/security testing or security-sensitive validation beyond public code review. |

## Boundary

This worksheet is local only. It creates and completes one local coordination task and adds one local evidence row; it does not browse, use accounts, accept terms, claim bounties, submit PRs, comment publicly, contact maintainers, perform security testing, touch wallets/payments, call APIs, assign/start workers, mutate service requests, or create external side effects.

## Next Action

Paid-code lane manager should complete the six local-only worksheet items first; any live issue refresh, claim, PR, payout, or security-sensitive step must go through service requests.

