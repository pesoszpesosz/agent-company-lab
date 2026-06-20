# Digital Products Marketplace Route Eligibility Wave 24

Generated UTC: 2026-06-18T03:24:00Z

Purpose: convert the Wave 23 digital-product money-path refresh into a route-specific local eligibility packet for Agent Skill Starter Kit v0.

## Decision

Recommended route: `promptbase_agent_skill_route`.

Reason: PromptBase is the closest semantic fit because the product is a Codex-style skill/template kit, and the current PromptBase seller page explicitly mentions selling prompts or agent skills/SKILL.md files. Gumroad remains a good direct-download fallback. Lemon Squeezy is promising for software/template commerce but carries heavier legal/tax/payment/account review needs.

No external action was taken. This packet does not browse marketplaces, create seller accounts, accept terms, configure payouts, create a zip, upload files, list products, submit prompts/skills, publish pages, assign service requests, start workers, or call model/MCP tools.

## Product Evidence

- Product: Agent Skill Starter Kit v0
- Manifest: `E:\agent-company-lab\reports\digital-products-templates-plugins\agent-skill-starter-kit-package-manifest-20260614.json`
- Files: 12
- Total bytes: 21,670
- Package status: `internal_review_manifest_only`
- Public listing ready: false
- Realized USD: 0

## Route Ranking

| Rank | Route | Fit | Why | Next Local Proof |
| ---: | --- | ---: | --- | --- |
| 1 | PromptBase agent skill route | 88 | Best fit for SKILL.md and agent-skill product language. | Draft PromptBase-specific local listing and eligibility checklist. |
| 2 | Gumroad direct download route | 79 | Good low-complexity Markdown/template bundle route. | Draft direct-download page copy and local asset checklist. |
| 3 | Lemon Squeezy software product route | 72 | Strong software/product commerce tooling, heavier legal/payment/account obligations. | Draft route decision note for download, lead magnet, license, or subscription shape. |

## Active Holds Preserved

| Hold | Gate | Resume Trigger |
| --- | --- | --- |
| `hold-live-marketplace-demand` | `browser_read_only_session` | Explicit user approval for read-only browser validation. |
| `hold-live-terms-and-fees` | `legal_kyc_tax_payment` | Explicit user approval for legal/payment review. |
| `hold-public-listing-action` | `public_action_approval` | Explicit user approval after browser and legal/payment evidence. |
| `hold-account-or-payment-setup` | `account_payment_approval` | Explicit user approval after terms, KYC/tax, and payout risks are understood. |

## Route Details

### PromptBase

Ready local assets:

- `README.md`
- `templates/SKILL.template.md`
- `examples/local-research-skill/SKILL.md`
- `docs/listing-draft.md`
- `docs/buyer-guide.md`
- `docs/license-and-ip-note.md`
- `docs/screenshot-plan.md`

Local gaps:

- Create route-specific listing copy that avoids revenue and marketplace-approval claims.
- Prepare local screenshot placeholders from static files only.
- Map PromptBase prompt/skill submission rules after browser approval.
- Confirm payout route requirements through legal/payment review.

### Gumroad

Ready local assets:

- `docs/listing-draft.md`
- `docs/buyer-guide.md`
- `docs/screenshot-plan.md`
- `templates/service-request-checklist.template.md`
- `templates/gate-checklist.template.md`

Local gaps:

- Create Gumroad-style direct-download product page copy.
- Prepare local package preview images or static screenshot placeholders.
- Decide whether to create a zip only after internal package review.
- Review seller terms, refunds, payout, tax, and account obligations after legal/payment approval.

### Lemon Squeezy

Ready local assets:

- `docs/license-and-ip-note.md`
- `docs/listing-draft.md`
- `README.md`
- `templates/artifact-contract.template.md`
- `templates/acceptance-review.template.md`

Local gaps:

- Choose whether this is a one-time digital download, lead magnet, license, or subscription route.
- Create a tax/payment/legal question list for human review.
- Prepare refund/support language without making live obligations.
- Keep all payment and seller account work frozen.

## Boundary

This is local route eligibility only. It performs no marketplace browsing, no account work, no KYC/tax/payment work, no listing, no upload, no zip creation, no public action, no service-request mutation, no worker start, no runtime start, no dependency install, no MCP/model call, and no external side effect.

## Next Action

Prepare PromptBase-specific local listing and eligibility checklist from existing package files only; keep browser validation, seller terms, account setup, payout setup, zip/public upload, listing, and submission behind explicit approvals.
