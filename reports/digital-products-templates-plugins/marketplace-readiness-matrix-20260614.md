# Marketplace Readiness Matrix - 2026-06-14

Lane: `digital_products_templates_plugins`
Scope: local readiness matrix for `MSD-008` through `MSD-012`
Product: `Agent Skill Starter Kit v0`
Product folder: `E:\agent-company-lab\products\agent-skill-starter-kit-v0`
Realized USD: `0`

## Boundary

This artifact is local planning only. It does not approve browser actions, seller signup, payment/tax/KYC setup, listing upload, public promotion, or real-money actions.

Current gated requests remain unchanged:

- `req-wave4-digital-products-browser-readonly-20260614`: `needs_review`.
- `req-next-wave-digital-marketplace-browser-readonly-20260614`: `needs_review`.
- `req-next-wave-digital-legal-payment-review-20260614`: `needs_review`.

## Local Asset Check

The local product bundle already contains:

- README;
- `SKILL.md` template;
- gate checklist;
- service-request checklist;
- artifact contract;
- acceptance review;
- fictional example skill;
- buyer guide;
- license/IP note;
- screenshot plan;
- listing draft.

Build-report checks found 12 required Markdown files, 0 missing required files, 0 missing required gate terms, and 0 non-ASCII files.

## Route Matrix

| Candidate | Route | Local Fit | Public Listing Ready | First Required Gate | Local Decision |
| --- | --- | --- | --- | --- | --- |
| `MSD-008` | Gumroad-style direct digital download | High | No | Approved browser-read-only marketplace terms and fee review. | Best first direct-download route after terms/payment review. |
| `MSD-009` | Lemon Squeezy-style direct product route | Medium-high | No | Approved browser-read-only marketplace terms and merchant/payment review. | Good second direct-download route after merchant/refund/payout review. |
| `MSD-010` | Prompt marketplace route | Medium | No | Approved browser-read-only accepted-format, review, payout, and IP rules review. | Possible only if current marketplace rules accept agent skill/template files. |
| `MSD-011` | Notion template route | Low-medium for v0 | No | Approved browser-read-only terms review after a Notion-native product exists. | Secondary route; current product is a Markdown kit, not a Notion workspace. |
| `MSD-012` | Shopify app/theme ecosystem | Poor for v0 | No | No v0 action; only reconsider after product becomes an app/theme or supportable service. | Hold. This route adds app-review and support burden that does not match the current bundle. |

## Ranking

1. Direct digital-download route family: `MSD-008` and `MSD-009`.
2. Prompt marketplace route: `MSD-010`, if current accepted formats support agent skill/template bundles.
3. Notion template route: `MSD-011`, only after a Notion-native version exists.
4. Shopify route: `MSD-012`, hold for v0.

## Next Safe Local Action

Prepare one direct-download listing-readiness packet that can be reused for Gumroad-style and Lemon-Squeezy-style review once browser/legal/payment gates are approved.
