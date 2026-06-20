import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from mcp_tool_registry_gate_core import (  # noqa: E402
    SERVER_ID,
    TOOL_ID,
    ZERO_BOUNDARY,
    base_entry,
    build_report,
    fixture_set,
    validate_entry,
)


def test_mcp_tool_registry_gate_core_stays_report_only_without_server_or_tool_activation() -> None:
    entry = base_entry("mcp-entry-positive-boundary")

    assert entry["server_id"] == SERVER_ID == "local-report-only-fixture-mcp"
    assert entry["allowed_tools"] == [TOOL_ID]
    assert entry["default_status"] == "approved_report_only"
    assert entry["credential_requirements"] == "none"
    assert entry["network_scope"] == "none"
    assert entry["write_action_capable"] is False
    assert entry["public_action_capable"] is False
    assert entry["payment_or_wallet_capable"] is False
    assert entry["browser_capable"] is False
    assert entry["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 19
    assert fixtures[0]["expected"] == "accepted"
    assert any(item["name"] == "negative_mcp_server_started" for item in fixtures)
    assert any(item["name"] == "negative_mcp_tool_called" for item in fixtures)
    assert any(item["name"] == "negative_registry_published" for item in fixtures)

    schema = {"properties": {"default_status": {"enum": ["disabled", "approved_report_only"]}}}
    identity_validation = {"all_checks_passed": True}
    egress_validation = {"all_checks_passed": True, "live_egress_allowed": False}

    accepted = validate_entry(entry, schema, identity_validation, egress_validation)
    assert accepted["accepted_for_local_report_only_registry"] is True
    assert accepted["mcp_server_enable_allowed"] is False
    assert accepted["mcp_tool_call_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = base_entry("mcp-entry-negative-boundary-tool-call")
    negative["runtime_boundary"]["mcp_tool_calls"] = True
    rejected = validate_entry(negative, schema, identity_validation, egress_validation)
    assert rejected["accepted_for_local_report_only_registry"] is False
    assert "runtime_boundary_mcp_tool_calls_must_equal_False" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, identity_validation, egress_validation, fixtures)
    assert report["positive_fixture"]["expected_result"] == "pass_local_report_only_registry_entry"
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["mcp_servers_started"] == 0
    assert validation["mcp_servers_installed"] == 0
    assert validation["mcp_servers_enabled"] == 0
    assert validation["mcp_tool_calls"] is False
    assert validation["credentials_created"] is False
    assert validation["registry_publications"] == 0
    assert validation["external_side_effects"] is False