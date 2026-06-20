# Temporal/Inngest Adapter CLI Hardening Checklist

Generated: 2026-06-15T14:59:10Z

## Scope

This packet hardens the local fixture-only command `dry-run-durable-service-request-reducer` after the first implementation pass. It does not approve service requests, assign workers, start workers, emit events, schedule activities, call APIs, start Temporal or Inngest, or mutate the service-request ledger.

Source code: `E:\agent-company-lab\tools\agent_company.py`  
Source hash: `799400CC78D467426F30163906129988AF78A268C37F20E157FC46C3D4D09983`

## Current Behavior

- Reads a required fixture JSON file.
- Optionally reads live service-request status from SQLite with `--check-live-status`.
- Optionally writes a result payload with `--result-path`.
- Forces all action and side-effect fields to `false`.
- Verified positive fixture count: 14.
- Verified positive failure count: 0.

## P0 Hardening

1. Safe result path: resolve `--result-path` and require it to stay inside `E:\agent-company-lab\reports\durable-orchestration` before creating directories or writing.
2. Fixture document schema: require `schema_version == agent_company.durable_adapter_reducer_fixture_set.v1`.
3. Failure write policy: do not write result output when fixture validation or path validation fails.

## P1 Hardening

1. Require top-level fixture keys: `fixture_id`, `request_id`, `input`, `expected_output`, and `expected_exit`.
2. Require non-empty string input fields: `status_snapshot`, `event_name`, `risk_gate`, `worker_type`, `idempotency_key`, and `source_event_id`.
3. Require expected action fields to exist and be explicitly `false`.
4. Restrict `output_state` to the known parked/completed/rejected states.
5. Reject duplicate fixture IDs, request IDs, and idempotency keys.
6. Validate `resume_requirements` as a list of strings, non-empty for parked states.
7. Require positive fixture packets to use `expected_exit.exit_code == 0`.
8. Add negative fixtures for missing input, true action output, duplicate idempotency, bad schema, and unsafe result path.

## P2 Hardening

1. Wire or remove `DURABLE_ADAPTER_DRY_RUN_DEFAULT_RESULT`, which is defined but not currently used.
2. Document whether `resume_requirements` ordering is semantic.
3. Normalize validation errors under `--json` with fixture index, field, expected, actual, and remediation.

## Acceptance Tests

- Existing help command still exposes `--fixtures`, `--result-path`, `--json`, and `--check-live-status`.
- Existing positive fixture JSON dry-run returns 14 results and zero failures.
- Existing positive result write succeeds inside durable-orchestration reports.
- Malformed fixture packets exit nonzero without result writes.
- Unsafe result paths exit nonzero before parent creation.
- Failed tests leave `service_requests` unchanged.
- No approval, assignment, worker start, API call, external side effect, Temporal workflow, or Inngest event occurs.

## Validation

Checklist items: 14  
P0 items: 3  
Source implementation validation: passed  
Source hash unchanged in this slice: yes  
Service-request mutation count: 0  
External side effects: none

## Next Action

Implement P0 hardening for safe result paths and fixture schema validation with `apply_patch`, then run positive and negative dry-run tests.
