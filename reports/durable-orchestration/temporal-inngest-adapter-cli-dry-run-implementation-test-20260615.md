# Durable Adapter CLI Dry-Run Implementation Test

Generated UTC: 2026-06-15T14:52:56Z

This verifies the newly added local fixture-only dry-run command. It ran help, JSON fixture dry-run, and local result write tests only.

## Summary

- `syntax_ok`: `True`
- `help_ok`: `True`
- `json_dry_run_ok`: `True`
- `write_dry_run_ok`: `True`
- `service_request_mutation_count`: `0`
- `result_count`: `14`
- `output_state_counts`: `{'parked.awaiting_human_review': 11, 'terminal.completed_from_ledger_snapshot': 1, 'terminal.rejected_from_ledger_snapshot': 2}`

## Boundary

- `python_files_modified`: `1`
- `cli_commands_added_to_runner`: `1`
- `cli_commands_executed`: `2`
- `dependency_installs`: `0`
- `dependency_imports`: `0`
- `service_requests_updated`: `0`
- `service_requests_assigned`: `0`
- `approvals_granted`: `0`
- `worker_starts`: `0`
- `temporal_server_started`: `False`
- `temporal_workflows_started`: `0`
- `temporal_activities_scheduled`: `0`
- `inngest_service_started`: `False`
- `inngest_functions_registered`: `0`
- `inngest_events_emitted`: `0`
- `api_calls`: `False`
- `external_side_effects`: `False`

## Validation

- Failure count: `0`
- All checks passed: `True`

## Files

- Result JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-dry-run-result-20260615.json`
- Test report JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-dry-run-implementation-test-20260615.json`
- Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-dry-run-implementation-validation-20260615.json`
