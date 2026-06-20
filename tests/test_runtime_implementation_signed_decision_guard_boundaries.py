import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from runtime_implementation_signed_decision_guard_core import (  # noqa: E402
    APPROVAL_ATTESTATION,
    APPROVAL_PACKET,
    NEXT_ACTION,
    ZERO_BOUNDARY,
    base_decision,
    build_guard_report,
    fixture_set,
    load_json,
    question_ids,
    validate_decision,
)


def test_runtime_implementation_signed_decision_guard_core_blocks_runtime_work() -> None:
    packet = load_json(APPROVAL_PACKET)
    decision = base_decision(
        packet,
        "runtime-implementation-signed-decision-positive-boundary",
        "approve_one_runtime_candidate",
    )

    assert decision["source_approval_packet_path"] == str(APPROVAL_PACKET)
    assert decision["decision"] == "approve_one_runtime_candidate"
    assert decision["selected_runtime_id"] == "sqlite_control_plane"
    assert decision["approved_question_ids"] == ["approve_runtime_candidate"]
    assert decision["allowed_dependency_names"] == []
    assert decision["allowed_runtime_processes"] == []
    assert decision["allowed_database_or_cloud_resources"] == []
    assert decision["service_request_mutation_scope"] == "none"
    assert decision["provider_model_and_cost_cap"] == "none"
    assert decision["signature_attestation"] == APPROVAL_ATTESTATION

    fixtures = fixture_set(packet)
    assert len(fixtures) >= 19
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_browser_public_action_approved" for item in fixtures)
    assert any(item["name"] == "negative_wallet_real_money_approved" for item in fixtures)
    assert any(item["name"] == "negative_security_testing_approved" for item in fixtures)

    accepted = validate_decision(decision, packet)
    assert accepted["accepted_for_later_preflight"] is True
    assert accepted["errors"] == []
    assert accepted["apply_allowed"] is False
    assert accepted["runtime_implementation_allowed"] is False
    assert accepted["runtime_code_write_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(decision)
    negative["approved_question_ids"] = [
        "approve_runtime_candidate",
        "approve_browser_or_public_action_scope",
    ]
    negative["denied_question_ids"] = [
        item for item in question_ids(packet) if item not in set(negative["approved_question_ids"])
    ]
    rejected = validate_decision(negative, packet)
    assert rejected["accepted_for_later_preflight"] is False
    assert "browser_public_actions_forbidden_in_runtime_guard" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_guard_report(packet, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert report["guard_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["decisions_applied"] == 0
    assert validation["runtime_implementation_allowed"] is False
    assert validation["runtime_code_write_allowed"] is False
    assert validation["external_side_effects"] is False
