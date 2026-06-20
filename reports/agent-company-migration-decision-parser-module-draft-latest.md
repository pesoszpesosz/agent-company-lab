# Agent Company Migration Decision Parser Module Draft

Generated UTC: 2026-06-19T22:35:23Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-module-draft-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-module-draft-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_module_draft_ready_for_report_only_module_fixtures`

Prepared a report-only parser module draft for migration operator decisions, including module sections, function blocks, guard mapping, result schema, and pseudocode.

## Module Sections

- `module_header_and_report_only_warning`
- `constants_and_allowed_decision_types`
- `result_schema`
- `guard_helpers`
- `parse_report_only_decision`
- `fixture_adapter`
- `error_and_refusal_mapping`
- `non_goal_boundaries`

## Function Blocks

- `load_decision_object`
- `guard_json_object_only`
- `guard_required_fields_present`
- `guard_known_decision_type`
- `guard_scope_boundaries`
- `guard_artifact_paths`
- `guard_expiration_and_signature`
- `build_report_only_result`
- `parse_report_only_decision`

## Pseudocode

```python
def parse_report_only_decision(decision: Mapping[str, object]) -> dict[str, object]:
    refusals = []
    refusals.extend(guard_json_object_only(decision))
    refusals.extend(guard_required_fields_present(decision))
    refusals.extend(guard_known_decision_type(decision))
    refusals.extend(guard_scope_boundaries(decision))
    refusals.extend(guard_artifact_paths(decision))
    refusals.extend(guard_expiration_and_signature(decision))
    return build_report_only_result(decision, refusals)
```

## Boundary

This is a report-only parser module draft. It does not write an importable parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Draft report-only module fixture checks next; do not install a parser module or parse live decisions.

