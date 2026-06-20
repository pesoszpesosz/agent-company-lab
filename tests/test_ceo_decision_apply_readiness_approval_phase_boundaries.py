import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_ceo_decision_apply_readiness_approval_facade_reexports_phase_modules() -> None:
    from agent_company_core import ceo_decision_apply_readiness_approval as facade
    from agent_company_core import ceo_decision_apply_readiness_operator_approval
    from agent_company_core import ceo_decision_apply_readiness_no_approval
    from agent_company_core import ceo_decision_apply_readiness_decision_intake

    assert (
        facade.write_ceo_decision_parser_apply_readiness_operator_approval_packet
        is ceo_decision_apply_readiness_operator_approval.write_ceo_decision_parser_apply_readiness_operator_approval_packet
    )
    assert (
        facade.write_ceo_decision_parser_apply_readiness_no_approval_blocker
        is ceo_decision_apply_readiness_no_approval.write_ceo_decision_parser_apply_readiness_no_approval_blocker
    )
    assert (
        facade.write_ceo_decision_parser_apply_readiness_decision_intake_packet
        is ceo_decision_apply_readiness_decision_intake.write_ceo_decision_parser_apply_readiness_decision_intake_packet
    )



def test_ceo_apply_readiness_operator_approval_content_builds_packet_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_apply_readiness_operator_approval_content import (
        build_ceo_apply_readiness_operator_approval_content,
    )

    content = build_ceo_apply_readiness_operator_approval_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/operator-packet.json",
        validation_path="reports/operator-packet-validation.json",
        source_runner_validation_path="reports/positive-runner-validation.json",
        lane_id="platform_engineering",
        packet_task_id="task-packet",
        packet_evidence_id="evidence-packet",
        source_runner_task_id="task-positive-runner",
        source_runner_evidence_id="evidence-positive-runner",
        readiness_packet={
            "target_request_id": "req-1",
            "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
            "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
            "rollback_checks": ["one", "two", "three", "four"],
            "required_operator_approvals": ["a", "b", "c", "d", "e"],
        },
        target_service_request_count=1,
        target_status_before="needs_review",
        target_status_after="needs_review",
    )

    payload = content["payload"]
    packet = content["operator_approval_packet"]
    markdown = content["markdown"]

    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_operator_approval_packet_ready_no_request"
    assert content["recommended_default"] == "wait_for_explicit_operator_apply_approval"
    assert content["operator_approval_packet_count"] == 1
    assert content["planned_field_update_count"] == 2
    assert content["rollback_check_count"] == 4
    assert content["required_operator_approval_count"] == 5
    assert content["approval_statement_count"] == 5
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert packet["target_request_id"] == "req-1"
    assert packet["approval_request_emitted"] is False
    assert packet["apply_command_enabled"] is False
    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_operator_approval_packet.v1"
    assert payload["operator_approval_packet"] == packet
    assert payload["source_runner_validation_path"] == "reports/positive-runner-validation.json"
    assert "Approve exact target request id: req-1" in markdown
    assert "This packet is a local artifact only" in markdown
    assert markdown.endswith("\n")

def test_ceo_apply_readiness_no_approval_content_blocks_without_mutation() -> None:
    from agent_company_core.ceo_decision_apply_readiness_no_approval_content import (
        build_ceo_apply_readiness_no_approval_content,
    )

    content = build_ceo_apply_readiness_no_approval_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/no-approval.json",
        validation_path="reports/no-approval-validation.json",
        source_packet_validation_path="reports/operator-packet-validation.json",
        lane_id="platform_engineering",
        blocker_task_id="task-blocker",
        blocker_evidence_id="evidence-blocker",
        source_packet_task_id="task-packet",
        source_packet_evidence_id="evidence-packet",
        operator_approval_packet={
            "target_request_id": "req-1",
            "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
            "approval_statements": ["a", "b", "c", "d", "e"],
            "apply_command_enabled": False,
            "approval_request_emitted": False,
        },
        target_service_request_count=1,
        target_status_before="needs_review",
        target_status_after="needs_review",
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_no_approval_blocked_no_mutation"
    assert content["recommended_default"] == "do_not_add_apply_command_until_explicit_operator_approval_exists"
    assert content["blocked_apply_attempt_count"] == 1
    assert content["blocked_reason_count"] == 4
    assert content["operator_approval_packet_count"] == 1
    assert content["planned_field_update_count"] == 2
    assert content["approval_statement_count"] == 5
    assert content["explicit_operator_approval_present"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_no_approval_blocker.v1"
    assert payload["simulated_apply_attempt"]["target_request_id"] == "req-1"
    assert payload["simulated_apply_attempt"]["mutation_applied"] is False
    assert payload["apply_command_enabled"] is False
    assert payload["approval_request_emitted"] is False
    assert "operator approval packet has not emitted an approval request" in markdown
    assert "This blocker is a local report-only simulation" in markdown
    assert markdown.endswith("\n")


def test_ceo_apply_readiness_no_approval_imports_content_helper() -> None:
    from agent_company_core import ceo_decision_apply_readiness_no_approval as no_approval
    from agent_company_core.ceo_decision_apply_readiness_no_approval_content import (
        build_ceo_apply_readiness_no_approval_content,
    )

    assert no_approval.build_ceo_apply_readiness_no_approval_content is build_ceo_apply_readiness_no_approval_content

