# Agent Company Department Schema Plan

Generated UTC: 2026-06-16T11:18:52Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-department-schema-plan-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-department-schema-plan-validation-latest.json`

## Decision

`agent_company_department_schema_plan_ready_for_report_only_migration_draft`

Converted the department architecture packet into a report-only schema plan for tables, columns, indexes, service request contracts, migration order, and guardrails.

## Table Plans

| Table | Columns | Indexes |
| --- | ---: | --- |
| `agent_threads` | 12 | department_state, owner_state |
| `departments` | 10 | status_manager, default_lane |
| `money_paths` | 13 | department_status, category_score |
| `opportunity_leads` | 15 | money_path_status, risk_payout |
| `worker_pool_interfaces` | 12 | department_status, approval_status |
| `approval_gates` | 14 | state_type, service_request_state |
| `evidence_packets` | 13 | department_status, source_task |
| `task_handoffs` | 12 | to_thread_status, task_status |
| `experiment_runs` | 13 | money_path_result, department_started |
| `roi_ledger` | 13 | money_path_status, value_probability |

## Service Request Contracts

- `research_money_path`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `normalize_opportunity_lead`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `draft_bounty_patch`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `draft_security_report`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `paper_trade_market`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `build_digital_asset`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `quality_review_artifact`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `request_registration_worker`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `request_wallet_worker`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `request_public_submission`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `request_real_money_action`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope
- `request_security_scope_review`: status starts as `needs_review`; required fields: request_id, department_id, source_path, risk_summary, approval_scope

## Migration Order

1. `create_departments_and_money_paths_plan`
2. `create_agent_threads_and_worker_pool_interfaces_plan`
3. `create_approval_gates_plan`
4. `create_opportunity_leads_plan`
5. `create_evidence_packets_and_task_handoffs_plan`
6. `create_experiment_runs_and_roi_ledger_plan`
7. `backfill_department_mappings_plan`
8. `run_report_only_integrity_validation_plan`

## Guardrails

- `report_only_until_operator_approval`
- `no_table_creation_in_this_command`
- `no_worker_start_or_assignment`
- `no_browser_or_account_action`
- `no_wallet_payment_or_real_money_action`
- `no_security_testing_beyond_read_only`
- `no_public_submission_or_marketplace_post`
- `preserve_existing_service_request_states`

## Boundary

This schema plan is report-only. It creates no database tables, starts no workers, assigns no service requests, calls no APIs, opens no browsers, registers no accounts, touches no wallets or payments, spends no money, posts nowhere, and performs no security testing.

## Next Action

Draft the report-only migration packet next; do not create tables or start any workers until explicitly approved.

