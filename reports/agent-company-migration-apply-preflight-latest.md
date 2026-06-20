# Agent Company Migration Apply Preflight

Generated UTC: 2026-06-19T23:16:41Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-apply-preflight-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-apply-preflight-validation-latest.json`

## Decision

`agent_company_migration_apply_preflight_ready_for_operator_review_packet`

Prepared a report-only migration apply-preflight packet with checks, dry-run steps, command contract, rollback drills, and operator gates; the apply command remains disabled.

## Preflight Checks

- `source_migration_validation_all_checks_passed`
- `migration_sql_present_but_not_executed`
- `operator_approval_missing_by_design`
- `backup_path_required_before_apply`
- `throwaway_copy_dry_run_required_before_apply`
- `rollback_sql_present_for_every_index_and_table`
- `service_request_counts_must_remain_constant`
- `worker_pool_must_remain_stopped`
- `post_apply_chain_integrity_required_before_next_layer`

## Operator Gates

- `operator_approval_required_before_sql_execution`
- `backup_agent_company_sqlite_before_apply`
- `run_migration_against_throwaway_copy_first`
- `confirm_no_service_request_state_mutation`
- `confirm_no_worker_threads_started`
- `confirm_no_browser_account_wallet_payment_public_or_security_actions`
- `record_post_apply_integrity_report_before_next_layer`

## Dry Run Steps

1. `copy_agent_company_sqlite_to_timestamped_sandbox`
2. `run_report_only_sql_against_sandbox_copy`
3. `execute_validation_queries_against_sandbox_copy`
4. `compare_table_and_index_inventory_against_plan`
5. `verify_existing_tasks_and_lane_evidence_counts_on_sandbox`
6. `run_rollback_sql_against_sandbox_copy`
7. `verify_rollback_restores_pre_apply_table_inventory`
8. `write_sandbox_dry_run_report_before_live_apply_request`

## Apply Command Contract

- Command: `apply-agent-company-department-schema-migration`
- Default enabled: `False`
- Required inputs: operator_approval_id, backup_path, dry_run_report_path, migration_draft_path
- Refuse when: approval_missing, backup_missing, dry_run_failed, service_request_drift_detected

## Rollback Drills

- `drop_planned_indexes_in_reverse_order_on_sandbox`
- `drop_planned_tables_in_reverse_order_on_sandbox`
- `re-run_chain_integrity_after_sandbox_rollback`

## Boundary

This preflight packet does not enable or run an apply command. It does not execute migration SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Prepare the operator review packet next, still without running the apply command or executing migration SQL.

