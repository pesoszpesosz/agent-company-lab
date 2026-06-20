import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_service_worker_decision_packets_facade_reexports_phase_modules():
    from agent_company_core import service_worker_decision_packets as packet_facade
    from agent_company_core import service_worker_human_decision_packets
    from agent_company_core import service_worker_post_decision_refresh_plan
    from agent_company_core import service_worker_post_decision_simulation

    assert (
        packet_facade.service_worker_human_decision_packet_rows
        is service_worker_human_decision_packets.service_worker_human_decision_packet_rows
    )
    assert (
        packet_facade.write_service_worker_human_decision_packets
        is service_worker_human_decision_packets.write_service_worker_human_decision_packets
    )
    assert (
        packet_facade.service_worker_post_decision_simulation_rows
        is service_worker_post_decision_simulation.service_worker_post_decision_simulation_rows
    )
    assert (
        packet_facade.write_service_worker_post_decision_simulation
        is service_worker_post_decision_simulation.write_service_worker_post_decision_simulation
    )
    assert (
        packet_facade.service_worker_post_decision_refresh_plan_rows
        is service_worker_post_decision_refresh_plan.service_worker_post_decision_refresh_plan_rows
    )
    assert (
        packet_facade.write_service_worker_post_decision_refresh_plan
        is service_worker_post_decision_refresh_plan.write_service_worker_post_decision_refresh_plan
    )


def test_service_worker_decisions_facade_reexports_phase_modules():
    from agent_company_core import service_worker_decision_authority
    from agent_company_core import service_worker_decision_packets
    from agent_company_core import service_worker_decision_safety
    from agent_company_core import service_worker_decisions as decision_facade
    from agent_company_core import service_workers

    assert (
        decision_facade.service_worker_human_decision_packet_rows
        is service_worker_decision_packets.service_worker_human_decision_packet_rows
    )
    assert (
        decision_facade.write_service_worker_human_decision_packets
        is service_worker_decision_packets.write_service_worker_human_decision_packets
    )
    assert (
        decision_facade.service_worker_post_decision_simulation_rows
        is service_worker_decision_packets.service_worker_post_decision_simulation_rows
    )
    assert (
        decision_facade.write_service_worker_post_decision_simulation
        is service_worker_decision_packets.write_service_worker_post_decision_simulation
    )
    assert (
        decision_facade.service_worker_post_decision_refresh_plan_rows
        is service_worker_decision_packets.service_worker_post_decision_refresh_plan_rows
    )
    assert (
        decision_facade.write_service_worker_post_decision_refresh_plan
        is service_worker_decision_packets.write_service_worker_post_decision_refresh_plan
    )

    assert (
        decision_facade.service_worker_decision_drift_rows
        is service_worker_decision_safety.service_worker_decision_drift_rows
    )
    assert (
        decision_facade.write_service_worker_decision_command_safety
        is service_worker_decision_safety.write_service_worker_decision_command_safety
    )

    assert (
        decision_facade.service_worker_decision_authority_for_packet
        is service_worker_decision_authority.service_worker_decision_authority_for_packet
    )
    assert (
        decision_facade.write_service_worker_decision_preflight
        is service_worker_decision_authority.write_service_worker_decision_preflight
    )
    assert service_workers.write_service_worker_decision_preflight is decision_facade.write_service_worker_decision_preflight

def test_service_worker_decision_authority_facade_reexports_phase_modules():
    from agent_company_core import service_worker_decision_authority
    from agent_company_core import service_worker_decision_authority_matrix
    from agent_company_core import service_worker_decision_preflight

    assert (
        service_worker_decision_authority.service_worker_decision_authority_for_packet
        is service_worker_decision_authority_matrix.service_worker_decision_authority_for_packet
    )
    assert (
        service_worker_decision_authority.service_worker_decision_authority_matrix_rows
        is service_worker_decision_authority_matrix.service_worker_decision_authority_matrix_rows
    )
    assert (
        service_worker_decision_authority.write_service_worker_decision_authority_matrix
        is service_worker_decision_authority_matrix.write_service_worker_decision_authority_matrix
    )
    assert (
        service_worker_decision_authority.service_worker_decision_preflight_rows
        is service_worker_decision_preflight.service_worker_decision_preflight_rows
    )
    assert (
        service_worker_decision_authority.write_service_worker_decision_preflight
        is service_worker_decision_preflight.write_service_worker_decision_preflight
    )

def test_service_worker_decision_safety_facade_reexports_phase_modules():
    from agent_company_core import service_worker_decision_command_safety
    from agent_company_core import service_worker_decision_drift
    from agent_company_core import service_worker_decision_safety
    from agent_company_core import service_workers

    assert (
        service_worker_decision_safety.service_worker_decision_drift_rows
        is service_worker_decision_drift.service_worker_decision_drift_rows
    )
    assert (
        service_worker_decision_safety.write_service_worker_decision_drift_guard
        is service_worker_decision_drift.write_service_worker_decision_drift_guard
    )
    assert (
        service_worker_decision_safety.service_worker_decision_command_safety_rows
        is service_worker_decision_command_safety.service_worker_decision_command_safety_rows
    )
    assert (
        service_worker_decision_safety.write_service_worker_decision_command_safety
        is service_worker_decision_command_safety.write_service_worker_decision_command_safety
    )
    assert service_workers.write_service_worker_decision_drift_guard is service_worker_decision_safety.write_service_worker_decision_drift_guard
    assert service_workers.write_service_worker_decision_command_safety is service_worker_decision_safety.write_service_worker_decision_command_safety
