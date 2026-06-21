# Browser Read-Only Apply Preflight Blocker v1

Generated UTC: 2026-06-21T15:49:33Z
Guard validation: `E:\agent-company-lab\reports\browser-read-only-signed-approval-guard-v1-validation-20260617.json`
Assignment preflight validation: `E:\agent-company-lab\reports\browser-read-only-assignment-preflight-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\browser-read-only-apply-preflight-blocker-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\browser-read-only-apply-preflight-blocker-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Apply preflight status: `blocked_no_real_signed_decision`
- Blocker reason: `no_real_signed_operator_decision_artifact`
- Real signed decision present: `False`
- Guard adapter contract gate: `present_valid_start_blocked`
- Guard adapter contract validation: `E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-validation-20260618.json`
- Apply allowed: `False`
- Assignment allowed: `False`
- Browser session start allowed: `False`
- Worker start allowed: `False`
- Candidate requests: `9`
- External side effects: `False`

## Checks

| Check | Passed | Detail |
| --- | --- | --- |
| `signed_approval_guard_passes` | `True` | E:\agent-company-lab\reports\browser-read-only-signed-approval-guard-v1-validation-20260617.json |
| `guard_does_not_allow_assignment_or_browser_start` | `True` | Guard accepts authority for later preflight only. |
| `signed_guard_adapter_contract_gate_present_valid_start_blocked` | `True` | E:\agent-company-lab\reports\browser-worker-adapter-contract-v1-validation-20260618.json |
| `assignment_preflight_still_blocks_without_signed_approval` | `True` | E:\agent-company-lab\reports\browser-read-only-assignment-preflight-v1-validation-20260617.json |
| `real_signed_decision_absent` | `True` | No real signed operator browser-read-only decision artifact was supplied. |

## Boundary

- This blocker writes reports only.
- It writes no apply command and executes no command.
- It assigns no service requests and opens no browser sessions.
- Accepted guard fixtures are not real signed operator decisions.
