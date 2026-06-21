# Local Trading No-Key Replay Prep v1

Generated UTC: 2026-06-21T13:37:36Z
Lane: `local_trading_strategy_research`
Task: `task-continuity-lane-next-task-20260621-local_trading_strategy_research-002`
Evidence: `E:\agent-company-lab\reports\local-trading\local-trading-paper-research-proof-v1-20260621.md`
Commit context: `085a03a Continue lane proof followups`
Mode: paper-only, local-only, no account/broker/API/paid-data/order/trade action

## Purpose

Prepare one safe local replay candidate without keys, accounts, brokers, paid data, external calls, orders, spending, or trading. This packet inventories only non-sensitive local file metadata, selects one readable local dataset, freezes the columns for a future paper replay, and states the stop conditions.

## Non-Sensitive Local Inventory

Inventory method:

- Listed local filenames, extensions, sizes, and timestamps only.
- Excluded paths matching account, credential, secret, key, token, password, wallet, balance, broker, session, order, live trade, private, login, cookie, OTP, or payment.
- Read schema and scalar metadata only for the selected raw market-data JSON.
- Did not inspect account files, credentials, API keys, balances, orders, broker state, or paid-data sources.

Observed safe file classes:

| Area | Example Path | Use | Decision |
| --- | --- | --- | --- |
| Prior lane evidence | `E:\agent-company-lab\reports\local-trading\local-trading-paper-research-proof-v1-20260621.md` | Defines hypothesis and replay requirements. | Evidence input only. |
| Lane source refresh | `E:\agent-company-lab\reports\local-trading-strategy-research\paper-trading-backtest-source-refresh-20260616.md` | Defines paper-only gates and local inventory boundaries. | Supporting context only. |
| Recovered trading notes | `C:\Users\matth\Documents\Codex\2026-06-12\recovered-trading-edge\outputs\trading-edge-xau-*.md` | Many XAU research notes and source-readiness notes. | Non-sensitive metadata only; not selected as replay dataset because markdown notes are not canonical bar data. |
| OpenClaw blind historical artifacts | `E:\openclaw-unified\.hermes\openclaw\blind-historical\...\blind_historical_raw_market_data_snapshots_*.json` | Local raw market-data snapshots and related proof artifacts. | Best no-key replay candidate class. |
| OpenClaw XAUUSD proof folders | `E:\openclaw-unified\.hermes\openclaw\blind-historical\xauusd-sweep-reclaim-bridge-v1\...` | XAUUSD raw market data, execution traces, manifests, audits, strategy freeze files. | Select only raw market data; do not use execution traces for the first replay prep. |

Sensitive or blocked classes:

- Account masters, account files, credentials, broker/session files, balances, order routes, live execution state, paid-data configuration, API keys, wallets, payments, or private tokens.
- Any file requiring login, browser session, external download, paid data access, or broker/API connection.

## Selected Dataset

Selected local dataset:

`E:\openclaw-unified\.hermes\openclaw\blind-historical\xauusd-sweep-reclaim-bridge-v1\blind_historical_raw_market_data_snapshots_latest.json`

Selection rationale:

- The path is a local `blind-historical` raw market-data snapshot artifact.
- Filename and parent folder indicate XAUUSD paper/backtest research, consistent with prior lane evidence.
- It is a JSON file readable locally without credentials, account inspection, broker connection, API calls, browser use, paid data, orders, spending, or trading.
- It contains `artifactKind = blind_historical_raw_market_data_snapshots`, `snapshotCount = 133`, and per-snapshot candle arrays.
- It avoids execution-trace and account-like files for the first replay prep.

Observed top-level schema:

- `schemaVersion`
- `artifactKind`
- `generatedAt`
- `commandId`
- `freezeHash`
- `strategyHash`
- `snapshotCount`
- `snapshots`

Observed first snapshot metadata:

- `windowId = benchmark-dukascopy-XAUUSD-5m-0`
- `phase = benchmark`
- `runKind = candidate`
- `costMultiplier = 1`
- `source = dukascopy`
- `symbol = XAUUSD`
- `timeframe = 5m`
- `requestedStartIndex = 0`
- `requestedEndIndexExclusive = 512`
- `candleCount = 512`
- `firstTimestamp = 2026-03-16T00:00:00.000Z`
- `lastTimestamp = 2026-03-17T19:35:00.000Z`

