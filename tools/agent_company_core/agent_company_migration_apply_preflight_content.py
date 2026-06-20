from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def build_agent_company_migration_apply_preflight_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    lane_id: str,
    preflight_task_id: str,
    preflight_evidence_id: str,
    source_migration_task_id: str,
    source_migration_evidence_id: str,
    preflight_checks: Sequence[Any],
    operator_gates: Sequence[Any],
    dry_run_steps: Sequence[Any],
    apply_command_contract: Mapping[str, Any],
    rollback_drills: Sequence[Any],
) -> dict[str, Any]:
    preflight_check_list = list(preflight_checks)
    operator_gate_list = list(operator_gates)
    dry_run_step_list = list(dry_run_steps)
    rollback_drill_list = list(rollback_drills)
    apply_command_contract_payload = dict(apply_command_contract)
    apply_command_contract_payload["required_inputs"] = list(apply_command_contract.get("required_inputs", []))
    apply_command_contract_payload["must_refuse_when"] = list(apply_command_contract.get("must_refuse_when", []))
    local_decision = "agent_company_migration_apply_preflight_ready_for_operator_review_packet"
    recommended_default = "prepare_operator_review_next_without_running_apply_command"
    summary = "Prepared a report-only migration apply-preflight packet with checks, dry-run steps, command contract, rollback drills, and operator gates; the apply command remains disabled."
    next_action = "Prepare the operator review packet next, still without running the apply command or executing migration SQL."
    runtime_boundary = {
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
        "schema_version": "agent_company.migration_apply_preflight.v1",
        "generated_utc": generated_utc,
        "preflight_lane_id": lane_id,
        "preflight_task_id": preflight_task_id,
        "preflight_evidence_id": preflight_evidence_id,
        "source_migration_task_id": source_migration_task_id,
        "source_migration_evidence_id": source_migration_evidence_id,
        "preflight_packet_count": 1,
        "preflight_check_count": len(preflight_check_list),
        "operator_gate_count": len(operator_gate_list),
        "dry_run_step_count": len(dry_run_step_list),
        "apply_command_contract_count": 1,
        "rollback_drill_count": len(rollback_drill_list),
        "preflight_checks": preflight_check_list,
        "operator_gates": operator_gate_list,
        "dry_run_steps": dry_run_step_list,
        "apply_command_contract": apply_command_contract_payload,
        "rollback_drills": rollback_drill_list,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Apply Preflight",
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
        "## Preflight Checks",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in preflight_check_list)
    md_lines.extend(["", "## Operator Gates", ""])
    md_lines.extend(f"- `{item}`" for item in operator_gate_list)
    md_lines.extend(["", "## Dry Run Steps", ""])
    md_lines.extend(f"{idx}. `{item}`" for idx, item in enumerate(dry_run_step_list, start=1))
    md_lines.extend(
        [
            "",
            "## Apply Command Contract",
            "",
            f"- Command: `{apply_command_contract_payload['command_name']}`",
            f"- Default enabled: `{apply_command_contract_payload['default_enabled']}`",
            f"- Required inputs: {', '.join(apply_command_contract_payload['required_inputs'])}",
            f"- Refuse when: {', '.join(apply_command_contract_payload['must_refuse_when'])}",
            "",
            "## Rollback Drills",
            "",
        ]
    )
    md_lines.extend(f"- `{item}`" for item in rollback_drill_list)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This preflight packet does not enable or run an apply command. It does not execute migration SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = ["build_agent_company_migration_apply_preflight_artifacts"]
