# Agent Company Source Specs

Generated UTC: 2026-06-15T17:08:08Z
Source definition: `E:\agent-company-lab\architecture\source-specs-draft.json`

## Boundary

- Each source spec belongs to exactly one lane.
- Refresh commands are instructions for lane owners, not blanket permission to execute side effects.
- Browser, account, wallet, public-action, legal/KYC/billing, and real-money gates still require service requests.

## Specs

| Lane | Spec | Type | Cadence | Gate | Outputs |
| --- | --- | --- | --- | --- | --- |
| `ai_ml_competitions` | `ai_ml_competitions_public_prize_source_seed` - AI/ML Competition Public Prize Source Seed | public_competition_registry | lane_owner_on_demand_or_weekly | read_only_public_research_no_account_submission_dataset_download_or_terms_acceptance | E:\agent-company-lab\reports\ai-ml-competitions\public-prize-source-refresh-YYYYMMDD.md; lane_evidence; service_request_candidates |
| `content_and_social_growth` | `content_grok_x_read_only_research` - Grok/X Read-Only Research | browser_or_api_research | service_request_only | no_public_x_action_no_like_follow_reply_post_no_account_setting_change | E:\agent-company-lab\data\x-grok-research\; service_requests |
| `digital_products_templates_plugins` | `digital_products_marketplace_demand_source_seed` - Digital Product Marketplace Demand Source Seed | public_marketplace_research | lane_owner_on_demand_or_weekly | read_only_market_research_no_listing_account_payment_or_public_submission | E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-demand-refresh-YYYYMMDD.md; lane_evidence; legal_kyc_tax_payment_gate_candidates |
| `lead_generation_and_sales` | `lead_generation_policy_sources` - Lead Generation Policy and Offer Sources | policy_and_crm_design | lane_owner_on_demand | no_spam_no_outreach_no_account_action_without_service_request_and_policy_review | lead generation manager packet |
| `local_trading_strategy_research` | `local_trading_research_import` - Local Trading Research Import | local_workspace | lane_owner_on_demand | paper_backtest_only_until_broker_treasury_and_real_money_gate_clear | local_trading manager packet |
| `money_source_discovery` | `money_source_discovery_public_venue_source_seed` - Money Source Discovery Public Venue Source Seed | public_venue_registry | lane_owner_on_demand_or_weekly | read_only_discovery_no_registration_outreach_wallet_payment_or_submission | E:\agent-company-lab\reports\money-source-discovery\public-venue-source-refresh-YYYYMMDD.md; lane_evidence; service_request_candidates |
| `paid_code_bounties` | `paid_code_profit_edge_scan_import` - Paid Code Scan Import | local_reports | lane_owner_on_demand | read_only_until_claim_rules_duplicate_checks_and_public_action_approval | lane_evidence; paid_code_bounties manager packet |
| `platform_engineering` | `platform_infra_repo_metadata` - Agent Infrastructure GitHub Metadata | github_metadata | weekly_or_before_architecture_choice | read_only_github_metadata | E:\agent-company-lab\data\curated-infra-repos-refresh-YYYYMMDD.json; E:\agent-company-lab\data\curated-infra-repos-refresh-YYYYMMDD.csv |
| `platform_engineering` | `platform_official_docs_refresh` - Official Agent Infrastructure Docs | web_docs | weekly_or_before_framework_commitment | read_only_web_research | E:\agent-company-lab\reports\source-research-refresh-YYYYMMDD.md |
| `platform_engineering` | `platform_profit_edge_daily_queue` - Profit Edge Daily Queue Snapshot | local_markdown | on_demand_before_ceo_review | read_only_local_import_no_execution_lane_ownership | E:\agent-company-lab\reports\profit-edge-import-latest.md; lane_evidence |
| `prediction_market_research` | `prediction_profit_edge_scan_import` - Prediction Market Research Import | local_reports | lane_owner_on_demand_or_scheduled_capture | data_only_until_venue_eligibility_fees_treasury_and_real_money_gate_clear | lane_evidence; prediction manager packet; paper/replay artifact |
| `security_bounty_private_reports` | `security_profit_edge_scan_import` - Security Bounty and Private Report Import | local_reports | lane_owner_on_demand | read_only_static_review_until_program_scope_user_approval_and_private_route_clear | lane_evidence; security manager packet |
| `web3_airdrops_grants_hackathons` | `web3_profit_edge_terms_import` - Web3 Terms and Target Import | local_reports | lane_owner_on_demand | no_wallet_registration_deployment_transaction_or_submission_without_user_approval | lane_evidence; web3 manager packet |

