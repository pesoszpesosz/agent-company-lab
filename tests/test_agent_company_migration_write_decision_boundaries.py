import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_agent_company_migration_write_decision_contract_reexports_phase_modules():
    from agent_company_core import agent_company_migration_write_decision_contract as contract_facade
    from agent_company_core import agent_company_migration_write_decision_fixture_suite
    from agent_company_core import agent_company_migration_write_decision_intake_contract

    assert (
        contract_facade.write_agent_company_migration_decision_parser_write_decision_intake_contract
        is agent_company_migration_write_decision_intake_contract.write_agent_company_migration_decision_parser_write_decision_intake_contract
    )
    assert (
        contract_facade.write_agent_company_migration_decision_parser_write_decision_fixture_suite
        is agent_company_migration_write_decision_fixture_suite.write_agent_company_migration_decision_parser_write_decision_fixture_suite
    )


def test_agent_company_migration_write_decision_facade_reexports_phase_modules():
    from agent_company_core import agent_company_migration as migration_facade
    from agent_company_core import agent_company_migration_write_decision as write_decision_facade
    from agent_company_core import agent_company_migration_write_decision_approval
    from agent_company_core import agent_company_migration_write_decision_contract
    from agent_company_core import agent_company_migration_write_decision_runner

    assert (
        write_decision_facade.write_agent_company_migration_decision_parser_write_decision_intake_contract
        is agent_company_migration_write_decision_contract.write_agent_company_migration_decision_parser_write_decision_intake_contract
    )
    assert (
        write_decision_facade.write_agent_company_migration_decision_parser_write_decision_fixture_suite
        is agent_company_migration_write_decision_contract.write_agent_company_migration_decision_parser_write_decision_fixture_suite
    )

    assert (
        write_decision_facade.write_agent_company_migration_decision_parser_write_decision_runner
        is agent_company_migration_write_decision_runner.write_agent_company_migration_decision_parser_write_decision_runner
    )
    assert (
        write_decision_facade.write_agent_company_migration_decision_parser_write_decision_runner_review
        is agent_company_migration_write_decision_runner.write_agent_company_migration_decision_parser_write_decision_runner_review
    )

    assert (
        write_decision_facade.write_agent_company_migration_decision_parser_write_approval_request
        is agent_company_migration_write_decision_approval.write_agent_company_migration_decision_parser_write_approval_request
    )
    assert (
        migration_facade.write_agent_company_migration_decision_parser_write_approval_request
        is write_decision_facade.write_agent_company_migration_decision_parser_write_approval_request
    )
def test_agent_company_migration_write_decision_runner_reexports_phase_modules():
    from agent_company_core import agent_company_migration_write_decision_run
    from agent_company_core import agent_company_migration_write_decision_runner
    from agent_company_core import agent_company_migration_write_decision_runner_review

    assert (
        agent_company_migration_write_decision_runner.write_agent_company_migration_decision_parser_write_decision_runner
        is agent_company_migration_write_decision_run.write_agent_company_migration_decision_parser_write_decision_runner
    )
    assert (
        agent_company_migration_write_decision_runner.write_agent_company_migration_decision_parser_write_decision_runner_review
        is agent_company_migration_write_decision_runner_review.write_agent_company_migration_decision_parser_write_decision_runner_review
    )



def test_agent_company_migration_write_decision_contract_content_model():
    from agent_company_core import agent_company_migration_write_decision_contract_content as content

    model = content.build_parser_write_decision_intake_contract_model(
        "tools/agent_company_core/decision_parser.py",
        "reports/parser-artifact.json",
        "reports/runner-review.json",
    )

    assert model["accepted_write_decision_types"] == [
        "hold",
        "approve_one_parser_file_write_only",
        "request_runner_review_rework",
        "reject_parser_write",
    ]
    assert len(model["required_fields"]) == 9
    assert len(model["positive_fixtures"]) == 4
    assert len(model["negative_fixtures"]) == 8
    assert len(model["parser_guards"]) == 9
    assert len(model["output_states"]) == 4
    assert len(model["evidence_links"]) == 4
    assert model["positive_fixtures"][1]["target_path"] == "tools/agent_company_core/decision_parser.py"





