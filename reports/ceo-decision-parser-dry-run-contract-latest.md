# CEO Decision Parser Dry-Run Contract

Generated UTC: 2026-06-15T23:25:19Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-dry-run-contract-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-dry-run-contract-validation-latest.json`

## Decision

`ceo_decision_parser_dry_run_contract_ready_parser_not_executed`

Created a local dry-run output contract for any future CEO decision parser. The contract defines report-only sections and mutation-preview states without executing a parser.

## Contract Sections

- `input_snapshot`: Echo the submitted decision intake and loaded guard version without modifying it.
- `field_validation`: Report missing, unknown, malformed, or ambiguous required fields.
- `rule_evaluation`: Map every rejection or acceptance condition to an explicit guard/preflight rule id.
- `scope_boundary`: List allowed blocker ids, allowed actions, forbidden actions, and expiration/review time.
- `mutation_preview`: Preview proposed service_request status changes and worker starts without applying them.
- `audit_footer`: Emit parser version, source artifact paths, hash inputs, and zero-side-effect counters.

## Mutation Preview States

- `no_change`
- `would_keep_held`
- `would_reject_or_park`
- `would_create_bounded_service_request_update`

## Boundary

This is a local dry-run contract only. It runs no parser, accepts no decisions, and does not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.

## Next Action

Implement a report-only parser against this contract before any real service_request mutation path is allowed.

