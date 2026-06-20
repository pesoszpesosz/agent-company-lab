# Service Request Packet

Generated UTC: 2026-06-14T15:26:51Z

## Identity

- Request ID: `req-next-wave-digital-marketplace-browser-readonly-20260614`
- Service ID: `browser_read_only_session`
- Request type: `browser_research`
- Lane: `digital_products_templates_plugins`
- Requester agent: `recovered-profitable-edge-infra`
- Risk gate: `catalog_required_approval_no_external_action`
- Approval scope: 
- Related artifact: 

## Service Purpose

Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings.

## Requested Action

Read public digital marketplace terms/fees/listing requirements for Agent Skill Starter Kit route; no browser side effects.

## Required Intake

| Field | Status | Value |
| --- | --- | --- |
| `lane_id` | present | digital_products_templates_plugins |
| `target_url` | present | https://gumroad.com/ ; https://www.lemonsqueezy.com/ecommerce/digital-products ; https://promptbase.com/sell |
| `allowed_read_scope` | present | Read public marketplace terms, fees, payout, listing, prohibited-content, refund, file-delivery, and seller-requirement pages relevant to the Agent Skill Starter Kit route. Capture |
| `forbidden_actions` | present | No login, signup, seller onboarding, terms acceptance, listing creation, product upload, payment setup, tax/KYC forms, purchase, public promotion, comments, messages, or browser ac |
| `evidence_needed` | present | Markdown capture with source URLs, fee/payout/listing requirements, account/payment/legal gates, IP/content risks, and recommendation: Gumroad vs Lemon Squeezy vs PromptBase for la |
| `session_sensitivity` | present | public_pages_only_no_signed_in_session |

## Allowed Actions

- Open public pages and read visible information.
- Use signed-in pages only when the service request names the site and allowed read scope.
- Capture screenshots, URLs, DOM text, and local notes.
- Stop if a page requires credentials, OTP, consent, payment, account settings, or private data.

## Hard Gates

- Do not click submit, publish, apply, buy, trade, follow, like, reply, repost, withdraw, deposit, connect wallet, or save settings.
- Do not enter credentials, OTPs, payment details, personal data, or wallet signatures.
- Do not bypass rate limits, paywalls, access controls, or platform rules.

## Approval Required By

- `requesting_manager`
- `chief_risk_officer`

## Expected Output Artifacts

- `browser-readonly-capture.md`
- `screenshots`
- `blocker-note.md`

## Creation Command

Run this only after all required intake fields are present:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-next-wave-digital-marketplace-browser-readonly-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id digital_products_templates_plugins --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read public digital marketplace terms/fees/listing requirements for Agent Skill Starter Kit route; no browser side effects." --intake-file E:\agent-company-lab\requests\service-requests\req-next-wave-digital-marketplace-browser-readonly-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```

## Non-Approval Notice

This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.
