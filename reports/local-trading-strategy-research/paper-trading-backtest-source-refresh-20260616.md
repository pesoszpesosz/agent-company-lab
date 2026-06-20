# Local Trading Strategy Research: Paper-Only Backtest Source Refresh

Generated UTC: 2026-06-16T20:40:00Z
Lane: `local_trading_strategy_research`
Scope: read-only public source scan plus local folder inventory; no broker login, API key use, account creation, deposit, withdrawal, order placement, strategy deployment, real-money trade, or financial advice.

## Executive Takeaway

The local trading lane should remain a research and paper-evidence lane until the company has a formal treasury gate, broker/account gate, and real-money risk review. The useful work now is to turn local strategy artifacts into reproducible paper-only evidence:

1. Inventory local trading/backtest workspaces.
2. Choose one paper-only replay standard.
3. Require fees, slippage, spread, data source, market regime, drawdown, and out-of-sample evidence.
4. Separate backtest, dry-run/paper-trade, and real-money gates.
5. Treat every live broker/API/balance/order action as blocked.

## Local Inventory

Observed local sources:

- `C:\Users\matth\Documents\Codex\2026-06-12\recovered-trading-edge`
  - folders: `outputs`, `scripts`, `tools`, `work`
- `E:\openclaw-unified`
  - notable folders/files: `.openclaw`, `.runtime`, `ops`, `v2`, `logs`, `memory`, `AGENTS.md`, `accounts_master.csv`, `accounts_master.xlsx`

Important boundary:

- The presence of accounts files or broker/workflow folders is not permission to use them.
- This refresh did not open credentials, use broker APIs, place orders, connect accounts, or inspect sensitive account state.

## Current Infrastructure Sources

| Source Class | Current Source Signal | Best Use | First Local Proof | Gate |
| --- | --- | --- | --- | --- |
| Alpaca paper trading | Alpaca docs describe a paper-only account that can use the API in a paper environment and track simulated activity/balance. Alpaca notes paper trading does not use real money and paper outcomes can differ from live trading. | Good developer API reference for simulated equities/crypto workflows. | Paper-account requirements and API-key handling checklist; no signup or keys. | Account, API keys, data plan, market data limits, no live order route. |
| IBKR paper trading | IBKR describes paper trading as a simulated environment with real market conditions and full trading capabilities for learning/testing. | Good multi-asset professional paper environment reference. | Broker-paper gate packet: account state needed, permissions, delayed/real data, order-type constraints. | IBKR account, trading permissions, market data, platform login. |
| QuantConnect / LEAN | QuantConnect paper trading runs real-time data into algorithms using fictional capital. LEAN is open-source and supports research, backtesting, and live trading in Python/C#. | Good framework model for research-to-paper-to-live separation. | LEAN/QuantConnect adapter decision memo; no deploy. | QuantConnect account, node/runtime, broker/data provider, live deploy gate. |
| Freqtrade | Official docs support backtesting with historic data and config for dry-runs including fees. | Good crypto strategy dry-run reference if kept isolated from exchange credentials. | Dry-run checklist: config, fee, pairs, data download, exchange sandbox, no keys. | Exchange account/API keys, wallet/funds, live mode, real orders. |
| Backtrader | Backtrader is a Python backtesting/trading framework focused on reusable strategies, indicators, and analyzers. | Good local Python baseline framework for simple reproducible tests. | Minimal strategy replay with explicit data/fee/slippage config. | Live broker integrations blocked. |
| Backtesting.py | Backtesting.py is a Python framework for inferring strategy viability on historical data and warns past performance is not future performance. | Good lightweight notebook/report artifact for one strategy idea. | One reproducible notebook/report with parameter sweep and regime caveat. | No live trading support unless separately reviewed. |
| vectorbt | vectorbt operates on pandas/NumPy, accelerated for testing many strategies quickly. | Good parameter sweep and robustness testing engine. | Grid search with walk-forward split and overfit warning. | Avoid optimization-to-overfit; no live route. |

