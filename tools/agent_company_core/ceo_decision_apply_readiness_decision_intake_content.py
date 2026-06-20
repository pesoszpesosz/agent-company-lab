from __future__ import annotations


def build_ceo_apply_readiness_decision_intake_model(
    *,
    operator_approval_packet: dict[str, object],
    source_blocker_task_id: str,
    artifact_output_path: str,
) -> dict[str, object]:
    planned_updates = operator_approval_packet.get("planned_field_updates", {})
    if not isinstance(planned_updates, dict):
        planned_updates = {}
    approval_statements = operator_approval_packet.get("approval_statements") or []
    rollback_snapshot = operator_approval_packet.get("rollback_snapshot", {})
    if not isinstance(rollback_snapshot, dict):
        rollback_snapshot = {}

    decision_fields = {
        "target_request_id": operator_approval_packet.get("target_request_id"),
        "approval_scope_text": planned_updates.get("approval_scope"),
        "decision_note_text": planned_updates.get("decision_note"),
        "operator_signature": None,
        "signed_decision_utc": None,
        "approval_expires_utc": None,
        "rollback_snapshot_updated_at": rollback_snapshot.get("updated_at"),
        "confirms_no_external_side_effects": None,
        "confirms_no_worker_start": None,
        "confirms_no_account_payment_public_security_real_money_action": None,
        "artifact_output_path": artifact_output_path,
        "rollback_plan_acknowledged": None,
    }
    requires = {
        "explicit_signed_decision": True,
        "exact_target_request_id": True,
        "approval_scope_text": True,
        "decision_note_text": True,
        "rollback_snapshot_match": True,
        "scope_expiration": True,
        "no_external_side_effects_default": True,
    }
    decision_intake_packet = {
        "packet_id": "ceo-decision-parser-apply-readiness-decision-intake-packet-20260616",
        "source_operator_approval_packet_id": operator_approval_packet.get("packet_id"),
        "source_no_approval_blocker_task_id": source_blocker_task_id,
        "decision_fields": decision_fields,
        "required_approval_statements": approval_statements,
        "approval_granted_by_intake_packet": False,
        "apply_command_enabled": False,
        "requires": requires,
    }
    return {
        "decision_fields": decision_fields,
        "decision_field_count": len(decision_fields),
        "approval_statements": approval_statements,
        "approval_statement_count": len(approval_statements),
        "approval_granted_by_intake_packet": False,
        "apply_command_enabled": False,
        "requires_explicit_signed_decision": requires["explicit_signed_decision"],
        "requires_exact_target_request_id": requires["exact_target_request_id"],
        "requires_approval_scope_text": requires["approval_scope_text"],
        "requires_decision_note_text": requires["decision_note_text"],
        "requires_rollback_snapshot_match": requires["rollback_snapshot_match"],
        "requires_scope_expiration": requires["scope_expiration"],
        "requires_no_external_side_effects_default": requires["no_external_side_effects_default"],
        "decision_intake_packet": decision_intake_packet,
    }

def build_ceo_apply_readiness_decision_intake_writer_content() -> dict[str, object]:
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
    return {
        "decision_intake_packet_count": 1,
        "approval_granted_by_intake_packet": False,
        "apply_command_enabled": False,
        "mutation_applied_count": 0,
        "queue_mutation_count": 0,
        "approval_request_count": 0,
        "summary": "Prepared a local decision-intake packet for the apply-readiness approval gate. It defines the exact fields required for a future signed operator decision, but grants no approval and keeps apply disabled.",
        "next_action": "Collect a separate explicit signed operator decision before adding or running any mutating apply command for this target request.",
        "boundary_text": "This packet is a local intake template only. It grants no approval, enables no apply command, updates no service request, emits no approval request, starts no worker, calls no API, opens no browser, and performs no account, wallet, payment, public, security-testing, external, or real-money action.",
        "runtime_boundary": runtime_boundary,
    }

