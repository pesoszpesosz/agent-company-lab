# CEO Decision Parser Fixture Suite

Generated UTC: 2026-06-15T23:35:38Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-fixture-suite-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-fixture-suite-validation-latest.json`

## Decision

`ceo_decision_parser_fixture_suite_ready_parser_not_executed`

Created a local parser fixture-suite manifest combining six negative fixtures and one positive dry-run fixture. A future parser must pass the suite before any queue mutation path is allowed.

## Suite Entries

| Entry | Fixtures | Expected Result |
| --- | --- | --- |
| `negative-fixtures` | `6` | `reject_all` |
| `positive-fixture` | `1` | `dry_run_preview_only` |

## Boundary

This is a local fixture-suite manifest only. It runs no parser, accepts no decision, approves nothing, and does not assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.

## Next Action

Use this suite as the acceptance gate for a report-only parser; do not execute or apply parser results until the suite passes and mutation approval exists.

