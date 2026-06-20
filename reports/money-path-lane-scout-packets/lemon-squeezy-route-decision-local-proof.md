# Lemon Squeezy Route Decision Local Proof

- Generated: `2026-06-18T07:06:11Z`
- Task: `task-lane-scout-lemon_squeezy_digital_products-20260618`
- Lane: `digital_products_templates_plugins`
- Status: `lemon_squeezy_route_decision_ready_local_only`
- Decision: `promising_but_gated_no_account_no_payment_no_public_action`
- Validation: `True` with `0` failures

## Summary

Lemon Squeezy remains a strong candidate for selling digital downloads, software licenses, lead magnets, bundles, and small SaaS assets, especially because of MoR/tax/fraud positioning. The route is not launch-ready: the next aligned step is a local product-readiness and launch-approval packet, not a store, account, upload, checkout, payment setup, API integration, or public listing.

## Sources

- `https://www.lemonsqueezy.com/` (official_home): Lemon Squeezy is positioned for payments, tax, subscriptions, software licenses, and digital downloads. It advertises merchant-of-record tax/compliance, fraud prevention, multi-currency support, PayPal, hosted checkouts, lead magnets, and pay-what-you-want. Homepage copy says digital downloads, subscriptions, and software licenses are core use cases.
- `https://www.lemonsqueezy.com/pricing` (official_pricing): Public pricing lists ecommerce at 5% plus 50 cents per transaction, with no monthly ecommerce charges. Pricing page highlights automated sales tax compliance, AI fraud protection, license key management, digital downloads, bundles, upsells, discounts, lead magnets, and revenue reporting. Some payments may have additional fees, so final margin requires payment-method and payout review.
- `https://www.lemonsqueezy.com/blog/2026-update` (official_2026_update): Lemon Squeezy says it is building with Stripe Managed Payments after Stripe acquired Lemon Squeezy. The 2026 update says Managed Payments handles global payments, tax compliance, fraud protection, disputes, and customer support across key markets. It says Managed Payments supported merchants in 35+ countries at publication and public access/migration was still evolving.
- `https://www.lemonsqueezy.com/blog/merchant-of-record` (official_mor_explainer): Merchant-of-record positioning reduces payment, refund, chargeback, tax collection, and global compliance burden. It also means seller/business compliance, product legality, IP, refunds, and customer promises still require operator review.
- `https://docs.lemonsqueezy.com/guides/developer-guide/getting-started` (official_api_docs): API access requires a private API key and Bearer authentication. API capabilities include products, customers, discounts, files, checkouts, orders, subscriptions, and license keys. API keys must not be saved in code or GitHub; therefore any API usage is gated.
- `https://www.lemonsqueezy.com/terms` (official_terms): Terms place important responsibility on the customer for legal/regulatory compliance and business decisions. Terms disclaim guaranteed results and include liability/indemnification limits that must be reviewed before launch.
- `E:\agent-company-lab\reports\money-path-lane-scout-packets\gumroad-direct-download-local-proof.md` (local_prior_packet): Prior Gumroad packet recommended Agent Skill Starter Kit v0 as a direct-download route. The same product can be evaluated against Lemon Squeezy, but only as local packaging/readiness until account, legal, payout, tax, product, and public-listing approval exists.
- `E:\agent-company-lab\reports\money-path-lane-scout-packets\promptbase-approval-rubric-local-proof.md` (local_prior_packet): Prior PromptBase work already created approval-rubric discipline for digital products. Reuse that rubric style for Lemon Squeezy: forbidden claims, asset ownership, refund/support terms, and launch checklist.

## Route Decision

- Route: `lemon_squeezy_digital_product_store`
- Decision: `promising_but_not_first_public_route_until_2026_managed_payments_and_operator_account_gates_are_reviewed`
- Recommended product: `Agent Skill Starter Kit v0 or a narrower AI workflow audit template pack`
- First allowed step: `local product readiness and launch approval packet only`

## Product Fit Matrix

| Product type | Fit | Example | Local requirements | Blocked until approval |
|---|---|---|---|---|
| direct_download_template_pack | high | Agent Skill Starter Kit v0 zip with docs, worksheets, and examples | license file; refund/support draft; checksum; sample screenshots; buyer promise audit | storefront; file upload; checkout; payment; public listing |
| software_license_key_pack | medium | small local CLI or template generator with license-key delivery | license-key logic design; offline activation fallback; support policy; security review | API key; license endpoint; customer data; checkout |
| subscription_saas | medium_later | monthly agent-company research brief or monitoring dashboard | recurring value proof; churn/support model; terms; privacy/data handling | subscriptions; customer portal; payment; email marketing |
| lead_magnet | high_for_audience_building_low_direct_cash | free AI workflow gate checklist feeding later paid product | email copy; privacy notice; no-spam policy; handoff to content lane | email capture; public promotion; mailing list |
| pay_what_you_want | experimental | public checklist or mini-template with optional payment | minimum-price decision; support burden cap; abuse/fraud expectation | checkout; payments; public listing |

## Launch Gates

- `country_and_managed_payments_availability_review`
- `account_creation_and_terms_acceptance_approval`
- `business_identity_tax_and_payout_review`
- `product_ip_license_and_asset_ownership_review`
- `refund_support_and_customer_promise_review`
- `prohibited_or_restricted_product_review`
- `pricing_margin_review_including_5_percent_plus_50_cent_fee_and_extra_payment_fees`
- `storefront_copy_screenshot_and_forbidden_claims_review`
- `zip_checksum_and_file_delivery_security_review`
- `privacy_customer_data_and_email_marketing_review`
- `api_key_secret_storage_review_before_any_api_or_webhook_work`
- `public_listing_and_launch_approval`

## Next Local Artifacts

- `product_readiness_matrix.md`
- `launch_approval_packet.md`
- `refund_support_terms_draft.md`
- `zip_manifest_and_checksum.json`
- `forbidden_claims_checklist.json`
- `pricing_margin_scenarios.csv`

## Hard Kill Reasons

- `managed_payments_or_country_support_unavailable`
- `operator_declines_account_terms_or_payout_setup`
- `product_ip_or_asset_rights_unclear`
- `product_category_restricted_or_terms_risk_unreviewed`
- `support_refund_or_customer_promise_unbounded`
- `gross_margin_too_low_after_fee_payment_method_refund_and_support_costs`
- `requires_api_keys_or_customer_data_before approval`
- `requires_public_listing_or_email_capture_before privacy_review`
- `product_value_not_distinct_from_existing_free_material`
- `cannot_produce_secure_zip_manifest_and_buyer_docs_locally`

## Boundary

- `browser_sessions_started`: `0`
- `lemon_squeezy_account_or_login`: `False`
- `terms_or_payout_accepted`: `False`
- `product_or_storefront_created`: `False`
- `files_uploaded`: `0`
- `checkout_or_payment_links_created`: `0`
- `payments_or_payout_setup`: `0`
- `api_keys_created_or_used`: `0`
- `customer_data_processed`: `0`
- `public_listing_or_promotion`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a Lemon Squeezy launch approval packet for Agent Skill Starter Kit v0 or a narrower AI workflow audit template pack, including product IP/license review, refund/support terms, forbidden claims, pricing margin scenarios, zip checksum plan, country/Managed Payments availability review, payout/tax/account gate, and explicit public-listing approval. Keep account, terms acceptance, payouts, uploads, checkouts, API keys, customer data, email capture, public promotion, worker/runtime, model/MCP, and all external actions blocked.
