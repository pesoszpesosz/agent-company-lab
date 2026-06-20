import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_agent_company_migration_write_application_runner_reexports_phase_modules():
    from agent_company_core import agent_company_migration_write_application_packet_run
    from agent_company_core import agent_company_migration_write_application_packet_runner_review
    from agent_company_core import agent_company_migration_write_application_runner

    assert (
        agent_company_migration_write_application_runner.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner
        is agent_company_migration_write_application_packet_run.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner
    )
    assert (
        agent_company_migration_write_application_runner.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review
        is agent_company_migration_write_application_packet_runner_review.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review
    )


def test_agent_company_migration_write_application_facade_reexports_phase_modules():
    from agent_company_core import agent_company_migration as migration_facade
    from agent_company_core import agent_company_migration_write_application as application_facade
    from agent_company_core import agent_company_migration_write_application_contract
    from agent_company_core import agent_company_migration_write_application_fixtures
    from agent_company_core import agent_company_migration_write_application_runner

    assert (
        application_facade.write_agent_company_migration_decision_parser_write_approval_response_application_preflight
        is agent_company_migration_write_application_contract.write_agent_company_migration_decision_parser_write_approval_response_application_preflight
    )
    assert (
        application_facade.write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract
        is agent_company_migration_write_application_contract.write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract
    )

    assert (
        application_facade.write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite
        is agent_company_migration_write_application_fixtures.write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite
    )

    assert (
        application_facade.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner
        is agent_company_migration_write_application_runner.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner
    )
    assert (
        application_facade.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review
        is agent_company_migration_write_application_runner.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review
    )
    assert (
        migration_facade.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review
        is application_facade.write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review
    )


def test_agent_company_migration_write_application_contract_reexports_phase_modules():
    from agent_company_core import agent_company_migration_write_application_contract
    from agent_company_core import agent_company_migration_write_application_packet_contract
    from agent_company_core import agent_company_migration_write_application_preflight

    assert (
        agent_company_migration_write_application_contract.write_agent_company_migration_decision_parser_write_approval_response_application_preflight
        is agent_company_migration_write_application_preflight.write_agent_company_migration_decision_parser_write_approval_response_application_preflight
    )
    assert (
        agent_company_migration_write_application_contract.write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract
        is agent_company_migration_write_application_packet_contract.write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract
    )

def test_agent_company_migration_write_application_fixture_content_builds_expected_packet_suite():
    from agent_company_core.agent_company_migration_write_application_fixture_content import (
        APPLICATION_PACKET_GUARDS,
        build_application_packet_fixture_suite,
    )

    content = build_application_packet_fixture_suite(
        expected_target_path=r"E:\agent-company-lab\tools\agent_company_core\decision_parser.py",
        expected_source_artifact_path=r"E:\agent-company-lab\reports\parser-artifact.json",
        expected_source_preflight_path=r"E:\agent-company-lab\reports\preflight.json",
        expected_source_runner_review_path=r"E:\agent-company-lab\reports\runner-review.json",
        expected_signed_response_artifact_path=r"E:\agent-company-lab\reports\signed-response.json",
    )

    fixtures = content["fixtures"]
    positive = [item for item in fixtures if item["kind"] == "positive"]
    negative = [item for item in fixtures if item["kind"] == "negative"]

    assert len(APPLICATION_PACKET_GUARDS) == 10
    assert content["application_packet_guards"] == APPLICATION_PACKET_GUARDS
    assert len(fixtures) == 10
    assert len(positive) == 1
    assert len(negative) == 9
    assert positive[0]["expected_state"] == "packet_valid_for_separate_application_review"
    assert {item["expected_guard"] for item in negative} == {
        "guard_required_fields_present",
        "guard_signed_response_artifact_local",
        "guard_source_preflight_matches_contract",
        "guard_source_runner_review_matches_contract",
        "guard_target_path_matches_request",
        "guard_source_artifact_matches_request",
        "guard_application_scope_review_only",
        "guard_not_expired",
        "guard_no_import_live_parse_sql_service_or_external_action",
    }
    assert content["fixture_assertion_count"] == 10
    assert content["expected_paths"] == {
        "target_path": r"E:\agent-company-lab\tools\agent_company_core\decision_parser.py",
        "source_artifact_path": r"E:\agent-company-lab\reports\parser-artifact.json",
        "source_preflight_path": r"E:\agent-company-lab\reports\preflight.json",
        "source_runner_review_path": r"E:\agent-company-lab\reports\runner-review.json",
    }



