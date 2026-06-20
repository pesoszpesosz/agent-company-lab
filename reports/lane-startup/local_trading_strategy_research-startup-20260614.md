# Local Trading Strategy Research Startup Memo

Generated: 2026-06-14
Lane: `local_trading_strategy_research`
Manager: `lane-manager-local_trading_strategy_research-019ec613`
Task: `task-local_trading_strategy_research-startup-20260614`

## Scope

This lane is paper/backtest research only. It does not own `submitted_bounty_payouts`, RustChain, Charles, GitHub payout chasing, or the separate trading-edge worker. It also does not operate OpenClaw execution, broker, deployment, account, or order-routing paths.

Approved work for this startup task:
- Inventory local trading/backtest evidence artifacts.
- Define a paper-only evidence standard.
- Identify one next proof task that can be completed from local artifacts without broker/API/order/live-signal action.

Hard stop:
- No broker connection.
- No API key use.
- No paper deployment registration.
- No order routing.
- No live signal service.
- No deposit, withdrawal, real-money execution, or account action.
- No financial advice or guaranteed-profit claim.

Prompt/eval safety gate used: `E:\agent-company-lab\reports\prompt-eval-review-latest.md` says prompt records and reviews do not bypass real-money, account, browser-public, legal/KYC, security, or model/API gates. This lane keeps the same rule for trading gates.

## Source Inventory

### Recovered trading-edge workspace

Path: `C:\Users\matth\Documents\Codex\2026-06-12\recovered-trading-edge`

