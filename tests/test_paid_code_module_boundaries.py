import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_paid_code_facade_reexports_stage_modules() -> None:
    from agent_company_core import paid_code as facade
    from agent_company_core import paid_code_duplicate_check
    from agent_company_core import paid_code_local_answers
    from agent_company_core import paid_code_browser_refresh

    assert facade.paid_code_duplicate_check_items is paid_code_duplicate_check.paid_code_duplicate_check_items
    assert facade.write_paid_code_duplicate_check_worksheet is paid_code_duplicate_check.write_paid_code_duplicate_check_worksheet
    assert facade.paid_code_local_answer_payloads is paid_code_local_answers.paid_code_local_answer_payloads
    assert facade.write_paid_code_local_worksheet_answers is paid_code_local_answers.write_paid_code_local_worksheet_answers
    assert facade.paid_code_browser_refresh_scope_items is paid_code_browser_refresh.paid_code_browser_refresh_scope_items
    assert facade.paid_code_browser_refresh_forbidden_actions is paid_code_browser_refresh.paid_code_browser_refresh_forbidden_actions
    assert facade.write_paid_code_browser_refresh_decision_packet is paid_code_browser_refresh.write_paid_code_browser_refresh_decision_packet
