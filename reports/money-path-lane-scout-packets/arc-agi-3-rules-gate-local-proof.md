# ARC-AGI-3 Rules Gate Local Proof

Generated UTC: 2026-06-18T06:44:08Z
Task: `task-lane-scout-arc_agi_3-20260618`
Lane: `ai_ml_competitions`

Purpose: convert current ARC-AGI-3 public rules and docs into a gate map for the AI/ML competitions lane. This is not a Kaggle login, ARC account action, API key creation, dependency install, official game run, scorecard, submission, publication, paid compute/API call, worker/runtime start, or public action.

## Source Observations

| Source | URL | Observation | Route Effect |
| --- | --- | --- | --- |
| `arc_agi_3_track_rules` | https://arcprize.org/competitions/2026/arc-agi-3 | ARC-AGI-3 is the 2026 interactive reasoning track. It lists $850K total, a $700K grand prize for 100%, guaranteed top-score and milestone prizes, Kaggle submission, no internet during evaluation, and open-source code/method requirements for prize eligibility. | Competition action requires Kaggle/rules, submission, open-source/license, and offline-evaluation readiness gates. |
| `arc_docs_local_vs_online` | https://docs.arcprize.org/local-vs-online | ARC docs recommend local development and testing with the engine: fast, no rate limits, many instances, and no API key. Online mode gives scorecards, shareable replays, and leaderboard visibility but requires an API key and is rate limited. | Local/offline toy baselines are allowed; online scorecards, API keys, shareable replays, and leaderboard effects are gated. |
| `arc_docs_api_keys` | https://docs.arcprize.org/api-keys | API key creation requires logging in with Google or GitHub on the ARC platform, then creating a key and setting it in an environment variable or .env file. | API key creation and storage are account/credential gates and should not be performed by an autonomous lane task. |
| `arc_docs_toolkit` | https://docs.arcprize.org/toolkit/overview | The open-source Python toolkit supports local development, custom games, and local/API interaction. The quickstart installs arc-agi and optionally uses an API key; recent changelog mentions competition mode and official scoring. | Installing/running the official toolkit can be a later local runtime task, but this rules-gate packet performs no dependency install or worker/runtime start. |
| `arc_docs_scoring_methodology` | https://docs.arcprize.org/methodology | ARC-AGI-3 uses Relative Human Action Efficiency. Scoring measures level completion and action efficiency against human baselines; internal reasoning/tool calls do not count as environment actions, but submitted environment actions do. | Local baselines should log completion and action count, not just final success, and should prefer efficient exploration over brute-force action spam. |
| `arc_docs_recordings_scorecards` | https://docs.arcprize.org/recordings | Official recordings are available for API and swarm modes. Local toolkit runs without API do not generate online recordings; swarm can save local recording files in JSONL format. | The next local proof should write its own replay JSON/JSONL without using online scorecards or API replay infrastructure. |
| `local_arc_prize_baseline_packet` | E:/agent-company-lab/reports/money-path-lane-scout-packets/arc-prize-2026-baseline-local-proof.md | Existing local baseline packet recommends an ARC-AGI-3 offline agent baseline and a micro-environment replay sprint, while keeping Kaggle account/rules, official data, submission, paid compute/API, worker/runtime, and public actions blocked. | This packet converts that baseline into a precise go/no-go gate checklist. |

## Gate Matrix

| Gate | Status | Approval Needed | Allowed Now | Blocked |
| --- | --- | --- | --- | --- |
| `local_synthetic_micro_env` | `allowed_now` | `false` | Write synthetic turn-based toy environments.<br>Run deterministic policies using Python standard library.<br>Record local JSON/JSONL replays.<br>Score completion and action counts locally. | official ARC data download<br>Kaggle submission<br>ARC online scorecards<br>API key use |
| `official_toolkit_install_or_runtime` | `needs_explicit_local_runtime_approval` | `true` | Draft dependency/install plan.<br>Review docs and API surface. | pip/uv install<br>running official games<br>starting worker runtime<br>downloading game sources |
| `arc_api_key_and_online_scorecard` | `blocked` | `true` | Prepare key-handling checklist.<br>Describe online scoring route. | Google/GitHub login<br>API key creation<br>.env write<br>online scorecard open/close<br>leaderboard-visible runs |
| `kaggle_competition_submission` | `blocked` | `true` | Prepare submission-readiness checklist.<br>Review public rules. | Kaggle login<br>rules acceptance<br>competition submission<br>notebook publication<br>official evaluation |
| `open_source_release` | `blocked` | `true` | Draft license/readme checklist.<br>Check third-party dependency licenses locally. | GitHub publication<br>public repo creation<br>release upload<br>paper/public claim |
| `paid_compute_or_model_api` | `blocked` | `true` | Estimate compute needs.<br>Design offline-first experiments. | paid GPU/compute<br>external model API calls<br>cloud jobs<br>billing setup |

## Next Local Proof

Proof: `arc_agi_3_micro_env_replay_gate_safe_v1`

Allowed scope: Python standard-library-only synthetic environments and local replay files.

Required outputs:
- micro-env fixture JSON with three toy environments.
- policy runner JSON/Markdown report comparing random vs exploration-memory policy.
- replay JSONL for each run.
- validation JSON proving no official data, account, API key, dependency install, runtime worker, paid compute, submission, or public action.

Success criteria:
- Exploration-memory policy beats random on at least two of three environments.
- Every run has action count, terminal state, and replay file.
- Validation confirms local-only zero external side effects.
- Failure taxonomy identifies at least three future solver improvements.

## Acceptance Checks

- ARC-AGI-3 competition, toolkit, local-vs-online, API key, scoring, and recording constraints are summarized.
- Allowed local actions are separated from gated official/toolkit/API/Kaggle/public actions.
- Every external or credentialed route has an explicit approval gate.
- The next local proof is scoped to standard-library synthetic environments and local replay artifacts.
- No account, API key, dependency install, official data, runtime worker, submission, payment/paid compute, public action, or external side effect occurs.

## Boundary

No account/login, API key, env/secret write, dependency install, official toolkit/game run, official/gated data download, scorecard, Kaggle submission, notebook/paper publication, paid compute/model API, public action, service-request mutation, worker/runtime start, or external side effect occurred.

## Next Action

Implement the standard-library ARC-AGI-3 micro-environment replay baseline locally; do not install the official toolkit, create/use API keys, log in, download official/gated data, open scorecards, submit to Kaggle, publish code/papers, use paid compute/model APIs, start workers/runtimes, or perform public actions without explicit approval.
