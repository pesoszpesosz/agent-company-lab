# Security Report Quality Gate v1

Generated UTC: 2026-06-17T21:54:02Z

Lane: `security_bounty_private_reports`

Task: `task-security-report-quality-gate-v1-20260618`

## Purpose

This packet defines the local gate a future Optimism security candidate must pass before code review, report drafting, or any submission packet. It is report-only and grants no authority to test targets, register accounts, submit reports, post publicly, touch wallets, or request payment details.

## Source Basis

- Immunefi report guidance: high-quality reports need clear title, description, impact, risk breakdown, recommendation, references, and runnable PoC evidence.
- Immunefi platform rules: mainnet/public-testnet testing, misrepresenting scope/severity/impact, duplicate reports, placeholder reports, public disclosure, and incomplete PoCs where required are disqualifying risks.
- Immunefi severity v2.3: severity is impact-centered, with downgrades or rejection possible when exploitability relies on elevated privileges or uncommon user interaction.
- Optimism program pages: candidate reports must map to current program assets, impacts, known issues, out-of-scope rows, PoC requirements, KYC/payment notes, and responsible-publication rules.

## Hard Stops

- Affected asset is not mapped to the Optimism asset scope table.
- Claimed impact is not mapped to an in-scope Optimism impact and Immunefi severity class.
- Candidate overlaps known issues, duplicate routes, upstream-only routes, public disclosures, or out-of-scope rows.
- Proof depends on mainnet, public testnet, automated target traffic, DoS, phishing, social engineering, or third-party systems.
- Candidate suggests public disclosure, GitHub issue, social post, or report submission before exact approval.
- No exact approved `security_report_submission_gate` service request exists.
- Side-effect audit shows any unapproved browser/account/service-request/worker/runtime/security-test/report/public/wallet/payment/external action.

## Required Candidate Inputs

1. Affected asset and Optimism scope category.
2. Impact mapping and Immunefi v2.3 severity claim.
3. Duplicate-matrix notes for every relevant known-issue/out-of-scope row.
4. Runnable local PoC plan or local PoC result with commands, fixtures, output, and failure mode.
5. Preconditions, attacker capabilities, timing assumptions, and privilege requirements.
6. Economic impact estimate and maximum plausible damage.
7. Root cause, vulnerable code path, and remediation direction.
8. Report-quality structure: title, summary, details, impact, risk breakdown, PoC, recommendation, references, and scope notes.
9. KYC/payout awareness without collecting personal/payment data.
10. Responsible-publication and submission-approval guard.

## Validation

- Gate rows: 17
- Hard-stop rows: 7
- Submission-ready rows: 0
- Boundary: report-only, no side effects

## Next Action

Build `optimism_local_review_candidate_filter_v1` from the Optimism asset scope table, duplicate matrix, and this report-quality gate. Do not perform target-specific code review, runtime testing, private report drafting, or external submission before that filter exists.
