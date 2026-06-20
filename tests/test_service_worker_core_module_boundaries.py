import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_service_worker_core_facade_reexports_phase_modules():
    from agent_company_core import service_worker_core
    from agent_company_core import service_worker_policy
    from agent_company_core import service_worker_readiness
    from agent_company_core import service_worker_request_synthesis
    from agent_company_core import service_workers

    assert service_worker_core.SERVICE_WORKER_TYPES is service_worker_policy.SERVICE_WORKER_TYPES
    assert service_worker_core.service_worker_type_for_request is service_worker_policy.service_worker_type_for_request
    assert service_worker_core.service_worker_expected_output is service_worker_policy.service_worker_expected_output
    assert service_worker_core.service_worker_packet_path is service_worker_request_synthesis.service_worker_packet_path
    assert (
        service_worker_core.synthesize_service_worker_request
        is service_worker_request_synthesis.synthesize_service_worker_request
    )
    assert (
        service_worker_core.validate_service_worker_request_object
        is service_worker_request_synthesis.validate_service_worker_request_object
    )
    assert service_worker_core.latest_approval_for_request is service_worker_readiness.latest_approval_for_request
    assert service_worker_core.approval_not_expired is service_worker_readiness.approval_not_expired
    assert service_worker_core.service_worker_readiness_entry is service_worker_readiness.service_worker_readiness_entry
    assert (
        service_worker_core.write_service_worker_execution_readiness
        is service_worker_readiness.write_service_worker_execution_readiness
    )
    assert service_workers.write_service_worker_execution_readiness is service_worker_core.write_service_worker_execution_readiness
