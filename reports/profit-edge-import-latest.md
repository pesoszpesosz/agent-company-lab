# Profit Edge Import Bridge

Generated UTC: 2026-06-18T22:18:49Z
Source root: `E:\profit-edge-lab`
Task: ``

## Boundary

- This is a read-only import into the agent-company control plane.
- `submitted_bounty_payouts` stays owned by the parallel payout-monitoring worker.
- This thread uses imported rows only for infrastructure, lane routing, launch packets, and future task assignment.

## Counts By Lane

| Lane | Imported Rows |
| --- | ---: |
| `paid_code_bounties` | 15 |
| `platform_engineering` | 2 |
| `prediction_market_research` | 9 |
| `security_bounty_private_reports` | 11 |
| `submitted_bounty_payouts` | 14 |
| `web3_airdrops_grants_hackathons` | 1 |

## Imported Evidence

| Lane | Status | Evidence | Source | Next Action |
| --- | --- | --- | --- | --- |
| `platform_engineering` | submission_ready | `pe-report-profit-edge-daily-action-queue-e7654b96ab3f` - Profit Edge Daily Action Queue | E:\profit-edge-lab\reports\daily-action-queue-latest.md | Cashflow: promoted ledger action "rustchain 293 14015 payout monitor"; next action is Monitor RustChain wallet issue #14058 for official claim/control instructions for the already-visible 70 RTC balance; no wallet/key/si |
| `submitted_bounty_payouts` | imported | `pe-report-submitted-bounty-monitor-34dd40c9671d` - Submitted Bounty Monitor | E:\profit-edge-lab\reports\submitted-bounty-monitor-latest.md | next: Monitor only. Direct payout to us requires bounty owner selection of our solver/PR work or an explicit request for our payout details. Existing next action: Monitor upstream PR #7014 and microbounty #905 for review |
| `submitted_bounty_payouts` | imported | `pe-report-charles-submission-monitor-6a23a0593fa4` - Charles Submission Monitor | E:\profit-edge-lab\reports\charles-submission-monitor-latest.md | next: Monitor Charles verification, award, payout request, or maintainer question; do not post a duplicate nudge. |
| `security_bounty_private_reports` | rejected | `pe-report-submitted-security-advisory-monitor-391de16b380f` - Submitted Security Advisory Monitor | E:\profit-edge-lab\reports\submitted-security-advisory-monitor-latest.md | next: Monitor for maintainer acceptance, questions, severity decision, or bounty/payout instructions. |
| `security_bounty_private_reports` | imported | `pe-report-security-bounty-source-scan-032255bc416b` - Security Bounty Source Scan | E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md | next: Shortlist one Google-owned flagship OSS repo with local repro potential; do static source review only until a concrete vulnerability hypothesis exists. |
| `security_bounty_private_reports` | imported | `pe-report-google-oss-static-review-shortlist-dbeac8a17965` - Google OSS Static Review Shortlist | E:\profit-edge-lab\reports\google-oss-static-review-shortlist-latest.md | next: Clone read-only and review supply-chain, parser, auth, credential, build, and release-boundary logic; no live testing. |
| `security_bounty_private_reports` | imported | `pe-report-issuehunt-security-program-scan-eaea569f83ac` - IssueHunt Security Program Scan | E:\profit-edge-lab\reports\issuehunt-security-program-scan-latest.md | next: Read the full program page and all scope text; draft non-invasive hypotheses only, then ask user before account setup or testing. |
| `security_bounty_private_reports` | imported | `pe-report-sherlock-contest-detail-c507970e8545` - Sherlock Contest Detail | E:\profit-edge-lab\reports\sherlock-contest-1259-detail-latest.md |  |
| `prediction_market_research` | imported | `pe-report-prediction-market-scan-feb389566f62` - Prediction Market Scan | E:\profit-edge-lab\reports\prediction-market-scan-latest.md |  |
| `prediction_market_research` | watch_only | `pe-report-cross-venue-next-team-scan-35be3fc7745a` - Cross-Venue Next-Team Scan | E:\profit-edge-lab\reports\cross-venue-next-team-latest.md | next: Watch only; no clean cross-venue trade from current public data. |
| `prediction_market_research` | watch_only | `pe-report-polymarket-tennis-edge-packet-68be67f48831` - Polymarket Tennis Edge Packet | E:\profit-edge-lab\reports\polymarket-tennis-edge-packet-latest.md |  |
| `prediction_market_research` | watch_only | `pe-report-kalshi-btc-range-edge-e654ec4ccb73` - Kalshi BTC Range Edge | E:\profit-edge-lab\reports\kalshi-btc-range-edge-latest.md |  |
| `prediction_market_research` | imported | `pe-report-kalshi-btc-settlement-lag-daa29bc18301` - Kalshi BTC Settlement Lag | E:\profit-edge-lab\reports\kalshi-btc-settlement-lag-latest.md |  |
| `prediction_market_research` | imported | `pe-report-kalshi-crypto-settlement-lag-7d155d530ac1` - Kalshi Crypto Settlement Lag | E:\profit-edge-lab\reports\kalshi-crypto-settlement-lag-latest.md |  |
| `prediction_market_research` | watch_only | `pe-report-kalshi-generic-settlement-lag-898b589d490d` - Kalshi Generic Settlement Lag | E:\profit-edge-lab\reports\kalshi-settlement-lag-latest.md |  |
| `paid_code_bounties` | parked_or_gated | `pe-report-paid-code-bounty-scan-bab9eff85a53` - Paid Code Bounty Scan | E:\profit-edge-lab\reports\bounty-scan-latest.md | next: Check whether the issue is unclaimed and whether no upstream PR already exists; if clear, clone repo and prepare minimal PR. |
| `paid_code_bounties` | rejected | `pe-report-fresh-github-bounty-pulse-3bcd8b72373f` - Fresh GitHub Bounty Pulse | E:\profit-edge-lab\reports\github-fresh-bounty-pulse-latest.md |  |
| `paid_code_bounties` | parked_or_gated | `pe-report-algora-bounty-scan-de35b904e742` - Algora Bounty Scan | E:\profit-edge-lab\reports\algora-bounty-scan-latest.md | next: Check if maintainer still honors the bounty before spending time. |
| `paid_code_bounties` | imported | `pe-report-opire-bounty-scan-d287f55ec949` - Opire Bounty Scan | E:\profit-edge-lab\reports\opire-bounty-scan-latest.md | next: Check whether the issue and reward are still honored before spending time. |
| `paid_code_bounties` | rejected | `pe-report-bountyhub-bounty-scan-9f4b55320f4b` - BountyHub Bounty Scan | E:\profit-edge-lab\reports\bountyhub-bounty-scan-latest.md | next: Park unless existing PRs are rejected and bounty creator asks for a fresh implementation. |
| `paid_code_bounties` | rejected | `pe-report-boss-bounty-scan-a7d282ac1bcd` - BOSS Bounty Scan | E:\profit-edge-lab\reports\boss-bounty-scan-latest.md | next: Do not duplicate unless existing PR/comment work is rejected and maintainer asks for alternatives. |
| `paid_code_bounties` | rejected | `pe-report-gibwork-bounty-scan-a957d84d939b` - Gibwork Bounty Scan | E:\profit-edge-lab\reports\gibwork-bounty-scan-latest.md | next: Too many submissions already; park unless creator asks for more or existing submissions are rejected. |
| `paid_code_bounties` | rejected | `pe-report-gitpay-task-scan-31d8ce391b0f` - Gitpay Task Scan | E:\profit-edge-lab\reports\gitpay-task-scan-latest.md | next: Do not implement until Gitpay assignment/assignee state is clear. |
| `paid_code_bounties` | parked_or_gated | `pe-report-unitone-skill-bounty-scan-c0c428cbab57` - UnitOne Skill Bounty Scan | E:\profit-edge-lab\reports\unitone-skill-bounty-scan-latest.md | next: Do not claim, comment, fork, build, or submit unless a maintainer explicitly asks for alternate implementations and payout attribution is clean for @pesoszpesosz. |
| `paid_code_bounties` | imported | `pe-report-projectdiscovery-bounty-scan-76f48603a8ed` - ProjectDiscovery Bounty Scan | E:\profit-edge-lab\reports\projectdiscovery-bounty-scan-latest.md |  |
| `web3_airdrops_grants_hackathons` | submission_ready | `pe-report-web3-public-code-target-shortlist-a43435a36e55` - Web3 Public Code Target Shortlist | E:\profit-edge-lab\reports\web3-public-code-target-shortlist-latest.md | next: Preserve the v3.0.2 packet, but treat expected value as downgraded by public Consensys 7.27 collision. Submit only once as an explicitly disclosed distinct-impact extension if the Immunefi account path is clean; ot |
| `platform_engineering` | imported_jsonl | `pe-report-profit-edge-manual-overrides-f46da04dfc8d` - Profit Edge Manual Overrides | E:\profit-edge-lab\opportunities\manual-overrides.jsonl | Do not attempt #4225 unless maintainers reopen the bounty for new implementations or request alternatives. |
| `paid_code_bounties` | profit_edge | `pe-ledger-profit-edge-ledger-row-af2308fb0f2e` - Profit Edge ledger row | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl |  |
| `security_bounty_private_reports` | security_bounty | `pe-ledger-profit-edge-ledger-row-72d7a7f187c6` - Profit Edge ledger row | https://issuehunt.io/programs/75563b98-3a9c-4ca3-956d-07b30d5d3962 | Keep ABEMA parked behind manual rules translation and scope review; promote only public-doc/static matrix work unless rules explicitly permit low-impact owned-account testing. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-ff82cf2d39e1` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `paid_code_bounties` | paid_code_bounty | `pe-ledger-profit-edge-ledger-row-4a9bf078639a` - Profit Edge ledger row | https://github.com/Veritas-Vaults-Network/soroban-guard-contracts/issues/421 | Monitor issue #421 for GrantFox/maintainer assignment; if assigned, rerun tests in complete Rust environment or CI and open PR. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-74113bf583bb` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `paid_code_bounties` | paid_code_bounty | `pe-ledger-profit-edge-ledger-row-1361ce242355` - Profit Edge ledger row | https://github.com/Veritas-Vaults-Network/soroban-guard-contracts/issues/421 | Monitor #421 for GrantFox/maintainer assignment. If assigned, rerun tests in CI or a complete Rust toolchain environment, then open PR. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-65d4cc1c310d` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `submitted_bounty_payouts` | paid_code_bounty | `pe-ledger-profit-edge-ledger-row-9402960becb2` - Profit Edge ledger row | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl |  |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-678d440e2fd2` - Profit Edge ledger row | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl |  |
| `security_bounty_private_reports` | security_bounty | `pe-ledger-profit-edge-ledger-row-ebc307304f97` - Profit Edge ledger row | https://issuehunt.io/programs/bitFlyer | Keep as monitored high-reward rules lane; do not test unless full program rules, account authorization, and user-controlled prerequisites are clean. |
| `prediction_market_research` | prediction_market | `pe-ledger-profit-edge-ledger-row-7def1a16b4c7` - Profit Edge ledger row | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Run scheduled close-window capture near the next allowed KXBTC/KXETH/KXXRP/KXDOGE close, especially around 2026-06-19T21:00:00Z for KXBTC if still current. Continue paper-only until accepting-orders, non-empty book, know |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-c82f9e0ac181` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `security_bounty_private_reports` | security_bounty | `pe-ledger-profit-edge-ledger-row-e4a9a92a36bd` - Profit Edge ledger row | https://issuehunt.io/programs/382ed642-bbb5-46fa-ab76-7f1b5633ac7b | Keep as a gated IssueHunt web-app lane; advance only with explicit user approval for IssueHunt/platform login and test-account use, with a narrow low-impact test plan. |
| `security_bounty_private_reports` | security_bounty | `pe-ledger-profit-edge-ledger-row-271312708dc3` - Profit Edge ledger row | https://issuehunt.io/programs/db5804cf-1391-483c-84ac-6d398dbce725 | Monitor only; revisit only if full program rules publish explicit scope, exclusions, report requirements, and allowed low-impact test methods. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-3e37c089341b` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-41f2601dd732` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `security_bounty_private_reports` | security_bounty | `pe-ledger-profit-edge-ledger-row-081c1ed5072c` - Profit Edge ledger row | https://issuehunt.io/programs/43f8fcd7-430d-47e1-bc1b-4ed59352797d | Monitor only; revisit only if full program rules publish explicit testing rules, exclusions, rate limits, account requirements, and allowed low-impact methods. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-3b3bb0fd2b78` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `paid_code_bounties` | paid_code_bounty | `pe-ledger-profit-edge-ledger-row-5210ea7255bc` - Profit Edge ledger row | https://github.com/daytonaio/devcontainer-generator/issues/25 | Keep current monitor lanes active and continue fresh paid-code scans; do not spend implementation time on these Algora rows unless source conditions change. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-41f2601dd732` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `paid_code_bounties` | paid_code_bounty | `pe-ledger-profit-edge-ledger-row-6f69b33b7ec3` - Profit Edge ledger row | https://github.com/rustdesk/rustdesk/issues/3762 | Monitor rustdesk/rustdesk#3762 and PR #15232; revisit only if PR #15232 is closed, rejected, or stale and the maintainer asks for an alternative implementation or narrow testing help. |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-41f2601dd732` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `security_bounty_private_reports` | security_bounty | `pe-ledger-profit-edge-ledger-row-aebdbee6579b` - Profit Edge ledger row | https://issuehunt.io/programs/a331fa90-426e-40e4-949a-6ba745b6d800 | Monitor only; revisit only if full public rules define scope, exclusions, rate limits, account requirements, test-account rules, and allowed low-impact methods without KYC/payment onboarding, deposits, withdrawals, trade |
| `submitted_bounty_payouts` | profit_edge | `pe-ledger-profit-edge-ledger-row-41f2601dd732` - Profit Edge ledger row | https://github.com/Scottcjn/rustchain-bounties/issues/14058 |  |
| `prediction_market_research` | prediction_market | `pe-ledger-profit-edge-ledger-row-5e49f83b24c0` - Profit Edge ledger row | E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl | Launch the close-window scheduler before targetStart for the next KXBTC/KXETH/KXXRP/KXDOGE close and keep it alive through pre-close plus the roughly 154s median settlement-delay window. Continue paper/read-only only unt |
