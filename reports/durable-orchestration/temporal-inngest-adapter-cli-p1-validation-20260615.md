# Durable Adapter CLI P1 Fixture Validation

Generated: 2026-06-15T15:12:34Z

## Implemented

- Added preflight validation for required fixture fields and required input string fields.
- Rejected duplicate `fixture_id`, `request_id`, and `input.idempotency_key` values inside a fixture packet.
- Required dry-run action fields to be explicitly `false`.
- Restricted output states to the parked/completed/rejected reducer contract.
- Required `resume_requirements` to be a list of non-empty strings and non-empty for parked states.
- Required `expected_exit.exit_code == 0` for positive reducer fixture packets.

## Verification

- Syntax compile: passed.
- Help command: passed.
- Canonical positive fixture: 14 results, 0 failures.
- Positive safe result write: passed.
- Negative missing-input fixture: rejected, no result file created.
- Negative duplicate-ID fixture: rejected, no result file created.
- Negative output-shape fixture: rejected, no result file created.
- Negative action-true fixture: rejected, no result file created.
- Service-request status mix after tests: 11 `needs_review`, 1 `complete`, 2 `rejected`.

## Boundary

No approvals, assignments, worker starts, service-request updates, Temporal/Inngest starts, API calls, dependency installs, or external effects occurred.

## Next Action

Implement P2 cleanup for the unused default result constant and document `resume_requirements` ordering policy.
