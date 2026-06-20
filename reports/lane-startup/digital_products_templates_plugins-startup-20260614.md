# Digital Products Templates Plugins Startup Memo - 2026-06-14

Lane: `digital_products_templates_plugins`  
Department: Product Studio  
Manager agent: `lane-manager-digital_products_templates_plugins-019ec69a`  
Thread: `019ec69a-9fe3-7530-b83e-ae404554bca7`  
Task: `task-digital_products_templates_plugins-startup-20260614`  
Status: local planning and proof-artifact selection only  

## Scope Learned

The Product Studio lane starts as a local product-research and prototype lane. The existing Wave-4 packet says agents may build templates, prompt packs, skill packs, plugin prototypes, documentation, demos, screenshots, and launch packets, but distribution is medium-risk because it requires account, payment, tax, listing, and public-action approval.

The starter service request `req-wave4-digital-products-browser-readonly-20260614` is still `needs_review`. I did not start it, assign it, complete it, browse marketplace pages, open accounts, inspect signed-in pages, or perform any marketplace action. The request is useful as a field specification only: future approved browser research should capture product formats, pricing patterns, buyer problems, listing requirements, fees, and payment/account gates from public pages.

Startup commands found zero current source specs and zero lane evidence for this lane. The lane is now claimed by `lane-manager-digital_products_templates_plugins-019ec69a`, and this startup task is the only active Product Studio task.

## Local Sources Reviewed

- `E:\agent-company-lab\README.md`
- `E:\agent-company-lab\reports\manager-packets\digital_products_templates_plugins-manager-packet.md`
- `E:\agent-company-lab\requests\service-requests\req-wave4-digital-products-browser-readonly-20260614\packet.md`
- `E:\agent-company-lab\requests\service-requests\req-wave4-digital-products-browser-readonly-20260614\intake.json`
- `E:\agent-company-lab\reports\agent-company-money-path-wave4-20260614.md`
- `E:\agent-company-lab\data\money-path-source-registry-wave4-20260614.json`
- `E:\agent-company-lab\reports\wave4-manager-launch-plan-20260614.md`

The local registry names these representative source targets for later approved read-only verification:

- Gumroad: `https://gumroad.com/`
- Lemon Squeezy digital products: `https://www.lemonsqueezy.com/ecommerce/digital-products`
- PromptBase sell prompts/skills: `https://promptbase.com/sell`
- Notion Marketplace: `https://www.notion.com/templates`
- Shopify app revenue share: `https://shopify.dev/docs/apps/launch/distribution/revenue-share`

Fee numbers are not recorded as current evidence in the local files. Exact marketplace fee, payout, tax, merchant-of-record, processor, refund, and revenue-share terms must be verified later through an approved browser-read-only and/or legal/KYC/tax/payment service request before any listing, pricing, or payout decision.

## Opportunity Shortlist

| Rank | Product idea | Buyer problem | Build artifact | Route | Marketplace fees to verify | Payment/listing gates |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Agent Skill Starter Kit | Builders can write useful agent instructions but struggle to package gates, examples, eval checks, and deliverables into a reusable product. | Local template bundle with `SKILL.md`, gate checklist, service-request checklist, example workflow, README, and listing draft. | PromptBase skill route; Gumroad or Lemon Squeezy direct-download route. | PromptBase seller commission/payout rules; Gumroad platform and processor fees; Lemon Squeezy merchant-of-record, tax, processor, and payout fees. | Account registration, seller verification, payment/tax setup, public listing review, brand/trademark wording review, license/IP review. |
| 2 | Agent Ops Notion Dashboard | Solo operators running several AI agents need a simple place to track lanes, tasks, gates, evidence, outcomes, and next actions. | Notion-importable workspace spec plus CSV/Markdown seed tables and example dashboards. | Notion Marketplace; Gumroad or Lemon Squeezy template download. | Notion paid-template policy/fees/payout terms; Gumroad/Lemon Squeezy fees if sold outside Notion. | Notion creator account, payment details, marketplace submission, listing screenshots, public template review, no real customer data in examples. |
| 3 | First-Dollar Product Launch Packet Generator | Creators know what they can build but stall on packaging, pricing hypotheses, gate checklists, README/docs, and launch copy. | Local CLI or worksheet that emits product spec, listing draft, pricing matrix, refund/license checklist, and screenshot checklist. | Gumroad and Lemon Squeezy direct product. | Platform fee, payment processing, refunds, VAT/sales-tax handling, payout timing, file-hosting limits. | Seller account, tax/payment onboarding, terms acceptance, listing/public action approval, no earnings claims without evidence. |
| 4 | Prompt Pack QA and Eval Kit | Prompt sellers need lightweight proof that a pack is organized, testable, and not just a bundle of vague prompts. | Spreadsheet/Markdown eval rubric, prompt version table, example test cases, output-review checklist, and changelog template. | PromptBase; Gumroad or Lemon Squeezy. | PromptBase marketplace/link fee and payout rules; direct-store fees for Gumroad/Lemon Squeezy. | Marketplace terms review, prohibited-content review, no copied prompts, no model/API execution unless separately approved. |
| 5 | Shopify App Listing Readiness Kit | Small app/theme builders need a preflight checklist for docs, screenshots, support, privacy, billing, and review readiness. | Checklist/template packet for app listing copy, screenshots, support docs, privacy/billing notes, and release evidence. | Gumroad/Lemon Squeezy as a template product; Shopify partner route only after review. | Shopify partner/app revenue share and registration requirements; direct-store fees if sold as a checklist. | Shopify account/partner terms, public listing rules, legal/privacy review, no app submission or partner action without approval. |

