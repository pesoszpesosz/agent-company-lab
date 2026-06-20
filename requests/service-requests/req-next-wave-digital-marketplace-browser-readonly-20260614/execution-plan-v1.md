# Service Request Execution Plan - Digital Marketplace Browser Read-Only

Request: `req-next-wave-digital-marketplace-browser-readonly-20260614`

Schema: `service_request_execution_plan.v1`

Status snapshot: `needs_review`

This plan is not an approval and does not start the browser service.

## Objective

After explicit approval only, a browser worker may read public marketplace terms, fees, payout, listing, prohibited-content, refund, file-delivery, and seller-requirement pages for the Agent Skill Starter Kit direct-download route.

## Allowed Scope

Allowed hosts:

- `gumroad.com`
- `www.lemonsqueezy.com`
- `lemonsqueezy.com`
- `promptbase.com`

Starting URLs:

- `https://gumroad.com/`
- `https://www.lemonsqueezy.com/ecommerce/digital-products`
- `https://promptbase.com/sell`

Allowed actions:

- Open public pages.
- Follow public documentation or help links on allowed hosts.
- Record source URLs and page titles.
- Summarize terms, fees, payout rules, listing requirements, refund rules, file-delivery constraints, and prohibited-content constraints.
- Capture local Markdown notes and optional screenshots.

## Prohibited Actions

- No login or signup.
- No seller onboarding.
- No terms acceptance.
- No listing creation or product upload.
- No payment setup.
- No tax or KYC form entry.
- No purchase.
- No public promotion.
- No comments or messages.
- No settings changes.
- No credential, OTP, payment, personal data, private file, or wallet entry.
- No signed-in pages.
- No bypassing paywalls, rate limits, access controls, or platform rules.

## Stop Conditions

Stop immediately if any page asks for login, signup, account creation, seller onboarding, consent acceptance, payment, tax, KYC, private data, credentials, OTP, wallet action, or file upload.

Stop if a page is not public, requires a signed-in state, leaves the allowed hosts, or requires a public/marketplace/real-money action.

## Execution Steps

1. Preflight: verify the request is explicitly approved and assigned. If it is still `needs_review`, do not open a browser.
2. Gumroad public review: capture public fee, payout, seller, prohibited-content, refund, and file-delivery evidence.
3. Lemon Squeezy public review: capture public digital product, merchant/payment/tax, fee, payout, seller, prohibited-content, refund, and file-delivery evidence.
4. PromptBase public review: capture accepted product type, seller, review, fee/payout, prohibited-content, and eligibility evidence.
5. Route comparison: recommend the first route using only captured public evidence and list remaining gates.

## Expected Outputs

- `E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-browser-readonly-capture-20260614.md`
- `E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-browser-readonly-route-comparison-20260614.json`
- Optional blocker note: `E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-browser-readonly-blocker-note-20260614.md`

## Current Gate State

- Request approval: not granted.
- Browser action: not performed.
- Account/seller action: not allowed.
- Legal/KYC/tax/payment action: not allowed.
- Public listing/action: not allowed.
- Real-money action: not allowed.
