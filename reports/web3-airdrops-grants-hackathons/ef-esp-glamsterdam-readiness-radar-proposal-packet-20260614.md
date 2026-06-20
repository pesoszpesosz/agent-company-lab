# EF ESP Glamsterdam Readiness Radar - Local Grant Proposal Packet

Lane: `web3_airdrops_grants_hackathons`
Task: `task-web3-grant-proposal-local-packet-20260614`
Manager: `lane-manager-web3_airdrops_grants_hackathons-019ec613`
Prepared: 2026-06-14
Status: local draft only; not submitted
Realized USD: 0

## Target

Ethereum Foundation Ecosystem Support Program Wishlist - Glamsterdam Grants Round.

Startup memo basis: `E:\agent-company-lab\reports\lane-startup\web3_airdrops_grants_hackathons-startup-20260614.md` ranked EF ESP Wishlist/RFPs as the cleanest next local-only proof path because proposal drafting can be done without account creation, wallet connection, public submission, or transaction work.

Primary public source captured in startup memo: https://esp.ethereum.foundation/applicants/wishlist

## Working Title

Glamsterdam Readiness Radar: open-source impact maps, monitoring checks, and operator-facing upgrade readiness packets.

## Fit Statement

The Glamsterdam grants wishlist asks for tooling, impact analysis, explorers/indexers, validator tooling, monitoring, and research around the Glamsterdam upgrade. This packet proposes a small, auditable public-good deliverable that helps application teams, infrastructure operators, and researchers understand the upgrade surface before and during rollout.

The work is intentionally scoped for a grant rather than a hackathon or quest. It avoids social actions, wallet actions, deployments, and public submissions until a separate service request approves the exact route.

## Proposed Deliverable

Build a local-first open-source Glamsterdam readiness package containing:

1. EIP and upgrade-surface map
   - Curated list of Glamsterdam-related EIPs and implementation-impact areas.
   - Plain-language impact notes for application developers, indexers, RPC providers, validators, and monitoring teams.
   - Confidence tags for finalized vs. moving upgrade details.

2. Readiness checklist generator
   - Markdown/JSON checklist templates for projects to assess code, infra, observability, and operational readiness.
   - Machine-readable schema for tracking affected components and unresolved questions.

3. Monitoring and alerting starter pack
   - Local sample checks for client/version readiness, network fork timing, RPC/indexer assumptions, and post-upgrade anomaly watchpoints.
   - Example dashboards or dashboard specs that can be implemented later without connecting production credentials.

4. Reproducible research artifact
   - Source index with exact references, snapshot dates, assumptions, and stale-data warnings.
   - Short final report describing upgrade risks, follow-up work, and where the artifact should not be relied on as canonical protocol guidance.

## Milestones

| Milestone | Duration | Output | Acceptance Evidence |
| --- | ---: | --- | --- |
| M1 - Scope and source map | 1 week | Public source index, EIP impact taxonomy, risk register | Local markdown and JSON source map committed to artifact folder |
| M2 - Checklist and schema | 1 week | Readiness checklist templates and tracking schema | Local templates with sample filled example |
| M3 - Monitoring starter pack | 2 weeks | Draft monitoring checks and dashboard specifications | Local scripts/specs that run without credentials or chain transactions |
| M4 - Review packet | 1 week | Final grant-progress report and maintenance plan | Local report with limitations, open questions, and next gates |

Total proposed duration: 5 weeks.

## Budget And Effort Assumptions

This is a draft budget for internal review only, not a quote or submitted ask.

| Item | Assumption | Draft Amount |
| --- | --- | ---: |
| Research and source mapping | 35 hours at USD 125/hour | USD 4,375 |
| Checklist/schema design | 25 hours at USD 125/hour | USD 3,125 |
| Monitoring starter pack | 55 hours at USD 125/hour | USD 6,875 |
| Report, documentation, and maintenance plan | 25 hours at USD 125/hour | USD 3,125 |
| Review buffer and upkeep | 20 hours at USD 100/hour | USD 2,000 |
| Lightweight infra/test allowance | Local/offline tooling only unless approved | USD 1,000 |
| Total draft request range | Round to grant-friendly budget | USD 20,000-25,000 |

Budget confidence: medium-low. Final amount should be adjusted after official ESP expectations, eligible cost categories, and maintenance obligations are reviewed.

## Submission Gates

No submission is allowed from this lane without an approved service request covering the exact scope. Required gates before any public action:

- `legal_kyc_tax_payment`: review ESP privacy policy, grant terms, legal entity or individual applicant implications, tax/payment obligations, and maintenance commitments.
- `public_action_execution` or `outreach_delivery`: approve the exact application/form submission route and final text.
- `account_registration`: only if the ESP application flow requires account creation or identity setup.
- `secrets_credentials_handling`: only if the application requires private files, credentials, or non-public identity documents.

Hard no without approval: form submission, proposal upload, email outreach, public repo creation for submission, public project announcement, Discord/Telegram contact, or accepting terms.

## Wallet And Payment Gates

The startup memo captured that approved EF ESP grants are paid on-chain in ETH by default. Therefore any future award route requires a separate wallet/payment gate:

- User chooses custody model and payment address; this lane must not generate wallets, store private keys, or control funds.
- Wallet address publication or form entry requires an approved `wallet_public_address_or_payment_reply` service request.
- Any KYC, tax, legal, billing, or grant-agreement step requires `legal_kyc_tax_payment` approval.
- No wallet connection, signature, transaction, deployment, donation, or gas-spending action is allowed inside this lane.

## Non-Goals

- No account registration.
- No ESP application submission.
- No wallet creation, connection, signature, payment address entry, or transaction.
- No deployment, mainnet/testnet interaction, quest completion, or social action.
- No work on `submitted_bounty_payouts`, RustChain, Charles, or GitHub payout chasing.

## Risk Register

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Glamsterdam scope changes before finalization | Medium | Use confidence tags and stale-data warnings; avoid claims of final protocol guidance |
| Existing ecosystem teams may already cover parts of this | Medium | Require duplicate/source sweep before submission gate |
| Grant budget may be too high or too low | Medium | Treat budget as draft; run legal/payment/program review before submission |
| Maintenance burden after grant | Medium | Include explicit maintenance window and handoff plan |
| Payment requires wallet/tax/legal gates | High | Stop until scoped service requests are approved |

## Local Evidence Checklist

- Fit statement: present.
- Deliverable: present.
- Budget/effort assumptions: present.
- Submission gates: present.
- Wallet/payment gates: present.
- No public submission: present.
- Realized money: USD 0.

## Recommended Next Action

Do not submit this proposal. If the lane continues, create one new local-only proof task to build the M1 source map and duplicate sweep for Glamsterdam readiness tooling. Submission, outreach, wallet, legal, and payment steps remain blocked until approved service requests exist for the exact scope.
