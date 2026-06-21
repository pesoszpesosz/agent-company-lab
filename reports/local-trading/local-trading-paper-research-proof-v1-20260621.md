# Local Trading Paper Research Proof v1

Generated UTC: 2026-06-21T13:26:09Z
Lane: `local_trading_strategy_research`
Task: `task-continuity-lane-next-task-20260621-local_trading_strategy_research-001`
Evidence: `E:\agent-company-lab\reports\manager-packets\local_trading_strategy_research-manager-packet.md`
Commit context: `8944215` pushed
Mode: paper-only, local-only, no broker/API/trade action

## Scope

This packet defines one paper trading research hypothesis and the local replay evidence required before any promotion discussion. It does not place orders, connect brokers, open accounts, call APIs, use paid data, spend money, trade, mutate ownership, or approve/start service requests.

## Hypothesis

A simple trend-following plus volatility-filter strategy on already-local historical price data may produce cleaner paper-replay evidence than ad hoc signal review if every entry, exit, cost, and drawdown rule is deterministic and replayable.

Candidate paper hypothesis:

- Instrument class: local historical market data only; prefer an instrument already represented in prior local trading evidence, such as XAU-related paper evidence, if non-sensitive files are available.
- Signal: trade only in the direction of a higher-timeframe moving-average trend.
- Filter: skip entries when recent realized volatility is outside a predefined middle band to avoid extremely quiet chop and extreme event spikes.
- Exit: fixed invalidation level, time stop, or opposite trend flip, chosen before replay.
- Sizing: fixed fractional paper risk per trade, capped by max paper portfolio drawdown.
- Promotion target: not profit alone; a candidate only survives if replay artifacts show stable behavior after fees/slippage and out-of-sample split.

Null hypothesis:

After realistic cost, spread, slippage, and drawdown constraints, the strategy does not produce robust enough paper evidence to justify more research.

## Replay Data Requirements

Required local inputs:

- Historical OHLCV or equivalent bar data from local files only.
- Source path, file timestamp, symbol/instrument, timeframe, timezone, and date range.
- A data dictionary for columns used in replay.
- Missing-bar, duplicate-row, and timestamp-order checks.
- Corporate action, roll, session, or contract-adjustment note where applicable.
- No credential, broker, account, balance, order, paid-data, or API-derived files.

Required replay configuration:

- In-sample and out-of-sample split fixed before metrics are reviewed.
- Commission, spread, financing, and slippage assumptions explicitly stated.
- Position sizing rule and max paper risk per trade.
- Max paper portfolio drawdown stop.
- Entry, exit, stop, and time-stop rules frozen before replay.
- `real_money_allowed = false`.

Required outputs:

- Reproducible local command or notebook path.
- Trade log with timestamp, side, entry, exit, size, gross PnL, estimated cost, net PnL, and exit reason.
- Summary metrics: trade count, win rate, expectancy, profit factor, max drawdown, average holding time, and out-of-sample net result.
- Sensitivity check across at least one moving-average parameter and one volatility-filter parameter.
- Failure note explaining how the apparent edge could disappear live.

## Risk Notes

- Backtests can overfit; a single profitable replay is not a money proof.
- XAU or similar instruments can gap, widen spreads, and behave differently around macro events.
- Local data may be stale, incomplete, adjusted, misaligned, or contaminated with lookahead.
- Cost assumptions can dominate short-horizon strategies.
- A volatility filter can accidentally select favorable regimes in hindsight.
- Paper fills are not live fills; no paper result authorizes real-money execution.
- Any broker connection, paper deployment, API use, paid data, account inspection, or real-money action requires a separate approved gate outside this task.

## Next Local Test

Create a no-key local replay prep artifact:

1. Inventory only non-sensitive local trading/backtest files by path, extension, approximate purpose, and whether they appear to contain price bars, strategy code, logs, or reports.
2. Select one candidate dataset that can be read without credentials, account files, broker sessions, paid data, or external calls.
3. Write `E:\agent-company-lab\reports\local-trading\local-trading-replay-data-readiness-v1-20260621.md` with data readiness, blockers, and the exact frozen replay configuration.
4. If no safe local dataset is available, park the hypothesis with a blocker artifact instead of widening scope.

## Completion Standard

This packet is complete when it is registered as the artifact for `task-continuity-lane-next-task-20260621-local_trading_strategy_research-001` and traced locally. The task remains paper-only and does not authorize deployment, broker connection, API calls, paid data, account inspection, order placement, spending, or trading.
