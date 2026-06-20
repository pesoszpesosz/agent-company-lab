# Kaggle No-Login Competition Fixture Scorer

- Generated: `2026-06-18T09:01:57Z`
- Task: `task-kaggle-no-login-competition-fixture-scorer-v1-20260618`
- Status: `kaggle_no_login_fixture_scorer_ready_local_only`
- Decision: `saved_rows_scored_zero_submission_ready_all_rows_have_local_action_or_kill_reason`
- Validation: `True` with `0` failures
- Fixture: `E:\agent-company-lab\reports\ai-ml-competitions\kaggle-no-login-competition-fixture-scorer-v1-fixture-20260618.json`
- Results: `E:\agent-company-lab\reports\ai-ml-competitions\kaggle-no-login-competition-fixture-scorer-v1-results-20260618.json`

## Summary

- `row_count`: `4`
- `local_baseline_candidate_count`: `4`
- `kill_only_count`: `0`
- `submission_ready_count`: `0`
- `source_acceptance_checks`: `6`

## Scored Rows

| Slug | Decision | Score | Local Action | Kill Reasons |
| --- | --- | ---: | --- | --- |
| `featured-tabular-forecasting-cash-prize-saved-snippet` | `local_baseline_only` | 70 | draft_local_baseline_stub_without_kaggle_data | `requires_accepting_terms_or_downloading_data_before_review`, `rules_or_eligibility_unreadable_without_account`, `tax_payment_or_country_eligibility_unclear` |
| `research-medical-image-cash-prize-saved-snippet` | `local_baseline_only` | 45 | draft_standard_library_code_submission_harness_without_running_notebook | `cannot_reproduce_baseline_locally`, `medical_biometric_child_or_sensitive_data_provenance_unclear`, `requires_accepting_terms_or_downloading_data_before_review`, `requires_paid_compute_or_large_gpu_without_budget_approval`, `rules_or_eligibility_unreadable_without_account`, `tax_payment_or_country_eligibility_unclear` |
| `playground-practice-no-cash-saved-snippet` | `local_baseline_only` | 30 | draft_local_baseline_stub_without_kaggle_data | `crowded_or_practice_only_lane`, `no_cash_prize_or_unclear_prize`, `requires_accepting_terms_or_downloading_data_before_review`, `rules_or_eligibility_unreadable_without_account`, `tax_payment_or_country_eligibility_unclear` |
| `code-agent-routing-challenge-saved-snippet` | `local_baseline_only` | 70 | draft_local_baseline_stub_without_kaggle_data; draft_standard_library_code_submission_harness_without_running_notebook | `requires_accepting_terms_or_downloading_data_before_review`, `rules_or_eligibility_unreadable_without_account`, `tax_payment_or_country_eligibility_unclear` |

## Boundary

- `saved_rows_created`: `4`
- `scored_rows`: `4`
- `local_baseline_candidate_count`: `4`
- `submission_ready_count`: `0`
- `kaggle_account_or_login`: `False`
- `api_token_or_credentials_created`: `False`
- `competition_rules_accepted`: `False`
- `competition_data_downloaded`: `0`
- `notebooks_executed`: `0`
- `submissions_made`: `0`
- `payments_or_tax_forms`: `0`
- `public_notebooks_or_comments`: `0`
- `browser_sessions_started`: `0`
- `service_requests_mutated`: `0`
- `workers_or_runtimes_started`: `0`
- `model_mcp_or_external_api_calls`: `0`
- `external_side_effects`: `0`

## Next Local Action

For local_baseline_only rows, create offline stub baselines using synthetic/public-open data only. Do not log in, create API tokens, accept competition rules, download Kaggle data, run Kaggle notebooks, submit, pay, post publicly, start workers/runtimes, or call model/MCP/external APIs from this packet alone.