## Detail

### ai_ml_competitions_public_prize_source_seed

- Lane: `ai_ml_competitions`
- Name: AI/ML Competition Public Prize Source Seed
- Type: `public_competition_registry`
- Cadence: `lane_owner_on_demand_or_weekly`
- Gate: `read_only_public_research_no_account_submission_dataset_download_or_terms_acceptance`
- Refresh command: `Prepare a read-only public listing scan only after lane manager claim; save results to a dated local shortlist artifact.`
- Notes: Use to find prize competitions and benchmark tasks. Account creation, dataset download behind terms, submissions, and paid compute all require separate gates.
- Sources:
  - `Kaggle competitions listing`
  - `DrivenData competitions listing`
  - `EvalAI challenges listing`
  - `AICrowd challenges listing`
  - `Hugging Face competitions/spaces calls when prize route is explicit`
- Outputs:
  - `E:\agent-company-lab\reports\ai-ml-competitions\public-prize-source-refresh-YYYYMMDD.md`
  - `lane_evidence`
  - `service_request_candidates`

### content_grok_x_read_only_research

- Lane: `content_and_social_growth`
- Name: Grok/X Read-Only Research
- Type: `browser_or_api_research`
- Cadence: `service_request_only`
- Gate: `no_public_x_action_no_like_follow_reply_post_no_account_setting_change`
- Refresh command: `Use grok-x-research skill only after service request approval; save prompt/output/verification artifacts.`
- Notes: Current request exists as req-grok-research-worker-20260614 and remains needs_review.
- Sources:
  - `https://x.com/i/grok`
  - `local x account manager workspace`
