# Agent Company Central Outbox History v1

Generated UTC: 2026-06-20T12:52:08Z
Fixture: `E:\agent-company-lab\reports\agent-company-central-outbox-history-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\agent-company-central-outbox-history-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\central-outbox-history-v1.schema.json`

## Summary

- Messages checked: `3`
- Passed: `3`
- Failed: `0`
- External side effects: `false`

## Messages

| Message | Lane | Type | Approval | Replay | Status |
| --- | --- | --- | --- | --- | --- |
| `msg-wave10-central-outbox-build-20260617` | `platform_engineering` | `artifact_notice` | `local_only` | `queued` | `pass` |
| `msg-paid-code-parser-followup-20260617` | `paid_code_bounties` | `gate_request` | `needs_human_review` | `queued` | `pass` |
| `msg-ai-competition-arc-followup-20260617` | `ai_ml_competitions` | `dispatch` | `local_only` | `queued` | `pass` |

## Contract Decision

Use this v1 outbox/history contract as a local replay surface for manager and service-worker communication before adding Temporal, Inngest, DBOS, LangGraph, OpenAI Agents, or A2A execution adapters.

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- Security testing actions: `false`
- Model/API calls: `false`
- Runtime starts: `0`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
