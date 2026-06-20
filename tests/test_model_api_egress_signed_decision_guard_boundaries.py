import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from model_api_egress_signed_decision_guard_core import (  # noqa: E402
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


def test_model_api_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("model-api-egress-guard-positive-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "model_api_call_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "model_api_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "model_api"
    assert decision["provider_key_use_allowed"] is False
    assert decision["provider_keys_used"] is False
    assert decision["model_api_call_allowed"] is False
    assert decision["model_api_calls"] is False
    assert decision["training_data_upload_allowed"] is False
    assert decision["training_data_uploaded"] is False
    assert decision["max_cost_usd"] == 0
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    accepted = validate_decision(decision, schema, route, intake_validation, egress_validation, identity_validation)
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("model-api-egress-guard-negative-live-call")
    negative["model_api_calls"] = True
    rejected = validate_decision(negative, schema, route, intake_validation, egress_validation, identity_validation)
    assert rejected["accepted_for_apply_preflight"] is False
    assert "model_api_calls_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 45
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_model_api_called" for item in fixtures)
    assert any(item["name"] == "negative_boundary_provider_keys_used" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "model_api_execution_gate",
        "secrets_credentials_handling_gate",
        "agent_egress_event_ledger_v1",
        "cost_budget_signed_decision",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["model_api_call_allowed"] is False
    assert validation["model_api_calls"] is False
    assert validation["provider_keys_used"] is False
    assert validation["external_side_effects"] is False