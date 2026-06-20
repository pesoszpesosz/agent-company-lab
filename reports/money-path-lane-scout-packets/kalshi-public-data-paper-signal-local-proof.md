# Kalshi Public Data Paper Signal Local Proof

Generated UTC: 2026-06-18T06:47:23Z
Task: `task-lane-scout-kalshi_public_market_data-20260618`
Lane: `prediction_market_research`

Purpose: define a Kalshi public-data paper-signal route for local prediction-market research. This is not a Kalshi account, API key, signed request, orderbook-depth call, trade, deposit, withdrawal, payment, worker/runtime start, or real-money action.

## Source Observations

| Source | URL | Observation | Route Effect |
| --- | --- | --- | --- |
| `kalshi_api_welcome` | https://docs.kalshi.com/welcome | Kalshi docs describe the Exchange API for real-time market data and trade execution, with Predictions APIs over REST, WebSocket, and FIX, plus demo environment, API keys, rate limits, and raw spec files. | The route must separate read-only market-data planning from authenticated trading and account operations. |
| `kalshi_get_markets` | https://docs.kalshi.com/api-reference/market/get-markets | Get Markets returns market metadata and fields such as ticker, event ticker, bid/ask, last price, volume, open interest, liquidity, rules, status, settlement fields, and pagination. It supports filters like status, tickers, series, timestamps, and multivariate exclusion. | This can support a paper scanner for market metadata, close windows, status, liquidity, rules, and settlement fields. |
| `kalshi_get_trades` | https://docs.kalshi.com/api-reference/market/get-trades | Get Trades returns completed transactions with ticker, yes/no price, quantity, timestamp, block-trade flag, pagination, and filters by ticker/time/block status. | This can support paper-only replay, recent activity checks, and block-trade filtering without placing orders. |
| `kalshi_get_candlesticks` | https://docs.kalshi.com/api-reference/market/get-market-candlesticks | Get Market Candlesticks returns open/low/high/close price, bid/ask, volume, and open interest for 1-minute, hourly, or daily periods; old settled markets move to historical candlestick endpoints. | This can support paper signal features such as drift, volatility, volume, and stale-price checks. |
| `kalshi_get_orderbook` | https://docs.kalshi.com/api-reference/market/get-market-orderbook | Get Market Orderbook returns yes/no bid levels, but the endpoint requires KALSHI-ACCESS-KEY, signature, and timestamp headers. | Orderbook depth remains credential-gated and cannot be used by this local-only packet. |
| `kalshi_historical_markets` | https://docs.kalshi.com/api-reference/historical/get-historical-markets | Historical Markets returns archived market metadata from the historical database with similar fields to live markets and mutually exclusive filters. | Historical endpoints can support deterministic replay design, still without trading or account actions. |
| `local_kalshi_crypto_settlement_replay` | E:/agent-company-lab/reports/prediction-market-research/kalshi-crypto-settlement-lag-paper-replay-20260614.md | Local replay kept zero paper candidates after deterministic gates. False positives included pre-close rows, terminal quotes, finalized/inactive markets, fees unverified, venue eligibility unverified, and absent real-money gate. | A safe paper scanner must default to kill unless settlement source, active quote, fees/depth, eligibility, and max-loss gates are proven. |
| `recent_profit_edge_kalshi_btc_packet` | E:/profit-edge-lab/reports/kalshi-btc-range-edge-20260618-061636.md | Recent local Kalshi BTC range scanner was watch-only with zero review candidates because CF Benchmark source, account eligibility, boundary buffer, liquidity, and orderbook depth were unverified. | Crypto range signals should remain watch-only until the official settlement source and depth/fee/eligibility blockers are verified. |

## Paper Signal Schema

Input sources:
- markets endpoint or local market snapshots
- trades endpoint or local trade snapshots
- candlesticks endpoint or local candle snapshots
- historical markets/candles for settled replay

Candidate fields:
- `ticker`
- `event_ticker`
- `market_title`
- `status`
- `close_time`
- `expiration_time`
- `settlement_ts`
- `rules_primary`
- `yes_bid`
- `yes_ask`
- `no_bid`
- `no_ask`
- `last_price`
- `volume`
- `volume_24h`
- `open_interest`
- `liquidity`
- `candlestick_drift`
- `trade_recency`
- `block_trade_flag`
- `kill_reasons`

Must-kill reasons:
- `real_money_gate_absent`
- `account_or_jurisdiction_eligibility_unverified`
- `fees_unverified`
- `orderbook_depth_unverified`
- `official_settlement_source_unverified`
- `pre_close_without_result`
- `inactive_or_finalized_market`
- `terminal_quotes_no_edge`
- `low_liquidity_or_missing_liquidity`
- `max_loss_not_defined`

## Paper-Only Signal Tests

| Test | Purpose | Required Data | Default Decision |
| --- | --- | --- | --- |
| `settlement_lag_watch` | Find post-close markets with official result/settlement value but still nonterminal active quotes. | `market status`<br>`close/settlement timestamps`<br>`settlement value`<br>`bid/ask`<br>`active/finalized state` | kill unless official value, active quote, fees, depth, eligibility, max loss, and real-money approval are all present. |
| `wide_spread_liquidity_watch` | Find markets where public metadata suggests wide spread or stale last price. | `bid/ask`<br>`last price`<br>`liquidity`<br>`volume`<br>`recent trades`<br>`candles` | paper-only because orderbook depth and executable size are credential-gated. |
| `crypto_range_boundary_watch` | Compare price-source-derived boundary distance against Kalshi range markets. | `market range`<br>`official settlement source`<br>`candles/trades`<br>`liquidity`<br>`close time` | watch-only unless official CF Benchmark source, buffer, liquidity, fees, and depth are verified. |
| `historical_replay_backtest` | Replay settled historical markets to validate that the checker kills false positives before testing fresh markets. | `historical market fields`<br>`historical trades/candles`<br>`settlement timestamps`<br>`terminal quotes` | local validation only; no account, trade, or live signal promotion. |

## Decision

`paper_research_only_no_trade_no_account_no_runtime`

Recommended next local proof: Build a standard-library parser/checker against saved Kalshi-style fixture rows that reproduces zero candidates on the local settlement-lag replay, then emits explicit kill reasons.

## Acceptance Checks

- Current Kalshi market, trades, candlesticks, orderbook, and historical docs are summarized.
- Local Kalshi replay lessons are included.
- Paper-signal fields and kill reasons are specified.
- At least four paper-only signal tests are defined.
- No Kalshi account/login, API key, signed orderbook call, trade, deposit, withdrawal, payment, real-money action, worker/runtime start, model/API call, or external side effect occurs.

## Boundary

No Kalshi account/login, API key, signed API request, market-data API call, orderbook call, order/trade, deposit, withdrawal, payment/wallet action, real-money action, public action, service-request mutation, worker/runtime start, model/MCP/external API call, or external side effect occurred.

## Next Action

Create a local Kalshi fixture parser/checker that consumes saved market/trade/candle-like rows, emits paper-only signal rows with kill reasons, and proves zero promotable candidates on the existing settlement-lag replay; keep account, API keys, signed requests, orderbook depth, trades, deposits, withdrawals, payments, worker/runtime, and real-money gates blocked.