## Frozen Replay Columns

Future replay must treat this as a snapshot-of-candles dataset. No additional columns may be inferred from external systems.

Snapshot-level columns:

- `windowId`
- `phase`
- `runKind`
- `costMultiplier`
- `source`
- `symbol`
- `timeframe`
- `requestedStartIndex`
- `requestedEndIndexExclusive`
- `candleCount`
- `firstTimestamp`
- `lastTimestamp`
- `regimeLabels`
- `regimeMetrics.candleCount`
- `regimeMetrics.directionalMovePct`
- `regimeMetrics.absoluteMovePct`
- `regimeMetrics.pathLengthPct`
- `regimeMetrics.trendEfficiency`
- `regimeMetrics.maxAbsReturnPct`
- `regimeMetrics.meanAbsReturnPct`
- `regimeMetrics.meanRangePct`

Candle-level columns:

- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `spreadQuote`

Derived columns allowed in a later paper replay:

- `barReturnPct = close / previous_close - 1`
- `trueRange = max(high - low, abs(high - previous_close), abs(low - previous_close))`
- `maFast`
- `maSlow`
- `trendDirection`
- `realizedVolatility`
- `entrySignal`
- `exitSignal`
- `paperPosition`
- `paperGrossPnl`
- `paperEstimatedCost`
- `paperNetPnl`
- `paperDrawdown`

Derived columns are local-only and must be computed from the selected dataset plus frozen cost assumptions. No external enrichment is allowed.

## Frozen Replay Rules

Replay hypothesis:

Run a paper-only trend plus volatility filter over XAUUSD 5m candle windows to test whether deterministic entry/exit rules survive spread/cost and drawdown constraints.

Frozen starting configuration for the next local test:

- Universe: `symbol == XAUUSD`
- Timeframe: `5m`
- Data source: selected local JSON only
- In-sample windows: first 70 percent of ordered `snapshots`
- Out-of-sample windows: final 30 percent of ordered `snapshots`
- Fast moving average: 12 candles
- Slow moving average: 48 candles
- Volatility window: 24 candles
- Volatility filter: only trade when rolling true-range percentile is between 30 and 80 within the current snapshot
- Entry: long when `maFast > maSlow` and volatility filter is true; short when `maFast < maSlow` and volatility filter is true
- Exit: moving-average cross reversal, volatility filter false for 3 consecutive bars, or end of snapshot
- Cost: use `spreadQuote` when present; otherwise stop and write blocker
- Position sizing: fixed paper unit size for comparability, no leverage assumption
- Risk cap: stop replay if paper max drawdown exceeds 5 percent of starting paper equity
- `real_money_allowed = false`

## Paper-Only Stop Conditions

Stop immediately and write a blocker artifact if any of these occur:

- Selected file is missing, unreadable, or not valid JSON.
- Required top-level fields or candle columns are absent.
- Timestamps are missing, duplicated within a snapshot, or not strictly increasing.
- OHLC values are nonnumeric, nonpositive, or violate `low <= open/close <= high`.
- `spreadQuote` is missing and no already-local cost assumption is available.
- Dataset appears to require paid data, API refresh, browser access, account login, broker session, credential, balance, or order inspection.
- Replay code would need to read account, credential, broker, session, order, balance, wallet, payment, private-key, token, or password files.
- A result is needed for live/paper deployment rather than local evidence.
- Any step would place/cancel orders, connect to a broker, call an external API, open a browser, spend money, subscribe to data, or trade.

## Next Local Test

Write a local-only replay readiness report that validates the selected JSON and produces counts only:

`E:\agent-company-lab\reports\local-trading\local-trading-selected-dataset-readiness-v1-20260621.md`

The readiness report may parse the selected JSON locally to count snapshots, candle rows, missing fields, timestamp-order failures, OHLC invariant failures, and spread availability. It must not run live signals, connect brokers, call APIs, open browsers, use paid data, inspect accounts, place orders, spend, or trade.

## Completion Note

This artifact completes the no-key replay prep step for the open follow-up task. It does not authorize a backtest promotion, paper deployment, broker/API setup, account inspection, paid-data access, order placement, spending, trading, or ownership mutation.
