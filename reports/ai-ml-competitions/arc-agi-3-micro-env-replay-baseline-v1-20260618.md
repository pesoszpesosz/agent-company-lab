# ARC-AGI-3 Micro-Environment Replay Baseline

- Generated: `2026-06-18T08:26:41Z`
- Task: `task-arc-agi-3-micro-env-replay-baseline-v1-20260618`
- Status: `arc_agi_3_micro_env_replay_baseline_complete_local_only`
- Decision: `continue_local_arc_agi_3_only_no_external_competition_action`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-micro-env-replay-baseline-v1-fixture-20260618.json`
- Replay JSONL: `E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-micro-env-replay-baseline-v1-replays-20260618.jsonl`

## Baseline Summary

- `environment_count`: `3`
- `policy_count`: `2`
- `episode_count`: `6`
- `memory_beats_random_count`: `3`
- `continue_rule_passed`: `True`

## Policy Comparison

| Environment | Random | Memory | Beats Random |
| --- | --- | --- | --- |
| `key_door_line` | success `False`, actions `7` | success `True`, actions `6` | `True` |
| `color_clue_button` | success `False`, actions `1` | success `True`, actions `1` | `True` |
| `bridge_toggle_goal` | success `False`, actions `4` | success `True`, actions `3` | `True` |

## Failure Taxonomy

- `random_action_spam` observed in `key_door_line`, `color_clue_button`, `bridge_toggle_goal`: Prefer information-gathering and prerequisite actions over uniform random actions.
- `hidden_prerequisite_ordering` observed in `key_door_line`, `bridge_toggle_goal`: Learn prerequisite graphs such as key-before-door and toggle-before-crossing from local replay traces.
- `single_observation_goal_binding` observed in `color_clue_button`: Bind symbolic clues to action names and verify before acting.

## Boundary

- `synthetic_environments_created`: `3`
- `episodes_run`: `6`
- `browser_sessions_started`: `0`
- `kaggle_account_or_login`: `False`
- `rules_or_terms_accepted`: `False`
- `official_or_gated_data_downloaded`: `False`
- `official_arc_toolkit_installed_or_run`: `False`
- `api_keys_created_or_used`: `False`
- `scorecards_opened`: `0`
- `submissions_made`: `0`
- `papers_or_notebooks_published`: `0`
- `paid_compute_or_model_api`: `False`
- `public_actions`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `external_side_effects`: `0`

## Next Local Action

Extend the synthetic micro-environment suite with distractors and a tiny planner that infers prerequisite graphs from replay history. Keep Kaggle account/rules, official data, ARC toolkit/API keys, scorecards, submissions, paper/public action, paid compute/API, worker/runtime, and external side effects blocked.
