import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from lane_manager_checkpoint_handoff_core import (  # noqa: E402
    NEXT_ACTION,
    ZERO_BOUNDARY,
    base_handoff,
    build_report,
    validate_handoff,
)


def test_lane_manager_checkpoint_handoff_core_builds_from_in_memory_lanes() -> None:
    schema = {"properties": {"handoff_allowed": {"const": False}}}
    lanes = [
        {
            "lane_id": "security_triage",
            "department": "Security",
            "owner_agent_id": "security-manager",
            "status": "active",
        },
        {
            "lane_id": "submitted_bounty_payouts",
            "department": "Revenue Collection",
            "owner_agent_id": "payout-manager",
            "status": "active",
        },
    ]
    accepted_handoff = base_handoff(lanes[0])
    rejected_handoff = copy.deepcopy(accepted_handoff)
    rejected_handoff["worker_start_allowed"] = True

    lane_map = {row["lane_id"]: row for row in lanes}
    assert validate_handoff(accepted_handoff, schema, lane_map) == []
    rejected_errors = validate_handoff(rejected_handoff, schema, lane_map)
    assert "worker_start_allowed_must_be_false" in rejected_errors

    fixtures = [
        {
            "name": "positive_security_triage_handoff",
            "expected": "accepted",
            "handoffs": [accepted_handoff],
        },
        {
            "name": "negative_worker_start_allowed",
            "expected": "rejected",
            "handoffs": [rejected_handoff],
        },
    ]

    report, validation = build_report(schema, fixtures, lanes=lanes)

    assert report["next_action"] == NEXT_ACTION
    assert report["expected_lane_ids"] == ["security_triage"]
    assert report["excluded_lanes"] == ["submitted_bounty_payouts"]
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert report["all_checks_passed"] is True
    assert validation["all_checks_passed"] is True
    assert validation["failure_count"] == 0
    assert validation["fixture_count"] == 2
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == 1
    assert validation["handoff_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["service_request_mutation_allowed"] is False
    assert validation["external_side_effects"] is False
