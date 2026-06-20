# Immunefi Directory Scope Shortlist v1

Generated UTC: 2026-06-17T21:31:00Z
Task: `task-immunefi-directory-scope-shortlist-v1-20260618`
Lane: `security_bounty_private_reports`

## Purpose

Convert the current Immunefi directory scan into a local-only shortlist for rules and scope extraction. This is not target testing, exploit work, account work, KYC, or report submission.

## Source Signals

- Immunefi directory: `https://immunefi.com/bug-bounty/`
- Directory observed update signal: metrics updated daily; page showed Jun 17th 2026 at 16:00 UTC.
- Candidate pages checked: Optimism, ENS, Lido, Immutable, Lista DAO, Sei, Drips, Immunefi, and Obyte.

## Ranking

| Rank | Program | Max Bounty | Last Updated | Score | Verdict | Next Local Proof |
| ---: | --- | ---: | --- | ---: | --- | --- |
| 1 | Optimism | $2,000,042 | 2026-06-16 | 91 | `promote_rules_extraction_first` | `optimism_scope_rules_extraction_packet_v1` |
| 2 | ENS | $250,000 | 2026-06-17 | 88 | `promote_known_issue_safe_rules_packet` | `ens_scope_known_issues_matrix_v1` |
| 3 | Lido | $2,000,000 | 2026-03-26 | 84 | `promote_rules_extraction_but_high_duplicate_risk` | `lido_scope_rules_extraction_packet_v1` |
| 4 | Immutable | $1,000,000 | 2026-01-29 | 81 | `promote_audit_gap_matrix_after_optimism_ens_lido` | `immutable_contract_audit_gap_matrix_v1` |
| 5 | Lista DAO | $1,000,000 | 2026-05-29 | 76 | `watch_and_extract_scope_before_any_target_work` | `lista_dao_scope_page_extraction_v1` |
| 6 | Sei | $500,000 | 2026-06-16 | 74 | `promote_after_contract_first_candidates` | `sei_chain_scope_rules_packet_v1` |
| 7 | Drips | $100,000 | 2024-11-18 | 71 | `good_low_kyc_rules_training_target` | `drips_audit_known_issue_diff_packet_v1` |
| 8 | Immunefi | $50,000 | 2025-11-17 | 64 | `use_as_rules_training_not_primary_cashflow` | `immunefi_platform_scope_training_packet_v1` |
| 9 | Obyte | $50,000 | 2026-06-15 | 58 | `park_low_ev_until_specific_static_signal_exists` | `obyte_impact_threshold_packet_v1` |

## Decision

Promote Immunefi rules and scope extraction only. There are zero submission-ready rows. The next useful proof is `optimism_scope_rules_extraction_packet_v1`, paired with `security_report_quality_gate_v1`, so every later target-specific claim has a quality, duplicate, scope, and allowed-proof gate before any external action.

## Required Gates

- `browser_read_only_session` before live browser refresh or signed-in page capture.
- `security_report_submission_gate` before any private report or platform submission.
- `legal_kyc_tax_payment_gate` for KYC, payout, tax, account-contract, or eligibility work.
- `wallet_public_address_or_payment_reply` before any payout address or payment response.

## Boundary

- Browser sessions started: `0`
- Accounts registered: `0`
- Service requests assigned/updated: `0` / `0`
- Worker starts/runtime starts: `0` / `0`
- Security tests: `False`
- Private reports submitted: `0`
- Public actions: `False`
- Wallet/payment actions: `False` / `False`
- External side effects: `False`
