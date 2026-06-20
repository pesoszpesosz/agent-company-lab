# Algora / Comet Opik Read-Only Refresh Service Request

- Generated: `2026-06-18T08:11:48Z`
- Task: `task-algora-opik-readonly-refresh-service-request-20260618`
- Request: `req-algora-opik-readonly-refresh-20260618`
- Service: `browser_read_only_session`
- Status: `needs_review`
- Decision: `create_needs_review_service_request_only_no_browser_or_public_action`
- Validation: `True` with `0` failures

## Requested Action

Read public Comet/Opik, Algora, and GitHub status for Opik bounty reopening; no claim, PR, account, CLA, payout, or public action.

## Intake

- `lane_id`: paid_code_bounties
- `target_url`: https://www.comet.com/docs/opik/contributing/developer-programs/bounties ; https://algora.io/ ; https://github.com/comet-ml/opik
- `allowed_read_scope`: Public pages only. Check whether the Opik bounty program is still paused, whether any public Algora/Comet bounty board shows open Opik issues, and whether linked GitHub issues/PRs/comments show duplicate, assigned, claimed, solved, or unclear status. Capture URLs, titles, timestamps, short paraphrased status notes, explicit amount/claim-state evidence, and a park/proceed-local-triage recommendation.
- `forbidden_actions`: No login, signup, CLA acceptance, Algora claim, GitHub comment, fork, branch, PR, issue edit, reaction, maintainer contact, assignment request, bounty reservation, payout/payment/KYC/tax setup, target testing, repository mutation, model/MCP calls, worker/runtime starts, or browser actions beyond approved public reading.
- `evidence_needed`: Algora/Comet Opik read-only refresh report with program-open status, bounty amount/state, duplicate/claim/PR risk, CLA/payment gates, and decision: still parked, local triage only, or request later public-action/legal-payment approval.
- `session_sensitivity`: public_pages_only_no_signed_in_session

## Source Decision

- `no_go_external_claim`: Comet/Opik bounty program is currently paused in the public docs; local fixtures remain useful for parser/checklist readiness, but no claim/comment/PR/payout path is clean.

## Required Before Execution

- Human/operator review of this exact request.
- Chief risk officer approval for public read-only scope.
- A signed decision packet that permits assignment preflight only.
- Post-action local receipt and chain-integrity refresh if later executed.

## Boundary

- `service_requests_created`: `1`
- `service_requests_approved`: `0`
- `service_requests_assigned`: `0`
- `service_requests_started`: `0`
- `service_requests_completed`: `0`
- `browser_sessions_started`: `0`
- `live_algora_fetch`: `False`
- `live_github_fetch`: `False`
- `accounts_or_logins`: `0`
- `cla_or_terms_accepted`: `False`
- `github_comments_claims_prs_or_forks`: `0`
- `payout_or_payment_actions`: `0`
- `security_testing`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Next Action

Leave this request in needs_review. Do not assign, start, approve, or execute it until a later exact signed decision permits a public read-only Opik/Algora refresh.
