# AI Resources Candidate Evaluation Queue V1

Generated UTC: 2026-06-20T22:50:01Z
Local date: 2026-06-21
Lane: `ai_resources_lab`
Owner: `candidate-registry-curator-20260621`
Handoff owner: `local-evaluation-harness-builder-20260621`
Status: queued local-only, no execution
JSON mirror: `E:\agent-company-lab\reports\ai-resources-candidate-evaluation-queue-v1-20260621.json`
Source registry: `E:\agent-company-lab\reports\ai-resources-candidate-registry-v2-20260621.json`

## Queue Policy

Allowed now: read existing local artifacts, write local report-only evaluation packets, write deterministic parser or fixture specifications, and run trusted local validation against generated JSON or existing repo tests when no external dependency install is required.

Not allowed: dependency installs, untrusted candidate code execution, runtime starts, worker starts, MCP server starts, browser sessions, containers, background services, model/API/MCP calls, account/login/profile work, terms/KYC/tax/payment/wallet/trade flows, submissions, publications, bounty claims, job applications, listings, PR comments, messages, or public actions.

## Queue

| Rank | Candidate | Eval ID | Family | Proof Artifact |
| ---: | --- | --- | --- | --- |
| 1 | `ceo_state_packet_v1` | `eval-ceo-state-packet-v1-local-integrity-20260621` | control-plane integrity | `reports\ai-resources-evals\ceo-state-packet-v1-local-integrity-20260621.md` |
| 2 | `human_action_feed_v1` | `eval-human-action-feed-v1-gate-separation-20260621` | human gate routing | `reports\ai-resources-evals\human-action-feed-v1-gate-separation-20260621.md` |
| 3 | `ai_resources_owner_acknowledgement_loop` | `eval-ai-resources-owner-ack-loop-stale-owner-fixture-20260621` | continuity and ownership | `reports\ai-resources-evals\owner-acknowledgement-loop-local-fixture-20260621.md` |
| 4 | `pydantic_ai_testmodel_adapter` | `eval-pydantic-ai-testmodel-fixture-only-20260621` | local prompt and worker harness | `reports\ai-resources-evals\pydantic-ai-testmodel-fixture-only-20260621.md` |
| 5 | `worker_capability_class_registry_v1` | `eval-worker-capability-class-overlap-map-20260621` | capability overlap | `reports\ai-resources-evals\worker-capability-class-overlap-map-20260621.md` |
| 6 | `playwright_foundation_adapter` | `eval-playwright-browser-policy-contract-20260621` | browser worker policy | `reports\ai-resources-evals\playwright-browser-policy-contract-20260621.md` |
| 7 | `langgraph_checkpoint_inbox_patterns` | `eval-langgraph-checkpoint-contract-shape-20260621` | checkpoint and interrupt pattern | `reports\ai-resources-evals\langgraph-checkpoint-contract-shape-20260621.md` |
| 8 | `prompt_eval_safety_harness` | `eval-candidate-registry-stop-gate-prompt-cases-20260621` | prompt safety | `reports\ai-resources-evals\candidate-registry-stop-gate-prompt-cases-20260621.md` |
| 9 | `promptbase_agent_skill_route` | `eval-promptbase-approval-rubric-local-only-20260621` | money route local proof | `reports\ai-resources-evals\promptbase-approval-rubric-local-only-20260621.md` |
| 10 | `upwork_ai_offer_matrix_route` | `eval-upwork-ai-offer-matrix-no-contact-20260621` | money route local proof | `reports\ai-resources-evals\upwork-ai-offer-matrix-no-contact-20260621.md` |
| 11 | `arc_prize_2026_baseline_harness` | `eval-arc-prize-local-toy-baseline-20260621` | competition local proof | `reports\ai-resources-evals\arc-prize-local-toy-baseline-20260621.md` |
| 12 | `kalshi_public_data_worksheet` | `eval-kalshi-saved-row-paper-signal-20260621` | paper market research | `reports\ai-resources-evals\kalshi-saved-row-paper-signal-20260621.md` |

## Recommended Order

1. Control-plane assets first.
2. Local eval harnesses second.
3. External repo contract comparisons third.
4. Money-route local proofs fourth.

## Boundary

- Dependency installs: `0`
- Runtime starts: `0`
- Worker starts: `0`
- Browser sessions started: `0`
- Accounts created or modified: `0`
- Wallets/payments touched: `0`
- Trades/orders placed: `0`
- Submissions/public actions: `0`
- Model/API/MCP calls: `false`
- External API calls: `0`
- Service requests approved, assigned, or started: `0`
- External side effects: `false`
