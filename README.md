# Agent Company Lab

Created: 2026-06-14

Purpose: design and build a separate infrastructure layer for parallel AI-agent work across online money-making paths. This lab is intentionally separate from `E:\profit-edge-lab`; it imports lessons from that system but does not own its RustChain/Charles/GitHub payout lane.

## Current Scope

- Study current open-source agent infrastructure, orchestration frameworks, workflow engines, browser workers, observability tools, and protocol standards.
- Design a company-style operating model: CEO, departments, managers, seekers, execution agents, service workers, approval gates, ledgers, and feedback loops.
- Build durable artifacts that later agents can use: source indexes, architecture notes, lane taxonomy, role registry, and implementation backlog.

## Hard Boundaries

- No legal, KYC, tax, billing, account-contract, or payment-onboarding commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or private-key/seed storage from autonomous agents.
- No public posting, bounty claims, PR comments, wallet-address comments, or marketplace submissions unless the route and owner are explicitly assigned.
- Agents can research, draft, test locally, and prepare action packets. Side-effect workers must log requests and approvals.

## Files

- `reports/agent-company-infra-research-20260614.md` - main research report.
- `reports/agent-company-deep-research-wave2-20260614.md` - source-backed wave-2 architecture synthesis across frameworks, workflows, protocols, observability, service departments, and lane sources.
- `reports/agent-company-deep-research-wave3-20260614.md` - source-backed wave-3 synthesis for service-request packet factories, durable workflows, human approvals, browser workers, and multi-agent coding workspaces.
- `reports/agent-company-money-path-wave4-20260614.md` - source-backed wave-4 expansion of online money paths, candidate lanes, human-only gates, and first proof tasks.
- `reports/agent-company-stack-wave5-20260614.md` - source-backed Wave-5 stack scan for agent runtimes, durable workflows, browser workers, protocols, and observability.
- `reports/agent-company-stack-wave6-20260614.md` - source-backed Wave-6 stack scan and decision to build approval-safe service execution plans before adding another top-level framework.
- `reports/agent-company-deep-research-wave7-20260615.md` - source-backed Wave-7 deep scan for agent runtimes, durable queues, browser workers, protocols, human UI, and observability.
- `reports/wave7-agent-company-operating-model-20260615.md` - Wave-7 operating model for CEO, departments, managers, seekers, gated service workers, reviewers, and approval boundaries.
- `reports/service-request-packet-factory-spec-20260614.md` - source-backed build spec for the catalog-backed service-request packet factory.
- `reports/service-request-packet-factory-acceptance-20260614.md` - acceptance report for the implemented `scaffold-service-request` packet factory.
- `reports/service-request-decision-packet-20260614.md` - CEO/CRO decision packet that ranks current `needs_review` service requests without approving or starting any service.
- `reports/wave4-manager-launch-plan-20260614.md` - focused copy-ready launch plan for the first three Wave-4 lane-manager chats.
- `reports/wave4-manager-thread-launch-run-20260614.md` - actual Wave-4 three-thread launch run with thread IDs, output directories, starter service requests, and boundaries.
- `data/curated-infra-repos-20260614.json` - GitHub metadata for curated infrastructure repos.
- `data/curated-infra-repos-20260614.csv` - compact repo table.
- `data/curated-infra-repos-wave3-20260614.json` - wave-3 GitHub metadata for durable workflow, approval, browser, protocol, and coding-agent orchestration repos.
- `data/curated-infra-repos-wave3-20260614.csv` - compact wave-3 repo table.
- `data/curated-infra-repos-wave6-20260614.json` - Wave-6 metadata snapshot for current agent runtimes, protocols, workflow engines, browser workers, and observability candidates.
- `data/curated-infra-repos-wave7-20260615.json` - Wave-7 metadata snapshot across agent runtimes, durable execution, browser workers, protocols, UI, observability, and messaging.
- `data/money-path-source-registry-wave4-20260614.json` - structured candidate-lane registry for AI/ML competitions, digital products, productized services, QA/usability gigs, AI-training gigs, affiliate programs, and recurring source discovery.
- `data/github-search-*.json` - raw GitHub search snapshots.
- `architecture/role-registry-draft.json` - draft company roles and responsibilities.
- `architecture/lane-taxonomy-draft.json` - draft money-path taxonomy and gates.
- `architecture/source-specs-draft.json` - per-lane source registry, refresh commands, outputs, and risk gates.
- `architecture/service-catalog-draft.json` - service-worker bureau catalog for account, wallet, browser, public-action, legal/KYC/payment, trading, model/API, outreach, GitHub, security-report, secrets, and paid data/API gates.
- `architecture/work-packet-v1.schema.json` - runtime-agnostic work packet schema for future worker adapters.
- `architecture/service-request-execution-plan-v1.schema.json` - approval-safe service execution plan schema for exact worker instructions without granting approval.
- `architecture/source-freshness-scheduler-v1.schema.json` - local source freshness scheduler schema for planning checks without executing gated browser/API/account/public/payment work.
- `architecture/service-worker-request-v1.schema.json` - reusable gated service-worker request schema for browser, account, wallet, legal/payment, public-submission, model/API, and local runtime workers.
- `architecture/durable-service-worker-queue-adapter-v1.schema.json` - local durable queue adapter manifest schema for mapping service-worker packets to SQLite, DBOS, Hatchet, and Temporal-style queues without executing them.
- `notes/research-log-20260614.md` - chronological research notes.
- `tools/agent_company.py` - Phase 0 SQLite control-plane CLI.
- `tools/typed_worker_runtime.py` - Pydantic-only local worker contract prototype.
- `tools/runtime_adapter_harness.py` - local-only deterministic runtime-adapter harness for `work_packet.v1` packets.
- `tools/pydantic_ai_worker_eval.py` - offline Pydantic AI `TestModel` eval.
- `tools/pydantic_ai_model_adapter.py` - gated Pydantic AI adapter shell; real mode requires approved service request.
- `prompts/lane-manager-startup-prompt-v1.txt` - canonical v1 prompt template for separate lane-manager chats.
- `prompts/lane-manager-startup-prompt-v2.txt` - active v2 manager prompt template with explicit approved-service-request language.
- `evals/manager-prompt-safety-cases-20260614.json` - safety eval cases for manager prompts.
- `evals/manager-prompt-stop-gates-20260614.json` - default stop-gate list for manager prompts.
- `evals/service-request-intake-valid-real-money-trade-20260614.json` - no-action structured intake fixture for service-request validator testing.
- `architecture/openinference-trace-metadata-v1.json` - OpenInference-style metadata convention for `trace_events.metadata_json`.
- `tools/monitor_lane_managers.py` - CEO monitor for launched lane-manager startup readiness.
- `state/agent_company.sqlite` - seeded control-plane database.
- `reports/control-plane-status-latest.md` - generated lane/task/service-request dashboard.
- `reports/profit-edge-import-latest.md` - read-only import report from `E:\profit-edge-lab`.
- `reports/ceo-review-latest.md` - generated executive lane scoreboard, launch order, and service gate review.
- `reports/ceo-lane-startup-digest-20260614.md` - CEO digest of completed lane-manager startup memos and missing prediction-lane startup record.
- `reports/source-research-refresh-20260614.md` - current official-doc/GitHub refresh for agent infrastructure.
- `reports/source-specs-latest.md` - generated source-spec registry report.
- `reports/service-catalog-latest.md` - generated service-worker bureau catalog and operating rules.
- `reports/service-request-intake-validator-20260614.md` - verification report for catalog-backed service request intake validation.
- `reports/prediction-manager-startup-recovery-20260614.md` - platform recovery memo for the interrupted prediction manager startup.
- `reports/prediction-manager-relaunch-20260614.md` - platform relaunch memo for the replacement prediction manager thread.
- `reports/prediction-manager-startup-recovered-20260614.md` - verified recovery-completion memo after prediction startup records landed.
- `reports/manager-packets/` - generated per-lane manager packets and index for future worker chats.
- `reports/lane-manager-thread-launch-manifest-latest.md` - generated launch queue and copy-ready prompts for separate lane-manager Codex chats.
- `reports/lane-manager-thread-launch-manifest-latest.json` - machine-readable version of the lane-manager launch queue.
- `reports/lane-manager-thread-launch-run-20260614.md` - actual seven-thread launch run with thread IDs, titles, output directories, and common boundaries.
- `reports/lane-manager-thread-launch-run-20260614.json` - machine-readable launch-run record.
- `reports/lane-manager-monitor-latest.md` - current CEO monitor for launched lane managers.
- `reports/lane-manager-monitor-latest.json` - machine-readable monitor state.
- `reports/trace-events-latest.md` - generated local trace/audit report.
- `reports/artifacts-latest.md` - generated artifact inventory with filters/counts.
- `reports/artifacts-control-plane-code-latest.md` - filtered artifact report for control-plane code artifacts.
- `reports/prompt-eval-review-latest.md` - generated prompt template/version, eval dataset/run, and review registry report.
- `reports/prompt-evals/` - prompt evaluation artifacts.
- `reports/openinference-trace-conventions-20260614.md` - human-readable trace metadata convention.
- `reports/runtime-adapters/runtime-adapter-harness-20260614.md` - deterministic adapter harness run; 12/12 checks passed with `api_calls=false` and no external side effects.
- `reports/runtime-adapters/runtime-adapter-harness-20260614.json` - machine-readable adapter harness run.
- `reports/runtime-adapters/packet-results/` - per-adapter/per-packet JSON result files written by the runtime harness.
- `reports/runtime-adapters/lane-packets/digital-products-agent-skill-starter-kit-marketplace-readiness-20260614.json` - first real money-lane `work_packet.v1` packet, local-only.
- `reports/runtime-adapters/lane-packet-runs/digital-products-agent-skill-starter-kit-marketplace-readiness/` - adapter run for the real digital-products lane packet.
- `reports/runtime-adapters/lane-packets/money-source-proof-queue-routing-20260614.json` - real money-source `work_packet.v1` packet for the 16-row proof queue, local-only.
- `reports/runtime-adapters/lane-packet-runs/money-source-proof-queue-routing/` - adapter run for the real money-source lane packet.
- `reports/money-source-discovery/msd-001-local-routing-decision-20260614.md` - local routing decision selecting `MSD-001` as the only currently unblocked money-source queue item and parking `MSD-002` through `MSD-016`.
- `reports/money-source-discovery/blocked-row-action-queue-20260614.json` - machine-readable action queue for `MSD-002` through `MSD-016`, with first required gates, prohibited actions, and safe local next actions.
- `reports/money-source-discovery/blocked-row-action-queue-20260614.md` - human-readable version of the blocked-row action queue.
- `reports/digital-products-templates-plugins/marketplace-readiness-matrix-20260614.json` - machine-readable marketplace readiness matrix for Agent Skill Starter Kit v0 across `MSD-008` through `MSD-012`.
- `reports/digital-products-templates-plugins/marketplace-readiness-matrix-20260614.md` - human-readable marketplace readiness matrix and route ranking.
- `reports/digital-products-templates-plugins/direct-download-listing-readiness-packet-20260614.json` - machine-readable direct-download listing readiness packet for Agent Skill Starter Kit v0.
- `reports/digital-products-templates-plugins/direct-download-listing-readiness-packet-20260614.md` - human-readable direct-download listing readiness packet with draft listing copy, asset readiness, and review gates.
- `reports/digital-products-templates-plugins/agent-skill-starter-kit-package-manifest-20260614.json` - internal review manifest for Agent Skill Starter Kit v0 with file sizes and SHA-256 hashes.
- `reports/digital-products-templates-plugins/agent-skill-starter-kit-package-checklist-20260614.md` - internal package checklist for Agent Skill Starter Kit v0.
- `requests/service-requests/req-next-wave-digital-marketplace-browser-readonly-20260614/execution-plan-v1.json` - machine-readable read-only execution plan for the digital marketplace service request; not an approval.
- `requests/service-requests/req-next-wave-digital-marketplace-browser-readonly-20260614/execution-plan-v1.md` - human-readable read-only execution plan for the digital marketplace service request; not an approval.
- `reports/source-freshness-scheduler-plan-20260615.json` - machine-readable local scheduler plan for source freshness checks and blocked gate routing.
- `reports/source-freshness-scheduler-plan-20260615.md` - human-readable local scheduler plan for source freshness checks and blocked gate routing.
- `reports/service-worker-request-queue-latest.md` - generated first-class service-worker queue grouped by worker type and risk gate.
- `reports/service-worker-request-queue-latest.json` - machine-readable service-worker queue.
- `reports/service-worker-request-queue-validation-latest.json` - validation mirror for the service-worker queue.
- `reports/service-worker-dequeue-plan-latest.md` - deterministic local dequeue dry-run over service-worker packets; writes result placeholders without starting workers.
- `reports/service-worker-dequeue-plan-latest.json` - machine-readable service-worker dequeue dry-run plan.
- `reports/service-worker-dequeue-plan-validation-latest.json` - validation mirror for the service-worker dequeue dry-run.
- `reports/service-worker-dequeue-results/` - per-packet local dequeue result placeholders.
- `reports/service-worker-execution-readiness-latest.md` - read-only verifier for approval scope, approval records, packet validity, and worker assignment before service-worker starts.
- `reports/service-worker-execution-readiness-latest.json` - machine-readable execution-readiness report.
- `reports/service-worker-execution-readiness-validation-latest.json` - validation mirror for the execution-readiness verifier.
- `reports/service-worker-approval-scope-diff-latest.md` - read-only diff of approval-scope text against service-worker packet boundaries.
- `reports/service-worker-approval-scope-diff-latest.json` - machine-readable approval-scope diff report.
- `reports/service-worker-approval-scope-diff-validation-latest.json` - validation mirror for the approval-scope diff.
- `reports/service-worker-exact-scope-templates-latest.md` - draft-only exact-scope templates for human/CRO review before service-worker approval decisions.
- `reports/service-worker-exact-scope-templates-latest.json` - machine-readable exact-scope template report.
- `reports/service-worker-exact-scope-templates-validation-latest.json` - validation mirror for the exact-scope template report.
- `reports/service-worker-cro-approval-review-latest.md` - local CRO approval review queue with draft approve/reject command previews; not an approval.
- `reports/service-worker-cro-approval-review-latest.json` - machine-readable CRO approval review queue.
- `reports/service-worker-cro-approval-review-validation-latest.json` - validation mirror for the CRO approval review queue.
- `reports/service-worker-assignment-plan-latest.md` - local service-worker assignment plan mapping queued requests to worker roles and pools; not an assignment.
- `reports/service-worker-assignment-plan-latest.json` - machine-readable service-worker assignment plan.
- `reports/service-worker-assignment-plan-validation-latest.json` - validation mirror for the service-worker assignment plan.
- `reports/service-worker-pool-registry-latest.md` - local registry of required service-worker pools, capabilities, current demand, and registration gaps; not worker registration.
- `reports/service-worker-pool-registry-latest.json` - machine-readable service-worker pool registry.
- `reports/service-worker-pool-registry-validation-latest.json` - validation mirror for the service-worker pool registry.
- `reports/service-worker-pool-registration-plan-latest.md` - manual registration packets for missing service-worker pools; not worker registration.
- `reports/service-worker-pool-registration-plan-latest.json` - machine-readable service-worker pool registration plan.
- `reports/service-worker-pool-registration-plan-validation-latest.json` - validation mirror for the service-worker pool registration plan.
- `reports/service-worker-gate-map-latest.md` - CEO/CRO gate map showing each service-worker request's current blocking gate; not approval, registration, assignment, or start.
- `reports/service-worker-gate-map-latest.json` - machine-readable service-worker gate map.
- `reports/service-worker-gate-map-validation-latest.json` - validation mirror for the service-worker gate map.
- `reports/service-worker-chain-integrity-latest.md` - local integrity audit over the service-worker validation chain and SQLite control-plane counters; not approval, registration, assignment, update, or start.
- `reports/service-worker-chain-integrity-latest.json` - machine-readable service-worker chain integrity report.
- `reports/service-worker-chain-integrity-validation-latest.json` - validation mirror for the service-worker chain integrity report.
- `reports/service-worker-human-decision-packets-latest.md` - local human/CRO decision packet index for reviewable service-worker requests; not approval, registration, assignment, update, or start.
- `reports/service-worker-human-decision-packets-latest.json` - machine-readable human/CRO decision packet index.
- `reports/service-worker-human-decision-packets-validation-latest.json` - validation mirror for the human decision packet index.
- `reports/service-worker-human-decision-packets/` - per-request Markdown/JSON decision packets with manual approve/reject previews.
- `reports/service-worker-post-decision-simulation-latest.md` - report-only simulation of manual approve/reject consequences for human decision packets.
- `reports/service-worker-post-decision-simulation-latest.json` - machine-readable post-decision simulation report.
- `reports/service-worker-post-decision-simulation-validation-latest.json` - validation mirror for the post-decision simulation.
- `reports/service-worker-post-decision-refresh-plan-latest.md` - report-only local refresh checklist for after a human/CRO approve or reject decision.
- `reports/service-worker-post-decision-refresh-plan-latest.json` - machine-readable post-decision refresh plan.
- `reports/service-worker-post-decision-refresh-plan-validation-latest.json` - validation mirror for the post-decision refresh plan.
- `reports/service-worker-decision-drift-guard-latest.md` - report-only drift guard comparing human decision packets to live service-request state.
- `reports/service-worker-decision-drift-guard-latest.json` - machine-readable service-worker decision drift report.
- `reports/service-worker-decision-drift-guard-validation-latest.json` - validation mirror for the decision drift guard.
- `reports/service-worker-decision-command-safety-latest.md` - report-only review of approve/reject command previews for direct-run safety.
- `reports/service-worker-decision-command-safety-latest.json` - machine-readable service-worker decision command safety report.
- `reports/service-worker-decision-command-safety-validation-latest.json` - validation mirror for the decision command safety report.
- `reports/service-worker-decision-authority-matrix-latest.md` - report-only authority matrix for pending human/CRO service-worker decisions.
- `reports/service-worker-decision-authority-matrix-latest.json` - machine-readable service-worker decision authority matrix.
- `reports/service-worker-decision-authority-matrix-validation-latest.json` - validation mirror for the decision authority matrix.
- `reports/service-worker-decision-preflight-latest.md` - report-only rollup of drift, command safety, and authority checks before human decision review.
- `reports/service-worker-decision-preflight-latest.json` - machine-readable service-worker decision preflight report.
- `reports/service-worker-decision-preflight-validation-latest.json` - validation mirror for the decision preflight report.
- `reports/durable-queue-adapters/durable-service-worker-queue-adapter-manifests-20260615.md` - local durable queue adapter review for SQLite, DBOS, Hatchet, and Temporal-style service-worker routing.
- `reports/durable-queue-adapters/durable-service-worker-queue-adapter-manifests-20260615.json` - machine-readable durable queue adapter manifest set.
- `reports/durable-queue-adapters/durable-service-worker-queue-adapter-validation-20260615.json` - validation mirror for the durable queue adapter manifest set.
- `reports/digital-products-templates-plugins/digital-marketplace-readonly-approval-review-20260615.json` - machine-readable approval review packet for the digital marketplace browser-read-only request; not an approval.
- `reports/digital-products-templates-plugins/digital-marketplace-readonly-approval-review-20260615.md` - human-readable approval review packet with draft approve/reject commands for user/CRO decision; not an approval.
- `reports/runtime-adapters/runtime-adapter-graduation-20260614.md` - review of all four local runtime adapters, graduation order, and next hardening target.
- `reports/worker-runtime/` - typed worker prototype outputs for lane proposal and boundary tests.
- `.venv-runtime/` - isolated Python environment for runtime experiments; currently contains `pydantic-ai==1.107.0`.

