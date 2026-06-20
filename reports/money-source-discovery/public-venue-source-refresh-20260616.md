# Money Source Discovery Public Venue Source Refresh

Generated UTC: 2026-06-16T20:12:00Z
Lane: `money_source_discovery`
Scope: read-only public source scan; no signup, login, application, browser account action, payment setup, wallet action, submission, public post, security testing, or real-money action.

## Executive Takeaway

The money-source discovery lane should become the company's permanent radar desk. Its job is not to execute every opportunity; it should find, classify, score, and route sources into the right execution lane with a first proof task and a gate.

The best current source classes for agent routing are:

1. AI training/evaluation contractor feeds.
2. Paid research/study platforms.
3. Open-source developer bounty platforms.
4. Public security bounty programs.
5. Web3 bug bounties, hackathons, grants, and public-goods funding.
6. General hackathon/prize directories.
7. Product/funding platforms that can monetize local software/assets.
8. Existing local `E:\profit-edge-lab` scanners and ledgers.

The highest-value first proof is a machine-readable venue registry. It should record payout route, account gate, proof artifact, likely lane owner, and next approval needed before any worker is allowed to act.

## Venue Registry Seeds

| Rank | Source Class | Current Example Sources | Why It Matters | First Local Proof | Route To Lane | Gate |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | AI training and evaluation work | OpenTrain AI, Outlier, DataAnnotation, Mercor, Prolific | Fastest path to cash-like online work if eligibility clears; useful for coding/math/reasoning/domain expertise. | Create a role-feed worksheet: role, pay signal, skill needed, residency, contract/KYC gate, test requirements, volatility risk. | `money_source_discovery` then `lead_generation_and_sales` or new `ai_training_contracts` lane if volume justifies it. | Account/application, contractor agreement, tax/KYC/payment, tests, possible unpaid assessment. |
| 2 | Paid studies and human-data tasks | Prolific participant studies, AI/human preference studies | Lower upside but simple proof path; can validate account-gate flow and payout rules. | Public participant eligibility and minimum reward-rate memo; no account creation. | `money_source_discovery` or future `microtasks_paid_studies`. | Account, demographics, payment, study ethics, location availability. |
| 3 | OSS developer bounties | Algora, Polar issue funding/rewards, Opire-style bounties, direct GitHub labels | Strong fit for coding agents; can produce local duplicate-check worksheets before public PR/comment. | Weekly explicit-payout issue registry with duplicate and owner checks. | `paid_code_bounties`. | GitHub identity, PR/comment, license, bounty terms, payment route. |
| 4 | Public security bounty programs | Intigriti, HackerOne, Bugcrowd, YesWeHack, HackenProof | High upside, but only safe if scope and allowed testing are explicit. | Scope-only target registry: program, payout range, asset class, allowed testing, private route. | `security_bounty_private_reports`. | Program terms, account, scope, no unauthorized testing, private report route. |
| 5 | Web3 bug bounties/audit contests | Immunefi, HackenProof, Sherlock/Code4rena-style contests | High payout potential and public code review fit; also high scope and wallet/payment complexity. | Read-only bounty/contest shortlist with scope, payout, repo, report route, wallet/payment requirements. | `security_bounty_private_reports` and `web3_airdrops_grants_hackathons`. | Account, wallet/payment, report rules, disclosure, no live exploit testing. |
| 6 | Web3 grants and hackathons | ETHGlobal, DoraHacks, Gitcoin funding directory, ecosystem grant pages | Good for prototype agents and local product assets; deadlines create action pressure. | Hackathon/grant calendar: deadline, prize/grant, required build, team/account/wallet gate. | `web3_airdrops_grants_hackathons` and `digital_products_templates_plugins`. | Registration, legal terms, wallet, public submission, demo/deployment. |
| 7 | General hackathon/prize directories | Devpost current/upcoming hackathons, ML Contests, Kaggle/AI challenge registries | Finds AI, SaaS, civic-tech, and sponsor prizes outside crypto. | Prize calendar with deadline, beginner/remote status, account gate, first local build artifact. | `ai_ml_competitions`, `digital_products_templates_plugins`, `web3_airdrops_grants_hackathons`. | Account, rules, submissions, eligibility, IP/licensing. |
| 8 | Product monetization platforms | Polar, Gumroad/Lemon Squeezy-style storefronts, GitHub Sponsors, marketplaces | Lets local artifacts become paid products or funded OSS, but requires billing/listing gates. | Product-platform gate matrix: fees, payout, tax/KYC, listing rules, product types. | `digital_products_templates_plugins`. | Payment processor, tax/KYC, listing/public action, refund/support obligations. |
| 9 | Existing local scanners | `E:\profit-edge-lab` daily queue, bounty scans, prediction-market scans, ledger rows | Already contains machine-readable leads and prior kills/parks; should prevent rediscovery of weak rows. | Import/refresh delta worksheet and killed-lane reasons. | Source-specific lane managers. | Respect ownership notes and external worker boundaries. |