def build_ceo_apply_readiness_decision_intake_writer_fields(
    *,
    operator_approval_packet: dict[str, object],
    source_blocker_task_id: str,
    artifact_output_path: str,
) -> dict[str, object]:
    intake_model = build_ceo_apply_readiness_decision_intake_model(
        operator_approval_packet=operator_approval_packet,
        source_blocker_task_id=source_blocker_task_id,
        artifact_output_path=artifact_output_path,
    )
    writer_content = build_ceo_apply_readiness_decision_intake_writer_content()
    return {
        **writer_content,
        "approval_statements": intake_model["approval_statements"],
        "approval_statement_count": intake_model["approval_statement_count"],
        "decision_fields": intake_model["decision_fields"],
        "decision_field_count": intake_model["decision_field_count"],
        "requires_explicit_signed_decision": intake_model["requires_explicit_signed_decision"],
        "requires_exact_target_request_id": intake_model["requires_exact_target_request_id"],
        "requires_approval_scope_text": intake_model["requires_approval_scope_text"],
        "requires_decision_note_text": intake_model["requires_decision_note_text"],
        "requires_rollback_snapshot_match": intake_model["requires_rollback_snapshot_match"],
        "requires_scope_expiration": intake_model["requires_scope_expiration"],
        "requires_no_external_side_effects_default": intake_model["requires_no_external_side_effects_default"],
        "decision_intake_packet": intake_model["decision_intake_packet"],
    }



def build_ceo_apply_readiness_decision_intake_artifacts(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_blocker_validation_path: str,
    lane_id: str,
    intake_task_id: str,
    intake_evidence_id: str,
    source_blocker_task_id: str,
    source_blocker_evidence_id: str,
    source_packet_task_id: str,
    blocked_apply_attempt_count: int,
    target_service_request_count: int,
    target_status_before: object,
    target_status_after: object,
    local_decision: str,
    recommended_default: str,
    writer_fields: dict[str, object],
) -> dict[str, object]:
    decision_fields = writer_fields["decision_fields"]
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_decision_intake_packet.v1",
        "generated_utc": generated_utc,
        "intake_lane_id": lane_id,
        "intake_task_id": intake_task_id,
        "intake_evidence_id": intake_evidence_id,
        "source_blocker_task_id": source_blocker_task_id,
        "source_blocker_evidence_id": source_blocker_evidence_id,
        "source_packet_task_id": source_packet_task_id,
        "source_blocker_validation_path": source_blocker_validation_path,
        "decision_intake_packet_count": writer_fields["decision_intake_packet_count"],
        "decision_field_count": writer_fields["decision_field_count"],
        "approval_statement_count": writer_fields["approval_statement_count"],
        "blocked_apply_attempt_count": blocked_apply_attempt_count,
        "target_service_request_count": target_service_request_count,
        "requires_explicit_signed_decision": writer_fields["requires_explicit_signed_decision"],
        "requires_exact_target_request_id": writer_fields["requires_exact_target_request_id"],
        "requires_approval_scope_text": writer_fields["requires_approval_scope_text"],
        "requires_decision_note_text": writer_fields["requires_decision_note_text"],
        "requires_rollback_snapshot_match": writer_fields["requires_rollback_snapshot_match"],
        "requires_scope_expiration": writer_fields["requires_scope_expiration"],
        "requires_no_external_side_effects_default": writer_fields["requires_no_external_side_effects_default"],
        "approval_granted_by_intake_packet": writer_fields["approval_granted_by_intake_packet"],
        "apply_command_enabled": writer_fields["apply_command_enabled"],
        "mutation_applied_count": writer_fields["mutation_applied_count"],
        "queue_mutation_count": writer_fields["queue_mutation_count"],
        "approval_request_count": writer_fields["approval_request_count"],
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "decision_intake_packet": writer_fields["decision_intake_packet"],
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": writer_fields["summary"],
        "next_action": writer_fields["next_action"],
        "runtime_boundary": writer_fields["runtime_boundary"],
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Decision Intake Packet",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        str(writer_fields["summary"]),
        "",
        "## Required Fields",
        "",
    ]
    for field_name in decision_fields:
        md_lines.append(f"- `{field_name}`")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            str(writer_fields["boundary_text"]),
            "",
            "## Next Action",
            "",
            str(writer_fields["next_action"]),
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}
