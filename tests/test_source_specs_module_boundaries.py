import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_source_specs_facade_reexports_phase_modules():
    from agent_company_core import source_spec_seed_apply
    from agent_company_core import source_spec_seed_packets
    from agent_company_core import source_specs
    from agent_company_core import source_specs_report

    assert source_specs.write_source_specs_report is source_specs_report.write_source_specs_report
    assert source_specs.proposed_source_spec_seed is source_spec_seed_packets.proposed_source_spec_seed
    assert source_specs.write_source_spec_seed_packets is source_spec_seed_packets.write_source_spec_seed_packets
    assert source_specs.write_source_spec_seed_apply is source_spec_seed_apply.write_source_spec_seed_apply
