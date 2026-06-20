import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_service_requests_facade_reexports_workflow_modules():
    from agent_company_core import service_requests as facade
    from agent_company_core import service_requests_core
    from agent_company_core import service_requests_lifecycle
    from agent_company_core import service_requests_review
    from agent_company_core import service_requests_scaffold

    assert facade.resolve_service_catalog_entry is service_requests_core.resolve_service_catalog_entry
    assert facade.validate_service_intake is service_requests_core.validate_service_intake
    assert facade.create_service_request is service_requests_core.create_service_request
    assert facade.get_service_request is service_requests_core.get_service_request
    assert facade.validate_service_request_record is service_requests_core.validate_service_request_record
    assert facade.validate_service_request is service_requests_core.validate_service_request

    assert facade.service_request_where is service_requests_review.service_request_where
    assert facade.service_request_recommendation is service_requests_review.service_request_recommendation
    assert facade.write_service_request_review is service_requests_review.write_service_request_review

    assert facade.generated_service_request_id is service_requests_scaffold.generated_service_request_id
    assert facade.render_service_request_packet is service_requests_scaffold.render_service_request_packet
    assert facade.render_service_request_checklist is service_requests_scaffold.render_service_request_checklist
    assert facade.scaffold_service_request is service_requests_scaffold.scaffold_service_request

    assert facade.approve_service_request is service_requests_lifecycle.approve_service_request
    assert facade.reject_service_request is service_requests_lifecycle.reject_service_request
    assert facade.assign_service_request is service_requests_lifecycle.assign_service_request
    assert facade.start_service_request is service_requests_lifecycle.start_service_request
    assert facade.complete_service_request is service_requests_lifecycle.complete_service_request