# Manager Packet - platform_engineering

Generated UTC: 2026-06-21T13:02:27Z
Department: Platform Engineering
Lane status: active
Current owner: `recovered-profitable-edge-infra`

## Manager Directive

Own only the `platform_engineering` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane.

## Recommended Next Task

Use manager packets to launch separate lane-manager chats; keep real model/API execution behind the pending service request.

## CEO Recommendation

Finish active platform task, then promote separate lane-manager launches from manager packets.

## Allowed Worker Types

- control_plane_builder
- schema_designer
- observability_integrator
- duplication_guardian

## Example Work

- agent registry
- lane ownership
- task leases
- service request queue
- artifact registry
- trace store

## Promotion Gates

- prevents duplicate lane ownership
- records service requests
- keeps artifacts traceable
- does not own money execution lanes

## Required Service Workers

- observability_worker
- chief_risk_officer

## Service Bureau Catalog

Use these request types when this lane needs registration, browser, wallet, public action, outreach, trading, model/API, data/API, security-report, payment/legal, or credential support. The catalog defines intake and hard stops; it does not approve the action.

| Status | Type | Service | Owner Role | Purpose |
| --- | --- | --- | --- | --- |
| available | account_registration | `account_registration_intake` | `account_registration_worker` | Prepare a local registration packet for a venue without creating the account or accepting terms. |
| available | browser_research | `browser_read_only_session` | `browser_action_worker` | Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings. |
| available | data_purchase_api_access | `data_purchase_api_access_gate` | `chief_risk_officer` | Review paid APIs, premium data, scraped data, or restricted sources before a lane depends on them. |
| gated | github_public_action | `github_public_action_gate` | `reputation_review_worker` | Review PRs, issue comments, bounty claims, advisory comments, and maintainer-facing GitHub actions before public execution. |
| available | legal_kyc_tax_payment | `legal_kyc_tax_payment_gate` | `chief_risk_officer` | Summarize legal, KYC, tax, billing, payment, and account-contract obligations before the user decides. |
| available | model_api_execution | `model_api_execution_gate` | `observability_worker` | Approve and observe real model/API executions after dry-runs pass and cost/data scope is explicit. |
| available | outreach_delivery | `outreach_delivery_gate` | `reputation_review_worker` | Review and gate outbound email, DM, proposal, marketplace, or form-contact actions for non-spam and brand safety. |
| gated | public_action_execution | `public_action_execution` | `browser_action_worker` | Execute one exact approved public action, such as a reply, post, PR comment, bounty claim, proposal submission, or form submission. |
| available | real_money_trade | `real_money_trade_gate` | `chief_risk_officer` | Evaluate whether a paper-only market or trading hypothesis is even eligible for real-money consideration. |
| available | secrets_credentials_handling | `secrets_credentials_handling_gate` | `chief_risk_officer` | Define how a task can use credentials, tokens, API keys, private files, cookies, or session state without leaking or storing sensitive data. |
| available | security_report_submission | `security_report_submission_gate` | `chief_risk_officer` | Gate private vulnerability reports, advisory submissions, and program contacts after local-only proof work. |
| gated | wallet_public_address_or_payment_reply | `wallet_public_address_response` | `wallet_ops_worker` | Prepare or verify the exact public payment-address response for payout collection after user approval. |
| available | wallet_setup | `wallet_setup_packet` | `wallet_ops_worker` | Prepare wallet requirements, network/token details, custody choices, and user action checklist without controlling keys or funds. |

## Forbidden Direct Side Effects

These require a scoped service request and approval before any execution:
- local filesystem writes
- local SQLite schema changes
- local scripts

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Source Specs

