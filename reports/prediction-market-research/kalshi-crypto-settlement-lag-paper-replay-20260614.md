# Kalshi Crypto Settlement-Lag Paper Replay

Generated UTC: 2026-06-14
Lane: `prediction_market_research`
Task: `task-prediction-kalshi-crypto-settlement-lag-replay-20260614`
Agent: `lane-manager-prediction_market_research-relaunch-20260614`

## Hard Stop

Paper/data-only replay from imported local packets. No accounts, credentials, venues, APIs, browser actions, orders, deposits, withdrawals, wallet actions, or real-money trades were used. Realized USD is `0`.

## Inputs

- `kalshi-crypto-settlement-lag-latest.md`: generated `2026-06-14T14:59:07.9148250Z`, status `pre_close_watch`, rows `2804`, review candidates `0`.
- `kalshi-btc-settlement-lag-latest.md`: generated `2026-06-13T10:09:07.5956915Z`, status `official_value_seen_no_edge`, rows `188`, review candidates `0`.
- `kalshi-settlement-lag-latest.md`: generated `2026-06-13T10:09:35.8611115Z`, status `pre_close_watch`, rows `1013`, review candidates `0`.

## Deterministic Checker Criteria

A row is paper-keepable only if all criteria pass:

1. `review=True` in the imported packet.
2. Close time has passed and the packet is not flagged `pre_close` or `official_value_not_seen`.
3. Venue result or `expirationValue` is present in the packet.
4. The market is still active after result publication, meaning it is not flagged `not_active` and not marked `finalized`.
5. The winning side is still offered below the configured stale-quote threshold or the losing side still has a nonterminal bid; terminal `1.0000/0.0000` or `0.0000/1.0000` quotes are killed.
6. Fees, depth, venue eligibility, and real-money gate are all explicitly verified. For this replay they are not verified, so every otherwise interesting row remains paper/no-trade only.

## Replay Summary

- Crypto event status counts: `{"official_value_seen_no_edge": 8, "pre_close_watch": 4}`
- Crypto series counts: `{"KXBTC": 3, "KXDOGE": 3, "KXETH": 3, "KXXRP": 3}`
- Parsed packet rows with result-style fields: `32`
- Kept paper candidates after all deterministic gates: `0`
- Final decision: `no_trade_no_candidate`.
- Realized USD: `0`.

## False-Positive Notes

- Pre-close rows can look tempting because they show nonterminal bid/ask spreads, but they are killed until official result or `expirationValue` appears.
- Official-value-seen rows can contain a clear winner, but rows with `winningAsk=1.0000` and `losingBid=0.0000` are already terminal and have no stale active quote to replay.
- Generic settlement rows can show `directEdge=1`; those are false positives when the same packet is `finalized`, `not_active`, or has terminal `yes/no` quotes.
- Any row still fails real-money promotion because fees, depth, account eligibility, and a scoped `real_money_trade_gate` approval are absent.

## Representative Killed Rows

| Input | Market | Close | Result | Yes | No | Kill reasons |
| --- | --- | --- | --- | --- | --- | --- |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59950 $59,900 to 59,999.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60050 $60,000 to 60,099.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59850 $59,800 to 59,899.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59650 $59,600 to 59,699.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59750 $59,700 to 59,799.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60150 $60,100 to 60,199.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60550 $60,500 to 60,599.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60650 $60,600 to 60,699.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60450 $60,400 to 60,499.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60250 $60,200 to 60,299.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B60350 $60,300 to 60,399.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |
| `kalshi-btc-settlement-lag-latest.md` | KXBTC-26JUN1306-B59550 $59,500 to 59,599.99 | `2026-06-13T10:00:00Z` | `no` | `0.0000/1.0000` | `0.0000/1.0000` | fees_unverified, no_real_money_gate, not_active_or_already_finalized, scanner_review_false, terminal_quotes_no_stale_active_edge, venue_eligibility_unverified |

## Gate Status

| Gate | Status | Note |
| --- | --- | --- |
| Source of truth | partial_local_packet_only | Imported packets include Kalshi result/expiration fields for some rows, but no fresh venue verification was performed. |
| Fees | blocked_unverified | No fee schedule, account fee treatment, or withdrawal/deposit costs verified. |
| Settlement timing | replayed_from_local_packets | T+ rows with official values exist, but all result rows are terminal or inactive. |
| Venue eligibility | blocked_unverified | No account/jurisdiction eligibility check performed. |
| Real-money gate | absent | No approved service request exists for trading. |
| Trading action | forbidden | No orders, API trading, accounts, deposits, withdrawals, or venue actions. |

## Next Action

Keep the lane in data/paper mode. A useful next local proof would be to implement a reusable parser/checker against archived close-window packets and require it to reproduce `0` candidates on this replay before testing future local packets. Do not request real-money review unless a future artifact shows active stale quotes plus verified fees, depth, venue eligibility, max loss, and kill switch.
