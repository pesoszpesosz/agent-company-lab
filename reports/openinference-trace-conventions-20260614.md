# OpenInference-Style Trace Metadata Conventions

Generated UTC: 2026-06-14T12:18:00Z

Machine-readable convention: `E:\agent-company-lab\architecture\openinference-trace-metadata-v1.json`

## Purpose

The control plane already has a `trace_events` table. This convention defines how future events should use `metadata_json` so the lab can later export to Phoenix, Langfuse, OpenTelemetry, or an OpenInference-compatible viewer without changing the business tables.

This is not a full OpenTelemetry implementation. It is a local audit convention.

## Canonical Columns

Keep these in the table columns:

- `trace_id`
- `lane_id`
- `task_id`
- `agent_id`
- `event_type`
- `event_time`
- `summary`
- `artifact_path`

Use `metadata_json` only for span/runtime/eval/review details.

## Span Kinds

Use these values in `metadata_json.span_kind`:

- `AGENT`
- `WORKFLOW`
- `LLM`
- `TOOL`
- `RETRIEVER`
- `EVALUATOR`
- `PROMPT`
- `GUARDRAIL`
- `SERVICE_REQUEST`
- `HUMAN_REVIEW`
- `ARTIFACT`
- `SOURCE_REFRESH`

## Required Baseline For New Structured Events

Every new structured event should include:

```json
{
  "span_kind": "EVALUATOR",
  "runtime": "local_static_text_coverage",
  "api_calls": false
}
```

Use the closest `span_kind`. If no kind fits, use `WORKFLOW` and add a note in `summary`.

## Model Events

For any real or simulated model event:

```json
{
  "span_kind": "LLM",
  "provider": "openai",
  "model": "MODEL_ID",
  "prompt_version_id": "PROMPT_VERSION_ID",
  "input_tokens": 0,
  "output_tokens": 0,
  "cost_usd": 0,
  "api_calls": false
}
```

Rules:

- `api_calls=false` for TestModel, dry-run, and local static evals.
- Real model calls must have a service request if they can cost money or touch external APIs.
- Do not claim a behavioral model eval unless the trace has provider/model/prompt_version_id and a linked eval run.

## Tool Events

For local CLI/tool events:

```json
{
  "span_kind": "TOOL",
  "tool_name": "agent_company.py write-dashboard",
  "exit_code": 0,
  "api_calls": false
}
```

Rules:

- Redact arguments.
- Do not store secrets, cookies, private keys, OTPs, or payment details.

## Eval Events

For prompt or worker evals:

```json
{
  "span_kind": "EVALUATOR",
  "runtime": "local_static_text_coverage",
  "dataset_id": "manager-prompt-safety-cases-20260614",
  "prompt_version_id": "lane-manager-startup-v2-20260614",
  "score": 1.0,
  "cases_total": 6,
  "cases_passed": 6,
  "api_calls": false
}
```

The first structured event using this convention is:

- `trace-event-manager-prompt-eval-runner-20260614`

## Service Request Events

For gated side-effect work:

```json
{
  "span_kind": "SERVICE_REQUEST",
  "service_request_id": "REQ_ID",
  "risk_gate": "wallet_action",
  "approval_id": "APPROVAL_ID",
  "api_calls": false
}
```

If a public/browser/wallet/legal/security/real-money event lacks `service_request_id`, interpret it as blocked or invalid, not approved.

## Near-Term Implementation Rule

Do not migrate the DB yet. Keep writing flexible JSON metadata, but require `span_kind`, `runtime`, and `api_calls` for new structured events from:

- prompt evals
- model evals
- service requests
- browser workers
- wallet workers
- public-action workers

