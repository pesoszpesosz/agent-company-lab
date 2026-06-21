# Evaluation Harness Outline - Candidate Registry + Continuity Owner Response

Generated local date: 2026-06-21
Owner role: `local_evaluation_harness_builder`
Lane: `ai_resources_lab`
Status: report-only first deliverable

## Purpose

Define a compact, reproducible, local-only evaluation harness that proves whether candidate AI workers, agent frameworks, control-plane assets, or money-making tools improve Agent Company before adoption. The first harness targets:

1. The `AI Resources Candidate Registry V2` evaluation queue.
2. The continuity owner-response workflow from restore findings to safe local dispatch tasks.

This outline is not permission to install tools, start runtimes, open browsers, create accounts, publish, submit, trade, spend, call APIs, mutate lane ownership, restart workers, or perform external side effects.

## Source Inputs

Required source documents:

- `E:\agent-company-lab\architecture\ceo-operating-goal-v1.md`
- `E:\agent-company-lab\architecture\ceo-worker-constellation-v1.md`
- `E:\agent-company-lab\reports\ceo-worker-roster-v1-20260621.md`
- `E:\agent-company-lab\reports\ai-resources-candidate-registry-v2-20260621.md`
- `E:\agent-company-lab\reports\manager-packets\ai_resources_lab-manager-packet.md`

Candidate queue mirror:

- `E:\agent-company-lab\reports\ai-resources-candidate-evaluation-queue-v1-20260621.json`

Continuity workflow evidence:

