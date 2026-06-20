# Kaggle Money Competition Scout Worksheet Local Proof

- Generated: `2026-06-18T07:02:31Z`
- Task: `task-lane-scout-kaggle_money_competitions-20260618`
- Lane: `ai_ml_competitions`
- Status: `kaggle_money_competition_scout_worksheet_ready_local_only`
- Decision: `worksheet_only_no_account_no_data_download_no_submission_no_runtime`
- Validation: `True` with `0` failures

## Summary

Kaggle is a valid money-competition lane, but current automated active-listing capture is gated by Kaggle authentication and competition-specific rules. This packet creates the scout worksheet, source route plan, scoring rubric, kill reasons, and exact gates for a later approved listing refresh.

## Sources

- `https://www.kaggle.com/competitions` (official_listing_page): Official competition listing exists but is JavaScript-heavy in text fetches. Use it as a human/browser review source only after an approved read-only browser request.
- `https://www.kaggle.com/api/v1/competitions/list?category=featured&page=1` (public_api_probe): Read-only unauthenticated probe returned HTTP 401 Unauthorized. Automated current listing refresh requires an approved Kaggle credential/API-token route.
- `https://raw.githubusercontent.com/Kaggle/kaggle-cli/main/README.md` (official_cli_readme): The official Kaggle CLI can list competitions, download competition data, and submit to competitions. These capabilities must be split into separate scout, data-access, and submission gates.
- `https://raw.githubusercontent.com/Kaggle/kaggle-cli/main/docs/README.md` (official_cli_docs): Kaggle CLI authentication requires a Kaggle account and token or OAuth flow. Any credential generation, account login, or API-token storage is gated.
- `https://raw.githubusercontent.com/Kaggle/kaggle-cli/main/docs/competitions.md` (official_cli_competitions_docs): The CLI supports competition list filters by group, category, prize sort, deadlines, teams, and created date. It also supports files, download, submit, submissions, leaderboard, and discussion topics commands.
- `https://en.wikipedia.org/wiki/Kaggle` (secondary_overview): Kaggle competitions can be paid or unpaid. Submission, leaderboard, and prize/IP conditions vary by competition and must be read in the specific rules.
- `https://arxiv.org/abs/2511.06304` (research_overview): Recent Kaggle ecosystem research frames the platform as a broad competition, notebook, model, dataset, and discussion ecosystem. Use discussions and prior writeups as learning signals, not as permission to submit.
- `E:\agent-company-lab\reports\money-path-lane-scout-packets\arc-prize-2026-baseline-local-proof.md` (local_prior_packet): Prior competition lane work kept account, official data, submission, paid compute, and public action blocked. Reuse that gate posture for Kaggle prize scouting.

## Worksheet Fields

- `competition_url_or_slug`
- `observed_utc`
- `source_route`
- `competition_group`
- `category`
- `title`
- `prize_usd_or_text`
- `deadline_utc`
- `teams_count`
- `submission_type`
- `data_access_requires_rules_acceptance`
- `code_competition`
- `external_data_policy`
- `license_or_ip_terms_summary`
- `eligibility_flags`
- `compute_requirements`
- `baseline_available_locally`
- `expected_hours_to_first_submission`
- `expected_value_score`
- `kill_reasons`
- `next_local_action`

## CLI Refresh Plan

- `manual_read_only_listing`: `Human/browser read of https://www.kaggle.com/competitions sorted by prizes/deadlines`; gate `browser_read_only_service_request`; allowed now `False`
- `credentialed_cli_listing`: `kaggle competitions list --group general --category featured --sort-by prize -v`; gate `kaggle_account_and_api_token_approval`; allowed now `False`
- `competition_files_probe`: `kaggle competitions files <slug> --page-size=20 -v -q`; gate `rules_and_data_access_review`; allowed now `False`
- `local_baseline_only`: `Use public/open fixtures or synthetic fixture locally; no Kaggle download or submission`; gate `local_only_no_external_action`; allowed now `True`

## Scoring Rubric

- `prize` (20 pts): cash prize explicit and nonzero
- `deadline` (15 pts): at least 14 days to first useful local baseline
- `data_access` (15 pts): data can be inspected after approved rules review; no private/medical ambiguity
- `baseline_feasibility` (15 pts): simple local baseline or public tutorial can be reproduced without paid compute
- `competition_density` (10 pts): low/moderate team count or niche expertise advantage
- `rules_clarity` (10 pts): external data, team, code, and IP rules are unambiguous
- `skill_fit` (10 pts): tabular/NLP/vision/agentic task matches available local skills
- `payout_route` (5 pts): eligibility and tax/payment route can be reviewed before submission

## Candidate Classes

- `featured_cash_prize`: route Kaggle featured category sorted by prize; first local action record slug/title/prize/deadline/rules URL only; promotion gate specific competition rules and eligibility reviewed.
- `research_cash_prize`: route Kaggle research category sorted by prize; first local action screen for data ethics, external data rules, and compute scale; promotion gate data provenance and publication/IP terms reviewed.
- `playground_practice`: route Kaggle playground category; first local action use as baseline rehearsal only; promotion gate do not count as money path unless cash prize exists.
- `code_competition`: route competition docs/files indicate notebook or code submission; first local action read kernel/submission constraints and design local harness; promotion gate no Kaggle notebook run or submit without account/compute approval.

## Hard Kill Reasons

- `no_cash_prize_or_unclear_prize`
- `deadline_too_close_for_first_local_baseline`
- `rules_or_eligibility_unreadable_without_account`
- `requires_accepting_terms_or_downloading_data_before_review`
- `medical_biometric_child_or_sensitive_data_provenance_unclear`
- `external_data_policy_unclear`
- `requires_paid_compute_or_large_gpu_without budget approval`
- `requires_team_or_organization_commitment`
- `requires_public_notebook_or_writeup_before approval`
- `tax_payment_or_country_eligibility_unclear`
- `cannot_reproduce_baseline_locally`

## Boundary

- `kaggle_account_or_login`: `False`
- `api_token_or_credentials_created`: `False`
- `competition_rules_accepted`: `False`
- `competition_data_downloaded`: `0`
- `submissions_made`: `0`
- `public_notebooks_or_comments`: `0`
- `payments_or_tax_forms`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Recommended Next Local Proof

Create a no-login Kaggle competition row fixture from manually saved public listing/rules snippets, then run the worksheet scorer and prove all rows either have a next local baseline action or a kill reason. Keep Kaggle account, API token, rules acceptance, data download, notebook execution, submission, payment, public action, worker/runtime, and model/MCP calls blocked.
