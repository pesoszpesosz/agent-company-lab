# Temporal/Inngest Adapter Static Dry-Run Result

Generated UTC: 2026-06-15T14:44:16Z

This is a static result artifact generated from fixtures. It did not add or execute a CLI command, modify Python files, start workers, call APIs, emit events, or mutate service requests.

## Summary

- Results: `14`
- Status counts: `{'complete': 1, 'needs_review': 11, 'rejected': 2}`
- Output states: `{'parked.awaiting_human_review': 11, 'terminal.completed_from_ledger_snapshot': 1, 'terminal.rejected_from_ledger_snapshot': 2}`
- Worker types: `{'browser_read_only': 7, 'browser_signed_in_read_only': 1, 'legal_kyc_tax_payment_review': 1, 'local_runtime_adapter': 2, 'model_api_execution': 1, 'other_gated_worker': 1, 'public_submission': 1}`
- Failure count: `0`
- All checks passed: `True`

## Runtime Boundary

- `dependency_installs`: `0`
- `dependency_imports`: `0`
- `python_files_modified`: `0`
- `cli_commands_added_to_runner`: `0`
- `cli_commands_executed`: `0`
- `static_result_generated_from_fixtures`: `True`
- `temporal_server_started`: `False`
- `inngest_service_started`: `False`
- `temporal_workflows_started`: `0`
- `temporal_activities_scheduled`: `0`
- `inngest_functions_registered`: `0`
- `inngest_events_emitted`: `0`
- `worker_starts`: `0`
- `service_requests_updated`: `0`
- `service_requests_assigned`: `0`
- `approvals_granted`: `0`
- `api_calls`: `False`
- `external_side_effects`: `False`

## Results

| Fixture | Request | Input | Output | Worker | Matches? | Mutates? | Starts? |
|---|---|---|---|---|---:|---:|---:|
| `fixture-reducer-dry-run-01` | `req-grok-research-worker-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_signed_in_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-02` | `req-next-wave-digital-legal-payment-review-20260614` | `needs_review` | `parked.awaiting_human_review` | `legal_kyc_tax_payment_review` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-03` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-04` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-05` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-06` | `req-next-wave-security-report-route-review-20260614` | `needs_review` | `parked.awaiting_human_review` | `public_submission` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-07` | `req-pydantic-ai-model-backed-adapter-20260614` | `needs_review` | `parked.awaiting_human_review` | `model_api_execution` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-08` | `req-test-browser-readonly-complete-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-09` | `req-test-lifecycle-approve-20260614` | `complete` | `terminal.completed_from_ledger_snapshot` | `local_runtime_adapter` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-10` | `req-test-lifecycle-reject-20260614` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `local_runtime_adapter` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-11` | `req-test-service-intake-valid-20260614` | `rejected` | `terminal.rejected_from_ledger_snapshot` | `other_gated_worker` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-12` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-13` | `req-wave4-digital-products-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |
| `fixture-reducer-dry-run-14` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `needs_review` | `parked.awaiting_human_review` | `browser_read_only` | `True` | `False` | `False` |

## Files

- Result JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-static-dry-run-result-20260615.json`
- Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-static-dry-run-result-validation-20260615.json`
- Source fixtures: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-reducer-dry-run-fixtures-20260615.json`
