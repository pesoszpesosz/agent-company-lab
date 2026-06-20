# Durable Adapter CLI Implementation Review Packet

Generated UTC: 2026-06-15T14:48:12Z

This is a review packet only. It does not modify `agent_company.py`, add the CLI command, execute a CLI command, or mutate service requests.

## Decision

- Local dry-run command readiness: `ready_after_review_packet_only_for_local_fixture_dry_run_command`
- External runtime readiness: `not_approved`
- Service-request mutation readiness: `not_approved`

## Proposed Code Surface

- Tool: `E:\agent-company-lab\tools\agent_company.py`
- Tool SHA-256 before/after review: `0D40754274B5234416AFDD0B35F1BDF4D7F8C6D8DFEC193AA3ED60267CC585C5`
- New subcommand: `dry-run-durable-service-request-reducer`
- Suggested implementation: pure fixture reader/result writer, no new third-party imports.

## Acceptance Tests

### help_lists_command

Command preview: `python E:\agent-company-lab\tools\agent_company.py dry-run-durable-service-request-reducer --help`

Expected: Command help displays fixture/result/json/check-live-status options.

### fixture_result_matches_static_artifact

Command preview: `python E:\agent-company-lab\tools\agent_company.py dry-run-durable-service-request-reducer --fixtures E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-reducer-dry-run-fixtures-20260615.json --json --check-live-status`

Expected: 14 result rows, output state counts 11 parked / 1 complete terminal / 2 rejected terminal, zero failures.

### optional_result_write_is_local_only

Command preview: `python E:\agent-company-lab\tools\agent_company.py dry-run-durable-service-request-reducer --fixtures E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-reducer-dry-run-fixtures-20260615.json --result-path E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-dry-run-result-latest.json`

Expected: Writes only the requested local result JSON artifact and prints ok JSON.

### service_request_rows_unchanged

Command preview: `Compare service_requests tracked fields before/after dry run.`

Expected: No request status, assignment, start, completion, decision note, or updated_at changes.

## No-Go Conditions

- Proposed command writes to service_requests, approvals, agents pool registry, or task lifecycle tables.
- Proposed command imports/starts Temporal, Inngest, browser automation, model providers, or network clients.
- Proposed command treats fixture output as approval to execute worker actions.
- Proposed command silently ignores live-status mismatch when --check-live-status is enabled.

## Validation

- Tool file unchanged: `True`
- Static result count: `14`
- Contract still not installed: `True`
- Failure count: `0`
- All checks passed: `True`

## Files

- Packet JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-implementation-review-packet-20260615.json`
- Validation JSON: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-implementation-review-validation-20260615.json`
