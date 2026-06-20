# Money Source Weekly Delta Local Dry Run - 20260614

Lane: `money_source_discovery`
Task: `task-money-source-weekly-delta-local-dry-run-20260614`
Owner agent: `lane-manager-money_source_discovery-019ec699`
Realized USD: `0`
Status: local proof artifact, no external verification

## Boundary

This dry run uses only existing local Wave-4 artifacts:

- `E:\agent-company-lab\data\money-path-source-registry-wave4-20260614.json`
- `E:\agent-company-lab\reports\agent-company-money-path-wave4-20260614.md`
- `E:\agent-company-lab\reports\lane-startup\money_source_discovery-startup-20260614.md`

No browser, account, API, public action, signup, application, submission, trade, wallet, payment, current-source verification, scraping, or work on `submitted_bounty_payouts` was performed. All external URLs below are copied from local Wave-4 files and remain `local_seed_unverified`.

## Method

I normalized the 32 representative local-source records from the Wave-4 JSON into 16 route-level weekly-delta rows. The table is meant to answer three questions before any future service request is used:

- What is the money route?
- Which owner lane should test it?
- What gate stops action, and what local proof artifact should come first?

Proof artifact paths in the table are planned destination paths for the next local proof packet. They are not submissions, browser captures, public claims, or evidence of current venue availability.

## Weekly Delta Table

Base proof-queue directory: `E:\agent-company-lab\reports\money-source-discovery\proof-queue`

| ID | Candidate source and local URL seed | Money route | Current-source status | Owner lane | Gate class | First local proof artifact path | Delta decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MSD-001 | Current Wave reports, `E:\agent-company-lab\reports` | Internal source routing intelligence that feeds all money lanes | `local_seed_verified_local_file` | `money_source_discovery` | Local file read only | `E:\agent-company-lab\reports\money-source-discovery\weekly-delta-local-dry-run-20260614.md` | Keep as the control row for weekly-delta format and evidence discipline |
| MSD-002 | GitHub search, `https://github.com/search`; starter target `https://github.com/topics/bounty` | Explicit paid-code bounty and security lead discovery | `local_seed_unverified` | `paid_code_bounties`, `security_bounty_private_reports` | Approved browser-read-only first; later GitHub public-action/security gates | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\github-bounty-source-capture-20260614.md` | Promote only to read-only capture after browser request approval; no claims/comments/PRs |
| MSD-003 | Kaggle competitions, `https://www.kaggle.com/competitions?prestigeFilter=money` | Money-prize ML competitions | `local_seed_unverified` | `ai_ml_competitions` | Account, rules, dataset license, compute/API spend, submission | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\kaggle-prize-scout-20260614.md` | Route to competition scout; first proof is rules/prize/deadline/baseline table, no submission |
| MSD-004 | DrivenData competitions, `https://www.drivendata.org/competitions/` | Data science competition prizes | `local_seed_unverified` | `ai_ml_competitions` | Account, rules, data license, final submission | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\drivendata-prize-scout-20260614.md` | Route after browser approval to compare active contests against Kaggle-style proof rubric |
| MSD-005 | ML Contests, `https://mlcontests.com/` | Aggregated ML, data, and robotics competitions | `local_seed_unverified` | `ai_ml_competitions` | Browser-read-only approval before current listings; account/submission gates later | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\mlcontests-aggregator-scout-20260614.md` | Use as aggregator source, not as proof of active prize availability until refreshed |
| MSD-006 | lablab.ai hackathons, `https://lablab.ai/ai-hackathons` | AI hackathon prizes, sponsor tracks, project visibility | `local_seed_unverified` | `ai_ml_competitions` | Registration, team eligibility, rules, public submission, possible API/compute cost | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\lablab-ai-hackathon-scout-20260614.md` | Promote for local feasibility scoring; no registration or project submission |
| MSD-007 | ETHGlobal, `https://ethglobal.com/` | Web3 hackathon prizes and sponsor bounties | `local_seed_unverified` | `web3_airdrops_grants_hackathons`, `ai_ml_competitions` | Registration, wallet, deployment, team, public submission, legal/terms | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\ethglobal-hackathon-gate-scout-20260614.md` | Keep gated; valuable only if wallet/deployment/submission path is user-approved |
| MSD-008 | Gumroad, `https://gumroad.com/` | Digital product storefront revenue | `local_seed_unverified` | `digital_products_templates_plugins` | Seller account, payment/tax setup, listing, public promotion, IP review | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\gumroad-product-route-packet-20260614.md` | Route to local prototype packet only; no marketplace account/listing |
| MSD-009 | Lemon Squeezy digital products, `https://www.lemonsqueezy.com/ecommerce/digital-products` | Digital product sales, SaaS billing, merchant-of-record route | `local_seed_unverified` | `digital_products_templates_plugins` | Seller account, payment/tax, terms, product listing, support obligations | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\lemon-squeezy-route-packet-20260614.md` | Compare as payment/distribution route, but stop before account/payment setup |
| MSD-010 | PromptBase sell prompts/skills, `https://promptbase.com/sell` | Prompt, agent skill, and template marketplace sales | `local_seed_unverified` | `digital_products_templates_plugins` | Marketplace account, payout setup, listing review, IP/copyright, public claims | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\promptbase-skill-marketplace-packet-20260614.md` | Good fit for local Codex skill pack proof; no listing or payout setup |
| MSD-011 | Notion Marketplace, `https://www.notion.com/templates` | Paid or discoverable templates | `local_seed_unverified` | `digital_products_templates_plugins` | Creator account, marketplace terms, listing, payment/tax where applicable | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\notion-template-route-packet-20260614.md` | Route to local Notion/ops template prototype packet; no submission |
| MSD-012 | Shopify app/theme revenue share, `https://shopify.dev/docs/apps/launch/distribution/revenue-share`; Shopify Partners, `https://www.shopify.com/partners` | App, theme, partner, or commerce service revenue | `local_seed_unverified` | `digital_products_templates_plugins`, `productized_services_marketplaces` | Partner account, app review, revenue share, payment/tax, public listing/support | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\shopify-app-theme-route-packet-20260614.md` | Higher gate burden; local proof should be an app/theme diagnostic packet first |
| MSD-013 | Upwork, `https://www.upwork.com/`; Fiverr, `https://www.fiverr.com/` | Productized service marketplace cashflow | `local_seed_unverified` | `productized_services_marketplaces`, `lead_generation_and_sales` | Marketplace account, KYC/tax/payment, proposals, outreach, reputation/public-action | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\service-marketplace-offer-packets-20260614.md` | Build fictional fixed-scope offer samples only; no leads/proposals/messages |
| MSD-014 | uTest, `https://www.utest.com/`; UserTesting, `https://www.usertesting.com/get-paid-to-test`; Test IO, `https://test.io/company/become-a-tester`; Applause/uTest, `https://www.applause.com/blog/work-from-home-with-utest/` | Human paid testing and usability feedback | `local_seed_unverified` | `qa_usability_testing_gigs` | Human-only work, real device/user feedback, account, KYC/tax/payment | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\qa-usability-human-gig-eligibility-20260614.md` | Preparation-only lane; proof is a QA practice kit and eligibility table |
| MSD-015 | DataAnnotation, `https://www.dataannotation.tech/`; Outlier, `https://outlier.ai/`; Toloka, `https://toloka.ai/`; TELUS Digital AI, `https://www.telusinternational.ai/`; Prolific, `https://www.prolific.com/participants` | Human AI-training, data annotation, expert review, and paid studies | `local_seed_unverified` | `ai_training_eval_gigs` | Human-only paid work, identity/account, KYC/tax/payment, privacy, no automation | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\ai-training-human-only-risk-packet-20260614.md` | Keep as human decision intelligence; agents must not do the paid tasks |
| MSD-016 | PartnerStack, `https://partnerstack.com/partners-and-publishers`; PartnerStack marketplace, `https://market.partnerstack.com/`; impact.com, `https://impact.com/partners/affiliate-partners/`; Rewardful, `https://www.rewardful.com/affiliate-program`; FirstPromoter, `https://firstpromoter.com/affiliate-program` | Affiliate, referral, or recurring SaaS commissions | `local_seed_unverified` | `affiliate_partner_programs`, `content_and_social_growth` | Program application, disclosure compliance, public content/link placement, outreach, payout setup | `E:\agent-company-lab\reports\money-source-discovery\proof-queue\affiliate-program-scout-table-20260614.md` | Useful later; first proof is 25-program scout table after read-only approval |

