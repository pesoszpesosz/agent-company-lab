# Typed Worker Proposal - prediction_market_research

Generated UTC: 2026-06-14T11:30:58Z
Worker agent: `typed-worker-prototype`
Mode: `read_only_local_artifact`

## Proposal

- Proposal ID: `proposal-prediction_market_research-20260614`
- Task title: Prepare paper-only replay spec for one imported market edge
- Duplicate key: `prediction_market_research:typed-worker-prototype:2026-06-14`
- Rationale: The lane has side-effect gates, so the safe prototype output is a local artifact proposal only.

## Evidence Refs

- `pe-report-cross-venue-next-team-scan-35be3fc7745a`
- `pe-report-polymarket-tennis-edge-packet-68be67f48831`
- `pe-report-kalshi-btc-range-edge-e654ec4ccb73`
- `pe-report-prediction-market-scan-feb389566f62`
- `pe-report-kalshi-btc-settlement-lag-daa29bc18301`

## Allowed Now

- read manager packet
- read source specs
- read local evidence/artifact reports
- write local proposal artifacts
- record artifacts/outcomes/traces through the control plane

## Blocked Actions

- paper trade
- real-money trade
- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.
- venue account action
- eligibility assertion without verification

## Required Service Requests

- market_eligibility_worker
- treasury_risk_worker

## Recommended Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id prediction_market_research
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id prediction_market_research --limit 25
python E:\agent-company-lab\tools\agent_company.py write-artifacts-report --lane-id prediction_market_research --path E:\agent-company-lab\reports\artifacts-prediction_market_research-latest.md
```

## Source Specs

| Spec | Type | Gate |
| --- | --- | --- |
| `prediction_profit_edge_scan_import` | local_reports | data_only_until_venue_eligibility_fees_treasury_and_real_money_gate_clear |

## Evidence Preview

| Status | Evidence | Source | Next Action |
| --- | --- | --- | --- |
| watch_only | `pe-report-cross-venue-next-team-scan-35be3fc7745a` - Cross-Venue Next-Team Scan | E:\profit-edge-lab\reports\cross-venue-next-team-latest.md | next: Watch only; no clean cross-venue trade from current public data. |
| watch_only | `pe-report-polymarket-tennis-edge-packet-68be67f48831` - Polymarket Tennis Edge Packet | E:\profit-edge-lab\reports\polymarket-tennis-edge-packet-latest.md |  |
| watch_only | `pe-report-kalshi-btc-range-edge-e654ec4ccb73` - Kalshi BTC Range Edge | E:\profit-edge-lab\reports\kalshi-btc-range-edge-latest.md |  |
| imported | `pe-report-prediction-market-scan-feb389566f62` - Prediction Market Scan | E:\profit-edge-lab\reports\prediction-market-scan-latest.md |  |
| imported | `pe-report-kalshi-btc-settlement-lag-daa29bc18301` - Kalshi BTC Settlement Lag | E:\profit-edge-lab\reports\kalshi-btc-settlement-lag-latest.md |  |
| imported | `pe-report-kalshi-crypto-settlement-lag-7d155d530ac1` - Kalshi Crypto Settlement Lag | E:\profit-edge-lab\reports\kalshi-crypto-settlement-lag-latest.md |  |
| imported | `pe-report-kalshi-generic-settlement-lag-898b589d490d` - Kalshi Generic Settlement Lag | E:\profit-edge-lab\reports\kalshi-settlement-lag-latest.md |  |
| kalshi_crypto_close_window_evidence | `pe-ledger-kalshi_crypto_close_window_evidence-9ed635b33ebd` - kalshi_crypto_close_window_evidence | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Rerun with a wider lookahead or explicit -Ticker/-EventTicker. |
