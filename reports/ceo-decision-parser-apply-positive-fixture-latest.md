# CEO Decision Parser Apply Positive Fixture

Generated UTC: 2026-06-15T23:59:01Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-parser-apply-positive-fixture-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-parser-apply-positive-fixture-validation-latest.json`

## Decision

`ceo_decision_parser_apply_positive_fixture_ready_preview_only`

Created one positive apply dry-run fixture that previews a single bounded service-request approval-scope update without applying it.

## Preview

- Target request: `req-wave4-digital-products-browser-readonly-20260614`
- Preview state: `would_update_single_service_request_approval_scope`
- Applied: `False`

## Boundary

This is a local positive dry-run fixture only. It previews one service-request field update and applies nothing; it does not update service requests, request approval, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.

## Next Action

Use this positive fixture with the apply guard before building any real apply path; the next step is a report-only apply dry-run runner that confirms the preview while leaving the DB unchanged.

