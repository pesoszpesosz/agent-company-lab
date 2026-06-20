# Runtime Implementation Human Approval Packet v2

Generated UTC: 2026-06-17T17:52:03Z
Packet JSON: `E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-human-approval-packet-v2-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-human-approval-packet-v2-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\runtime-implementation-human-approval-packet-v2.schema.json`

## Current Decision

- Approval granted by this packet: `false`
- Runtime implementation allowed now: `false`
- Runtime code write allowed now: `false`
- Validation failures: `0`

## Source Evidence

- Outbox acknowledgement runner failures: `0`
- State-machine runner failures: `0`
- Chain integrity failures: `0`

## Runtime Candidates

| Rank | Runtime | Current Decision | Score | Required Gates |
| ---: | --- | --- | ---: | --- |
| `1` | `sqlite_control_plane` | `promote_now_local_only` | `94` | none_for_local_report_only |
| `2` | `temporal_python` | `hold_for_human_runtime_approval_after_local_runner` | `83` | dependency_install_approval, runtime_server_worker_approval, service_worker_pool_registration_approval, determinism_review, human_signal_authority_packet |
| `3` | `inngest` | `hold_for_event_adapter_approval_after_local_outbox_ack` | `78` | dependency_install_approval, network_or_cloud_boundary_review, event_endpoint_approval, trace_export_contract_approval |
| `4` | `dbos_python` | `hold_for_database_provisioning_review` | `76` | dependency_install_approval, database_provisioning_review, secrets_credentials_handling_gate, state_migration_review |
| `5` | `pydantic_ai_durable_execution` | `reference_only_until_model_api_gate` | `75` | model_api_execution_gate, provider_model_cost_scope_approval, credential_route_approval, output_artifact_scope_approval |
| `6` | `restate` | `watchlist_after_local_outbox_service_boundaries` | `70` | dependency_install_approval, server_runtime_review, service_invocation_approval, llm_tool_execution_gate, state_retention_review |
| `7` | `prefect` | `watchlist_for_source_refresh_after_local_runner` | `66` | dependency_install_approval, server_or_cloud_boundary_review_if_used, source_refresh_service_request_approval, retry_idempotency_review |

## Approval Questions

| Question ID | Default | Question |
| --- | --- | --- |
| `approve_runtime_candidate` | `deny_all` | Which one runtime candidate, if any, is approved for implementation? |
| `approve_dependency_install_scope` | `no` | May dependencies be installed for the selected runtime? |
| `approve_runtime_import_scope` | `no` | May selected runtime libraries be imported from executable code? |
| `approve_runtime_start_scope` | `no` | May local servers, workers, workflows, functions, schedules, or event emitters be started? |
| `approve_database_or_cloud_scope` | `no` | May databases, cloud services, accounts, endpoints, or service credentials be provisioned or contacted? |
| `approve_service_request_mutation_scope` | `no` | May runtime code assign, start, complete, reject, or otherwise mutate service_requests rows? |
| `approve_worker_pool_registration_scope` | `no` | May service-worker pools be registered as executable workers rather than report-only plans? |
| `approve_model_api_scope` | `no` | May model/API execution be used, including provider, model, data scope, and cost cap? |
| `approve_trace_export_scope` | `no` | May traces be sent to an observability backend rather than local JSONL/SQLite artifacts? |
| `approve_browser_or_public_action_scope` | `no` | May browser sessions, public actions, submissions, comments, forms, or account actions occur? |
| `approve_wallet_payment_real_money_scope` | `no` | May wallet, payment, deposit, withdrawal, trade, payout, or real-money actions occur? |
| `approve_security_testing_scope` | `no` | May security testing or private-report submission occur beyond local/public-code review? |

## Required Decision Fields

| Field | Required | Default | Purpose |
| --- | --- | --- | --- |
| `decision_id` | `true` | `""` | Stable human decision identifier. |
| `decision` | `true` | `"deny"` | Explicit deny or limited approval. |
| `approver` | `true` | `""` | Human approver identity. |
| `signed_utc` | `true` | `""` | Human signature timestamp. |
| `expires_utc` | `true` | `""` | Approval expiry timestamp. |
| `selected_runtime_id` | `true` | `"none"` | Exactly one runtime candidate or none. |
| `approved_question_ids` | `true` | `[]` | Question IDs explicitly granted. |
| `denied_question_ids` | `true` | `["approve_runtime_candidate", "approve_dependency_install_scope", "approve_runtime_import_scope", "approve_runtime_start_scope", "approve_database_or_cloud_scope", "approve_service_request_mutation_scope", "approve_worker_pool_registration_scope", "approve_model_api_scope", "approve_trace_export_scope", "approve_browser_or_public_action_scope", "approve_wallet_payment_real_money_scope", "approve_security_testing_scope"]` | Question IDs denied or still parked. |
| `allowed_dependency_names` | `true` | `[]` | Exact dependency names and versions if installs are approved. |
| `allowed_runtime_processes` | `true` | `[]` | Exact local server/worker/process commands if starts are approved. |
| `allowed_database_or_cloud_resources` | `true` | `[]` | Exact DB/cloud/account resources if any are approved. |
| `service_request_mutation_scope` | `true` | `"none"` | Exact rows and mutations allowed, otherwise none. |
| `provider_model_and_cost_cap` | `true` | `"none"` | Model/API provider, model, data scope, and cost cap. |
| `artifact_output_path` | `true` | `""` | Allowed local output artifact path. |
| `rollback_plan` | `true` | `""` | How to stop/revert approved runtime work. |
| `human_notes` | `false` | `""` | Optional constraints and rationale. |

## Boundary

- This packet does not approve dependency installs, runtime imports, runtime starts, server/cloud/database provisioning, worker-pool registration, model/API calls, browser/public/account/wallet/payment/security/real-money actions, or service-request mutation.
- A separate signed human decision artifact is required before any executable runtime implementation work.
