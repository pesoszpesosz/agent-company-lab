import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def spec_ids(specs: list[dict[str, object]]) -> list[str]:
    return [str(spec["id"]) for spec in specs]


def test_service_worker_integrity_specs_facade_preserves_family_order() -> None:
    from agent_company_core.service_worker_integrity_specs import service_worker_chain_integrity_specs
    from agent_company_core.service_worker_integrity_specs_ceo import ceo_integrity_specs
    from agent_company_core.service_worker_integrity_specs_durable import durable_integrity_specs
    from agent_company_core.service_worker_integrity_specs_migration import migration_integrity_specs
    from agent_company_core.service_worker_integrity_specs_money import money_lane_integrity_specs
    from agent_company_core.service_worker_integrity_specs_runtime import runtime_integrity_specs
    from agent_company_core.service_worker_integrity_specs_service_workers import service_worker_control_integrity_specs

    families = [
        service_worker_control_integrity_specs(),
        money_lane_integrity_specs(),
        ceo_integrity_specs(),
        migration_integrity_specs(),
        durable_integrity_specs(),
        runtime_integrity_specs(),
    ]
    expected_ids = [spec_id for family in families for spec_id in spec_ids(family)]
    actual_specs = service_worker_chain_integrity_specs()

    assert len(actual_specs) == 138
    assert spec_ids(actual_specs) == expected_ids
    assert spec_ids(families[0])[:3] == ["queue", "dequeue", "readiness"]
    assert spec_ids(families[2])[0] == "ceo_gate_blocker_board"
    assert spec_ids(families[3])[-1] == "agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review"
    assert spec_ids(families[5])[-1] == "worker_pool_registration_review_v1"

def test_durable_integrity_specs_facade_preserves_phase_order() -> None:
    from agent_company_core.service_worker_integrity_specs_durable import durable_integrity_specs
    from agent_company_core.service_worker_integrity_specs_durable_human_decision import durable_human_decision_integrity_specs
    from agent_company_core.service_worker_integrity_specs_durable_runtime import durable_runtime_integrity_specs
    from agent_company_core.service_worker_integrity_specs_durable_source_specs import durable_source_spec_integrity_specs

    phases = [
        durable_source_spec_integrity_specs(),
        durable_runtime_integrity_specs(),
        durable_human_decision_integrity_specs(),
    ]
    expected_ids = [spec_id for phase in phases for spec_id in spec_ids(phase)]

    assert spec_ids(durable_integrity_specs()) == expected_ids
    assert spec_ids(phases[0]) == [
        "source_spec_seed_packets",
        "source_spec_seed_apply",
    ]
    assert spec_ids(phases[1]) == [
        "durable_service_worker_integration",
        "durable_runtime_interface_contract",
        "durable_runtime_interface_negative_fixtures",
        "durable_runtime_implementation_preflight",
        "durable_runtime_report_only_fixtures",
        "durable_runtime_report_only_scaffolding_packet",
        "durable_runtime_report_only_scaffolding_artifacts",
    ]
    assert spec_ids(phases[2]) == [
        "durable_runtime_human_approval_packet",
        "durable_runtime_human_decision_intake_packet",
    ]


def test_service_worker_control_integrity_specs_split_into_lifecycle_and_decision_phases() -> None:
    from agent_company_core.service_worker_integrity_specs_service_worker_decisions import (
        service_worker_decision_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_service_worker_lifecycle import (
        service_worker_lifecycle_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_service_workers import service_worker_control_integrity_specs

    lifecycle_specs = service_worker_lifecycle_integrity_specs()
    decision_specs = service_worker_decision_integrity_specs()

    assert spec_ids(lifecycle_specs) == [
        "queue",
        "dequeue",
        "readiness",
        "scope_diff",
        "scope_templates",
        "approval_review",
        "assignment_plan",
        "pool_registry",
        "pool_registration",
        "gate_map",
    ]
    assert spec_ids(decision_specs) == [
        "human_decision_packets",
        "post_decision_simulation",
        "post_decision_refresh_plan",
        "decision_drift_guard",
        "decision_command_safety",
        "decision_authority_matrix",
        "decision_preflight",
    ]
    assert spec_ids(service_worker_control_integrity_specs()) == spec_ids(lifecycle_specs) + spec_ids(decision_specs)
    assert lifecycle_specs[0]["expected"]["schema_version"] == "service_worker_request_queue_validation.v1"
    assert lifecycle_specs[-1]["expected"]["gate_counts"] == {
        "human_cro_approval_required": 13,
        "terminal_no_execution": 3,
    }
    assert decision_specs[0]["expected"]["decision_packet_count"] == 11
    assert decision_specs[-1]["expected"]["execution_allowed_count"] == 0
