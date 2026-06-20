# Knowledge Application Loop V1

Generated UTC: 2026-06-20T17:04:00Z
Owner: `premium-customer-intake-agent-20260620`
Status: active local rule
JSON mirror: `E:\agent-company-lab\reports\knowledge-application-loop-v1-20260620.json`

## Purpose

Guarantee that useful knowledge discovered by the customer, workers, managers, AR evaluations, or lane research is not merely stored and forgotten.

## Loop

1. Capture the new knowledge as an input packet, artifact, route packet, source note, or lane packet.
2. Classify the knowledge by lane, gate, urgency, and possible application.
3. Pick an application path.
4. Update the smallest durable company object: task, packet, prompt, source registry, product artifact, script batch, eval, gate packet, dashboard, goal-evolver review, or watch list.
5. Emit a compact CEO/customer update.
6. Verify that the item is either applied, routed, parked with a revisit condition, or blocked by a named gate.

## Valid Application Paths

- Money lane packet
- Service lane packet
- AI Resources evaluation
- Human-action feed item
- Goal-evolver review
- CEO state packet
- Prompt or task update
- Source registry update
- Product artifact update
- Script/content batch update
- Evaluation fixture or result
- Dashboard or snapshot update
- Watch list with revisit condition

## Anti-Rejection Policy

Do not use rejection as the default. If knowledge is not immediately actionable, park it with a reason and revisit trigger. If it is unsafe or out of scope, record why and provide a safer route when one exists.

## Boundary

This loop applies knowledge to local company memory only. It does not authorize external actions.
