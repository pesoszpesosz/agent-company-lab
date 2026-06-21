# Runtime Start Apply Preflight Blocker v1

Generated UTC: 2026-06-21T15:44:18Z
Guard validation: `E:\agent-company-lab\reports\runtime-start-signed-decision-guard-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\runtime-start-apply-preflight-blocker-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\runtime-start-apply-preflight-blocker-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Apply preflight status: `blocked_no_real_signed_decision`
- Blocker reason: `no_real_signed_operator_decision_artifact`
- Real signed decision present: `False`
- Apply allowed: `False`
- Runtime start allowed: `False`
- Worker start allowed: `False`
- Runtime processes started: `0`
- External side effects: `False`

## Checks

| Check | Passed | Detail |
| --- | --- | --- |
| `guard_validation_passes` | `True` | E:\agent-company-lab\reports\runtime-start-signed-decision-guard-v1-validation-20260617.json |
| `guard_does_not_allow_runtime_start` | `True` | Guard accepts authority for later preflight only. |
| `real_signed_decision_absent` | `True` | No real signed operator runtime-start decision artifact was supplied. |

## Boundary

- This blocker writes reports only.
- It writes no apply command and executes no command.
- Accepted guard fixtures are not real signed operator decisions.
