import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_ceo_decision_signed_apply_command_facades_reexport_phase_modules() -> None:
    import agent_company_core.ceo_decision_signed_apply_command as apply_facade
    import agent_company_core.ceo_decisions as ceo_facade
    from agent_company_core import ceo_decision_signed_apply_closeout
    from agent_company_core import ceo_decision_signed_apply_command_contract
    from agent_company_core import ceo_decision_signed_apply_command_fixtures
    from agent_company_core import ceo_decision_signed_apply_preflight

    assert (
        apply_facade.write_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight
        is ceo_decision_signed_apply_preflight.write_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet
        is ceo_decision_signed_apply_preflight.write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract
        is ceo_decision_signed_apply_command_contract.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner
        is ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
        is ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
    )
    assert (
        ceo_facade.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout
        is ceo_decision_signed_apply_closeout.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout
    )
def test_ceo_decision_signed_apply_preflight_facade_reexports_phase_modules() -> None:
    from agent_company_core import ceo_decision_signed_apply_operator_approval_packet
    from agent_company_core import ceo_decision_signed_apply_preflight
    from agent_company_core import ceo_decision_signed_apply_preflight_check

    assert (
        ceo_decision_signed_apply_preflight.write_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight
        is ceo_decision_signed_apply_preflight_check.write_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight
    )
    assert (
        ceo_decision_signed_apply_preflight.write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet
        is ceo_decision_signed_apply_operator_approval_packet.write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet
    )



def test_signed_apply_command_shared_evaluator_accepts_positive_fixture() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_evaluator import evaluate_signed_apply_command_positive_fixture

    fixture = {
        "confirmations": {f"confirm_{index}": True for index in range(6)},
        "required_fields_present": [f"field_{index}" for index in range(8)],
        "operator_signature": "LOCAL_FIXTURE_SIGNATURE_NOT_REAL_APPROVAL",
        "target_request_id": "req-1",
        "rollback_snapshot_updated_at": "2026-06-14T14:37:52Z",
        "target_update_fields": ["approval_scope", "decision_note"],
        "explicit_apply_execution_flag": True,
        "expected_real_mutation": False,
    }

    result = evaluate_signed_apply_command_positive_fixture(fixture, target_request_id="req-1")

    assert result["accepted"] is True
    assert result["preview_state"] == "positive_apply_command_fixture_valid_apply_still_disabled"
    assert result["real_mutation_allowed"] is False


def test_signed_apply_command_shared_evaluator_rejects_negative_override() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_evaluator import evaluate_signed_apply_command_negative_fixture

    result = evaluate_signed_apply_command_negative_fixture(
        {"input_overrides": {"explicit_apply_execution_flag": False}},
        target_request_id="req-1",
    )

    assert result["accepted"] is False
    assert result["rule_id"] == "reject_missing_explicit_execution_flag"


def test_signed_apply_command_contract_content_model_is_disabled_and_bounded() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_contract_content import (
        build_signed_apply_command_contract_model,
    )

    model = build_signed_apply_command_contract_model("req-1")
    contract = model["apply_command_contract"]

    assert model["command_step_count"] == 7
    assert model["guard_check_count"] == 10
    assert model["target_update_field_count"] == 2
    assert model["rollback_step_count"] == 4
    assert model["approval_granted_by_contract"] is False
    assert model["explicit_operator_apply_approval_present"] is False
    assert model["apply_command_enabled"] is False
    assert model["apply_execution_allowed"] is False
    assert model["target_update_fields"] == ["approval_scope", "decision_note"]
    assert model["bounded_update_shape"] == {
        "table": "service_requests",
        "where": ["request_id", "updated_at"],
        "set_fields": ["approval_scope", "decision_note"],
        "max_rows": 1,
        "requires_parameterized_sql": True,
        "requires_transaction": True,
    }
    assert contract["status"] == "contract_only_disabled"
    assert contract["target_request_id"] == "req-1"
    assert contract["approval_granted_by_contract"] is False
    assert contract["apply_command_enabled"] is False
    assert "explicit_apply_execution_flag_true" in contract["guard_checks"]


