# OptimismPortal l2Sender Fixture Plan v1

Generated UTC: 2026-06-17T22:12:32Z

Lane: `security_bounty_private_reports`

Task: `task-optimism-portal-l2sender-fixture-plan-v1-20260618`

Status: report-only fixture plan. No patch, no local upstream test execution, no report submission.

## Purpose

Convert the previous `opi-007` no-finding invariant memo into a concrete local regression fixture plan. The target invariant is that `optimismPortal2.l2Sender()` returns `Constants.DEFAULT_L2_SENDER` after every relevant withdrawal finalization path.

## Current Source Snapshot

- `OptimismPortal2.sol`: 789 lines, SHA-256 `B541EF7166AF8CD177F64324571E642D9C511AB8C7441268B096954C5F3E464F`, source https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/src/L1/OptimismPortal2.sol
- `OptimismPortal2.t.sol`: 2724 lines, SHA-256 `FF9721FAD3CED4B7FBE7CE1B008EBD41897C2B3457F1D4E45EC0C209A28E3935`, source https://raw.githubusercontent.com/ethereum-optimism/optimism/refs/heads/develop/packages/contracts-bedrock/test/L1/OptimismPortal2.t.sol

Key production anchor: `OptimismPortal2.sol` lines 556-560 guard against reentrancy, lines 582-595 set and reset `l2Sender`, and lines 609-613 may revert for gas estimation after the reset branch.

## Fixture Rows

| ID | Case | Existing Test Anchor | Proposed Insertion | Assertion |
| --- | --- | --- | --- | --- |
| `opl2sf-001` | successful empty-data finalization | `test_finalizeWithdrawalTransaction_noTxData_succeeds` lines 1276-1335 | after line 1332 | `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);` |
| `opl2sf-002` | target failure without gas-estimation origin | `test_finalizeWithdrawalTransaction_targetFails_fails` lines 1538-1561 | after line 1552 | `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);` |
| `opl2sf-003` | target failure with gas-estimation origin | `test_finalizeWithdrawalTransaction_targetFailsAndCallerIsEstimationAddress_reverts` lines 1255-1273 | after line 1272 | `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);` |
| `opl2sf-004` | insufficient gas revert | `test_finalizeWithdrawalTransaction_onInsufficientGas_reverts` lines 1629-1675 | after line 1674 | `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);` |
| `opl2sf-005` | nested finalize reentrancy attempt | `test_finalizeWithdrawalTransaction_onReentrancy_reverts` lines 1677-1732 | after line 1728 | `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);` |
| `opl2sf-006` | external-proof finalization by secondary proof submitter | `test_finalizeWithdrawalTransaction_secondProofReplay_reverts` lines 2118-2164 | after line 2158 | `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);` |

## Patch Design

- Target file: `packages/contracts-bedrock/test/L1/OptimismPortal2.t.sol`.
- Add one explicit post-state assertion to each existing fixture; do not add a helper unless repeated assertion style becomes noisy during approved patch materialization.
- Preferred assertion: `assertEq(optimismPortal2.l2Sender(), Constants.DEFAULT_L2_SENDER);`.
- Start with the normal success path after line 1332, then cover failed target, gas-estimation revert, insufficient-gas revert, nested reentrancy, and external-proof finalization.

## Gate Status

- Submission-ready rows: 0.
- Local upstream patch materialization requires explicit user approval.
- Local upstream test execution requires explicit user approval.
- Any private report route still requires the security report submission gate.

## Boundary

Report-only. No clone, no upstream patch application, no fork execution, no live target testing, no browser work, no account registration, no service-worker assignment, no runtime start, no private report submission, no public disclosure, no wallet action, no payment action, and no external side effect.

## Next Action

Only after explicit approval, materialize a local patch file and run local upstream tests; do not submit or test live targets.
