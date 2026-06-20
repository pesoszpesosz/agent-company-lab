import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from runtime_start_signed_decision_guard_core import (  # noqa: E402
    ATTESTATION,
    NEXT_ACTION,
    PREFLIGHT_VALIDATION,
    SCHEMA_PATH,
    WORKER_POOL_ID,
    ZERO_BOUNDARY,
    base_decision,
    build_report,
    command_preview_hash,
    fixture_set,
    load_json,
    preflight_summary,
    validate_decision,
)


def test_runtime_start_signed_decision_guard_core_blocks_runtime_starts() -> None:
    decision = base_decision("runtime-start-decision-positive-boundary")

    assert decision["worker_pool_id"] == WORKER_POOL_ID
    assert decision["source_runtime_start_preflight_path"] == str(PREFLIGHT_VALIDATION)
    assert decision["decision"] == "approve_runtime_start_preflight_only"
    assert decision["operator_attestation"] == ATTESTATION
    assert decision["allowed_scope"] == "runtime_start_preflight_only"
    assert decision["allowed_command_preview_sha256"] == command_preview_hash()
    assert decision["allowed_output_artifact_path"].endswith("runtime-start-preflight-v1-20260617.json")
    assert decision["allowed_trace_id"] == "trace-runtime-start-preflight-v1-20260617"
    assert decision["runtime_start_allowed"] is False
    assert decision["worker_start_allowed"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 19
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_runtime_start_allowed" for item in fixtures)
    assert any(item["name"] == "negative_runtime_process_started" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    preflight = preflight_summary()
    accepted = validate_decision(decision, schema, preflight)
    assert accepted["accepted_for_later_preflight"] is True
    assert accepted["errors"] == []
    assert accepted["runtime_start_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(decision)
    negative["runtime_boundary"]["runtime_processes_started"] = 1
    rejected = validate_decision(negative, schema, preflight)
    assert rejected["accepted_for_later_preflight"] is False
    assert "runtime_boundary_runtime_processes_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["runtime_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["external_side_effects"] is False
