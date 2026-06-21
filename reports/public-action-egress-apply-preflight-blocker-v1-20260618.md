# Public Action Egress Apply Preflight Blocker v1

Generated UTC: 2026-06-21T15:44:16Z
Target route: `public_action_gateway`
Report JSON: `E:\agent-company-lab\reports\public-action-egress-apply-preflight-blocker-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\public-action-egress-apply-preflight-blocker-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Apply preflight status: `blocked_no_real_signed_decision`
- Blocker reason: `no_real_signed_operator_public_action_egress_decision_artifact`
- Real signed decision present: `False`
- Exact action-body approval present: `False`
- Apply command contract present: `False`
- Public action allowed: `False`
- Public actions: `False`
- Posts created: `0`
- Forms submitted: `0`
- PRs opened: `0`
- Bounty claims: `0`
- Messages sent: `0`
- Browser session start allowed: `False`
- Browser sessions started: `0`
- Account actions: `False`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `False`

## Checks

| Check | Passed | Detail |
| --- | --- | --- |
| `gateway_docket_validation_passes` | `True` | E:\agent-company-lab\reports\unified-agent-egress-gateway-docket-v1-validation-20260618.json |
| `signed_decision_intake_validation_passes` | `True` | E:\agent-company-lab\reports\egress-route-signed-decision-intake-contract-v1-validation-20260618.json |
| `public_action_signed_decision_guard_passes_for_target_route` | `True` | E:\agent-company-lab\reports\public-action-egress-signed-decision-guard-v1-validation-20260618.json |
| `agent_egress_event_ledger_validation_passes` | `True` | E:\agent-company-lab\reports\agent-egress-event-ledger-v1-validation-20260617.json |
| `service_worker_chain_integrity_passes_without_start` | `True` | E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json |
| `real_signed_decision_absent` | `True` | No real signed operator public-action egress-route decision artifact was supplied. |
| `exact_action_body_approval_absent` | `True` | No exact action-body approval packet was supplied. |
| `public_action_apply_command_contract_absent` | `True` | No public_action_gateway apply-command contract exists yet. |

## Boundary

- This blocker writes no apply command and executes no command preview.
- Public actions remain blocked until a real signed decision, exact action-body approval, and apply-command contract exist.
- No post, form submission, PR, bounty claim, message send, browser mutation, account action, service-request mutation, worker start, or live egress is allowed.

Next action: Provide a real signed operator public_action_gateway decision artifact, exact action-body approval, and public-action apply-command contract before any post, form submission, PR, bounty claim, message send, browser mutation, account action, service-request mutation, or live egress can be considered.
