import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from mcp_egress_apply_command_guard_core import (  # noqa: E402
    NEXT_ACTION,
    TARGET_EGRESS_TYPE,
    TARGET_ROUTE_ID,
    ZERO_BOUNDARY,
    base_command,
    build_report,
    fixture_set,
    source_summary,
    validate_command,
)


def test_mcp_apply_command_guard_core_blocks_live_mcp_execution() -> None:
    command = base_command("mcp-egress-apply-command-positive-guard")

    assert command["target_route_id"] == TARGET_ROUTE_ID == "mcp_tool_gateway"
    assert command["target_egress_type"] == TARGET_EGRESS_TYPE == "mcp_tool"
    assert command["apply_command_allowed"] is False
    assert command["mcp_server_enable_allowed"] is False
    assert command["mcp_tool_call_allowed"] is False
    assert command["mcp_servers_started"] == 0
    assert command["mcp_servers_enabled"] == 0
    assert command["credentials_created"] is False
    assert command["credential_access_allowed"] is False
    assert command["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 38
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_mcp_tool_call_allowed" for item in fixtures)
    assert any(item["name"] == "negative_boundary_credentials_created" for item in fixtures)

    schema = {
        "properties": {
            "command_type": {"enum": ["deny_noop", "report_only_apply_command_guard"]},
            "target_route_id": {"const": TARGET_ROUTE_ID},
            "target_egress_type": {"const": TARGET_EGRESS_TYPE},
            "live_egress_allowed": {"const": False},
        }
    }
    source = source_summary()
    accepted = validate_command(command, schema, source)
    assert accepted["accepted_for_guard_only"] is True
    assert accepted["errors"] == []

    negative = base_command("mcp-egress-apply-command-negative-live-tool")
    negative["mcp_tool_call_allowed"] = True
    rejected = validate_command(negative, schema, source)
    assert rejected["accepted_for_guard_only"] is False
    assert "mcp_tool_call_allowed_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_command_allowed"] is False
    assert validation["mcp_tool_call_allowed"] is False
    assert validation["external_side_effects"] is False