import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from ceo_operator_event_surface_contract_core import (  # noqa: E402
    EVENT_TYPES,
    NEXT_ACTION,
    ZERO_BOUNDARY,
    base_event,
    build_report,
    fixture_set,
    source_summary,
    validate_event,
)


def test_ceo_operator_event_surface_core_accepts_report_only_events_without_live_transport() -> None:
    event_type, label, producer, consumer = EVENT_TYPES[0]
    event = base_event(event_type, label, producer, consumer)
    schema = {
        "properties": {
            "event_surface_status": {"const": "report_only_contract"},
            "event_transport_enabled": {"const": False},
            "sse_enabled": {"const": False},
            "websocket_enabled": {"const": False},
            "approval_granted_by_event": {"const": False},
        }
    }
    sources = source_summary()

    assert len(EVENT_TYPES) >= 12
    assert event["event_surface_status"] == "report_only_contract"
    assert event["event_type"] == event_type == "ceo_review_snapshot"
    assert event["producer_role"] == producer == "ceo"
    assert event["consumer_role"] == consumer == "all_managers"
    assert event["event_transport_enabled"] is False
    assert event["sse_enabled"] is False
    assert event["websocket_enabled"] is False
    assert event["approval_granted_by_event"] is False
    assert event["worker_start_allowed"] is False
    assert event["service_request_mutation_allowed"] is False
    assert event["model_api_call_allowed"] is False
    assert event["mcp_tool_call_allowed"] is False
    assert event["public_action_allowed"] is False
    assert event["external_side_effects"] is False
    assert event["runtime_boundary"] == ZERO_BOUNDARY

    accepted_errors = validate_event(event, schema, sources)
    assert accepted_errors == []

    negative = copy.deepcopy(event)
    negative["runtime_boundary"]["operator_events_emitted"] = 1
    rejected_errors = validate_event(negative, schema, sources)
    assert "runtime_boundary_operator_events_emitted_must_equal_0" in rejected_errors

    fixtures = fixture_set()
    assert len(fixtures) >= len(EVENT_TYPES) + 20
    assert all(item["expected"] == "accepted" for item in fixtures[: len(EVENT_TYPES)])
    assert any(item["name"] == "negative_event_transport_enabled" for item in fixtures)
    assert any(item["name"] == "negative_boundary_operator_events_emitted" for item in fixtures)
    assert any(item["name"] == "negative_boundary_external_side_effects" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["contract_status"] == "report_only_event_surface_ready"
    assert set(report["event_type_ids"]) == {item[0] for item in EVENT_TYPES}
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == len(EVENT_TYPES)
    assert validation["rejected_count"] == validation["fixture_count"] - len(EVENT_TYPES)
    assert validation["event_transport_enabled"] is False
    assert validation["sse_enabled"] is False
    assert validation["websocket_enabled"] is False
    assert validation["operator_events_emitted"] == 0
    assert validation["operator_events_persisted"] == 0
    assert validation["service_requests_updated"] == 0
    assert validation["worker_starts"] == 0
    assert validation["browser_sessions_started"] == 0
    assert validation["model_api_calls"] is False
    assert validation["mcp_tool_calls"] is False
    assert validation["external_side_effects"] is False
