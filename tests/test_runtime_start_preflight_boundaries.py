import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from runtime_start_preflight_core import (  # noqa: E402
    ACTIVATION_CHAIN_VALIDATION,
    NEXT_ACTION,
    SCHEMA_PATH,
    TRACE_ID,
    WORKER_POOL_ID,
    ZERO_BOUNDARY,
    activation_chain_summary,
    base_preflight,
    build_report,
    fixture_set,
    load_json,
    validate_preflight,
)


def test_runtime_start_preflight_core_blocks_process_and_worker_starts() -> None:
    entry = base_preflight("runtime-start-preflight-positive-boundary")
    command = entry["command_preview"]

    assert entry["worker_pool_id"] == WORKER_POOL_ID
    assert entry["activation_chain_validation_path"] == str(ACTIVATION_CHAIN_VALIDATION)
    assert entry["operator_decision_status"] == "report_only_no_signed_start_authority"
    assert entry["runtime_start_verdict"] == "dry_run_preview_valid_start_blocked"
    assert entry["runtime_start_allowed"] is False
    assert entry["worker_start_allowed"] is False
    assert entry["trace_id"] == TRACE_ID
    assert entry["runtime_boundary"] == ZERO_BOUNDARY
    assert command["mode"] == "preview_only"
    assert command["command_kind"] == "local_python_report_only"
    assert "--dry-run" in command["command_string"]
    assert "--no-execute" in command["command_string"]
    assert command["execution_allowed"] is False

    fixtures = fixture_set()
    assert len(fixtures) >= 16
    assert fixtures[0]["expected"] == "accepted"
    assert any(item["name"] == "negative_runtime_process_started" for item in fixtures)
    assert any(item["name"] == "negative_command_preview_executed" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    activation_chain = activation_chain_summary()
    accepted = validate_preflight(entry, schema, activation_chain)
    assert accepted["accepted_for_runtime_start_preflight"] is True
    assert accepted["errors"] == []
    assert accepted["runtime_start_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(entry)
    negative["runtime_boundary"]["runtime_processes_started"] = 1
    rejected = validate_preflight(negative, schema, activation_chain)
    assert rejected["accepted_for_runtime_start_preflight"] is False
    assert "runtime_boundary_runtime_processes_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert report["activation_chain"]["chain_verdict"] == "preflight_passed_registration_blocked"
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["runtime_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["external_side_effects"] is False
