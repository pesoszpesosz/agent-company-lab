import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_write_approval_response_runner_reexports_phase_modules():
    from agent_company_core import agent_company_migration_write_approval_response_run
    from agent_company_core import agent_company_migration_write_approval_response_runner
    from agent_company_core import agent_company_migration_write_approval_response_runner_review

    assert (
        agent_company_migration_write_approval_response_runner.write_agent_company_migration_decision_parser_write_approval_response_runner
        is agent_company_migration_write_approval_response_run.write_agent_company_migration_decision_parser_write_approval_response_runner
    )
    assert (
        agent_company_migration_write_approval_response_runner.write_agent_company_migration_decision_parser_write_approval_response_runner_review
        is agent_company_migration_write_approval_response_runner_review.write_agent_company_migration_decision_parser_write_approval_response_runner_review
    )


def test_agent_company_migration_write_approval_response_facade_reexports_phase_modules():
    from agent_company_core import agent_company_migration as migration_facade
    from agent_company_core import agent_company_migration_write_approval_response as response_facade
    from agent_company_core import agent_company_migration_write_approval_response_contract
    from agent_company_core import agent_company_migration_write_approval_response_fixtures
    from agent_company_core import agent_company_migration_write_approval_response_runner

    assert (
        response_facade.write_agent_company_migration_decision_parser_write_approval_response_intake_contract
        is agent_company_migration_write_approval_response_contract.write_agent_company_migration_decision_parser_write_approval_response_intake_contract
    )
    assert (
        response_facade.write_agent_company_migration_decision_parser_write_approval_response_fixture_suite
        is agent_company_migration_write_approval_response_fixtures.write_agent_company_migration_decision_parser_write_approval_response_fixture_suite
    )
    assert (
        response_facade.write_agent_company_migration_decision_parser_write_approval_response_runner
        is agent_company_migration_write_approval_response_runner.write_agent_company_migration_decision_parser_write_approval_response_runner
    )
    assert (
        response_facade.write_agent_company_migration_decision_parser_write_approval_response_runner_review
        is agent_company_migration_write_approval_response_runner.write_agent_company_migration_decision_parser_write_approval_response_runner_review
    )
    assert (
        migration_facade.write_agent_company_migration_decision_parser_write_approval_response_runner_review
        is response_facade.write_agent_company_migration_decision_parser_write_approval_response_runner_review
    )

def test_agent_company_migration_write_approval_response_fixture_content_builds_expected_suite():
    from agent_company_core.agent_company_migration_write_approval_response_fixture_content import (
        NEGATIVE_APPROVAL_RESPONSE_FIXTURE_SPECS,
        build_approval_response_fixture_suite,
    )

    content = build_approval_response_fixture_suite(
        positive_fixture_specs=[
            {"fixture": "hold-positive", "response_type": "hold", "expected_state": "held_for_review"},
            {"fixture": "approve-positive", "response_type": "approve_one_parser_file_write_only", "expected_state": "approved_for_review_only"},
            {"fixture": "rework-positive", "response_type": "request_approval_request_rework", "expected_state": "needs_rework"},
            {"fixture": "reject-positive", "response_type": "reject_parser_write_request", "expected_state": "rejected"},
        ],
        expected_target_path=r"E:\agent-company-lab\tools\agent_company_core\decision_parser.py",
        expected_source_artifact_path=r"E:\agent-company-lab\reports\parser-artifact.json",
        expected_source_request_path=r"E:\agent-company-lab\reports\approval-request.json",
    )

    fixtures = content["fixtures"]
    positive = content["positive_fixtures"]
    negative = content["negative_fixtures"]

    assert len(NEGATIVE_APPROVAL_RESPONSE_FIXTURE_SPECS) == 9
    assert content["parser_write_approval_response_fixture_suite_count"] == 13
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 9
    assert content["fixture_assertion_count"] == 13
    assert fixtures == positive + negative
    assert [item["fixture_id"] for item in positive] == [
        "hold-positive",
        "approve-positive",
        "rework-positive",
        "reject-positive",
    ]
    assert all(item["expected_valid"] is True for item in positive)
    assert {item["expected_guard"] for item in negative} == {
        "guard_required_fields_present",
        "guard_known_response_type",
        "guard_target_path_matches_request",
        "guard_source_artifact_matches_request",
        "guard_source_request_matches_packet",
        "guard_approval_scope_one_file_only",
        "guard_not_expired",
        "guard_signed_timestamp_present",
        "guard_no_import_or_live_parse_permission",
    }
    assert negative[0]["response"]["target_path"] == r"E:\agent-company-lab\tools\agent_company_core\decision_parser.py"





