import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from local_a2a_egress_signed_decision_guard_core import (  # noqa: E402
    EGRESS_VALIDATION,
    IDENTITY_VALIDATION,
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


def test_local_a2a_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("local-a2a-egress-guard-positive-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "local_agent_to_agent_report_only"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "agent_to_agent"
    assert decision["gateway_registration_allowed"] is False
    assert decision["gateway_start_allowed"] is False
    assert decision["live_egress_allowed"] is False
    assert decision["agent_message_send_allowed"] is False
    assert decision["agent_messages_sent"] == 0
    assert decision["service_requests_assigned"] == 0
    assert decision["service_requests_updated"] == 0
    assert decision["model_api_calls"] is False
    assert decision["mcp_tool_calls"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    accepted = validate_decision(decision, schema, route, intake_validation, egress_validation, identity_validation)
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("local-a2a-egress-guard-negative-message-sent")
    negative["agent_messages_sent"] = 1
    rejected = validate_decision(negative, schema, route, intake_validation, egress_validation, identity_validation)
    assert rejected["accepted_for_apply_preflight"] is False
    assert "agent_messages_sent_must_be_zero" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 38
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_agent_messages_sent" for item in fixtures)
    assert any(item["name"] == "negative_boundary_agent_message_sent" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "agent_egress_event_ledger_v1",
        "local_runtime_adapter_pool_identity_envelope_v1",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["agent_message_send_allowed"] is False
    assert validation["agent_messages_sent"] == 0
    assert validation["external_side_effects"] is False