# Service Worker Human Decision Packet

Generated UTC: 2026-06-17T20:41:28Z
Request: `req-next-wave-digital-marketplace-browser-readonly-20260614`
Lane: `digital_products_templates_plugins`
Worker type: `browser_read_only`
Risk gate: `catalog_required_approval_no_external_action`

## Operating Rule

This packet is for human/CRO decision support only. It does not approve, reject, register, assign, update, start, browse, call APIs, post, submit, pay, trade, or contact anyone.

## Gate State

- Current blocking gate: `human_cro_approval_required`
- Review route: `ready_for_human_cro_review`
- Scope diff route: `missing_exact_scope`
- Scope compatible with packet: `False`
- Recommended worker pool: `service-worker-browser-read-only-pool`
- Pool status: `missing_service_worker_pool`

## Preconditions

| Check | Passed |
| --- | --- |
| `chain_integrity_all_checks_passed` | `True` |
| `service_status_needs_review` | `True` |
| `packet_valid` | `True` |
| `current_gate_human_cro_approval_required` | `True` |
| `manual_review_required` | `True` |
| `approve_preview_present` | `True` |
| `reject_preview_present` | `True` |

## Suggested Exact Scope

DRAFT ONLY - NOT APPROVED. For source service request `req-next-wave-digital-marketplace-browser-readonly-20260614` and worker request `swr-next-wave-digital-marketplace-browser-readonly-20260615`, allow `browser_read_only` worker activity only after separate explicit user/CRO approval. Objective: After explicit approval only, read public Gumroad, Lemon Squeezy, and PromptBase marketplace pages for terms, fees, payouts, listing requirements, refund constraints, prohibited content, and seller requirements relevant to Agent Skill Starter Kit. Allowed actions: Open public pages on allowed hosts after approval; Follow public help, documentation, pricing, fees, terms, refund, payout, seller, and prohibited-content links on allowed hosts; Record source URLs and page titles; Summarize factual marketplace requirements with short compliant excerpts only; Capture local Markdown notes and optional screenshots Allowed hosts: gumroad.com; www.lemonsqueezy.com; lemonsqueezy.com; promptbase.com Starting URLs: https://gumroad.com/; https://www.lemonsqueezy.com/ecommerce/digital-products; https://promptbase.com/sell Allowed data: public marketing page text; public help/documentation page text; public page title; public URL; local screenshot if approval permits browser capture Required outputs: E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-browser-readonly-capture-20260614.md; E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-browser-readonly-route-comparison-20260614.json; E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-browser-readonly-blocker-note-20260614.md Hard denials: no credentials, OTPs, secrets, private files, private data, payment details, tax/KYC data, or wallet data; no login, signup, account creation, account settings changes, or terms/legal acceptance; no payments, purchases, deposits, withdrawals, trades, wallet connections, wallet signatures, or real-money action; no public posts, comments, replies, messages, listings, uploads, form submissions, issue/PR actions, or external contact; no external side effects, API/provider/model calls, paid cost, worker start, or queue mutation unless separately approved in an exact scope; no bypassing paywalls, rate limits, access controls, platform rules, or the packet stop conditions; login; signup; seller onboarding; terms acceptance; listing creation; product upload; payment setup; tax form entry; KYC form entry; purchase; public promotion; comments or messages; saving settings; submitting forms; entering credentials, OTPs, payment details, personal data, private files, or wallet information; using signed-in pages; bypassing paywalls, rate limits, access controls, or platform rules Stop conditions: The source service request is not approved and assigned; Any page asks for login, signup, account creation, seller onboarding, consent acceptance, payment, tax, KYC, private data, credentials, OTP, wallet action, or file upload; A required page is not public or requires a signed-in state; A link leaves the allowed hosts; The browser worker cannot distinguish public guidance from contractual acceptance; The task would require a public action, marketplace listing, or real-money/payment action Max cost USD: 0. This draft expires unless separately approved with `approve-service-request`; this report grants no approval, assignment, start authority, browser action, API call, public action, payment, trade, submission, or external side effect.

## Approve Preview

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "approve-service-request",
  "--request-id",
  "req-next-wave-digital-marketplace-browser-readonly-20260614",
  "--approved-by",
  "USER_OR_CRO",
  "--exact-scope",
  "REPLACE_WITH_MANUALLY_REVIEWED_EXACT_SCOPE_FROM_SUGGESTED_SCOPE",
  "--decision-note",
  "Manual approval after reviewing packet, risk gate, exact scope, and stop conditions."
]
```

## Reject Preview

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "reject-service-request",
  "--request-id",
  "req-next-wave-digital-marketplace-browser-readonly-20260614",
  "--rejected-by",
  "USER_OR_CRO",
  "--reason",
  "Manual rejection after reviewing packet, risk gate, exact scope, and stop conditions."
]
```

## Next Action

Human/CRO must review the packet, risk gate, exact scope, gate map, and current external context before running any approve/reject command manually.

