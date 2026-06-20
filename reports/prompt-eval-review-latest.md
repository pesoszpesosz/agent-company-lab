# Agent Company Prompt/Eval/Review Registry

Generated UTC: 2026-06-14T12:23:05Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`

## Boundary

- Prompt records are not permission to run real model/API calls.
- Eval runs can be dry-run/manual until a model/API service request is approved.
- Human reviews record decisions; they do not bypass account, wallet, public-action, legal/KYC, security, or real-money gates.

## Counts

- Prompt templates: 1
- Prompt versions: 2
- Eval datasets: 1
- Eval runs: 2
- Human reviews: 0

## Prompt Templates

| Lane | Template | Owner | Purpose | Default Stop Gates |
| --- | --- | --- | --- | --- |
| `platform_engineering` | `lane-manager-startup-template` - Lane manager startup prompt | recovered-profitable-edge-infra | Canonical startup prompt for separate lane-manager Codex chats, with one-task-at-a-time workflow and side-effect gates. | account_registration; wallet_action; browser_public_action; legal_kyc_tax_billing; security_testing_or_submission; real_money_trade; public_pr_comment_or_bounty_submission; submitted_bounty_payout_lane |

## Prompt Versions

| Status | Lane | Version | Template | SHA256 | Source |
| --- | --- | --- | --- | --- | --- |
| active | `platform_engineering` | `lane-manager-startup-v2-20260614` - v2 2026-06-14 explicit approved-service-request coverage | `lane-manager-startup-template` - Lane manager startup prompt | `116eedc348fab642` | E:\agent-company-lab\reports\prompt-evals\manager-prompt-safety-local-eval-v2-20260614.md |
| superseded | `platform_engineering` | `lane-manager-startup-v1-20260614` - v1 2026-06-14 shell-safe manager startup prompt | `lane-manager-startup-template` - Lane manager startup prompt | `8f356ba586ae8263` | E:\agent-company-lab\reports\lane-manager-thread-launch-manifest-latest.md |

## Eval Datasets

| Lane | Dataset | Cases | Purpose |
| --- | --- | ---: | --- |
| `platform_engineering` | `manager-prompt-safety-cases-20260614` - Manager prompt safety cases | 6 | Static safety cases for separate lane-manager prompts: lane boundaries, service gates, artifact discipline, and no fake money claims. |

## Eval Runs

| Status | Score | Runtime | Dataset | Prompt Version | Lane | Artifact |
| --- | ---: | --- | --- | --- | --- | --- |
| pass | 1.0 | local_static_text_coverage | `manager-prompt-safety-cases-20260614` - Manager prompt safety cases | `lane-manager-startup-v2-20260614` | `platform_engineering` | E:\agent-company-lab\reports\prompt-evals\manager-prompt-safety-local-eval-v2-20260614.md |
| manual_static_pass | 1.0 | manual_static_coverage | `manager-prompt-safety-cases-20260614` - Manager prompt safety cases | `lane-manager-startup-v1-20260614` | `platform_engineering` | E:\agent-company-lab\reports\prompt-evals\manager-prompt-safety-manual-eval-20260614.md |

## Human Reviews

| Status | Decision | Lane | Review | Artifact | Trace | Prompt Version | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none |  |  |  |  |  |  |  |
