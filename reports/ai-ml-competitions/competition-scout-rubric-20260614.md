# AI/ML Competition Scout Rubric

Generated UTC: 2026-06-14T14:52:00Z
Agent: lane-manager-ai_ml_competitions-019ec69a
Thread: 019ec69a-3c39-7de3-849b-f2d19a2d03da
Lane: ai_ml_competitions
Task: task-ai_ml_competitions-startup-20260614

## Scope

This is a local proof artifact for the blocked starter service request:

`req-wave4-ai-ml-competitions-browser-readonly-20260614`

The request is still `needs_review`, so no browser session, account action, live competition page read, dataset access, rules acceptance, notebook run, API spend, or submission was performed. This artifact converts the requested shortlist into a reproducible capture plan for an approved browser-read-only worker.

## Candidate Source Queue

These sources come from local Wave-4 research. Current competition details must be verified later by an approved read-only service worker.

| Source | Prize Route To Capture | Deadline To Capture | Dataset Gate To Capture | Baseline Feasibility Signal | Stop/Service Blockers |
| --- | --- | --- | --- | --- | --- |
| Kaggle money-prize competitions | Public prize pool, medal/payout rules, leaderboard/prize eligibility, winner obligations | Competition deadline and final submission date | Whether data is public metadata only, requires Kaggle login, requires Join, requires Accept Rules, or has external data restrictions | High if metric, sample submission, public notebooks, and small/standard data are visible; medium if image/text/LLM data needs large compute; blocked if data requires acceptance/download | Kaggle account, competition join, rules acceptance, dataset download, notebook submission, model/API spend |
| DrivenData competitions | Public prize amount, sponsor route, prize conditions, eligibility | End date, phase dates, submission cadence | Whether data page is public, account-gated, terms-gated, or license-restricted | High for tabular/time-series/social-impact datasets with clear metric; medium for geospatial/CV/remote-sensing; blocked until data route is approved | Account registration, data terms, dataset download, submission route |
| ML Contests aggregator | Aggregated prize field and upstream source | Aggregated deadline, then upstream deadline | Aggregator does not settle dataset rights; upstream source must be read | Useful for discovery only; baseline feasibility cannot be trusted until upstream rules and data are checked | Must verify upstream official page; no submission/account action from aggregator lead |
| lablab.ai AI hackathons | Prize pool/sponsor tracks, judging route, team awards | Hackathon close date, demo/submission windows | Usually project-building rather than dataset access; capture API/model/tool requirements and allowed assets | Medium if a small demo can be built locally; lower if it depends on paid APIs, team formation, or proprietary tools | Account registration, team/project creation, model/API spend, public submission, demo publishing |
| ETHGlobal AI/web3 tracks | Hackathon prize tracks, sponsor bounties, judging rules | Event dates, submission deadline, judging period | Dataset usually not primary; capture wallet, protocol, API, repo, and deployment requirements | Medium for local prototype planning; lower if contract deployment, wallet transaction, or live demo is required | Registration, wallet action, deployment/transaction, sponsor terms, public project submission |

## Shortlist Capture Schema

For each approved live candidate, capture:

| Field | Requirement |
| --- | --- |
| source_name | Official source, not only aggregator |
| source_url | Public URL read under approved scope |
| competition_title | Exact public title |
| prize_route | Prize amount, payout conditions, sponsor/judging route, eligibility caveats |
| deadline | Absolute deadline date and timezone if visible |
| account_gate | None, login, signup, join, team registration, KYC/tax/payment, or unknown |
| rules_gate | Public rules visible, requires acceptance, legal/terms review needed, or unknown |
| dataset_gate | Public metadata only, data visible without download, download required, paid/API access, restricted license, or unknown |
| metric | Evaluation metric, judging rubric, or manual review route |
| baseline_feasibility | One-day baseline estimate: high, medium, low, or blocked |
| compute_cost_risk | Local CPU/GPU feasible, cloud/API likely, paid service likely, or unknown |
| submission_blocker | Exact public action that is forbidden until approved |
| service_requests_needed | Account, data/API, legal/terms, model/API, public action, wallet, or none |
| next_local_artifact | Baseline plan, data-access packet, legal/rules packet, or park note |

## Scoring

