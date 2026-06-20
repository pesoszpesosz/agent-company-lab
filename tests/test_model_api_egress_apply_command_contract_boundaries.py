import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from model_api_egress_apply_command_contract_core import (  # noqa: E402
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


def test_model_api_apply_command_contract_core_blocks_live_model_api_calls() -> None:
    command = base_command("model-api-apply-command-positive-contract")

    assert command["target_route_id"] == TARGET_ROUTE_ID == "model_api_gateway"
    assert command["target_egress_type"] == TARGET_EGRESS_TYPE == "model_api"
    assert command["apply_command_allowed"] is False
    assert command["provider_key_use_allowed"] is False
    assert command["provider_keys_used"] is False
    assert command["model_api_call_allowed"] is False
    assert command["model_api_calls"] is False
    assert command["training_data_upload_allowed"] is False
    assert command["training_data_uploaded"] is False
    assert command["max_cost_usd"] == 0
    assert command["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 45
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_model_api_called" for item in fixtures)
    assert any(item["name"] == "negative_provider_key_boundary" for item in fixtures)

    schema = {
        "properties": {
            "command_type": {"enum": ["deny_noop", "report_only_apply_command_contract"]},
            "target_route_id": {"const": TARGET_ROUTE_ID},
            "target_egress_type": {"const": TARGET_EGRESS_TYPE},
            "model_api_call_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }
    sources = source_summary()
    accepted = validate_command(command, schema, sources)
    assert accepted["accepted_for_contract_only"] is True
    assert accepted["errors"] == []

    negative = base_command("model-api-apply-command-negative-live-call")
    negative["model_api_calls"] = True
    rejected = validate_command(negative, schema, sources)
    assert rejected["accepted_for_contract_only"] is False
    assert "model_api_calls_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_command_allowed"] is False
    assert validation["model_api_call_allowed"] is False
    assert validation["model_api_calls"] is False
    assert validation["external_side_effects"] is False