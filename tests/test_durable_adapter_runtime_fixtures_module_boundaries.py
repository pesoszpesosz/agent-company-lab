import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_durable_adapter_runtime_fixtures_facade_reexports_stage_modules() -> None:
    from agent_company_core import durable_adapter_runtime_fixtures as facade
    from agent_company_core import durable_adapter_runtime_negative_fixtures
    from agent_company_core import durable_adapter_runtime_implementation_preflight
    from agent_company_core import durable_adapter_runtime_report_only_fixtures

    assert (
        facade.durable_runtime_negative_fixture_definitions
        is durable_adapter_runtime_negative_fixtures.durable_runtime_negative_fixture_definitions
    )
    assert (
        facade.write_durable_adapter_runtime_negative_fixtures
        is durable_adapter_runtime_negative_fixtures.write_durable_adapter_runtime_negative_fixtures
    )
    assert (
        facade.write_durable_adapter_runtime_implementation_preflight
        is durable_adapter_runtime_implementation_preflight.write_durable_adapter_runtime_implementation_preflight
    )
    assert (
        facade.durable_runtime_report_only_fixture_definitions
        is durable_adapter_runtime_report_only_fixtures.durable_runtime_report_only_fixture_definitions
    )
    assert (
        facade.write_durable_adapter_runtime_report_only_fixtures
        is durable_adapter_runtime_report_only_fixtures.write_durable_adapter_runtime_report_only_fixtures
    )

def test_durable_runtime_implementation_preflight_content_builds_artifacts() -> None:
    from agent_company_core.durable_adapter_runtime_implementation_preflight_content import (
        build_durable_runtime_implementation_preflight_content,
    )

    upstream_validations = [
        {"id": "integration", "passed": True},
        {"id": "readiness", "passed": True},
    ]
    preflight_checks = [
        {"check_id": "runtime_readiness_blocks_external_runtime", "passed": True},
        {"check_id": "runtime_implementation_remains_blocked", "passed": True},
    ]
    negative_validation = {
        "negative_fixture_count": 8,
        "rejected_fixture_count": 8,
        "accepted_fixture_count": 0,
        "all_negative_fixtures_rejected": True,
    }

    content = build_durable_runtime_implementation_preflight_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/preflight.json",
        validation_path="reports/preflight-validation.json",
        upstream_validations=upstream_validations,
        preflight_checks=preflight_checks,
        runtime_implementation_allowed=False,
        runtime_code_write_allowed=False,
        report_only_scaffolding_allowed=True,
        explicit_runtime_approval_present=False,
        external_runtime_implementation_allowed_now=False,
        local_report_only_implementation_allowed_now=True,
        negative_validation=negative_validation,
        forbidden_imports=[],
        model_request={"request_id": "req-1", "status": "needs_review"},
        model_api_gate_remains_parked=True,
        model_api_pool_registered=False,
        failures=[],
    )

    payload = content["payload"]
    validation_payload = content["validation_payload"]
    markdown = content["markdown"]

    assert content["passed_preflight_check_count"] == 2
    assert content["upstream_validation_passed_count"] == 2
    assert content["runtime_boundary"]["dependency_installs"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["schema_version"] == "temporal_inngest_adapter_runtime_implementation_preflight.v1"
    assert payload["runtime_implementation_allowed"] is False
    assert payload["report_only_scaffolding_allowed"] is True
    assert payload["negative_fixture_summary"]["accepted_fixture_count"] == 0
    assert validation_payload["schema_version"] == "temporal_inngest_adapter_runtime_implementation_preflight_validation.v1"
    assert validation_payload["all_checks_passed"] is True
    assert validation_payload["failure_count"] == 0
    assert validation_payload["model_api_gate_remains_parked"] is True
    assert "Runtime implementation remains blocked" in markdown
    assert "runtime_implementation_remains_blocked" in markdown
    assert markdown.endswith("\n")


def test_durable_runtime_implementation_preflight_writer_imports_content_helper() -> None:
    from agent_company_core import durable_adapter_runtime_implementation_preflight as preflight
    from agent_company_core.durable_adapter_runtime_implementation_preflight_content import (
        build_durable_runtime_implementation_preflight_content,
    )

    assert preflight.build_durable_runtime_implementation_preflight_content is build_durable_runtime_implementation_preflight_content

