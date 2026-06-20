import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_profit_edge_import_facade_reexports_import_layers():
    from agent_company_core import profit_edge_import
    from agent_company_core import profit_edge_import_command
    from agent_company_core import profit_edge_ledger_import
    from agent_company_core import profit_edge_source_summary

    assert profit_edge_import.summarize_source_file is profit_edge_source_summary.summarize_source_file
    assert profit_edge_import.find_first_url is profit_edge_source_summary.find_first_url
    assert profit_edge_import.normalize_profit_edge_lane is profit_edge_ledger_import.normalize_profit_edge_lane
    assert profit_edge_import.import_ledger_rows is profit_edge_ledger_import.import_ledger_rows
    assert profit_edge_import.write_profit_edge_import_report is profit_edge_import_command.write_profit_edge_import_report
    assert profit_edge_import.import_profit_edge is profit_edge_import_command.import_profit_edge
    assert profit_edge_import.PROFIT_EDGE_REPORT_IMPORTS is profit_edge_import_command.PROFIT_EDGE_REPORT_IMPORTS
