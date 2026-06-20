# Source Freshness Scheduler Plan - 2026-06-15

Schema: `source_freshness_scheduler.v1`

Purpose: plan recurring current-source checks for the agent-company lab without executing browser, account, API/model, payment, public-action, wallet, security-testing, or real-money work.

## Execution Policy

This scheduler plan is not execution.

Allowed now:

- Read local files already present in `E:\agent-company-lab` and `E:\profit-edge-lab`.
- Read GitHub repository metadata with read-only `gh` commands when current architecture choices require it.
- Write local scheduler reports, task packets, and service-request plans.

Requires service approval:

- Browser read-only current-source checks.
- Signed-in research tools.
- Model/API-backed research.
- External scans that query paid-code, bounty, marketplace, or trading venues.
- Security scope verification beyond public documentation or public code review.

Prohibited:

- Account creation or login.
- Seller onboarding, marketplace listing, product upload, public post, PR comment, bounty claim, or report submission.
- Legal/KYC/tax/payment setup.
- Wallet setup, wallet connection, private-key handling, transactions, deposits, withdrawals, trades, or real-money actions.
- Acting on `submitted_bounty_payouts`, which remains owned by the parallel payout worker.

## Scheduled Source Classes

| Source | Lane | State | Next check | Mode | Output |
| --- | --- | --- | --- | --- | --- |
| `platform_infra_repo_metadata` | `platform_engineering` | fresh | 2026-06-21 | read-only GitHub metadata | `data\curated-infra-repos-refresh-YYYYMMDD.json` |
| `platform_official_docs_refresh` | `platform_engineering` | blocked until approval | 2026-06-21 | service request only | `reports\source-research-refresh-YYYYMMDD.md` |
| `digital_marketplace_terms` | `digital_products_templates_plugins` | blocked until approval | 2026-06-15 | service request only | `reports\digital-products-templates-plugins\marketplace-browser-readonly-capture-YYYYMMDD.md` |
| `money_source_discovery_current_sources` | `money_source_discovery` | blocked until approval | 2026-06-15 | service request only | `reports\money-source-discovery\source-freshness-capture-YYYYMMDD.md` |
| `paid_code_readonly_bounty_sources` | `paid_code_bounties` | blocked until approval | 2026-06-15 | service request only | `reports\paid-code-bounties\readonly-bounty-source-capture-YYYYMMDD.md` |
| `security_scope_rules` | `security_bounty_private_reports` | blocked until approval | 2026-06-15 | service request only | `reports\security-bounty-private-reports\scope-rules-readonly-capture-YYYYMMDD.md` |
| `prediction_market_data_sources` | `prediction_market_research` | manual only | 2026-06-16 | local file read | `reports\prediction-market-research\data-freshness-note-YYYYMMDD.md` |
| `profit_edge_daily_queue_snapshot` | `platform_engineering` | due | 2026-06-15 | local planning only | `reports\profit-edge-import-latest.md` |

## Immediate Routing

The only freshness work ready without approval is local planning over existing files and read-only metadata checks when a platform architecture choice needs it.

The highest-value blocked freshness work remains digital marketplace terms for Agent Skill Starter Kit v0. It already has `req-next-wave-digital-marketplace-browser-readonly-20260614` plus `execution-plan-v1`; no browser work starts until explicit approval.

## Gate State

- Browser actions performed: no.
- API/model calls performed: no.
- Account, seller, legal/KYC/tax/payment, wallet, public, or real-money actions performed: no.
- Service requests changed: no.
- `submitted_bounty_payouts` touched: no.
