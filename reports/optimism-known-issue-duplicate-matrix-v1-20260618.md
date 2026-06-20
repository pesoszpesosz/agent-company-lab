# Optimism Known-Issue Duplicate Matrix v1

Generated UTC: 2026-06-17T22:04:00Z
Task: `task-optimism-known-issue-duplicate-matrix-v1-20260618`
Lane: `security_bounty_private_reports`

## Purpose

Create a mandatory duplicate and out-of-scope filter for any future Optimism candidate before code review, local proof planning, report drafting, or submission.

## Source Signals

- Optimism Immunefi information page lists known issues for Smart Contract and Blockchain/DLT, both last updated 2025-06-12.
- Optimism Immunefi scope page lists program-specific out-of-scope rules for Blockchain/DLT, Smart Contracts, Web & App, and default out-of-scope rules.
- The same pages prohibit mainnet/public testnet testing, third-party/oracle testing, phishing/social engineering, denial of service, automated traffic, and public disclosure.

## Summary

| Metric | Count |
| --- | ---: |
| Controls | 21 |
| Hard stops | 9 |
| Duplicate checks | 2 |
| Upstream route checks | 1 |
| Submission-ready rows | 0 |

## Mandatory Controls

| ID | Area | Decision | Required Check |
| --- | --- | --- | --- |
| `optimism-dup-001` | Smart Contract | `duplicate_check_required` | Compare against Optimism smart-contract known issues. |
| `optimism-dup-002` | Blockchain/DLT | `duplicate_check_required` | Compare against Optimism Blockchain/DLT known issues. |
| `optimism-dup-003` | Blockchain/DLT | `upstream_route_check_required` | Check upstream reth and Ethereum Foundation status before op-reth promotion. |
| `optimism-dup-004` | Blockchain/DLT | `hard_stop_until_cleared` | Compare networking/devp2p claims against Ethereum devp2p known issues. |
| `optimism-dup-005` | Blockchain/DLT | `hard_stop` | Reject public JSON-RPC or Beacon API exposure dependency. |
| `optimism-dup-006` | Blockchain/DLT | `hard_stop` | Reject chain-operator best-practice or network-topology-only claims. |
| `optimism-dup-007` | Blockchain/DLT | `hard_stop` | Reject Alt-DA feature claims for op-node or op-batcher. |
| `optimism-dup-008` | Blockchain/DLT | `hard_stop` | Reject end-of-service execution clients such as op-geth. |
| `optimism-dup-009` | Smart Contract | `hard_stop_for_third_party_bridge_only` | Separate canonical bridge behavior from third-party custom token bridge bugs. |
| `optimism-dup-010` | Smart Contract | `hard_stop_if_detected_by_op_dispute_mon` | Prove dispute-game issue is not already detected/resolved by op-dispute-mon. |
| `optimism-dup-011` | Smart Contract | `hard_stop` | Reject proof-of-whale based attacks on Fault Proofs. |
| `optimism-dup-012` | Smart Contract | `hard_stop_unless_new_bypass` | Reject fake ERC20 bridge issue restatement without new bypass. |
| `optimism-dup-013` | Smart Contract | `hard_stop_unless_new_affected_layout` | Reject ResolvedDelegateProxy storage-slot non-impact restatement. |
| `optimism-dup-014` | Smart Contract | `hard_stop_unless_distinct_new_impact` | Reject documented L1 contract deposit edge case restatement. |
| `optimism-dup-015` | Smart Contract | `hard_stop_unless_new_impact` | Reject large-data/gas griefing restatement without new impact. |
| `optimism-dup-016` | Smart Contract | `hard_stop_unless_new_bypass` | Reject MAX_RESOURCE_LIMIT griefing restatement without new bypass. |
| `optimism-dup-017` | Smart Contract | `hard_stop_for_configuration_foot_gun` | Reject user/developer/token bridge configuration foot guns. |
| `optimism-dup-018` | Web & App | `browser_and_scope_gate_required` | Confirm web asset is in scope and not out of scope before review. |
| `optimism-dup-019` | All categories | `quality_gate_required` | Pass default out-of-scope filters before draft report. |
| `optimism-dup-020` | All categories | `hard_stop_for_autonomous_agent` | No live testing without local-fork/runtime/browser/submission gates. |
| `optimism-dup-021` | All categories | `quality_gate_required` | Include feasibility and downgrade-risk notes before draft report. |

## Decision

No Optimism candidate is ready for target-specific code review, local proof execution, or submission. The next local proof should be `security_report_quality_gate_v1`, then an `optimism_local_review_candidate_filter_v1` that uses this matrix as a pre-code-review blocker.

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
