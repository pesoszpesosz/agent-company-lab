import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from service_worker_signed_decision_intake_contract_core import (  # noqa: E402
    NEXT_ACTION,
    REQUIRED_DECISION_FIELDS,
    ZERO_BOUNDARY,
    build_report,
    template_for_service,
    validate_template,
)


def authority_report() -> dict[str, object]:
    return {
        "coverage_status": "report_only_no_authority_granted",
        "service_count": 1,
        "current_request_count": 1,
        "current_requests_covered": 1,
        "request_rows": [
            {
                "request_id": "req-public-action",
                "service_id": "public_action_execution",
                "request_type": "public_action",
            }
        ],
        "service_rows": [
            {
                "service_id": "public_action_execution",
                "request_type": "public_action",
                "risk_family": "public_reputation",
                "authority_route": "human_user_cro_reputation_required_exact_public_action_only",
                "approval_required_by": ["human_user", "chief_risk_officer"],
            }
        ],
    }


def test_service_worker_signed_decision_intake_core_builds_in_memory_contract() -> None:
    schema = {"properties": {"decision": {"enum": ["deny"]}}}
    authority = authority_report()
    authority_validation = {"all_checks_passed": True, "failure_count": 0}
    service_row = authority["service_rows"][0]

    template = template_for_service(service_row, authority)
    assert template["service_id"] == "public_action_execution"
    assert template["allowed_request_ids"] == ["req-public-action"]
    assert "deny" in template["allowed_decisions"]
    assert "approve_exact_action_preflight_only" in template["allowed_decisions"]
    assert template["required_fields"] == REQUIRED_DECISION_FIELDS
    assert template["approval_is_not_apply"] is True
    assert template["exact_scope_required"] is True
    assert template["decision_example"]["runtime_boundary"] == ZERO_BOUNDARY
    assert validate_template(template, schema) == []

    report, validation = build_report(
        schema,
        authority=authority,
        authority_validation=authority_validation,
    )

    assert report["next_action"] == NEXT_ACTION
    assert report["contract_status"] == "report_only_intake_contract_ready"
    assert report["service_count"] == 1
    assert report["service_template_count"] == 1
    assert report["current_request_count"] == 1
    assert report["current_requests_covered"] == 1
    assert report["missing_required_field_count"] == 0
    assert report["all_checks_passed"] is True
    assert report["approval_granted_by_contract"] is False
    assert report["apply_allowed"] is False
    assert report["external_side_effects"] is False
    assert validation["all_checks_passed"] is True
    assert validation["failure_count"] == 0
    assert validation["templates_with_exact_scope_required_count"] == 1
    assert validation["templates_with_attestation_required_count"] == 1
    assert validation["approval_granted_by_contract"] is False
    assert validation["apply_allowed"] is False
    assert validation["external_side_effects"] is False
