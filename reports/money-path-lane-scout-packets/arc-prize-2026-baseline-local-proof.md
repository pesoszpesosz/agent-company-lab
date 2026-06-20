# ARC Prize 2026 Baseline Local Proof

Generated UTC: 2026-06-18T06:38:12Z
Task: `task-lane-scout-arc_prize_2026-20260618`
Lane: `ai_ml_competitions`

Purpose: convert ARC Prize 2026 public rules and existing local toy-harness evidence into a baseline plan. This is not a Kaggle account, rules acceptance, data download, competition submission, notebook, paper, paid compute/API run, or public action.

## Source Observations

| Source | URL | Observation | Route Effect |
| --- | --- | --- | --- |
| `arc_prize_2026_overview` | https://arcprize.org/competitions/2026 | ARC Prize 2026 lists $2M in prizes across three tracks: ARC-AGI-3, ARC-AGI-2, and Paper Prize. Key dates include March 25 start, June 30 ARC-AGI-3 Milestone #1, September 30 Milestone #2, November 2 submissions due, November 8 papers due, and December 4 results. | High upside and strategic learning value, but the route is not quick cash and requires rules, Kaggle, open-source, and submission gates before external action. |
| `arc_agi_3_track` | https://arcprize.org/competitions/2026/arc-agi-3 | ARC-AGI-3 challenges participants to build AI agents for novel interactive environments without instructions. The track lists $850K total, including a $700K grand prize for 100%, guaranteed top-score awards, and milestone prizes. Submissions must go through Kaggle, no internet access is available during evaluation, and all code/methods must be open sourced to be prize eligible. | Any serious baseline must be offline-capable, reproducible, open-source-ready, and tested locally before account/rules/submission gates. |
| `arc_agi_3_docs_quickstart` | https://docs.arcprize.org/ | ARC-AGI-3 docs describe an interactive benchmark for exploration, percept-plan-action, memory, goal acquisition, and alignment. Quickstart references installing the arc-agi toolkit and optional API key, then playing public environments. | Toolkit/API use remains gated here; this packet keeps the baseline at synthetic/local proof until approval exists. |
| `local_arc_toy_harness` | E:/agent-company-lab/reports/ai-ml-competitions/arc-toy-harness-run-20260616.md | Existing local toy harness checked five synthetic tasks and passed all five: translation, recolor, mirror, crop-and-tile, and explicit no-solution failure case. It used no official ARC data, no Kaggle login/download, no paid compute/API, no submission/public action, and no external side effects. | The local kill criterion has enough proof to justify a next local baseline design, but not enough to justify Kaggle/account/submission action. |

## Baseline Tracks

| Priority | Track | Target | Local Start | Gates |
| ---: | --- | --- | --- | --- |
| 1 | `arc_agi_3_offline_agent_baseline` | ARC-AGI-3 interactive reasoning | Extend synthetic toy harness from static transforms into a tiny turn-based environment with replay traces. | `account`, `kaggle_rules`, `submission`, `public_action`, `worker_runtime`, `paid_compute`, `api_key` |
| 2 | `arc_agi_2_symbolic_solver_baseline` | ARC-AGI-2 static reasoning | Continue the existing DSL harness and add more transform families before using any official/gated competition data. | `account`, `kaggle_rules`, `dataset_download`, `submission`, `public_action` |
| 3 | `paper_prize_experiment_log` | ARC Prize 2026 paper track | Maintain a structured experiment log from every toy-harness and baseline run. | `public_action`, `submission`, `open_source_license_review`, `claim_review` |

## Track Details

### `arc_agi_3_offline_agent_baseline`

The official track is agentic and offline-evaluated, so the baseline must focus on exploration, memory, world-model inference, and action planning without API calls.

Deliverables:
- Offline local environment fixture with at least three tiny games.
- Deterministic random/explore baseline.
- Replay JSON with observations, actions, score, and terminal state.
- Failure taxonomy for exploration, goal inference, and planning misses.

### `arc_agi_2_symbolic_solver_baseline`

Existing synthetic grid-transform proof already works locally, and static tasks are a cleaner proving ground for deterministic DSL search.

Deliverables:
- At least eight synthetic transform families.
- Candidate program search metrics.
- Generalization failure cases.
- Open-source-ready solver scaffold notes.

### `paper_prize_experiment_log`

Paper route may preserve value even if leaderboard performance is weak, but claims need reproducible experiments.

Deliverables:
- Experiment log schema.
- Method comparison table.
- Negative results registry.
- Paper outline after at least two local baselines.

## Recommended First Track

`arc_agi_3_offline_agent_baseline`

ARC Prize 2026 has large upside and strong strategic fit, and the local toy harness already proves a small deterministic baseline path. External action remains premature because Kaggle/rules/submission/open-source/license/compute gates are unresolved and no official baseline has been run.

## Next Local Sprint

Sprint: `arc_agi_3_micro_env_replay_baseline_v1`
Duration hypothesis: 3-6

Success criteria:
- Create three toy interactive environments with deterministic state transitions.
- Run at least two baseline policies: random and simple exploration-memory.
- Write replay JSON for every run.
- Pass deterministic replay validation without network, API, Kaggle, official data, paid compute, or account access.

Continue/kill rule: Continue toward ARC-AGI-3 only if the simple exploration-memory baseline beats random on at least two of three toy environments and the replay logs identify actionable failure modes.

## Acceptance Checks

- Official ARC Prize 2026 overview, ARC-AGI-3 track, and docs are summarized.
- Local toy harness evidence is incorporated.
- At least three baseline tracks are defined with deliverables and gates.
- A next local sprint is specified with success criteria and a measurable continue/kill rule.
- No Kaggle account/login, rules acceptance, data download, submission, paid compute, API key, worker/runtime start, public action, or external side effect occurs.

## Boundary

No Kaggle account/login, rules acceptance, official/gated data download, submission, paper/notebook publication, paid compute/API, API key, public action, service-request mutation, worker/runtime start, or external side effect occurred.

## Next Action

Create the ARC-AGI-3 micro-environment replay baseline locally; keep Kaggle account/rules, official data, submission, paper/public action, paid compute/API, worker/runtime, and external side effects blocked until human approval.
