# Service Worker Request v1

Generated UTC: 2026-06-14T21:59:06Z

- Worker request ID: `swr-grok-research-worker-20260614`
- Source service request: `req-grok-research-worker-20260614`
- Worker type: `browser_signed_in_read_only`
- Lane: `platform_engineering`
- Status: `needs_review`
- Risk gate: `browser_grok_or_x_requires_signed_in_browser_and_no_public_actions`

## Non-Approval Notice

This backfill artifact grants no approval and performs no execution. It only converts the current service request row into the service_worker_request.v1 contract.

## Objective

After explicit approval only, run a signed-in read-only research enrichment worker for req-grok-research-worker-20260614; capture research notes and perform no public X/Grok action, account setting change, or message/post/reply.

## Allowed Actions

- after explicit approval, inspect approved signed-in research surface in read-only mode
- capture local notes and source references
- avoid likes, follows, replies, posts, settings, messages, and account changes

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
