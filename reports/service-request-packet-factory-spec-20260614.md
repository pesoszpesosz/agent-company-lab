# Service Request Packet Factory Spec

Generated UTC: 2026-06-14

Workspace: `E:\agent-company-lab`
Lane owner: `platform_engineering`

## Purpose

Build the missing bridge between lane managers and service workers: a local packet factory that turns the existing service catalog into complete, reviewable request folders. The factory must make it easy for a manager to request help from browser, account, wallet, public-action, legal/KYC/payment, model/API, outreach, GitHub, security-report, secrets, data/API, or real-money review workers without hand-writing malformed JSON and without triggering external side effects.

This is not a workflow engine, browser worker, account worker, or approval engine. It is the contract generator those later systems will consume.

## Current Local Substrate

Already present:

- SQLite control plane: `E:\agent-company-lab\state\agent_company.sqlite`
- CLI: `E:\agent-company-lab\tools\agent_company.py`
- Service catalog: 13 catalog-backed services with `required_intake_json`, allowed actions, hard gates, approvers, and expected output artifacts.
- Validator: `create-service-request` blocks incomplete catalog-backed intake; `validate-service-request` reports missing fields.
- Service lifecycle: requests can be approved, rejected, assigned, started, and completed, with unapproved starts blocked.
- Artifact, outcome, and trace tables exist.

Missing:

- A command that generates a request folder from the catalog before a manager tries to create a DB request.
- A human-readable packet that combines required fields, allowed actions, hard gates, approvals, and exact requested action.
- A checklist that tells the requester exactly what is missing before DB creation.

## Source-Backed Design Inputs

Primary source signals checked on 2026-06-14:

- OpenAI Agents SDK docs recommend the Agents SDK for code-first orchestration involving agents, tools, handoffs, guardrails, tracing, or sandbox execution. Local implication: our packet must be independent of a specific runtime, but map cleanly to tool/handoff/trace concepts later.
- Hatchet's MCP cookbook exposes workflows/tasks as agent tools through typed input schemas, with workers executing runs and Hatchet providing reliability/observability. It also warns that MCP is not a security boundary and inputs must be validated at workflow level. Local implication: catalog-backed JSON intake should be the stable tool schema; prompt text cannot be the guardrail.
- Inngest `waitForEvent` docs describe pausing a function until an event arrives, explicitly useful for human-in-the-loop AI workflows and audit trails. Local implication: every packet needs approval metadata and a status path that can later become a wait-for-approval event.
- DBOS queues durably enqueue functions and return handles; docs state an enqueued function is guaranteed to eventually execute even if the app is interrupted. Local implication: the future DBOS/Hatchet bakeoff should consume the same packet folder and record a durable handle, not invent a separate request format.
- HumanLayer's 12-factor agents guidance emphasizes launch/pause/resume APIs, contacting humans with tool calls, owning control flow, and interrupting between tool selection and invocation for review. Local implication: the packet factory should create the review object between manager intent and worker execution.

## Recommended CLI

Add one command to `agent_company.py`:

```powershell
python E:\agent-company-lab\tools\agent_company.py scaffold-service-request `
  --service-id browser_read_only_session `
  --lane-id content_and_social_growth `
  --requester-agent-id lane-manager-content_and_social_growth-019ec613 `
  --requested-action "Read only the named X/Grok/Radar pages and capture evidence" `
  --output-dir E:\agent-company-lab\requests\service-requests
```

Optional arguments:

- `--request-id REQ_ID`: otherwise generate `req-{service_id}-{lane_id}-{YYYYMMDD-HHMMSS}`.
- `--request-type TYPE`: allowed as fallback, but if multiple catalog entries match, require `--service-id`.
- `--risk-gate TEXT`: default from service hard gates summarized as `catalog_required_approval_no_external_action`.
- `--prefill-json JSON` or `--prefill-file PATH`: prefill known intake fields.
- `--create-db-request`: only if validation passes; otherwise write files and return missing fields without touching `service_requests`.
- `--artifact-path PATH`: optional existing proof artifact to reference in the packet.

## Generated Folder

For each request:

```text
E:\agent-company-lab\requests\service-requests\REQ_ID\
  intake.json
  packet.md
  checklist.md
  metadata.json
