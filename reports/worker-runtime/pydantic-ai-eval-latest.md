# Pydantic AI Dry-Run Eval

Generated UTC: 2026-06-19T23:58:50Z
Pydantic AI version: `1.107.0`
Model: `pydantic_ai.models.test.TestModel`
API calls: `false`

## Decision Signal

Pydantic AI can carry the existing `TaskProposal` output contract in an offline dry-run. It should remain isolated until a real model/API service request is approved.

## Results

| Lane | Passed | Mode | Evidence Refs | Failed Checks |
| --- | --- | --- | ---: | --- |
| `platform_engineering` | true | `read_only_local_artifact` | 5 |  |

## Gates

- This eval used `TestModel`; it made no network or model/API call.
- Real model execution still requires a service request because it can use credentials and incur cost.
- The payout lane must continue to return `no_action_read_only` in this workspace.

## Recommended Next Step

Add a model-backed adapter behind a service request only after deciding model/provider, max cost, allowed lanes, and output artifact path.
