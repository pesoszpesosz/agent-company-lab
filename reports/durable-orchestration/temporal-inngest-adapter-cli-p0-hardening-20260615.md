# Durable Adapter CLI P0 Hardening

Generated: 2026-06-15T15:05:35Z

## Implemented

- Added fixture document schema check for `agent_company.durable_adapter_reducer_fixture_set.v1`.
- Added safe `--result-path` resolution that keeps dry-run output inside `E:\agent-company-lab\reports\durable-orchestration`.
- Changed result writing so reducer failures do not create or overwrite a requested result file.
- Kept the dry-run command local-only: no approvals, service-request updates, assignments, worker starts, Temporal/Inngest runtime starts, API calls, or external effects.

## Verification

- Syntax compile: passed.
- Help command: passed.
- Positive JSON dry-run: 14 results, 0 failures.
- Positive safe result write: passed.
- Unsafe result path: rejected, exit code 1, file not created.
- Bad fixture schema: rejected, exit code 1.
- Reducer failure with requested result path: exit code 1, file not created.
- Service-request status mix after tests: 11 `needs_review`, 1 `complete`, 2 `rejected`.

## Artifacts

- Positive result: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-p0-hardening-positive-result-20260615.json`
- Negative bad-schema fixture: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-negative-bad-schema-20260615.json`
- Negative action-true fixture: `E:\agent-company-lab\reports\durable-orchestration\temporal-inngest-adapter-cli-negative-action-true-20260615.json`

## Next Action

Implement P1 fixture field/type validation and duplicate-id negative tests before broad dry-run usage.
