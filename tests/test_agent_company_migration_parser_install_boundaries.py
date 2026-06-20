import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_parser_install_facade_reexports_phase_modules():
    from agent_company_core import agent_company_migration as migration_facade
    from agent_company_core import agent_company_migration_parser_install as install_facade
    from agent_company_core import agent_company_migration_parser_install_contract
    from agent_company_core import agent_company_migration_parser_install_fixtures
    from agent_company_core import agent_company_migration_parser_install_runner

    assert (
        install_facade.write_agent_company_migration_decision_parser_install_decision_intake_contract
        is agent_company_migration_parser_install_contract.write_agent_company_migration_decision_parser_install_decision_intake_contract
    )
    assert (
        install_facade.write_agent_company_migration_decision_parser_install_decision_fixture_suite
        is agent_company_migration_parser_install_fixtures.write_agent_company_migration_decision_parser_install_decision_fixture_suite
    )
    assert (
        install_facade.write_agent_company_migration_decision_parser_install_decision_runner
        is agent_company_migration_parser_install_runner.write_agent_company_migration_decision_parser_install_decision_runner
    )
    assert (
        install_facade.write_agent_company_migration_decision_parser_install_decision_runner_review
        is agent_company_migration_parser_install_runner.write_agent_company_migration_decision_parser_install_decision_runner_review
    )
    assert (
        migration_facade.write_agent_company_migration_decision_parser_install_decision_runner_review
        is install_facade.write_agent_company_migration_decision_parser_install_decision_runner_review
    )
def test_agent_company_migration_parser_install_runner_reexports_phase_modules():
    from agent_company_core import agent_company_migration_parser_install_decision_run
    from agent_company_core import agent_company_migration_parser_install_runner
    from agent_company_core import agent_company_migration_parser_install_runner_review

    assert (
        agent_company_migration_parser_install_runner.write_agent_company_migration_decision_parser_install_decision_runner
        is agent_company_migration_parser_install_decision_run.write_agent_company_migration_decision_parser_install_decision_runner
    )
    assert (
        agent_company_migration_parser_install_runner.write_agent_company_migration_decision_parser_install_decision_runner_review
        is agent_company_migration_parser_install_runner_review.write_agent_company_migration_decision_parser_install_decision_runner_review
    )


def test_agent_company_migration_parser_install_decision_runner_evaluator_accepts_and_rejects() -> None:
    from agent_company_core.agent_company_migration_parser_install_decision_runner_evaluator import (
        evaluate_parser_install_decision_fixture,
    )

    required_fields = {
        "decision_type",
        "target_path",
        "source_artifact_path",
        "expires_at",
        "signed_utc",
        "risk_acknowledgement",
    }
    base_decision = {
        "decision_type": "approve_one_file_write_only",
        "target_path": "tools/agent_company_core/decision_parser.py",
        "source_artifact_path": "reports/parser-artifact.json",
        "expires_at": "2026-06-17T00:00:00Z",
        "signed_utc": "2026-06-16T12:00:00Z",
        "risk_acknowledgement": "One local file write review only.",
    }

    accepted = evaluate_parser_install_decision_fixture(
        {
            "fixture_id": "positive",
            "kind": "positive",
            "decision": base_decision,
            "expected_valid": True,
            "expected_state": "accepted_one_file_write_only",
        },
        required_fields=required_fields,
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        accepted_decision_types={"approve_one_file_write_only"},
    )
    assert accepted["actual_valid"] is True
    assert accepted["actual_state"] == "accepted_one_file_write_only"
    assert accepted["passed"] is True

    rejected = evaluate_parser_install_decision_fixture(
        {
            "fixture_id": "negative",
            "kind": "negative",
            "decision": {**base_decision, "source_artifact_path": "reports/other.json"},
            "expected_valid": False,
            "expected_guard": "guard_source_artifact_matches_preflight",
        },
        required_fields=required_fields,
        expected_target_path="tools/agent_company_core/decision_parser.py",
        expected_source_artifact_path="reports/parser-artifact.json",
        accepted_decision_types={"approve_one_file_write_only"},
    )
    assert rejected["actual_valid"] is False
    assert "guard_source_artifact_matches_preflight" in rejected["reasons"]
    assert rejected["passed"] is True



