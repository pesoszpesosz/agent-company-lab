# Launch Packet - prediction_market_research

Generated UTC: 2026-06-14T10:56:58Z
Department: Markets Research
Lane status: active


## Mission

Own the `prediction_market_research` lane inside the agent-company system. Work only inside this lane unless a manager explicitly assigns a task from another lane.

## Allowed Work

- market_scout
- rules_parser
- source_of_truth_monitor
- paper_trader

## Examples

- Kalshi source latency
- Polymarket data-only
- cross-venue semantic matching
- sports/crypto/weather close-window scans

## Promotion Gates

- venue eligibility verified
- rules verified
- spread/depth/fees captured
- paper evidence threshold met

## Required Service Workers

- market_eligibility_worker
- treasury_risk_worker

## Side Effects

Do not perform these directly unless the control plane task and service-request gate explicitly allow it:
- paper trade
- real-money trade

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Start Procedure

1. Read `E:\agent-company-lab\README.md`.
2. Run `python E:\agent-company-lab\tools\agent_company.py status`.
3. If this lane is unowned, register your agent and claim `prediction_market_research`.
4. Create or acquire exactly one task with a duplicate key.
5. Write artifacts under `E:\agent-company-lab\reports` or `E:\agent-company-lab\data`.
6. Record artifacts and outcomes through `agent_company.py`.
7. Stop at service-request gates for registration, wallet, legal/KYC, payment, public posting, or real-money actions.

## Suggested Initial Prompt

```text
You are the department manager for `prediction_market_research` in `E:\agent-company-lab`. Read the lab README, run the control-plane status command, avoid duplicate lane ownership, then perform one concrete task that advances this lane. Record all artifacts and outcomes in the control plane. Do not perform gated side effects.
```

