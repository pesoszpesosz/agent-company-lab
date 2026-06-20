# CEO/CRO Model API Gate Checklist

Generated: `2026-06-15T12:58:00Z`
Request: `req-pydantic-ai-model-backed-adapter-20260614`
Lane: `platform_engineering`
Risk gate: `model_api_call_requires_provider_model_cost_lane_and_artifact_scope`

## Boundary

This checklist is decision support only. It does not approve, reject, assign, update, start, install, import, call a model/API, browse, submit, pay, trade, or contact anyone.

## Recommendation Now

Park the request in `needs_review` until provider, model, maximum cost, exact local input artifacts, exact local output artifacts, allowed runner, worker pool, and stop conditions are concrete.

## Required Authorities

- `human_user`
- `chief_risk_officer`
- `ceo_orchestrator`

## Minimum Scope Fields

- `provider`: required before approval; current value `None`. Do not infer provider from this checklist.
- `model`: required before approval; current value `None`. Must match provider and cost ceiling.
- `max_cost_usd`: required before approval; current value `0`. Any nonzero cost requires explicit user/CRO/CEO approval.
- `input_artifact_paths`: required before approval; current value `[]`. No private files, secrets, credentials, tax/KYC/payment/wallet data.
- `output_artifact_paths`: required before approval; current value `[]`. Output paths must be local artifacts only.
- `allowed_runner_agent_id`: required before approval; current value `None`. Do not assign/start until pool registration and approval are separate facts.
- `stop_conditions`: required before approval; current value `['latest_approval_exists', 'latest_approval_approved', 'latest_approval_not_expired', 'approval_scope_matches_service_scope', 'side_effect_denials_present']`. Stop conditions must be enforced before any API execution.

## CEO Questions

- Is a model/API call necessary, or can a local deterministic adapter produce the needed artifact?
- Which money-path lane benefits from this model call, and what artifact proves that benefit?
- What is the maximum acceptable spend and who owns that budget?
- Will this create reusable company infrastructure, or only a one-off convenience?

## CRO Questions

- Does the input scope include secrets, credentials, personal data, tax/KYC/payment/wallet data, or private files?
- Are browser/account/public/payment/trading/security-testing actions explicitly excluded?
- Are stop conditions observable before cost or data exposure exceeds the approval?
- Can the request be safely rejected or parked without losing an active money opportunity?

## Decision Branches

- `park`: recommended now `true`. Provider/model/cost/data/output scope is still missing and worker pool is not registered.
- `reject`: recommended now `false`. Use if CEO/CRO decides model/API execution is unnecessary or too risky for this lane.
- `approve_later`: recommended now `false`. Only after all minimum scope fields are filled, cost is explicit, worker pool exists, and user/CRO/CEO approvals are recorded.

## Validation

- All no-execution checks passed: `true`
- API calls / external effects: `false` / `false`
- Service updates / assignments / worker starts: `0` / `0` / `0`
- Recommended branch now: `park`
