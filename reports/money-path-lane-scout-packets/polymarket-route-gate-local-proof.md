# Polymarket Route Gate Local Proof

- Generated: `2026-06-18T07:27:45Z`
- Task: `task-lane-scout-polymarket_docs_research-20260618`
- Lane: `prediction_market_research`
- Status: `polymarket_route_gate_ready_local_only`
- Decision: `route_gate_only_no_account_no_wallet_no_payment_no_trade_no_runtime`
- Validation: `True` with `0` failures

## Summary

Polymarket can support prediction-market research only as a docs-and-fixture route until jurisdiction, platform variant, account, wallet, fee, liquidity, order signing, bridge/payment, max-loss, and legal gates are reviewed. This packet creates the local route map and paper-signal worksheet without API calls, account work, wallet work, trades, runtime starts, or public actions.

## Jurisdiction Disambiguation

Polymarket international, Polymarket US, and any API/docs route must be treated as separate legal/eligibility surfaces. The user is estimated in the United States, while the current environment timezone is Europe/Sofia; neither fact grants permission to trade. Polymarket US, international Polymarket, KYC/KYB, geoblock, state/country restrictions, wallet custody, tax, and gambling/derivatives rules require human review before any account, wallet, payment, or trade.

## Sources

- `https://docs.polymarket.com/` (official_docs_index): Polymarket docs expose market data, trading, market maker, builder, contracts, data resources, fees, bridges, and availability/legal links. The docs preview new unified TypeScript and Python SDKs, but SDK usage can cross install/runtime/account/wallet gates.
- `https://docs.polymarket.com/market-data/fetching-markets` (official_market_data_docs): Market data can be fetched by slug, tag, or active events endpoint. The events endpoint supports active and closed filters, order fields such as volume, liquidity, start/end date, competitive, and pagination. This is the only route this packet treats as potentially local-fixture-friendly; live API calls still remain gated unless explicitly approved.
- `https://docs.polymarket.com/trading/overview` (official_trading_auth_docs): Polymarket CLOB is a hybrid-decentralized trading system with offchain matching and onchain settlement on Polygon. Trading uses EIP-712 signed orders and L2 HMAC API credentials. Public methods include market data, orderbooks, prices, and spreads; L1/L2 methods include signing orders, deriving API credentials, placing/canceling orders, querying trades, and notifications. Private keys, API credentials, order signing, order posting, and trade operations are blocked by this packet.
- `https://docs.polymarket.com/trading/deposit-wallets` (official_deposit_wallet_docs): Deposit wallets are the wallet path for new API users and can be deployed, funded, approved, synced, and used for POLY_1271 CLOB orders. The flow requires owner/session signer handling, relayer transactions, pUSD funding, approvals, CLOB credentials, and order signing. Every wallet, private key, relayer, funding, approval, allowance, and order step is an explicit human gate.
- `https://docs.polymarket.com/trading/fees` (official_fee_docs): Polymarket charges taker fees on certain markets and makers are not charged fees. Fees depend on market category and share price, and markets expose fee enablement and fee parameters. Any paper signal must include fee and spread gates before promotion; this packet does not calculate or execute real trades.
- `https://docs.polymarket.com/llms.txt` (official_docs_index_machine_readable): The documentation index lists public market-data endpoints such as midpoint, order book, spread, prices, market info, price history, markets, events, rewards, and geoblock. It also lists authenticated relayer, maker, builder, account, position, reward, bridge, and withdrawal endpoints that are blocked here.
- `https://polymarket.com/tos` (official_terms_or_availability): The terms page footer states that Polymarket operates globally through separate legal entities. It identifies Polymarket US as operated by QCX LLC d/b/a Polymarket US, a CFTC-regulated Designated Contract Market. It says the international platform is not regulated by the CFTC, operates independently, and trading involves substantial risk of loss. This makes jurisdiction, platform variant, eligibility, KYC, and legal review mandatory gates.
- `https://docs.polymarket.us/` (official_us_docs_route): Polymarket documentation links separately to Polymarket US documentation. A US-located operator must not treat international docs, US docs, and jurisdiction availability as interchangeable.
- `E:\agent-company-lab\reports\money-path-lane-scout-packets\kalshi-public-data-paper-signal-local-proof.md` (local_prior_prediction_market_packet): The Kalshi packet established the prediction-market rule: paper research only unless account, jurisdiction, fee, orderbook, settlement, max-loss, and real-money gates are proven. Reuse the same default-kill posture for Polymarket.

## Route Fields