def test_signed_apply_command_negative_fixture_content_matches_evaluator_rules() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_negative_fixture_content import (
        build_signed_apply_command_negative_fixture_results,
        build_signed_apply_command_negative_fixtures,
    )

    fixtures = build_signed_apply_command_negative_fixtures()
    results = build_signed_apply_command_negative_fixture_results(fixtures, target_request_id="req-1")

    assert len(fixtures) == 6
    assert {item["expected_rule_id"] for item in fixtures} == {
        "reject_missing_operator_signature",
        "reject_expired_approval",
        "reject_stale_target_snapshot",
        "reject_wrong_target_request_id",
        "reject_unapproved_field_set",
        "reject_missing_explicit_execution_flag",
    }
    assert all(item["expected_accepted"] is False for item in fixtures)
    assert all(item["actual_accepted"] is False for item in results)
    assert all(item["matched_expected"] is True for item in results)
    assert [item["expected_rule_id"] for item in results] == [item["actual_rule_id"] for item in results]

def test_signed_apply_command_closeout_content_summarizes_disabled_sources() -> None:
    from agent_company_core.ceo_decision_signed_apply_closeout_content import (
        build_signed_apply_command_closeout_content,
    )

    source_validations = [
        {
            "id": f"source-{index}",
            "task_id": f"task-{index}",
            "path": f"reports/source-{index}.json",
            "validation": {
                "schema_version": f"schema-{index}",
                "all_checks_passed": True,
                "failure_count": 0,
                "apply_command_enabled": False,
                "apply_execution_allowed": False,
                "service_requests_updated": 0,
                "service_requests_assigned": 0,
            },
        }
        for index in range(4)
    ]

    content = build_signed_apply_command_closeout_content(source_validations)

    assert content["apply_command_closeout_count"] == 1
    assert content["source_validation_count"] == 4
    assert content["passed_source_validation_count"] == 4
    assert content["remaining_gate_count"] == 5
    assert content["remaining_gates"] == [
        "real_operator_signature_not_fixture_placeholder",
        "operator_approval_expiration_and_scope_review",
        "explicit_permission_to_mutate_service_request_fields",
        "fresh_target_updated_at_snapshot_at_apply_time",
        "separate_mutation_implementation_and_rollback_review",
    ]
    assert content["ready_for_real_mutation"] is False
    assert content["approval_granted_by_closeout"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["apply_execution_allowed"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["source_validation_results"][0]["schema_version"] == "schema-0"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert "real mutation remains parked" in content["summary"]



def test_signed_apply_command_positive_runner_content_summarizes_preview_only_fixture() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_positive_runner_content import (
        build_signed_apply_command_positive_runner_content,
    )

    signed_fixture = {
        "fixture_id": "positive-apply-command",
        "target_request_id": "req-1",
        "confirmations": {f"confirm_{index}": True for index in range(6)},
        "required_fields_present": [f"field_{index}" for index in range(8)],
        "operator_signature": "LOCAL_FIXTURE_SIGNATURE_NOT_REAL_APPROVAL",
        "rollback_snapshot_updated_at": "2026-06-14T14:37:52Z",
        "target_update_fields": ["approval_scope", "decision_note"],
        "explicit_apply_execution_flag": True,
        "expected_accepted": True,
        "expected_preview_state": "positive_apply_command_fixture_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }

    content = build_signed_apply_command_positive_runner_content(
        signed_fixture=signed_fixture,
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    assert content["positive_apply_command_execution_count"] == 1
    assert content["accepted_apply_fixture_count"] == 1
    assert content["rejected_apply_fixture_count"] == 0
    assert content["preview_state_match_count"] == 1
    assert content["real_mutation_allowed_count"] == 0
    assert content["approval_granted_by_runner"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["apply_execution_allowed"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert content["positive_results"][0]["matched_expected"] is True
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert "preview-only state" in content["summary"]



def test_signed_apply_command_positive_runner_artifacts_render_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_positive_runner_content import (
        build_signed_apply_command_positive_runner_artifacts,
        build_signed_apply_command_positive_runner_content,
    )

    signed_fixture = {
        "fixture_id": "positive-apply-command",
        "target_request_id": "req-1",
        "confirmations": {f"confirm_{index}": True for index in range(6)},
        "required_fields_present": [f"field_{index}" for index in range(8)],
        "operator_signature": "LOCAL_FIXTURE_SIGNATURE_NOT_REAL_APPROVAL",
        "rollback_snapshot_updated_at": "2026-06-14T14:37:52Z",
        "target_update_fields": ["approval_scope", "decision_note"],
        "explicit_apply_execution_flag": True,
        "expected_accepted": True,
        "expected_preview_state": "positive_apply_command_fixture_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }
    runner_content = build_signed_apply_command_positive_runner_content(
        signed_fixture=signed_fixture,
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    artifacts = build_signed_apply_command_positive_runner_artifacts(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/positive-apply-runner.json",
        validation_path="reports/positive-apply-runner.validation.json",
        source_fixture_validation_path="reports/positive-apply-fixture.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-positive-apply-runner",
        runner_evidence_id="evidence-positive-apply-runner",
        source_fixture_task_id="task-positive-apply-fixture",
        source_fixture_evidence_id="evidence-positive-apply-fixture",
        target_request_id="req-1",
        target_status_before="needs_review",
        runner_content=runner_content,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner.v1"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["source_fixture_validation_path"] == "reports/positive-apply-fixture.validation.json"
    assert payload["positive_apply_command_execution_count"] == 1
    assert payload["accepted_apply_fixture_count"] == 1
    assert payload["approval_granted_by_runner"] is False
    assert payload["apply_execution_allowed"] is False
    assert payload["target_request_id"] == "req-1"
    assert payload["target_status_after"] == "needs_review"
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["positive_results"][0]["fixture_id"] == "positive-apply-command"
    assert "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Positive Runner" in markdown
    assert "`ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner_accepted_preview_only_no_mutation`" in markdown
    assert "| `positive-apply-command` | `True` | `positive_apply_command_fixture_valid_apply_still_disabled` | `False` | `True` |" in markdown
    assert "This runner is report-only" in markdown
    assert markdown.endswith("\n")

def test_signed_apply_command_guard_runner_content_rejects_negative_fixtures_without_mutation() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_guard_runner_content import (
        build_signed_apply_command_guard_runner_content,
    )
    from agent_company_core.ceo_decision_signed_apply_command_negative_fixture_content import (
        build_signed_apply_command_negative_fixtures,
    )

    content = build_signed_apply_command_guard_runner_content(
        negative_fixtures=build_signed_apply_command_negative_fixtures(),
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    assert content["apply_command_guard_execution_count"] == 6
    assert content["rejected_fixture_count"] == 6
    assert content["accepted_fixture_count"] == 0
    assert content["matched_rejection_rule_count"] == 6
    assert content["apply_command_execution_count"] == 0
    assert content["approval_granted_by_runner"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["apply_execution_allowed"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert all(item["matched_expected"] is True for item in content["guard_results"])
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner_rejected_all_no_mutation"
    assert content["recommended_default"] == "keep_apply_command_disabled_until_positive_signed_operator_apply_approval_passes"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "Every fixture rejected" in content["summary"]


def test_signed_apply_operator_approval_packet_content_is_draft_only() -> None:
    from agent_company_core.ceo_decision_signed_apply_operator_approval_packet_content import (
        build_signed_apply_operator_approval_packet_content,
    )

    content = build_signed_apply_operator_approval_packet_content(
        decision_fields_template={
            "target_request_id": "req-1",
            "approval_scope_text": "scope",
            "decision_note_text": "note",
            "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
        },
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    assert content["operator_apply_approval_packet_count"] == 1
    assert content["required_approval_field_count"] == 8
    assert content["required_confirmation_count"] == 6
    assert content["approval_granted_by_packet"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["operator_apply_approval_packet"]["target_request_id"] == "req-1"
    assert content["operator_apply_approval_packet"]["approval_scope_text"] == "scope"
    assert content["operator_apply_approval_packet"]["apply_command_enabled"] is False
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet_ready_no_mutation"
    assert content["recommended_default"] == "operator_must_explicitly_approve_before_apply_command_is_enabled"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "does not grant approval" in content["summary"]


def test_signed_apply_preflight_content_blocks_without_operator_approval() -> None:
    from agent_company_core.ceo_decision_signed_apply_preflight_check_content import (
        build_signed_apply_preflight_content,
    )

    content = build_signed_apply_preflight_content(
        runner_validation={
            "accepted_signed_decision_count": 1,
            "apply_command_enabled": False,
            "approval_granted_by_runner": False,
            "real_mutation_allowed_count": 0,
        },
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    assert content["apply_preflight_check_count"] == 1
    assert content["apply_blocked_count"] == 1
    assert content["blocked_reason_count"] == 5
    assert content["accepted_signed_decision_count"] == 1
    assert content["apply_command_enabled"] is False
    assert content["approval_granted_by_runner"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["real_mutation_allowed_count"] == 0
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert [item["reason_id"] for item in content["blocked_reasons"]] == [
        "positive_runner_preview_only",
        "apply_command_disabled",
        "runner_did_not_grant_approval",
        "missing_explicit_operator_apply_approval",
        "real_mutation_allowance_zero",
    ]
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_apply_preflight_blocked_no_mutation"
    assert content["recommended_default"] == "wait_for_explicit_operator_apply_approval_before_mutating_service_request"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "Apply remains blocked" in content["summary"]


def test_signed_apply_command_positive_fixture_content_is_preview_only() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_positive_fixture_content import (
        build_signed_apply_command_positive_fixture_content,
    )

    content = build_signed_apply_command_positive_fixture_content(
        operator_packet={
            "target_request_id": "req-1",
            "approval_scope_text": "scope",
            "decision_note_text": "note",
            "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
            "apply_command_name": "apply-command",
            "required_approval_fields": [f"field_{index}" for index in range(8)],
            "required_confirmations": [f"confirm_{index}" for index in range(6)],
        },
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    fixture = content["signed_operator_apply_fixture"]

    assert content["positive_apply_command_fixture_count"] == 1
    assert content["required_field_count"] == 8
    assert content["confirmation_count"] == 6
    assert content["target_update_field_count"] == 2
    assert content["approval_granted_by_fixture"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["apply_execution_allowed"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert fixture["target_request_id"] == "req-1"
    assert fixture["approval_scope_text"] == "scope"
    assert fixture["decision_note_text"] == "note"
    assert fixture["operator_signature"] == "LOCAL_FIXTURE_SIGNATURE_NOT_REAL_APPROVAL"
    assert fixture["confirmations"] == {f"confirm_{index}": True for index in range(6)}
    assert fixture["target_update_fields"] == ["approval_scope", "decision_note"]
    assert fixture["expected_preview_state"] == "positive_apply_command_fixture_valid_apply_still_disabled"
    assert fixture["expected_real_mutation"] is False
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture_ready_preview_only"
    assert content["recommended_default"] == "positive_apply_command_fixture_requires_report_only_runner_before_any_apply_implementation"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "does not grant approval" in content["summary"]


def test_signed_apply_command_negative_fixtures_content_rejects_all_without_mutation() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_negative_fixture_content import (
        build_signed_apply_command_negative_fixtures,
        build_signed_apply_command_negative_fixtures_content,
    )

    content = build_signed_apply_command_negative_fixtures_content(
        negative_fixtures=build_signed_apply_command_negative_fixtures(),
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    assert content["apply_command_negative_fixture_count"] == 6
    assert content["expected_rejection_count"] == 6
    assert content["unique_rejection_rule_count"] == 6
    assert content["apply_command_execution_count"] == 0
    assert content["approval_granted_by_fixtures"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["apply_execution_allowed"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert all(item["matched_expected"] is True for item in content["fixture_results"])
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures_ready_no_mutation"
    assert content["recommended_default"] == "reject_apply_command_inputs_until_explicit_operator_apply_approval_is_validated"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "six local negative fixtures" in content["summary"]

def test_signed_apply_command_contract_content_builds_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_contract_content import (
        build_signed_apply_command_contract_content,
    )

    content = build_signed_apply_command_contract_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/contract.json",
        validation_path="reports/contract-validation.json",
        source_packet_validation_path="reports/packet-validation.json",
        lane_id="platform_engineering",
        contract_task_id="task-contract",
        contract_evidence_id="evidence-contract",
        source_packet_task_id="task-packet",
        source_packet_evidence_id="evidence-packet",
        target_request_id="req-1",
        target_status_before="needs_review",
        target_status_after="needs_review",
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["apply_command_contract_count"] == 1
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["command_step_count"] == 7
    assert content["guard_check_count"] == 10
    assert content["target_update_field_count"] == 2
    assert content["rollback_step_count"] == 4
    assert content["approval_granted_by_contract"] is False
    assert content["explicit_operator_apply_approval_present"] is False
    assert content["apply_command_enabled"] is False
    assert content["apply_execution_allowed"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract.v1"
    assert payload["target_request_id"] == "req-1"
    assert payload["target_status_before"] == "needs_review"
    assert payload["target_status_after"] == "needs_review"
    assert payload["apply_command_contract"]["status"] == "contract_only_disabled"
    assert "## Guard Checks" in markdown
    assert "explicit_apply_execution_flag_true" in markdown
    assert "This is a contract-only artifact" in markdown
    assert markdown.endswith("\n")




def test_signed_apply_command_closeout_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.ceo_decision_signed_apply_closeout_content import (
        build_signed_apply_command_closeout_artifacts,
        build_signed_apply_command_closeout_content,
    )

    source_validations = [
        {
            "id": f"source-{index}",
            "task_id": f"task-{index}",
            "path": f"reports/source-{index}.json",
            "validation": {
                "schema_version": f"schema-{index}",
                "all_checks_passed": True,
                "failure_count": 0,
                "apply_command_enabled": False,
                "apply_execution_allowed": False,
                "service_requests_updated": 0,
                "service_requests_assigned": 0,
            },
        }
        for index in range(4)
    ]
    closeout_content = build_signed_apply_command_closeout_content(source_validations)

    artifacts = build_signed_apply_command_closeout_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/closeout.json"),
        validation_path=Path("reports/closeout.validation.json"),
        lane_id="platform_engineering",
        closeout_task_id="task-closeout",
        closeout_evidence_id="closeout-evidence",
        source_positive_runner_task_id="task-positive-runner",
        source_positive_runner_evidence_id="positive-runner-evidence",
        target_request_id="req-target",
        target_status_before="needs_review",
        target_status_after="needs_review",
        closeout_content=closeout_content,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["closeout_lane_id"] == "platform_engineering"
    assert payload["apply_command_closeout_count"] == 1
    assert payload["source_validation_count"] == 4
    assert payload["passed_source_validation_count"] == 4
    assert payload["remaining_gate_count"] == 5
    assert payload["target_status_before"] == "needs_review"
    assert payload["target_status_after"] == "needs_review"
    assert payload["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout_parked_waiting_for_real_operator_approval"
    assert payload["recommended_default"] == "do_not_implement_or_run_mutating_apply_until_real_operator_approval_is_supplied"
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Closeout" in markdown
    assert "| `source-0` | `True` | `0` | `False` | `False` |" in markdown
    assert "This closeout is local-only." in markdown
    assert "Do not implement or run a mutating apply command" in markdown

def test_signed_apply_command_guard_runner_artifacts_render_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_guard_runner_content import (
        build_signed_apply_command_guard_runner_artifacts,
        build_signed_apply_command_guard_runner_content,
    )
    from agent_company_core.ceo_decision_signed_apply_command_negative_fixture_content import (
        build_signed_apply_command_negative_fixtures,
    )

    runner_content = build_signed_apply_command_guard_runner_content(
        negative_fixtures=build_signed_apply_command_negative_fixtures(),
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    artifacts = build_signed_apply_command_guard_runner_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path="reports/guard-runner.json",
        validation_path="reports/guard-runner.validation.json",
        source_fixture_validation_path="reports/negative-fixtures.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-guard-runner",
        runner_evidence_id="evidence-guard-runner",
        source_fixture_task_id="task-negative-fixtures",
        source_fixture_evidence_id="evidence-negative-fixtures",
        target_request_id="req-1",
        target_status_before="needs_review",
        runner_content=runner_content,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner.v1"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["source_fixture_validation_path"] == "reports/negative-fixtures.validation.json"
    assert payload["apply_command_guard_execution_count"] == 6
    assert payload["rejected_fixture_count"] == 6
    assert payload["accepted_fixture_count"] == 0
    assert payload["matched_rejection_rule_count"] == 6
    assert payload["apply_command_execution_count"] == 0
    assert payload["approval_granted_by_runner"] is False
    assert payload["apply_execution_allowed"] is False
    assert payload["target_request_id"] == "req-1"
    assert payload["target_status_after"] == "needs_review"
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["guard_results"][0]["fixture_id"] == "apply-command-reject-missing-operator-signature"
    assert "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Guard Runner" in markdown
    assert "`ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner_rejected_all_no_mutation`" in markdown
    assert "| `apply-command-reject-missing-operator-signature` | `False` | `reject_missing_operator_signature` | `True` |" in markdown
    assert "This runner is report-only" in markdown
    assert markdown.endswith("\n")
