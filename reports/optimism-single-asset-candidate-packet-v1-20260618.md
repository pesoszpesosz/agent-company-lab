# Optimism Single-Asset Candidate Packet v1

Generated UTC: 2026-06-17T22:00:11Z

Lane: `security_bounty_private_reports`

Task: `task-optimism-single-asset-candidate-packet-v1-20260618`

## Selection

Selected asset: `optimism-sc-005` / `OptimismPortal`

Implementation focus: `OptimismPortal2`

Selected filter: `olf-001` / local smart-contract invariant review

This is not a vulnerability finding and it is not submission-ready. It is a local review work order for one in-scope asset.

## Why This Asset

OptimismPortal is the OP Stack L1/L2 deposit and withdrawal interface. The OP Stack specification describes it as the primary portal for deposits and withdrawals and as the contract that checks withdrawal transactions against output roots declared valid by the fault proof system.

This asset is a better next local target than bridge foot-gun, public RPC, or governance/economic routes because the immediate work can stay inside public source review, invariant mapping, and local PoC planning.

## Source Snapshot

- Source: `https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/src/L1/OptimismPortal2.sol`
- Lines: 790
- SHA-256: `B541EF7166AF8CD177F64324571E642D9C511AB8C7441268B096954C5F3E464F`

## Known Duplicate Risk

A closed public issue documents the case where ETH sent directly to a portal implementation is not observed by the rollup node and can be stranded. Future work must not repackage this as a finding unless it proves a distinct new bypass, direct impact, and duplicate clearance.

## Review Invariants

1. `opi-001` - pause gate covers proof and finalization paths.
2. `opi-002` - unsafe targets remain blocked.
3. `opi-003` - dispute game eligibility is complete.
4. `opi-004` - output-root and withdrawal inclusion proof data are bound correctly.
5. `opi-005` - proof submitter isolation prevents one submitter from blocking another unexpectedly.
6. `opi-006` - replay protection is set before external target calls.
7. `opi-007` - `l2Sender` guard and reset hold across success/failure paths.
8. `opi-008` - ETHLockbox accounting handles failed withdrawal target calls.
9. `opi-009` - deposit gas/calldata/address-aliasing checks cover unpaid or misattributed resource usage.
10. `opi-010` - custom gas token mode blocks ETH value paths.

## Recommended First Work

Start with one of:

- `opi-007` because it is narrow, source-local, and tied to reentrancy and message-origin semantics.
- `opi-008` because ETHLockbox failure-path accounting is concrete and local-fixture friendly.

The next artifact should be `optimism_portal_invariant_memo_v1` for exactly one invariant group.

## Boundary

Report-only. No fork execution, no live target testing, no browser work, no account registration, no service-worker assignment, no runtime start, no private report submission, no public disclosure, no wallet action, no payment action, and no external side effect.
