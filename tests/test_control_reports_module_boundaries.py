import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_control_reports_facade_reexports_report_modules() -> None:
    from agent_company_core import control_ceo_review
    from agent_company_core import control_expansion_gap_map
    from agent_company_core import control_reports
    from agent_company_core import control_status_reports

    assert control_reports.list_status is control_status_reports.list_status
    assert control_reports.write_dashboard is control_status_reports.write_dashboard
    assert control_reports.lane_recommendation is control_ceo_review.lane_recommendation
    assert control_reports.write_ceo_review is control_ceo_review.write_ceo_review
    assert control_reports.suggested_manager_task is control_expansion_gap_map.suggested_manager_task
    assert control_reports.write_company_expansion_gap_map is control_expansion_gap_map.write_company_expansion_gap_map