- Outputs:
  - `E:\agent-company-lab\data\x-grok-research\`
  - `service_requests`

### digital_products_marketplace_demand_source_seed

- Lane: `digital_products_templates_plugins`
- Name: Digital Product Marketplace Demand Source Seed
- Type: `public_marketplace_research`
- Cadence: `lane_owner_on_demand_or_weekly`
- Gate: `read_only_market_research_no_listing_account_payment_or_public_submission`
- Refresh command: `Prepare a read-only demand and fee scan only after lane manager claim; no listing, account, checkout, or payment action.`
- Notes: Use to identify sellable template/plugin ideas and marketplace blockers. Publishing/listing/payment setup requires explicit service requests.
- Sources:
  - `Gumroad public marketplace/search pages`
  - `Lemon Squeezy storefront examples`
  - `Etsy digital product public category pages`
  - `GitHub trending/template/plugin repositories`
  - `Codex/OpenAI plugin and skill local product notes`
- Outputs:
  - `E:\agent-company-lab\reports\digital-products-templates-plugins\marketplace-demand-refresh-YYYYMMDD.md`
  - `lane_evidence`
  - `legal_kyc_tax_payment_gate_candidates`

### lead_generation_policy_sources

- Lane: `lead_generation_and_sales`
- Name: Lead Generation Policy and Offer Sources
- Type: `policy_and_crm_design`
- Cadence: `lane_owner_on_demand`
- Gate: `no_spam_no_outreach_no_account_action_without_service_request_and_policy_review`
- Refresh command: `Draft policy and offer packets only; no email, DM, marketplace, or CRM action.`
- Notes: This lane starts with compliance and targeting rules, not sending messages.
- Sources:
  - `future outreach policy notes`
  - `future offer templates`
- Outputs:
  - `lead generation manager packet`

### local_trading_research_import

- Lane: `local_trading_strategy_research`
- Name: Local Trading Research Import
- Type: `local_workspace`
- Cadence: `lane_owner_on_demand`
- Gate: `paper_backtest_only_until_broker_treasury_and_real_money_gate_clear`
- Refresh command: `Read-only inventory first; no broker/API/trading action.`
- Notes: Do not duplicate OpenClaw trading execution; import patterns only.
- Sources:
  - `C:\Users\matth\Documents\Codex\2026-06-12\recovered-trading-edge`
  - `E:\openclaw-unified`
- Outputs:
  - `local_trading manager packet`

### money_source_discovery_public_venue_source_seed

- Lane: `money_source_discovery`
- Name: Money Source Discovery Public Venue Source Seed
- Type: `public_venue_registry`
- Cadence: `lane_owner_on_demand_or_weekly`
- Gate: `read_only_discovery_no_registration_outreach_wallet_payment_or_submission`
- Refresh command: `Prepare a read-only source registry scan only after lane manager claim; classify venue, payout route, account gate, and proof artifact.`
- Notes: Use to widen the online money-path map. Any registration, outreach, wallet, payment, or public submission remains separately gated.
- Sources:
  - `public bounty and paid-task venue lists`
  - `grant and hackathon aggregators`
  - `creator-marketplace opportunity lists`
  - `AI evaluation and data-labeling opportunity pages`
  - `local profit-edge imported negative and parked rows`
- Outputs:
  - `E:\agent-company-lab\reports\money-source-discovery\public-venue-source-refresh-YYYYMMDD.md`
  - `lane_evidence`
  - `service_request_candidates`

### paid_code_profit_edge_scan_import

- Lane: `paid_code_bounties`
- Name: Paid Code Scan Import
- Type: `local_reports`
- Cadence: `lane_owner_on_demand`
- Gate: `read_only_until_claim_rules_duplicate_checks_and_public_action_approval`
- Refresh command: `Run only from paid_code_bounties lane owner after claim: E:\profit-edge-lab scanner scripts listed in README.`
- Notes: Imported rows are mostly negative samples. Do not submit PRs from platform_engineering.
- Sources:
  - `E:\profit-edge-lab\reports\bounty-scan-latest.md`
  - `E:\profit-edge-lab\reports\github-fresh-bounty-pulse-latest.md`
  - `E:\profit-edge-lab\reports\algora-bounty-scan-latest.md`
  - `E:\profit-edge-lab\reports\opire-bounty-scan-latest.md`
  - `E:\profit-edge-lab\reports\bountyhub-bounty-scan-latest.md`
  - `E:\profit-edge-lab\reports\gibwork-bounty-scan-latest.md`
  - `E:\profit-edge-lab\reports\gitpay-task-scan-latest.md`
  - `E:\profit-edge-lab\reports\unitone-skill-bounty-scan-latest.md`
  - `E:\profit-edge-lab\reports\projectdiscovery-bounty-scan-latest.md`
- Outputs:
  - `lane_evidence`
  - `paid_code_bounties manager packet`

### platform_infra_repo_metadata

- Lane: `platform_engineering`
- Name: Agent Infrastructure GitHub Metadata
- Type: `github_metadata`
- Cadence: `weekly_or_before_architecture_choice`
- Gate: `read_only_github_metadata`
- Refresh command: `gh repo view <repo> --json nameWithOwner,description,stargazerCount,forkCount,primaryLanguage,licenseInfo,url,updatedAt,latestRelease`
- Notes: Use for architecture research only; not a signal to file issues or PRs.
- Sources:
  - `microsoft/agent-framework`
  - `pydantic/pydantic-ai`
  - `PrefectHQ/prefect`
  - `dagster-io/dagster`
  - `ray-project/ray`
  - `langfuse/langfuse`
  - `Arize-ai/phoenix`
  - `vercel-labs/agent-browser`
- Outputs:
  - `E:\agent-company-lab\data\curated-infra-repos-refresh-YYYYMMDD.json`
  - `E:\agent-company-lab\data\curated-infra-repos-refresh-YYYYMMDD.csv`

### platform_official_docs_refresh

- Lane: `platform_engineering`
- Name: Official Agent Infrastructure Docs
- Type: `web_docs`
- Cadence: `weekly_or_before_framework_commitment`
- Gate: `read_only_web_research`
- Refresh command: `Use web research and save citations into a dated source-refresh report.`
- Notes: Prefer official docs and primary GitHub repos over blog/tutorial summaries.
- Sources:
  - `https://docs.langchain.com/oss/python/langgraph/overview`
  - `https://developers.openai.com/api/docs/guides/agents`
  - `https://openai.github.io/openai-agents-python/agents/`
  - `https://learn.microsoft.com/en-us/agent-framework/overview/`
  - `https://pydantic.dev/docs/ai/overview/`
  - `https://docs.crewai.com/`
  - `https://pydantic.dev/docs/ai/integrations/durable_execution/temporal/`
  - `https://www.prefect.io/solutions/agents`
  - `https://docs.dagster.io/`
  - `https://langfuse.com/docs/observability/overview`
  - `https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/instrument`
  - `https://agent-browser.dev/`
