# CEO Decision Parser Apply Readiness Signed Decision Positive Fixture

Generated UTC: 2026-06-16T09:52:37Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-positive-fixture-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-readiness-signed-decision-positive-fixture-validation-latest.json`

## Decision

`ceo_decision_parser_apply_readiness_signed_decision_positive_fixture_ready_preview_only`

Created one local positive signed-decision fixture that should pass the signed-decision guard while still keeping apply disabled and granting no real approval.

## Fixture

- Fixture: `valid-signed-decision-preview-only`
- Expected accepted: `True`
- Apply command enabled: `False`
- Real mutation expected: `False`

## Boundary

This fixture is local test data only. It grants no approval, enables no apply command, updates no service request, emits no approval request, starts no worker, calls no API, opens no browser, and performs no account, wallet, payment, public, security-testing, external, or real-money action.

## Next Action

Run a report-only positive signed-decision runner; do not add or run any mutating apply command without a separate explicit operator approval.

