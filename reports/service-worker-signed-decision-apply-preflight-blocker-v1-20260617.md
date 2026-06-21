# Service Worker Signed Decision Apply Preflight Blocker v1

Generated UTC: 2026-06-21T15:49:45Z
Guard validation: `E:\agent-company-lab\reports\service-worker-signed-decision-guard-v1-validation-20260617.json`
Intake validation: `E:\agent-company-lab\reports\service-worker-signed-decision-intake-contract-v1-validation-20260617.json`
Authority validation: `E:\agent-company-lab\reports\service-worker-approval-authority-coverage-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\service-worker-signed-decision-apply-preflight-blocker-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\service-worker-signed-decision-apply-preflight-blocker-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Apply preflight status: `blocked_no_real_signed_decision`
- Blocker reason: `no_real_signed_operator_decision_artifact`
- Real signed decision present: `False`
- Apply allowed: `False`
- Decision apply allowed: `False`
- Assignment allowed: `False`
- Worker start allowed: `False`
- Service templates: `13`
- Current service requests: `16`
- External side effects: `False`

## Checks

| Check | Passed | Detail |
| --- | --- | --- |
| `signed_decision_guard_passes` | `True` | E:\agent-company-lab\reports\service-worker-signed-decision-guard-v1-validation-20260617.json |
| `guard_is_not_apply_authority` | `True` | The signed-decision guard may accept fixtures only for a later apply preflight. |
| `intake_contract_passes_without_authority` | `True` | E:\agent-company-lab\reports\service-worker-signed-decision-intake-contract-v1-validation-20260617.json |
| `authority_coverage_passes_without_grant` | `True` | E:\agent-company-lab\reports\service-worker-approval-authority-coverage-v1-validation-20260617.json |
| `real_signed_decision_absent` | `True` | No real signed operator service-worker decision artifact was supplied. |

## Boundary

- This blocker writes reports only.
- It writes no apply command and executes no command.
- It assigns or updates no service requests.
- It starts no workers, browsers, MCP servers, runtimes, model calls, API calls, wallet actions, payments, public actions, or security submissions.
- Accepted guard fixtures are not real signed operator decisions.
