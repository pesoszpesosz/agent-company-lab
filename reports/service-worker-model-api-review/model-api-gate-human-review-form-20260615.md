# Model API Gate Human Review Form

Generated: `2026-06-15T13:12:00Z`
Request: `req-pydantic-ai-model-backed-adapter-20260614`
Lane: `platform_engineering`
Risk gate: `model_api_call_requires_provider_model_cost_lane_and_artifact_scope`

## Boundary

This form is for manual review notes only. Filling it out does not approve, reject, assign, update, start, install, import, call a model/API, browse, submit, pay, trade, or contact anyone.

## Default Decision

`park`

## Reviewer Fields

- Human user reviewer: `[blank]`
- Chief risk officer reviewer: `[blank]`
- CEO orchestrator reviewer: `[blank]`
- Review timestamp UTC: `[blank]`
- Decision: `park` / `reject` / `approve_later`
- Decision note: `[blank]`

## Scope Fields Required Before Approve Later

- `provider`: `None`
- `model`: `None`
- `max_cost_usd`: `0`
- `input_artifact_paths`: `[]`
- `input_data_sensitivity`: `local_public_or_internal_artifact_metadata_only`
- `output_artifact_paths`: `[]`
- `allowed_runner_agent_id`: `None`
- `approved_trace_id`: `None`
- `approved_task_id`: `None`
- `stop_conditions`: `['cost ceiling reached', 'unexpected sensitive/private data appears', 'provider/model differs from exact approval', 'output path differs from exact approval', 'any browser/account/payment/public/real-money/security-testing action becomes necessary', 'chain integrity check fails before execution']`
- `hard_denials_confirmed`: `['no credentials, OTPs, secrets, private files, private personal data, tax/KYC/payment/wallet data', 'no browser, login, signup, account settings, form submission, public post/comment/message/listing/upload/contact', 'no payment, purchase, deposit, withdrawal, trade, wallet connection, wallet signature, or real-money action', 'no security testing beyond local artifact analysis', 'no dependency install/import or worker start unless separately recorded and approved']`

## Manual Decision Routes

- `park`: default `true`. No service-request mutation. Keep request in needs_review.
- `reject`: default `false`. This form does not reject. Human/CRO must separately run a reject command after review if desired.
- `approve_later`: default `false`. This form does not approve. Human, CRO, and CEO must separately approve exact scope after all scope fields are complete.

## CEO Prompts

- Is a model/API call necessary, or can a local deterministic adapter produce the needed artifact?
- Which money-path lane benefits from this model call, and what artifact proves that benefit?
- What is the maximum acceptable spend and who owns that budget?
- Will this create reusable company infrastructure, or only a one-off convenience?

## CRO Prompts

- Does the input scope include secrets, credentials, personal data, tax/KYC/payment/wallet data, or private files?
- Are browser/account/public/payment/trading/security-testing actions explicitly excluded?
- Are stop conditions observable before cost or data exposure exceeds the approval?
- Can the request be safely rejected or parked without losing an active money opportunity?

## Completion Rules

- A filled form is still not an approval unless a separate approve-service-request record exists.
- A filled form is still not a rejection unless a separate reject-service-request record exists.
- Any manual approval must preserve max cost, exact input/output artifact paths, hard denials, and stop conditions.
- The worker pool must be registered separately before any assignment or start.

## Validation

- All no-execution checks passed: `true`
- Default decision: `park`
- API calls / external effects: `false` / `false`
- Service updates / assignments / worker starts: `0` / `0` / `0`
