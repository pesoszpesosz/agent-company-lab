import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def spec_ids(specs: list[dict[str, object]]) -> list[str]:
    return [str(spec["id"]) for spec in specs]


def test_migration_integrity_specs_are_grouped_by_phase_modules() -> None:
    from agent_company_core import service_worker_integrity_specs_migration as facade
    from agent_company_core import service_worker_integrity_specs_migration_application
    from agent_company_core import service_worker_integrity_specs_migration_approval_response
    from agent_company_core import service_worker_integrity_specs_migration_decision
    from agent_company_core import service_worker_integrity_specs_migration_foundation
    from agent_company_core import service_worker_integrity_specs_migration_parser_install
    from agent_company_core import service_worker_integrity_specs_migration_write_decision

    families = [
        service_worker_integrity_specs_migration_foundation.migration_foundation_integrity_specs(),
        service_worker_integrity_specs_migration_decision.migration_decision_integrity_specs(),
        service_worker_integrity_specs_migration_parser_install.migration_parser_install_integrity_specs(),
        service_worker_integrity_specs_migration_write_decision.migration_write_decision_integrity_specs(),
        service_worker_integrity_specs_migration_approval_response.migration_approval_response_integrity_specs(),
        service_worker_integrity_specs_migration_application.migration_application_integrity_specs(),
    ]

    expected_ids = [spec_id for family in families for spec_id in spec_ids(family)]
    actual_ids = spec_ids(facade.migration_integrity_specs())

    assert actual_ids == expected_ids
    assert spec_ids(families[0])[0] == "agent_company_infrastructure_radar"
    assert spec_ids(families[0])[-1] == "agent_company_migration_operator_review"
    assert spec_ids(families[1]) == [
        "agent_company_migration_decision_intake_contract",
        "agent_company_migration_decision_fixture_suite",
        "agent_company_migration_decision_fixture_runner",
        "agent_company_migration_decision_parser_scaffold",
        "agent_company_migration_decision_parser_module_draft",
        "agent_company_migration_decision_module_fixture_checks",
        "agent_company_migration_decision_parser_module_file_draft",
        "agent_company_migration_decision_parser_static_review",
    ]
    assert spec_ids(families[2])[-1] == "agent_company_migration_decision_parser_install_decision_runner_review"
    assert spec_ids(families[3])[-1] == "agent_company_migration_decision_parser_write_approval_request"
    assert spec_ids(families[4])[-1] == "agent_company_migration_decision_parser_write_approval_response_runner_review"
    assert spec_ids(families[5])[-1] == "agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review"

def test_migration_decision_integrity_specs_are_grouped_by_subphase_modules() -> None:
    from agent_company_core import service_worker_integrity_specs_migration_decision as facade
    from agent_company_core import service_worker_integrity_specs_migration_decision_fixtures
    from agent_company_core import service_worker_integrity_specs_migration_decision_parser_module

    fixture_ids = spec_ids(
        service_worker_integrity_specs_migration_decision_fixtures.migration_decision_fixture_integrity_specs()
    )
    parser_ids = spec_ids(
        service_worker_integrity_specs_migration_decision_parser_module.migration_decision_parser_module_integrity_specs()
    )

    assert spec_ids(facade.migration_decision_integrity_specs()) == [*fixture_ids, *parser_ids]
    assert fixture_ids == [
        "agent_company_migration_decision_intake_contract",
        "agent_company_migration_decision_fixture_suite",
        "agent_company_migration_decision_fixture_runner",
    ]
    assert parser_ids == [
        "agent_company_migration_decision_parser_scaffold",
        "agent_company_migration_decision_parser_module_draft",
        "agent_company_migration_decision_module_fixture_checks",
        "agent_company_migration_decision_parser_module_file_draft",
        "agent_company_migration_decision_parser_static_review",
    ]