- Outputs:
  - `E:\agent-company-lab\reports\source-research-refresh-YYYYMMDD.md`

### platform_profit_edge_daily_queue

- Lane: `platform_engineering`
- Name: Profit Edge Daily Queue Snapshot
- Type: `local_markdown`
- Cadence: `on_demand_before_ceo_review`
- Gate: `read_only_local_import_no_execution_lane_ownership`
- Refresh command: `powershell -ExecutionPolicy Bypass -File E:\profit-edge-lab\scripts\Build-DailyActionQueue.ps1`
- Notes: Use for lane-routing context only. Do not act on the promoted RustChain payout item from this thread.
- Sources:
  - `E:\profit-edge-lab\reports\daily-action-queue-latest.md`
- Outputs:
  - `E:\agent-company-lab\reports\profit-edge-import-latest.md`
  - `lane_evidence`

### prediction_profit_edge_scan_import

- Lane: `prediction_market_research`
- Name: Prediction Market Research Import
- Type: `local_reports`
- Cadence: `lane_owner_on_demand_or_scheduled_capture`
- Gate: `data_only_until_venue_eligibility_fees_treasury_and_real_money_gate_clear`
- Refresh command: `Run only from prediction_market_research lane owner after claim; use paper/data-only mode.`
- Notes: Treat Polymarket as data-only for a US user unless eligibility changes are explicitly verified.
- Sources:
  - `E:\profit-edge-lab\reports\prediction-market-scan-latest.md`
  - `E:\profit-edge-lab\reports\cross-venue-next-team-latest.md`
  - `E:\profit-edge-lab\reports\polymarket-tennis-edge-packet-latest.md`
  - `E:\profit-edge-lab\reports\kalshi-btc-range-edge-latest.md`
  - `E:\profit-edge-lab\reports\kalshi-btc-settlement-lag-latest.md`
  - `E:\profit-edge-lab\reports\kalshi-crypto-settlement-lag-latest.md`
  - `E:\profit-edge-lab\reports\kalshi-settlement-lag-latest.md`
- Outputs:
  - `lane_evidence`
  - `prediction manager packet`
  - `paper/replay artifact`

### security_profit_edge_scan_import

- Lane: `security_bounty_private_reports`
- Name: Security Bounty and Private Report Import
- Type: `local_reports`
- Cadence: `lane_owner_on_demand`
- Gate: `read_only_static_review_until_program_scope_user_approval_and_private_route_clear`
- Refresh command: `Run only from security_bounty_private_reports lane owner after claim and scope rules review.`
- Notes: Security testing beyond public code review requires explicit scope and approval.
- Sources:
  - `E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md`
  - `E:\profit-edge-lab\reports\google-oss-static-review-shortlist-latest.md`
  - `E:\profit-edge-lab\reports\issuehunt-security-program-scan-latest.md`
  - `E:\profit-edge-lab\reports\sherlock-contest-1259-detail-latest.md`
  - `E:\profit-edge-lab\reports\submitted-security-advisory-monitor-latest.md`
- Outputs:
  - `lane_evidence`
  - `security manager packet`

### web3_profit_edge_terms_import

- Lane: `web3_airdrops_grants_hackathons`
- Name: Web3 Terms and Target Import
- Type: `local_reports`
- Cadence: `lane_owner_on_demand`
- Gate: `no_wallet_registration_deployment_transaction_or_submission_without_user_approval`
- Refresh command: `Run only from web3 lane owner after claim; terms and deadline scouting only.`
- Notes: Wallet/account/deployment work must be a separate service request.
- Sources:
  - `E:\profit-edge-lab\reports\web3-public-code-target-shortlist-latest.md`
- Outputs:
  - `lane_evidence`
  - `web3 manager packet`

