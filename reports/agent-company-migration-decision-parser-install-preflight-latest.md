# Agent Company Migration Decision Parser Install Preflight

Generated UTC: 2026-06-16T12:35:34Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-preflight-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-preflight-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_install_preflight_ready_for_operator_install_review`

Recommended default: `hold_without_operator_approval_to_write_parser_module_file`

Prepared a report-only install preflight for the migration decision parser module, with target file, gates, rollback steps, and operator approval requirements.

## Target File

- `E:\agent-company-lab\tools\migration_decision_parser.py`: not_written_requires_operator_approval

## Install Gates

- `operator_signed_file_write_approval_required`
- `target_path_must_be_inside_agent_company_lab_tools`
- `backup_existing_target_if_present`
- `write_to_temp_file_before_replace`
- `run_py_compile_on_temp_file`
- `run_saved_fixture_runner_against_temp_file`
- `do_not_import_from_live_command_path`
- `preserve_service_request_counts`
- `write_post_install_static_review_before_enabling_live_parse`

## Rollback Steps

- `delete_temp_file_if_compile_fails`
- `restore_existing_target_from_backup_if_replace_fails`
- `remove_new_target_if_post_install_static_review_fails`
- `restore_pre_install_artifact_index`
- `rerun_chain_integrity_after_rollback`

## Approval Requirements

- `signed_operator_decision_id`
- `exact_target_path`
- `exact_source_artifact_path`
- `permission_to_write_one_local_file_only`
- `permission_expires_after_one_attempt`
- `no_permission_to_parse_live_decisions`

## Boundary

This is a report-only install preflight. It does not write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Prepare the operator install review packet next; do not write, install, import, or run the parser module.

