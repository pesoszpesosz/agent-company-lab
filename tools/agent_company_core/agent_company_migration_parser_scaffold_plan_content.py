from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence


PARSER_STAGES = [
    "load_json_object",
    "require_exact_field_set",
    "validate_decision_type",
    "validate_scope_boundaries",
    "validate_artifact_paths",
    "validate_expiration_and_signature",
    "emit_report_only_result",
]

GUARD_FUNCTIONS = [
    "guard_json_object_only",
    "guard_required_fields_present",
    "guard_known_decision_type",
    "guard_no_live_apply_scope",
    "guard_no_external_or_gated_action_scope",
    "guard_artifact_paths_match_review_packet",
    "guard_not_expired",
    "guard_signed_timestamp_present",
    "guard_result_is_report_only",
]

ACCEPTED_DECISION_TYPES = [
    "hold",
    "approve_sandbox_dry_run_only",
    "request_rework",
    "reject_migration_path",
]

RESULT_FIELDS = [
    "accepted",
    "decision_type",
    "result_state",
    "refusal_reasons",
    "artifact_paths",
    "expires_at",
    "signed_utc",
    "report_only",
]

REFUSAL_REASONS = [
    "missing_required_fields",
    "unknown_decision_type",
    "forbidden_scope",
    "missing_artifact_paths",
    "expired_or_missing_expiration",
    "unsigned_decision",
    "artifact_path_mismatch",
    "not_json_object",
]


def build_agent_company_migration_decision_parser_scaffold_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    scaffold_task_id: str,
    scaffold_evidence_id: str,
    source_runner_task_id: str,
    source_runner_evidence_id: str,
    fixture_coverage: Sequence[Any],
) -> dict[str, Any]:
    local_decision = "agent_company_migration_decision_parser_scaffold_ready_for_report_only_parser_module"
    recommended_default = "draft_report_only_parser_module_next_without_live_decision_intake"
    summary = "Prepared a report-only parser scaffold for migration operator decisions, grounded in the passing fixture runner and explicit guard/result schemas."
    next_action = "Draft the report-only parser module next; do not parse live decisions or apply operator decisions."
    runtime_boundary = {
        "parser_module_written": False,
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
    fixture_coverage_list = list(fixture_coverage)
    payload = {
        "schema_version": "agent_company.migration_decision_parser_scaffold.v1",
        "generated_utc": generated_utc,
        "scaffold_lane_id": lane_id,
        "scaffold_task_id": scaffold_task_id,
        "scaffold_evidence_id": scaffold_evidence_id,
        "source_runner_task_id": source_runner_task_id,
        "source_runner_evidence_id": source_runner_evidence_id,
        "parser_scaffold_count": 1,
        "parser_stage_count": len(PARSER_STAGES),
        "guard_function_count": len(GUARD_FUNCTIONS),
        "accepted_decision_type_count": len(ACCEPTED_DECISION_TYPES),
        "result_field_count": len(RESULT_FIELDS),
        "refusal_reason_count": len(REFUSAL_REASONS),
        "fixture_coverage_count": len(fixture_coverage_list),
        "parser_stages": list(PARSER_STAGES),
        "guard_functions": list(GUARD_FUNCTIONS),
        "accepted_decision_types": list(ACCEPTED_DECISION_TYPES),
        "result_fields": list(RESULT_FIELDS),
        "refusal_reasons": list(REFUSAL_REASONS),
        "fixture_coverage": fixture_coverage_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Scaffold",
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
        "## Parser Stages",
        "",
    ]
    md_lines.extend(f"{idx}. `{item}`" for idx, item in enumerate(PARSER_STAGES, start=1))
    md_lines.extend(["", "## Guard Functions", ""])
    md_lines.extend(f"- `{item}`" for item in GUARD_FUNCTIONS)
    md_lines.extend(["", "## Result Fields", ""])
    md_lines.extend(f"- `{item}`" for item in RESULT_FIELDS)
    md_lines.extend(["", "## Refusal Reasons", ""])
    md_lines.extend(f"- `{item}`" for item in REFUSAL_REASONS)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This scaffold is report-only. It does not write a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "ACCEPTED_DECISION_TYPES",
    "GUARD_FUNCTIONS",
    "PARSER_STAGES",
    "REFUSAL_REASONS",
    "RESULT_FIELDS",
    "build_agent_company_migration_decision_parser_scaffold_artifacts",
]
