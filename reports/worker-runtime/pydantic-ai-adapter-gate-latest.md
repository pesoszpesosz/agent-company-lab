# Pydantic AI Adapter Gate

Generated UTC: 2026-06-14T11:46:00Z

## Result

The gated adapter shell is implemented and verified.

- Script: `E:\agent-company-lab\tools\pydantic_ai_model_adapter.py`
- Venv: `E:\agent-company-lab\.venv-runtime`
- Runtime: `pydantic-ai==1.107.0`
- Dry-run model: `pydantic_ai.models.test.TestModel`
- API calls in verification: `false`

## Verification

Dry-run command:

```powershell
E:\agent-company-lab\.venv-runtime\Scripts\python.exe E:\agent-company-lab\tools\pydantic_ai_model_adapter.py --mode dry-run --lane-id prediction_market_research
```

Dry-run output:

- `E:\agent-company-lab\reports\worker-runtime\pydantic-ai-adapter-dry-run-prediction_market_research.md`
- `E:\agent-company-lab\reports\worker-runtime\pydantic-ai-adapter-dry-run-prediction_market_research.json`

Real-mode refusal command:

```powershell
E:\agent-company-lab\.venv-runtime\Scripts\python.exe E:\agent-company-lab\tools\pydantic_ai_model_adapter.py --mode real --lane-id prediction_market_research --model test-real-model-placeholder
```

Observed refusal:

```text
Refusing real model run: service request req-pydantic-ai-model-backed-adapter-20260614 is needs_review. Approve exact provider, model, max cost, allowed lanes, output artifact path, and credential route first.
```

## Boundary

Real model execution remains blocked until `req-pydantic-ai-model-backed-adapter-20260614` is explicitly approved with provider, model, max cost, allowed lanes, output artifact path, and credential route.
