import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_ceo_decision_apply_readiness_facades_reexport_phase_modules() -> None:
    import agent_company_core.ceo_decision_apply_readiness as readiness_facade
    import agent_company_core.ceo_decisions as ceo_facade
    from agent_company_core import ceo_decision_apply_readiness_approval
    from agent_company_core import ceo_decision_apply_readiness_base
    from agent_company_core import ceo_decision_apply_readiness_fixtures

    assert (
        readiness_facade.write_ceo_decision_parser_apply_readiness
        is ceo_decision_apply_readiness_base.write_ceo_decision_parser_apply_readiness
    )
    assert (
        readiness_facade.write_ceo_decision_parser_apply_readiness_guard_runner
        is ceo_decision_apply_readiness_fixtures.write_ceo_decision_parser_apply_readiness_guard_runner
    )
    assert (
        readiness_facade.write_ceo_decision_parser_apply_readiness_positive_runner
        is ceo_decision_apply_readiness_fixtures.write_ceo_decision_parser_apply_readiness_positive_runner
    )
    assert (
        readiness_facade.write_ceo_decision_parser_apply_readiness_decision_intake_packet
        is ceo_decision_apply_readiness_approval.write_ceo_decision_parser_apply_readiness_decision_intake_packet
    )
    assert (
        ceo_facade.write_ceo_decision_parser_apply_readiness_no_approval_blocker
        is ceo_decision_apply_readiness_approval.write_ceo_decision_parser_apply_readiness_no_approval_blocker
    )


def test_ceo_apply_readiness_shared_evaluator_accepts_preview_only_packet() -> None:
    from agent_company_core.ceo_decision_apply_readiness_evaluator import evaluate_ceo_apply_readiness_packet

    packet = {
        "required_operator_approvals": ["a", "b", "c", "d", "e"],
        "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        "target_updated_at_before": "2026-06-19T00:00:00Z",
        "target_status_before": "needs_review",
        "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
        "planned_update_sql_shape": {"table": "service_requests", "max_rows": 1},
        "apply_boundary": {
            "worker_starts": 0,
            "external_side_effects": False,
            "service_requests_updated": 0,
            "apply_allowed_now": False,
            "requires_explicit_operator_apply_approval": True,
        },
    }

    result = evaluate_ceo_apply_readiness_packet(packet, require_preview_apply_boundary=True)

    assert result["accepted_readiness"] is True
    assert result["preview_state"] == "readiness_packet_valid_apply_still_disabled"
    assert result["real_mutation_allowed"] is False


def test_ceo_apply_readiness_shared_evaluator_rejects_drift() -> None:
    from agent_company_core.ceo_decision_apply_readiness_evaluator import evaluate_ceo_apply_readiness_packet

    result = evaluate_ceo_apply_readiness_packet({"required_operator_approvals": []})

    assert result["accepted_readiness"] is False
    assert result["rule_id"] == "reject_missing_operator_approval_bundle"


