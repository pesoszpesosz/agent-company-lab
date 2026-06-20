# Model Runtime Selection

Generated UTC: 2026-06-14T11:36:00Z

## Decision

Evaluate `pydantic-ai` first, in an isolated virtual environment, and keep OpenAI Agents SDK as the second runtime candidate.

Reason: the current agent-company control plane already owns orchestration, approvals, tasks, artifacts, and trace events. The next model-backed runtime should therefore improve typed outputs and lane-context validation before it adds another orchestration layer. Pydantic AI matches the typed worker contract we already prototyped in `tools/typed_worker_runtime.py`.

## Current Package Facts

Checked with `python -m pip index versions` on 2026-06-14:

| Package | Latest on pip | Installed locally | Note |
| --- | ---: | ---: | --- |
| `pydantic-ai` | `1.107.0` | not installed | First candidate for isolated evaluation. |
| `openai-agents` | `0.17.5` | not installed | Second candidate for orchestration-heavy workflows. |
| `openai` | `2.41.1` | `2.31.0` | Installed but not latest; do not upgrade globally just for this prototype. |

## Source Findings

### Pydantic AI

Official docs describe Pydantic AI as a Python agent framework for production-grade generative AI applications and workflows:

- https://pydantic.dev/docs/ai/overview/

Fit for this lab:

- Type safety is a first-class feature, which maps directly to the local `LaneContext` and `TaskProposal` schemas.
- Structured outputs are validated with Pydantic, and the Agent result carries the output type.
- Built-in model/provider support includes OpenAI plus many other providers, which keeps the worker runtime portable.
- Human-in-the-loop tool approval and durable execution are available for later service-worker gates.

Relevant source pages:

- https://pydantic.dev/docs/ai/core-concepts/output/
- https://pydantic.dev/docs/ai/models/overview/

### OpenAI Agents SDK

OpenAI docs say to use the Agents SDK when an application needs code-first orchestration for agents, tools, handoffs, guardrails, tracing, or sandbox execution:

- https://developers.openai.com/api/docs/libraries#use-the-agents-sdk
- https://developers.openai.com/api/docs/guides/agents

Fit for this lab:

- Strong second candidate once we need model-run orchestration, handoffs, guardrails, tracing, sandbox agents, and MCP/tool execution in one SDK.
- Less urgent for the immediate next step because SQLite already owns company state, approvals, traces, artifacts, and lane ownership.

## Recommendation

Use `pydantic-ai==1.107.0` for the first model-backed experiment.

Scope:

1. Create an isolated venv under `E:\agent-company-lab\.venv-runtime`.
2. Install only `pydantic-ai==1.107.0` there.
3. Implement a tiny adapter that imports the existing `LaneContext` and `TaskProposal` contract.
4. Run in dry-run mode first: load lane context, build instructions, and validate a synthetic model output without API calls.
5. Only after dry-run passes, add a service request for real model/API execution because model calls can incur cost and may require credential/account confirmation.

Do not:

- Upgrade the global `openai` package yet.
- Install both runtimes at once.
- Give the runtime direct account, wallet, browser, public-comment, KYC/billing, or trading capability.
- Let the runtime write to GitHub or X directly.

## Evaluation Criteria

Pass conditions for the first runtime:

| Criterion | Required Result |
| --- | --- |
| Typed output | Produces a valid `TaskProposal` or rejects invalid output. |
| Lane boundary | Returns `no_action_read_only` for `submitted_bounty_payouts`. |
| Service gates | Blocks side-effect lanes unless a service request exists. |
| Artifacts | Writes local JSON/Markdown artifacts and records them. |
| Traceability | Records trace events with lane, task, and artifact IDs. |
| Reproducibility | Runs from one command without relying on chat memory. |

## Next Task

Create `task-pydantic-ai-isolated-eval-20260614`:

- Build `.venv-runtime`.
- Install `pydantic-ai==1.107.0`.
- Add `tools/pydantic_ai_worker_eval.py` with dry-run validation only.
- Generate a report under `reports/worker-runtime/pydantic-ai-eval-latest.md`.
- Record artifacts, outcome, and trace event.
