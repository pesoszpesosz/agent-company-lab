# Source Spec Seed Packet: ai_ml_competitions

Generated UTC: 2026-06-15T17:00:55Z
JSON mirror: `E:\agent-company-lab\reports\source-spec-seed-packets\ai_ml_competitions-source-spec-seed-20260615.json`

## Proposed Source Spec

- ID: `ai_ml_competitions_public_prize_source_seed`
- Name: AI/ML Competition Public Prize Source Seed
- Type: `public_competition_registry`
- Cadence: `lane_owner_on_demand_or_weekly`
- Risk gate: `read_only_public_research_no_account_submission_dataset_download_or_terms_acceptance`

## Source Paths

- Kaggle competitions listing
- DrivenData competitions listing
- EvalAI challenges listing
- AICrowd challenges listing
- Hugging Face competitions/spaces calls when prize route is explicit

## Outputs

- E:\agent-company-lab\reports\ai-ml-competitions\public-prize-source-refresh-YYYYMMDD.md
- lane_evidence
- service_request_candidates

## Boundary

This packet is report-only. It does not add a source spec, execute refresh commands, browse, register accounts, accept terms, download gated data, publish, submit, touch wallets/payments, mutate service requests, assign workers, call APIs, or create external side effects.

## Next Action

Review and, if accepted, convert into a source-spec registry row in a separate local-only task.

