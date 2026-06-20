# Agent Company Migration Decision Parser Static Review

Generated UTC: 2026-06-16T12:30:26Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-static-review-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-static-review-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_static_review_ready_for_report_only_install_preflight`

Static-reviewed the report-only parser module file draft; all source checks passed and no issues were found without writing or importing a parser module.

## Static Checks

| Check | Passed |
| --- | --- |
| `has_report_only_docstring` | `True` |
| `has_allowed_decision_types` | `True` |
| `has_required_fields` | `True` |
| `has_json_object_guard` | `True` |
| `has_scope_guard` | `True` |
| `has_artifact_guard` | `True` |
| `has_expiration_signature_guard` | `True` |
| `has_result_builder` | `True` |
| `has_parse_entrypoint` | `True` |
| `result_always_report_only` | `True` |
| `no_apply_or_service_mutation_calls` | `True` |

## Recommendations

- Keep the first installed version behind a report-only command flag.
- Run the saved 12-fixture suite after writing any real module file.
- Require static review to pass before importing the parser module.
- Keep live operator decision parsing disabled until a signed operator approval exists.
- Preserve service request and migration boundaries as hard parser guards.

## Boundary

This is a report-only static review. It does not write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Draft the report-only install preflight next; do not write, install, import, or run the parser module.

