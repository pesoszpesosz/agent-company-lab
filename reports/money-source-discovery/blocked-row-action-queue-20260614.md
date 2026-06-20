# Blocked Row Action Queue - 2026-06-14

Lane: `money_source_discovery`
Schema: `blocked_row_action_queue.v1`
Source queue: `E:\agent-company-lab\reports\money-source-discovery\money-source-proof-queue-20260614.json`
Routing decision: `E:\agent-company-lab\reports\money-source-discovery\msd-001-local-routing-decision-20260614.md`

## Summary

- Source queue candidates: 16.
- Already routed as local-only control row: `MSD-001`.
- Blocked rows in this queue: 15.
- Rows ready for external execution: 0.
- Primary service request: `req-wave4-money-source-discovery-browser-readonly-20260614`.
- Primary service request status: `needs_review`.
- Realized USD: 0.

## Boundary

This queue does not approve:

- browser actions;
- current-source verification;
- API calls;
- account actions;
- wallet actions;
- legal, KYC, tax, billing, payment, or seller setup;
- public comments, listings, applications, submissions, outreach, or claims;
- human-only paid work;
- trades, deposits, withdrawals, or money movement;
- `submitted_bounty_payouts` work.

## Queue

| Candidate | Lane | First Required Gate | Safe Local Next Action |
| --- | --- | --- | --- |
| `MSD-002` | `paid_code_bounties` plus `security_bounty_private_reports` | Approve `req-wave4-money-source-discovery-browser-readonly-20260614` for exact public-read scope. | Prepare a read-only capture template for GitHub bounty-source evidence fields without opening GitHub. |
| `MSD-003` | `ai_ml_competitions` | Approve browser read-only for public-read scope. | Draft a prize-competition evaluation rubric using only existing local Wave-4 fields. |
| `MSD-004` | `ai_ml_competitions` | Approve browser read-only for public-read scope. | Reuse the AI/ML competition rubric and add fields for social-impact/prize probability. |
| `MSD-005` | `ai_ml_competitions` | Approve browser read-only for exact public-read scope. | Create aggregator capture fields: prize, deadline, host, rules URL, account need, and duplicate source. |
| `MSD-006` | `ai_ml_competitions` | Approve browser read-only for public-read scope. | Draft hackathon triage fields for deadline, team size, allowed AI APIs, judging criteria, and expected build hours. |
| `MSD-007` | `web3_airdrops_grants_hackathons` plus `ai_ml_competitions` | Approve browser read-only for public-read scope. | Prepare a web3 hackathon gate checklist that separates read-only research from wallet/deploy/public-submission actions. |
| `MSD-008` | `digital_products_templates_plugins` | Approve browser read-only for public-read scope. | Map the existing Agent Skill Starter Kit proof packet to a Gumroad-style listing-readiness checklist without opening Gumroad. |
| `MSD-009` | `digital_products_templates_plugins` | Approve browser read-only for public-read scope. | Create a platform-neutral seller-readiness checklist from local product proof artifacts. |
| `MSD-010` | `digital_products_templates_plugins` | Approve browser read-only for public-read scope. | Convert the product proof packet into reusable marketplace evidence fields. |
| `MSD-011` | `digital_products_templates_plugins` | Approve browser read-only for public-read scope. | Draft a template-product readiness checklist using only local proof package structure. |
| `MSD-012` | `digital_products_templates_plugins` plus `productized_services_marketplaces` | Approve browser read-only for public-read scope. | Prepare an app/theme route decision template: build complexity, review burden, support burden, expected time to first sale. |
| `MSD-013` | `productized_services_marketplaces` plus `lead_generation_and_sales` | Approve browser read-only for public-read scope. | Create fictional offer packets and pricing hypotheses without using real leads or marketplace accounts. |
| `MSD-014` | `qa_usability_testing_gigs` | Human-only decision before any account, test, or application action. | Write a human-only eligibility and risk packet; agents may not perform tests or submit user feedback. |
| `MSD-015` | `ai_training_eval_gigs` | Human-only decision before any account, test, or application action. | Write a human-only risk packet emphasizing no automation, no answer submission, and no identity/account action by agents. |
| `MSD-016` | `affiliate_partner_programs` plus `content_and_social_growth` | Approve browser read-only for public-read scope. | Create a local affiliate-program scout table schema with disclosure and payout-risk fields; do not apply or publish links. |

## Recommended Local Priority

1. `MSD-008` to `MSD-012`: highest local reuse because the product proof bundle already exists.
2. `MSD-003` to `MSD-006`: useful rubric work for future competition managers without accounts or data downloads.
3. `MSD-013`: useful as fictional offer design only.
4. `MSD-014` and `MSD-015`: keep as human-only policy packets.
5. `MSD-002`, `MSD-007`, and `MSD-016`: wait for browser/current-source service approval before route-specific effort.

## Next Safe Local Task

Package the highest-leverage local proof template among `MSD-003` through `MSD-016`; browser/current-source verification remains blocked until service approval.