| Spec | Type | Cadence | Gate | Refresh | Outputs |
| --- | --- | --- | --- | --- | --- |
| `platform_infra_repo_metadata` - Agent Infrastructure GitHub Metadata | github_metadata | weekly_or_before_architecture_choice | read_only_github_metadata | gh repo view <repo> --json nameWithOwner,description,stargazerCount,forkCount,primaryLanguage,licenseInfo,url,updatedAt,latestRelease | E:\agent-company-lab\data\curated-infra-repos-refresh-YYYYMMDD.json; E:\agent-company-lab\data\curated-infra-repos-refresh-YYYYMMDD.csv |
| `platform_official_docs_refresh` - Official Agent Infrastructure Docs | web_docs | weekly_or_before_framework_commitment | read_only_web_research | Use web research and save citations into a dated source-refresh report. | E:\agent-company-lab\reports\source-research-refresh-YYYYMMDD.md |
| `platform_profit_edge_daily_queue` - Profit Edge Daily Queue Snapshot | local_markdown | on_demand_before_ceo_review | read_only_local_import_no_execution_lane_ownership | powershell -ExecutionPolicy Bypass -File E:\profit-edge-lab\scripts\Build-DailyActionQueue.ps1 | E:\agent-company-lab\reports\profit-edge-import-latest.md; lane_evidence |

## Current Evidence

| Status | Evidence | Source | Next Action | Ownership Note |
| --- | --- | --- | --- | --- |
| submission_ready | `pe-report-profit-edge-daily-action-queue-e7654b96ab3f` - Profit Edge Daily Action Queue | E:\profit-edge-lab\reports\daily-action-queue-latest.md | Cashflow: promoted ledger action "rustchain 293 14015 payout monitor"; next action is Monitor RustChain wallet registration #14058 and payout follow-up threads #293/#14015 for owner award/payment replies or explicit payo | Read-only source snapshot used for lane routing and infrastructure design. |
| imported_jsonl | `pe-report-profit-edge-manual-overrides-f46da04dfc8d` - Profit Edge Manual Overrides | E:\profit-edge-lab\opportunities\manual-overrides.jsonl | Do not monitor PR #1413 or RustChain #14037 as active cashflow. Keep the current promoted action focused on RustChain #14058/#293/#14015 payout monitoring only. | Read-only negative-sample and policy memory for future lane managers. |
| local_agent_company_money_path_coverage_audit_complete | `agent-company-money-path-coverage-audit-20260616` - Agent company money-path coverage audit | E:\agent-company-lab\reports\agent-company-money-path-coverage-audit-latest.md | Launch/report the six undercovered money lanes as read-only or local-proof research waves before adding more platform approval plumbing. | Platform evidence only; it does not execute money-lane side effects. |
| complete_report_only_contract | `evidence-sandbox-execution-gate-contract-v1-20260617` - Sandbox execution gate contract v1 | E:\agent-company-lab\reports\sandbox-execution-gate-contract-v1-validation-20260617.json | Build sandbox execution approval packet and fixture runner before any code-worker or cloud sandbox execution. | Owned by platform engineering. Contract is report-only and grants no sandbox execution authority. |
| complete_local_architecture_matrix | `evidence-agent-platform-capability-matrix-v1-20260617` - Agent platform capability matrix v1 | E:\agent-company-lab\reports\agent-platform-capability-matrix-v1-validation-20260617.json | Build sandbox_execution_gate_contract_v1 or workflow_automation_service_worker_manifest_v1 as local-only artifacts. | Owned by platform engineering. Matrix is pattern/gate guidance only and performs no external action. |
| complete_current_source_radar | `evidence-agent-company-current-source-radar-wave11-20260617` - Agent Company current-source platform radar Wave 11 | E:\agent-company-lab\reports\agent-company-current-source-radar-wave11-validation-20260617.json | Build agent_platform_capability_matrix_v1 or sandbox_execution_gate_contract_v1 locally; rerun rate-limited repository metadata refresh later before any dependency or runtime decision. | Owned by platform engineering. Research only: no installs, starts, accounts, browser sessions, model/API calls, public actions, or external side effects. |
| complete_report_only_blocker | `evidence-runtime-implementation-apply-preflight-blocker-v1-20260617` - Runtime implementation apply preflight blocker v1 | E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-apply-preflight-blocker-v1-validation-20260617.json | If a real signed runtime decision is provided later, run guard validation and build a separate apply preflight before any executable runtime or service-request mutation work. | Owned by platform engineering. This evidence blocks fixture or missing signed decisions from runtime application. |
| complete_report_only_guard | `evidence-runtime-implementation-signed-decision-guard-v1-20260617` - Runtime implementation signed decision guard v1 | E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-signed-decision-guard-v1-validation-20260617.json | Build a separate apply-preflight only if a real signed human runtime decision is provided and accepted by this guard. | Owned by platform engineering. This evidence does not approve or execute runtime implementation work. |
| complete | `evidence-runtime-implementation-human-approval-packet-v2-20260617` - Runtime implementation human approval packet v2 validation | E:\agent-company-lab\reports\durable-orchestration\runtime-implementation-human-approval-packet-v2-validation-20260617.json | Build signed runtime decision intake/fixture guard before any approval can be applied. | Owned by recovered-profitable-edge-infra; report-only approval packet, no dependency/runtime/worker/service mutation approval granted. |
| complete | `evidence-local-service-worker-request-state-machine-runner-v1-20260617` - Local service-worker request state-machine runner validation | E:\agent-company-lab\reports\durable-orchestration\local-service-worker-request-state-machine-runner-v1-validation-20260617.json | Prepare runtime implementation human approval packet v2 before any external runtime or worker execution. | Owned by recovered-profitable-edge-infra; local-only preview, no service-request mutation and no worker start. |
| local_sqlite_outbox_acknowledgement_runner_v1_complete | `evidence-sqlite-outbox-acknowledgement-runner-v1-20260617` - SQLite outbox acknowledgement runner preview v1 | E:gent-company-lab eportsgent-company-central-outbox-history-v1-20260617.json | Build local_service_worker_request_state_machine_runner_v1_without_worker_start as the next local executable-control-plane preview. | Platform engineering local runner preview; no outbox row update, service-request mutation, worker start, browser/API/model call, public action, or external side effect. |
| local_durable_runtime_comparison_decision_packet_v1_complete | `evidence-durable-runtime-comparison-decision-packet-v1-20260617` - Durable runtime comparison decision packet v1 | E:gent-company-lab eports\durable-orchestration\durable-runtime-adapter-matrix-v2-validation-20260617.json | Build sqlite_outbox_acknowledgement_runner_v1_without_service_request_mutation as the next local executable-control-plane preview. | Platform engineering decision packet; no runtime dependency, import, server, queue, workflow, event, service mutation, worker start, browser/API/model call, or external side effect. |

