from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence


def build_agent_company_migration_decision_parser_install_preflight_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    preflight_task_id: str,
    preflight_evidence_id: str,
    source_static_review_task_id: str,
    source_static_review_evidence_id: str,
    target_files: Sequence[dict[str, Any]],
    install_gates: Sequence[Any],
    preflight_checks: Sequence[Any],
    rollback_steps: Sequence[Any],
    approval_requirements: Sequence[Any],
) -> dict[str, Any]:
    target_file_list = [dict(item) for item in target_files]
    install_gate_list = list(install_gates)
    preflight_check_list = list(preflight_checks)
    rollback_step_list = list(rollback_steps)
    approval_requirement_list = list(approval_requirements)
    local_decision = "agent_company_migration_decision_parser_install_preflight_ready_for_operator_install_review"
    recommended_default = "hold_without_operator_approval_to_write_parser_module_file"
    summary = "Prepared a report-only install preflight for the migration decision parser module, with target file, gates, rollback steps, and operator approval requirements."
    next_action = "Prepare the operator install review packet next; do not write, install, import, or run the parser module."
    runtime_boundary = {
        "install_preflight_executed": True,
        "parser_module_file_written": False,
        "parser_module_imported": False,
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
        "schema_version": "agent_company.migration_decision_parser_install_preflight.v1",
        "generated_utc": generated_utc,
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "preflight_evidence_id": preflight_evidence_id,
        "source_static_review_task_id": source_static_review_task_id,
        "source_static_review_evidence_id": source_static_review_evidence_id,
        "install_preflight_count": 1,
        "install_gate_count": len(install_gate_list),
        "preflight_check_count": len(preflight_check_list),
        "rollback_step_count": len(rollback_step_list),
        "approval_requirement_count": len(approval_requirement_list),
        "target_file_count": len(target_file_list),
        "target_files": target_file_list,
        "install_gates": install_gate_list,
        "preflight_checks": preflight_check_list,
        "rollback_steps": rollback_step_list,
        "approval_requirements": approval_requirement_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Install Preflight",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        summary,
        "",
        "## Target File",
        "",
    ]
    md_lines.extend(f"- `{item['target_path']}`: {item['install_status']}" for item in target_file_list)
    md_lines.extend(["", "## Install Gates", ""])
    md_lines.extend(f"- `{item}`" for item in install_gate_list)
    md_lines.extend(["", "## Rollback Steps", ""])
    md_lines.extend(f"- `{item}`" for item in rollback_step_list)
    md_lines.extend(["", "## Approval Requirements", ""])
    md_lines.extend(f"- `{item}`" for item in approval_requirement_list)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only install preflight. It does not write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_agent_company_migration_decision_parser_install_preflight_artifacts"]