def test_agent_company_migration_write_approval_response_fixture_artifacts_build_payload_and_markdown():
    from pathlib import Path

    from agent_company_core.agent_company_migration_write_approval_response_fixture_content import (
        build_approval_response_fixture_artifacts,
    )

    fixtures = [
        {"fixture_id": "hold-positive", "kind": "positive", "expected_valid": True, "expected_state": "held_for_review"},
        {"fixture_id": "missing_decision_id", "kind": "negative", "expected_valid": False, "expected_guard": "guard_required_fields_present"},
    ]
    artifacts = build_approval_response_fixture_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/approval-response-fixtures.json"),
        validation_path=Path("reports/approval-response-fixtures.validation.json"),
        lane_id="platform_engineering",
        fixture_task_id="task-fixtures",
        fixture_evidence_id="evidence-fixtures",
        source_intake_task_id="task-intake",
        source_intake_evidence_id="evidence-intake",
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_request_path="reports/approval-request.json",
        parser_write_approval_response_fixture_suite_count=2,
        positive_fixture_count=1,
        negative_fixture_count=1,
        required_field_count=10,
        response_guard_count=10,
        output_state_count=4,
        fixture_assertion_count=2,
        fixtures=fixtures,
        required_fields=["response_type", "target_path"],
        response_guards=["guard_required_fields_present"],
        output_states=["held_for_review"],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_approval_response_fixture_suite.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["fixture_lane_id"] == "platform_engineering"
    assert payload["parser_write_approval_response_fixture_suite_count"] == 2
    assert payload["positive_fixture_count"] == 1
    assert payload["negative_fixture_count"] == 1
    assert payload["fixture_assertion_count"] == 2
    assert payload["runtime_boundary"]["fixtures_executed"] is False
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_fixture_suite_ready_for_report_only_runner"
    assert payload["recommended_default"] == "build_report_only_parser_write_approval_response_runner_next_without_applying_approval"
    assert "# Agent Company Migration Decision Parser Write Approval Response Fixture Suite" in markdown
    assert "`hold-positive` (positive): held_for_review" in markdown
    assert "`missing_decision_id` (negative): guard_required_fields_present" in markdown
    assert "This is a report-only approval response fixture suite" in markdown
    assert markdown.endswith("\n")
def test_agent_company_migration_write_approval_response_contract_content_builds_intake_contract():
    from agent_company_core.agent_company_migration_write_approval_response_contract_content import (
        build_parser_write_approval_response_intake_contract_content,
    )

    source_request_payload = {
        "target_path": r"E:\agent-company-lab\tools\agent_company_core\decision_parser.py",
        "source_artifact_path": r"E:\agent-company-lab\reports\parser-artifact.json",
    }
    expected_source_request_path = r"E:\agent-company-lab\reports\approval-request.json"

    content = build_parser_write_approval_response_intake_contract_content(
        source_request_payload=source_request_payload,
        expected_source_request_path=expected_source_request_path,
    )

    assert content["parser_write_approval_response_intake_contract_count"] == 1
    assert content["accepted_response_types"] == [
        "hold",
        "approve_one_parser_file_write_only",
        "request_approval_request_rework",
        "reject_parser_write_request",
    ]
    assert content["accepted_response_type_count"] == 4
    assert content["required_field_count"] == 10
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 9
    assert content["response_guard_count"] == 10
    assert content["output_state_count"] == 4
    assert content["expected_target_path"] == source_request_payload["target_path"]
    assert content["expected_source_artifact_path"] == source_request_payload["source_artifact_path"]
    assert content["expected_source_request_path"] == expected_source_request_path
    assert content["positive_fixtures"][1]["expected_state"] == "accepted_one_parser_file_write_only"
    assert "bundled_import_or_live_parse_permission" in content["negative_fixtures"]
    assert content["runtime_boundary"]["parser_module_imported"] is False
    assert "report-only signed parser-write approval response" in content["summary"]


