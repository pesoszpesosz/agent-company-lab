# EF ESP Read-Only Ingestion Packet

Generated UTC: 2026-06-16T21:12:00Z
Task: `task-ef-esp-readonly-ingestion-packet-20260616`
Lane: `web3_airdrops_grants_hackathons`
Owner: `lane-manager-web3_airdrops_grants_hackathons-019ec613`
Source evidence: `E:\agent-company-lab\reports\web3-airdrops-grants-hackathons\ef-esp-wishlist-rfp-classifier-prototype-20260616.md`
Status: local ingestion plan only

## Purpose

Define the exact read-only ingestion workflow for EF ESP Wishlist/RFP opportunities before any browser refresh, application, office-hours request, proposal, budget commitment, wallet, deployment, or public action.

## Ingestion Scope

Allowed after a separately approved read-only source refresh:

- Read public Wishlist/RFP pages.
- Capture title, URL, category, deadline, expected artifact, eligibility hints, and application route.
- Classify rows with the local prototype scoring formula.
- Save a local Markdown/JSON decision packet.

Not allowed:

- Apply for ESP funding.
- Request office hours.
- Contact EF/ESP or any maintainer.
- Propose a budget.
- Commit milestones.
- Create a wallet.
- Deploy contracts or public repos.
- Accept terms, legal commitments, or payment routes.

## Data Contract

Each ingested row should include:

| Field | Required | Notes |
| --- | --- | --- |
| `source_url` | yes | Public Wishlist/RFP URL only |
| `title` | yes | Exact public title |
| `category` | yes | Normalize to tooling, research, security, education, app-layer, community, cryptography, other |
| `deadline` | if visible | `null` when not visible |
| `expected_artifact` | yes | Report, prototype, implementation, documentation, event, research |
| `eligibility_notes` | yes | Local summary, no legal conclusion |
| `application_route` | yes | Read-only description |
| `budget_signal` | if visible | Do not propose budget |
| `agent_company_fit` | yes | Which existing lane/product can produce local proof |
| `gate_burden` | yes | Account, wallet, legal, deployment, public, payment, security, none |
| `decision` | yes | Classifier output |

## Classifier Application

Reuse the prototype formula:

`fit_score = strategic_fit + local_proofability + reuse_value - gate_burden - credential_gap`

Promotion rule:

- Promote to local prototype only if `fit_score >= 6`.
- Park if rules, budget, eligibility, wallet, deployment, or public commitment are unclear.
- Reject if the item requires domain expertise or credentials that cannot be evidenced.

## Example Row Shapes

| Type | Likely Decision | Reason |
| --- | --- | --- |
| Public-goods opportunity radar | `promote_local_prototype` | Reuses source registry, dashboard, and gate model |
| Builder workflow approval templates | `promote_local_prototype` | Reuses service-worker decision packet templates |
| Security education / audit-prep tooling | `park_for_rules_review` | Security scope and public claims need review |
| Ethereum app-layer prototype | `park_for_rules_review` | Wallet, deployment, and public repo gates likely |
| Cryptography research implementation | `reject_poor_fit` | Specialist gap unless human skill inventory changes |

## Read-Only Refresh Request Draft

Request type: `browser_research`

Risk gate: `catalog_required_approval_no_external_action`

Requested action:

`Read public EF ESP Wishlist/RFP pages and capture opportunity rows into the local classifier contract. Do not apply, request office hours, create accounts, provide budgets, contact maintainers, deploy code, create wallets, or perform public actions.`

Approval scope:

`Public read-only page capture of EF ESP Wishlist/RFP opportunity metadata into E:\agent-company-lab reports. No login, form submission, contact, budget proposal, wallet, payment, deployment, public repo, or account action.`

## Acceptance Checks

- Every row has a source URL and local decision.
- No application or contact text is drafted as if approved.
- No budget promise appears.
- No wallet/deployment step is marked executable.
- Rows requiring public commitment are parked, not promoted.

## Decision

Current status: `ready_for_human_review_of_readonly_refresh`.

This packet is enough to request a read-only browser worker later, but it does not itself authorize that worker.

## Boundary

- ESP application: `false`
- Office-hours request: `false`
- Proposal/budget commitment: `false`
- Wallet/payment: `false`
- Deployment: `false`
- Public action: `false`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