## Tasks

| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |
| ---: | --- | --- | --- | --- | --- | --- |
| 2 | new | `task-agent-company-atlas-agent-party-v1-20260618` - Add lane Agent Party overview | recovered-profitable-edge-infra |  | Verified selected lane Overview shows bot portrait cards with readiness, pressure, thread id, and local COM/Q/PATH actions across responsive viewports. | Add lane-party animation skins or expanded generated portraits for future lane agents. |
| 2 | new | `task-agent-company-atlas-runway-lenses-v1-20260618` - Add Milestone Runway lens controls | recovered-profitable-edge-infra |  | Verified Runway lenses filter All, Gates, Unlocks, Events, and Future route layers with no overflow or clipped labels across responsive viewports. | Add lane-specific lens skins or a future-slot texture generator for realm-specific path previews. |
| 116 | complete | `task-control-plane-capacity-benchmark-v1-20260620` - Benchmark and index control-plane capacity | recovered-profitable-edge-infra |  | Synthetic benchmark raw JSON, capacity benchmark report/JSON, schema index patch, applied index verification, trace event | Runner created and verified; next gate is 500000 and 1000000 row benchmark before high-volume worker rollout. |
| 108 | complete | `task-agent-company-atlas-path-stage-atmosphere-v1-20260618` - Path Stage Atmosphere | recovered-profitable-edge-infra |  | Direct Path board uses the repo-local procedural path-stage-atmosphere texture as a cockpit-wide level-world background with no horizontal overflow. | Continue adding lane-specific art and meaningful motion layers while preserving compact first-viewport density. |
| 107 | complete | `task-agent-company-atlas-path-stage-focus-lens-v1-20260618` - Path Stage Focus Lens | recovered-profitable-edge-infra |  | Direct Path Stage Ribbon shows the focused level's type, cleaned title, and next meaning in a compact overlay without adding a scroll panel. | Continue improving lane-specific stage art, motion, and focused proof/blocker visibility without adding scroll. |
| 106 | complete | `task-agent-company-atlas-path-core-snapshot-v1-20260618` - Path Core Snapshot | recovered-profitable-edge-infra |  | Direct Path Core deck uses a compact snapshot lens instead of mounting full scroll-heavy Scan, Command, or Route panels inside the bounded stage. | Continue upgrading the Path cockpit with higher-quality lane-specific motion, richer agent art, and compact game-board layers. |
| 105 | complete | `task-agent-company-atlas-path-depth-pill-v1-20260618` - Path Depth Pill | recovered-profitable-edge-infra |  | Default Stage Depth controls float as a compact pill inside the Path stage, preserving Archive and Tools as explicit deeper modes while reducing first-screen vertical weight. | Continue replacing tall dashboard stacks with compact game HUD layers and improve lane-specific motion quality. |
| 104 | complete | `task-agent-company-atlas-path-crew-presence-v1-20260618` - Path Crew Presence | recovered-profitable-edge-infra |  | Direct Path Mission Glance shows mapped bot portraits, callsigns, readiness bars, and gated/ready/staged state without adding a new scroll panel. | Continue improving bot communication and avatar richness while keeping first-viewport Path cockpit compact. |
| 103 | complete | `task-agent-company-atlas-path-run-meter-hud-v1-20260618` - Path Run Meter HUD | recovered-profitable-edge-infra |  | Mission Glance Path Run Meter uses the generated path-run-meter-hud texture, remains within the first viewport, and is registered in the Visual Asset Vault. | Continue increasing premium visual texture inside compact first-viewport HUD surfaces, then move to bot/avatar richness without increasing scroll. |
| 102 | complete | `task-agent-company-atlas-path-run-meter-v1-20260618` - Path Run Meter | recovered-profitable-edge-infra |  | Direct Path view shows a five-socket Mission Glance run meter for route, gate, proof, tasks, and notes without adding scroll or overflow. | Continue replacing text-heavy first-viewport status with compact game HUD controls while keeping deeper history behind deliberate depth switches. |
| 101 | complete | `task-agent-company-atlas-path-route-focus-v1-20260618` - Path Route Focus | recovered-profitable-edge-infra |  | Direct Path links preserve an already-visible cockpit instead of yanking the Path board to the viewport top. | Keep improving first-viewport Path readability before adding deeper panels or longer scroll. |
| 100 | complete | `task-agent-company-atlas-path-core-live-tokens-v1-20260618` - Path Core Live Tokens | recovered-profitable-edge-infra |  | Direct Path view shows compact live blocker, proof, and work tokens inside the Core rail without adding scroll or horizontal overflow. | Continue tightening the direct Path stage with richer bot/blocker/proof readouts that stay inside the first viewport. |