def test_agent_company_migration_write_approval_response_runner_review_content_is_hold_only():
    from agent_company_core.agent_company_migration_write_approval_response_runner_review_content import (
        build_approval_response_runner_review_content,
    )

    content = build_approval_response_runner_review_content(
        runner_report_path="reports/approval-response-runner.md",
        runner_validation_path="reports/approval-response-runner-validation.json",
        fixture_suite_report_path="reports/approval-response-fixtures.md",
        intake_contract_report_path="reports/approval-response-contract.md",
        approval_request_report_path="reports/approval-request.md",
    )

    assert content["parser_write_approval_response_runner_review_count"] == 1
    assert content["runner_result_check_count"] == 6
    assert content["approval_condition_count"] == 6
    assert content["hold_condition_count"] == 6
    assert content["evidence_link_count"] == 5
    assert content["operator_instruction_count"] == 7
    assert content["runner_result_checks"] == [
        "runner_validation_clean",
        "all_approval_response_fixture_results_passed",
        "positive_fixture_accept_count_is_4",
        "negative_fixture_reject_count_is_9",
        "no_parser_file_write_import_or_approval_application",
        "no_service_request_or_external_side_effect",
    ]
    assert content["evidence_links"] == [
        "reports/approval-response-runner.md",
        "reports/approval-response-runner-validation.json",
        "reports/approval-response-fixtures.md",
        "reports/approval-response-contract.md",
        "reports/approval-request.md",
    ]
    assert content["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_runner_review_ready_for_signed_response_or_hold"
    assert content["recommended_default"] == "hold_without_signed_parser_write_approval_response_application"
    assert content["runtime_boundary"]["operator_decision_applied"] is False
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "hold-first operator boundary" in content["summary"]
    assert "Hold unless a signed approval response" in content["next_action"]


def test_agent_company_migration_write_approval_response_runner_review_imports_content_helper():
    from agent_company_core import agent_company_migration_write_approval_response_runner_review as runner_review
    from agent_company_core.agent_company_migration_write_approval_response_runner_review_content import (
        build_approval_response_runner_review_content,
    )

    assert runner_review.build_approval_response_runner_review_content is build_approval_response_runner_review_content

def test_agent_company_migration_write_approval_response_runner_content_summarizes_fixture_results():
    from agent_company_core.agent_company_migration_write_approval_response_runner_content import (
        build_approval_response_runner_content,
    )

    fixture_results = [
        {
            "fixture_id": "hold-positive",
            "expected_valid": True,
            "expected_state": "accepted_hold",
            "expected_guard": None,
            "actual_valid": True,
            "actual_state": "accepted_hold",
            "passed": True,
            "reasons": [],
        },
        {
            "fixture_id": "missing-required",
            "expected_valid": False,
            "expected_state": None,
            "expected_guard": "guard_required_fields_present",
            "actual_valid": False,
            "actual_state": None,
            "passed": True,
            "reasons": ["missing required fields"],
        },
    ]

    content = build_approval_response_runner_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/runner.json",
        validation_path="reports/runner-validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-runner",
        runner_evidence_id="evidence-runner",
        source_fixture_task_id="task-fixtures",
        source_fixture_evidence_id="evidence-fixtures",
        fixture_results=fixture_results,
        response_guard_count=10,
        output_state_count=4,
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["parser_write_approval_response_runner_count"] == 1
    assert content["fixture_suite_count"] == 2
    assert content["fixtures_evaluated"] == 2
    assert content["accepted_result_count"] == 1
    assert content["rejected_result_count"] == 1
    assert content["passed_fixture_count"] == 2
    assert content["failed_fixture_count"] == 0
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_approval_response_runner.v1"
    assert payload["fixture_results"] == fixture_results
    assert payload["response_guard_count"] == 10
    assert payload["output_state_count"] == 4
    assert "## Runner Results" in markdown
    assert "hold-positive" in markdown
    assert "This runner evaluates saved synthetic approval response fixture data only" in markdown
    assert markdown.endswith("\n")


def test_agent_company_migration_write_approval_response_runner_imports_content_helper():
    from agent_company_core import agent_company_migration_write_approval_response_run as runner
    from agent_company_core.agent_company_migration_write_approval_response_runner_content import (
        build_approval_response_runner_content,
    )

    assert runner.build_approval_response_runner_content is build_approval_response_runner_content

