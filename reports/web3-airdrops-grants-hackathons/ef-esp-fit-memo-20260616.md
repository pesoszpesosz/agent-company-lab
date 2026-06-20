# EF ESP Wishlist/RFP Fit Memo

Generated UTC: 2026-06-16T20:44:00Z
Task: `task-ef-esp-fit-memo-20260616`
Lane: `web3_airdrops_grants_hackathons`
Owner: `lane-manager-web3_airdrops_grants_hackathons-019ec613`
JSON mirror: `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-fit-memo-20260616.json`

## Executive Decision

Ethereum Foundation ESP is a strategic grant lane, not a quick cash lane. It is worth local prototype and fit-memo work because ESP publicly supports Wishlist/RFP-aligned projects, but all application, proposal, budget, milestone, and payment commitments must remain gated.

Decision: promote one local prototype-fit task; do not apply or contact ESP yet.

## Current Public Signals

| Signal | Evidence | Routing Meaning |
| --- | --- | --- |
| Funding is structured around Wishlist/RFP items | EF ESP home says financial support is offered through Wishlist and RFPs curated by EF teams. | Generic grant applications are weaker; fit must map to listed priorities. |
| Wishlist is idea-oriented | Wishlist applications page says it identifies ecosystem gaps and invites builders to propose ideas. | Best first proof is a fit memo plus prototype plan, not a complete application. |
| Review may include negotiation | Applicants overview describes review with EF teams and possible interview, rescoping, or budget negotiation. | Proposal scope, budget, and commitments need human review. |
| Office Hours can be non-financial support | ESP home mentions office hours for feedback and ecosystem alignment. | Potential low-risk later gate, but still an external interaction. |
| Program structure changed recently | EF blog says ESP moved to Wishlist/RFP structure across areas like cryptography, privacy, app layer, security, and community growth. | Lane should track current RFP/Wishlist items instead of old open-grant assumptions. |

## Fit Ideas

| Rank | Local Project Idea | Why It Might Fit | First Local Proof | Gate Before Submission |
| ---: | --- | --- | --- | --- |
| 1 | Agent-company grant/RFP radar for Ethereum public goods | We are already building a source registry, gate map, and worker queue; this could help builders find and safely execute ecosystem tasks. | Local demo showing source ingestion, Wishlist/RFP classifier, and no-wallet/no-submission gates. | ESP account/application, legal/payment, public proposal, budget review. |
| 2 | Open-source service-worker approval templates for Web3 grants/hackathons | EF ecosystem builders often need safer contribution and grant workflows. | Publishable local template set for approval scopes, milestone checklists, and evidence bundles. | Public repo/listing/proposal gate. |
| 3 | Local-only smart-contract audit contest prep harness | ESP/security ecosystem might value safer audit education/tooling. | Read-only code-review checklist and synthetic vulnerable contract examples. | Security/legal/public release review. |
| 4 | Ethereum hackathon/grant calendar with eligibility gates | Matches the lab's money-source discovery function and could benefit builders. | Calendar schema plus sample dashboard from public sources. | Public deployment/proposal gate. |

## Smallest Prototype To Build First

Build `ef-esp-wishlist-rfp-classifier-prototype-20260616.md/json`:

- Input: public Wishlist/RFP item title, description, category, deadline, expected artifact, and application route.
- Output: fit score, first local prototype, budget-risk flag, public-action gate, payment/legal gate, and kill criterion.
- No account, proposal, submission, wallet, payment, or contact.

## Score

| Metric | Score | Notes |
| --- | ---: | --- |
| Strategic upside | 5 | Could turn agent-company infra into grant-aligned public-good tooling. |
| Cash probability | 2 | Grants are selective and slow; not immediate revenue. |
| Time to first local proof | 4 | Fit memo and classifier prototype are local. |
| Gate burden | 5 | Proposal, budget, payment, legal, public commitments. |
| Reuse value | 5 | Same classifier helps other grant/hackathon lanes. |

## Kill Criterion

Do not request ESP application approval unless a local classifier prototype maps at least five current Wishlist/RFP items into concrete local prototype candidates and rejects at least two as poor fit with clear reasons.

## Required Gates Before External Action

- `account_registration_intake`
- `legal_kyc_tax_payment_gate`
- `public_action_execution`
- Budget/milestone commitment review

## Next Action

Create a local `ef-esp-wishlist-rfp-classifier-prototype-20260616.md/json` using public Wishlist/RFP fields and no external action.

## Source URLs

- https://esp.ethereum.foundation/
- https://esp.ethereum.foundation/applicants
- https://esp.ethereum.foundation/applicants/wishlist
- https://blog.ethereum.org/2025/11/03/new-esp-grants

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- Security testing actions: `false`
- Real-money actions: `false`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
