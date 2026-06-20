# Agent Company Expansion Gap Map

Generated UTC: 2026-06-15T20:26:12Z
JSON mirror: `E:\agent-company-lab\reports\company-expansion-gap-map-latest.json`
Validation: `E:\agent-company-lab\reports\company-expansion-gap-map-validation-latest.json`

## Summary

- Active lanes scanned: `12`
- Owned active lanes: `11`
- Service catalog entries: `13`
- Owned lanes missing source specs: `0`
- Owned non-platform lanes missing evidence: `0`
- Parked service requests: `11`
- Read-only payout boundary preserved: `True`

## Lane Gap Rows

| Lane | Sources | Evidence | Parked Requests | Open Tasks | Traces | Gap Tags | Next Test |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `ai_ml_competitions` | 1 | 1 | 1 | 0 | 3 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `content_and_social_growth` | 1 | 1 | 1 | 0 | 4 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `digital_products_templates_plugins` | 1 | 1 | 3 | 0 | 8 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `lead_generation_and_sales` | 1 | 1 | 0 | 0 | 3 | create_next_narrow_manager_task | Draft non-spam offer rules, target filters, proof artifacts, and review gates before any outreach account or message action. |
| `local_trading_strategy_research` | 1 | 1 | 0 | 0 | 2 | create_next_narrow_manager_task | Inventory local backtest artifacts and define a paper-only evidence standard; no broker/API/trade action. |
| `money_source_discovery` | 1 | 1 | 1 | 0 | 6 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `paid_code_bounties` | 1 | 15 | 1 | 0 | 4 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `platform_engineering` | 3 | 2 | 2 | 0 | 117 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `prediction_market_research` | 1 | 9 | 0 | 0 | 3 | create_next_narrow_manager_task | Create a paper-only replay task for one imported market edge and define the data source of truth, fees, settlement timing, and no-trade gate. |
| `security_bounty_private_reports` | 1 | 19 | 2 | 0 | 4 | refresh_parked_service_requests, create_next_narrow_manager_task | Refresh the parked service-request review packet and keep action gated. |
| `submitted_bounty_payouts` | 0 | 21 | 0 | 0 | 0 | keep_read_only_external_owner_boundary | Keep read-only visibility; do not duplicate the external payout worker. |
| `web3_airdrops_grants_hackathons` | 1 | 1 | 0 | 0 | 3 | create_next_narrow_manager_task | Scout terms, deadlines, eligibility, and required account/wallet actions; stop before registration, wallet, deployment, or transaction work. |

## Boundary

- This report is local and report-only.
- It does not start browser sessions, register accounts, touch wallets or payments, perform public actions, run security tests, place trades, mutate service requests, assign workers, start workers, call APIs, or create external side effects.

## Next Action

Create source-spec seed packets for owned lanes with missing source specs, then refresh parked service-request review packets without side effects.

