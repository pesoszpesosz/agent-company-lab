# Runtime Implementation Signed Decision Guard v1

Generated UTC: 2026-06-20T11:17:46Z
Source approval packet: `E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-human-approval-packet-v2-20260617.json`
Guard report JSON: `E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-signed-decision-guard-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-signed-decision-guard-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\runtime-implementation-signed-decision-guard-v1.schema.json`

## Summary

- All checks passed: `True`
- Fixture count: `19`
- Accepted fixtures: `2`
- Rejected fixtures: `17`
- Decisions applied: `0`
- Runtime implementation allowed: `False`
- Runtime code write allowed: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_all` | `accepted` | `True` | `True` |  |
| `positive_sqlite_control_plane_report_only` | `accepted` | `True` | `True` |  |
| `negative_missing_approver` | `rejected` | `False` | `True` | approver_empty |
| `negative_expired_decision` | `rejected` | `False` | `True` | expires_not_after_signed, decision_expired |
| `negative_unknown_runtime` | `rejected` | `False` | `True` | selected_runtime_not_in_source_candidates |
| `negative_multiple_runtime_tokens` | `rejected` | `False` | `True` | selected_runtime_must_be_single_id, selected_runtime_not_in_source_candidates |
| `negative_approved_without_runtime_question` | `rejected` | `False` | `True` | approval_missing_approve_runtime_candidate_question |
| `negative_dependency_without_names` | `rejected` | `False` | `True` | dependency_install_scope_requires_exact_dependency_names |
| `negative_wildcard_dependency` | `rejected` | `False` | `True` | dependency_names_must_not_be_wildcard |
| `negative_runtime_start_without_process` | `rejected` | `False` | `True` | runtime_start_scope_requires_exact_processes |
| `negative_wildcard_service_request_mutation` | `rejected` | `False` | `True` | service_request_mutation_scope_must_not_be_wildcard |
| `negative_model_api_without_cost_cap` | `rejected` | `False` | `True` | model_api_approval_requires_provider_model_and_cost_cap |
| `negative_browser_public_action_approved` | `rejected` | `False` | `True` | browser_public_actions_forbidden_in_runtime_guard |
| `negative_wallet_real_money_approved` | `rejected` | `False` | `True` | wallet_payment_real_money_forbidden_in_runtime_guard |
| `negative_security_testing_approved` | `rejected` | `False` | `True` | security_testing_forbidden_in_runtime_guard |
| `negative_non_top_runtime_without_rationale` | `rejected` | `False` | `True` | non_top_runtime_requires_non_top_rationale |
| `negative_missing_rollback_plan` | `rejected` | `False` | `True` | approval_requires_specific_rollback_plan |
| `negative_overlapping_question_ids` | `rejected` | `False` | `True` | overlapping_question_ids:approve_runtime_candidate |
| `negative_missing_attestation` | `rejected` | `False` | `True` | approval_signature_attestation_missing_or_wrong |

## Guard Boundary

- Accepted decisions are accepted for later preflight only.
- This guard applies no approval, writes no approval rows, installs no dependencies, starts no runtime/server/worker, mutates no service request, opens no browser, calls no API/model, performs no public/account/wallet/payment/security/real-money action, and has no external side effects.
- Browser/public, wallet/payment/real-money, and security-testing approvals are rejected here because those require separate lane-specific service gates.
