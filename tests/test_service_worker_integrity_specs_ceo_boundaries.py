import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def spec_ids(specs: list[dict[str, object]]) -> list[str]:
    return [str(spec["id"]) for spec in specs]


def test_ceo_integrity_specs_are_grouped_by_phase_modules() -> None:
    from agent_company_core import service_worker_integrity_specs_ceo as facade
    from agent_company_core import service_worker_integrity_specs_ceo_apply
    from agent_company_core import service_worker_integrity_specs_ceo_apply_command
    from agent_company_core import service_worker_integrity_specs_ceo_intake
    from agent_company_core import service_worker_integrity_specs_ceo_parser
    from agent_company_core import service_worker_integrity_specs_ceo_readiness
    from agent_company_core import service_worker_integrity_specs_ceo_signed_decision

    families = [
        service_worker_integrity_specs_ceo_intake.ceo_intake_integrity_specs(),
        service_worker_integrity_specs_ceo_parser.ceo_parser_integrity_specs(),
        service_worker_integrity_specs_ceo_apply.ceo_apply_integrity_specs(),
        service_worker_integrity_specs_ceo_readiness.ceo_readiness_integrity_specs(),
        service_worker_integrity_specs_ceo_signed_decision.ceo_signed_decision_integrity_specs(),
        service_worker_integrity_specs_ceo_apply_command.ceo_apply_command_integrity_specs(),
    ]

    expected_ids = [spec_id for family in families for spec_id in spec_ids(family)]
    actual_ids = spec_ids(facade.ceo_integrity_specs())

    assert actual_ids == expected_ids
    assert spec_ids(families[0]) == [
        "ceo_gate_blocker_board",
        "ceo_blocker_triage",
        "ceo_decision_packet_drafts",
        "ceo_decision_intake_guard",
        "ceo_decision_intake_negative_fixtures",
    ]
    assert spec_ids(families[1])[-1] == "ceo_decision_parser_mutation_preflight"
    assert spec_ids(families[2])[-1] == "ceo_decision_parser_apply_dry_runner"
    assert spec_ids(families[3])[-1] == "ceo_decision_parser_apply_readiness_decision_intake_packet"
    assert spec_ids(families[4])[-1] == "ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet"
    assert spec_ids(families[5])[-1] == "ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout"

def test_ceo_readiness_integrity_specs_are_grouped_by_subphase_modules() -> None:
    from agent_company_core import service_worker_integrity_specs_ceo_readiness as facade
    from agent_company_core import service_worker_integrity_specs_ceo_readiness_approval
    from agent_company_core import service_worker_integrity_specs_ceo_readiness_flow

    phases = [
        service_worker_integrity_specs_ceo_readiness_flow.ceo_readiness_flow_integrity_specs(),
        service_worker_integrity_specs_ceo_readiness_approval.ceo_readiness_approval_integrity_specs(),
    ]
    expected_ids = [spec_id for phase in phases for spec_id in spec_ids(phase)]

    assert spec_ids(facade.ceo_readiness_integrity_specs()) == expected_ids
    assert spec_ids(phases[0]) == [
        "ceo_decision_parser_apply_readiness",
        "ceo_decision_parser_apply_readiness_negative_fixtures",
        "ceo_decision_parser_apply_readiness_guard_runner",
        "ceo_decision_parser_apply_readiness_positive_fixture",
        "ceo_decision_parser_apply_readiness_positive_runner",
    ]
    assert spec_ids(phases[1]) == [
        "ceo_decision_parser_apply_readiness_operator_approval_packet",
        "ceo_decision_parser_apply_readiness_no_approval_blocker",
        "ceo_decision_parser_apply_readiness_decision_intake_packet",
    ]

