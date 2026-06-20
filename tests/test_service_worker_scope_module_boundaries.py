import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_service_worker_scope_facade_reexports_core_and_report_modules() -> None:
    from agent_company_core import service_worker_scope as facade
    from agent_company_core import service_worker_scope_core
    from agent_company_core import service_worker_scope_diff
    from agent_company_core import service_worker_scope_templates
    from agent_company_core import service_worker_approval_review

    assert facade.normalized_scope_text is service_worker_scope_core.normalized_scope_text
    assert facade.service_worker_scope_diff_entry is service_worker_scope_diff.service_worker_scope_diff_entry
    assert facade.write_service_worker_scope_diff is service_worker_scope_diff.write_service_worker_scope_diff
    assert facade.service_worker_scope_template_entry is service_worker_scope_templates.service_worker_scope_template_entry
    assert facade.write_service_worker_scope_templates is service_worker_scope_templates.write_service_worker_scope_templates
    assert facade.service_worker_approval_review_entry is service_worker_approval_review.service_worker_approval_review_entry
    assert facade.write_service_worker_approval_review is service_worker_approval_review.write_service_worker_approval_review
