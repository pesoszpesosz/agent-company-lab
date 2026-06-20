import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from browser_worker_adapter_contract_core import (  # noqa: E402
    POSITIVE_REQUEST_ID,
    TRACE_ID,
    ZERO_BOUNDARY,
    base_contract,
    build_report,
    build_trace_metadata,
    fixture_set,
    request_index,
    validate_contract,
)


def test_browser_worker_adapter_core_accepts_read_only_contract_without_runtime_start() -> None:
    contract = base_contract("browser-worker-adapter-contract-positive-boundary")

    assert contract["request_id"] == POSITIVE_REQUEST_ID
    assert contract["adapter_kind"] == "playwright_deterministic"
    assert contract["runtime_candidate"] == "microsoft/playwright"
    assert contract["execution_mode"] == "report_only_contract"
    assert contract["session_mode"] == "public_read_only_no_login"
    assert contract["browser_session_start_allowed"] is False
    assert contract["worker_start_allowed"] is False
    assert contract["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 19
    assert fixtures[0]["expected"] == "accepted"
    assert any(item["name"] == "negative_browser_started" for item in fixtures)
    assert any(item["name"] == "negative_worker_started" for item in fixtures)
    assert any(item["name"] == "negative_allowed_login" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = {"properties": {"adapter_kind": {"enum": ["playwright_deterministic", "stagehand_agent_sdk"]}}}
    requests = request_index()
    accepted = validate_contract(contract, schema, requests)
    assert accepted["accepted_for_adapter_contract"] is True
    assert accepted["contract_verdict"] == "adapter_contract_valid_start_blocked"
    assert accepted["browser_session_start_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = base_contract("browser-worker-adapter-contract-negative-boundary-browser-start")
    negative["runtime_boundary"]["browser_sessions_started"] = 1
    rejected = validate_contract(negative, schema, requests)
    assert rejected["accepted_for_adapter_contract"] is False
    assert "runtime_boundary_browser_sessions_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    trace_metadata = build_trace_metadata(validation)
    assert report["positive_fixture"]["adapter_kind"] == "playwright_deterministic"
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["browser_session_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["browser_sessions_started"] == 0
    assert validation["workers_started"] == 0
    assert validation["mcp_servers_started"] == 0
    assert validation["service_requests_assigned"] == 0
    assert validation["service_requests_mutated"] == 0
    assert validation["external_side_effects"] is False
    assert trace_metadata["trace_id"] == TRACE_ID
    assert trace_metadata["browser_actions"] is False
    assert trace_metadata["external_side_effects"] is False