def test_ceo_apply_readiness_decision_intake_content_model_is_non_approving_template() -> None:
    from agent_company_core.ceo_decision_apply_readiness_decision_intake_content import (
        build_ceo_apply_readiness_decision_intake_model,
    )

    model = build_ceo_apply_readiness_decision_intake_model(
        operator_approval_packet={
            "packet_id": "packet-1",
            "target_request_id": "req-1",
            "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
            "approval_statements": ["a", "b", "c", "d", "e"],
            "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        },
        source_blocker_task_id="task-blocker",
        artifact_output_path="reports/intake.json",
    )

    assert model["decision_field_count"] == 12
    assert model["approval_statement_count"] == 5
    assert model["approval_granted_by_intake_packet"] is False
    assert model["apply_command_enabled"] is False
    assert model["requires_explicit_signed_decision"] is True
    assert model["requires_exact_target_request_id"] is True
    assert model["requires_no_external_side_effects_default"] is True
    assert model["decision_fields"]["target_request_id"] == "req-1"
    assert model["decision_fields"]["approval_scope_text"] == "scope"
    assert model["decision_fields"]["decision_note_text"] == "note"
    assert model["decision_fields"]["operator_signature"] is None
    assert model["decision_intake_packet"]["source_operator_approval_packet_id"] == "packet-1"
    assert model["decision_intake_packet"]["source_no_approval_blocker_task_id"] == "task-blocker"
    assert model["decision_intake_packet"]["requires"]["scope_expiration"] is True

def test_ceo_apply_readiness_positive_runner_content_summarizes_preview_only_fixture() -> None:
    from agent_company_core.ceo_decision_apply_readiness_positive_runner_content import (
        build_positive_readiness_runner_content,
    )

    readiness_packet = {
        "required_operator_approvals": ["a", "b", "c", "d", "e"],
        "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        "target_updated_at_before": "2026-06-19T00:00:00Z",
        "target_status_before": "needs_review",
        "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
        "planned_update_sql_shape": {"table": "service_requests", "max_rows": 1},
        "apply_boundary": {
            "worker_starts": 0,
            "external_side_effects": False,
            "service_requests_updated": 0,
            "apply_allowed_now": False,
            "requires_explicit_operator_apply_approval": True,
        },
    }
    fixture = {
        "fixture_id": "positive-readiness",
        "expected_accepted": True,
        "expected_preview_state": "readiness_packet_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }

    content = build_positive_readiness_runner_content(fixture, readiness_packet)

    assert content["readiness_guard_execution_count"] == 1
    assert content["accepted_readiness_count"] == 1
    assert content["rejected_readiness_count"] == 0
    assert content["expected_acceptance_match_count"] == 1
    assert content["preview_state_match_count"] == 1
    assert content["real_mutation_allowed_count"] == 0
    assert content["readiness_guard_results"] == [
        {
            "fixture_id": "positive-readiness",
            "expected_accepted": True,
            "actual_accepted": True,
            "expected_preview_state": "readiness_packet_valid_apply_still_disabled",
            "actual_preview_state": "readiness_packet_valid_apply_still_disabled",
            "expected_real_mutation": False,
            "actual_real_mutation_allowed": False,
            "actual_rule_id": None,
            "matched_expected": True,
        }
    ]

def test_ceo_apply_readiness_decision_intake_writer_content_is_no_approval_boundary() -> None:
    from agent_company_core.ceo_decision_apply_readiness_decision_intake_content import (
        build_ceo_apply_readiness_decision_intake_writer_content,
    )

    content = build_ceo_apply_readiness_decision_intake_writer_content()

    assert content["decision_intake_packet_count"] == 1
    assert content["approval_granted_by_intake_packet"] is False
    assert content["apply_command_enabled"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "grants no approval" in content["summary"]
    assert "Collect a separate explicit signed operator decision" in content["next_action"]
    assert "This packet is a local intake template only" in content["boundary_text"]



def test_ceo_apply_readiness_positive_runner_content_carries_preview_only_boundary_defaults() -> None:
    from agent_company_core.ceo_decision_apply_readiness_positive_runner_content import (
        build_positive_readiness_runner_content,
    )

    readiness_packet = {
        "required_operator_approvals": ["a", "b", "c", "d", "e"],
        "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        "target_updated_at_before": "2026-06-19T00:00:00Z",
        "target_status_before": "needs_review",
        "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
        "planned_update_sql_shape": {"table": "service_requests", "max_rows": 1},
        "apply_boundary": {
            "worker_starts": 0,
            "external_side_effects": False,
            "service_requests_updated": 0,
            "apply_allowed_now": False,
            "requires_explicit_operator_apply_approval": True,
        },
    }
    fixture = {
        "fixture_id": "positive-readiness",
        "expected_accepted": True,
        "expected_preview_state": "readiness_packet_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }

    content = build_positive_readiness_runner_content(fixture, readiness_packet)

    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_positive_runner_passed_preview_only"
    assert content["recommended_default"] == "positive_runner_still_requires_separate_operator_apply_approval"
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "preview-only state" in content["summary"]
    assert "separate explicit operator apply approval" in content["next_action"]



def test_ceo_apply_readiness_positive_runner_artifacts_render_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_apply_readiness_positive_runner_content import (
        build_positive_readiness_runner_artifacts,
        build_positive_readiness_runner_content,
    )

    readiness_packet = {
        "required_operator_approvals": ["a", "b", "c", "d", "e"],
        "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        "target_updated_at_before": "2026-06-19T00:00:00Z",
        "target_status_before": "needs_review",
        "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
        "planned_update_sql_shape": {"table": "service_requests", "max_rows": 1},
        "apply_boundary": {
            "worker_starts": 0,
            "external_side_effects": False,
            "service_requests_updated": 0,
            "apply_allowed_now": False,
            "requires_explicit_operator_apply_approval": True,
        },
    }
    fixture = {
        "fixture_id": "positive-readiness",
        "expected_accepted": True,
        "expected_preview_state": "readiness_packet_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }
    runner_content = build_positive_readiness_runner_content(fixture, readiness_packet)

    artifacts = build_positive_readiness_runner_artifacts(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/positive-runner.json",
        validation_path="reports/positive-runner.validation.json",
        source_fixture_validation_path="reports/positive-fixture.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-positive-runner",
        runner_evidence_id="evidence-positive-runner",
        source_fixture_task_id="task-positive-fixture",
        source_fixture_evidence_id="evidence-positive-fixture",
        positive_readiness_fixture_count=1,
        target_service_request_count=1,
        planned_field_update_count=2,
        rollback_check_count=4,
        required_operator_approval_count=5,
        target_status_before="needs_review",
        target_status_after="needs_review",
        runner_content=runner_content,
    )

    payload = artifacts["payload"]
    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_positive_runner.v1"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["source_fixture_validation_path"] == "reports/positive-fixture.validation.json"
    assert payload["positive_readiness_fixture_count"] == 1
    assert payload["planned_field_update_count"] == 2
    assert payload["readiness_guard_execution_count"] == 1
    assert payload["accepted_readiness_count"] == 1
    assert payload["mutation_applied_count"] == 0
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["readiness_guard_results"][0]["fixture_id"] == "positive-readiness"

    markdown = artifacts["markdown"]
    assert "# CEO Decision Parser Apply Readiness Positive Runner" in markdown
    assert "`ceo_decision_parser_apply_readiness_positive_runner_passed_preview_only`" in markdown
    assert "| `positive-readiness` | `True` | `readiness_packet_valid_apply_still_disabled` | `False` | `True` |" in markdown
    assert "This runner is report-only" in markdown
    assert "separate explicit operator apply approval" in markdown
    assert markdown.endswith("\n")

def test_ceo_apply_readiness_decision_intake_content_flattens_writer_fields():
    from agent_company_core.ceo_decision_apply_readiness_decision_intake_content import (
        build_ceo_apply_readiness_decision_intake_writer_fields,
    )

    fields = build_ceo_apply_readiness_decision_intake_writer_fields(
        operator_approval_packet={
            "packet_id": "packet-1",
            "target_request_id": "req-1",
            "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
            "approval_statements": ["a", "b", "c", "d", "e"],
            "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        },
        source_blocker_task_id="task-blocker",
        artifact_output_path="reports/intake.json",
    )

    assert fields["decision_intake_packet_count"] == 1
    assert fields["decision_field_count"] == 12
    assert fields["approval_statement_count"] == 5
    assert fields["approval_granted_by_intake_packet"] is False
    assert fields["apply_command_enabled"] is False
    assert fields["mutation_applied_count"] == 0
    assert fields["queue_mutation_count"] == 0
    assert fields["approval_request_count"] == 0
    assert fields["requires_explicit_signed_decision"] is True
    assert fields["requires_exact_target_request_id"] is True
    assert fields["requires_no_external_side_effects_default"] is True
    assert fields["decision_fields"]["target_request_id"] == "req-1"
    assert fields["decision_intake_packet"]["source_no_approval_blocker_task_id"] == "task-blocker"
    assert fields["runtime_boundary"]["service_requests_updated"] == 0
    assert "grants no approval" in fields["summary"]


def test_ceo_apply_readiness_base_content_builds_no_apply_packet() -> None:
    from agent_company_core.ceo_decision_apply_readiness_base_content import (
        build_ceo_apply_readiness_base_content,
    )

    content = build_ceo_apply_readiness_base_content(
        target_request_id="req-1",
        target_request={
            "status": "needs_review",
            "approval_scope": None,
            "decision_note": None,
            "updated_at": "2026-06-19T00:00:00Z",
        },
        planned_updates={"approval_scope": "scope", "decision_note": "note"},
    )

    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_ready_no_apply"
    assert content["recommended_default"] == "hold_for_explicit_operator_apply_approval"
    assert content["readiness_packet_count"] == 1
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["planned_field_update_count"] == 2
    assert content["rollback_check_count"] == 4
    assert content["required_operator_approval_count"] == 5
    assert content["rollback_checks"] == [
        "snapshot target service request before apply",
        "verify status count delta is zero except intended field update",
        "restore approval_scope and decision_note to previous values on failure",
        "write post-apply validation artifact before any worker start",
    ]
    assert content["required_operator_approvals"][-1] == "confirm rollback snapshot is captured before apply"
    assert content["readiness_packet"]["target_request_id"] == "req-1"
    assert content["readiness_packet"]["planned_update_sql_shape"]["set_fields"] == ["approval_scope", "decision_note"]
    assert content["readiness_packet"]["rollback_snapshot"]["updated_at"] == "2026-06-19T00:00:00Z"
    assert content["readiness_packet"]["apply_boundary"]["apply_allowed_now"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "single service-request preview" in content["summary"]
    assert "Hold real apply disabled" in content["next_action"]


def test_ceo_apply_readiness_base_imports_content_helper() -> None:
    from agent_company_core import ceo_decision_apply_readiness_base as readiness_base
    from agent_company_core.ceo_decision_apply_readiness_base_content import (
        build_ceo_apply_readiness_base_content,
    )

    assert readiness_base.build_ceo_apply_readiness_base_content is build_ceo_apply_readiness_base_content


def test_ceo_apply_readiness_decision_intake_artifacts_render_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_apply_readiness_decision_intake_content import (
        build_ceo_apply_readiness_decision_intake_artifacts,
        build_ceo_apply_readiness_decision_intake_writer_fields,
    )

    writer_fields = build_ceo_apply_readiness_decision_intake_writer_fields(
        operator_approval_packet={
            "packet_id": "packet-1",
            "target_request_id": "req-1",
            "planned_field_updates": {"approval_scope": "scope", "decision_note": "note"},
            "approval_statements": ["a", "b", "c", "d", "e"],
            "rollback_snapshot": {"updated_at": "2026-06-19T00:00:00Z"},
        },
        source_blocker_task_id="task-blocker",
        artifact_output_path="reports/intake.json",
    )

    artifacts = build_ceo_apply_readiness_decision_intake_artifacts(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/intake.json",
        validation_path="reports/intake-validation.json",
        source_blocker_validation_path="reports/blocker-validation.json",
        lane_id="platform_engineering",
        intake_task_id="task-intake",
        intake_evidence_id="evidence-intake",
        source_blocker_task_id="task-blocker",
        source_blocker_evidence_id="evidence-blocker",
        source_packet_task_id="task-packet",
        blocked_apply_attempt_count=1,
        target_service_request_count=1,
        target_status_before="needs_review",
        target_status_after="needs_review",
        local_decision="ceo_decision_parser_apply_readiness_decision_intake_packet_ready_no_approval",
        recommended_default="collect_signed_operator_decision_before_apply_command",
        writer_fields=writer_fields,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_decision_intake_packet.v1"
    assert payload["decision_intake_packet_count"] == 1
    assert payload["decision_field_count"] == 12
    assert payload["approval_statement_count"] == 5
    assert payload["approval_granted_by_intake_packet"] is False
    assert payload["apply_command_enabled"] is False
    assert payload["mutation_applied_count"] == 0
    assert payload["queue_mutation_count"] == 0
    assert payload["approval_request_count"] == 0
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["runtime_boundary"]["external_side_effects"] is False
    assert payload["decision_intake_packet"]["source_no_approval_blocker_task_id"] == "task-blocker"
    assert "# CEO Decision Parser Apply Readiness Decision Intake Packet" in markdown
    assert "`ceo_decision_parser_apply_readiness_decision_intake_packet_ready_no_approval`" in markdown
    assert "- `target_request_id`" in markdown
    assert "This packet is a local intake template only" in markdown
    assert markdown.endswith("\n")


def test_ceo_apply_readiness_decision_intake_imports_artifact_helper() -> None:
    from agent_company_core import ceo_decision_apply_readiness_decision_intake as decision_intake
    from agent_company_core.ceo_decision_apply_readiness_decision_intake_content import (
        build_ceo_apply_readiness_decision_intake_artifacts,
    )

    assert (
        decision_intake.build_ceo_apply_readiness_decision_intake_artifacts
        is build_ceo_apply_readiness_decision_intake_artifacts
    )

