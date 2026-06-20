# Service Request Packet

Generated UTC: 2026-06-14T15:26:51Z

## Identity

- Request ID: `req-next-wave-digital-legal-payment-review-20260614`
- Service ID: `legal_kyc_tax_payment_gate`
- Request type: `legal_kyc_tax_payment`
- Lane: `digital_products_templates_plugins`
- Requester agent: `recovered-profitable-edge-infra`
- Risk gate: `legal_kyc_tax_payment_requires_user_decision_no_commitment`
- Approval scope: 
- Related artifact: 

## Service Purpose

Summarize legal, KYC, tax, billing, payment, and account-contract obligations before the user decides.

## Requested Action

Review legal/KYC/tax/payment/payout/account-contract gates for Agent Skill Starter Kit marketplace route; no commitments.

## Required Intake

| Field | Status | Value |
| --- | --- | --- |
| `lane_id` | present | digital_products_templates_plugins |
| `venue_url` | present | Gumroad, Lemon Squeezy, PromptBase, and any direct-download route identified by the local Agent Skill Starter Kit bundle. |
| `action_requested` | present | Review legal/KYC/tax/payment/payout/account-contract gates before any marketplace listing, seller signup, payment setup, or public sales claim for the Agent Skill Starter Kit. |
| `jurisdiction_if_relevant` | present | User location presumed United States unless user specifies otherwise; payment/tax review must ask the user before any commitment. |
| `funds_or_payout_involved` | present | Potential digital product revenue; no funds received and no payout setup approved. |
| `deadline` | present | No external deadline; review before any marketplace or seller-account action. |

## Allowed Actions

- Read public terms, privacy, fee, payout, tax, and eligibility pages.
- Identify commitments, documents, payments, personal data, and jurisdiction constraints.
- Write a decision packet with risks, alternatives, and user-only actions.
- Mark unresolved blockers in the service request.

## Hard Gates

- Do not accept terms, sign contracts, upload identity documents, enter tax forms, attach payment methods, subscribe, deposit, or withdraw.
- Do not provide legal, tax, or financial advice as a substitute for professional review.
- Do not proceed when obligations are unclear.

## Approval Required By

- `user`

## Expected Output Artifacts

- `legal-kyc-tax-payment-review.md`
- `terms-snapshot.md`
- `user-decision-checklist.md`

## Creation Command

Run this only after all required intake fields are present:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-next-wave-digital-legal-payment-review-20260614 --service-id legal_kyc_tax_payment_gate --request-type legal_kyc_tax_payment --lane-id digital_products_templates_plugins --risk-gate "legal_kyc_tax_payment_requires_user_decision_no_commitment" --requested-action "Review legal/KYC/tax/payment/payout/account-contract gates for Agent Skill Starter Kit marketplace route; no commitments." --intake-file E:\agent-company-lab\requests\service-requests\req-next-wave-digital-legal-payment-review-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```

## Non-Approval Notice

This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.
