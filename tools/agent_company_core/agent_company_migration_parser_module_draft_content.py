from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence


MODULE_SECTIONS = [
    "module_header_and_report_only_warning",
    "constants_and_allowed_decision_types",
    "result_schema",
    "guard_helpers",
    "parse_report_only_decision",
    "fixture_adapter",
    "error_and_refusal_mapping",
    "non_goal_boundaries",
]

FUNCTION_BLOCKS = [
    "load_decision_object",
    "guard_json_object_only",
    "guard_required_fields_present",
    "guard_known_decision_type",
    "guard_scope_boundaries",
    "guard_artifact_paths",
    "guard_expiration_and_signature",
    "build_report_only_result",
    "parse_report_only_decision",
]

MODULE_PSEUDOCODE = [
    "def parse_report_only_decision(decision: Mapping[str, object]) -> dict[str, object]:",
    "    refusals = []",
    "    refusals.extend(guard_json_object_only(decision))",
    "    refusals.extend(guard_required_fields_present(decision))",
    "    refusals.extend(guard_known_decision_type(decision))",
    "    refusals.extend(guard_scope_boundaries(decision))",
    "    refusals.extend(guard_artifact_paths(decision))",
    "    refusals.extend(guard_expiration_and_signature(decision))",
    "    return build_report_only_result(decision, refusals)",
]


def build_agent_company_migration_decision_parser_module_draft_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    module_task_id: str,
    module_evidence_id: str,
    source_scaffold_task_id: str,
    source_scaffold_evidence_id: str,
    guard_functions: Sequence[Any],
    accepted_decision_types: Sequence[Any],
    result_fields: Sequence[Any],
    refusal_reasons: Sequence[Any],
    fixture_coverage: Sequence[Any],
) -> dict[str, Any]:
    guard_function_list = list(guard_functions)
    accepted_decision_type_list = list(accepted_decision_types)
    result_field_list = list(result_fields)
    refusal_reason_list = list(refusal_reasons)
    fixture_coverage_list = list(fixture_coverage)
    local_decision = "agent_company_migration_decision_parser_module_draft_ready_for_report_only_module_fixtures"
    recommended_default = "draft_report_only_module_fixture_check_next_without_installing_parser_module"
    summary = "Prepared a report-only parser module draft for migration operator decisions, including module sections, function blocks, guard mapping, result schema, and pseudocode."
    next_action = "Draft report-only module fixture checks next; do not install a parser module or parse live decisions."
    runtime_boundary = {
        "parser_module_file_written": False,
        "live_decisions_parsed": False,
        "operator_decision_applied": False,
        "migration_sql_executed": False,
        "apply_command_enabled": False,
        "tables_created": 0,
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "agent_company.migration_decision_parser_module_draft.v1",
        "generated_utc": generated_utc,
        "module_lane_id": lane_id,
        "module_task_id": module_task_id,
        "module_evidence_id": module_evidence_id,
        "source_scaffold_task_id": source_scaffold_task_id,
        "source_scaffold_evidence_id": source_scaffold_evidence_id,
        "parser_module_draft_count": 1,
        "module_section_count": len(MODULE_SECTIONS),
        "function_block_count": len(FUNCTION_BLOCKS),
        "guard_function_count": len(guard_function_list),
        "accepted_decision_type_count": len(accepted_decision_type_list),
        "result_field_count": len(result_field_list),
        "refusal_reason_count": len(refusal_reason_list),
        "fixture_coverage_count": len(fixture_coverage_list),
        "module_sections": list(MODULE_SECTIONS),
        "function_blocks": list(FUNCTION_BLOCKS),
        "guard_functions": guard_function_list,
        "accepted_decision_types": accepted_decision_type_list,
        "result_fields": result_field_list,
        "refusal_reasons": refusal_reason_list,
        "fixture_coverage": fixture_coverage_list,
        "module_pseudocode": list(MODULE_PSEUDOCODE),
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Module Draft",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        summary,
        "",
        "## Module Sections",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in MODULE_SECTIONS)
    md_lines.extend(["", "## Function Blocks", ""])
    md_lines.extend(f"- `{item}`" for item in FUNCTION_BLOCKS)
    md_lines.extend(["", "## Pseudocode", "", "```python"])
    md_lines.extend(MODULE_PSEUDOCODE)
    md_lines.extend(
        [
            "```",
            "",
            "## Boundary",
            "",
            "This is a report-only parser module draft. It does not write an importable parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "FUNCTION_BLOCKS",
    "MODULE_PSEUDOCODE",
    "MODULE_SECTIONS",
    "build_agent_company_migration_decision_parser_module_draft_artifacts",
]