```

`intake.json` should contain every required catalog field. Missing values use empty strings, not invented facts.

Recommended JSON shape:

```json
{
  "request_id": "req-browser_read_only_session-content_and_social_growth-20260614-000000",
  "service_id": "browser_read_only_session",
  "request_type": "browser_research",
  "lane_id": "content_and_social_growth",
  "requester_agent_id": "lane-manager-content_and_social_growth-019ec613",
  "requested_action": "Read only the named pages and capture evidence.",
  "risk_gate": "catalog_required_approval_no_external_action",
  "approval_scope": "",
  "intake": {
    "lane_id": "content_and_social_growth",
    "target_url": "",
    "allowed_read_scope": "",
    "forbidden_actions": "",
    "evidence_needed": "",
    "session_sensitivity": ""
  }
}
```

`packet.md` should include:

- request id, service id, request type, lane, requester, generated time;
- service purpose;
- exact requested action;
- required intake table with present/missing status;
- allowed actions copied from catalog;
- hard gates copied from catalog;
- approval required by copied from catalog;
- expected output artifacts copied from catalog;
- command to create the DB request after missing fields are filled;
- explicit statement: no account, wallet, payment, trade, public post, PR/comment, browser submit, API key, credential, or real-money action is approved by this packet.

`checklist.md` should be short and operational:

- missing required fields;
- blocker questions for the manager;
- whether `--create-db-request` was skipped;
- next exact command after completion.

`metadata.json` should record:

```json
{
  "generated_utc": "...",
  "api_calls": false,
  "external_side_effects": false,
  "source": "agent_company.py scaffold-service-request",
  "catalog_service_id": "...",
  "validation_ok": false,
  "missing_fields": []
}
```

## Validation Rules

1. Unknown `service_id` fails.
2. Mismatched `service_id` and `request_type` fails.
3. Unknown `lane_id` fails unless `--allow-unregistered-lane` is explicitly added later; do not add this in v1.
4. Unknown requester agent should warn, not fail, because future lane managers may be external chats not yet registered.
5. Prefill keys not in required intake should be preserved under `extra_context`, not silently dropped.
6. Missing required fields should still produce a packet, but must not create a DB request.
7. `--create-db-request` must call the same validator path as `create-service-request`.
8. All generated packets must be local-only and `api_calls=false`.

## Control Plane Recording

When scaffolding succeeds, register:

- artifact kind: `service_request_packet_spec` for this spec;
- artifact kind: `service_request_packet` for each generated packet folder;
- outcome type: `service_request_packet_factory_design` for this spec;
- trace event type: `service_request_packet_factory_spec_written` for this spec;
- trace event type: `service_request_packet_scaffolded` for each generated packet.

The trace metadata should include:

```json
{
  "span_kind": "internal",
  "runtime": "local_cli",
  "api_calls": false,
  "external_side_effects": false,
  "service_id": "...",
  "validation_ok": false
}
```

## Acceptance Tests

Minimum verification before declaring implementation complete:

1. `python E:\agent-company-lab\tools\agent_company.py scaffold-service-request --service-id browser_read_only_session --lane-id content_and_social_growth --requester-agent-id test-manager --requested-action "Read-only capture" --output-dir E:\agent-company-lab\requests\service-requests`
   - creates a folder with `intake.json`, `packet.md`, `checklist.md`, `metadata.json`;
   - missing required fields are visible;
   - no DB service request is created without `--create-db-request`.

2. Same command with a complete prefill file and `--create-db-request`:
   - creates a `needs_review` service request;
   - `validate-service-request --request-id REQ` returns `ok: true`;
   - request status is not approved or started.

3. Complete prefill for `real_money_trade_gate`:
   - creates only `needs_review`;
   - start still fails until explicit approval;
   - packet says paper/data-only until approval.

4. Mismatched service type fails:
   - `--service-id browser_read_only_session --request-type real_money_trade` exits nonzero.

5. Generated `packet.md` contains every hard gate for the selected catalog service.

6. `python -m py_compile E:\agent-company-lab\tools\agent_company.py` passes.

7. Refresh commands pass after implementation:

```powershell
python E:\agent-company-lab\tools\agent_company.py write-dashboard
python E:\agent-company-lab\tools\agent_company.py write-ceo-review
python E:\agent-company-lab\tools\agent_company.py write-trace-report
python E:\agent-company-lab\tools\agent_company.py write-artifacts-report
```

## Money-Lane Impact

This unlocks the next launch wave without giving agents unsafe powers:

- `money_source_discovery`: can request browser/API/source reviews and account-intake packets without registering anywhere.
- `ai_ml_competitions`: can request account/terms/eligibility review for Kaggle, DrivenData, lablab.ai, hackathons, and contest platforms.
- `digital_products_templates_plugins`: can request marketplace account/payment/legal review before any listing.
- `qa_usability_testing_gigs` and `ai_training_eval_gigs`: remain human-only for paid task execution; agents can prepare packets and decision notes only.
- `affiliate_partner_programs`: can request account/legal/payment reviews; no application submissions without explicit approval.

## Implementation Order

1. Add pure helper functions for request id generation, service packet rendering, checklist rendering, and metadata rendering.
2. Add CLI parser for `scaffold-service-request`.
3. Reuse `resolve_service_catalog_entry`, `validate_service_intake`, and existing `create_service_request` path where possible.
4. Add artifact/trace registration for generated packet folders.
5. Run the acceptance tests above.
6. Generate three starter packet folders for the first Wave-4 lanes only after implementation passes.

## Decision

Recommended: implement as a minimal command inside `agent_company.py` first. Do not introduce DBOS, Hatchet, Inngest, Trigger.dev, Temporal, Stagehand, or a browser worker until this packet contract is proven locally.
