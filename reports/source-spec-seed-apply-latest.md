# Source Spec Seed Apply

Generated UTC: 2026-06-15T17:05:23Z
JSON mirror: `E:\agent-company-lab\reports\source-spec-seed-apply-latest.json`
Validation: `E:\agent-company-lab\reports\source-spec-seed-apply-validation-latest.json`

## Summary

- Seed packet rows: `3`
- Applied specs: `3`
- Source-spec DB rows before: `10`
- Source-spec DB rows after: `13`
- Registry specs before: `10`
- Registry specs after: `13`
- Source-spec gaps after apply: `0`

## Applied Specs

| Lane | Spec | Source Type | Packet |
| --- | --- | --- | --- |
| `ai_ml_competitions` | `ai_ml_competitions_public_prize_source_seed` | `public_competition_registry` | `E:\agent-company-lab\reports\source-spec-seed-packets\ai_ml_competitions-source-spec-seed-20260615.json` |
| `digital_products_templates_plugins` | `digital_products_marketplace_demand_source_seed` | `public_marketplace_research` | `E:\agent-company-lab\reports\source-spec-seed-packets\digital_products_templates_plugins-source-spec-seed-20260615.json` |
| `money_source_discovery` | `money_source_discovery_public_venue_source_seed` | `public_venue_registry` | `E:\agent-company-lab\reports\source-spec-seed-packets\money_source_discovery-source-spec-seed-20260615.json` |

## Boundary

- This command only updates local registry and SQLite source-spec rows.
- It does not run refresh commands, browse, register accounts, accept terms, download gated data, publish, submit, touch wallets/payments, mutate service requests, assign workers, start workers, call APIs, or create external side effects.

## Next Action

Regenerate source-spec, gap-map, and seed-packet reports; missing source-spec count should now be zero.

