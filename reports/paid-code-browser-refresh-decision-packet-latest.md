# Paid-Code Browser Refresh Decision Packet

Generated UTC: 2026-06-15T20:55:45Z
JSON mirror: `E:\agent-company-lab\reports\paid-code-browser-refresh-decision-packet-latest.json`
Validation: `E:\agent-company-lab\reports\paid-code-browser-refresh-decision-packet-validation-latest.json`

## Request

- Request: `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614`
- Status: `needs_review`
- Lane: `paid_code_bounties`
- Service: `browser_read_only_session`
- Risk gate: `catalog_required_approval_no_external_action`

## Exact Read-Only Scope

| Scope | Description |
| --- | --- |
| `issue-open-state` | Read the target issue/bounty page to confirm whether it is open and still accepting new work. |
| `claim-and-pr-state` | Read comments, linked PRs, and claim indicators to detect active or accepted duplicate work. |
| `bounty-terms-snapshot` | Read visible bounty terms, payout wording, attribution requirements, and account/payment caveats without accepting anything. |
| `repo-readiness-snapshot` | Read public repo metadata, language/tooling hints, test/build docs, and recent activity to estimate local effort. |
| `refresh-outcome-note` | Write a local refresh outcome note that updates go/no-go status; do not claim, comment, fork, or submit. |

## Forbidden Actions

- Do not sign in, register, accept terms, or change account settings.
- Do not claim a bounty, comment, open a PR, fork for submission, contact maintainers, or make any public action.
- Do not upload files, download gated/private data, or disclose private/user data.
- Do not perform security testing, exploit validation, scanning, fuzzing, or proof-of-concept execution.
- Do not touch wallets, payments, payout settings, KYC, tax forms, deposits, withdrawals, or real-money flows.
- Do not call model/API providers, assign service workers, start workers, or mutate service requests from this packet.

## Decision State

- Approval required: `true`
- Decision granted: `false`
- Decision rejected: `false`

## Next Action

Human/CRO may approve, reject, or keep parked. If approved later, rerun service-worker scope diff, assignment, readiness, and chain integrity before any worker starts.

