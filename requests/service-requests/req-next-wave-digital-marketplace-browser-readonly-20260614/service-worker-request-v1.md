# Service Worker Request v1

Generated UTC: 2026-06-14T21:59:06Z

- Worker request ID: `swr-next-wave-digital-marketplace-browser-readonly-20260615`
- Source service request: `req-next-wave-digital-marketplace-browser-readonly-20260614`
- Worker type: `browser_read_only`
- Lane: `digital_products_templates_plugins`
- Status: `needs_review`
- Risk gate: `catalog_required_approval_no_external_action`

## Non-Approval Notice

This backfill artifact grants no approval and performs no execution. It only converts the current service request row into the service_worker_request.v1 contract.

## Objective

After explicit approval only, read public Gumroad, Lemon Squeezy, and PromptBase marketplace pages for terms, fees, payouts, listing requirements, refund constraints, prohibited content, and seller requirements relevant to Agent Skill Starter Kit.

## Allowed Actions

- Open public pages on allowed hosts after approval
- Follow public help, documentation, pricing, fees, terms, refund, payout, seller, and prohibited-content links on allowed hosts
- Record source URLs and page titles
- Summarize factual marketplace requirements with short compliant excerpts only
- Capture local Markdown notes and optional screenshots

## Prohibited Actions

- login
- signup
- seller onboarding
- terms acceptance
- listing creation
- product upload
- payment setup
- tax form entry
- KYC form entry
- purchase
- public promotion
- comments or messages
- saving settings
- submitting forms
- entering credentials, OTPs, payment details, personal data, private files, or wallet information
- using signed-in pages
- bypassing paywalls, rate limits, access controls, or platform rules
