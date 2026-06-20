# Service Request Packet

Generated UTC: 2026-06-14T14:37:52Z

## Identity

- Request ID: `req-wave4-money-source-discovery-browser-readonly-20260614`
- Service ID: `browser_read_only_session`
- Request type: `browser_research`
- Lane: `money_source_discovery`
- Requester agent: `recovered-profitable-edge-infra`
- Risk gate: `catalog_required_approval_no_external_action`
- Approval scope: 
- Related artifact: 

## Service Purpose

Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings.

## Requested Action

Read public opportunity-source directories and capture monetizable source candidates; no browser side effects.

## Required Intake

| Field | Status | Value |
| --- | --- | --- |
| `lane_id` | present | money_source_discovery |
| `target_url` | present | https://github.com/topics/bounty |
| `allowed_read_scope` | present | Public pages only. Identify monetizable source registries, bounty directories, competition directories, grant listings, and marketplace opportunity indexes. Capture URLs and rules |
| `forbidden_actions` | present | No login, signup, account creation, application, claim, comment, message, payment, API key, scraping against rules, or public action. |
| `evidence_needed` | present | A local source-discovery capture note with candidate URLs, monetization path, account gates, and first proof task per candidate. |
| `session_sensitivity` | present | public_read_only |

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
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-wave4-money-source-discovery-browser-readonly-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id money_source_discovery --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read public opportunity-source directories and capture monetizable source candidates; no browser side effects." --intake-file E:\agent-company-lab\requests\service-requests\req-wave4-money-source-discovery-browser-readonly-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```

## Non-Approval Notice

This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.
