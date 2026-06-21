# CEO Worker Constellation V1

Generated from the CEO objective on 2026-06-21.

## Purpose

The CEO brain stays context-light by delegating durable operating loops to AI Resources and adjacent workers. The bootstrap command keeps one AR lane, strengthens the existing `ai_resources_lab` owner, and adds specialized non-overlapping workers with active goals.

## Command

```powershell
python tools\agent_company.py bootstrap-ceo-workers
```

Optional live handles can be attached with:

```powershell
--ar-thread-id
--overlap-thread-id
--candidate-thread-id
--evaluation-thread-id
--retirement-thread-id
--continuity-thread-id
--premium-router-thread-id
--browser-ops-thread-id
```

## Workers

- `lane-manager-ai_resources_lab-20260620`: owns the AR queue and hire/evolve/park/retire decisions.
- `capability-overlap-mapper-20260621`: proves whether existing agents can evolve before any new hire.
- `candidate-registry-curator-20260621`: collects candidate AI workers/tools into a local registry.
- `local-evaluation-harness-builder-20260621`: designs local-only eval packets for candidates.
- `adoption-retirement-reviewer-20260621`: recommends evolve, watch, reject, merge, or retire decisions.
- `continuity-watchdog-worker-20260621`: checks stale, offline, ownerless, overlapping, and goal-less work.
- `premium-customer-context-router-20260621`: accepts customer materials, preserves raw context, and routes capsules.
- `browser-account-ops-worker-20260621`: separates AI-doable browser/account work from human KYC, billing, tax, and legal gates.

## Automation

App automation `agent-company-continuity-watchdog` wakes every 15 minutes to continue the CEO continuity loop, inspect current state, spawn bounded parallel helper agents when useful, and write local restore/escalation packets or CEO updates.

The executable local snapshot command is:

```powershell
python tools\agent_company.py write-continuity-watchdog-snapshot
```

It reports ownerless lanes, missing owner-agent rows, agents missing thread handles, stale open tasks, expired leases, duplicate active keys, lanes with no open tasks, and stale owner acknowledgements. It only writes local reports and audit rows.

Convert the snapshot into per-action local restore packets with:

```powershell
python tools\agent_company.py write-continuity-watchdog-restore-plan
```

The restore plan assigns each detected action to AI Resources, an existing lane owner, or a CEO decision batch while preserving the zero-side-effect boundary.

Convert restore packets into owner-facing response contracts with:

```powershell
python tools\agent_company.py write-continuity-watchdog-restore-response-bundle
```

The response bundle tells each owner or CEO decision surface exactly which response options and evidence fields are required. It does not mutate source restore packets, tasks, lanes, owner assignments, or external systems.

Convert owner-facing response contracts into selected local response artifacts with:

```powershell
python tools\agent_company.py write-continuity-watchdog-owner-response-artifacts
```

The owner response artifact step chooses the safe local response for each contract, writes per-response JSON/Markdown evidence, and keeps source tasks, lanes, owner assignments, workers, and external systems unchanged.

## Boundary

The constellation is local-control-plane only by default. It does not open browsers, create accounts, approve service requests, start external runtimes, publish, submit, trade, spend, call APIs, or contact anyone without a scoped gate.