## Paper Evidence Standard

Every candidate strategy must produce:

- data source and timestamp range
- instrument/symbol
- timeframe
- spread, commission, financing, and slippage assumptions
- position sizing rule
- max loss per trade and max portfolio drawdown
- in-sample and out-of-sample split
- market regime labels
- number of trades
- win rate, profit factor, expectancy, max drawdown, Sharpe/Sortino where appropriate
- sensitivity/parameter stability check
- trade log
- reproducible command/notebook
- reason it might fail live
- explicit `real_money_allowed = false`

## Agent Assignment

| Agent Type | Responsibility | Output |
| --- | --- | --- |
| `strategy_miner` | Inventory local strategy ideas and classify them by instrument, timeframe, data source, and implementation status. | `local-strategy-inventory-YYYYMMDD.md/json` |
| `backtest_runner` | Run reproducible local backtests only with approved historical data and no broker/API keys. | `paper-backtest-report-<strategy>.md/json` |
| `data_quality_auditor` | Check missing data, survivorship bias, timestamp alignment, fees, spread, slippage, and lookahead risk. | `data-quality-note-<strategy>.md` |
| `risk_reviewer` | Decide whether a strategy stays research-only, moves to paper-run simulation, or is killed. | `paper-risk-review-<strategy>.md` |
| `treasury_risk_worker` | Only after explicit approval, evaluate whether real-money consideration is even eligible. | `real-money-trade-gate-review.md` |

## First Work Packet

Task ID proposal: `task-local-trading-paper-replay-standard-20260616`

Worker: `strategy_miner`

Allowed scope:

- Inventory local trading artifacts by filename, high-level purpose, and non-sensitive metadata.
- Do not read credentials, account files, broker sessions, private keys, or payment/balance data.
- Draft a paper-only replay standard and choose one candidate strategy for a no-key local replay.
- Write local markdown/json only.

Forbidden scope:

- No broker login or API calls.
- No account creation or permission changes.
- No API key, secret, password, OTP, private-key, seed phrase, account balance, or payment inspection.
- No market order, limit order, cancellation, position change, deposit, withdrawal, transfer, or subscription.
- No real-money trading.
- No financial advice or recommendation to trade.

Required proof artifact:

- `reports/local-trading-strategy-research/paper-replay-standard-YYYYMMDD.md`
- `reports/local-trading-strategy-research/local-strategy-inventory-YYYYMMDD.json`

## Promotion Gates

| Stage | Allowed | Blocked |
| --- | --- | --- |
| Backtest | local historical data, fees/slippage assumptions, deterministic reports | broker login, live data subscriptions, orders |
| Dry-run/Paper | simulated capital only, approved sandbox/paper account only after explicit service request | real balances, deposits, withdrawals, live mode |
| Real-money review | risk memo only | any order or fund movement |
| Real-money execution | not allowed in this lane | all execution until a future explicit user-approved treasury workflow exists |

## Source URLs

- https://docs.alpaca.markets/us/docs/paper-trading
- https://alpaca.markets/learn/start-paper-trading
- https://www.interactivebrokers.com/campus/trading-course/ibkr-paper-trading-account/
- https://www.ibkrguides.com/clientportal/papertradingaccount.htm
- https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading
- https://www.quantconnect.com/docs/v2/lean-engine/getting-started
- https://www.lean.io/
- https://www.freqtrade.io/en/stable/backtesting/
- https://www.freqtrade.io/en/stable/configuration/
- https://www.backtrader.com/
- https://www.backtrader.com/docu/
- https://kernc.github.io/backtesting.py/
- https://kernc.github.io/backtesting.py/doc/backtesting/
- https://vectorbt.dev/
- https://vectorbt.dev/getting-started/usage/

## Next Action

Create the `paper-replay-standard` and `local-strategy-inventory` artifacts. Start by inventorying `recovered-trading-edge` and `E:\openclaw-unified` without opening credentials or account files. The first acceptable trading output is a reproducible paper-only report, not a broker connection.
