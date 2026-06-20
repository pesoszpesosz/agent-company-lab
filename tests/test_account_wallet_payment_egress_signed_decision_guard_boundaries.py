import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from account_wallet_payment_egress_signed_decision_guard_core import (  # noqa: E402
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
    EGRESS_VALIDATION,
    IDENTITY_VALIDATION,
    INTAKE_VALIDATION,
)


def test_signed_decision_guard_core_accepts_only_report_only_preflight_decisions() -> None:
    decision = base_decision("account-wallet-payment-guard-positive-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "account_creation_allowed": {"const": False},
            "wallet_creation_allowed": {"const": False},
            "private_key_custody_allowed": {"const": False},
            "funds_transfer_allowed": {"const": False},
            "payment_action_allowed": {"const": False},
            "legal_kyc_tax_action_allowed": {"const": False},
            "public_payment_address_allowed": {"const": False},
            "real_money_action_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "account_wallet_payment_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "account_wallet_payment"
    assert decision["gateway_registration_allowed"] is False
    assert decision["account_creation_allowed"] is False
    assert decision["wallet_creation_allowed"] is False
    assert decision["payment_action_allowed"] is False
    assert decision["real_money_action_allowed"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    identity_validation = load_json(IDENTITY_VALIDATION)
    accepted = validate_decision(decision, schema, route, intake_validation, egress_validation, identity_validation)
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("account-wallet-payment-guard-negative-payment-action")
    negative["payment_action_allowed"] = True
    rejected = validate_decision(negative, schema, route, intake_validation, egress_validation, identity_validation)
    assert rejected["accepted_for_apply_preflight"] is False
    assert "payment_action_allowed_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 50
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_payment_action_allowed" for item in fixtures)
    assert any(item["name"] == "negative_boundary_funds_transferred" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "account_registration_intake",
        "wallet_setup_packet",
        "wallet_public_address_response",
        "legal_kyc_tax_payment_gate",
        "agent_egress_event_ledger_v1",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_allowed"] is False
    assert validation["external_side_effects"] is False