## What I Will Test First

First local proof: `Agent Skill Starter Kit`.

Reason: it is closest to the lab's existing strengths, requires no marketplace account, can be built and reviewed entirely as local files, and has a plausible buyer problem for builders who want safer agent workflows. It can produce a concrete artifact before any distribution decision.

Saved proof packet:

- `E:\agent-company-lab\reports\digital-products-templates-plugins\agent-skill-starter-kit-proof-packet-20260614.md`

Recommended next task:

`Create local v0 product bundle: Agent Skill Starter Kit`

Evidence required:

`Local product folder with README, SKILL.md template, gate checklist, service-request checklist, example workflow, license/IP note, listing draft, and screenshot plan.`

Next action:

Build the v0 bundle locally and run a file-level acceptance check. Do not browse, list, upload, sell, or promote it.

## Stop Gates

- Do not start, assign, execute, or complete `req-wave4-digital-products-browser-readonly-20260614` unless the request is approved by the required reviewers.
- No browser research, marketplace page inspection, screenshot capture, DOM capture, or public-page fee verification under the unapproved service request.
- No marketplace account creation, login, signup, seller profile, creator profile, app/partner registration, or terms acceptance.
- No listing creation, listing draft upload, template submission, product upload, app submission, review request, public listing edit, or marketplace message.
- No purchase, payment setup, payout setup, bank/card/PayPal/Stripe details, merchant-of-record setup, billing settings, KYC, tax form, legal agreement, or account contract.
- No public promotion, post, comment, reply, DM, email, form submission, review, affiliate link, or outreach.
- No real-money action, revenue claim, expected-value claim as success, or `realized_usd` above zero without actual received funds.
- No model/API execution, paid compute, paid data, premium API, or external automation without the relevant approved service request.
- No use of copyrighted, trademarked, restricted, copied, or platform-prohibited assets unless license and attribution are reviewed.
- No private customer data, credentials, cookies, tokens, OTPs, wallet actions, or account settings.
- No GitHub payout, RustChain, Charles, submitted-bounty monitoring, bounty claim, PR comment, or unrelated lane work.

## Lane Record Fields

- Source: local README, manager packet, Wave-4 report, Wave-4 registry, launch plan, and unapproved browser-read-only service request packet.
- Hypothesis: a narrow agent-workflow template product can be proven locally before marketplace distribution gates, and it may be a better first Product Studio test than a broad Notion or Shopify product.
- Proof artifact: this startup memo and the saved Agent Skill Starter Kit proof packet.
- Blocker: exact marketplace fees, payout terms, listing terms, and seller requirements are not verified because the browser-read-only service request is still `needs_review`.
- Risk: stale fee assumptions, accidental listing/payment action, trademark/brand wording, copied assets, unsupported revenue claims, and cross-lane work.
- Next action: create the local v0 product bundle only, then request approved browser/legal/payment review before any marketplace decision.
