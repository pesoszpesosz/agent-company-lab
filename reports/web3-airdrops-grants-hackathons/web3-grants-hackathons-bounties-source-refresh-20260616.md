# Web3 Grants, Hackathons, Bounties, and Airdrop-Adjacent Source Refresh

Generated UTC: 2026-06-16T20:20:00Z
Lane: `web3_airdrops_grants_hackathons`
Scope: read-only public source scan; no registration, wallet connection, signature, transaction, deployment, proposal submission, bounty claim, public post, security testing, or real-money action.

## Executive Takeaway

The Web3 lane has real money paths, but almost every valuable route crosses at least one high-risk service gate: account registration, wallet custody, public submission, sponsor terms, security scope, or payment/KYC. The lane should therefore operate as a proof-factory first:

1. Scout current grants/hackathons/bounties.
2. Translate each opportunity into a local build/proposal/report packet.
3. Score by prize/grant size, deadline, local prototype feasibility, wallet/account burden, legal terms, and public-action risk.
4. Escalate only the best packet to the account/wallet/public-action/security service workers.

The best current first proof is not an airdrop claim. It is a Web3 opportunity calendar plus one local feasibility packet for a grant or hackathon that can be drafted without registration.

## Current Opportunity Classes

| Rank | Source Class | Current Source Signals | Why It Matters | First Local Proof | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | Ethereum Foundation ESP Wishlist/RFP grants | EF ESP now presents financial support through Wishlist and RFP pathways; applicants browse items, then apply with methodology, timeline, and deliverables. | High-signal grants for public goods; strong fit for proposal-writing agents and local architecture packets. | Choose one Wishlist/RFP item and draft a local fit memo plus work plan; no application. | Application, legal terms, identity/payment info, deliverable commitment. |
| 2 | ETHGlobal hackathons | ETHGlobal lists 2026 hackathon events; Lisbon 2026 is listed for July 24-26, 2026. ETHGlobal Cannes 2026 had $150k available in prizes and sponsor tracks. | Hackathons create time-boxed prototype opportunities with clear prize tracks and sponsor APIs. | Build a hackathon-readiness matrix: event, deadline, sponsor tracks, required deployment, repo/demo needs. | Attendance/application, submission form, team/account, public demo, sponsor terms. |
| 3 | DoraHacks hackathons/grants/bounties | DoraHacks positions itself around hackathons, grants, and bounties; current pages include Grant Factory with a $100k prize pool and sponsor bounty examples. | Broad Web3 incentive platform; useful for grants, hackathons, focused bounties, and ecosystem campaigns. | Create a DoraHacks source row set: program, prize, track, submission artifact, wallet/account gate. | Account, BUIDL submission, wallet/payment, public profile, terms. |
| 4 | Gitcoin funding landscape | Gitcoin now curates funding campaigns, apps, mechanisms, case studies, and Ethereum/AI public-goods funding resources. | Better as a funding-intelligence map than a simple bounty board; useful for finding grant mechanisms and ecosystem funders. | Map Gitcoin apps/campaigns relevant to AI agents, public goods, tooling, and local prototypes. | Program-specific terms, application, wallet/payment, public-good eligibility. |
| 5 | Web3 bug bounties and audit contests | Immunefi's bug bounty surface is updated daily and includes Web3 bounties/audit competitions; HackenProof also lists crypto/Web3 programs. | High upside for code-review agents, but only safe through strict scope and private-report gates. | Read-only target shortlist: repo/source, asset scope, payout, allowed testing, report route. | No testing until scope approval; account, private report, wallet/payment. |
| 6 | General hackathon directories with Web3 tracks | Devpost and similar directories list online/current hackathons, including AI and blockchain tracks. | Captures non-Ethereum and sponsor-led prize opportunities that ETHGlobal/DoraHacks miss. | Weekly Web3/general hackathon delta scan. | Account, terms, submission, IP/licensing, public demo. |
| 7 | Airdrop/task campaigns | Potentially high-variance source class, but commonly requires wallet connection, social actions, signatures, bridge/transaction activity, or Sybil-sensitive behavior. | Usually poor first autonomous target; useful only as rules/gate research. | Rules-only risk memo with required actions and disqualifying gates. | Wallet/private key, transaction, social action, KYC, Sybil policy, real funds. |

## Candidate Watchlist

