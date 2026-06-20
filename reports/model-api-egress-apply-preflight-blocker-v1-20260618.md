# Model API Egress Apply Preflight Blocker v1

Generated UTC: 2026-06-20T21:07:35Z
Target route: `model_api_gateway`
Guard validation: `E:\agent-company-lab\reports\model-api-egress-signed-decision-guard-v1-validation-20260618.json`
Egress ledger validation: `E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json`
Identity validation: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\model-api-egress-apply-preflight-blocker-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\model-api-egress-apply-preflight-blocker-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Apply preflight status: `blocked_no_real_signed_decision`
- Blocker reason: `no_real_signed_operator_model_api_egress_decision_artifact`
- Real signed decision present: `False`
- Apply command contract present: `False`
- Apply allowed: `False`
- Provider key use allowed: `False`
- Provider keys used: `False`
- Model/API call allowed: `False`
- Model/API calls: `False`
- Training data upload allowed: `False`
- Training data uploaded: `False`
- Max cost USD: `0`
- Worker start allowed: `False`
- External side effects: `False`

## Checks

| Check | Passed | Detail |
| --- | --- | --- |
| `gateway_docket_validation_passes` | `True` | E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-validation-20260618.json |
| `signed_decision_intake_validation_passes` | `True` | E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-validation-20260618.json |
| `model_api_signed_decision_guard_passes_for_target_route` | `True` | E:\agent-company-lab\reports\model-api-egress-signed-decision-guard-v1-validation-20260618.json |
| `agent_egress_event_ledger_validation_passes` | `True` | E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json |
| `identity_envelope_validation_passes` | `True` | E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json |
| `real_signed_decision_absent` | `True` | No real signed operator model/API egress-route decision artifact was supplied. |
| `model_api_apply_command_contract_absent` | `True` | No model/API egress apply-command contract exists yet. |

## Boundary

This blocker writes reports only. It writes no apply command, executes no command, uses no provider key, calls no model/API, uploads no data, spends no money, starts no worker, mutates no service request, and performs no live egress.

Next action: Provide a real signed operator model/API egress-route decision artifact, then build a model/API apply-command contract before any provider key use, model/API call, data upload, worker start, service-request mutation, or live egress can be considered.