## Agent Assignment

| Agent Type | Responsibility | Output |
| --- | --- | --- |
| `source_mapper` | Keep a rolling source-class registry and identify which lanes should own each opportunity. | `public-venue-registry-YYYYMMDD.json/md` |
| `venue_rules_reader` | Read public rules, terms, account, payout, and eligibility pages without signing up. | `venue-gate-packet-<venue>.md` |
| `expected_value_ranker` | Score candidates by payout, time to first proof, approval burden, risk, competition, and repeatability. | `venue-scoreboard-YYYYMMDD.md` |
| `lane_launcher` | Convert top candidates into lane-specific first proof packets. | `work-packet-<lane>-<venue>.md` |

## Machine-Readable Registry Schema

Each venue row should include:

- `source_id`
- `source_class`
- `venue_name`
- `venue_url`
- `candidate_lane`
- `money_mechanism`
- `payout_signal`
- `deadline_or_cadence`
- `account_required`
- `payment_or_kyc_required`
- `wallet_required`
- `public_action_required`
- `security_scope_required`
- `first_local_proof`
- `blocked_action`
- `approval_needed`
- `confidence`
- `kill_reason_if_rejected`

## First Work Packet

Task ID proposal: `task-money-source-public-venue-registry-20260616`

Worker: `source_mapper`

Allowed scope:

- Read public venue pages and local existing lab reports.
- Record source class, payout route, account/payment/wallet/security/public-action gates, and first proof artifact.
- Write local markdown/json registry only.

Forbidden scope:

- No account creation or application.
- No login/session use.
- No wallet connection, address submission, transaction, or signature.
- No KYC/tax/payment setup.
- No public posting, PR comment, proposal, form submission, or bounty claim.
- No security testing.
- No real-money trade or deposit.

Required proof artifact:

- `reports/money-source-discovery/public-venue-registry-YYYYMMDD.md`
- `reports/money-source-discovery/public-venue-registry-YYYYMMDD.json`

## Source URLs

- https://www.opentrain.ai/become-freelancer/
- https://outlier.ai/
- https://www.dataannotation.tech/
- https://www.prolific.com/participants
- https://devpost.com/hackathons
- https://ethglobal.com/
- https://dorahacks.io/
- https://immunefi.com/bug-bounty/
- https://www.intigriti.com/researchers/bug-bounty-programs
- https://gitcoin.co/
- https://algora.io/polarsource/bounties?status=completed
- https://polar.sh/

## Current Observations

- OpenTrain positions itself as a feed aggregating AI training and labeling roles from 20+ platforms, including Mercor, Handshake, Micro1, DataAnnotation, and Outlier.
- Outlier advertises remote AI trainer work and large-scale expert payments, but account, residency, assessment, and contractor gates remain mandatory.
- DataAnnotation advertises remote AI training work with coding/STEM/law/medicine/writing categories and hourly pay signals, but application and assessment gates apply.
- Prolific is a legitimate paid-study route and publishes participant-facing earning language, but its researcher docs require studies to pay through Prolific and meet minimum reward-rate rules.
- Devpost currently lists new/upcoming hackathons including AI/machine-learning prize events, making it a useful general prize calendar.
- ETHGlobal currently lists upcoming 2026 Ethereum hackathon events, useful for Web3 prototype opportunities.
- Immunefi's bug bounty page is updated daily and includes Web3 bounties/audit competitions, but all action must remain scope-bound and private-route safe.
- Intigriti exposes public programs, program types, payout ranges, and "T&C Required" markers that make it good for scope/gate scouting before any security work.
- Gitcoin has shifted into a funding-mechanism/app/campaign directory for Ethereum/AI public-goods funding; it is useful as a grants/funding radar rather than a simple bounty board.
- Algora and Polar remain useful OSS funding/bounty/payment references, but each specific issue or product path needs payout and contributor-route verification.

## Next Action

Create the formal `public-venue-registry` JSON/Markdown pair and score at least 20 rows across AI training, paid studies, OSS bounties, security bounties, Web3 grants/hackathons, general hackathons, and product monetization. Route each row to a lane and stop before any account, payment, wallet, public, or security side effect.
