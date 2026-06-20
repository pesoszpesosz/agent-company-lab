# OptimismPortal Invariant Memo v1

Generated UTC: 2026-06-17T22:04:11Z

Lane: `security_bounty_private_reports`

Task: `task-optimism-portal-invariant-memo-v1-20260618`

Selected asset: `optimism-sc-005` / `OptimismPortal`

Selected invariant: `opi-007` / `l2Sender` guard and reset

## Conclusion

This is not a vulnerability finding and it is not submission-ready.

The source and upstream tests show a deliberate `l2Sender` reentrancy guard and reset pattern. The useful next local task is a hardening/regression fixture plan: add explicit post-state assertions that `l2Sender` is `Constants.DEFAULT_L2_SENDER` after each finalization path.

## Source Snapshot

- `OptimismPortal2.sol`: SHA-256 `B541EF7166AF8CD177F64324571E642D9C511AB8C7441268B096954C5F3E464F`
- `OptimismPortal2.t.sol`: SHA-256 `FF9721FAD3CED4B7FBE7CE1B008EBD41897C2B3457F1D4E45EC0C209A28E3935`

## Source Observations

- `OptimismPortal2.sol` lines 556-560 check `l2Sender` before the external target call and revert with `OptimismPortal_NoReentrancy` when it is not default.
- Lines 582-595 set `l2Sender` to the L2 withdrawal sender before `SafeCall.callWithMinGas` and reset it immediately after the call returns.
- Lines 597-614 emit `WithdrawalFinalized` after reset and may then revert only for the special gas-estimation origin when the target call failed.
- `OptimismPortal2.t.sol` lines 1677-1731 include a target-call reentrancy test that expects `OptimismPortal_NoReentrancy`.

## State Matrix

| Case | Path | Expected Exit | Gap |
| --- | --- | --- | --- |
| `opi007-case-001` | successful finalize | `l2Sender == DEFAULT_L2_SENDER` | Add explicit post-state assertion. |
| `opi007-case-002` | target returns false | `l2Sender == DEFAULT_L2_SENDER` | Add explicit post-state assertion. |
| `opi007-case-003` | target returns false with gas-estimation origin | transaction reverts and persisted state remains default | Add explicit assertion after expected revert. |
| `opi007-case-004` | insufficient gas revert | transaction reverts and persisted state remains default | Add explicit assertion after expected revert. |
| `opi007-case-005` | nested finalize during target call | nested call reverts; outer call can finish | Add explicit post-state assertion after outer call. |
| `opi007-case-006` | external-proof finalization | `l2Sender == DEFAULT_L2_SENDER` | Add explicit post-state assertion. |

## Local Fixture Plan

Future local fixture name: `OptimismPortal2_l2Sender_postcondition_fixture`

Candidate assertions:

1. Assert default `l2Sender` after successful `finalizeWithdrawalTransaction`.
2. Assert default `l2Sender` after failed-target finalization that emits `WithdrawalFinalized(false)`.
3. Assert default `l2Sender` after gas-estimation revert.
4. Assert default `l2Sender` after insufficient-gas revert.
5. Assert default `l2Sender` after the reentrancy test outer finalization.
6. Assert default `l2Sender` after `finalizeWithdrawalTransactionExternalProof`.

## Gate Status

- Duplicate matrix: no finding, no duplicate claim.
- Quality gate: not applicable until a concrete finding exists.
- Impact claim: none.
- Submission-ready rows: 0.

## Boundary

Report-only. No fork execution, no live target testing, no browser work, no account registration, no service-worker assignment, no runtime start, no private report submission, no public disclosure, no wallet action, no payment action, and no external side effect.
