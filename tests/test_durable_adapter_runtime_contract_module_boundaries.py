import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_durable_adapter_runtime_contract_facade_reexports_phase_modules():
    from agent_company_core import durable_adapter_runtime_contract
    from agent_company_core import durable_adapter_runtime_import_guard
    from agent_company_core import durable_adapter_runtime_interface_contract
    from agent_company_core import durable_adapter_service_worker_integration
    from agent_company_core import durable_adapters

    assert (
        durable_adapter_runtime_contract.write_durable_adapter_service_worker_integration
        is durable_adapter_service_worker_integration.write_durable_adapter_service_worker_integration
    )
    assert (
        durable_adapter_runtime_contract.forbidden_runtime_imports_in_source
        is durable_adapter_runtime_import_guard.forbidden_runtime_imports_in_source
    )
    assert (
        durable_adapter_runtime_contract.write_durable_adapter_runtime_interface_contract
        is durable_adapter_runtime_interface_contract.write_durable_adapter_runtime_interface_contract
    )
    assert (
        durable_adapters.write_durable_adapter_service_worker_integration
        is durable_adapter_runtime_contract.write_durable_adapter_service_worker_integration
    )
    assert (
        durable_adapters.forbidden_runtime_imports_in_source
        is durable_adapter_runtime_contract.forbidden_runtime_imports_in_source
    )
    assert (
        durable_adapters.write_durable_adapter_runtime_interface_contract
        is durable_adapter_runtime_contract.write_durable_adapter_runtime_interface_contract
    )


def test_durable_adapter_runtime_import_guard_scans_split_modules():
    from agent_company_core.durable_adapter_runtime_import_guard import forbidden_runtime_imports_in_source

    assert forbidden_runtime_imports_in_source() == []
