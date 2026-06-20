# Prediction Market Research Startup

Generated UTC: 2026-06-14

Agent: `lane-manager-prediction_market_research-relaunch-20260614`
Thread: `019ec637-a391-7693-915f-5ec5e5d82ee7`
Lane: `prediction_market_research`
Task: `task-prediction_market_research-startup-20260614`

## Scope

This manager owns only `prediction_market_research`.

Hard stop: data/paper-only. No account setup, KYC, deposits, withdrawals, orders, trades, wallet actions, broker/API keys, API trading, market manipulation, or real-money action is allowed unless an approved service request exists for that exact scope.

Excluded lanes: `submitted_bounty_payouts`, RustChain, Charles, GitHub payout chasing, paid-code PR work, and all other lane-manager work.

## Startup State

- Required docs read: lab README, prediction manager packet, launch manifest, service catalog, and prediction manager recovery memo.
- Live SQLite state before claim: `prediction_market_research` was unowned and had no prediction startup task, artifact, outcome, or lane trace.
- Registered agent id: `lane-manager-prediction_market_research-relaunch-20260614`.
- Claimed lane: `prediction_market_research` only.
- Created/acquired exactly one startup task: `task-prediction_market_research-startup-20260614`.

## Imported Evidence Reviewed

- `E:\profit-edge-lab\reports\prediction-market-scan-latest.md`
- `E:\profit-edge-lab\reports\kalshi-btc-range-edge-latest.md`
- `E:\profit-edge-lab\reports\kalshi-btc-settlement-lag-latest.md`
- `E:\profit-edge-lab\reports\kalshi-crypto-settlement-lag-latest.md`
- `E:\profit-edge-lab\reports\kalshi-settlement-lag-latest.md`
- `E:\profit-edge-lab\reports\cross-venue-next-team-latest.md`

The imported prediction evidence is useful for replay design, but none of it is tradable evidence. Existing reports repeatedly flag missing venue eligibility, unverified fees, unverified official source mechanics, one-sided books, low/no reported liquidity, stale quotes, or rule-window mismatch.

## First Proof Task

Chosen first proof: paper-only Kalshi crypto settlement-lag replay.

Objective: replay the imported Kalshi crypto close-window packets and determine whether a deterministic local checker can identify only cases where:

1. the market close time has passed;
2. Kalshi exposes a result or `expiration_value`;
3. the winning side and losing side can be derived from the venue result fields;
4. post-result quotes are still active and stale in the report data; and
5. a paper-only edge survives explicit fee/depth/eligibility blockers.

Initial evidence set:

- `kalshi-crypto-settlement-lag-latest.md`, including KXBTC, KXETH, KXXRP, and KXDOGE close windows.
- `kalshi-btc-settlement-lag-latest.md`, including event `KXBTC-26JUN1306`, close `2026-06-13T10:00:00Z`, official value `63712.97`, and zero review candidates.
- `kalshi-settlement-lag-latest.md`, including generic finalized-result packets, currently marked `review=False` and `not_active`.

Output target for the next task: a local replay artifact under `E:\agent-company-lab\reports\prediction-market-research\` with parsed candidate rows, reasons kept/killed, paper price assumptions, and a final no-trade recommendation unless every gate is cleared.

## Source Of Truth

Primary source of truth for settlement replay:

- Kalshi market detail/result fields and exposed `expiration_value` after market close.
- For crypto range events, the official benchmark referenced by the venue rules, not Coinbase or CoinGecko spot. Existing imported packets warn that BTC range markets resolve on CF Benchmarks' Bitcoin Real-Time Index, and crypto settlement packets refer to official CF/CME index results.

Local reports may be used as replay inputs only. They are not an execution source of truth and cannot justify action without fresh venue/result verification.

## Fees

Fees are not verified for real-money execution in this lane.

Paper replay must record:

- quoted bid/ask used by the imported report;
- whether the quote was active or already finalized;
- gross payout if correct;
- fee status as `unverified`;
- conservative net status as `blocked_by_fee_verification` until an approved service request confirms venue fee schedule, account fee treatment, and any withdrawal/deposit costs.

No paper candidate may be promoted to real-money review unless fees and depth are explicitly captured in a later artifact.

## Settlement Timing

Replay timing standard:

- Treat all pre-close rows as monitoring only.
- Check T-3 minutes to T+7 minutes around close in paper mode when source data exists.
- Promote for review only after close and only if Kalshi exposes result or `expiration_value`.
- Kill rows when markets are not active, winning ask is already 1.0000, losing bid is 0.0000, or the report shows no actionable post-result stale quote.

Existing reviewed packets currently show zero review candidates.

## Venue Eligibility

Eligibility is not verified for this lane.

- Kalshi: venue/account eligibility, jurisdiction, balance, fees, and settlement mechanics are unverified. This lane may only prepare data/paper artifacts.
- Polymarket: data-only for a US user unless eligibility changes are explicitly verified through an approved service request. Cross-venue packets are watch-only and currently blocked by rule-window mismatch and Polymarket data-only constraints.

## No-Trade Gate

Default decision: no trade.

A future real-money gate cannot be requested unless a completed paper artifact shows all of the following:

- official venue result and rule source captured;
- fee schedule and depth captured;
- settlement timing and stale-quote window reproduced;
- venue/account eligibility reviewed;
- maximum loss and kill switch defined;
- no market-manipulation or public-action requirement;
- approved `real_money_trade_gate` service request for the exact market, proposed capital, and action scope.

Until then, every output remains research, replay, or no-trade evidence only.

## Next Action

Create one follow-up proof task for the paper-only Kalshi crypto settlement-lag replay and write the replay artifact locally. Do not open accounts, use credentials, place orders, or call trading APIs.