Score only after official page evidence exists.

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Prize route clarity | No visible prize | Prize mentioned but conditions unclear | Prize and broad conditions visible | Prize, eligibility, and payout route clear |
| Deadline feasibility | Closed or impossible | Under 7 days | 7 to 30 days | More than 30 days or generous cadence |
| Dataset access | Unknown or blocked | Requires acceptance/download | Public metadata and likely obtainable with approval | Public sample/data enough for baseline planning |
| Baseline feasibility | No local baseline path | Heavy compute or unclear metric | Simple baseline likely after data approval | Baseline can be built in one day after data approval |
| Agent leverage | Mostly manual/team/social | Requires product demo or large system | Notebook/prototype iteration useful | Reproducible experiments are the core work |
| Gate burden | Public action plus legal/payment/account | Multiple service requests | One clear service request | Read-only evaluation sufficient for next step |

## First Approved Test

When and only when the browser-read-only service request is approved:

1. Confirm the request status is approved before starting.
2. Read the Kaggle money-prize listing first, because the local registry explicitly named it and the requested target URL is Kaggle.
3. Capture up to 10 visible money-prize leads from the listing without logging in or clicking Join/Submit/Download.
4. Open only public overview/rules pages that do not require login, rule acceptance, or account changes.
5. Produce a five-row shortlist with the schema above.
6. If every candidate is gated, write a blocker note instead of escalating by clicking through.

## Local Baseline Planning Rule

No baseline notebook should start until dataset access is legal and approved. Before approval, baseline work is limited to a paper plan: likely model class, metric, expected data shape, compute estimate, reproducibility checklist, and service requests needed.

## Local Shortlist Refinement

Added UTC: 2026-06-14T15:20:00Z
Task: task-ai-ml-competition-local-shortlist-template-20260614

This refinement keeps the scout rubric usable before browser approval. It defines the status vocabulary and promotion rule that the blank top-five shortlist must use.

### Gate Status Vocabulary

Use these exact labels in shortlist rows:

| Label | Meaning |
| --- | --- |
| `unverified_local_only` | Placeholder from local planning only; no current official page evidence. |
| `public_read_visible` | Visible under an approved read-only pass without login, join, rule acceptance, or download. |
| `browser_read_required` | Needs an approved browser-read-only worker before the field can be trusted. |
| `account_gate` | Requires login, signup, profile, team, KYC, tax, or payment setup. |
| `rules_acceptance_gate` | Requires Join, Accept Rules, legal agreement, eligibility attestation, or similar commitment. |
| `dataset_download_gate` | Requires downloading, API access, restricted license acceptance, or private/restricted data. |
| `api_or_compute_spend_gate` | Requires paid model/API/cloud/compute spend or nonzero procurement. |
| `public_submission_gate` | Requires notebook, prediction, demo, repo, form, or project submission. |
| `wallet_or_deployment_gate` | Requires wallet connection, transaction, smart-contract deployment, or public web3 action. |
| `parked_unknown` | Cannot rank safely because a core field is unknown or contradictory. |

### Promotion Rule

Do not promote a competition to baseline work from local memory alone. A row can move from `unverified_local_only` to `baseline_plan_candidate` only when an approved read-only evidence artifact has captured:

- official source URL
- competition title
- prize route or non-prize rationale
- absolute deadline
- account gate
- rules gate
- dataset gate
- metric or judging route
- compute/API risk
- exact forbidden submission action

Even then, baseline execution is still blocked until the dataset gate is separately cleared. Before that, the notebook template may contain only metadata, synthetic smoke tests, data-contract assumptions, and a paper experiment plan.

### Tie Breakers

When two candidates have similar scores, prefer:

1. public official-page evidence over aggregator-only evidence
2. explicit prize route over vague award language
3. clear metric over manual judging
4. longer deadline over urgent deadlines
5. smaller/local baseline path over paid-compute assumptions
6. fewer service requests over account/data/legal/API/public-action chains

### Park Reasons

Use one of these reasons when a row should not advance:

| Park Reason | Use When |
| --- | --- |
| `no_prize_route` | Prize, sponsor award, or earning route is absent or unclear. |
| `deadline_not_feasible` | The deadline is closed, expired, timezone-ambiguous, or too close for a reviewed baseline. |
| `data_gate_unclear` | Dataset route, license, or download requirement is not visible. |
| `rules_gate_unclear` | Eligibility, team rules, or required acceptance is not visible. |
| `compute_cost_unclear` | Expected API/cloud/model spend cannot be bounded. |
| `submission_route_gated` | Only meaningful next step is a public submission or join action. |
| `wrong_lane` | Better routed to web3 hackathon, digital product, productized service, or another lane. |
