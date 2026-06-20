import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_decision_contract_facade_reexports_phase_modules() -> None:
    from agent_company_core import agent_company_migration_decision_contracts as facade
    from agent_company_core import agent_company_migration_decision_intake_contract
    from agent_company_core import agent_company_migration_decision_fixture_suite
    from agent_company_core import agent_company_migration_decision_fixture_runner

    assert (
        facade.write_agent_company_migration_decision_intake_contract
        is agent_company_migration_decision_intake_contract.write_agent_company_migration_decision_intake_contract
    )
    assert (
        facade.write_agent_company_migration_decision_fixture_suite
        is agent_company_migration_decision_fixture_suite.write_agent_company_migration_decision_fixture_suite
    )
    assert (
        facade.write_agent_company_migration_decision_fixture_runner
        is agent_company_migration_decision_fixture_runner.write_agent_company_migration_decision_fixture_runner
    )


def test_agent_company_migration_decision_fixture_runner_evaluator_accepts_and_rejects() -> None:
    from agent_company_core.agent_company_migration_decision_fixture_runner_evaluator import (
        evaluate_migration_decision_fixture,
    )

    required_fields = {
        "decision_id",
        "operator_name",
        "decision_type",
        "scope",
        "artifact_paths",
        "expires_at",
        "risk_acknowledgement",
        "signed_utc",
    }
    accepted_types = {"approve_sandbox_dry_run_only"}
    base_intake = {
        "decision_id": "decision-1",
        "operator_name": "local-operator",
        "decision_type": "approve_sandbox_dry_run_only",
        "scope": "sandbox dry run only",
        "artifact_paths": ["a", "b", "c", "d"],
        "expires_at": "2026-06-17T00:00:00Z",
        "risk_acknowledgement": "No live operation.",
        "signed_utc": "2026-06-16T12:00:00Z",
    }

    accepted = evaluate_migration_decision_fixture(
        {"fixture_id": "positive", "submitted_intake": base_intake, "expected": "accept"},
        accepted_decision_types=accepted_types,
        required_fields=required_fields,
    )
    assert accepted["actual"] == "accept"
    assert accepted["passed"] is True

    rejected = evaluate_migration_decision_fixture(
        {
            "fixture_id": "negative",
            "submitted_intake": {**base_intake, "scope": "use browser and wallet"},
            "expected": "reject",
        },
        accepted_decision_types=accepted_types,
        required_fields=required_fields,
    )
    assert rejected["actual"] == "reject"
    assert "forbidden_scope" in rejected["reasons"]
    assert rejected["passed"] is True