## Service Requests

| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rejected | real_money_trade_gate | real_money_trade | `req-test-service-intake-valid-20260614` |  | test_validator_no_external_action | Validator positive test only: no external action, no real trade, no funds. | E:\agent-company-lab\reports\service-catalog-latest.md | Validator positive-path test completed; no external action required or allowed. |
| needs_review |  | model_api_execution | `req-pydantic-ai-model-backed-adapter-20260614` |  | model_api_call_requires_provider_model_cost_lane_and_artifact_scope | Run a real model-backed Pydantic AI adapter only after provider, model, max cost, allowed lanes, output artifact path, and credential route are explicitly approved. | E:\agent-company-lab\reports\worker-runtime\pydantic-ai-eval-latest.md |  |
| complete |  | lifecycle_test | `req-test-lifecycle-approve-20260614` | recovered-profitable-edge-infra | test_no_external_action | Dummy lifecycle approval/start/complete test; no browser, account, wallet, public, or money action. | E:\agent-company-lab\reports\source-research-refresh-20260614.md | Completed lifecycle verification; unapproved start was blocked, approval path completed, rejection path recorded. |
| rejected |  | lifecycle_test | `req-test-lifecycle-reject-20260614` |  | test_no_external_action | Dummy lifecycle rejection test; no browser, account, wallet, public, or money action. |  | Lifecycle rejection-path test. No external action required or allowed. |
| needs_review |  | research_enrichment | `req-grok-research-worker-20260614` |  | browser_grok_or_x_requires_signed_in_browser_and_no_public_actions | Later run Grok/X research prompts for current agent-company infrastructure trends; save prompt/output/verification artifacts; do not post, like, follow, or reply. | E:\agent-company-lab\notes\research-log-20260614.md |  |