## Current Ownership

- This recovered thread owns only `platform_engineering`.
- The existing GitHub payout lane `submitted_bounty_payouts` is explicitly not owned by this thread.

## Useful Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-evidence --limit 25
python E:\agent-company-lab\tools\agent_company.py import-profit-edge --source-root E:\profit-edge-lab --ledger-tail 40
python E:\agent-company-lab\tools\agent_company.py write-dashboard
python E:\agent-company-lab\tools\agent_company.py write-ceo-review
python E:\agent-company-lab\tools\agent_company.py seed-source-specs
python E:\agent-company-lab\tools\agent_company.py list-source-specs
python E:\agent-company-lab\tools\agent_company.py write-source-specs-report
python E:\agent-company-lab\tools\agent_company.py seed-service-catalog
python E:\agent-company-lab\tools\agent_company.py list-service-catalog --limit 25
python E:\agent-company-lab\tools\agent_company.py write-service-catalog-report
python E:\agent-company-lab\tools\agent_company.py write-service-request-review
python E:\agent-company-lab\tools\agent_company.py write-service-worker-queue
python E:\agent-company-lab\tools\agent_company.py write-service-worker-dequeue-plan
python E:\agent-company-lab\tools\agent_company.py write-service-worker-execution-readiness
python E:\agent-company-lab\tools\agent_company.py write-service-worker-scope-diff
python E:\agent-company-lab\tools\agent_company.py write-service-worker-scope-templates
python E:\agent-company-lab\tools\agent_company.py write-service-worker-approval-review
python E:\agent-company-lab\tools\agent_company.py write-service-worker-assignment-plan
python E:\agent-company-lab\tools\agent_company.py write-service-worker-pool-registry
python E:\agent-company-lab\tools\agent_company.py write-service-worker-pool-registration-plan
python E:\agent-company-lab\tools\agent_company.py write-service-worker-gate-map
python E:\agent-company-lab\tools\agent_company.py write-service-worker-chain-integrity
python E:\agent-company-lab\tools\agent_company.py write-service-worker-human-decision-packets
python E:\agent-company-lab\tools\agent_company.py write-service-worker-post-decision-simulation
python E:\agent-company-lab\tools\agent_company.py write-service-worker-post-decision-refresh-plan
python E:\agent-company-lab\tools\agent_company.py write-service-worker-decision-drift-guard
python E:\agent-company-lab\tools\agent_company.py write-service-worker-decision-command-safety
python E:\agent-company-lab\tools\agent_company.py write-service-worker-decision-authority-matrix
python E:\agent-company-lab\tools\agent_company.py write-service-worker-decision-preflight
python E:\agent-company-lab\tools\agent_company.py validate-service-request --request-id REQ
python E:\agent-company-lab\tools\agent_company.py write-manager-packets
python E:\agent-company-lab\tools\agent_company.py write-lane-thread-manifest
python E:\agent-company-lab\tools\agent_company.py record-trace-event --trace-id TRACE --event-type EVENT --summary "What happened"
python E:\agent-company-lab\tools\agent_company.py list-trace-events --limit 25
python E:\agent-company-lab\tools\agent_company.py write-trace-report
python E:\agent-company-lab\tools\agent_company.py list-artifacts --lane-id platform_engineering --limit 25
python E:\agent-company-lab\tools\agent_company.py write-artifacts-report
python E:\agent-company-lab\tools\agent_company.py write-prompt-eval-report
python E:\agent-company-lab\tools\monitor_lane_managers.py
python E:\agent-company-lab\tools\monitor_manager_local_proofs.py
python E:\agent-company-lab\tools\agent_company.py record-prompt-template --template-id TEMPLATE --name "Name" --purpose "Purpose"
python E:\agent-company-lab\tools\agent_company.py record-prompt-version --prompt-version-id VERSION --template-id TEMPLATE --version-label "v1" --prompt-file PATH
python E:\agent-company-lab\tools\agent_company.py record-eval-dataset --dataset-id DATASET --name "Name" --purpose "Purpose" --cases-file PATH
python E:\agent-company-lab\tools\agent_company.py record-eval-run --eval-run-id RUN --dataset-id DATASET --runtime manual_static_coverage --status manual_static_pass
python E:\agent-company-lab\tools\eval_manager_prompt.py --prompt-file E:\agent-company-lab\prompts\lane-manager-startup-prompt-v2.txt --name manager-prompt-safety-local-eval-v2-YYYYMMDD
python E:\agent-company-lab\tools\typed_worker_runtime.py --lane-id prediction_market_research --worker-agent-id typed-worker-prototype
E:\agent-company-lab\.venv-runtime\Scripts\python.exe E:\agent-company-lab\tools\pydantic_ai_worker_eval.py
E:\agent-company-lab\.venv-runtime\Scripts\python.exe E:\agent-company-lab\tools\pydantic_ai_model_adapter.py --mode dry-run --lane-id prediction_market_research
python E:\agent-company-lab\tools\agent_company.py write-launch-packets
python E:\agent-company-lab\tools\agent_company.py approve-service-request --request-id REQ --approved-by USER_OR_AGENT --exact-scope "Exact allowed action"
python E:\agent-company-lab\tools\agent_company.py reject-service-request --request-id REQ --rejected-by USER_OR_AGENT --reason "Reason"
python E:\agent-company-lab\tools\agent_company.py assign-service-request --request-id REQ --agent-id AGENT
python E:\agent-company-lab\tools\agent_company.py start-service-request --request-id REQ --agent-id AGENT
python E:\agent-company-lab\tools\agent_company.py complete-service-request --request-id REQ --agent-id AGENT --artifact-path PATH --decision-note "What happened"
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id REQ --service-id SERVICE --request-type TYPE --intake-file PATH --risk-gate GATE --requested-action "Exact requested preparation"
python E:\agent-company-lab\tools\agent_company.py claim-lane --lane-id platform_engineering --agent-id recovered-profitable-edge-infra --thread-id 019ebbda-2002-7361-8597-03625189c3ff
python E:\agent-company-lab\tools\agent_company.py acquire-task --task-id task-phase0-control-plane-hardening-20260614 --agent-id recovered-profitable-edge-infra --lease-minutes 240
```

## Current Status

- Phase 0 control plane exists in SQLite and includes roles, departments, lanes, agents, tasks, service requests, approvals, artifacts, outcomes, lane evidence, source specs, trace events, prompt/eval/review tables, and service catalog entries.
- The read-only profit-edge import bridge imported 67 evidence rows from `E:\profit-edge-lab`: paid-code, security, prediction-market, web3, platform, and submitted-payout rows.
- The CEO review packet ranks next launch order as platform engineering, security private reports, prediction-market research, paid-code scouting, content/social, web3 terms scouting, lead generation, and local trading research.
- Current source research recommends keeping SQLite as the control plane, then evaluating Pydantic AI, Prefect/Temporal, agent-browser, and Langfuse/Phoenix as specialized layers after the local operating system is useful.
- Service-request lifecycle commands are implemented and tested: unapproved start is blocked; approved requests can be assigned, started, completed with artifacts; rejected requests preserve audit rows.
- Source-spec registry is seeded with 10 specs across 8 lanes. Each spec maps a lane to allowed read sources, refresh commands, expected outputs, cadence, and risk gates.
- Service-worker bureau catalog is seeded with 13 services: account registration, browser read-only, public action execution, wallet setup, wallet public-address response, legal/KYC/tax/payment review, real-money trade gate, model/API execution, outreach delivery, GitHub public action, security report submission, secrets/credentials handling, and data/API access.
- Catalog-backed service requests now support `service_id` and structured `intake_json`. Missing required intake fields block request creation and worker start; a fake `real_money_trade` validator test passed positive validation and was rejected as a no-action test row.
- Manager packets are generated for all 9 lanes under `reports/manager-packets/`. Each packet combines lane rules, source specs, service catalog entries, evidence, tasks, service requests, outcomes, startup commands, and a suggested manager prompt.
- Lane-manager thread launch manifest exists for 7 separate manager chats: security, prediction-market, paid-code, content/social, web3, lead-generation, and local-trading. `platform_engineering` stays with this coordinator and `submitted_bounty_payouts` stays with the parallel payout worker.
- Seven projectless Codex lane-manager chats have been created and titled from the launch manifest. Their IDs and boundaries are recorded in `reports/lane-manager-thread-launch-run-20260614.md`.
- CEO monitor exists for launched managers. Latest monitor state: all 7 launched lane startups are complete. `prediction_market_research` is now owned by replacement manager `lane-manager-prediction_market_research-relaunch-20260614` in thread `019ec637-a391-7693-915f-5ec5e5d82ee7`.
- CEO startup digest exists. Its earlier snapshot captured six completed lane startup memos and a missing prediction-lane startup record; the later recovery memo confirms that gap has been closed and the prediction lane is paper/data-only.
- Wave-2 deep research report recommends: SQLite now, Postgres later, Temporal for durable service workflows, NATS/Postgres queues for fanout, Pydantic AI first typed runtime, OpenAI Agents SDK later behind model/API gate, LangGraph as orchestration pattern, MCP first adapter, A2A/AG-UI later.
- Wave-3 deep research recommends a service-request packet factory before adding another runtime. The packet factory should generate catalog-backed JSON/Markdown case files so managers can request service workers without malformed intake or accidental side effects. It also recommends evaluating DBOS/Hatchet/Inngest/Trigger/Temporal only against that shared contract.
- Wave-4 money-path research adds seven candidate lane expansions: `money_source_discovery`, `ai_ml_competitions`, `digital_products_templates_plugins`, `productized_services_marketplaces`, `qa_usability_testing_gigs`, `ai_training_eval_gigs`, and `affiliate_partner_programs`. It ranks the first three as the best agent-suited next launches after the packet factory exists.
- Service-request packet factory spec is now written and registered in the control plane. It defines the `scaffold-service-request` CLI, generated `intake.json`/`packet.md`/`checklist.md`/`metadata.json` folder contract, validation rules, acceptance tests, and Wave-4 unlock sequence.
- Service-request packet factory is now implemented in `tools/agent_company.py`. Acceptance checks passed for incomplete intake without DB creation, complete intake with `needs_review` DB creation, mismatched service/request-type failure, and blocked unapproved start. Next platform step is controlled lane expansion for the first three Wave-4 lanes, then starter packet scaffolding.
- First Wave-4 lane expansion is now seeded in the control plane: `money_source_discovery`, `ai_ml_competitions`, and `digital_products_templates_plugins`. Each has a catalog-backed `browser_read_only_session` starter service request in `needs_review`; no browser or public action was performed.
- The lane-thread manifest now promotes those three Wave-4 lanes into the launch queue, and `reports/wave4-manager-launch-plan-20260614.md` extracts only those prompts so they can be launched without reusing the seven already-running managers. No new Codex threads were created by this update.
- Three Wave-4 projectless Codex manager chats have now been created and titled: `money_source_discovery` thread `019ec699-e02b-7ce1-a7a6-32afc857c254`, `ai_ml_competitions` thread `019ec69a-3c39-7de3-849b-f2d19a2d03da`, and `digital_products_templates_plugins` thread `019ec69a-9fe3-7530-b83e-ae404554bca7`. Startup records are pending until those managers claim lanes and write startup memos.
- CEO monitor now covers both the original seven-lane launch run and the Wave-4 three-lane launch run. Latest monitor state: 10 of 10 launched lane managers are `startup_complete`.
- Service-request review queue now exists at `reports/service-request-review-latest.md` with a machine-readable mirror at `reports/service-request-review-latest.json`. Latest queue state: 14 requests total, 11 `needs_review`, 2 `rejected`, 1 `complete`; report generation grants no approval and performs no external action.
- Manager local-proof queue now exists at `reports/manager-local-proof-queue-20260614.md`. It routes 10 `new` local-only proof tasks to the lane managers that already own the lanes, while excluding `submitted_bounty_payouts` and keeping platform engineering in monitor-only mode.
- Manager local-proof dispatch run now exists at `reports/manager-local-proof-dispatch-run-20260614.md` and `.json`. Ten lane-manager threads were sent exact task prompts with lane-specific stop gates; no external action was performed.
- Manager local-proof monitor now exists at `tools/monitor_manager_local_proofs.py`; latest report `reports/manager-local-proof-monitor-latest.md` shows all 10 dispatched proof tasks as `proof_complete` with artifacts and outcomes.
- CEO graduation queue now exists at `reports/manager-local-proof-graduation-queue-20260614.md`. It ranks completed local proofs and selects: digital product gated review, security gated review, money-source proof queue schema, web3 M1 source map, paid-code read-only verification, leadgen policy review, holds for AI/content, and parks for prediction/trading until stronger evidence.
- Next-wave routing run now exists at `reports/next-wave-routing-run-20260614.md` and `.json`. It created 4 local-only manager tasks and 5 new `needs_review` service packets; `reports/next-wave-local-proof-monitor-latest.md` now shows all 4 next-wave local tasks as `proof_complete`.
- Service-request review latest state: 14 requests total, 11 `needs_review`, 2 `rejected`, 1 `complete`. No service request is approved by report generation.
- Service-request decision packet exists at `reports/service-request-decision-packet-20260614.md`. It recommends three read-only approval candidates for user/CRO decision: digital marketplace browse, Google OSS VRP rules browse, and Algora Archestra bounty browse. It holds or rejects the remaining requests and grants no approval by itself.
- Wave-5 stack scan exists at `reports/agent-company-stack-wave5-20260614.md`. It recommends keeping SQLite as the company ledger, using frameworks as adapters, MCP before A2A, Browser Use only behind service gates, and Langfuse/Phoenix later after local trace value is proven.
- Wave-6 stack scan exists at `reports/agent-company-stack-wave6-20260614.md` with a machine-readable mirror at `data/curated-infra-repos-wave6-20260614.json`. It keeps SQLite as the source of truth and selects `service_request_execution_plan.v1` as the next local platform build.
- `service_request_execution_plan.v1` now exists at `architecture/service-request-execution-plan-v1.schema.json`. The first concrete plan is for `req-next-wave-digital-marketplace-browser-readonly-20260614` and limits any future approved worker to public Gumroad/Lemon Squeezy/PromptBase reading with no login, signup, seller onboarding, listing, upload, payment, legal/KYC/tax, public, or real-money action.
- `source_freshness_scheduler.v1` now exists at `architecture/source-freshness-scheduler-v1.schema.json`. The first scheduler plan is `reports/source-freshness-scheduler-plan-20260615.md` and classifies source checks as local-only, read-only GitHub metadata, or service-request-only without executing gated refreshes.
- Digital marketplace approval review packet now exists at `reports/digital-products-templates-plugins/digital-marketplace-readonly-approval-review-20260615.md`. It packages exact approve/reject command drafts for user/CRO decision but grants no approval and performs no browser action.
- Wave-7 deep research now exists at `reports/agent-company-deep-research-wave7-20260615.md` with a machine-readable repo dataset at `data/curated-infra-repos-wave7-20260615.json`. It keeps the SQLite ledger as CEO/control plane, treats frameworks as adapters, and selects gated `service_worker_request.v1` plus durable queue adapter tests as the next infrastructure path.
- `service_worker_request.v1` now exists at `architecture/service-worker-request-v1.schema.json`. All 14 service requests have been backfilled into per-request `service-worker-request-v1.json` packets, and `write-service-worker-queue` is now a first-class CLI command that generates latest Markdown/JSON/validation reports without approving or starting any request.
- `durable_service_worker_queue_adapter_manifest.v1` now exists at `architecture/durable-service-worker-queue-adapter-v1.schema.json`. It maps the 14 current service-worker packets across 4 local adapter contracts: SQLite queue, DBOS manifest, Hatchet manifest, and Temporal manifest. All 56 mapped routes are no-enqueue routes: 44 hold for approval, 4 terminal complete, and 8 terminal rejected across the adapter set; no dependency import, network, API/model, approval, start, browser, public, account, payment, wallet, legal/KYC/tax, security-testing, or real-money action was performed.
- `write-service-worker-dequeue-plan` is now implemented. It evaluates the 14 current service-worker packets, writes 28 local result-placeholder files under `reports/service-worker-dequeue-results/`, and records a dry-run plan with 11 hold-for-approval routes, 1 terminal-complete route, and 2 terminal-rejected routes. It approves 0 requests, starts 0 workers, updates 0 service requests, calls 0 APIs, and performs 0 external side effects.
- `write-service-worker-execution-readiness` is now implemented. It verifies service-worker packet validity, service request status, exact approval scope, latest approval row, approval expiry, packet/service status match, worker assignment, optional worker-id match, result path presence, and side-effect flags before any start. Current readiness is 0 of 14 startable: 11 blocked until approval, 1 terminal complete, and 2 terminal rejected; it grants no approval and performs no start or update.
- `write-service-worker-scope-diff` is now implemented. It compares service request approval-scope text and latest approval rows against packet allowed actions, prohibited actions, stop conditions, host boundaries, and side-effect denials. Current scope compatibility is 0 of 14: 9 missing exact scope, 2 have scope text without an approval record, 1 terminal complete, and 2 terminal rejected; it grants no approval and performs no start or update.
- `write-service-worker-scope-templates` is now implemented. It writes draft-only exact-scope templates for all 14 service-worker packets: 11 human-review drafts, 1 terminal-complete do-not-approve note, and 2 terminal-rejected do-not-approve notes. Templates grant no approval and perform no service request update, worker start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-approval-review` is now implemented. It combines service-worker packets, scope diffs, and scope templates into a local CRO review queue with 11 human/CRO review candidates, 3 terminal do-not-approve rows, and 11 approve/reject command previews that require manual review. It grants no approval and performs no service request update, worker start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-assignment-plan` is now implemented. It maps all 14 service-worker requests to lane managers, required worker capabilities, recommended worker roles, and proposed worker pools. Current state has 11 post-approval assignment previews but 0 assignable-now rows because approval, scope compatibility, and readiness checks are still missing; it assigns no worker and performs no update or start.
- `write-service-worker-pool-registry` is now implemented. It defines 7 required service-worker pools, maps current demand from the assignment plan, and shows all 7 dedicated pool registrations are still missing. The registry performs no worker registration, approval, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-pool-registration-plan` is now implemented. It writes 7 manual registration packets and 7 `register-agent` command previews for the missing service-worker pools, with boundaries and capabilities attached. It registers no worker and performs no approval, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-gate-map` is now implemented. It consolidates packet validity, CRO review, scope diff, readiness, assignment planning, pool registry, and pool registration state into one CEO/CRO gate board. Current state maps 11 requests to `human_cro_approval_required` and 3 terminal rows to `terminal_no_execution`; it performs no approval, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-chain-integrity` is now implemented. It checks 17 service-worker validation layers, including human decision packets, post-decision simulation, post-decision refresh plans, decision drift guard, decision command safety, decision authority matrix, and decision preflight, plus SQLite task/service/artifact/trace/agent counters. Latest integrity state passes with 0 failures, 14 service requests, 11 `needs_review`, 2 `rejected`, 1 `complete`, 0 ready assignments, 0 approvals, 0 registrations, 0 assignments, 0 updates, 0 worker starts, 0 API calls, and 0 external side effects.
- `write-service-worker-human-decision-packets` is now implemented. It packages the 11 human/CRO approval candidates into per-request Markdown/JSON decision packets with approve/reject command previews, exact-scope drafts, precondition checks, and gate/pool context. It performs no approval, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-post-decision-simulation` is now implemented. It simulates the manual approve and reject branches for the 11 human decision packets, showing that approval would only clear the human/CRO gate while scope refresh, pool registration, assignment, readiness, and worker start remain separate later gates. It performs no approval, rejection, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-post-decision-refresh-plan` is now implemented. It converts the 11 post-decision simulations into approve/reject refresh checklists with 99 command previews for local report regeneration only. It performs no approval, rejection, refresh execution, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-decision-drift-guard` is now implemented. It compares the 11 human decision packets with current SQLite service-request state and flags stale packets after status, approval/rejection, assignment, start, completion, or update drift. Current drift state is 11 current packets and 0 stale packets; it performs no recovery command execution, approval, rejection, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-decision-command-safety` is now implemented. It reviews the 11 approve and 11 reject command previews from human decision packets, marks approve commands as not directly runnable while exact-scope placeholders remain, and requires manual review for every decision command. It performs no approval, rejection, command execution, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-decision-authority-matrix` is now implemented. It maps the 11 pending human decision packets to required authority routes: 11 require CRO review, 4 require the human user, 1 requires CEO/platform authority, and 1 requires reputation review. It grants no authority and performs no approval, rejection, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- `write-service-worker-decision-preflight` is now implemented. It rolls up decision drift, command safety, and authority matrix state for the 11 pending human decision packets. Current state marks all 11 ready for human review while still allowing 0 execution, 0 assignment, and 0 worker starts. It performs no authority grant, approval, rejection, registration, assignment, update, start, API call, browser action, public action, payment, trade, submission, or external side effect.
- Runtime-agnostic `work_packet.v1` schema and adapter harness now exist. Latest harness result: 12 of 12 checks passed across `typed_worker_runtime_local_adapter`, `pydantic_ai_testmodel_local_adapter`, `openai_agents_sandbox_manifest_adapter`, and `langgraph_static_graph_adapter`; no API calls or external side effects were performed. All four harness adapters now have concrete local behavior for safe packets and refuse or route gated packets to stop paths before external execution.
- Runtime adapter graduation report exists at `reports/runtime-adapters/runtime-adapter-graduation-20260614.md`. It ranks next hardening as: per-packet result writer first, then typed-worker per-packet output, Pydantic AI per-packet eval paths, LangGraph standalone graph artifacts, and OpenAI Agents only as a static manifest until model/API service approval exists.
- Per-packet adapter result writer is implemented in `tools/runtime_adapter_harness.py`. Latest harness run wrote 12 parseable JSON result files under `reports/runtime-adapters/packet-results/` and linked them from the aggregate Markdown/JSON reports.
- First real lane packet run is complete for `digital_products_templates_plugins`: `packet-digital-products-agent-skill-starter-kit-marketplace-readiness` passed 4 of 4 adapters, wrote 4 parseable result files, and kept marketplace/browser/legal/payment/public/real-money actions blocked.
- Second real lane packet run is complete for `money_source_discovery`: `packet-money-source-proof-queue-routing` passed 4 of 4 adapters, wrote 4 parseable result files, and kept browser/current-source/API/account/public/payment/legal/real-money actions blocked.
- `MSD-001` local routing decision is complete at `reports/money-source-discovery/msd-001-local-routing-decision-20260614.md`. It selects the local control row as the only currently actionable money-source queue item and keeps `MSD-002` through `MSD-016` parked until browser/current-source or other service gates are approved.
- Blocked-row action queue is complete at `reports/money-source-discovery/blocked-row-action-queue-20260614.json` and `.md`. It routes all 15 parked money-source rows to explicit first gates and safe local next actions; 0 rows are ready for external execution.
- Marketplace readiness matrix is complete at `reports/digital-products-templates-plugins/marketplace-readiness-matrix-20260614.json` and `.md`. It ranks `MSD-008` and `MSD-009` as the best direct-download route family for the existing Agent Skill Starter Kit v0 after browser/legal/payment gates, keeps `MSD-010` conditional, and holds `MSD-011`/`MSD-012` for v0.
- Direct-download listing readiness packet is complete at `reports/digital-products-templates-plugins/direct-download-listing-readiness-packet-20260614.json` and `.md`. It packages reusable draft listing copy, asset readiness, review questions, and hard gates for `MSD-008`/`MSD-009`; 0 routes are public-listing ready.
- Internal package manifest/checklist is complete at `reports/digital-products-templates-plugins/agent-skill-starter-kit-package-manifest-20260614.json` and `reports/digital-products-templates-plugins/agent-skill-starter-kit-package-checklist-20260614.md`. It records 12 files, 21,670 bytes, SHA-256 hashes, no zip, and no public listing readiness.
- Prompt/eval/review registry exists with 1 lane-manager prompt template, 2 prompt versions, 1 safety dataset, and 2 eval runs. Active v2 passed the deterministic local static evaluator with score `1.0` across 6 safety cases.
- OpenInference-style trace metadata convention exists for future `trace_events.metadata_json` use. New structured events should include `span_kind`, `runtime`, and `api_calls`.
- Trace-event storage exists in SQLite and `reports/trace-events-latest.md` records the latest trace window from 121 total trace events, including Wave-7 research, service-worker request schema/backfill, the first-class service-worker queue/dequeue/readiness/scope-diff/scope-template/CRO-review/assignment-plan/pool-registry/pool-registration/gate-map/chain-integrity/human-decision-packets/post-decision-simulation/post-decision-refresh-plan/decision-drift-guard/decision-command-safety/decision-authority-matrix/decision-preflight CLI commands, the doc-refresh trace, and durable queue adapter manifests.
- Artifact inventory commands are implemented and verified: list by lane/task/kind/text, generate full artifact inventory, and generate filtered artifact reports. The latest full inventory contains 327 artifacts.
- Typed worker-runtime prototype exists in `tools/typed_worker_runtime.py`. It uses Pydantic schemas to validate lane context and produce local proposal artifacts; prediction-market output is read-only, and submitted-payout output returns `no_action_read_only`.
- Pydantic AI isolated eval passed with `pydantic-ai==1.107.0` using `TestModel` and `api_calls=false`. The next model-backed adapter must be behind a service request with provider, model, max cost, allowed lanes, and output artifact scope.
- Gated Pydantic AI adapter shell exists. Dry-run writes local artifacts; real mode refuses while `req-pydantic-ai-model-backed-adapter-20260614` is `needs_review`.
- `submitted_bounty_payouts` evidence is imported only for visibility. The parallel payout-monitoring worker owns that lane.


