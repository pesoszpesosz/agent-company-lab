# Money Source Public Venue Registry

Generated UTC: 2026-06-16T20:24:00Z
JSON mirror: `E:\agent-company-lab\reports\money-source-discovery\public-venue-registry-20260616.json`
Lane: `money_source_discovery`
Schema: `agent_company.money_source_discovery.public_venue_registry.v1`

## Summary

This registry converts the latest public venue/source refresh into a 20-row routing table for the agent-company lanes. Each row records the money mechanism, payout signal, first local proof artifact, blocking action, and approval gate before any account, wallet, payment, public action, security testing, or real-money step.

Scoring:

- `expected_value_score`: 1-5 estimate of payout potential if later gates clear.
- `proofability_score`: 1-5 estimate of how quickly a local proof artifact can be produced without side effects.
- `gate_risk_score`: 1-5 approval burden; 5 is heavy account/legal/payment/wallet/security risk.
- `priority_score`: expected value plus proofability minus gate risk.

## Top Dispatch Rows

| Priority | Source | Lane | First Local Proof | Required Gate |
| ---: | --- | --- | --- | --- |
| 5 | OpenTrain AI freelancer feed | `money_source_discovery` | AI training role-feed worksheet with role, pay signal, skill, residency, assessment, contract/KYC, and volatility risk columns | `account_registration_intake` plus `legal_kyc_tax_payment_gate` |
| 5 | Algora bounties | `paid_code_bounties` | Explicit-payout issue worksheet with duplicate checks, owner route, testability, and payout terms | `github_public_action_gate` plus `legal_kyc_tax_payment_gate` |
| 5 | Ethereum Foundation Ecosystem Support Program | `web3_airdrops_grants_hackathons` | EF ESP Wishlist/RFP fit memo with methodology, timeline, deliverables, and local prototype feasibility | account, legal/payment, and public-action review |
| 5 | Devpost hackathons | `ai_ml_competitions` | Weekly prize calendar with deadline, prize, remote status, account gate, rules, and first local build artifact | account, public-action, and terms review |
| 5 | ARC Prize 2026 | `ai_ml_competitions` | ARC rules matrix and baseline feasibility memo using public resources | account, competition rules/legal, and submission gate |
| 5 | Upwork AI consultants and automation engineers | `lead_generation_and_sales` | AI workflow audit offer packet with buyer segment, deliverables, proof asset, target filters, and marketplace gate | account, legal/payment, and public-action review |

## Registry Rows

