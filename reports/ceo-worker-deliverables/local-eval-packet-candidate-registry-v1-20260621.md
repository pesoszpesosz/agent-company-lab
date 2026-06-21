# Local Evaluation Packet - Candidate Registry V1

Generated local date: 2026-06-21
Lane: `ai_resources_lab`
Owner role: `local_evaluation_harness_builder`
Source queue: `E:\agent-company-lab\reports\ai-resources-candidate-evaluation-queue-v1-20260621.json`
Status: report-only packet

## Evaluation Contract

This packet evaluates the 12 queued candidate registry items using existing local evidence only. It proves readiness for local proof work, not adoption into live execution.

Allowed:

- Read existing local artifacts.
- Write report-only evaluation packets and scorecards.
- Specify deterministic local fixtures.
- Run trusted local validations only when no external dependency install, runtime start, browser, model/API, account, or public action is required.

Not allowed:

- Install dependencies or execute untrusted candidate repos.
- Start runtimes, workers, MCP servers, browsers, containers, queues, or background services.
- Call model APIs, MCP tools, external APIs, or live web endpoints.
- Create accounts, log in, accept terms, use credentials, touch KYC/tax/payment/wallet/trade flows.
- Publish, submit, message, claim bounties, apply to jobs, post listings, create PR comments, or perform public actions.

## Evidence Check

All 12 candidate queue items have existing local input evidence paths. No missing input evidence paths were found during this packet pass.

## Scoring Method

Total score: 100.

- Company fit: 20
- Local proofability: 20
- Risk containment: 20
- Overlap discipline: 15
- Measurable value: 15
- Reproducibility: 10

Decision thresholds:

- `promote_local_packet`: 85+ and no unresolved hard gate for report-only/local fixture work.
- `keep_and_harden`: 80-84 for current control-plane assets that need hardening before broader use.
- `adapt_or_merge`: 70-79 where existing owners or policies should absorb the candidate.
- `watch_reference`: 55-69 where the candidate is useful but not ready for local proof work.
- `park_or_reject`: under 55 or blocked beyond two work blocks.

## Candidate Results

| Rank | Candidate | Family | Score | Decision | First Local Proof |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `ceo_state_packet_v1` | control_plane_integrity | 92 | `promote_local_packet` | Integrity packet for CEO state coverage, stale links, gates, and raw-context exclusion. |
| 2 | `human_action_feed_v1` | human_gate_routing | 90 | `promote_local_packet` | Gate-separation review for human-required actions without approval apply. |
| 3 | `ai_resources_owner_acknowledgement_loop` | continuity_and_ownership | 91 | `promote_local_packet` | Stale-owner reducer fixture from request, monitor, and dispatch rows. |
| 4 | `pydantic_ai_testmodel_adapter` | local_prompt_and_worker_harness | 76 | `adapt_or_merge` | Fixture-only prompt/worker harness check from saved reports. |
| 5 | `worker_capability_class_registry_v1` | capability_overlap | 88 | `promote_local_packet` | Capability-overlap map for queued candidates and existing owners. |
| 6 | `playwright_foundation_adapter` | browser_worker_policy | 72 | `adapt_or_merge` | No-start browser policy contract checklist. |
| 7 | `langgraph_checkpoint_inbox_patterns` | checkpoint_and_interrupt_pattern | 73 | `adapt_or_merge` | Framework-agnostic checkpoint/inbox contract shape extraction. |
| 8 | `prompt_eval_safety_harness` | prompt_safety | 84 | `keep_and_harden` | Candidate-registry stop-gate prompt cases from local eval fixtures. |
| 9 | `promptbase_agent_skill_route` | money_route_local_proof | 71 | `adapt_or_merge` | Local approval rubric for saved PromptBase packets. |
| 10 | `upwork_ai_offer_matrix_route` | money_route_local_proof | 72 | `adapt_or_merge` | No-contact offer matrix from saved observations. |
| 11 | `arc_prize_2026_baseline_harness` | competition_local_proof | 70 | `adapt_or_merge` | Local toy-fixture baseline plan, no official data or submission. |
| 12 | `kalshi_public_data_worksheet` | paper_market_research | 70 | `adapt_or_merge` | Saved-row paper signal checker spec, no live market access. |

## Promotion Order

1. Promote local packets for `ceo_state_packet_v1`, `human_action_feed_v1`, `ai_resources_owner_acknowledgement_loop`, and `worker_capability_class_registry_v1`.
2. Harden `prompt_eval_safety_harness` by adding stop-gate cases for dependency installs, runtime starts, public actions, and payment/trading gates.
3. Adapt framework references into policy contracts only: `playwright_foundation_adapter`, `langgraph_checkpoint_inbox_patterns`, and `pydantic_ai_testmodel_adapter`.
4. Keep money routes local-only until approval packets exist: PromptBase, Upwork, ARC/Kaggle-style competitions, and Kalshi paper research.

## Candidate-Specific Gates

- `ceo_state_packet_v1`: no service request mutation, worker restart, thread message, or external API call.
- `human_action_feed_v1`: no account mutation, payment/wallet action, public action, or approval apply.
- `ai_resources_owner_acknowledgement_loop`: no thread message, worker restart, service request assignment, or external notification.
- `pydantic_ai_testmodel_adapter`: no model/API call, dependency install, runtime start, or credential use.
- `worker_capability_class_registry_v1`: no worker registration, worker start, runtime start, or service request assignment.
- `playwright_foundation_adapter`: no browser session start, dependency install, account login, or public action.
- `langgraph_checkpoint_inbox_patterns`: no dependency install, model/API call, runtime start, or worker start.
- `prompt_eval_safety_harness`: no model/API call, external API call, public action, or dependency install.
- `promptbase_agent_skill_route`: no marketplace account, payment/tax/payout flow, public listing, or submission.
- `upwork_ai_offer_matrix_route`: no account login, proposal/message, payment/tax/payout flow, or public action.
- `arc_prize_2026_baseline_harness`: no competition account, official data download, submission, paid compute, or model/API call.
- `kalshi_public_data_worksheet`: no live API call, account login, trade/order, deposit, withdrawal, payment, or signed request.

## Required Packet Outputs

The next concrete local proof step should write these report-only packets under `E:\agent-company-lab\reports\ai-resources-evals\`:

- `ceo-state-packet-v1-local-integrity-20260621.md`
- `human-action-feed-v1-gate-separation-20260621.md`
- `owner-acknowledgement-loop-local-fixture-20260621.md`
- `worker-capability-class-overlap-map-20260621.md`
- `candidate-registry-stop-gate-prompt-cases-20260621.md`

## Fast-Fail Rule

If any candidate cannot produce a useful local proof from existing files within two focused work blocks, mark it `watch_reference`, `park_or_reject`, or route it to an exact missing-input request. Do not compensate by installing tools, starting runtimes, opening browsers, or calling APIs.

## Zero Side-Effect Attestation

- Dependency installs: 0
- Runtime starts: 0
- Worker starts: 0
- Browser sessions started: 0
- Accounts created or modified: 0
- Wallets/payments touched: 0
- Trades/orders placed: 0
- Submissions/public actions: 0
- Model/API/MCP calls: 0
- External API calls: 0
- Service requests approved, assigned, or started: 0
- External side effects: false
