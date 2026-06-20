# Kalshi Public-Data Paper Signal Checker

- Generated: `2026-06-18T08:39:46Z`
- Task: `task-kalshi-public-data-paper-signal-checker-v1-20260618`
- Status: `kalshi_public_data_paper_signal_checker_complete_local_only`
- Decision: `zero_promotable_candidates_paper_only_no_trade_no_account`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\prediction-market-research\kalshi-public-data-paper-signal-checker-v1-fixture-20260618.json`
- Results: `E:\agent-company-lab\reports\prediction-market-research\kalshi-public-data-paper-signal-checker-v1-results-20260618.json`

## Summary

- `row_count`: `4`
- `promotable_count`: `0`
- `killed_count`: `4`
- `aggregate_kill_reason_count`: `11`

## Paper Rows

| Ticker | Decision | Spread | Drift | Kill Reasons |
| --- | --- | ---: | ---: | --- |
| `KXBTC-20260618-105000` | `kill` | 8 | 1 | `account_or_jurisdiction_eligibility_unverified`, `fees_unverified`, `max_loss_not_defined`, `official_settlement_source_unverified`, `orderbook_depth_unverified`, `pre_close_without_result`, `real_money_gate_absent` |
| `KXOLD-20260617-FINAL` | `kill` | 1 | 1 | `account_or_jurisdiction_eligibility_unverified`, `fees_unverified`, `inactive_or_finalized_market`, `low_liquidity_or_missing_liquidity`, `max_loss_not_defined`, `orderbook_depth_unverified`, `real_money_gate_absent`, `terminal_quotes_no_edge` |
| `KXTHIN-20260618` | `kill` | 60 | 0 | `account_or_jurisdiction_eligibility_unverified`, `block_trade_activity_not_executable_depth`, `fees_unverified`, `low_liquidity_or_missing_liquidity`, `max_loss_not_defined`, `official_settlement_source_unverified`, `orderbook_depth_unverified`, `pre_close_without_result`, `real_money_gate_absent` |
| `KXPOSTCLOSE-20260618` | `kill` | 4 | 6 | `account_or_jurisdiction_eligibility_unverified`, `fees_unverified`, `max_loss_not_defined`, `official_settlement_source_unverified`, `orderbook_depth_unverified`, `pre_close_without_result`, `real_money_gate_absent` |

## Aggregate Kill Reasons

- `account_or_jurisdiction_eligibility_unverified`
- `block_trade_activity_not_executable_depth`
- `fees_unverified`
- `inactive_or_finalized_market`
- `low_liquidity_or_missing_liquidity`
- `max_loss_not_defined`
- `official_settlement_source_unverified`
- `orderbook_depth_unverified`
- `pre_close_without_result`
- `real_money_gate_absent`
- `terminal_quotes_no_edge`

## Boundary

- `fixture_rows_created`: `4`
- `paper_rows_emitted`: `4`
- `promotable_candidates`: `0`
- `browser_sessions_started`: `0`
- `kalshi_account_or_login`: `False`
- `api_key_created_or_used`: `False`
- `signed_api_requests`: `0`
- `market_data_api_calls`: `0`
- `orderbook_api_calls`: `0`
- `orders_or_trades`: `0`
- `deposits_or_withdrawals`: `0`
- `payments_or_wallets`: `0`
- `real_money_actions`: `0`
- `public_actions`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Next Local Action

Add a historical-settled replay fixture with verified settlement values and keep the checker pessimistic until fees, depth, eligibility, official source, and max-loss fields are proven. Keep account, API keys, signed requests, orderbook depth, trades, deposits, withdrawals, payments, worker/runtime, and real-money gates blocked.