def test_agent_company_migration_write_decision_intake_contract_content_builds_payload_and_markdown():
    from agent_company_core.agent_company_migration_write_decision_contract_content import (
        build_parser_write_decision_intake_contract_content,
    )

    content = build_parser_write_decision_intake_contract_content(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path="reports/write-decision-intake.json",
        validation_path="reports/write-decision-intake.validation.json",
        lane_id="platform_engineering",
        intake_task_id="task-intake",
        intake_evidence_id="evidence-intake",
        source_review_task_id="task-review",
        source_review_evidence_id="evidence-review",
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_review_path="reports/runner-review.json",
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["parser_write_decision_intake_contract_count"] == 1
    assert content["accepted_write_decision_type_count"] == 4
    assert content["required_field_count"] == 9
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 8
    assert content["parser_guard_count"] == 9
    assert content["output_state_count"] == 4
    assert content["evidence_link_count"] == 4
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["tables_created"] == 0
    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_decision_intake_contract.v1"
    assert payload["expected_target_path"] == "tools/agent_company_core/decision_parser.py"
    assert payload["expected_source_review_path"] == "reports/runner-review.json"
    assert payload["positive_fixtures"][1]["decision_type"] == "approve_one_parser_file_write_only"
    assert payload["negative_fixtures"][-1] == "bundled_import_or_live_parse_permission"
    assert "# Agent Company Migration Decision Parser Write Decision Intake Contract" in markdown
    assert "## Parser Guards" in markdown
    assert "guard_no_import_or_live_parse_permission" in markdown
    assert "This is a report-only parser-write decision intake contract" in markdown
    assert markdown.endswith("\n")

def test_agent_company_migration_write_decision_fixture_content_builds_expected_suite():
    from agent_company_core.agent_company_migration_write_decision_fixture_content import (
        NEGATIVE_WRITE_DECISION_FIXTURE_SPECS,
        build_parser_write_decision_fixture_suite,
    )

    content = build_parser_write_decision_fixture_suite(
        positive_fixture_specs=[
            {"fixture": "hold", "decision_type": "hold", "expected_state": "held_for_operator"},
            {
                "fixture": "approve",
                "decision_type": "approve_one_parser_file_write_only",
                "expected_state": "accepted_one_parser_file_write_only",
            },
            {
                "fixture": "rework",
                "decision_type": "request_runner_review_rework",
                "expected_state": "returned_for_runner_review_rework",
            },
            {"fixture": "reject", "decision_type": "reject_parser_write", "expected_state": "rejected_by_operator"},
        ],
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_review_path="reports/runner-review.json",
    )

    assert len(NEGATIVE_WRITE_DECISION_FIXTURE_SPECS) == 8
    assert content["parser_write_decision_fixture_suite_count"] == 12
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 8
    assert content["fixture_assertion_count"] == 12
    assert content["positive_fixtures"][1]["decision"]["decision_type"] == "approve_one_parser_file_write_only"
    assert content["positive_fixtures"][1]["expected_state"] == "accepted_one_parser_file_write_only"
    assert content["negative_fixtures"][0]["fixture_id"] == "missing_decision_id"
    assert content["negative_fixtures"][-1]["expected_guard"] == "guard_no_import_or_live_parse_permission"
    assert content["fixtures"] == content["positive_fixtures"] + content["negative_fixtures"]



def test_agent_company_migration_write_decision_fixture_artifacts_build_payload_and_markdown():
    from pathlib import Path

    from agent_company_core.agent_company_migration_write_decision_fixture_content import (
        build_parser_write_decision_fixture_artifacts,
    )

    fixtures = [
        {"fixture_id": "hold", "kind": "positive", "expected_valid": True, "expected_state": "held_for_operator"},
        {"fixture_id": "missing_decision_id", "kind": "negative", "expected_valid": False, "expected_guard": "guard_required_fields_present"},
    ]
    artifacts = build_parser_write_decision_fixture_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/write-decision-fixtures.json"),
        validation_path=Path("reports/write-decision-fixtures.validation.json"),
        lane_id="platform_engineering",
        fixture_task_id="task-fixtures",
        fixture_evidence_id="evidence-fixtures",
        source_intake_task_id="task-intake",
        source_intake_evidence_id="evidence-intake",
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_review_path="reports/runner-review.json",
        parser_write_decision_fixture_suite_count=2,
        positive_fixture_count=1,
        negative_fixture_count=1,
        required_field_count=9,
        parser_guard_count=9,
        output_state_count=4,
        fixture_assertion_count=2,
        fixtures=fixtures,
        required_fields=["decision_type", "target_path"],
        parser_guards=["guard_required_fields_present"],
        output_states=["held_for_operator"],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_decision_fixture_suite.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["fixture_lane_id"] == "platform_engineering"
    assert payload["parser_write_decision_fixture_suite_count"] == 2
    assert payload["positive_fixture_count"] == 1
    assert payload["negative_fixture_count"] == 1
    assert payload["fixture_assertion_count"] == 2
    assert payload["runtime_boundary"]["fixtures_executed"] is False
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_write_decision_fixture_suite_ready_for_report_only_runner"
    assert payload["recommended_default"] == "build_report_only_parser_write_decision_runner_next_without_writing_parser"
    assert "# Agent Company Migration Decision Parser Write Decision Fixture Suite" in markdown
    assert "`hold` (positive): held_for_operator" in markdown
    assert "`missing_decision_id` (negative): guard_required_fields_present" in markdown
    assert "This is a report-only parser-write decision fixture suite" in markdown
    assert markdown.endswith("\n")
def test_agent_company_migration_write_decision_runner_evaluator_accepts_and_rejects():
    from agent_company_core.agent_company_migration_write_decision_runner_evaluator import (
        evaluate_parser_write_decision_fixture,
    )

    required_fields = {
        "decision_type",
        "target_path",
        "source_artifact_path",
        "source_review_path",
        "expires_at",
        "signed_utc",
        "risk_acknowledgement",
    }
    base_decision = {
        "decision_type": "approve_one_parser_file_write_only",
        "target_path": "tools/agent_company_core/decision_parser.py",
        "source_artifact_path": "reports/parser-artifact.json",
        "source_review_path": "reports/runner-review.json",
        "expires_at": "2026-06-17T00:00:00Z",
        "signed_utc": "2026-06-16T12:00:00Z",
        "risk_acknowledgement": "Local report-only review; parser loading and live parsing are outside this permission.",
    }

    accepted = evaluate_parser_write_decision_fixture(
        {
            "fixture_id": "positive",
            "kind": "positive",
            "decision": base_decision,
            "expected_valid": True,
            "expected_state": "accepted_one_parser_file_write_only",
        },
        required_fields=required_fields,
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_review_path="reports/runner-review.json",
        accepted_decision_types={"approve_one_parser_file_write_only"},
    )
    assert accepted["actual_valid"] is True
    assert accepted["actual_state"] == "accepted_one_parser_file_write_only"
    assert accepted["passed"] is True

    rejected = evaluate_parser_write_decision_fixture(
        {
            "fixture_id": "negative",
            "kind": "negative",
            "decision": {**base_decision, "target_path": "tools/other.py"},
            "expected_valid": False,
            "expected_guard": "guard_target_path_matches_preflight",
        },
        required_fields=required_fields,
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_review_path="reports/runner-review.json",
        accepted_decision_types={"approve_one_parser_file_write_only"},
    )
    assert rejected["actual_valid"] is False
    assert "guard_target_path_matches_preflight" in rejected["reasons"]
    assert rejected["passed"] is True


def test_agent_company_migration_write_approval_response_runner_evaluator_accepts_and_rejects():
    from agent_company_core.agent_company_migration_write_approval_response_runner_evaluator import (
        evaluate_parser_write_approval_response_fixture,
    )

    required_fields = {
        "response_type",
        "target_path",
        "source_artifact_path",
        "source_request_path",
        "approval_scope",
        "expires_at",
        "signed_utc",
        "risk_acknowledgement",
    }
    output_states = {
        "approve_one_parser_file_write_only": "accepted_one_parser_file_write_only",
    }
    base_response = {
        "response_type": "approve_one_parser_file_write_only",
        "target_path": "tools/agent_company_core/decision_parser.py",
        "source_artifact_path": "reports/parser-artifact.json",
        "source_request_path": "reports/write-request.json",
        "approval_scope": "one_local_file_write_only",
        "expires_at": "2026-06-17T00:00:00Z",
        "signed_utc": "2026-06-16T12:00:00Z",
        "risk_acknowledgement": "One local file write approval only.",
    }

    accepted = evaluate_parser_write_approval_response_fixture(
        {
            "fixture_id": "positive",
            "kind": "positive",
            "response": base_response,
            "expected_valid": True,
            "expected_state": "accepted_one_parser_file_write_only",
        },
        required_fields=required_fields,
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_request_path="reports/write-request.json",
        accepted_response_types={"approve_one_parser_file_write_only"},
        output_state_by_response_type=output_states,
    )
    assert accepted["actual_valid"] is True
    assert accepted["actual_state"] == "accepted_one_parser_file_write_only"
    assert accepted["passed"] is True

    rejected = evaluate_parser_write_approval_response_fixture(
        {
            "fixture_id": "negative",
            "kind": "negative",
            "response": {**base_response, "approval_scope": "two_files"},
            "expected_valid": False,
            "expected_guard": "guard_approval_scope_one_file_only",
        },
        required_fields=required_fields,
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        expected_source_request_path="reports/write-request.json",
        accepted_response_types={"approve_one_parser_file_write_only"},
        output_state_by_response_type=output_states,
    )
    assert rejected["actual_valid"] is False
    assert "guard_approval_scope_one_file_only" in rejected["reasons"]
    assert rejected["passed"] is True


def test_agent_company_migration_write_application_packet_runner_evaluator_accepts_and_rejects():
    from agent_company_core.agent_company_migration_write_application_packet_runner_evaluator import (
        evaluate_parser_write_application_packet_fixture,
    )

    application_fields = {
        "signed_response_artifact_path",
        "source_preflight_path",
        "source_runner_review_path",
        "target_path",
        "source_artifact_path",
        "application_scope",
        "expires_at",
        "signed_utc",
        "risk_acknowledgement",
    }
    expected_paths = {
        "source_preflight_path": "reports/preflight.json",
        "source_runner_review_path": "reports/runner-review.json",
        "target_path": "tools/agent_company_core/decision_parser.py",
        "source_artifact_path": "reports/parser-artifact.json",
    }
    base_packet = {
        "signed_response_artifact_path": "E:\\agent-company-lab\\reports\\signed-response.json",
        "source_preflight_path": "reports/preflight.json",
        "source_runner_review_path": "reports/runner-review.json",
        "target_path": "tools/agent_company_core/decision_parser.py",
        "source_artifact_path": "reports/parser-artifact.json",
        "application_scope": "one_local_parser_file_write_application_review_only",
        "expires_at": "2026-06-17T00:00:00Z",
        "signed_utc": "2026-06-16T12:00:00Z",
        "risk_acknowledgement": "Review-only application packet; no action taken.",
    }

    accepted = evaluate_parser_write_application_packet_fixture(
        {
            "fixture_id": "positive",
            "kind": "positive",
            "application_packet": base_packet,
            "expected_valid": True,
            "expected_state": "packet_valid_for_separate_application_review",
        },
        application_fields=application_fields,
        expected_paths=expected_paths,
    )
    assert accepted["actual_valid"] is True
    assert accepted["actual_state"] == "packet_valid_for_separate_application_review"
    assert accepted["passed"] is True

    rejected = evaluate_parser_write_application_packet_fixture(
        {
            "fixture_id": "negative",
            "kind": "negative",
            "application_packet": {**base_packet, "signed_response_artifact_path": "https://example.test/signed.json"},
            "expected_valid": False,
            "expected_guard": "guard_signed_response_artifact_local",
        },
        application_fields=application_fields,
        expected_paths=expected_paths,
    )
    assert rejected["actual_valid"] is False
    assert "guard_signed_response_artifact_local" in rejected["reasons"]
    assert rejected["passed"] is True






def test_agent_company_migration_write_decision_approval_request_content_is_hold_only():
    from agent_company_core.agent_company_migration_write_decision_approval_content import (
        build_parser_write_approval_request_content,
    )

    content = build_parser_write_approval_request_content(
        target_path="tools/agent_company_core/decision_parser.py",
        source_artifact_path="reports/parser-artifact.json",
        source_review_path="reports/runner-review.json",
        source_review_report_path="reports/runner-review.md",
        source_review_validation_path="reports/runner-review-validation.json",
        source_runner_report_path="reports/runner.md",
        source_fixture_suite_report_path="reports/fixtures.md",
        install_preflight_report_path="reports/preflight.md",
    )

    assert content["parser_write_approval_request_count"] == 1
    assert content["approval_field_count"] == 9
    assert content["boundary_condition_count"] == 8
    assert content["refusal_trigger_count"] == 8
    assert content["evidence_link_count"] == 5
    assert content["operator_instruction_count"] == 7
    assert content["approval_fields"] == [
        "decision_id",
        "operator_name",
        "decision_type",
        "target_path",
        "source_artifact_path",
        "source_review_path",
        "approval_scope",
        "expires_at",
        "signed_utc",
    ]
    assert content["approval_request"]["target_path"] == "tools/agent_company_core/decision_parser.py"
    assert content["approval_request"]["source_artifact_path"] == "reports/parser-artifact.json"
    assert content["local_decision"] == "agent_company_migration_decision_parser_write_approval_request_ready_for_signed_operator_decision_or_hold"
    assert content["recommended_default"] == "hold_without_signed_one_file_parser_write_approval"
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "one-file parser-write approval request packet" in content["summary"]
    assert "Hold for a signed operator approval" in content["next_action"]


def test_agent_company_migration_write_decision_runner_review_content_is_hold_only():
    from agent_company_core.agent_company_migration_write_decision_runner_review_content import (
        build_parser_write_decision_runner_review_content,
    )

    content = build_parser_write_decision_runner_review_content(
        runner_report_path="reports/runner.md",
        runner_validation_path="reports/runner-validation.json",
        fixture_suite_report_path="reports/fixtures.md",
        install_preflight_report_path="reports/preflight.md",
    )

    assert content["parser_write_decision_runner_review_count"] == 1
    assert content["runner_result_check_count"] == 6
    assert content["approval_condition_count"] == 6
    assert content["hold_condition_count"] == 6
    assert content["evidence_link_count"] == 4
    assert content["operator_instruction_count"] == 6
    assert content["runner_result_checks"] == [
        "runner_validation_clean",
        "all_parser_write_fixture_results_passed",
        "positive_fixture_accept_count_is_4",
        "negative_fixture_reject_count_is_8",
        "no_parser_file_write_or_import",
        "no_service_request_or_external_side_effect",
    ]
    assert content["evidence_links"] == [
        "reports/runner.md",
        "reports/runner-validation.json",
        "reports/fixtures.md",
        "reports/preflight.md",
    ]
    assert content["local_decision"] == "agent_company_migration_decision_parser_write_decision_runner_review_ready_for_signed_parser_write_or_hold"
    assert content["recommended_default"] == "hold_without_signed_one_file_parser_write_approval"
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "operator-facing hold-or-one-file-write boundary" in content["summary"]
    assert "Hold for a signed one-file parser-write approval" in content["next_action"]


def test_agent_company_migration_write_decision_runner_review_imports_content_helper():
    from agent_company_core import agent_company_migration_write_decision_runner_review as runner_review
    from agent_company_core.agent_company_migration_write_decision_runner_review_content import (
        build_parser_write_decision_runner_review_content,
    )

    assert runner_review.build_parser_write_decision_runner_review_content is build_parser_write_decision_runner_review_content



def test_agent_company_migration_write_decision_runner_content_builds_payload_and_markdown():
    from agent_company_core.agent_company_migration_write_decision_runner_content import (
        build_parser_write_decision_runner_content,
    )

    fixture_results = [
        {
            "fixture_id": "positive-approve",
            "expected_valid": True,
            "actual_valid": True,
            "expected_state": "accepted_one_parser_file_write_only",
            "actual_state": "accepted_one_parser_file_write_only",
            "expected_guard": None,
            "passed": True,
            "reasons": [],
        },
        {
            "fixture_id": "negative-live-parse",
            "expected_valid": False,
            "actual_valid": False,
            "expected_state": None,
            "actual_state": None,
            "expected_guard": "guard_no_import_or_live_parse_permission",
            "passed": True,
            "reasons": ["guard_no_import_or_live_parse_permission"],
        },
    ]

    content = build_parser_write_decision_runner_content(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path="reports/write-decision-runner.json",
        validation_path="reports/write-decision-runner.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-runner",
        runner_evidence_id="evidence-runner",
        source_fixture_task_id="task-fixtures",
        source_fixture_evidence_id="evidence-fixtures",
        fixture_results=fixture_results,
        parser_guard_count=9,
        output_state_count=4,
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["parser_write_decision_runner_count"] == 1
    assert content["fixture_suite_count"] == 2
    assert content["fixtures_evaluated"] == 2
    assert content["accepted_result_count"] == 1
    assert content["rejected_result_count"] == 1
    assert content["passed_fixture_count"] == 2
    assert content["failed_fixture_count"] == 0
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["tables_created"] == 0
    assert payload["schema_version"] == "agent_company.migration_decision_parser_write_decision_runner.v1"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["fixture_results"] == fixture_results
    assert payload["local_decision"] == "agent_company_migration_decision_parser_write_decision_runner_ready_for_report_only_parser_write_review"
    assert payload["recommended_default"] == "review_report_only_parser_write_runner_results_next_without_writing_parser"
    assert "# Agent Company Migration Decision Parser Write Decision Runner" in markdown
    assert "| `negative-live-parse` | `guard_no_import_or_live_parse_permission` | `reject` | `True`" in markdown
    assert "This runner evaluates saved synthetic fixture data only." in markdown
    assert markdown.endswith("\n")

