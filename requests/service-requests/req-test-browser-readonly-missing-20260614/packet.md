# Service Request Packet

Generated UTC: 2026-06-14T14:31:37Z

## Identity

- Request ID: `req-test-browser-readonly-missing-20260614`
- Service ID: `browser_read_only_session`
- Request type: `browser_research`
- Lane: `content_and_social_growth`
- Requester agent: `test-manager`
- Risk gate: `catalog_required_approval_no_external_action`
- Approval scope: 
- Related artifact: 

## Service Purpose

Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings.

## Requested Action

Read-only capture acceptance test; no browser opened.

## Required Intake

| Field | Status | Value |
| --- | --- | --- |
| `lane_id` | present | content_and_social_growth |
| `target_url` | missing |  |
| `allowed_read_scope` | missing |  |
| `forbidden_actions` | missing |  |
| `evidence_needed` | missing |  |
| `session_sensitivity` | missing |  |

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
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-test-browser-readonly-missing-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id content_and_social_growth --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read-only capture acceptance test; no browser opened." --intake-file E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-missing-20260614\intake.json
```

## Non-Approval Notice

This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.