Observed inventory:
- `scripts\`: 53 local audit/ledger scripts, mostly XAU, ETF cross-asset, forward-readiness, paper-watch, source-clean, and candidate-priority tools.
- `outputs\`: 432 Markdown reports, 358 JSON artifacts, and 51 CSV files.
- `outputs\**\latest.md`: 170 latest-summary reports.

Useful evidence surfaces:
- `outputs\trading-edge-candidate-priority-supplement\latest.md`: latest decision says the stablecoin-enhanced XAU blend is a strong offline research control but blocked for runtime, demo, or paper promotion.
- `outputs\xau-stablecoin-blend-forward-watch-readiness-audit\latest.md`: preferred offline control reports 37.597191R common-era, PF 1.953576, maxDD -2.716151R, but readiness is blocked by stale local XAU data, missing stablecoin publication proof, no current ETF signal, and insufficient closed post-freeze observations.
- `outputs\xau-source-reachable-stablecoin-blend-audit\latest.md`: source-reachable stablecoin variants remain positive offline but explicitly lack forward intent packages, lifecycle logs, and closed paper/demo outcomes.
- `outputs\xau-current-source-paper-watch-ledger\latest.md`: paper-only ledger has 1 closed observation event, 2 open observation events, closed netR 2.5, and open mark-to-date R 0.797549. Open marks are diagnostics only.
- `outputs\xau-current-source-platform-sequential-paper-audit\latest.md`: no-overlap sequential scoring keeps 10 rows, skips 37 overlapping rows, and leaves only 1 closed market event plus open observations.
- `outputs\falsified-hypothesis-ledger-addendum\latest.md`: parks/kills microstructure, hour-22 rollover, and ETF lead-lag branches until materially new mechanisms or independent forward/broker-native proof exists.
- `outputs\xau-gvz-no-lookahead-repair-retraction-audit\latest.md`: retracts GVZ as forward-ready after no-lookahead repair fails yearly consistency.
- `outputs\v3-proof-state-recovery-audit\latest.md`: V3 governance/proof artifacts report 0 proof survivors, 0 proof eligible, and no work execution allowed.

Startup interpretation:
- The freshest local evidence is useful for negative memory, paper observation, and offline-control prioritization.
- No local artifact proves a deployable or promotion-ready trading edge.
- The best immediate work is to standardize paper evidence intake and continue only closed, predeclared, no-overlap observations.

### OpenClaw unified workspace

Path: `E:\openclaw-unified`

Relevant local surfaces inspected without reading account or credential files:
- `v2\README.md`: V2 focus includes deterministic signal evaluation, risk-bounded trade-intent generation, scheduler correctness, backtest metrics, strategy/deployment registries, approval queue, and safety for paper deployments.
- `v2\paper_funnel_summary.json`: reports 3 active demo-backed paper deployments, 12 ready demo accounts, 9 free ready demo accounts, and 3 paper-eligible GBPUSD candidates. This is execution-adjacent evidence, not an authority for this lane to operate paper deployments.
- `v2\OPENCLAW_HERMES_V3_COMPLETION_AUDIT.md`: V3 is active but not complete; no candidate has passed the full downstream bounded proof, expanded-window proof, broker replay, forward/no-hindsight, paper, portfolio/risk, and promotion path. Write authorities remain disabled.
- `v2\.hermes\openclaw\v3\`: large local artifact store with current state, completion audit, convergence audit, failure drilldown, operator handoff, and control-plane runbook artifacts.
- `v2\packages\v3-core\src\`: proof, broker-replay, forward-evidence, paper, promotion, admission, negative-memory, and deployment-adjacent code surfaces.
- `v2\scripts\`: many backtest/proof/market-data/broker/paper/deployment scripts. These are inventory only for this lane.

Startup interpretation:
- OpenClaw can provide governance patterns, proof gate names, negative-memory conventions, and local artifact references.
- This lane must not run OpenClaw broker capture, demo monitor, position manager, deployment, registry write, or order/order-like commands without an approved service request for that exact scope.
- Existing paper deployments are not to be modified, refreshed, or monitored by this lane.

## Paper-Only Evidence Standard

An artifact can count as lane evidence only if it satisfies the full standard below.

### Backtest evidence

Required fields:
- Strategy family, rule version, symbol, timeframe, and side rules.
- Exact script path and output path.
- Data source, local snapshot path, first/last timestamp, row/candle count, and known gaps.
- Frozen parameter set before scoring.
- In-sample, out-of-sample, and holdout split boundaries.
- Cost and slippage assumptions, including stress tests.
- Trade count, net R or quote PnL, profit factor, max drawdown, expectancy, rolling-window stability, and year/fold stability.
- Null/control comparison and multiple-testing/family-budget note.
- No-lookahead and source publication-timestamp check where external features are used.
- Explicit blockers and reopen conditions for failures.

Disallowed as proof:
- Open-ended search output without holdout accounting.
- Results that use same-bar future information, post-entry source values, or unstamped external data.
- Aggregate row scores that double-count overlapping trades.
- Any report that claims money-ready status without forward/no-hindsight and closed paper evidence.

### Paper observation evidence

Required fields:
- Predeclared signal before outcome observation.
- Frozen source snapshot hash or immutable local file path.
- Entry, stop, target, full-horizon timeout, and no-overlap rule.
- Mark/exit source, mark timeframe, and reason for closure.
- Closed event scoring only for evidence; open mark-to-date values are diagnostics.
- Skipped overlaps recorded and excluded from evidence.
- Paper ledger updated from local data only unless a service request explicitly approves a refresh scope.

Minimum promotion consideration, not approval:
- At least 30 closed post-freeze market events or a preapproved smaller-sample rationale.
- Positive net after costs and slippage stress.
- Stable across time folds and robust to source/lag variants.
- Null/control advantage remains after family-budget correction.
- Drawdown within a predeclared risk envelope.
- No unresolved source timing, publication timestamp, or market-data coverage blockers.

### OpenClaw import evidence

Allowed:
- Read local reports and machine artifacts.
- Borrow proof-gate vocabulary and negative-memory patterns.
- Record paths to local audit outputs.

Not allowed:
- Broker telemetry capture.
- Demo account verification.
- Paper deployment registration.
- Strategy/deployment registry writes.
- Position manager, live monitor, order, or order-intent execution.
- API key usage or account file inspection.

## Current Lane Decision

No promotion, no deployment, no broker/demo/order work, and no live signal action.

The lane should treat the stablecoin-enhanced XAU blend as the leading offline research control, not as a tradable system. The paper watch ledger has too little closed evidence to support any stronger conclusion. OpenClaw V3 should be used as a governance reference and local evidence source only.

## Next Local Proof Task

Create a paper-evidence intake checklist/report for the XAU current-source watch that:
- Reconciles `xau-current-source-paper-watch-ledger\latest.md` against the sequential audit.
- Verifies open observations are still open or closed using only already-local XAU platform data.
- Produces a closed-event-only evidence table.
- Records skipped overlaps and excludes them from totals.
- Carries forward blockers for stale 15m/5m platform data and missing stablecoin publication timestamps.

This next task must stop before any network refresh, broker/demo/account path, registry write, paper deployment, order routing, or real-money action.

## Control-Plane Fields

Source: local workspaces from `local_trading_research_import`.
Hypothesis: local backtest/paper artifacts can be converted into a strict paper-only evidence ledger without operating trading infrastructure.
Proof artifact: this startup memo and the cited local `latest.md` reports.
Blocker: no lane evidence in the control plane yet; local paper evidence has only 1 closed XAU event; OpenClaw reports no promotion-ready survivor.
Risk: execution-adjacent OpenClaw broker/demo/deployment files must remain inventory-only.
Next action: create one narrow local proof task for XAU paper-evidence intake after startup is recorded.
