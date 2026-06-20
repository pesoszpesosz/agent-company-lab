# AI/ML Competitions Public Prize Source Refresh

Generated UTC: 2026-06-16T19:56:00Z
Lane: `ai_ml_competitions`
Scope: read-only public source scan; no account creation, terms acceptance, dataset download, submission, paid compute, or external side effect.

## Executive Takeaway

The AI/ML competitions lane is worth promoting from "thin coverage" to an active seeker lane. The current best near-term candidates are not generic Kaggle practice competitions; they are prize tracks where agents can create local feasibility artifacts before any account or submission gate:

1. ARC Prize 2026 / Kaggle ARC-AGI tracks: large prize pool, open-source requirement, no-internet evaluation constraint.
2. AIcrowd ARC White-Box Estimation Challenge 2026: $100k pool, LLM-assisted development explicitly allowed, public starter-kit route.
3. Intrinsic AI for Industry Challenge: $180k robotics/simulation prize, GitHub toolkit, high technical complexity.
4. GENIAC-PRIZE 2026: very large Japan/NEDO prize and compute pool, but eligibility and language/registration gates need review.
5. Zindi / DrivenData / EvalAI / Hugging Face / Codabench: good recurring source registries; individual competitions need filtering for cash prizes, eligibility, deadline, and account/data terms.

## Candidate Shortlist

| Rank | Candidate | Prize Signal | Why It Matters | First Local Proof | Gate Before Action |
| ---: | --- | --- | --- | --- | --- |
| 1 | ARC Prize 2026, ARC-AGI-2/3/Paper tracks | ARC page reports $2M across three tracks and Kaggle submission routes. | Strong fit for agentic reasoning, open-source progress, and reusable local research artifacts. | Build a local rules matrix and baseline feasibility memo from public ARC resources; no Kaggle login or submission. | Kaggle account, competition rules acceptance, open-source licensing, no-internet evaluation constraints. |
| 2 | AIcrowd ARC White-Box Estimation Challenge 2026 | AIcrowd page reports a $100k prize pool with Phase 1 and Phase 2 dates in 2026. | LLM-assisted development is explicitly permitted; likely suitable for iterative code agents. | Clone/read the public starter kit only if license/scope is clear; draft a local packaging and scoring harness plan. | AIcrowd account, official rules, team submission caps, package upload/submission. |
| 3 | Intrinsic AI for Industry Challenge | Intrinsic page lists $180k in cash prizes and a GitHub participant toolkit. | Robotics/simulation challenge could use local agents for environment setup, baseline controller review, and feasibility. | Read the toolkit and create a "can we run sim locally?" checklist; no registration. | Team registration, participant terms, hardware/remote deployment phase, compute requirements. |
| 4 | GENIAC-PRIZE 2026 | METI says maximum prize money is 630M yen plus up to 400M yen compute resources for one theme. | Huge prize/compute signal, but likely heavier eligibility, language, jurisdiction, and program rules. | Translate/summarize dedicated-site eligibility and theme requirements into a gate packet. | Jurisdiction, Japanese application flow, corporate/student eligibility, legal terms. |
| 5 | Kaggle active AI/hackathon list | Search result showed active AI competitions including BenchFlow ($20k) and Triagegeist ($10k). | Useful rolling source for smaller agent-feasible competitions and portfolio wins. | Build a weekly Kaggle active-prize scraper worksheet from public listings; no login. | Competition-specific rules, account, datasets, submissions. |
| 6 | Zindi competitions | Zindi says 100k+ AI builders, 575+ challenges, and over $1M awarded. | Good broad venue for practical applied ML challenges and smaller cash prizes. | Public listing inventory: prize, eligibility, dataset access, region restrictions. | Account, rules acceptance, data terms, team/collaboration limits. |
| 7 | DrivenData competitions | DrivenData reports $4.976M+ in prizes and 260k submissions historically. | High-quality social-impact competitions; often strong documentation and reproducible baselines. | Identify currently open cash-prize competitions and produce a feasibility memo. | Account, competition rules, data terms, submission route. |
| 8 | EvalAI / Hugging Face / Codabench registries | EvalAI hosts challenge pages; Hugging Face has a competitions page; Codabench has active challenge pages. | Useful as source registries, but individual prize/eligibility must be verified per challenge. | Add registry checks to the weekly source-spec cadence. | Hosting/platform terms, hidden test data, compute cost, submission rules. |

## Agent Assignment

Recommended lane manager action:

- Assign `competition_scout` to maintain a weekly public prize registry.
- Assign `dataset_reader` only after a rules packet proves dataset access is public or approved.
- Assign `baseline_builder` only after local feasibility is clear and no account/terms/download gate is crossed.
- Hold `submission_packet_writer` until a specific competition has user-approved account/rules scope.

## First Work Packet

Task ID proposal: `task-ai-ml-competitions-public-prize-shortlist-20260616`

Worker: `competition_scout`

Allowed scope:

- Read public competition pages.
- Record prize, deadline, platform, account gate, dataset gate, compute needs, and local baseline feasibility.
- Create local markdown/json shortlist only.

Forbidden scope:

- No signup/login.
- No competition rules acceptance.
- No dataset download behind terms.
- No notebook submission or package upload.
- No paid compute.
- No team creation.

Required proof artifact:

- `reports/ai-ml-competitions/public-prize-shortlist-YYYYMMDD.md`
- Columns: candidate, source URL, prize, deadline, eligibility, account gate, dataset gate, baseline feasibility, expected hours to first local proof, next approval needed.

## Sources Checked

- https://mlcontests.com/
- https://arcprize.org/competitions/2026
- https://www.aicrowd.com/challenges/arc-white-box-estimation-challenge-2026
- https://www.intrinsic.ai/events/ai-for-industry-challenge
- https://www.meti.go.jp/english/press/2026/0529_002.html
- https://zindi.africa/
- https://www.drivendata.org/competitions/
- https://www.kaggle.com/competitions
- https://huggingface.co/competitions
- https://eval.ai/web/challenges
- https://www.codabench.org/competitions/14060/

## Next Action

Create the formal `public-prize-shortlist` work packet for `competition_scout`, starting with ARC Prize 2026 and AIcrowd WhestBench because they have the clearest current prize signals and local-feasibility path.
