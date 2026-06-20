import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from mcp_egress_signed_decision_guard_core import (  # noqa: E402
    EGRESS_VALIDATION,
    IDENTITY_VALIDATION,
    INTAKE_VALIDATION,
    MCP_GATE_VALIDATION,
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


def test_mcp_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("mcp-egress-guard-positive-mcp-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "mcp_tool_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "mcp_tool"
    assert decision["gateway_registration_allowed"] is False
    assert decision["gateway_start_allowed"] is False
    assert decision["live_egress_allowed"] is False
    assert decision["mcp_servers_started"] == 0
    assert decision["mcp_servers_enabled"] == 0
    assert decision["mcp_tool_call_allowed"] is False
    assert decision["credentials_created"] is False
    assert decision["credential_access_allowed"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    mcp_gate_validation = load_json(MCP_GATE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    accepted = validate_decision(
        decision,
        schema,
        route,
        intake_validation,
        mcp_gate_validation,
        egress_validation,
        identity_validation,
    )
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("mcp-egress-guard-negative-tool-call")
    negative["mcp_tool_calls"] = True
    rejected = validate_decision(
        negative,
        schema,
        route,
        intake_validation,
        mcp_gate_validation,
        egress_validation,
        identity_validation,
    )
    assert rejected["accepted_for_apply_preflight"] is False
    assert "mcp_tool_calls_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 40
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_mcp_tool_call" for item in fixtures)
    assert any(item["name"] == "negative_boundary_mcp_server_started" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "mcp_tool_registry_gate_v1",
        "agent_egress_event_ledger_v1",
        "local_runtime_adapter_pool_identity_envelope_v1",
        "signed_operator_decision_required",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["mcp_servers_started"] == 0
    assert validation["mcp_servers_enabled"] == 0
    assert validation["mcp_tool_calls"] is False
    assert validation["credentials_created"] is False
    assert validation["external_side_effects"] is False