- `E:\agent-company-lab\reports\continuity-watchdog-snapshot-v1-20260621.md`
- `E:\agent-company-lab\reports\continuity-watchdog-restore-plan-v1-20260621.md`
- `E:\agent-company-lab\reports\continuity-watchdog-restore-response-bundle-v1-20260621.md`
- `E:\agent-company-lab\reports\continuity-watchdog-owner-response-artifacts-v1-20260621.md`
- `E:\agent-company-lab\reports\continuity-watchdog-owner-response-task-dispatch-v1-20260621.md`
- `E:\agent-company-lab\reports\continuity-owner-responses-v1-20260621\`

## Harness Packet Shape

Each local evaluation packet should contain:

- `packet_id`: stable id with candidate or workflow slug and date.
- `subject`: candidate id, route id, control-plane asset, or continuity workflow step.
- `hypothesis`: one sentence describing the company improvement expected.
- `existing_owner_overlap`: current owner or tool that may already cover the need.
- `fixtures`: local files used as inputs, with no external fetch.
- `procedure`: deterministic read/check/write steps, report-only unless explicitly approved.
- `scores`: weighted rubric fields with pass/fail thresholds.
- `gates`: side-effect, legal, account, model/API, browser, payment, security, and public-action stops.
- `fast_fail`: maximum two focused work blocks to produce a useful local proof.
- `decision`: promote, keep and harden, adapt, merge, watch, park, reject, or retire.
- `evidence_paths`: generated report paths and raw source paths.
- `next_action`: exact local next step or exact human/action gate if blocked.

## Candidate Registry Harness

Scope: evaluate the 12 queued candidates first, beginning with control-plane assets and local harnesses because they improve the company without new dependencies.

Queued candidates:

1. `ceo_state_packet_v1`
2. `human_action_feed_v1`
3. `ai_resources_owner_acknowledgement_loop`
4. `pydantic_ai_testmodel_adapter`
5. `worker_capability_class_registry_v1`
6. `playwright_foundation_adapter`
7. `langgraph_checkpoint_inbox_patterns`
8. `prompt_eval_safety_harness`
9. `promptbase_agent_skill_route`
10. `upwork_ai_offer_matrix_route`
11. `arc_prize_2026_baseline_harness`
12. `kalshi_public_data_worksheet`

### Fixture Classes

- Registry fixture: normalized candidate rows from the candidate registry JSON.
- Company-context fixture: worker roster, operating goal, manager packet, and current CEO packet if present.
- Gate fixture: service bureau catalog, hard boundaries, zero-side-effect boundary, and human-action categories.
- Overlap fixture: current worker roles, allowed worker types, active goals, and duplicate-key rules.
- Evidence fixture: local report paths only; no browser, repo fetch, API, account, or install required.

### Scoring Rubric

Total: 100 points.

- Company fit, 20: maps to a priority lane, current worker gap, or control-plane improvement.
- Local proofability, 20: useful proof can be produced from fixtures within two focused work blocks.
- Risk containment, 20: gates are explicit and no hidden side effects are needed.
- Overlap discipline, 15: improves or reuses an existing owner before proposing a new worker/tool.
- Measurable value, 15: defines evidence that can change a promote/watch/reject decision.
- Reproducibility, 10: packet can be rerun from local source paths with stable expected outputs.

Decision thresholds:

- `promote`: 80+ and no unresolved hard gate.
- `keep_and_harden`: 70+ for existing control-plane assets with clear hardening steps.
- `adapt_or_merge`: 60-79 with meaningful overlap to an existing worker or tool.
- `watch`: 45-59 or useful reference value but no immediate local proof.
- `reject_or_park`: under 45, duplicate without advantage, unsafe, under-specified, or blocked beyond two work blocks.

### Candidate Test Cases

- Completeness check: required fields exist for every queued candidate.
- Gate check: every candidate has explicit stops for installs, runtimes, browser, accounts, public actions, spend, model/API calls, and external APIs.
- Overlap check: every candidate names the existing owner or explains the capability gap.
- Proof check: every candidate has one local proof artifact with input paths and expected output shape.
- Adoption check: every candidate can produce a decision without relying on external execution.

## Continuity Owner-Response Harness

Scope: prove that continuity findings become safe, owner-facing, local dispatch tasks without mutating source tasks, source lanes, owner assignments, worker queues, threads, or external systems.

Workflow under test:

1. `write-continuity-watchdog-snapshot`
2. `write-continuity-watchdog-restore-plan`
3. `write-continuity-watchdog-restore-response-bundle`
4. `write-continuity-watchdog-owner-response-artifacts`
5. `write-continuity-watchdog-owner-response-task-dispatch`

The harness does not run these commands unless separately authorized. It evaluates the existing local reports and defines deterministic fixture expectations for future dry runs.

### Continuity Fixture Classes

- Snapshot fixture: detected stale, offline, ownerless, overlapping, goal-less, duplicate, and acknowledgement issues.
- Restore-plan fixture: per-action routing to AI Resources, existing lane owner, or CEO decision batch.
- Response-contract fixture: required owner options, evidence fields, and stop gates.
- Selected-response fixture: chosen safe response option and rationale.
- Dispatch fixture: stable local task rows, duplicate keys, owner, evidence path, and next action.

### Continuity Scoring Rubric

Total: 100 points.

- Chain integrity, 25: every source finding has a traceable restore packet, response contract, selected response, and dispatch item or documented park/reject reason.
- Owner discipline, 20: existing owners are reused when possible; CEO decision batch receives only genuinely ownerless or ambiguous items.
- Non-mutation guarantee, 20: reports prove no source task completion, owner change, worker start, thread message, lane mutation, or external action occurred.
- Evidence sufficiency, 15: each dispatch task includes source evidence, required response evidence, stop gate, and next action.
- Duplicate resistance, 10: stable duplicate keys prevent repeated task creation.
- Business usefulness, 10: unresolved items are moved toward promote, park, retire, or exact human gate instead of generic follow-up.

Decision thresholds:

- `workflow_pass`: 85+ with no hard-boundary violation.
- `workflow_harden`: 70-84 with missing evidence fields or duplicate-key improvements needed.
- `workflow_blocked`: under 70 or any mutation/side-effect ambiguity.

### Continuity Test Cases

- Source-to-dispatch trace: every dispatch task links back to exactly one restore/response evidence path.
- Ack-loop reducer: stale owner acknowledgements become local owner-response tasks, not duplicate owners or worker restarts.
- Ownerless-lane handling: ownerless or ambiguous lanes route to AI Resources or CEO decision batch with select/park/retire options.
- Existing-owner handling: tasks for `lane-manager-ai_resources_lab-20260620` remain with the existing owner and require local evidence.
- No-side-effect check: reports must explicitly state zero thread messages, zero worker starts, zero owner mutations, zero external calls, and zero public actions.

## Output Artifacts

Recommended first concrete packet set:

- `local-eval-packet-candidate-registry-control-plane-v1-20260621.md`
- `local-eval-packet-candidate-registry-money-routes-v1-20260621.md`
- `local-eval-packet-continuity-owner-response-v1-20260621.md`
- `local-eval-scorecard-v1-20260621.json`

Recommended summary report:

- `local-evaluation-harness-index-v1-20260621.md`

## Minimal Implementation Plan

1. Create fixture manifests from the existing local report paths.
2. Build one packet template for candidates and one packet template for continuity workflow steps.
3. Populate the 12 queued candidate packet stubs from the registry JSON.
4. Populate one continuity workflow packet from existing continuity reports.
5. Score all packets with the rubrics above.
6. Emit an index with promote/watch/reject/harden recommendations and exact blocked gates.

## Hard Stops

Stop and write a blocker instead of continuing if a packet requires:

- Dependency install or untrusted code execution.
- Browser session, account login, account creation, terms acceptance, or credentials.
- Paid or external model/API call.
- Public post, proposal, PR, bounty claim, submission, outreach, or form send.
- Payment, wallet, trading, order, deposit, withdrawal, or real-money commitment.
- Live security testing or contact with a third party.
- Mutation of source tasks, lane ownership, worker queues, thread messages, service requests, or external systems.

## First Recommendation

Start with `ceo_state_packet_v1`, `human_action_feed_v1`, and `ai_resources_owner_acknowledgement_loop`, then evaluate the continuity owner-response workflow as one chain. These four proofs directly improve company memory, gate hygiene, owner discipline, and CEO context control without requiring external dependencies.
