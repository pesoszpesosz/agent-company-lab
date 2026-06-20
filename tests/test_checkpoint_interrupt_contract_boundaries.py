import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from checkpoint_interrupt_contract_core import (  # noqa: E402
    APPLY_PREFLIGHT_VALIDATION,
    DOCKET_VALIDATION,
    NEXT_ACTION,
    SCHEMA_PATH,
    WAVE15_VALIDATION,
    ZERO_BOUNDARY,
    base_checkpoint,
    build_report,
    fixture_set,
    load_json,
    validate_checkpoint,
    validation_ready,
)


def test_checkpoint_interrupt_contract_core_pauses_without_resume_or_apply() -> None:
    checkpoint = base_checkpoint(
        "checkpoint-boundary",
        "service_request",
        "security_bounty_private_reports",
        "service_worker_gate",
    )

    assert checkpoint["schema_version"] == "agent_company.checkpoint_interrupt_contract.v1"
    assert checkpoint["source_kind"] == "service_request"
    assert checkpoint["service_request_id"]
    assert checkpoint["manual_review_required"] is True
    assert checkpoint["resume_allowed"] is False
    assert checkpoint["apply_allowed"] is False
    assert checkpoint["worker_start_allowed"] is False
    assert checkpoint["required_artifacts"] == [
        str(WAVE15_VALIDATION),
        str(DOCKET_VALIDATION),
        str(APPLY_PREFLIGHT_VALIDATION),
    ]
    assert checkpoint["runtime_boundary"] == ZERO_BOUNDARY
    assert validation_ready(WAVE15_VALIDATION) is True
    assert validation_ready(DOCKET_VALIDATION) is True
    assert validation_ready(APPLY_PREFLIGHT_VALIDATION) is True

    fixtures = fixture_set()
    assert len(fixtures) >= 19
    assert [item["expected"] for item in fixtures[:3]] == ["accepted", "accepted", "accepted"]
    assert any(item["name"] == "negative_resume_allowed" for item in fixtures)
    assert any(item["name"] == "negative_resume_command_written" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    accepted = validate_checkpoint(checkpoint, schema)
    assert accepted["accepted_for_checkpoint_interrupt"] is True
    assert accepted["errors"] == []
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(checkpoint)
    negative["runtime_boundary"]["resume_commands_written"] = 1
    rejected = validate_checkpoint(negative, schema)
    assert rejected["accepted_for_checkpoint_interrupt"] is False
    assert "runtime_boundary_resume_commands_written_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert report["source_state"]["wave15_validation_ready"] is True
    assert report["source_state"]["operator_docket_validation_ready"] is True
    assert report["source_state"]["apply_preflight_validation_ready"] is True
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 3
    assert validation["rejected_count"] == validation["fixture_count"] - 3
    assert validation["resume_allowed"] is False
    assert validation["apply_allowed"] is False
    assert validation["external_side_effects"] is False
