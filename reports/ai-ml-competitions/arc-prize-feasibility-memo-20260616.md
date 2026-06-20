# ARC Prize 2026 Feasibility Memo

Generated UTC: 2026-06-16T20:41:00Z
Task: `task-arc-prize-feasibility-memo-20260616`
Lane: `ai_ml_competitions`
Owner: `lane-manager-ai_ml_competitions-019ec69a`
JSON mirror: `E:\agent-company-lab\reports\ai-ml-competitions\arc-prize-feasibility-memo-20260616.json`

## Executive Decision

ARC Prize 2026 is worth local research and baseline work, but not yet worth account/submission action. It has large prize upside and strong alignment with reasoning-agent research, but the competition route has Kaggle/rules/submission gates and a high bar for real prize probability.

Decision: promote a local baseline memo/harness task only. Do not join, accept rules, download gated data, or submit.

## Current Public Signals

| Signal | Current Evidence | Implication |
| --- | --- | --- |
| Large prize pool | ARC Prize competitions page describes ARC Prize 2026 as `$2M in prizes` across 3 tracks. | High upside, but high competition. |
| ARC-AGI-2 track | Public ARC-AGI-2 page lists progress prizes totaling `$275,000` plus ranked prizes. | Good fit for local baseline/research, not quick cash. |
| ARC-AGI-3 track | Public ARC-AGI-3 page lists guaranteed milestone prizes with June 30 and September 30 milestones. | Milestone #1 is too close for serious new work; milestone #2 is more realistic. |
| Key dates | 2026 page lists March 25 start, June 30 milestone, September 30 milestone, November 2 submissions due, November 8 papers due, December 4 results. | There is time for local baseline exploration before final deadline. |
| Kaggle route | Kaggle pages indicate competition-rule acceptance and submission deadlines. | Account/rules/submission gate is mandatory. |

## Local Baseline Path

| Step | Local Artifact | No-Side-Effect Rule | Pass/Fail Gate |
| ---: | --- | --- | --- |
| 1 | Public rules/source summary | Use public pages only; no Kaggle login or rule acceptance. | Pass if rules, dates, and tracks are summarized. |
| 2 | Baseline taxonomy | Categorize approaches: symbolic search, program synthesis, test-time adaptation, LLM-assisted solver, hybrid solver. | Pass if at least four approaches have feasibility notes. |
| 3 | Compute estimate | Estimate local hardware/runtime needs for small experiments. | Pass if baseline can run locally without paid APIs. |
| 4 | Sample solver plan | Define a local-only toy ARC-style puzzle harness using public/simple examples or synthetic grids. | Pass if no gated data is required. |
| 5 | Kill criteria | Define when to stop before expensive account/submission work. | Pass if kill criterion is measurable. |

## Approach Ranking

| Rank | Approach | Why | Local Proof | Risk |
| ---: | --- | --- | --- | --- |
| 1 | Hybrid symbolic search plus LLM critique | Uses agent strengths for hypothesis generation while keeping verification deterministic. | Build toy grid-transform harness with rule candidates and verifier. | May not transfer to official tasks. |
| 2 | Program synthesis library survey | ARC tasks often reward compositional transforms. | Survey small Python DSL options and write two synthetic transforms. | Time can vanish into framework building. |
| 3 | Test-time adaptation notes | Competition likely rewards generalization beyond memorized patterns. | Local memo comparing adaptation methods without training large models. | Compute/data constraints. |
| 4 | Paper-track synthesis | Paper prizes may reward insight even without top leaderboard result. | Draft outline of what a small open-source solver experiment could teach. | Requires actual competition entry for some paper routes. |

## Score

| Metric | Score | Notes |
| --- | ---: | --- |
| Prize upside | 5 | Large public prize pool. |
| Time to first local proof | 3 | A toy harness is feasible, but meaningful signal takes time. |
| Gate burden | 4 | Account, Kaggle rules, submission, possible open-source/public notebook requirements. |
| Competition intensity | 5 | Global competition, likely sophisticated entrants. |
| Strategic value | 5 | Strong infrastructure value for reasoning agents even if no prize. |

## Required Gates Before External Action

- `account_registration_intake`
- Competition rules/legal review
- `public_action_execution` for any submission/notebook/writeup
- Cost approval before paid compute/API use

## Kill Criterion

Do not request Kaggle/rules/submission approval unless a local toy harness demonstrates at least three distinct grid-transform families with deterministic verification and a written hypothesis for why the approach could generalize.

## Next Action

Create `arc-local-toy-harness-plan-20260616.md` with a minimal DSL, three synthetic task families, deterministic verifier, and no paid compute/API dependency.

## Source URLs

- https://arcprize.org/competitions
- https://arcprize.org/competitions/2026
- https://arcprize.org/competitions/2026/arc-agi-2
- https://arcprize.org/competitions/2026/arc-agi-3
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2

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
