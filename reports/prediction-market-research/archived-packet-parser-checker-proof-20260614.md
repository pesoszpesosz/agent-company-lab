# Archived Packet Parser/Checker Proof

Generated UTC: 2026-06-14
Lane: `prediction_market_research`
Task: `task-prediction-archived-packet-parser-checker-20260614`
Agent: `lane-manager-prediction_market_research-relaunch-20260614`

## Hard Stop

This proof is local-only and offline. It reads archived Markdown packets from disk and writes local JSON/Markdown evidence. It made no live venue calls, used no accounts or credentials, placed no orders, used no trading APIs, made no deposits or withdrawals, and performed no real-money trades. Realized USD is `0`.

## Artifacts

- Reusable checker script: `E:\agent-company-lab\reports\prediction-market-research\archived_packet_checker_20260614.py`
- Checker JSON output: `E:\agent-company-lab\reports\prediction-market-research\archived-packet-parser-checker-results-20260614.json`
- Proof report: `E:\agent-company-lab\reports\prediction-market-research\archived-packet-parser-checker-proof-20260614.md`

## Input Set

| File | Generated UTC | Status | Rows | Review candidates | Parsed packets |
| --- | --- | --- | ---: | ---: | ---: |
| `kalshi-crypto-settlement-lag-latest.md` | `2026-06-14T14:59:07.9148250Z` | `pre_close_watch` | `2804` | `0` | 0 |
| `kalshi-btc-settlement-lag-latest.md` | `2026-06-13T10:09:07.5956915Z` | `official_value_seen_no_edge` | `188` | `0` | 12 |
| `kalshi-settlement-lag-latest.md` | `2026-06-13T10:09:35.8611115Z` | `pre_close_watch` | `1013` | `0` | 20 |

## Checker Contract

The checker is intentionally conservative. A packet is actionable only if all of these pass:

1. The archived packet has `review=True`.
2. It is not flagged `pre_close` or `official_value_not_seen`.
3. It has a `result` or `expirationValue` in the archived packet.
4. It is not flagged `not_active` and is not `status=finalized`.
5. It has a nonterminal stale quote: `winningAsk < 0.98` or `losingBid > 0.02`.
6. Fees, depth, venue eligibility, and real-money trade gate are verified. In this local-only proof those gates are deliberately absent, so otherwise interesting packets still cannot promote.

## Reproduction Result

- Mode: `offline_local_archived_packets_only`
- Network calls: `False`
- Accounts or credentials: `False`
- Orders or trades: `False`
- Parsed packet rows: `32`
- Actionable candidates: `0`
- Killed candidates: `32`
- Realized USD: `0`

The checker reproduces the killed replay set with `0` actionable candidates.

## Event Status Counts

`{"official_value_seen_no_edge": 8, "pre_close_watch": 4}`

## Kill Reason Counts

| Reason | Count |
| --- | ---: |
| `depth_unverified` | 32 |
| `fees_unverified` | 32 |
| `no_nonterminal_stale_quote` | 12 |
| `not_active_or_finalized` | 32 |
| `real_money_gate_absent` | 32 |
| `review_false` | 32 |
| `venue_eligibility_unverified` | 32 |

## Killed Sample

| Input | Market | Close | Result | Flags | Reasons |
| --- | --- | --- | --- | --- | --- |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59950 $59,900 to 59,999.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60050 $60,000 to 60,099.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59850 $59,800 to 59,899.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59650 $59,600 to 59,699.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59750 $59,700 to 59,799.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60150 $60,100 to 60,199.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60550 $60,500 to 60,599.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60650 $60,600 to 60,699.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60450 $60,400 to 60,499.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60250 $60,200 to 60,299.99 | `2026-06-13T10:00:00Z` | `no` | `not_active` | review_false, not_active_or_finalized, no_nonterminal_stale_quote, fees_unverified, depth_unverified, venue_eligibility_unverified, real_money_gate_absent |

## Next Action

Keep this lane in data/paper mode. The next local-only improvement would be to feed future archived close-window packets into `archived_packet_checker_20260614.py` and compare JSON outputs over time. Do not request real-money review unless a future artifact has nonzero actionable candidates plus verified source of truth, fees, depth, venue eligibility, max loss, kill switch, and an approved exact-scope service request.
