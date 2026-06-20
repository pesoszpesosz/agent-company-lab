import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_egress_event_ledger_core import (  # noqa: E402
    POOL_ID,
    REPORT_ONLY_TYPES,
    ZERO_BOUNDARY,
    base_event,
    build_report,
    fixture_set,
    validate_event,
)


def test_agent_egress_event_ledger_core_blocks_live_egress_and_external_effects() -> None:
    event = base_event("egress-positive-boundary")

    assert event["worker_pool_id"] == POOL_ID == "service-worker-local-runtime-adapter-pool"
    assert event["egress_type"] in REPORT_ONLY_TYPES == {"agent_to_agent"}
    assert event["credential_scope"] == "none"
    assert event["browser_scope"] == "none"
    assert event["mcp_scope"] == "none"
    assert event["model_api_scope"] == "none"
    assert event["wallet_scope"] == "none"
    assert event["payment_scope"] == "none"
    assert event["public_action_scope"] == "none"
    assert event["external_side_effects_expected"] is False
    assert event["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 19
    assert fixtures[0]["expected"] == "accepted"
    assert any(item["name"] == "negative_gateway_started" for item in fixtures)
    assert any(item["name"] == "negative_model_call_recorded" for item in fixtures)
    assert any(item["name"] == "negative_mcp_call_recorded" for item in fixtures)
    assert any(item["name"] == "negative_service_request_assigned" for item in fixtures)

    schema = {"properties": {"policy_verdict": {"enum": ["deny", "allow_report_only_preflight"]}}}
    identity_validation = {"all_checks_passed": True, "accepted_count": 1}
    accepted = validate_event(event, schema, identity_validation)
    assert accepted["accepted_for_local_report_only_preflight"] is True
    assert accepted["live_egress_allowed"] is False
    assert accepted["registration_allowed"] is False
    assert accepted["assignment_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = base_event("egress-negative-boundary-live-egress")
    negative["runtime_boundary"]["live_egress_events_recorded"] = 1
    rejected = validate_event(negative, schema, identity_validation)
    assert rejected["accepted_for_local_report_only_preflight"] is False
    assert "runtime_boundary_live_egress_events_recorded_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, identity_validation, fixtures)
    assert report["positive_fixture"]["expected_result"] == "pass_report_only_preflight_event"
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["live_egress_allowed"] is False
    assert validation["gateway_started"] is False
    assert validation["gateway_installed"] is False
    assert validation["api_keys_created"] is False
    assert validation["live_egress_events_recorded"] == 0
    assert validation["model_api_calls"] is False
    assert validation["mcp_tool_calls"] is False
    assert validation["browser_sessions_started"] == 0
    assert validation["service_requests_assigned"] == 0
    assert validation["worker_starts"] == 0
    assert validation["external_side_effects"] is False