import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from local_a2a_egress_apply_command_contract_core import (  # noqa: E402
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


def test_local_a2a_apply_command_contract_core_blocks_live_agent_messages() -> None:
    command = base_command("local-a2a-apply-command-positive-contract")

    assert command["target_route_id"] == TARGET_ROUTE_ID == "local_agent_to_agent_report_only"
    assert command["target_egress_type"] == TARGET_EGRESS_TYPE == "agent_to_agent"
    assert command["apply_command_allowed"] is False
    assert command["apply_allowed"] is False
    assert command["agent_message_send_allowed"] is False
    assert command["agent_messages_sent"] == 0
    assert command["worker_start_allowed"] is False
    assert command["service_requests_assigned"] == 0
    assert command["service_requests_updated"] == 0
    assert command["model_api_calls"] is False
    assert command["mcp_tool_calls"] is False
    assert command["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 40
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_agent_messages_sent" for item in fixtures)
    assert any(item["name"] == "negative_agent_message_boundary_sent" for item in fixtures)

    schema = {
        "properties": {
            "command_type": {"enum": ["deny_noop", "report_only_apply_command_contract"]},
            "target_route_id": {"const": TARGET_ROUTE_ID},
            "target_egress_type": {"const": TARGET_EGRESS_TYPE},
            "agent_message_send_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }
    sources = source_summary()
    accepted = validate_command(command, schema, sources)
    assert accepted["accepted_for_contract_only"] is True
    assert accepted["errors"] == []

    negative = base_command("local-a2a-apply-command-negative-message")
    negative["agent_messages_sent"] = 1
    rejected = validate_command(negative, schema, sources)
    assert rejected["accepted_for_contract_only"] is False
    assert "agent_messages_sent_must_be_zero" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_command_allowed"] is False
    assert validation["agent_message_send_allowed"] is False
    assert validation["agent_messages_sent"] == 0
    assert validation["worker_start_allowed"] is False
    assert validation["external_side_effects"] is False