import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from telemetry_export_egress_signed_decision_guard_core import (  # noqa: E402
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


def test_telemetry_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("telemetry-export-guard-positive-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "telemetry_export_allowed": {"const": False},
            "external_trace_export_allowed": {"const": False},
            "private_prompt_upload_allowed": {"const": False},
            "credential_export_allowed": {"const": False},
            "unredacted_log_sync_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "telemetry_export_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "telemetry_export"
    assert decision["telemetry_export_allowed"] is False
    assert decision["external_trace_export_allowed"] is False
    assert decision["private_prompt_upload_allowed"] is False
    assert decision["credential_export_allowed"] is False
    assert decision["unredacted_log_sync_allowed"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    accepted = validate_decision(decision, schema, route, intake_validation, egress_validation, identity_validation)
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("telemetry-export-guard-negative-live-export")
    negative["telemetry_export_allowed"] = True
    rejected = validate_decision(negative, schema, route, intake_validation, egress_validation, identity_validation)
    assert rejected["accepted_for_apply_preflight"] is False
    assert "telemetry_export_allowed_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 45
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_telemetry_export_allowed" for item in fixtures)
    assert any(item["name"] == "negative_boundary_credentials_exported" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "telemetry_privacy_export_gate_v1",
        "agent_egress_event_ledger_v1",
        "secrets_credentials_handling_gate",
    }
    assert set(report["blocked_actions"]) == {
        "external_trace_export",
        "private_prompt_upload",
        "credential_export",
        "unredacted_log_sync",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["telemetry_export_allowed"] is False
    assert validation["external_side_effects"] is False