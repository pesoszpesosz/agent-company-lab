# Trace Export Contract v1

Generated UTC: 2026-06-20T12:49:27Z
Fixture: `E:\agent-company-lab\reports\trace-export-contract-v1-20260617.json`
Schema: `E:\agent-company-lab\architecture\trace-export-contract-v1.schema.json`
Validation JSON: `E:\agent-company-lab\reports\trace-export-contract-validation-20260617.json`
Preview JSONL: `E:\agent-company-lab\reports\trace-export-contract-preview-20260617.jsonl`

## Summary

- Spans checked: `4`
- Passed: `4`
- Failed: `0`
- Backend calls: `false`
- External side effects: `false`

## Export Rows

| Event | Lane | Kind | Runtime | Status |
| --- | --- | --- | --- | --- |
| `trace-central-outbox-history-v1-20260617` | `platform_engineering` | `ARTIFACT` | `python_stdlib` | `pass` |
| `trace-agent-company-deep-research-wave10-20260617` | `platform_engineering` | `SOURCE_REFRESH` | `codex_web_and_github_public` | `pass` |
| `trace-evidence-algora-candidate-refresh-fixture-check-20260616` | `paid_code_bounties` | `EVALUATOR` | `python_stdlib` | `pass` |
| `trace-evidence-arc-toy-harness-run-20260616` | `ai_ml_competitions` | `EVALUATOR` | `python_stdlib` | `pass` |

## Contract Decision

This contract permits local JSONL preview exports only. Langfuse, Phoenix, OpenTelemetry, or any hosted collector remain future adapter targets and require a separate service/API/credential review before use.

## Boundary

- Observability backend calls: `false`
- Model/API calls: `false`
- Dependency installs/imports: `false`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
