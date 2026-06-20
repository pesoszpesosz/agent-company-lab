# Local Runtime Adapter Pool Identity Envelope Contract v1

Generated UTC: 2026-06-17T19:34:00Z

Lane: `platform_engineering`

Task: `task-local-runtime-adapter-pool-identity-envelope-contract-v1-20260617`

Worker pool: `service-worker-local-runtime-adapter-pool`

## Purpose

This artifact defines the report-only identity envelope contract required before the local runtime adapter worker pool can become a registration candidate.

It does not register a pool, assign a service request, start a worker, mint credentials, issue SPIFFE IDs, open a browser, call a model API, call MCP tools, or perform any external action.

## Why This Is The Next Layer

The activation runway selected `service-worker-local-runtime-adapter-pool` as the safest first pilot because it is local-only. The activation preflight still blocks it because identity, operator-decision, egress, assignment, runtime-start, and chain-integrity contracts are incomplete.

The identity envelope is the next narrow piece: it binds a future worker pool candidate to a role, department, allowed runtime mode, denied external scopes, trace requirements, and revocation state.

Current public research points in the same direction. Agent systems increasingly need non-human identity, policy checks, registry-scoped tool access, and audit evidence before execution. SPIFFE/SPIRE, OpenFGA, OPA, Cedar, MCP registry projects, ToolHive, AI gateways, and 2026 agentic IAM guidance are useful references, but this lab should not install or run them yet. The local SQLite ledger remains the source of truth until the contracts and validators exist.

## Required Fixed Values

| Field | Required value |
| --- | --- |
| `worker_pool_id` | `service-worker-local-runtime-adapter-pool` |
| `role_id` | `observability_worker` |
| `department_id` | `service_worker_observability` |
| `principal_mode` | `non_human_worker_pool_candidate` |
| `allowed_runtime_modes` | `report_only_local_dry_run` only |
| `allowed_egress_types` | empty |
| `allowed_mcp_servers` | empty |
| `allowed_mcp_tools` | empty |
| `credential_policy` | `deny` |
| `browser_session_policy` | `deny` |
| `model_api_policy` | `deny_until_separate_costed_provider_approval` |
| `mcp_policy` | `deny_until_registry_gate_and_egress_event` |
| `wallet_policy` | `deny` |
| `payment_policy` | `deny` |
| `account_policy` | `deny` |
| `public_action_policy` | `deny` |
| `network_policy` | `deny` |

## Required Fields

The machine-readable JSON companion lists the full required field set. The important categories are:

- identity metadata: envelope id, schema version, created/expiry times, revocation status
- pool binding: pool id, role id, department id, lane ids, owner agent/thread
- delegation: principal mode and delegation chain
- source artifacts: operator decision and activation contract paths
- scopes: allowed service request types, runtime modes, input paths, output roots, egress types, targets, MCP servers/tools
- denied policies: browser, credentials, model API, MCP, wallet, payment, account, public action, and network
- evidence rules: trace event, recording/redaction, post-run evidence, runtime boundary, policy verifier

## Validation Rules

The future validator should fail unless all of these hold:

1. Schema version matches exactly.
2. The envelope is not expired or revoked.
3. Worker pool, role, and department match the local runtime adapter pool exactly.
4. Operator-decision and activation-contract artifacts exist, but neither is treated as registration approval.
5. Runtime mode is only `report_only_local_dry_run`.
6. Service request types do not exceed the current local pool scope.
7. Egress, MCP, browser, credential, wallet, payment, account, public-action, and network scopes are denied or empty.
8. Filesystem writes are limited to declared report output roots.
9. Trace event and post-run evidence are required.
10. Runtime boundary reports zero external side effects.

## Positive Fixture

`identity_local_runtime_adapter_report_only_candidate`

Expected result: `pass_identity_candidate_not_registration_approval`

Meaning: the candidate can be used by a later validator as evidence for a local report-only activation candidate, but it cannot authorize registration, assignment, worker start, browser use, model/API calls, MCP calls, credentials, wallet/payment/account work, or public actions.

## Negative Fixtures

- `wrong_worker_pool_id`
- `wrong_role_id`
- `wrong_department_id`
- `missing_operator_decision_artifact`
- `operator_decision_claims_registration_approval`
- `expired_identity_envelope`
- `revoked_identity_envelope`
- `allowed_runtime_mode_live`
- `allowed_egress_type_browser_read_only`
- `allowed_egress_type_model_api`
- `allowed_mcp_server_non_empty`
- `credential_policy_allow`
- `browser_session_policy_allow`
- `network_policy_allow`
- `wallet_policy_allow`
- `payment_policy_allow`
- `account_policy_allow`
- `public_action_policy_allow`
- `filesystem_writes_unbounded`
- `trace_event_required_false`
- `post_run_evidence_required_false`
- `external_side_effects_true`

## Current Status

`identity_contract_design_only`

Registration allowed: no.

Assignment allowed: no.

Worker start allowed: no.

## Recommended Next Build

`local_runtime_adapter_pool_identity_envelope_v1_schema_fixture_files_validator_runner`

That next step should create a schema, positive/negative fixtures, and a local validator. It should still avoid pool registration, assignment, worker starts, browser/API/MCP calls, credentials, accounts, wallets, payments, public actions, and other external side effects.