def test_agent_company_migration_decision_fixture_suite_content_builds_submitted_intakes() -> None:
    from agent_company_core.agent_company_migration_decision_fixture_suite_content import (
        build_migration_decision_fixture_suite_content,
    )

    intake_payload = {
        "parser_guards": [f"guard_{index}" for index in range(9)],
        "output_states": ["accepted_hold", "accepted_dry_run", "rework", "rejected"],
        "required_fields": [
            "decision_id",
            "operator_name",
            "decision_type",
            "scope",
            "artifact_paths",
            "expires_at",
            "risk_acknowledgement",
            "signed_utc",
        ],
        "positive_fixtures": [
            {"fixture_id": "positive_hold", "decision_type": "hold", "expected_state": "accepted_hold"},
            {
                "fixture_id": "positive_dry_run",
                "decision_type": "approve_sandbox_dry_run_only",
                "expected_state": "accepted_dry_run",
            },
            {"fixture_id": "positive_rework", "decision_type": "request_rework", "expected_state": "rework"},
            {"fixture_id": "positive_reject", "decision_type": "reject_migration", "expected_state": "rejected"},
        ],
        "negative_fixtures": [
            {"fixture_id": "missing_decision_id", "reason": "missing_required_fields"},
            {"fixture_id": "unknown_decision_type", "reason": "unknown_decision_type"},
            {"fixture_id": "live_apply_scope", "reason": "forbidden_scope"},
            {"fixture_id": "missing_artifact_paths", "reason": "missing_artifact_paths"},
            {"fixture_id": "expired_decision", "reason": "expired_or_missing_expiration"},
            {"fixture_id": "unsigned_decision", "reason": "unsigned_decision"},
            {"fixture_id": "gated_action_bundle", "reason": "forbidden_scope"},
            {"fixture_id": "service_request_mutation", "reason": "forbidden_scope"},
        ],
    }
    artifact_paths = ["review.md", "review-validation.json", "intake.md", "intake-validation.json"]

    content = build_migration_decision_fixture_suite_content(
        intake_payload=intake_payload,
        artifact_paths=artifact_paths,
    )

    assert content["fixture_suite_count"] == 12
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 8
    assert content["expected_accept_count"] == 4
    assert content["expected_reject_count"] == 8
    assert content["parser_guard_count"] == 9
    assert content["output_state_count"] == 4
    assert content["required_field_count"] == 8
    assert content["fixtures"] == content["positive_fixtures"] + content["negative_fixtures"]

    positive = content["positive_fixtures"][1]
    assert positive["submitted_intake"]["decision_type"] == "approve_sandbox_dry_run_only"
    assert positive["submitted_intake"]["artifact_paths"] == artifact_paths

    negative_by_id = {item["fixture_id"]: item for item in content["negative_fixtures"]}
    assert "decision_id" not in negative_by_id["missing_decision_id"]["submitted_intake"]
    assert negative_by_id["live_apply_scope"]["submitted_intake"]["scope"] == "live_migration_sql_apply"
    assert negative_by_id["service_request_mutation"]["submitted_intake"]["scope"] == "update_service_request_and_assign_worker"
    assert content["runtime_boundary"]["fixtures_executed"] is False

def test_agent_company_migration_decision_intake_contract_content_model_and_markdown() -> None:
    from agent_company_core.agent_company_migration_decision_intake_contract_content import (
        build_migration_decision_intake_contract_content,
    )

    content = build_migration_decision_intake_contract_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/intake.json",
        validation_path="reports/intake-validation.json",
        lane_id="platform_engineering",
        intake_task_id="task-intake",
        intake_evidence_id="evidence-intake",
        source_review_task_id="task-review",
        source_review_evidence_id="evidence-review",
        accepted_decision_types=[
            "hold",
            "approve_sandbox_dry_run_only",
            "request_rework",
            "reject_migration",
        ],
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["decision_intake_contract_count"] == 1
    assert content["accepted_decision_type_count"] == 4
    assert content["required_field_count"] == 8
    assert content["positive_fixture_count"] == 4
    assert content["negative_fixture_count"] == 8
    assert content["parser_guard_count"] == 9
    assert content["output_state_count"] == 4
    assert content["local_decision"] == "agent_company_migration_decision_intake_contract_ready_for_report_only_fixture_suite"
    assert content["recommended_default"] == "build_report_only_fixture_suite_next_without_applying_operator_decision"
    assert content["positive_fixtures"][1]["expected_state"] == "accepted_for_sandbox_dry_run_preparation_only"
    assert content["negative_fixtures"][-1]["fixture_id"] == "service_request_mutation"
    assert content["runtime_boundary"]["operator_decision_applied"] is False
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["schema_version"] == "agent_company.migration_decision_intake_contract.v1"
    assert payload["accepted_decision_types"] == [
        "hold",
        "approve_sandbox_dry_run_only",
        "request_rework",
        "reject_migration",
    ]
    assert "## Parser Guards" in markdown
    assert "This contract is report-only" in markdown
    assert markdown.endswith("\n")


def test_agent_company_migration_decision_intake_contract_writer_imports_content_helper() -> None:
    from agent_company_core import agent_company_migration_decision_intake_contract as intake_contract
    from agent_company_core.agent_company_migration_decision_intake_contract_content import (
        build_migration_decision_intake_contract_content,
    )

    assert intake_contract.build_migration_decision_intake_contract_content is build_migration_decision_intake_contract_content

