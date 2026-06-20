# Service Worker Request v1

Generated UTC: 2026-06-14T21:59:06Z

- Worker request ID: `swr-next-wave-digital-legal-payment-review-20260614`
- Source service request: `req-next-wave-digital-legal-payment-review-20260614`
- Worker type: `legal_kyc_tax_payment_review`
- Lane: `digital_products_templates_plugins`
- Status: `needs_review`
- Risk gate: `legal_kyc_tax_payment_requires_user_decision_no_commitment`

## Non-Approval Notice

This backfill artifact grants no approval and performs no execution. It only converts the current service request row into the service_worker_request.v1 contract.

## Objective

Review legal, KYC, tax, payment, and seller-account requirements for req-next-wave-digital-legal-payment-review-20260614 as a local decision packet only; make no commitments and enter no private data.

## Allowed Actions

- prepare local review notes
- identify required legal, tax, KYC, payment, seller, and contractual decisions
- produce questions for the user/CRO

## Prohibited Actions

- execute without explicit approval
- login unless explicitly approved
- signup or account creation
- accept terms or legal agreements
- enter credentials, OTPs, personal data, private files, payment details, tax/KYC data, or wallet information
- submit forms
- publish, post, reply, comment, message, list, upload, or contact external parties
- purchase, deposit, withdraw, trade, connect wallet, sign wallet messages, or perform real-money actions
- change account settings
- bypass paywalls, rate limits, access controls, or platform rules
