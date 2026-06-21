# Local Runtime Adapter Pool Identity Envelope v1 Validation

Generated UTC: 2026-06-21T15:49:40Z
Contract design: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-contract-v1-20260617.json`
Schema: `E:\agent-company-lab\architecture\local-runtime-adapter-pool-identity-envelope-v1.schema.json`
Validation JSON: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json`
Report JSON: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-20260617.json`
Fixture directory: `E:\agent-company-lab\reports\local-runtime-adapter-pool-identity-envelope-v1-fixtures`

## Summary

- All checks passed: `True`
- Fixture count: `26`
- Accepted fixtures: `1`
- Rejected fixtures: `25`
- Registration allowed: `False`
- Assignment allowed: `False`
- Worker start allowed: `False`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_report_only_identity_candidate` | `accepted` | `True` | `True` |  |
| `negative_wrong_worker_pool_id` | `rejected` | `False` | `True` | worker_pool_id_mismatch |
| `negative_wrong_role_id` | `rejected` | `False` | `True` | role_id_mismatch |
| `negative_wrong_department_id` | `rejected` | `False` | `True` | department_id_mismatch |
| `negative_missing_operator_decision_artifact` | `rejected` | `False` | `True` | operator_decision_artifact_path_missing |
| `negative_operator_decision_claims_registration_approval` | `rejected` | `False` | `True` | operator_decision_must_not_claim_registration_approval |
| `negative_expired_identity_envelope` | `rejected` | `False` | `True` | expires_not_after_created, identity_envelope_expired |
| `negative_revoked_identity_envelope` | `rejected` | `False` | `True` | identity_envelope_not_active |
| `negative_allowed_runtime_mode_live` | `rejected` | `False` | `True` | allowed_runtime_modes_must_be_report_only_local_dry_run_only |
| `negative_allowed_egress_type_browser_read_only` | `rejected` | `False` | `True` | allowed_egress_types_must_be_empty |
| `negative_allowed_egress_type_model_api` | `rejected` | `False` | `True` | allowed_egress_types_must_be_empty |
| `negative_allowed_mcp_server_non_empty` | `rejected` | `False` | `True` | allowed_mcp_servers_must_be_empty |
| `negative_allowed_mcp_tool_non_empty` | `rejected` | `False` | `True` | allowed_mcp_tools_must_be_empty |
| `negative_credential_policy_allow` | `rejected` | `False` | `True` | credential_policy_must_be_deny |
| `negative_browser_session_policy_allow` | `rejected` | `False` | `True` | browser_session_policy_must_be_deny |
| `negative_network_policy_allow` | `rejected` | `False` | `True` | network_policy_must_be_deny |
| `negative_wallet_policy_allow` | `rejected` | `False` | `True` | wallet_policy_must_be_deny |
| `negative_payment_policy_allow` | `rejected` | `False` | `True` | payment_policy_must_be_deny |
| `negative_account_policy_allow` | `rejected` | `False` | `True` | account_policy_must_be_deny |
| `negative_public_action_policy_allow` | `rejected` | `False` | `True` | public_action_policy_must_be_deny |
| `negative_filesystem_writes_unbounded` | `rejected` | `False` | `True` | filesystem_policy_unbounded_writes_must_be_false, filesystem_policy_write_scope_must_not_be_wildcard |
| `negative_trace_event_required_false` | `rejected` | `False` | `True` | trace_event_required_must_be_true |
| `negative_post_run_evidence_required_false` | `rejected` | `False` | `True` | post_run_evidence_required_must_be_true |
| `negative_external_side_effects_true` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |
| `negative_service_request_assignment_nonzero` | `rejected` | `False` | `True` | runtime_boundary_service_requests_assigned_must_equal_0 |
| `negative_worker_start_nonzero` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |

## Boundary

- This validator creates local fixture/report files only.
- It does not register the pool, assign a service request, start a worker, issue credentials, issue SPIFFE/SVID identities, call model APIs, call MCP tools, open a browser, use the network as a worker, or perform account/wallet/payment/public actions.
- A passing result means the candidate identity envelope is acceptable as evidence for a later preflight, not that execution is approved.
