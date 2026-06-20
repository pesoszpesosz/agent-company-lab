# Runtime Adapter Graduation Report - 2026-06-14

Scope: `platform_engineering`

This report compares the four local runtime adapters now covered by `work_packet.v1`. It performs no model/API call, browser action, account action, public action, wallet action, trade, submission, or payment action.

## Current Harness Result

Source report: `E:\agent-company-lab\reports\runtime-adapters\runtime-adapter-harness-20260614.md`

- Total adapter-packet checks: 12
- Passed: 12
- Failed: 0
- API calls: false
- External side effects: false
- Test packets:
  - `packet-safe-local-research`
  - `packet-browser-readonly-needs-review`
  - `packet-real-money-public-action-refusal`

## Adapter Status

| Adapter | Current behavior | Strong evidence | Weakness | Graduation decision |
| --- | --- | --- | --- | --- |
| `typed_worker_runtime_local_adapter` | Calls real local `typed_worker_runtime.py` proposal path for safe local packets; refuses gated packets before worker execution. | Uses existing lane-context loader and proposal contract; safe packet produced `proposal-platform_engineering-20260614`; gated packets report `typed_worker_runtime_called=false`. | Proposal output is still lane-level, not full `work_packet.v1` execution output. | Graduate to first production-local adapter after adding packet-to-proposal mapping and per-packet output files. |
| `pydantic_ai_testmodel_local_adapter` | Calls isolated `.venv-runtime` Pydantic AI `TestModel` eval for safe packets; refuses gated packets before Pydantic AI execution. | Uses `pydantic-ai==1.107.0`; eval reports `api_calls=false`; safe packet generated eval artifacts; gated packets report `pydantic_ai_testmodel_called=false`. | Still depends on a separate eval script and latest-file outputs; no per-packet adapter artifact path yet. | Graduate after adapter writes per-packet results and captures eval version/output hashes. |
| `openai_agents_sandbox_manifest_adapter` | Builds SDK-shaped sandbox manifest for safe packets; refuses gated packets before manifest construction; never imports/calls SDK. | Manifest includes local read/write tools, model execution disabled, `openai_agents_sdk_called=false`, and explicit guardrails. | It is a manifest contract, not actual SDK execution. That is intentional until model/API service approval exists. | Keep as sandbox contract; do not graduate to SDK execution until `model_api_execution` service request is approved. |
| `langgraph_static_graph_adapter` | Materializes static graph plan for every packet; safe packet routes to `synthesize`; gated packets route to `stop`; no graph engine import. | Graph has 5 nodes and 4 edges with explicit stop/synthesize route decisions; `langgraph_engine_imported=false`. | It is not dependency-backed LangGraph execution; it is a graph spec. | Keep as graph contract; only add dependency-backed execution after per-packet local writes are stable. |

## Graduation Order

1. `typed_worker_runtime_local_adapter`
   - Lowest risk because it already uses local DB context and local Pydantic schemas.
   - Next change: write one per-packet adapter result file to the expected output path, not only the shared harness JSON.

2. `pydantic_ai_testmodel_local_adapter`
   - Useful second because it exercises a real framework in offline mode.
   - Next change: isolate per-packet eval output names instead of `pydantic-ai-eval-latest.*`.

3. `langgraph_static_graph_adapter`
   - Useful for orchestration design once per-packet outputs are reliable.
   - Next change: export graph plans as standalone JSON artifacts that managers can inspect.

4. `openai_agents_sandbox_manifest_adapter`
   - Keep as contract-only until user/CRO approves model/API scope.
   - Next change: static validation of manifest shape, not SDK execution.

## Next Infrastructure Target

Build a per-packet adapter result writer:

- Add stable result paths under `E:\agent-company-lab\reports\runtime-adapters\packet-results\`.
- Each adapter-packet run should write one JSON result file.
- Harness summary should link to those files.
- The harness must still pass with:
  - `api_calls=false`
  - `external_side_effects=false`
  - all gated packets refused or routed to stop
  - all expected output paths created locally

This target is better than adding another framework because it strengthens the common contract all future agents will need. The current weakness is not framework coverage; it is per-run evidence granularity.

## Service Gate Position

No service request is approved by this report.

- `model_api_execution` remains blocked.
- `browser_read_only_session` remains blocked unless explicitly approved.
- public actions remain blocked.
- real-money actions remain blocked.
- account, wallet, legal, KYC, tax, billing, and payment setup remain blocked.

## Money-System Relevance

This is infrastructure work, not immediate cashflow. Its purpose is to make future money-path agents auditable:

- every agent receives the same `work_packet.v1` contract;
- every runtime must stop at service gates;
- every run produces local evidence before external action;
- managers can compare runtimes without account/API/browser/trading risk;
- the CEO layer can route work by evidence rather than chat claims.

Next practical step: implement the per-packet result writer, then use it to package one real lane task from `digital_products_templates_plugins` or `money_source_discovery` without external action.
