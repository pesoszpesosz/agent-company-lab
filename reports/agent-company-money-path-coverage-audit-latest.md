# Agent Company Money-Path Coverage Audit

Generated UTC: 2026-06-20T12:52:17Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-money-path-coverage-audit-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-money-path-coverage-audit-validation-latest.json`

## Summary

- Active lanes: `12`
- Owned active lanes: `11`
- Source specs: `13`
- Thin-evidence actionable lanes, threshold <= 1: `0`
- Parked service requests: `13`
- Read-only payout boundary preserved: `True`

## CEO Dispatch Order

| Rank | Lane | Agent | Evidence | Gate | First Task | Required Proof |
| ---: | --- | --- | ---: | --- | --- | --- |

## Full Lane Coverage

| Lane | Sources | Evidence | Tasks | Requests | Traces | Coverage | Urgency | Next Agent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ai_ml_competitions` | 1 | 9 | 17 | 1 | 17 | 25 | 5 | `competition_scout` |
| `content_and_social_growth` | 1 | 2 | 6 | 1 | 7 | 11 | 3 | `trend_scout` |
| `digital_products_templates_plugins` | 1 | 22 | 38 | 4 | 20 | 27 | 3 | `market_gap_scout` |
| `lead_generation_and_sales` | 1 | 5 | 12 | 0 | 11 | 18 | 0 | `offer_builder` |
| `local_trading_strategy_research` | 1 | 2 | 4 | 0 | 3 | 10 | 0 | `strategy_miner` |
| `money_source_discovery` | 1 | 7 | 15 | 1 | 15 | 21 | 5 | `source_mapper` |
| `paid_code_bounties` | 1 | 22 | 14 | 2 | 17 | 27 | 3 | `repo_triager` |
| `platform_engineering` | 3 | 95 | 434 | 2 | 374 | 33 | 3 | `control_plane_builder` |
| `prediction_market_research` | 1 | 9 | 8 | 0 | 8 | 26 | 0 | `market_scout` |
| `security_bounty_private_reports` | 1 | 20 | 17 | 2 | 19 | 27 | 3 | `program_rules_reader` |
| `submitted_bounty_payouts` | 0 | 21 | 1 | 0 | 1 | 21 | 0 | `payout_monitor` |
| `web3_airdrops_grants_hackathons` | 1 | 5 | 12 | 0 | 11 | 18 | 2 | `program_scout` |

## Boundary

- This audit is local and report-only except for recording its own task, evidence, artifacts, and trace row.
- It does not start browser sessions, register accounts, touch wallets or payments, perform public actions, run security tests, place trades, mutate service requests, assign workers, start workers, call APIs, or create external side effects.

## Next Action

Launch/report the six undercovered money lanes as read-only or local-proof research waves before adding more platform approval plumbing.