## Recent Outcomes

| Status | Type | Outcome | Realized USD | Evidence | Next Action |
| --- | --- | --- | ---: | --- | --- |
| local_status_smoke_complete | platform_live_thread_status | `outcome-platform-engineering-live-thread-status-20260621` | 0.0 | E:\agent-company-lab\reports\platform-engineering\platform-engineering-status-20260621.md | Run 500000-row synthetic capacity benchmark before claiming high-volume readiness; CEO/AR decision still required for submitted_bounty_payouts ownership. |
| validated | control_plane_capacity_capability | `outcome-control-plane-capacity-benchmark-runner-v1-20260620` | 0.0 | E:\agent-company-lab\reports\control-plane-capacity-benchmark-runner-v1-20260620.md | Run 500000 and 1000000 row scenarios before high-volume worker orchestration. |
| complete | control_plane_capacity_benchmark | `outcome-control-plane-capacity-benchmark-v1-20260620` | 0.0 | E:\agent-company-lab\reports\control-plane-capacity-benchmark-v1-20260620.md | Create control_plane_capacity_benchmark_runner_v1 as a reusable local script or CLI command. |
| milestone_runway_browser_verified | browser_verification | `outcome-agent-company-atlas-milestone-runway-browser-verification-20260618` | 0.0 | E:\agent-company-lab\reports\agent-company-atlas-milestone-runway-browser-verification-20260618.json | Continue closing Atlas platform tasks, starting with Milestone Runway lens controls. |
| crew_bridge_browser_verified | browser_verification | `outcome-agent-company-atlas-crew-bridge-browser-verification-20260618` | 0.0 | E:\agent-company-lab\reports\agent-company-atlas-crew-bridge-browser-verification-20260618.json | Continue closing Atlas platform tasks, starting with Milestone Runway verification. |
| motion_forge_browser_verified | browser_verification | `outcome-agent-company-atlas-motion-forge-browser-verification-20260618` | 0.0 | E:\agent-company-lab\reports\agent-company-atlas-motion-forge-browser-verification-20260618.json | Continue closing Atlas platform tasks, starting with Crew Bridge squad-readiness verification. |
| arcade_stingers_browser_verified | browser_verification | `outcome-agent-company-atlas-arcade-stingers-browser-verification-20260618` | 0.0 | E:\agent-company-lab\reports\agent-company-atlas-arcade-stingers-browser-verification-20260618.json | Continue closing Atlas platform tasks, starting with Motion Forge animation-audit verification. |
| arcade_deck_browser_verified | browser_verification | `outcome-agent-company-atlas-arcade-deck-browser-verification-20260618` | 0.0 | E:\agent-company-lab\reports\agent-company-atlas-arcade-deck-browser-verification-20260618.json | Continue closing Atlas platform tasks, starting with Arcade Deck animated stingers and Motion Forge verification. |

## Startup Commands

```powershell
python E:\agent-company-lab\tools\agent_company.py status
python E:\agent-company-lab\tools\agent_company.py list-source-specs --lane-id platform_engineering
python E:\agent-company-lab\tools\agent_company.py list-evidence --lane-id platform_engineering --limit 25
```

## Suggested Manager Prompt

```text
You are the department manager for `platform_engineering` in `E:\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate.
```

