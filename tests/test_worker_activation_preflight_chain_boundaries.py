import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from worker_activation_preflight_chain_core import (  # noqa: E402
    NEXT_ACTION,
    WORKER_POOL_ID,
    ZERO_BOUNDARY,
    base_chain,
    build_report,
    validate_chain,
)


def passing_composed_validators() -> dict[str, dict[str, object]]:
    return {
        "identity": {"exists": True, "all_checks_passed": True, "accepted_count": 1},
        "egress": {"exists": True, "all_checks_passed": True, "accepted_count": 1},
        "mcp_registry": {"exists": True, "all_checks_passed": True, "accepted_count": 1},
    }


def test_worker_activation_preflight_chain_core_builds_from_inline_fixtures() -> None:
    schema = {"properties": {"chain_verdict": {"enum": ["blocked_missing_validator"]}}}
    composed = passing_composed_validators()
    accepted_entry = base_chain("chain-boundary-positive")
    rejected_entry = copy.deepcopy(accepted_entry)
    rejected_entry["chain_id"] = "chain-boundary-negative-registration"
    rejected_entry["registration_allowed"] = True

    accepted = validate_chain(accepted_entry, schema, composed)
    assert accepted["accepted_for_activation_preflight"] is True
    assert accepted["errors"] == []
    assert accepted["registration_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    rejected = validate_chain(rejected_entry, schema, composed)
    assert rejected["accepted_for_activation_preflight"] is False
    assert "registration_allowed_must_be_false" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = [
        {"name": "positive_inline_chain", "expected": "accepted", "entry": accepted_entry},
        {"name": "negative_registration_allowed", "expected": "rejected", "entry": rejected_entry},
    ]
    report, validation = build_report(schema, fixtures, composed=composed)

    assert report["next_action"] == NEXT_ACTION
    assert report["worker_pool_id"] == WORKER_POOL_ID
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert report["all_checks_passed"] is True
    assert validation["all_checks_passed"] is True
    assert validation["failure_count"] == 0
    assert validation["fixture_count"] == 2
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == 1
    assert validation["registration_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["mcp_tool_call_allowed"] is False
    assert validation["external_side_effects"] is False
