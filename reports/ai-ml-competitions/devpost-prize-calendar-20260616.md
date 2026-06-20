# Devpost Weekly Prize Calendar

Generated UTC: 2026-06-16T20:42:00Z
Task: `task-devpost-prize-calendar-20260616`
Lane: `ai_ml_competitions`
Owner: `lane-manager-ai_ml_competitions-019ec69a`
JSON mirror: `E:\agent-company-lab\reports\ai-ml-competitions\devpost-prize-calendar-20260616.json`

## Purpose

Create a reusable local calendar template for Devpost-style hackathons so the AI/ML competition lane can rank prize opportunities before any registration, team join, rules acceptance, or submission.

## Current Public Signals

| Signal | Evidence | Routing Meaning |
| --- | --- | --- |
| Devpost has current online AI hackathons | Public AI category page lists online AI hackathons with prizes and deadlines. | Useful weekly source for prize scouting. |
| Some opportunities are already too late | USAII Global AI Hackathon shows registration expired even though deadline remains. | Calendar must track registration gate separately from submission deadline. |
| Large prize pools exist | Build with Gemini XPRIZE appears in Devpost listings with `$2,000,000` in prizes and August 17 deadline. | High upside, likely high rules/public-action burden. |
| Smaller remote AI events exist | Listings include Qwen Cloud, Arm Create, education AI-agent, and other AI hackathons with varying prizes. | Good for local prototype reuse and ranking. |

## Calendar Template

| Field | Meaning | Required Before Promotion |
| --- | --- | --- |
| Event name | Human-readable hackathon/challenge name. | Yes |
| Devpost URL | Public listing URL. | Yes |
| Prize pool | Cash or non-cash prize signal. | Yes |
| Deadline | Submission deadline and timezone. | Yes |
| Registration status | Open, expired, unclear, or gated. | Yes |
| Online/in-person | Determines feasibility. | Yes |
| Eligibility | Student, age, geography, team-size, professional exclusions. | Yes |
| Required artifact | Demo, repo, video, pitch, notebook, deployed app, paper. | Yes |
| Local build fit | Whether an existing agent-company asset can become a submission candidate. | Yes |
| Gate burden | Account, legal terms, public submission, IP/license, API/compute, team. | Yes |
| Expected value | Prize upside adjusted by competition, time, eligibility, and fit. | Yes |
| First local artifact | What can be built locally before registration. | Yes |

## Initial Watchlist Rows

| Rank | Event / Source | Public Prize Signal | Deadline Signal | Fit | Gate | Decision |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Build with Gemini XPRIZE | `$2,000,000` in prizes on Devpost AI listing | Aug 17, 2026 | Strong if existing agent-company dashboard can become a useful product/demo. | High: rules, account, public submission, likely API/product terms. | Watchlist; needs separate rules packet. |
| 2 | Global AI Hackathon Series with Qwen Cloud | Devpost AI category shows large prize signal across tracks. | Jul 9, 2026 | Strong agent-building theme, but cloud/platform terms likely matter. | High: account, platform/API, public submission. | Watchlist; no API use without approval. |
| 3 | Arm Create: AI Optimization Challenge | Devpost AI category lists `$8,000` in prizes. | Aug 14, 2026 | Possible if local optimization or edge-agent prototype is feasible. | Medium-high: rules and platform constraints. | Candidate for local rules summary. |
| 4 | India High School Exoplanet Data Challenge | Devpost AI category lists `$10,300` in prizes. | Jul 31, 2026 | Interesting data challenge, but eligibility may exclude us. | Eligibility gate. | Park until eligibility clear. |
| 5 | USAII Global AI Hackathon 2026 | Public page lists `$15,000` cash, but registration expired June 6. | Jun 21, 2026 submission deadline | Too late for new registration. | Registration closed; student/team gates. | Reject for current sprint; keep as calendar negative sample. |
| 6 | Smaller AI-agent education/business hackathons | Public category includes smaller/non-monetary prizes. | Rolling July-August | Good for practice/prototype reuse, weak cash. | Lower cash upside, still public submission. | Use only as practice if no high-value event passes. |

## Promotion Rule

Promote a Devpost event into a build sprint only if all are true:

- Registration is open or no registration is required.
- Eligibility is compatible with the user/company.
- Prize or strategic upside is meaningful.
- Required artifact can be built locally before the deadline.
- No paid API, account, public submission, or legal terms are needed before a separate approval gate.
- The event has a concrete first local artifact that can be produced without external side effects.

## Score

| Metric | Score | Notes |
| --- | ---: | --- |
| Source value | 5 | Devpost is a broad current prize radar. |
| Cash probability | 2 | Many events are crowded, eligibility-gated, or non-cash. |
| Time to first local proof | 5 | Calendar and rules packets are local. |
| Gate burden | 4 | Account, terms, team, IP, public submission, and sometimes API/platform gates. |
| Repeatability | 5 | Weekly refresh can keep the lane fed. |

## Next Action

Create a `devpost-rules-packet-build-with-gemini-xprize-20260616.md` only after a read-only rules refresh confirms eligibility, artifact requirements, API terms, and deadline. Until then, keep Devpost as radar, not execution.

## Source URLs

- https://devpost.com/hackathons
- https://devpost.com/c/artificial-intelligence
- https://devpost.com/
- https://usaii-global-ai-hackathon-2026.devpost.com/

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
