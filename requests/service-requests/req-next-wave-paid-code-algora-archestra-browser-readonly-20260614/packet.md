# Service Request Packet

Generated UTC: 2026-06-14T15:26:51Z

## Identity

- Request ID: `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614`
- Service ID: `browser_read_only_session`
- Request type: `browser_research`
- Lane: `paid_code_bounties`
- Requester agent: `recovered-profitable-edge-infra`
- Risk gate: `catalog_required_approval_no_external_action`
- Approval scope: 
- Related artifact: 

## Service Purpose

Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings.

## Requested Action

Read public Algora/GitHub issue state for archestra-ai/archestra#3218; no GitHub public action.

## Required Intake

| Field | Status | Value |
| --- | --- | --- |
| `lane_id` | present | paid_code_bounties |
| `target_url` | present | https://github.com/archestra-ai/archestra/issues/3218 |
| `allowed_read_scope` | present | Read public issue state, linked PRs, comments, claim history, acceptance terms, and Algora/GitHub bounty status for archestra-ai/archestra#3218. Capture whether it is clean, crowde |
| `forbidden_actions` | present | No login-required actions, comments, PRs, forks, branches, bounty claims, maintainer contact, reactions, issue edits, assignment requests, or payout monitoring. |
| `evidence_needed` | present | Markdown verification packet with source URLs, issue status, linked PR/comment/claim evidence, payout/acceptance rules, duplicate/crowding risk, and final decision: park or request |
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
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-next-wave-paid-code-algora-archestra-browser-readonly-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id paid_code_bounties --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read public Algora/GitHub issue state for archestra-ai/archestra#3218; no GitHub public action." --intake-file E:\agent-company-lab\requests\service-requests\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```

## Non-Approval Notice

This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.
