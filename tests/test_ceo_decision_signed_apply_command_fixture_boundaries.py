import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_signed_apply_command_fixture_set_facade_reexports_negative_and_positive_modules() -> None:
    from agent_company_core import ceo_decision_signed_apply_command_fixture_sets
    from agent_company_core import ceo_decision_signed_apply_command_negative_fixtures
    from agent_company_core import ceo_decision_signed_apply_command_positive_fixture

    assert (
        ceo_decision_signed_apply_command_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures
        is ceo_decision_signed_apply_command_negative_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures
    )
    assert (
        ceo_decision_signed_apply_command_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture
        is ceo_decision_signed_apply_command_positive_fixture.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture
    )


def test_signed_apply_command_runner_facade_reexports_guard_and_positive_modules() -> None:
    from agent_company_core import ceo_decision_signed_apply_command_guard_runner
    from agent_company_core import ceo_decision_signed_apply_command_positive_runner
    from agent_company_core import ceo_decision_signed_apply_command_runners

    assert (
        ceo_decision_signed_apply_command_runners.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner
        is ceo_decision_signed_apply_command_guard_runner.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner
    )
    assert (
        ceo_decision_signed_apply_command_runners.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
        is ceo_decision_signed_apply_command_positive_runner.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
    )


def test_signed_apply_command_fixture_facade_reexports_phase_modules() -> None:
    from agent_company_core import ceo_decision_signed_apply_command as apply_facade
    from agent_company_core import ceo_decision_signed_apply_command_fixture_sets
    from agent_company_core import ceo_decision_signed_apply_command_fixtures
    from agent_company_core import ceo_decision_signed_apply_command_runners

    assert (
        ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures
        is ceo_decision_signed_apply_command_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures
    )
    assert (
        ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture
        is ceo_decision_signed_apply_command_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture
    )
    assert (
        ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner
        is ceo_decision_signed_apply_command_runners.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner
    )
    assert (
        ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
        is ceo_decision_signed_apply_command_runners.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
        is ceo_decision_signed_apply_command_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner
    )

def test_signed_apply_command_negative_fixture_artifact_builder_renders_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_signed_apply_command_negative_fixture_content import (
        build_signed_apply_command_negative_fixture_artifacts,
        build_signed_apply_command_negative_fixtures,
        build_signed_apply_command_negative_fixtures_content,
    )

    fixture_content = build_signed_apply_command_negative_fixtures_content(
        negative_fixtures=build_signed_apply_command_negative_fixtures(),
        target_request_id="req-target",
        target_status_before="needs_review",
    )

    artifacts = build_signed_apply_command_negative_fixture_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/negative-fixtures.json"),
        validation_path=Path("reports/negative-fixtures-validation.json"),
        fixture_lane_id="platform_engineering",
        fixture_task_id="task-fixtures",
        fixture_evidence_id="evidence-fixtures",
        source_contract_task_id="task-contract",
        source_contract_evidence_id="evidence-contract",
        source_contract_validation_path=Path("reports/contract-validation.json"),
        fixture_content=fixture_content,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures.v1"
    assert payload["apply_command_negative_fixture_count"] == 6
    assert payload["expected_rejection_count"] == 6
    assert payload["target_request_id"] == "req-target"
    assert payload["target_status_before"] == "needs_review"
    assert payload["target_status_after"] == "needs_review"
    assert payload["apply_command_enabled"] is False
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Negative Fixtures" in markdown
    assert "| `apply-command-reject-missing-operator-signature` | `reject_missing_operator_signature` | `False` |" in markdown
    assert "These are local rejection fixtures only." in markdown

