# AI Resources Candidate Registry Gap List V1

Generated UTC: 2026-06-21T12:17:39Z
Local date: 2026-06-21
Lane: `ai_resources_lab`
Owner: `candidate-registry-curator-20260621`
Status: report-only gap list, local only
JSON mirror: `E:\agent-company-lab\reports\ai-resources-candidate-registry-gap-list-v1-20260621.json`
Source registry: `E:\agent-company-lab\reports\ai-resources-candidate-registry-v2-20260621.json`
Source eval queue: `E:\agent-company-lab\reports\ai-resources-candidate-evaluation-queue-v1-20260621.json`

## Summary

- Registry candidates: `33`
- Queued evaluation candidates: `12`
- Existing evaluation packets: `0`
- Missing evaluation packets: `12`
- Eval packet directory exists: `False`
- Watch-reference candidates not currently eval-ready: `15`
- Blocked-until-gate candidates: `4`

## Immediate Gap

All 12 queued candidates need report-only evaluation packets because `E:\agent-company-lab\reports\ai-resources-evals` is not present yet. This is a packet gap only, not approval to execute candidates.

## Candidates Needing Evaluation Packets

| Rank | Candidate | Eval Family | Required Packet | Stop Gates |
| ---: | --- | --- | --- | --- |
| 1 | `ceo_state_packet_v1` | `control_plane_integrity` | `reports\ai-resources-evals\ceo-state-packet-v1-local-integrity-20260621.md` | service_request_mutation, worker_restart, thread_message, external_api_call |
| 2 | `human_action_feed_v1` | `human_gate_routing` | `reports\ai-resources-evals\human-action-feed-v1-gate-separation-20260621.md` | account_mutation, payment_or_wallet_action, public_action, approval_apply |
| 3 | `ai_resources_owner_acknowledgement_loop` | `continuity_and_ownership` | `reports\ai-resources-evals\owner-acknowledgement-loop-local-fixture-20260621.md` | thread_message, worker_restart, service_request_assignment, external_notification |
| 4 | `pydantic_ai_testmodel_adapter` | `local_prompt_and_worker_harness` | `reports\ai-resources-evals\pydantic-ai-testmodel-fixture-only-20260621.md` | model_api_call, dependency_install, runtime_start, credential_use |
| 5 | `worker_capability_class_registry_v1` | `capability_overlap` | `reports\ai-resources-evals\worker-capability-class-overlap-map-20260621.md` | worker_registration, worker_start, runtime_start, service_request_assignment |
| 6 | `playwright_foundation_adapter` | `browser_worker_policy` | `reports\ai-resources-evals\playwright-browser-policy-contract-20260621.md` | browser_session_start, dependency_install, account_login, public_action |
| 7 | `langgraph_checkpoint_inbox_patterns` | `checkpoint_and_interrupt_pattern` | `reports\ai-resources-evals\langgraph-checkpoint-contract-shape-20260621.md` | dependency_install, model_api_call, runtime_start, worker_start |
| 8 | `prompt_eval_safety_harness` | `prompt_safety` | `reports\ai-resources-evals\candidate-registry-stop-gate-prompt-cases-20260621.md` | model_api_call, external_api_call, public_action, dependency_install |
| 9 | `promptbase_agent_skill_route` | `money_route_local_proof` | `reports\ai-resources-evals\promptbase-approval-rubric-local-only-20260621.md` | marketplace_account, payment_tax_payout, public_listing, submission |
| 10 | `upwork_ai_offer_matrix_route` | `money_route_local_proof` | `reports\ai-resources-evals\upwork-ai-offer-matrix-no-contact-20260621.md` | account_login, proposal_or_message, payment_tax_payout, public_action |
| 11 | `arc_prize_2026_baseline_harness` | `competition_local_proof` | `reports\ai-resources-evals\arc-prize-local-toy-baseline-20260621.md` | competition_account, official_data_download, submission, paid_compute_or_model_api |
| 12 | `kalshi_public_data_worksheet` | `paper_market_research` | `reports\ai-resources-evals\kalshi-saved-row-paper-signal-20260621.md` | live_api_call, account_login, trade_or_order, deposit_withdrawal_payment |

## Recommended Manager Task

- Task: `task-ai-resources-candidate-eval-packet-gap-close-20260621`
- Duplicate key: `ai_resources_candidate_eval_packet_gap_close_20260621`
- Owner: `local-evaluation-harness-builder-20260621`
- Reviewer: `candidate-registry-curator-20260621`
- Priority: `96`
- Next action: Create the first three report-only evaluation packets for ceo_state_packet_v1, human_action_feed_v1, and ai_resources_owner_acknowledgement_loop; then continue down the ranked queue only after each packet has evidence and stop-gate checks.

## Watch And Blocked Candidates

Watch-reference candidates should remain watch-only until capability-overlap or gate evidence makes an evaluation packet useful. Blocked candidates should not receive eval packets until their manual architecture, security, wallet/KYC, public-action, or service gates are scoped.

## Boundary

- Dependency installs: `0`
- Untrusted tools run: `0`
- Runtime starts: `0`
- Worker starts: `0`
- Browser sessions: `0`
- Model/API/MCP calls: `false`
- Accounts, wallets, payments, trades, submissions, public actions: `0`
- Service requests approved, assigned, or started: `0`
- External side effects: `false`
