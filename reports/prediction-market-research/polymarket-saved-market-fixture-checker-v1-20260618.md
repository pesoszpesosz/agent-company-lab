# Polymarket Saved-Market Fixture Checker

- Generated: `2026-06-18T09:20:02Z`
- Task: `task-polymarket-saved-market-fixture-checker-v1-20260618`
- Status: `polymarket_saved_market_fixture_checker_ready_paper_only`
- Decision: `saved_market_rows_scored_zero_promotable_no_live_api_no_wallet_no_trade`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\prediction-market-research\polymarket-saved-market-fixture-checker-v1-fixture-20260618.json`
- Results: `E:\agent-company-lab\reports\prediction-market-research\polymarket-saved-market-fixture-checker-v1-results-20260618.json`

## Summary

- `row_count`: `4`
- `paper_rows`: `4`
- `promotable_count`: `0`
- `killed_count`: `4`
- `source_acceptance_checks`: `7`

## Paper Rows

| Market | Spread | Liquidity | Decision | Kill Reasons |
| --- | ---: | ---: | --- | --- |
| `example-resolution-lag-yes-no` | 0.05 | 3500 | `kill` | `fees_spread_or_orderbook_depth_unverified`, `jurisdiction_or_platform_variant_unverified`, `max_loss_real_money_gate_absent`, `requires_account_login_wallet_or_private_key`, `requires_api_credentials_eip712_signature_or_hmac_headers`, `requires_bridge_deposit_withdrawal_or_payment_action`, `requires_deposit_wallet_relayer_funding_or_token_approval`, `requires_order_signing_order_posting_cancellation_or_trade_query`, `resolution_source_or_market_rules_unclear`, `terms_kyc_kyb_or_age_eligibility_unreviewed` |
| `example-wide-spread-thin-yes-no` | 0.54 | 40 | `kill` | `fees_spread_or_orderbook_depth_unverified`, `jurisdiction_or_platform_variant_unverified`, `liquidity_too_low_or_market_closed_inactive_or_resolved`, `max_loss_real_money_gate_absent`, `requires_account_login_wallet_or_private_key`, `requires_bridge_deposit_withdrawal_or_payment_action`, `requires_deposit_wallet_relayer_funding_or_token_approval`, `requires_order_signing_order_posting_cancellation_or_trade_query`, `resolution_source_or_market_rules_unclear`, `terms_kyc_kyb_or_age_eligibility_unreviewed` |
| `example-reward-decoy-yes-no` | 0.02 | 80000 | `kill` | `jurisdiction_or_platform_variant_unverified`, `max_loss_real_money_gate_absent`, `requires_account_login_wallet_or_private_key`, `requires_api_credentials_eip712_signature_or_hmac_headers`, `requires_bridge_deposit_withdrawal_or_payment_action`, `requires_deposit_wallet_relayer_funding_or_token_approval`, `requires_order_signing_order_posting_cancellation_or_trade_query`, `requires_worker_runtime_bot_market_making_or_low_latency_infrastructure`, `resolution_source_or_market_rules_unclear`, `terms_kyc_kyb_or_age_eligibility_unreviewed` |
| `example-closed-market-yes-no` | 0.01 | 0 | `kill` | `fees_spread_or_orderbook_depth_unverified`, `jurisdiction_or_platform_variant_unverified`, `liquidity_too_low_or_market_closed_inactive_or_resolved`, `max_loss_real_money_gate_absent`, `requires_account_login_wallet_or_private_key`, `requires_bridge_deposit_withdrawal_or_payment_action`, `requires_deposit_wallet_relayer_funding_or_token_approval`, `requires_order_signing_order_posting_cancellation_or_trade_query`, `terms_kyc_kyb_or_age_eligibility_unreviewed` |

## Required Gates Before Any Live Market Action

- `jurisdiction_and_platform_variant_review`
- `terms_kyc_kyb_age_tax_review`
- `account_login_approval`
- `wallet_private_key_session_signer_approval`
- `deposit_bridge_withdrawal_payment_approval`
- `fee_spread_orderbook_depth_review`
- `resolution_source_and_market_rules_review`
- `max_loss_and_real_money_trade_approval`
- `bot_runtime_or_market_making_approval`
- `public_content_or_referral_approval`

## Boundary

- `saved_market_rows_created`: `4`
- `paper_rows_emitted`: `4`
- `promotable_candidates`: `0`
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

## Next Local Action

Add more manually saved market/event snippets only, or create an exact-scope public-market-data service request. Do not call live APIs, log in, connect/create wallets, use private keys/session signers/API credentials, bridge, deposit, withdraw, approve tokens, post/cancel/sign orders, trade, market make, post referrals, start workers/runtimes, or call model/MCP/external APIs from this packet alone.
