# Local Runtime Adapter Pool Activation Contract Design v1

Generated UTC: 2026-06-17T19:20:34Z

Lane: platform_engineering

Task: task-local-runtime-adapter-pool-activation-contract-design-v1-20260617

## Purpose

This artifact defines a validator-ready contract design for `service-worker-local-runtime-adapter-pool` activation.

It is still report-only. It does not create the validator, register the pool, assign service requests, start workers, execute local runtime commands, or mutate external state.

## Source Artifacts

- Activation preflight: `E:\agent-company-lab\reports\local-runtime-adapter-pool-activation-preflight-v1-20260617.json`
- Worker activation runway: `E:\agent-company-lab\reports\worker-activation-runway-v1-20260617.json`
- Operator decision packet: `E:\agent-company-lab\reports\worker-pool-operator-decision-packet-v1-20260617.json`
- Identity envelope matrix: `E:\agent-company-lab\reports\agent-identity-envelope-matrix-v1-20260617.json`
- Egress event ledger packet: `E:\agent-company-lab\reports\agent-egress-event-ledger-packet-v1-20260617.json`
- Chain integrity validation: `E:\agent-company-lab\reports\service-worker-chain-integrity-validation-latest.json`

## Contract Inputs

The future validator should accept one JSON activation candidate with:

- `activation_contract_id`
- `activation_schema_version`
- `created_utc`
- `expires_utc`
- `worker_pool_id`
- `role_id`
- `department_id`
- `operator_decision_artifact_path`
- `identity_envelope_artifact_path`
- `egress_contract_artifact_path`
- `assignment_preflight_artifact_path`
- `runtime_start_preflight_artifact_path`
- `chain_integrity_artifact_path`
- `allowed_runtime_mode`
- `input_artifact_paths`
- `output_artifact_path`
- `trace_id`
- `teardown_or_rollback_plan`
- `post_run_evidence_requirements`
- `runtime_boundary`

## Required Fixed Values

The first accepted candidate must be constrained to:

- `worker_pool_id`: `service-worker-local-runtime-adapter-pool`
- `role_id`: `observability_worker`
- `department_id`: `service_worker_observability`
- `allowed_runtime_mode`: `report_only_local_dry_run`
- `runtime_boundary.network`: false
- `runtime_boundary.browser`: false
- `runtime_boundary.model_api_calls`: false
- `runtime_boundary.mcp_tool_calls`: false
- `runtime_boundary.credentials`: false
- `runtime_boundary.account_wallet_payment_public_actions`: false
- `runtime_boundary.external_side_effects`: false

## Validation Rules

The future validator must pass only if:

1. `activation_schema_version` is `agent_company.local_runtime_adapter_pool_activation_contract.v1`.
2. `worker_pool_id`, `role_id`, and `department_id` match the required fixed values.
3. `created_utc` and `expires_utc` are present and ordered correctly.
4. Operator decision artifact exists and does not authorize direct registration.
5. Identity envelope artifact exists and explicitly denies browser, model/API, MCP, wallet, payment, account, credential, public, GitHub public, X, marketplace, legal/KYC, and tax actions.
6. Egress contract artifact exists and allows no live egress.
7. Assignment preflight artifact proves no service request assignment occurs in this contract.
8. Runtime start preflight artifact exists before any future start step.
9. Output artifact path is declared.
10. Trace id is declared.
11. Teardown or rollback plan exists.
12. Post-run evidence requirements exist.
13. Runtime boundary is report-only and local-only.
14. No command preview is executed by the contract.
15. No worker registration, assignment, or start is performed by the contract.

## Negative Fixtures

Future validator fixture set must include:

| Fixture id | Expected result |
| --- | --- |
| `wrong_worker_pool_id` | reject |
| `wrong_role_id` | reject |
| `wrong_department_id` | reject |
| `expired_contract` | reject |
| `missing_operator_decision` | reject |
| `operator_decision_authorizes_registration` | reject |
| `missing_identity_envelope` | reject |
| `identity_allows_browser` | reject |
| `identity_allows_model_api` | reject |
| `identity_allows_mcp` | reject |
| `identity_allows_credentials` | reject |
| `identity_allows_public_action` | reject |
| `missing_egress_contract` | reject |
| `egress_allows_live_network` | reject |
| `assignment_mutation_true` | reject |
| `missing_runtime_start_preflight` | reject |
| `missing_output_artifact_path` | reject |
| `missing_trace_id` | reject |
| `missing_teardown_plan` | reject |
| `external_side_effects_true` | reject |
| `command_preview_executed` | reject |

## Positive Fixture Shape

A single positive fixture should be allowed only when it proves:

- source review exists
- worker pool id is exact
- operator decision is present but report-only
- identity envelope denies all external and privileged actions
- egress is denied
- no service request is assigned
- no worker starts
- local runtime mode is dry-run/report-only
- output artifact and trace id are present
- post-run evidence seal is required

Expected result: `pass_report_only_activation_candidate`

## Validator Output

The future validator should emit:

- `validation_schema_version`
- `generated_utc`
- `activation_contract_path`
- `all_checks_passed`
- `failure_count`
- `failures`
- `worker_pool_id`
- `activation_candidate_status`
- `registration_allowed`
- `assignment_allowed`
- `worker_start_allowed`
- `external_side_effects`
- `runtime_boundary`
- `next_required_artifact`

Expected status for current system: `candidate_contract_design_only`.

## Runtime Boundary

This design:

- creates no validator
- registers no worker pool
- assigns no service request
- starts no worker
- executes no command preview
- starts no local runtime process
- opens no browser session
- calls no model/API/MCP tool
- creates no credentials
- touches no account, wallet, payment, public, GitHub, X, marketplace, legal/KYC, or tax state
- changes no external state

## Decision

Recommended next build, after implementation-design approval: actual `local_runtime_adapter_pool_activation_contract_v1` schema, fixture files, and validator runner.