## Gate Summary

| Gate | Rows affected | Service or owner needed before external action |
| --- | --- | --- |
| Browser-read-only approval | MSD-002 through MSD-016 | `browser_read_only_session`, request must be approved with exact read scope |
| Account registration or marketplace account | MSD-003 through MSD-016 except local-only MSD-001 | `account_registration_worker` |
| Legal, KYC, tax, payment, payout, or billing | MSD-008 through MSD-016, plus any prize payout route | `legal_kyc_tax_payment_gate` |
| Public action or submission | MSD-002, MSD-003, MSD-006, MSD-007, MSD-008 through MSD-013, MSD-016 | `public_action_execution` or lane-specific submission gate |
| Human-only work | MSD-014 and MSD-015 | User-only decision; agents may prepare packets but must not perform paid tasks |
| Wallet, deployment, or web3 transaction | MSD-007 | wallet/deployment gates; no autonomous wallet or transaction action |
| Paid compute, model/API, or data access | MSD-003, MSD-006, MSD-012 where relevant | `model_api_execution_gate` or `data_purchase_api_access_gate` |

## First Follow-Up Proof

Recommended next local task if the browser request remains unapproved:

`task-money-source-proof-queue-schema-20260614`

Produce a small machine-readable queue file from this table with columns:

- candidate_id
- source_urls
- owner_lane
- gate_class
- planned_proof_artifact_path
- current_source_status
- blocked_until

Recommended next task if `req-wave4-money-source-discovery-browser-readonly-20260614` is approved:

Use only the approved read scope to fill `browser-readonly-capture.md` with visible source URLs, rules links, payout routes, account gates, and first proof tasks. Stop immediately at login, consent, payment, account settings, private data, public actions, platform uncertainty, or rate-limit/scraping concerns.

## Outcome

This dry run creates a repeatable weekly delta format and a 16-row candidate routing table. It does not claim current availability, expected revenue, account eligibility, or realized earnings.

`realized_usd=0`
