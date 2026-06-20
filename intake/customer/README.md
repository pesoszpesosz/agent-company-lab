# Customer Intake Workspace

This workspace is for premium-customer inputs that should be routed to Agent Company lanes without filling the CEO context window with raw material.

## Folders

- `dropbox/`: raw customer-provided requests or materials before routing.
- `routes/`: local routing packets that say where each input went and why.
- `processed/`: routed inputs after they have a lane, artifact, task, watch condition, or human-action entry.

## Intake Rule

Raw input should be preserved here or in a referenced artifact. The CEO should receive only a compact context capsule: intent, target lane, summary, application path, status, next artifact, and whether human action is needed.

## Routing Command

Use the local router when customer-provided requests or materials need to enter the company memory:

```powershell
python tools\agent_company.py route-premium-customer-input --input-path intake\customer\dropbox\example.md
```

The router preserves raw material in `dropbox/`, writes compact route packets in `routes/`, updates the customer routing ledger and update feed, and records local DB trace rows unless `--no-db-record` is supplied.

After routing, create lane-owned follow-up tasks from the route packet:

```powershell
python tools\agent_company.py synthesize-premium-customer-followups --route-packet intake\customer\routes\example.json
```

The synthesizer writes compact follow-up packets in `processed/`, creates or refreshes one local task per target lane, and preserves existing task status on reruns so it does not duplicate or reset lane work.

Monitor generated follow-up tasks so routed knowledge does not sit unnoticed:

```powershell
python tools\agent_company.py monitor-premium-customer-followups --input-id customer-input-id
```

The monitor writes a local status report, updates the routing ledger and customer update feed, and flags ownerless, blocked, stale, or unacknowledged follow-ups without claiming tasks or starting workers.

Escalate stale or blocked follow-ups into a single controlled triage packet:

```powershell
python tools\agent_company.py escalate-premium-customer-followups --monitor-report reports\customer-followup-monitor-v1-20260620.json
```

The escalation command creates one local triage task for AI Resources or CEO review and does not mutate the original lane follow-up tasks.

## Non-Rejection Rule

Inputs should be routed, synthesized, applied, or parked with a revisit condition. Rejection is reserved for unsafe, illegal, impossible, spammy, duplicate-without-new-information, or out-of-scope inputs.
