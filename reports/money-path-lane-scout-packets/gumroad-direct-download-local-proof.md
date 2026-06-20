# Gumroad Direct Download Local Proof

Generated UTC: 2026-06-18T06:41:33Z
Task: `task-lane-scout-gumroad_direct_download-20260618`
Lane: `digital_products_templates_plugins`

Purpose: evaluate whether an existing local digital product can become a Gumroad direct-download route. This is not a Gumroad account, seller setup, listing, upload, price publication, payout setup, payment action, or public action.

## Source Observations

| Source | URL | Observation | Route Effect |
| --- | --- | --- | --- |
| `gumroad_features` | https://gumroad.com/features | Gumroad's public features page describes a simple creator-commerce flow for digital downloads, ebooks, courses, memberships, subscriptions, multiple versions, license keys, lightweight DRM, and immediate customer access after purchase. | A local file bundle is a plausible route if it stays a downloadable product, not a consulting/service promise. |
| `gumroad_pricing` | https://gumroad.com/pricing | Gumroad's pricing page states 10% plus $0.50 per transaction for profile/direct-link sales, 30% for marketplace-discovered sales, no monthly charge, and merchant-of-record tax handling from January 1, 2025. | Direct-link economics can be modeled locally, but account, payout, tax, and terms review remain gated before listing. |
| `gumroad_prohibited_products` | https://gumroad.com/prohibited | Gumroad's prohibited-products page blocks categories including deceptive marketing, crypto products, hacking/cracking materials, copyrighted/unauthorized goods, gambling, bulk marketing/spam tools, and certain services/consulting/business-opportunity offerings. | The product must avoid revenue promises, crypto/security-bypass claims, spam tools, unauthorized assets, consulting delivery, and get-rich/business-opportunity positioning. |
| `local_agent_skill_starter_kit` | E:/agent-company-lab/products/agent-skill-starter-kit-v0/ | Local product bundle contains README, listing draft, screenshot plan, buyer guide, license/IP note, templates, and a fictional local-research example skill. | This is the strongest Gumroad direct-download candidate because it is already file-based and has local listing/IP notes. |
| `local_ai_builder_launch_pack` | E:/agent-company-lab/reports/digital-products-local-package-files-latest.md | Local AI builder launch checklist pack has package-file, quality-pass, and packaging-manifest evidence, with gates preserved for live marketplace research, terms, listings, accounts, payouts, and payment setup. | This is a second candidate, but it is less directly materialized as a product directory than the Agent Skill Starter Kit. |

## Candidate Comparison

| Candidate | Product Type | Readiness | Why | Gates |
| --- | --- | ---: | --- | --- |
| `agent_skill_starter_kit_v0`<br>Agent Skill Starter Kit: Templates For Safer Reusable AI-Agent Workflows | downloadable_markdown_template_kit | 91 | Already packaged as a concrete file tree, avoids live client data, and can be positioned as templates rather than consulting, revenue claims, or platform endorsement. | `gumroad_account`, `seller_terms`, `payout_setup`, `tax_payment_review`, `public_listing`, `ip_license_claims_review` |
| `ai_builder_launch_checklist_pack`<br>AI Builder Launch Checklist Pack | downloadable_markdown_launch_planning_pack | 76 | The package has strong local QA and manifest evidence, but it currently exists mainly as reports rather than a single product directory ready for checksum/zip review. | `gumroad_account`, `seller_terms`, `payout_setup`, `tax_payment_review`, `public_listing`, `ip_license_claims_review` |

## Candidate Details

### `agent_skill_starter_kit_v0`

Working title: Agent Skill Starter Kit: Templates For Safer Reusable AI-Agent Workflows

Download shape:
- `README.md`
- `templates/SKILL.template.md`
- `templates/gate-checklist.template.md`
- `templates/service-request-checklist.template.md`
- `templates/artifact-contract.template.md`
- `templates/acceptance-review.template.md`
- `examples/local-research-skill/SKILL.md`
- `examples/local-research-skill/sample-output.md`
- `docs/buyer-guide.md`
- `docs/license-and-ip-note.md`
- `docs/listing-draft.md`
- `docs/screenshot-plan.md`

Required pre-listing fixes:
- Review Gumroad prohibited-products list against the final listing copy.
- Avoid consulting, get-rich, crypto, hacking/cracking, spam, revenue, compliance, or platform-approval claims.
- Confirm the license/IP note matches the intended buyer license.
- Create a local zip manifest and checksum before any upload approval.
- Human-review title, category, price, refund language, and all claims.

Local evidence assets:
- `products/agent-skill-starter-kit-v0/README.md`
- `products/agent-skill-starter-kit-v0/docs/listing-draft.md`
- `products/agent-skill-starter-kit-v0/docs/license-and-ip-note.md`

### `ai_builder_launch_checklist_pack`

Working title: AI Builder Launch Checklist Pack

Download shape:
- `README.md`
- `positioning-template.md`
- `launch-checklist.md`
- `screenshot-shotlist.md`
- `qa-pass.md`
- `post-launch-review.md`

Required pre-listing fixes:
- Materialize the six files into a product folder.
- Run a file presence and link check.
- Remove any language implying marketplace validation, buyer count, revenue, conversion, or payout.
- Human-review whether launch-planning language is safely a template product and not a business-opportunity/service offer.

Local evidence assets:
- `reports/digital-products-local-packaging-manifest-latest.md`
- `reports/digital-products-local-package-files-latest.md`
- `reports/digital-products-local-quality-pass-latest.md`

## Direct-Link Unit Economics

Internal planning only. This uses Gumroad's public direct/profile fee and does not include refunds, chargebacks, income tax, payment-country differences, or paid promotion.

| Price | Estimated Gumroad Direct Fee | Before Other Costs | Note |
| ---: | ---: | ---: | --- |
| $9 | $1.40 | $7.60 | Uses 10% + $0.50 direct/profile fee from public pricing page; ignores refunds, chargebacks, income tax, payment-country differences, and paid promotion. |
| $19 | $2.40 | $16.60 | Middle planning price for a compact template bundle. |
| $29 | $3.40 | $25.60 | Higher planning price; needs stronger proof of utility before public use. |

## Recommended First Candidate

`agent_skill_starter_kit_v0`

Gumroad supports direct digital downloads and the starter kit is already a file-based local product. External action remains blocked because Gumroad account, seller terms, payout/tax/payment, prohibited-category, IP/license, listing copy, price, refund language, and public listing gates have not been approved.

## Acceptance Checks

- Official Gumroad feature, pricing, and prohibited-product sources are summarized.
- At least two local product candidates are compared.
- A recommended first candidate is selected from existing local product assets.
- Direct-link unit economics are modeled using the public direct/profile fee only as an internal planning estimate.
- No Gumroad account/login, seller setup, terms acceptance, payout setup, upload, listing, price publication, public action, payment action, service-request mutation, worker/runtime start, model/API call, or external side effect occurs.

## Boundary

No Gumroad account/login, seller profile, terms acceptance, product upload/edit, listing, price publication, payout/payment setup, order, public action, service-request mutation, worker/runtime start, model/MCP/external API call, or external side effect occurred.

## Next Action

Create a no-publish Gumroad approval request packet for Agent Skill Starter Kit v0; include seller terms/prohibited-products review, IP/license review, price/refund/copy review, zip checksum plan, payout/tax/payment gate, and public listing approval.
