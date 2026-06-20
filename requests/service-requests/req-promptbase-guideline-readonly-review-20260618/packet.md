# PromptBase Read-Only Guideline Review Service Request

- Generated: `2026-06-18T08:00:36Z`
- Task: `task-promptbase-guideline-readonly-service-request-20260618`
- Request: `req-promptbase-guideline-readonly-review-20260618`
- Service: `browser_read_only_session`
- Status: `needs_review`
- Decision: `create_needs_review_service_request_only_no_browser_execution`
- Validation: `True` with `0` failures

## Requested Action

Review public PromptBase guideline/seller pages for Agent Skill Starter Kit v0; no browser side effects.

## Source Approval Packet

- Approval: `approval-promptbase-readonly-guideline-review`
- Gate: `browser_read_only_session`
- Purpose: Compare current PromptBase public seller, support, prompt-guideline, terms, and homepage pages against the local package.

## Intake

- `lane_id`: digital_products_templates_plugins
- `target_url`: https://promptbase.com/sell ; https://promptbase.com/prompt-engineering-guide ; https://promptbase.com/marketplace
- `allowed_read_scope`: Public PromptBase pages only. Read seller, support, prompt-guideline, terms, homepage, marketplace category, and product-format guidance relevant to Agent Skill Starter Kit v0. Capture URLs, page titles, timestamps, short paraphrased rule notes, and file-by-file package implications into a local artifact only.
- `forbidden_actions`: No login, signup, account creation, seller onboarding, terms acceptance, listing save, listing creation, upload, submission, checkout, purchase, comments, messages, profile edits, payout setup, tax/KYC forms, public promotion, model/MCP calls, worker/runtime starts, or browser actions beyond approved public reading.
- `evidence_needed`: PromptBase guideline mapping report with every package file marked pass, edit-needed, blocked, or not-applicable; include source URLs, date/time observed, unsupported claims, file-format/category requirements, and next gate recommendation.
- `session_sensitivity`: public_pages_only_no_signed_in_session

## Required Before Execution

- Human/operator review of this exact request.
- Chief risk officer approval for the exact read-only scope.
- A signed decision packet that permits assignment preflight only.
- Post-action local receipt and chain-integrity refresh if later executed.

## Boundary

- `service_requests_created`: `1`
- `service_requests_approved`: `0`
- `service_requests_assigned`: `0`
- `service_requests_started`: `0`
- `service_requests_completed`: `0`
- `browser_sessions_started`: `0`
- `accounts_created`: `0`
- `logins_performed`: `0`
- `terms_accepted`: `0`
- `uploads_or_marketplace_drafts`: `0`
- `submissions_or_public_actions`: `0`
- `payments_payouts_kyc_tax_actions`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Next Action

Leave the request in needs_review. Do not assign, start, approve, or execute it until a later exact signed decision permits a read-only PromptBase browser session.
