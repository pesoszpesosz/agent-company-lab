import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_durable_adapter_human_decision_facade_reexports_phase_modules():
    from agent_company_core import durable_adapter_human_approval_packet
    from agent_company_core import durable_adapter_human_decision
    from agent_company_core import durable_adapter_human_decision_intake
    from agent_company_core import durable_adapters

    assert (
        durable_adapter_human_decision.write_durable_adapter_runtime_human_approval_packet
        is durable_adapter_human_approval_packet.write_durable_adapter_runtime_human_approval_packet
    )
    assert (
        durable_adapter_human_decision.write_durable_adapter_runtime_human_decision_intake_packet
        is durable_adapter_human_decision_intake.write_durable_adapter_runtime_human_decision_intake_packet
    )
    assert (
        durable_adapters.write_durable_adapter_runtime_human_approval_packet
        is durable_adapter_human_decision.write_durable_adapter_runtime_human_approval_packet
    )
    assert (
        durable_adapters.write_durable_adapter_runtime_human_decision_intake_packet
        is durable_adapter_human_decision.write_durable_adapter_runtime_human_decision_intake_packet
    )
