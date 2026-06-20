import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from public_action_egress_signed_decision_guard_core import (  # noqa: E402
    EGRESS_VALIDATION,
    INTAKE_VALIDATION,
    NEXT_ACTION,
    TARGET_EGRESS_TYPE,
    TARGET_ROUTE_ID,
    ZERO_BOUNDARY,
    base_decision,
    build_report,
    fixture_set,
    load_json,
    route_summary,
    validate_decision,
)


def test_public_action_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("public-action-egress-guard-positive-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "public_action_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "public_action_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "public_submission"
    assert decision["public_action_allowed"] is False
    assert decision["public_actions"] is False
    assert decision["browser_session_start_allowed"] is False
    assert decision["browser_sessions_started"] == 0
    assert decision["account_actions"] is False
    assert decision["service_requests_assigned"] == 0
    assert decision["service_requests_updated"] == 0
    assert decision["model_api_calls"] is False
    assert decision["mcp_tool_calls"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    accepted = validate_decision(decision, schema, route, intake_validation, egress_validation)
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("public-action-egress-guard-negative-public-action")
    negative["public_actions"] = True
    rejected = validate_decision(negative, schema, route, intake_validation, egress_validation)
    assert rejected["accepted_for_apply_preflight"] is False
    assert "public_actions_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 45
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_public_actions" for item in fixtures)
    assert any(item["name"] == "negative_boundary_post_created" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "public_action_execution_gate",
        "reputation_review_worker",
        "agent_egress_event_ledger_v1",
        "exact_action_body_approval",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["public_action_allowed"] is False
    assert validation["public_actions"] is False
    assert validation["browser_sessions_started"] == 0
    assert validation["external_side_effects"] is False