import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from account_wallet_payment_egress_apply_command_contract_core import (  # noqa: E402
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


def test_apply_command_contract_core_builds_and_rejects_fixtures() -> None:
    command = base_command("account-wallet-payment-apply-command-positive-contract")

    assert command["target_route_id"] == TARGET_ROUTE_ID == "account_wallet_payment_gateway"
    assert command["target_egress_type"] == TARGET_EGRESS_TYPE == "account_wallet_payment"
    assert command["apply_command_allowed"] is False
    assert command["account_creation_allowed"] is False
    assert command["wallet_creation_allowed"] is False
    assert command["payment_action_allowed"] is False
    assert command["real_money_action_allowed"] is False
    assert command["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 50
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_payment_action_allowed" for item in fixtures)
    assert any(item["name"] == "negative_boundary_funds_transferred" for item in fixtures)

    schema = {
        "properties": {
            "command_type": {"enum": ["deny_noop", "report_only_apply_command_contract"]},
            "target_route_id": {"const": TARGET_ROUTE_ID},
            "target_egress_type": {"const": TARGET_EGRESS_TYPE},
            "account_creation_allowed": {"const": False},
            "wallet_creation_allowed": {"const": False},
            "payment_action_allowed": {"const": False},
            "real_money_action_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }
    sources = source_summary()
    accepted = validate_command(command, schema, sources)
    assert accepted["accepted_for_contract_only"] is True
    assert accepted["errors"] == []

    negative = base_command("account-wallet-payment-apply-command-negative-payment")
    negative["payment_action_allowed"] = True
    rejected = validate_command(negative, schema, sources)
    assert rejected["accepted_for_contract_only"] is False
    assert "payment_action_allowed_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_command_allowed"] is False
    assert validation["external_side_effects"] is False