def test_agent_company_migration_parser_install_decision_runner_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.agent_company_migration_parser_install_decision_run_content import (
        build_agent_company_migration_decision_parser_install_decision_runner_artifacts,
    )

    fixture_results = [
        {
            "fixture_id": f"positive-{index}",
            "expected_valid": True,
            "expected_state": "accepted_one_file_write_only",
            "expected_guard": None,
            "actual_valid": True,
            "actual_state": "accepted_one_file_write_only",
            "passed": True,
            "reasons": [],
        }
        for index in range(4)
    ] + [
        {
            "fixture_id": f"negative-{index}",
            "expected_valid": False,
            "expected_state": None,
            "expected_guard": "guard_source_artifact_matches_preflight",
            "actual_valid": False,
            "actual_state": None,
            "passed": True,
            "reasons": ["guard_source_artifact_matches_preflight"],
        }
        for index in range(7)
    ]

    artifacts = build_agent_company_migration_decision_parser_install_decision_runner_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/parser-install-decision-runner.json"),
        validation_path=Path("reports/parser-install-decision-runner.validation.json"),
        lane_id="platform_engineering",
        runner_task_id="task-runner",
        runner_evidence_id="evidence-runner",
        source_fixture_task_id="task-fixtures",
        source_fixture_evidence_id="evidence-fixtures",
        fixture_suite_count=11,
        fixtures_evaluated=11,
        accepted_result_count=4,
        rejected_result_count=7,
        passed_fixture_count=11,
        failed_fixture_count=0,
        parser_guard_count=8,
        output_state_count=4,
        fixture_results=fixture_results,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_install_decision_runner.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["install_decision_runner_count"] == 1
    assert payload["fixture_suite_count"] == 11
    assert payload["fixtures_evaluated"] == 11
    assert payload["accepted_result_count"] == 4
    assert payload["rejected_result_count"] == 7
    assert payload["passed_fixture_count"] == 11
    assert payload["failed_fixture_count"] == 0
    assert payload["parser_guard_count"] == 8
    assert payload["output_state_count"] == 4
    assert payload["runtime_boundary"]["report_only_fixtures_evaluated"] is True
    assert payload["runtime_boundary"]["parser_module_imported"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_install_decision_runner_ready_for_report_only_parser_static_review"
    assert payload["recommended_default"] == "review_report_only_runner_results_next_without_writing_or_importing_parser"
    assert "# Agent Company Migration Decision Parser Install Decision Runner" in markdown
    assert "| Fixture | Expected | Actual | Passed | Reasons |" in markdown
    assert "This runner evaluates saved synthetic fixture data only." in markdown
    assert markdown.endswith("\n")


def test_agent_company_migration_parser_install_fixture_suite_content_builds_contract_fixtures() -> None:
    from agent_company_core.agent_company_migration_parser_install_fixture_content import (
        build_parser_install_fixture_suite_content,
    )

    source_intake_payload = {
        "accepted_install_decision_types": [
            "hold",
            "approve_one_file_write_only",
            "request_preflight_rework",
            "reject_parser_install",
        ],
        "required_fields": [
            "decision_id",
            "operator_name",
            "decision_type",
            "target_path",
            "source_artifact_path",
            "expires_at",
            "risk_acknowledgement",
            "signed_utc",
        ],
        "parser_guards": [
            "guard_required_fields_present",
            "guard_known_install_decision_type",
            "guard_target_path_matches_preflight",
            "guard_source_artifact_matches_preflight",
            "guard_not_expired",
            "guard_signed_timestamp_present",
            "guard_no_import_or_live_parse_permission",
            "guard_report_only_output_state",
        ],
        "output_states": [
            "held_for_review",
            "accepted_one_file_write_only",
            "preflight_rework_requested",
            "parser_install_rejected",
        ],
        "expected_target_path": "E:\\agent-company-lab\\tools\\agent_company_core\\decision_parser.py",
        "expected_source_artifact_path": "E:\\agent-company-lab\\reports\\parser-module-file-draft.json",
        "positive_fixtures": [
            {"fixture": "hold_fixture", "decision_type": "hold", "expected_state": "held_for_review"},
            {
                "fixture": "approve_fixture",
                "decision_type": "approve_one_file_write_only",
                "expected_state": "accepted_one_file_write_only",
            },
            {
                "fixture": "rework_fixture",
                "decision_type": "request_preflight_rework",
                "expected_state": "preflight_rework_requested",
            },
            {
                "fixture": "reject_fixture",
                "decision_type": "reject_parser_install",
                "expected_state": "parser_install_rejected",
            },
        ],
    }

    content = build_parser_install_fixture_suite_content(source_intake_payload)

    assert content["install_decision_fixture_suite_count"] == 11
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 7
    assert content["required_field_count"] == 8
    assert content["parser_guard_count"] == 8
    assert content["output_state_count"] == 4
    assert content["fixture_assertion_count"] == 11
    assert content["expected_target_path"] == source_intake_payload["expected_target_path"]
    assert content["expected_source_artifact_path"] == source_intake_payload["expected_source_artifact_path"]

    positive = content["fixtures"][0]
    assert positive["fixture_id"] == "hold_fixture"
    assert positive["kind"] == "positive"
    assert positive["decision"]["decision_type"] == "hold"
    assert positive["expected_valid"] is True
    assert positive["expected_state"] == "held_for_review"

    negative_by_id = {item["fixture_id"]: item for item in content["fixtures"] if item["kind"] == "negative"}
    assert negative_by_id["target_path_changed"]["expected_guard"] == "guard_target_path_matches_preflight"
    assert negative_by_id["bundled_live_parse_permission"]["decision"]["risk_acknowledgement"] == "also_allows_import_and_live_parse"


def test_agent_company_migration_parser_install_contract_content_builds_intake_contract() -> None:
    from agent_company_core.agent_company_migration_parser_install_contract_content import (
        build_parser_install_intake_contract_content,
    )

    source_review_payload = {
        "decision_options": [
            {"option": "hold"},
            {"option": "approve_one_file_write_only"},
            {"option": "request_preflight_rework"},
            {"option": "reject_parser_install"},
        ]
    }
    preflight_payload = {
        "target_files": [
            {
                "target_path": "E:\\agent-company-lab\\tools\\agent_company_core\\decision_parser.py",
                "source_artifact": "E:\\agent-company-lab\\reports\\parser-module-file-draft.json",
            }
        ]
    }

    content = build_parser_install_intake_contract_content(
        source_review_payload=source_review_payload,
        preflight_payload=preflight_payload,
    )

    assert content["install_decision_intake_contract_count"] == 1
    assert content["accepted_install_decision_types"] == [
        "hold",
        "approve_one_file_write_only",
        "request_preflight_rework",
        "reject_parser_install",
    ]
    assert content["accepted_install_decision_type_count"] == 4
    assert content["required_field_count"] == 8
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 7
    assert content["parser_guard_count"] == 8
    assert content["output_state_count"] == 4
    assert content["expected_target_path"] == preflight_payload["target_files"][0]["target_path"]
    assert content["expected_source_artifact_path"] == preflight_payload["target_files"][0]["source_artifact"]
    assert content["positive_fixtures"][1]["expected_state"] == "accepted_one_file_write_only"
    assert "bundled_live_parse_permission" in content["negative_fixtures"]
    assert content["runtime_boundary"]["parser_module_imported"] is False


def test_agent_company_migration_parser_install_runner_review_content_is_hold_only() -> None:
    from agent_company_core.agent_company_migration_parser_install_runner_review_content import (
        build_install_decision_runner_review_content,
    )

    content = build_install_decision_runner_review_content(
        runner_report_path="reports/install-runner.md",
        runner_validation_path="reports/install-runner-validation.json",
        fixture_suite_report_path="reports/install-fixtures.md",
        install_preflight_report_path="reports/install-preflight.md",
    )

    assert content["install_decision_runner_review_count"] == 1
    assert content["runner_result_check_count"] == 6
    assert content["approval_condition_count"] == 6
    assert content["hold_condition_count"] == 6
    assert content["evidence_link_count"] == 4
    assert content["operator_instruction_count"] == 6
    assert content["runner_result_checks"] == [
        "runner_validation_clean",
        "all_fixture_results_passed",
        "positive_fixture_accept_count_is_4",
        "negative_fixture_reject_count_is_7",
        "no_parser_file_write_or_import",
        "no_service_request_or_external_side_effect",
    ]
    assert content["evidence_links"] == [
        "reports/install-runner.md",
        "reports/install-runner-validation.json",
        "reports/install-fixtures.md",
        "reports/install-preflight.md",
    ]
    assert content["local_decision"] == "agent_company_migration_decision_parser_install_decision_runner_review_ready_for_operator_parser_write_decision_or_hold"
    assert content["recommended_default"] == "hold_without_signed_operator_parser_write_approval"
    assert content["runtime_boundary"]["parser_module_file_written"] is False
    assert content["runtime_boundary"]["parser_module_imported"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "operator-facing hold-or-parser-write boundary" in content["summary"]
    assert "Hold for a signed one-file parser-write approval" in content["next_action"]


def test_agent_company_migration_parser_install_runner_review_imports_content_helper() -> None:
    from agent_company_core import agent_company_migration_parser_install_runner_review as runner_review
    from agent_company_core.agent_company_migration_parser_install_runner_review_content import (
        build_install_decision_runner_review_content,
    )

    assert runner_review.build_install_decision_runner_review_content is build_install_decision_runner_review_content
