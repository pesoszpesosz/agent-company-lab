import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from service_worker_signed_decision_guard_core import (  # noqa: E402
    ATTESTATION_SUFFIX,
    INTAKE_CONTRACT,
    INTAKE_VALIDATION,
    NEXT_ACTION,
    SCHEMA_PATH,
    ZERO_BOUNDARY,
    base_decision,
    build_report,
    fixture_set,
    load_json,
    validate_decision,
)


def test_service_worker_signed_decision_guard_core_blocks_apply_side_effects() -> None:
    decision = base_decision(
        "service-worker-signed-decision-positive-boundary",
        "browser_read_only_session",
        "approve_assignment_preflight_only",
    )

    assert decision["source_intake_contract_path"] == str(INTAKE_CONTRACT)
    assert decision["service_id"] == "browser_read_only_session"
    assert decision["decision"] == "approve_assignment_preflight_only"
    assert decision["allowed_scope"] == (
        "browser_read_only_session:approve_assignment_preflight_only:exact_scope"
    )
    assert decision["allowed_request_ids"]
    assert decision["exact_scope_required"] is True
    assert decision["approval_is_not_apply"] is True
    assert decision["apply_allowed"] is False
    assert ATTESTATION_SUFFIX in decision["operator_attestation"]
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 27
    assert [item["expected"] for item in fixtures[:3]] == ["accepted", "accepted", "accepted"]
    assert any(item["name"] == "negative_apply_allowed" for item in fixtures)
    assert any(item["name"] == "negative_worker_started" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    contract = load_json(INTAKE_CONTRACT)
    contract_validation = load_json(INTAKE_VALIDATION)
    accepted = validate_decision(decision, schema, contract, contract_validation)
    assert accepted["accepted_for_later_apply_preflight"] is True
    assert accepted["errors"] == []
    assert accepted["apply_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(decision)
    negative["runtime_boundary"]["worker_starts"] = 1
    rejected = validate_decision(negative, schema, contract, contract_validation)
    assert rejected["accepted_for_later_apply_preflight"] is False
    assert "runtime_boundary_worker_starts_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert report["guard_status"] == "report_only_signed_decision_guard_ready"
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 3
    assert validation["rejected_count"] == validation["fixture_count"] - 3
    assert validation["apply_allowed"] is False
    assert validation["worker_starts"] == 0
    assert validation["external_side_effects"] is False
