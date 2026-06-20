# ARC-AGI-3 Prerequisite Planner Baseline

- Generated: `2026-06-18T08:36:48Z`
- Task: `task-arc-agi-3-prereq-planner-baseline-v1-20260618`
- Source scout: `task-lane-scout-arc_agi_3-20260618`
- Status: `arc_agi_3_prereq_planner_baseline_complete_local_only`
- Decision: `continue_local_arc_agi_3_prerequisite_planner_no_external_competition_action`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-prereq-planner-baseline-v1-fixture-20260618.json`
- Replay JSONL: `E:\agent-company-lab\reports\ai-ml-competitions\arc-agi-3-prereq-planner-baseline-v1-replays-20260618.jsonl`

## Baseline Summary

- `environment_count`: `4`
- `policy_count`: `2`
- `episode_count`: `8`
- `planner_beats_count`: `4`
- `continue_rule_passed`: `True`

## Policy Comparison

| Environment | Distractor Sweep | Prerequisite Planner | Beats Sweep |
| --- | --- | --- | --- |
| `key_door_with_decoys` | success `False`, actions `6` | success `True`, actions `3` | `True` |
| `bridge_toggle_with_waits` | success `False`, actions `6` | success `True`, actions `3` | `True` |
| `color_sequence_lock` | success `False`, actions `6` | success `True`, actions `4` | `True` |
| `tool_bridge_repair` | success `False`, actions `6` | success `True`, actions `4` | `True` |

## Planner Observations

- Prerequisite graph planning beats distractor sweep when observations expose action ordering constraints.
- The local planner remains brittle because it assumes prerequisite edges are visible in observations.
- Next useful local work is hidden-edge discovery from failed attempts rather than official ARC/Kaggle action.

## Boundary

- `synthetic_environments_created`: `4`
- `episodes_run`: `8`
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

Add hidden-prerequisite environments where the planner must infer edges from blocked actions and failed attempts, then compare learned-edge planning against the visible-edge planner. Keep Kaggle account/rules, official data, ARC toolkit/API keys, scorecards, submissions, paper/public action, paid compute/API, worker/runtime, and external side effects blocked.