| Priority | Source ID | Venue | Candidate Lane | Secondary Lane | Mechanism | First Local Proof | Blocked Action |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 5 | `ai-training-opentrain-feed` | OpenTrain AI freelancer feed | `money_source_discovery` | `lead_generation_and_sales` | AI training, labeling, RLHF, red-teaming, and expert evaluation work | Role-feed worksheet with pay signal, skills, residency, assessment, contract/KYC, and volatility risk | Do not apply, create account, take assessments, submit identity, or accept contractor terms |
| 4 | `ai-training-outlier` | Outlier AI | `money_source_discovery` | `lead_generation_and_sales` | Remote freelance AI training and expert evaluation | Eligibility and role-risk memo | Do not apply, log in, accept terms, submit identity, or begin unpaid assessments |
| 4 | `ai-training-dataannotation` | DataAnnotation | `money_source_discovery` | `lead_generation_and_sales` | Remote AI model training work | Category-fit worksheet | Do not apply, take tests, or accept contractor/payment terms |
| 4 | `paid-studies-prolific` | Prolific participants | `money_source_discovery` | `microtasks_paid_studies_candidate` | Paid academic, industry, and AI/human-data studies | Participant eligibility and reward-rate memo | Do not sign up, submit demographics, or start studies |
| 5 | `oss-bounty-algora` | Algora bounties | `paid_code_bounties` | `digital_products_templates_plugins` | Paid GitHub issue and PR bounty workflow | Explicit-payout issue worksheet | Do not comment, claim, fork, submit PR, or provide payout details |
| 4 | `oss-funding-polar` | Polar | `digital_products_templates_plugins` | `paid_code_bounties` | OSS funding, subscriptions, digital products, and payments | Monetization gate matrix | Do not create account, connect GitHub, list products, create checkout, or accept payment terms |
| 3 | `security-bounty-intigriti` | Intigriti public programs | `security_bounty_private_reports` | `money_source_discovery` | Public bug bounty and VDP programs | Scope-only target registry | Do not test targets, create account, or submit reports |
| 3 | `security-bounty-hackerone` | HackerOne bug bounty programs | `security_bounty_private_reports` | `money_source_discovery` | Responsible-disclosure bounty programs | Scope-gate worksheet | Do not perform security testing or submit reports |
| 3 | `security-bounty-bugcrowd` | Bugcrowd | `security_bounty_private_reports` | `money_source_discovery` | Crowdsourced bounty, VDP, pentest, and security programs | Program shortlist with scope and no-testing gate | Do not test, register, submit, or use private program details |
| 2 | `security-bounty-yeswehack` | YesWeHack | `security_bounty_private_reports` | `money_source_discovery` | Bug bounty and vulnerability disclosure programs | Public-program scope worksheet | Do not register, test, or submit reports |
| 3 | `web3-bounty-immunefi` | Immunefi | `security_bounty_private_reports` | `web3_airdrops_grants_hackathons` | Web3 bug bounties and audit competitions | Read-only target shortlist | Do not connect wallet, test live targets, or submit reports |
| 4 | `web3-audit-sherlock` | Sherlock audit contests | `security_bounty_private_reports` | `web3_airdrops_grants_hackathons` | Competitive Web3 smart-contract audit contests | Contest calendar with prize pool, source, dates, judging rules, and allowed review scope | Do not join contest, submit finding, connect wallet, or test beyond public code review |
| 3 | `web3-audit-code4rena-winddown` | Code4rena | `security_bounty_private_reports` | `money_source_discovery` | Competitive Web3 audit contests and bounties | Winddown note and migration watchlist | Do not register, join audits, or submit findings |
| 5 | `web3-grants-ef-esp` | Ethereum Foundation Ecosystem Support Program | `web3_airdrops_grants_hackathons` | `digital_products_templates_plugins` | Wishlist/RFP grants and ecosystem support | Wishlist/RFP fit memo | Do not apply, submit proposal, or make deliverable commitments |
| 4 | `web3-hackathon-ethglobal` | ETHGlobal | `web3_airdrops_grants_hackathons` | `digital_products_templates_plugins` | Web3 hackathons with sponsor prize tracks | Event readiness matrix | Do not apply, register, submit project, deploy, or connect wallet |
| 4 | `web3-hackathon-dorahacks` | DoraHacks | `web3_airdrops_grants_hackathons` | `digital_products_templates_plugins` | Hackathons, grants, bounties, and ecosystem campaigns | Program gate packet | Do not register, submit BUIDL, connect wallet, claim bounty, or post publicly |
| 5 | `general-hackathon-devpost` | Devpost hackathons | `ai_ml_competitions` | `web3_airdrops_grants_hackathons` | Online and sponsor hackathons with cash/prize pools | Weekly prize calendar | Do not register, join, submit project, or accept terms |
| 5 | `ai-competition-arc-prize` | ARC Prize 2026 | `ai_ml_competitions` | `content_and_social_growth` | AI reasoning competition prize tracks | Rules matrix and baseline feasibility memo | Do not join Kaggle/ARC track, accept rules, download gated data, or submit notebooks |
| 4 | `ai-competition-aicrowd-arc-whitebox` | AIcrowd ARC White-Box Estimation Challenge 2026 | `ai_ml_competitions` | `money_source_discovery` | AI challenge prize competition | Starter-kit/rules feasibility memo and local scoring harness plan | Do not register, accept rules, upload packages, or submit |
| 5 | `freelance-marketplace-upwork-ai` | Upwork AI consultants and automation engineers | `lead_generation_and_sales` | `digital_products_templates_plugins` | AI automation, consulting, chatbot, lead qualification, and workflow services | AI workflow audit offer packet | Do not create profile, apply to jobs, send proposals, or accept contracts |

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- Security testing actions: `false`
- Real-money actions: `false`
- Service requests updated: `0`
- Service requests assigned: `0`
- Worker starts: `0`
- API calls: `false`
- External side effects: `false`

## Next Action

Promote the top priority rows into lane-specific work packets, starting with OpenTrain AI role-feed worksheet, Algora explicit-payout issue worksheet, EF ESP fit memo, Devpost prize calendar, ARC Prize feasibility memo, and Upwork AI workflow audit offer packet.