def test_agent_company_migration_write_application_preflight_content_builds_expected_boundary():
    from agent_company_core.agent_company_migration_write_application_preflight_content import (
        build_application_preflight_content,
    )

    content = build_application_preflight_content(
        runner_review_report_path=r"E:\agent-company-lab\reports\runner-review.md",
        runner_review_validation_path=r"E:\agent-company-lab\reports\runner-review-validation.json",
        runner_report_path=r"E:\agent-company-lab\reports\runner.md",
        approval_request_report_path=r"E:\agent-company-lab\reports\approval-request.md",
    )

    assert content["parser_write_approval_response_application_preflight_count"] == 1
    assert content["prerequisite_check_count"] == 7
    assert content["signed_response_requirement_count"] == 8
    assert content["blocked_action_count"] == 12
    assert content["hold_condition_count"] == 6
    assert content["evidence_link_count"] == 4
    assert content["signed_response_present"] is False
    assert content["application_allowed"] is False
    assert content["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_application_preflight_blocked_without_signed_response"
    assert content["recommended_default"] == "keep_hold_until_signed_approval_response_application_packet_exists"
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert content["evidence_links"] == [
        r"E:\agent-company-lab\reports\runner-review.md",
        r"E:\agent-company-lab\reports\runner-review-validation.json",
        r"E:\agent-company-lab\reports\runner.md",
        r"E:\agent-company-lab\reports\approval-request.md",
    ]


def test_agent_company_migration_write_application_packet_contract_content_builds_expected_boundary():
    from agent_company_core.agent_company_migration_write_application_packet_contract_content import (
        build_application_packet_contract_content,
    )

    content = build_application_packet_contract_content(
        application_preflight_report_path=r"E:\agent-company-lab\reports\application-preflight.md",
        application_preflight_validation_path=r"E:\agent-company-lab\reports\application-preflight-validation.json",
        runner_review_report_path=r"E:\agent-company-lab\reports\runner-review.md",
        intake_contract_report_path=r"E:\agent-company-lab\reports\intake-contract.md",
        approval_request_report_path=r"E:\agent-company-lab\reports\approval-request.md",
    )

    assert content["parser_write_approval_response_application_packet_contract_count"] == 1
    assert content["application_field_count"] == 10
    assert content["eligibility_rule_count"] == 8
    assert content["blocked_action_count"] == 12
    assert content["hold_condition_count"] == 6
    assert content["evidence_link_count"] == 5
    assert content["application_allowed"] is False
    assert content["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_application_packet_contract_ready_for_signed_packet_or_hold"
    assert content["recommended_default"] == "wait_for_signed_approval_response_application_packet_without_applying"
    assert content["runtime_boundary"]["parser_module_imported"] is False
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert content["application_fields"] == [
        "application_packet_id",
        "operator_name",
        "signed_response_artifact_path",
        "source_preflight_path",
        "source_runner_review_path",
        "target_path",
        "source_artifact_path",
        "application_scope",
        "expires_at",
        "signed_utc",
    ]
    assert content["evidence_links"] == [
        r"E:\agent-company-lab\reports\application-preflight.md",
        r"E:\agent-company-lab\reports\application-preflight-validation.json",
        r"E:\agent-company-lab\reports\runner-review.md",
        r"E:\agent-company-lab\reports\intake-contract.md",
        r"E:\agent-company-lab\reports\approval-request.md",
    ]



def test_agent_company_migration_write_application_packet_runner_artifact_builder_renders_payload_and_markdown():
    from pathlib import Path

    from agent_company_core.agent_company_migration_write_application_packet_run_content import (
        build_application_packet_runner_artifacts,
    )

    fixture_results = [
        {
            "fixture_id": "positive-valid",
            "expected_valid": True,
            "expected_state": "packet_valid_for_separate_application_review",
            "expected_guard": None,
            "actual_valid": True,
            "actual_state": "packet_valid_for_separate_application_review",
            "passed": True,
            "reasons": [],
        }
    ] + [
        {
            "fixture_id": f"negative-{index}",
            "expected_valid": False,
            "expected_state": None,
            "expected_guard": "guard_signed_response_artifact_local",
            "actual_valid": False,
            "actual_state": None,
            "passed": True,
            "reasons": ["guard_signed_response_artifact_local"],
        }
        for index in range(9)
    ]

    artifacts = build_application_packet_runner_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/application-packet-runner.json"),
        validation_path=Path("reports/application-packet-runner.validation.json"),
        lane_id="platform_engineering",
        runner_task_id="task-runner",
        runner_evidence_id="evidence-runner",
        source_fixture_task_id="task-fixtures",
        source_fixture_evidence_id="evidence-fixtures",
        fixture_suite_count=10,
        fixtures_evaluated=10,
        accepted_result_count=1,
        rejected_result_count=9,
        passed_fixture_count=10,
        failed_fixture_count=0,
        application_packet_guard_count=10,
        application_allowed=False,
        fixture_results=fixture_results,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_approval_response_application_packet_runner.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["parser_write_approval_response_application_packet_runner_count"] == 1
    assert payload["fixture_suite_count"] == 10
    assert payload["fixtures_evaluated"] == 10
    assert payload["accepted_result_count"] == 1
    assert payload["rejected_result_count"] == 9
    assert payload["passed_fixture_count"] == 10
    assert payload["failed_fixture_count"] == 0
    assert payload["application_packet_guard_count"] == 10
    assert payload["application_allowed"] is False
    assert payload["runtime_boundary"]["report_only_fixtures_evaluated"] is True
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_application_packet_runner_ready_for_report_only_review"
    assert payload["recommended_default"] == "review_report_only_approval_response_application_packet_runner_results_next_without_applying"
    assert "# Agent Company Migration Decision Parser Write Approval Response Application Packet Runner" in markdown
    assert "| Fixture | Expected | Actual | Passed | Reasons |" in markdown
    assert "This runner evaluates saved synthetic application packet fixture data only." in markdown
    assert markdown.endswith("\n")

def test_agent_company_migration_write_application_packet_runner_review_content_builds_expected_boundary():
    from agent_company_core.agent_company_migration_write_application_packet_runner_review_content import (
        build_application_packet_runner_review_content,
    )

    content = build_application_packet_runner_review_content(
        runner_report_path=r"E:\agent-company-lab\reports\runner.md",
        runner_validation_path=r"E:\agent-company-lab\reports\runner-validation.json",
        fixture_suite_report_path=r"E:\agent-company-lab\reports\fixture-suite.md",
        packet_contract_report_path=r"E:\agent-company-lab\reports\packet-contract.md",
    )

    assert content["parser_write_approval_response_application_packet_runner_review_count"] == 1
    assert content["runner_result_check_count"] == 6
    assert content["application_condition_count"] == 6
    assert content["hold_condition_count"] == 6
    assert content["evidence_link_count"] == 4
    assert content["operator_instruction_count"] == 7
    assert content["application_allowed"] is False
    assert content["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review_ready_for_signed_packet_or_hold"
    assert content["recommended_default"] == "hold_without_signed_approval_response_application_packet_application"
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert content["evidence_links"] == [
        r"E:\agent-company-lab\reports\runner.md",
        r"E:\agent-company-lab\reports\runner-validation.json",
        r"E:\agent-company-lab\reports\fixture-suite.md",
        r"E:\agent-company-lab\reports\packet-contract.md",
    ]



def test_agent_company_migration_write_application_packet_runner_review_artifacts_build_payload_and_markdown():
    from pathlib import Path

    from agent_company_core.agent_company_migration_write_application_packet_runner_review_content import (
        build_application_packet_runner_review_artifacts,
        build_application_packet_runner_review_content,
    )

    review_content = build_application_packet_runner_review_content(
        runner_report_path=r"E:\agent-company-lab\reports\runner.md",
        runner_validation_path=r"E:\agent-company-lab\reports\runner-validation.json",
        fixture_suite_report_path=r"E:\agent-company-lab\reports\fixture-suite.md",
        packet_contract_report_path=r"E:\agent-company-lab\reports\packet-contract.md",
    )
    artifacts = build_application_packet_runner_review_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/application-packet-runner-review.json"),
        validation_path=Path("reports/application-packet-runner-review.validation.json"),
        lane_id="platform_engineering",
        review_task_id="task-review",
        review_evidence_id="evidence-review",
        source_runner_task_id="task-runner",
        source_runner_evidence_id="evidence-runner",
        review_content=review_content,
        runner_result_summary={
            "fixtures_evaluated": 10,
            "accepted_result_count": 1,
            "rejected_result_count": 9,
            "passed_fixture_count": 10,
            "failed_fixture_count": 0,
            "application_allowed": False,
        },
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_approval_response_application_packet_runner_review.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["review_lane_id"] == "platform_engineering"
    assert payload["parser_write_approval_response_application_packet_runner_review_count"] == 1
    assert payload["runner_result_check_count"] == 6
    assert payload["application_condition_count"] == 6
    assert payload["hold_condition_count"] == 6
    assert payload["evidence_link_count"] == 4
    assert payload["operator_instruction_count"] == 7
    assert payload["application_allowed"] is False
    assert payload["runner_result_summary"]["fixtures_evaluated"] == 10
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review_ready_for_signed_packet_or_hold"
    assert payload["recommended_default"] == "hold_without_signed_approval_response_application_packet_application"
    assert "# Agent Company Migration Decision Parser Write Approval Response Application Packet Runner Review" in markdown
    assert "runner_validation_clean" in markdown
    assert "This is a report-only application packet runner review." in markdown
    assert markdown.endswith("\n")

def test_agent_company_migration_write_application_fixture_artifacts_build_payload_and_markdown():
    from agent_company_core.agent_company_migration_write_application_fixture_content import (
        build_application_packet_fixture_suite,
        build_application_packet_fixture_suite_artifacts,
    )

    fixture_content = build_application_packet_fixture_suite(
        expected_target_path=r"E:\agent-company-lab\tools\agent_company_core\decision_parser.py",
        expected_source_artifact_path=r"E:\agent-company-lab\reports\parser-artifact.json",
        expected_source_preflight_path=r"E:\agent-company-lab\reports\preflight.json",
        expected_source_runner_review_path=r"E:\agent-company-lab\reports\runner-review.json",
        expected_signed_response_artifact_path=r"E:\agent-company-lab\reports\signed-response.json",
    )

    content = build_application_packet_fixture_suite_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path="reports/application-fixtures.json",
        validation_path="reports/application-fixtures.validation.json",
        lane_id="platform_engineering",
        fixture_task_id="task-fixtures",
        fixture_evidence_id="evidence-fixtures",
        source_contract_task_id="task-contract",
        source_contract_evidence_id="evidence-contract",
        application_fields=["application_packet_id", "operator_name"],
        eligibility_rules=["signed_packet_present"],
        application_allowed=False,
        fixture_content=fixture_content,
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["parser_write_approval_response_application_packet_fixture_suite_count"] == 10
    assert content["positive_fixture_count"] == 1
    assert content["negative_fixture_count"] == 9
    assert content["application_field_count"] == 2
    assert content["eligibility_rule_count"] == 1
    assert content["application_packet_guard_count"] == 10
    assert content["fixture_assertion_count"] == 10
    assert content["application_allowed"] is False
    assert content["runtime_boundary"]["fixtures_executed"] is False
    assert content["runtime_boundary"]["tables_created"] == 0
    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_approval_response_application_packet_fixture_suite.v1"
    assert payload["fixture_lane_id"] == "platform_engineering"
    assert payload["fixtures"] == fixture_content["fixtures"]
    assert payload["local_decision"] == "agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite_ready_for_report_only_runner"
    assert payload["recommended_default"] == "build_report_only_approval_response_application_packet_runner_next_without_applying"
    assert "# Agent Company Migration Decision Parser Write Approval Response Application Packet Fixture Suite" in markdown
    assert "Recommended default: `build_report_only_approval_response_application_packet_runner_next_without_applying`" in markdown
    assert "positive_valid_review_only_application_packet" in markdown
    assert "This is a report-only fixture suite." in markdown
    assert markdown.endswith("\n")
