# Agent Skill Starter Kit Proof Packet - 2026-06-14

Lane: `digital_products_templates_plugins`  
Parent task: `task-digital_products_templates_plugins-startup-20260614`  
Status: local proof packet only  

## Product Hypothesis

Builders who use AI coding agents need reusable skill and workflow templates that include practical action gates, acceptance checks, examples, and artifact discipline. A compact starter kit can save them time and reduce accidental public/account/payment actions.

This is not a listing and not a revenue claim. It is the first local proof artifact for deciding whether a buildable product exists.

## Target Buyer

- Indie builders using AI coding agents for repeatable workflows.
- Small teams experimenting with local agent operating procedures.
- Technical operators who want safer task packets before delegating work.

Excluded first:

- Enterprises needing legal/compliance customization.
- Users expecting managed service, credentials handling, or guaranteed marketplace results.
- Buyers who need platform-specific support that requires signed-in account inspection.

## Buyer Problem

The buyer can write ad hoc prompts, but packaging a reusable workflow is harder:

- unclear `SKILL.md` structure;
- missing stop gates for accounts, payments, public actions, credentials, and APIs;
- no acceptance checklist;
- no example artifact contract;
- no lightweight eval or review template;
- no listing or documentation draft.

## Local Build Artifact

Proposed v0 folder:

```text
agent-skill-starter-kit/
  README.md
  templates/
    SKILL.template.md
    gate-checklist.template.md
    service-request-checklist.template.md
    artifact-contract.template.md
    acceptance-review.template.md
  examples/
    local-research-skill/
      SKILL.md
      sample-output.md
  docs/
    buyer-guide.md
    license-and-ip-note.md
    screenshot-plan.md
    listing-draft.md
```

Acceptance checks:

- all files are local Markdown;
- no external API calls;
- no browser actions;
- no credentials or private data;
- gate checklist includes account, payment, legal/KYC/tax, public action, model/API, data purchase, and secrets handling;
- examples use fictional or local-only scenarios;
- listing draft avoids guaranteed revenue, platform endorsement, and unsupported claims.

## Marketplace Routes And Fee Gates

| Route | Fit | Fee status | Gate |
| --- | --- | --- | --- |
| PromptBase | Local registry says PromptBase advertises selling prompts and agent `skill.md` files. | Current marketplace fees, payout thresholds, seller terms, accepted formats, and review rules are not verified locally. | Requires approved browser-read-only review plus listing/public-action approval before submission. |
| Gumroad | Direct digital-download route for a Markdown/template bundle. | Current platform, processor, refund, tax, and payout terms are not verified locally. | Requires account, legal/KYC/tax/payment review, listing approval, and public-action approval. |
| Lemon Squeezy | Direct product route with merchant-of-record possibility. | Current merchant-of-record fee, tax handling, payout, refund, and file-delivery rules are not verified locally. | Requires account, payment/tax review, listing approval, and public-action approval. |
| Notion Marketplace | Secondary route if kit becomes a Notion workspace later. | Current paid-template and payout terms are not verified locally. | Not first route; requires separate Notion template build and marketplace review. |
| Shopify app/theme ecosystem | Poor first fit for this specific product. | Revenue-share and registration terms require later verification. | Excluded from v0 distribution. |

## Price Hypothesis

Local planning range only: USD 9 to 29 depending on completeness, examples, and screenshots. This is not a revenue forecast and not a sale claim.

## First Local Build Task

Create the v0 bundle under a local working directory, then record a proof artifact if the files are complete.

Suggested task:

`task-digital_products_templates_plugins-agent-skill-starter-kit-v0-20260614`

Evidence required:

`README, templates, one fictional example, listing draft, screenshot plan, and acceptance checklist saved locally.`

Hard stop:

Do not publish, upload, sell, submit, promote, message, or create accounts. Do not verify marketplace fees until `req-wave4-digital-products-browser-readonly-20260614` or a replacement service request is approved.
