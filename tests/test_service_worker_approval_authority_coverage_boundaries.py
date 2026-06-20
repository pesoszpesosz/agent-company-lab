import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from service_worker_approval_authority_coverage_core import (  # noqa: E402
    NEXT_ACTION,
    ZERO_BOUNDARY,
    build_report,
)


def test_service_worker_approval_authority_core_builds_in_memory_report_without_grants() -> None:
    schema = {"properties": {"coverage_status": {"enum": ["report_only_no_authority_granted"]}}}
    services = [
        {
            "service_id": "public_action_execution",
            "department_id": "growth",
            "name": "Public action execution",
            "request_type": "public_action",
            "owner_role_id": "public_action_worker",
            "purpose": "Prepare an externally visible action for approval.",
            "allowed_actions": ["draft_public_reply"],
            "hard_gates": ["Do not post without explicit human user and CRO approval."],
            "required_intake": ["target_url"],
            "approval_required_by": ["user", "chief_risk_officer"],
            "output_artifacts": ["decision_packet"],
            "default_status": "gated",
        }
    ]
    requests = [
        {
            "request_id": "req-public-action",
            "service_id": "public_action_execution",
            "request_type": "public_action",
            "lane_id": "growth",
            "status": "queued",
            "risk_gate": "public_reputation",
            "requested_action": "draft_public_reply",
            "approval_scope": "report_only",
            "artifact_path": "reports/public-action.json",
            "assigned_agent_id": None,
            "started_at": None,
            "completed_at": None,
        }
    ]

    report, validation = build_report(
        schema,
        known_roles={"public_action_worker", "chief_risk_officer"},
        services=services,
        requests=requests,
        minimum_service_count=1,
    )

    assert report["next_action"] == NEXT_ACTION
    assert report["coverage_status"] == "report_only_no_authority_granted"
    assert report["service_count"] == 1
    assert report["current_request_count"] == 1
    assert report["service_rows_covered"] == 1
    assert report["current_requests_covered"] == 1
    assert report["all_checks_passed"] is True
    assert report["failures"] == []
    assert report["approval_granted_by_coverage"] is False
    assert report["external_side_effects"] is False
    assert validation["all_checks_passed"] is True
    assert validation["failure_count"] == 0
    assert validation["service_rows_covered"] == validation["service_count"]
    assert validation["current_requests_covered"] == validation["current_request_count"]
    assert validation["approval_granted_by_coverage"] is False
    assert validation["external_side_effects"] is False
    assert report["service_rows"][0]["authority_route"] == (
        "human_user_cro_reputation_required_exact_public_action_only"
    )
    for key, value in ZERO_BOUNDARY.items():
        assert report["service_rows"][0][key] == value
        assert report["request_rows"][0][key] == value
