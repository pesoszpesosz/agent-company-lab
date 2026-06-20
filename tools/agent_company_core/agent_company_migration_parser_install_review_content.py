from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence


def build_agent_company_migration_decision_parser_install_review_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    review_task_id: str,
    review_evidence_id: str,
    source_preflight_task_id: str,
    source_preflight_evidence_id: str,
    decision_options: Sequence[dict[str, Any]],
    approval_conditions: Sequence[Any],
    refusal_conditions: Sequence[Any],
    evidence_links: Sequence[Any],
    operator_instructions: Sequence[Any],
) -> dict[str, Any]:
    decision_option_list = [dict(item) for item in decision_options]
    approval_condition_list = list(approval_conditions)
    refusal_condition_list = list(refusal_conditions)
    evidence_link_list = list(evidence_links)
    operator_instruction_list = list(operator_instructions)
    local_decision = "agent_company_migration_decision_parser_install_review_ready_for_signed_install_decision_or_hold"
    recommended_default = "hold_without_signed_operator_file_write_approval"
    summary = "Prepared a report-only operator review packet for the parser module install preflight, with hold as the default and one-file-write approval boundaries."
    next_action = "Wait for a signed operator install decision or draft a report-only install-decision intake contract."
    runtime_boundary = {
        "operator_install_decision_applied": False,
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
        "schema_version": "agent_company.migration_decision_parser_install_review.v1",
        "generated_utc": generated_utc,
        "review_lane_id": lane_id,
        "review_task_id": review_task_id,
        "review_evidence_id": review_evidence_id,
        "source_preflight_task_id": source_preflight_task_id,
        "source_preflight_evidence_id": source_preflight_evidence_id,
        "install_review_count": 1,
        "decision_option_count": len(decision_option_list),
        "approval_condition_count": len(approval_condition_list),
        "refusal_condition_count": len(refusal_condition_list),
        "evidence_link_count": len(evidence_link_list),
        "operator_instruction_count": len(operator_instruction_list),
        "decision_options": decision_option_list,
        "approval_conditions": approval_condition_list,
        "refusal_conditions": refusal_condition_list,
        "evidence_links": evidence_link_list,
        "operator_instructions": operator_instruction_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Parser Install Review",
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
        "## Decision Options",
        "",
    ]
    for item in decision_option_list:
        marker = " default" if item["default"] else ""
        md_lines.append(f"- `{item['option']}`{marker}: {item['effect']}")
    md_lines.extend(["", "## Approval Conditions", ""])
    md_lines.extend(f"- {item}" for item in approval_condition_list)
    md_lines.extend(["", "## Refusal Conditions", ""])
    md_lines.extend(f"- {item}" for item in refusal_condition_list)
    md_lines.extend(["", "## Operator Instructions", ""])
    md_lines.extend(f"- {item}" for item in operator_instruction_list)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a report-only operator review packet. It does not apply an install decision, write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_agent_company_migration_decision_parser_install_review_artifacts"]