- `market_or_event_url`
- `observed_utc`
- `platform_variant`
- `jurisdiction_allowed`
- `account_required`
- `kyc_or_kyb_required`
- `wallet_or_deposit_wallet_required`
- `private_key_or_session_signer_required`
- `api_credentials_required`
- `event_slug`
- `market_slug`
- `condition_id`
- `token_ids`
- `active`
- `closed`
- `end_date`
- `resolution_source`
- `outcomes`
- `best_bid`
- `best_ask`
- `midpoint`
- `spread`
- `last_trade_price`
- `volume`
- `volume_24hr`
- `liquidity`
- `open_interest`
- `fees_enabled`
- `fee_parameters`
- `orderbook_depth_available`
- `settlement_or_resolution_status`
- `data_source_for_truth`
- `category_or_tag`
- `regulatory_or_terms_risk`
- `max_loss_if_promoted`
- `paper_signal_score`
- `kill_reasons`
- `next_local_action`

## Route Stages

- `docs_only_route_map`: Extract market-data, trading, wallet, fee, bridge, legal, and availability gates from public docs. Gate `public_read_only`. Allowed now `True`.
- `saved_market_fixture`: Use manually saved event/market JSON snippets or prior local rows to test parser logic without live API calls. Gate `local_fixture_only`. Allowed now `True`.
- `paper_signal_scoring`: Score only hypothetical rows using liquidity, spread, fee, resolution, and max-loss blockers. Gate `local_paper_only`. Allowed now `True`.
- `public_market_data_refresh`: Call public Gamma/CLOB market-data endpoints for active rows. Gate `explicit_public_api_approval_required`. Allowed now `False`.
- `wallet_account_payment_gate`: Create/login account, connect wallet, derive API credentials, deploy/fund deposit wallet, approve tokens, bridge, deposit, withdraw, or handle payment/tax. Gate `explicit_account_wallet_payment_approval_required`. Allowed now `False`.
- `trade_execution_gate`: Sign order, post/cancel order, query authenticated trades, market make, run bot/runtime, or perform real-money trade. Gate `explicit_real_money_trade_approval_required`. Allowed now `False`.
- `public_content_or_affiliate_gate`: Post, refer, affiliate-promote, comment, share, or publish market claims. Gate `explicit_public_action_approval_required`. Allowed now `False`.

## Paper Signal Tests

- `wide_spread_watch`: Identify wide-spread markets where apparent mispricing disappears after fee, depth, and execution checks. Default decision: kill unless public fixture has bid/ask, liquidity, fee status, resolution source, jurisdiction, and max-loss approval.
- `resolution_lag_watch`: Detect markets near or after resolution where source truth appears settled but market status lags. Default decision: paper-only because live trading requires account, wallet, order signing, settlement, and legal gates.
- `category_fee_drag_watch`: Estimate whether taker fees and spread erase a naive edge by category and share price. Default decision: kill unless fee parameters, spread, and executable depth are present.
- `liquidity_reward_decoy_watch`: Reject rows where rewards or volume look attractive but require market-maker operations, runtime, or KYC/KYB. Default decision: local research only; rewards, builders, market making, and runtimes remain blocked.

## Hard Kill Reasons

- `jurisdiction_or_platform_variant_unverified`
- `terms_kyc_kyb_or_age_eligibility_unreviewed`
- `requires_account_login_wallet_or_private_key`
- `requires_deposit_wallet_relayer_funding_or_token_approval`
- `requires_bridge_deposit_withdrawal_or_payment_action`
- `requires_api_credentials_eip712_signature_or_hmac_headers`
- `requires_order_signing_order_posting_cancellation_or_trade_query`
- `fees_spread_or_orderbook_depth_unverified`
- `resolution_source_or_market_rules_unclear`
- `liquidity_too_low_or_market_closed_inactive_or_resolved`
- `max_loss_real_money_gate_absent`
- `requires_worker_runtime_bot_market_making_or_low_latency_infrastructure`
- `public_claim_affiliate_or_referral_action_required`

## Boundary

- `browser_sessions_started`: `0`
- `polymarket_account_or_login`: `False`
- `polymarket_us_account_or_login`: `False`
- `wallet_created_or_connected`: `False`
- `private_key_or_session_signer_used`: `False`
- `api_credentials_created_or_used`: `False`
- `market_data_api_calls`: `0`
- `orderbook_api_calls`: `0`
- `relayer_or_bridge_calls`: `0`
- `deposits_withdrawals_or_wallet_approvals`: `0`
- `orders_or_trades`: `0`
- `payments_or_tax_forms`: `0`
- `public_actions_or_referrals`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a Polymarket saved-market fixture parser/checker from manually saved docs/API examples only; emit paper-only rows with spread, fee, liquidity, resolution, jurisdiction, wallet, and max-loss kill reasons. Keep live API calls, account/login, Polymarket US onboarding, wallet/private-key/session-signer work, deposits, withdrawals, bridge, payments, trades, market-making, public posts/referrals, worker/runtime, and model/MCP calls blocked.