| Candidate | Date/Status As Of 2026-06-16 | Prize/Support Signal | Best Agent | First Proof Packet |
| --- | --- | --- | --- | --- |
| EF ESP Wishlist/RFP | Ongoing standard grant route after 2025 program redesign. | Financial and non-financial support through curated Wishlist/RFP needs. | `program_scout` + `proposal_packet_writer` | `ef-esp-wishlist-fit-memo-YYYYMMDD.md` |
| ETHGlobal Lisbon 2026 | Upcoming July 24-26, 2026. | ETHGlobal 2026 event with hackathon application route. | `hackathon_scout` | `ethglobal-lisbon-readiness-matrix-YYYYMMDD.md` |
| ETHGlobal future city events | Tokyo 2026 appears in event directories for Sept. 25-27, 2026; verify official ETHGlobal page before acting. | Multi-day Ethereum hackathon pipeline. | `hackathon_scout` | `ethglobal-event-calendar-YYYYMMDD.md` |
| DoraHacks Grant Factory / Taiko | Current DoraHacks page reports a $100k prize pool. | Grant/hackathon route with track-based submissions. | `program_scout` | `dorahacks-grant-factory-gate-packet-YYYYMMDD.md` |
| DoraHacks bounty examples | DoraHacks pages show bounty-style sponsor rewards. | Focused work items may fit local prototype agents. | `bounty_scout` | `dorahacks-bounty-scope-sheet-YYYYMMDD.md` |
| Immunefi bug bounties/audit competitions | Page says metrics are updated daily; as of the observed page, last updated Jun. 16, 2026 at 16:00 UTC. | High-value Web3 security route. | `scope_reader` | `immunefi-readonly-target-shortlist-YYYYMMDD.md` |
| Gitcoin campaigns/apps | Gitcoin presents 2026 funding apps, campaigns, and Ethereum/AI public-goods references. | Funding-mechanism intelligence and grant discovery. | `funding_mapper` | `gitcoin-funding-map-YYYYMMDD.md` |
| Devpost Web3/AI hackathons | Directory lists current/upcoming online hackathons and prize pools. | Broad prize feed outside crypto-native venues. | `hackathon_scout` | `devpost-web3-ai-delta-YYYYMMDD.md` |

## Agent Assignment

| Agent Type | Responsibility | Output |
| --- | --- | --- |
| `program_scout` | Find grants, hackathons, ecosystem programs, bounty campaigns, and public-goods funding sources. | `web3-opportunity-calendar-YYYYMMDD.md/json` |
| `terms_reader` | Read eligibility, deadlines, required deliverables, wallet/payment needs, public submission rules, and IP/licensing terms. | `web3-gate-packet-<program>.md` |
| `prototype_planner` | Convert one opportunity into a local build plan without registering or deploying. | `web3-local-prototype-plan-<program>.md` |
| `submission_packet_writer` | Draft proposal/demo copy only after a gate packet exists. | `web3-submission-draft-<program>.md` |
| `wallet_ops_worker` | Prepare wallet/network requirements only after explicit service request approval. | `wallet-requirements-packet.md` |
| `public_action_worker` | Submit/apply/post only after exact user-approved destination and text. | Public receipt/proof artifact |

## First Work Packet

Task ID proposal: `task-web3-opportunity-calendar-20260616`

Worker: `program_scout`

Allowed scope:

- Read public event, grant, bounty, and funding pages.
- Record deadlines, prize/grant signal, sponsor tracks, account/wallet/public-action/security gates, and first local prototype/proposal artifact.
- Produce local markdown/json only.

Forbidden scope:

- No account creation or login.
- No wallet connection, address submission, signature, private key, seed phrase, transaction, bridge, swap, claim, deployment, or faucet use.
- No proposal, BUIDL, bounty, report, PR, issue, public post, or form submission.
- No security testing beyond read-only public rules/source review.
- No real-money action.

Required proof artifact:

- `reports/web3-airdrops-grants-hackathons/web3-opportunity-calendar-YYYYMMDD.md`
- `reports/web3-airdrops-grants-hackathons/web3-opportunity-calendar-YYYYMMDD.json`

Minimum columns:

- program
- venue
- source URL
- opportunity type
- prize/grant signal
- deadline/cadence
- required build/proposal
- account gate
- wallet/payment gate
- public-submission gate
- security-scope gate
- first local proof
- candidate lane
- approval needed

## Source URLs

- https://esp.ethereum.foundation/
- https://esp.ethereum.foundation/applicants
- https://blog.ethereum.org/2025/11/03/new-esp-grants
- https://ethglobal.com/
- https://ethglobal.com/events/cannes2026
- https://ethglobal.com/events/newdelhi/info/details
- https://dorahacks.io/
- https://dorahacks.io/hackathon
- https://dorahacks.io/hackathon/grant-factory/detail
- https://dorahacks.io/hackathon/grant-factory/buidl
- https://immunefi.com/bug-bounty/
- https://gitcoin.co/
- https://gitcoin.co/apps/ethereum-foundation-esp
- https://devpost.com/hackathons

## Next Action

Create the formal `web3-opportunity-calendar` markdown/json pair. Start with EF ESP Wishlist/RFP and ETHGlobal Lisbon 2026 because they can produce useful local fit/prototype packets without wallet or transaction work. Treat airdrops as rules-only research until a human explicitly approves wallet/account/public-action scope.
