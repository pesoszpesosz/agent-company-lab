# EF ESP Wishlist/RFP Classifier Prototype

Generated UTC: 2026-06-16T20:57:00Z
Task: `task-ef-esp-wishlist-rfp-classifier-prototype-20260616`
Lane: `web3_airdrops_grants_hackathons`
Owner: `lane-manager-web3_airdrops_grants_hackathons-019ec613`
JSON mirror: `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-wishlist-rfp-classifier-prototype-20260616.json`

## Purpose

Define a local classifier for EF ESP Wishlist/RFP opportunities. The classifier does not apply, contact ESP, request office hours, propose a budget, or commit to milestones.

## Classifier Inputs

| Field | Meaning |
| --- | --- |
| `item_id` | Stable local ID for Wishlist/RFP item. |
| `title` | Public item title. |
| `category` | Cryptography, privacy, app layer, security, community, tooling, research, etc. |
| `deadline` | Deadline if available. |
| `expected_artifact` | Report, prototype, tool, research, event, implementation. |
| `required_public_commitment` | Whether application/proposal/public repo is needed. |
| `agent_company_fit` | Which existing lane/product can produce proof. |
| `budget_risk` | Low, medium, high, unknown. |

## Scoring Formula

`fit_score = strategic_fit + local_proofability + reuse_value - gate_burden - credential_gap`

Each component is 0-5. Promote only rows with `fit_score >= 6` and no fatal eligibility gap.

## Prototype Rows

| Row | Hypothetical Wishlist/RFP Type | Strategic Fit | Local Proof | Gate Burden | Credential Gap | Score | Decision |
| ---: | --- | ---: | --- | ---: | ---: | ---: | --- |
| 1 | Public-goods opportunity radar / grant discovery tooling | 5 | Source registry and dashboard slice | 4 | 0 | 10 | Promote local prototype. |
| 2 | Builder workflow approval templates | 4 | Service-worker gate templates | 3 | 0 | 9 | Promote local template pack. |
| 3 | Security education or audit-prep tooling | 4 | Synthetic vulnerable contract checklist | 5 | 2 | 5 | Park until security scope review. |
| 4 | Community growth analytics | 3 | Public content/social dashboard | 4 | 1 | 5 | Park until public-data rules clear. |
| 5 | Cryptography research implementation | 2 | None yet | 5 | 4 | -2 | Reject unless specialist joins. |
| 6 | Ethereum app-layer prototype | 3 | Agent-company ops dashboard concept | 5 | 2 | 3 | Park pending wallet/deployment gates. |
| 7 | Developer tooling documentation | 4 | Local docs/template generator | 3 | 0 | 9 | Promote if exact RFP appears. |

## Output Decision Contract

Each classified row must output:

- `promote_local_prototype`
- `park_for_rules_review`
- `reject_poor_fit`
- `request_human_skill_inventory`
- `request_service_gate_packet`

## Kill Criteria

- Reject any item requiring credentials or domain authority we cannot evidence.
- Reject any item requiring immediate public commitment or budget before local proof.
- Park any item requiring wallet, deployment, legal entity, or payment setup.

## Next Action

Create a live-read-only Wishlist/RFP ingestion packet only if the user approves a browser/read-only refresh. Until then, use this classifier as a local decision contract.

## Boundary

- ESP application: `false`
- Office-hours request: `false`
- Proposal/budget commitment: `false`
- Wallet/payment: `false`
- Public action: `false`
- External side effects: `false`
