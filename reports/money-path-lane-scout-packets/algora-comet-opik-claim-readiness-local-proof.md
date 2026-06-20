# Algora / Comet Opik Claim-Readiness Local Proof

Generated UTC: 2026-06-18T06:27:07Z
Task: `task-lane-scout-algora_comet_opik-20260618`
Lane: `paid_code_bounties`

Purpose: create a claim-readiness checklist and duplicate-risk worksheet for the Comet Opik -> Algora route without claiming, commenting, opening a PR, accepting a CLA, touching payout/account surfaces, or performing live GitHub/Algora actions.

## Decision

Go/no-go: `no_go_external_claim`

Reason: Comet/Opik bounty program is currently paused in the public docs; local fixtures remain useful for parser/checklist readiness, but no claim/comment/PR/payout path is clean.

Local next step: Keep the Algora parser fixture and duplicate worksheet as the readiness base; if the program reopens, run one approved read-only refresh before any local triage sprint.

## Source Observations

| Source | URL | Observation | Claim-Readiness Effect |
| --- | --- | --- | --- |
| `comet_opik_bounty_docs` | https://www.comet.com/docs/opik/contributing/developer-programs/bounties | The Opik bounty page says the bounty program is currently paused until further notice, while preserving reference instructions for CLA, contribution guide, Algora board, claim-if-applicable, PR submission, and reward flow. | Route is not externally actionable until the pause is lifted and a fresh read-only validation confirms an open bounty. |
| `algora_home` | https://algora.io/ | Algora public site presents open-source recruiting and bounty surfaces with sign-in and public bounty examples. | Algora/account/payment/public action remains gated; public pages can inform local fixture shape only. |
| `local_algora_fixture_checker` | E:/agent-company-lab/reports/paid-code-bounties/algora-candidate-refresh-fixture-check-20260616.md | No-network fixture checker validated six candidate rows with six passes and zero failures. | Local parser/checklist machinery is ready for read-only refresh, but not for claim/comment/PR/payout. |
| `local_duplicate_check_worksheet` | E:/agent-company-lab/reports/paid-code-duplicate-check-worksheet-latest.md | Existing worksheet separates six local duplicate/payout/effort checks from browser, legal/payment, public-action, and security gates. | New route should reuse these local-only checks and forbid live actions until approvals exist. |

## Candidate Rows From Local Fixture

| Fixture | Amount | State | Claims | Testability | Decision | Readiness | Gate |
| --- | ---: | --- | ---: | --- | --- | --- | --- |
| `algora_org_examples_reference_only` |  | `unclear` |  | `blocked` | `reference_only` | `reference_only` | No candidate issue; use only to verify parser shape. |
| `golemcloud_zero_open_watchlist` |  | `none_open` |  | `blocked` | `watchlist` | `watchlist_only` | Wait for an explicit open bounty before local triage. |
| `capsoftware_low_amount_crowded_reject` | 50 | `open` | 5 | `clear` | `reject` | `reject` | Do not spend sprint time on low-value crowded bounty. |
| `turso_unclear_amount_watchlist` |  | `unclear` |  | `unclear` | `watchlist` | `watchlist_only` | Read-only refresh required for explicit amount and acceptance state. |
| `prettier_clear_local_triage_candidate` | 250 | `open` | 1 | `clear` | `promote_local_triage` | `local_triage_only` | Local triage only; no claim, comment, PR, or payout details without GitHub/public-action approval. |
| `tsperf_subjective_acceptance_reject` | 300 | `open` | 0 | `unclear` | `reject` | `reject` | Reject until measurable acceptance target exists. |

## Readiness Gates

| Gate | Status | Required Evidence |
| --- | --- | --- |
| `program_open_check` | `blocked_by_pause` | Fresh read-only source confirms Opik bounty program is no longer paused and the target bounty is open. |
| `cla_and_contribution_review` | `approval_required` | CLA/contribution guide reviewed locally; no agreement accepted without explicit approval. |
| `duplicate_and_claim_check` | `approval_required_for_live_refresh` | Read-only issue/PR/comment/claim scan shows low duplicate risk and clear reservation rules. |
| `local_reproduction` | `local_only_allowed` | Repro steps and tests run on local fixture or cloned public repo only after repo access is approved/safe. |
| `public_claim_or_pr` | `blocked` | Exact public-action approval for a specific issue, claim/comment text, branch/PR body, and receipt. |
| `payout_terms` | `blocked` | Legal/KYC/tax/payment review of bounty terms and payout route. |

## Claim-Readiness Checklist

- Confirm program is active, not paused.
- Confirm explicit bounty amount before work starts.
- Confirm issue is open, unsolved, and still accepting work.
- Confirm claim/reservation rules and competing claims.
- Confirm CLA/contribution requirements without accepting anything.
- Confirm local reproduction and deterministic acceptance target.
- Reject tiny/crowded, subjective, credential-requiring, or unclear acceptance tasks.
- Draft public claim/PR text only after exact public-action approval.
- Keep payout/tax/KYC/account setup behind legal/payment approval.

## Boundary

No live Algora fetch, live GitHub fetch, account/login, CLA or terms acceptance, GitHub comment, bounty claim, PR, fork, payout/payment action, security testing, service-request mutation, worker/runtime start, model/MCP/external API call, or other external side effect occurred.

## Next Action

Park external Algora/Comet claim work until the Opik bounty program is verified active by an approved read-only refresh; then re-run duplicate/claim/payout checks before any public claim, comment, PR, account, CLA, or payout action.
