import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from egress_route_signed_decision_guard_core import (  # noqa: E402
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


def test_egress_route_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("egress-route-guard-positive-boundary")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "browser_read_only_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "browser_read_only"
    assert decision["gateway_registration_allowed"] is False
    assert decision["gateway_start_allowed"] is False
    assert decision["live_egress_allowed"] is False
    assert decision["browser_session_start_allowed"] is False
    assert decision["service_requests_assigned"] == 0
    assert decision["service_requests_updated"] == 0
    assert decision["model_api_calls"] is False
    assert decision["mcp_tool_calls"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    accepted = validate_decision(decision, schema, route, intake_validation)
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("egress-route-guard-negative-boundary-browser-start")
    negative["runtime_boundary"]["browser_sessions_started"] = 1
    rejected = validate_decision(negative, schema, route, intake_validation)
    assert rejected["accepted_for_apply_preflight"] is False
    assert "runtime_boundary_browser_sessions_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 30
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_browser_start_allowed" for item in fixtures)
    assert any(item["name"] == "negative_boundary_browser_started" for item in fixtures)
    assert any(item["name"] == "negative_boundary_external_side_effect" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) >= {
        "browser_read_only_apply_command_contract_v1",
        "agent_egress_event_ledger_v1",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["gateway_registrations"] == 0
    assert validation["gateway_starts"] == 0
    assert validation["live_egress_events"] == 0
    assert validation["browser_sessions_started"] == 0
    assert validation["worker_starts"] == 0
    assert validation["external_side_effects"] is False
