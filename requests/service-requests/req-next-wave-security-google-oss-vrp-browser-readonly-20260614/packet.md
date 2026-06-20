# Service Request Packet

Generated UTC: 2026-06-14T15:26:51Z

## Identity

- Request ID: `req-next-wave-security-google-oss-vrp-browser-readonly-20260614`
- Service ID: `browser_read_only_session`
- Request type: `browser_research`
- Lane: `security_bounty_private_reports`
- Requester agent: `recovered-profitable-edge-infra`
- Risk gate: `catalog_required_approval_no_external_action`
- Approval scope: 
- Related artifact: 

## Service Purpose

Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings.

## Requested Action

Read public Google OSS VRP rendered rules/scope/submission route for rules_android; no account or submission action.

## Required Intake

| Field | Status | Value |
| --- | --- | --- |
| `lane_id` | present | security_bounty_private_reports |
| `target_url` | present | https://bughunters.google.com/open-source-security |
| `allowed_read_scope` | present | Read public Google OSS VRP rendered rules/scope/safe-harbor/submission-route text relevant to bazelbuild/rules_android. Capture whether rules_android appears in scope, reward/safe- |
| `forbidden_actions` | present | No login, account creation, report submission, OAuth, public comment, PR, issue, exploit attempt, live target testing, private data, or payout chasing. |
| `evidence_needed` | present | Markdown rules-route review with source URLs, scope status, safe-harbor text summary, submission route, account requirements, and decision: submit-gate-ready, local-repro-needed, o |
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
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-next-wave-security-google-oss-vrp-browser-readonly-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id security_bounty_private_reports --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read public Google OSS VRP rendered rules/scope/submission route for rules_android; no account or submission action." --intake-file E:\agent-company-lab\requests\service-requests\req-next-wave-security-google-oss-vrp-browser-readonly-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```

## Non-Approval Notice

This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.
