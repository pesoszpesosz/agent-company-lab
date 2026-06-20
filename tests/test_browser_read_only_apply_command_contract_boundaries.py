import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from browser_read_only_apply_command_contract_core import (  # noqa: E402
    ADAPTER_CONTRACT_VALIDATION,
    APPLY_PREFLIGHT_VALIDATION,
    GUARD_VALIDATION,
    NEXT_ACTION,
    SCHEMA_PATH,
    ZERO_BOUNDARY,
    base_command,
    build_report,
    fixture_set,
    load_json,
    source_summary,
    validate_command,
)


def test_browser_read_only_apply_command_contract_core_blocks_runtime_apply() -> None:
    command = base_command("browser-read-only-apply-command-positive-boundary")

    assert command["source_apply_preflight_blocker_path"] == str(APPLY_PREFLIGHT_VALIDATION)
    assert command["source_guard_validation_path"] == str(GUARD_VALIDATION)
    assert command["source_adapter_contract_validation_path"] == str(ADAPTER_CONTRACT_VALIDATION)
    assert command["expected_source_apply_preflight_status"] == "blocked_no_real_signed_decision"
    assert command["real_signed_decision_present"] is False
    assert command["real_signed_decision_path"] == ""
    assert command["target_request_ids"] == []
    assert command["apply_command_allowed"] is False
    assert command["apply_allowed"] is False
    assert command["assignment_allowed"] is False
    assert command["browser_session_start_allowed"] is False
    assert command["worker_start_allowed"] is False
    assert command["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 29
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_browser_started" for item in fixtures)
    assert any(item["name"] == "negative_service_request_assigned" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    sources = source_summary()
    accepted = validate_command(command, schema, sources)
    assert accepted["accepted_for_contract_only"] is True
    assert accepted["errors"] == []

    negative = copy.deepcopy(command)
    negative["runtime_boundary"]["browser_sessions_started"] = 1
    rejected = validate_command(negative, schema, sources)
    assert rejected["accepted_for_contract_only"] is False
    assert "runtime_boundary_browser_sessions_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["apply_command_allowed"] is False
    assert validation["assignment_allowed"] is False
    assert validation["browser_session_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["external_side_effects"] is False
