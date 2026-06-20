import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from egress_route_apply_command_contract_core import (  # noqa: E402
    TARGET_ROUTE_ID,
    ZERO_BOUNDARY,
    base_command,
    build_report,
    fixture_set,
    source_summary,
    validate_command,
)


def test_egress_route_apply_command_contract_core_blocks_live_browser_egress() -> None:
    command = base_command("egress-route-apply-command-positive-boundary")

    assert command["target_route_id"] == TARGET_ROUTE_ID == "browser_read_only_gateway"
    assert command["apply_command_allowed"] is False
    assert command["apply_allowed"] is False
    assert command["gateway_registration_allowed"] is False
    assert command["gateway_start_allowed"] is False
    assert command["live_egress_allowed"] is False
    assert command["browser_session_start_allowed"] is False
    assert command["worker_start_allowed"] is False
    assert command["service_requests_assigned"] == 0
    assert command["service_requests_updated"] == 0
    assert command["model_api_calls"] is False
    assert command["mcp_tool_calls"] is False
    assert command["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 35
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_browser_start_allowed" for item in fixtures)
    assert any(item["name"] == "negative_browser_started" for item in fixtures)
    assert any(item["name"] == "negative_service_request_boundary" for item in fixtures)

    schema = {
        "properties": {
            "command_type": {"enum": ["deny_noop", "report_only_apply_command_contract"]},
            "target_route_id": {"const": TARGET_ROUTE_ID},
        }
    }
    sources = source_summary()
    accepted = validate_command(command, schema, sources)
    assert accepted["accepted_for_contract_only"] is True
    assert accepted["errors"] == []

    negative = base_command("egress-route-apply-command-negative-browser-start")
    negative["runtime_boundary"]["browser_sessions_started"] = 1
    rejected = validate_command(negative, schema, sources)
    assert rejected["accepted_for_contract_only"] is False
    assert "runtime_boundary_browser_sessions_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["next_action"] == (
        "Build egress route apply-command guard v1 only after a real signed operator decision and executable "
        "command preview exist; until then, keep browser egress blocked."
    )
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_command_allowed"] is False
    assert validation["gateway_start_allowed"] is False
    assert validation["live_egress_allowed"] is False
    assert validation["browser_session_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["external_side_effects"] is False