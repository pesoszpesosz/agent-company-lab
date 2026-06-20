from __future__ import annotations


def build_signed_apply_command_contract_model(target_request_id: object) -> dict[str, object]:
    approval_granted_by_contract = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    apply_execution_allowed = False
    target_update_fields = ["approval_scope", "decision_note"]
    command_steps = [
        "load_operator_apply_approval_artifact",
        "verify_packet_schema_and_source_task",
        "verify_target_snapshot_is_current",
        "verify_all_required_fields_and_confirmations",
        "verify_no_external_side_effect_boundary",
        "build_single_row_parameterized_update_preview",
        "write_apply_result_and_rollback_artifacts",
    ]
    guard_checks = [
        "operator_signature_present",
        "approval_not_expired",
        "target_request_id_matches",
        "target_updated_at_matches_snapshot",
        "target_status_is_needs_review",
        "approved_fields_exactly_approval_scope_and_decision_note",
        "approval_scope_text_matches_packet",
        "decision_note_text_matches_packet",
        "no_worker_start_assignment_or_external_side_effect",
        "explicit_apply_execution_flag_true",
    ]
    rollback_steps = [
        "capture_pre_apply_service_request_row",
        "write_rollback_json_before_update",
        "on_failure_restore_approval_scope_and_decision_note_from_snapshot",
        "write_post_apply_audit_and_validation",
    ]
    bounded_update_shape = {
        "table": "service_requests",
        "where": ["request_id", "updated_at"],
        "set_fields": target_update_fields,
        "max_rows": 1,
        "requires_parameterized_sql": True,
        "requires_transaction": True,
    }
    apply_command_contract = {
        "command_name": "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command",
        "status": "contract_only_disabled",
        "target_request_id": target_request_id,
        "target_update_fields": target_update_fields,
        "command_steps": command_steps,
        "guard_checks": guard_checks,
        "rollback_steps": rollback_steps,
        "bounded_update_shape": bounded_update_shape,
        "approval_granted_by_contract": approval_granted_by_contract,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
    }
    return {
        "apply_command_contract": apply_command_contract,
        "approval_granted_by_contract": approval_granted_by_contract,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
        "target_update_fields": target_update_fields,
        "command_steps": command_steps,
        "guard_checks": guard_checks,
        "rollback_steps": rollback_steps,
        "bounded_update_shape": bounded_update_shape,
        "command_step_count": len(command_steps),
        "guard_check_count": len(guard_checks),
        "target_update_field_count": len(target_update_fields),
        "rollback_step_count": len(rollback_steps),
    }



def build_signed_apply_command_contract_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_packet_validation_path: str,
    lane_id: str,
    contract_task_id: str,
    contract_evidence_id: str,
    source_packet_task_id: str,
    source_packet_evidence_id: str,
    target_request_id: object,
    target_status_before: object,
    target_status_after: object,
) -> dict[str, object]:
    contract_model = build_signed_apply_command_contract_model(target_request_id)
    local_decision = "ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract_disabled_no_mutation"
    recommended_default = "implement_apply_command_only_after_explicit_operator_apply_approval"
    apply_command_contract_count = 1
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    contract_summary = (
        "Defined the local signed-decision apply-command contract with bounded update shape, guards, and rollback steps. The command remains disabled until explicit operator apply approval exists."
    )
    contract_next_action = (
        "Keep this as a contract-only artifact; implement or enable execution only after explicit operator apply approval is supplied and validated."
    )
    runtime_boundary = {
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
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract.v1",
        "generated_utc": generated_utc,
        "contract_lane_id": lane_id,
        "contract_task_id": contract_task_id,
        "contract_evidence_id": contract_evidence_id,
        "source_packet_task_id": source_packet_task_id,
        "source_packet_evidence_id": source_packet_evidence_id,
        "source_packet_validation_path": source_packet_validation_path,
        "apply_command_contract_count": apply_command_contract_count,
        "command_step_count": contract_model["command_step_count"],
        "guard_check_count": contract_model["guard_check_count"],
        "target_update_field_count": contract_model["target_update_field_count"],
        "rollback_step_count": contract_model["rollback_step_count"],
        "apply_command_contract": contract_model["apply_command_contract"],
        "approval_granted_by_contract": contract_model["approval_granted_by_contract"],
        "explicit_operator_apply_approval_present": contract_model["explicit_operator_apply_approval_present"],
        "apply_command_enabled": contract_model["apply_command_enabled"],
        "apply_execution_allowed": contract_model["apply_execution_allowed"],
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": contract_summary,
        "next_action": contract_next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Contract",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        contract_summary,
        "",
        "## Guard Checks",
        "",
    ]
    md_lines.extend(f"- `{check}`" for check in contract_model["guard_checks"])
    md_lines.extend(["", "## Command Steps", ""])
    md_lines.extend(f"- `{step}`" for step in contract_model["command_steps"])
    md_lines.extend(["", "## Rollback Steps", ""])
    md_lines.extend(f"- `{step}`" for step in contract_model["rollback_steps"])
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a contract-only artifact. It does not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            contract_next_action,
            "",
        ]
    )

    return {
        **contract_model,
        "apply_command_contract_count": apply_command_contract_count,
        "approval_request_count": approval_request_count,
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "mutation_applied_count": mutation_applied_count,
        "next_action": contract_next_action,
        "payload": payload,
        "queue_mutation_count": queue_mutation_count,
        "recommended_default": recommended_default,
        "runtime_boundary": runtime_boundary,
        "summary": contract_summary,
    }


__all__ = ["build_signed_apply_command_contract_content", "build_signed_apply_command_contract_model"]
