import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from browser_read_only_assignment_preflight_core import (  # noqa: E402
    ADAPTER_CONTRACT_VALIDATION,
    NEXT_ACTION,
    POLICY_VALIDATION,
    REQUEST_TYPE,
    SCHEMA_PATH,
    SERVICE_ID,
    TRACE_ID,
    ZERO_BOUNDARY,
    browser_requests,
    build_report,
    classify_request,
    load_json,
)


def test_browser_read_only_assignment_preflight_core_blocks_assignment_without_signed_approval() -> None:
    requests = browser_requests()
    assert len(requests) >= 7

    row = requests[0]
    result = classify_request(
        row,
        policy_ok=True,
        adapter_contract_ok=True,
        operator_signed_approval_present=False,
    )
    assert result["request_id"] == row["request_id"]
    assert result["packet_complete"] is True
    assert result["assignment_allowed"] is False
    assert result["blocked_reason"] == "no_signed_operator_approval"
    assert result["errors"] == []

    assigned = copy.deepcopy(row)
    assigned["assigned_agent_id"] = "agent-browser"
    rejected = classify_request(
        assigned,
        policy_ok=True,
        adapter_contract_ok=True,
        operator_signed_approval_present=False,
    )
    assert rejected["packet_complete"] is False
    assert "request_must_not_already_be_assigned" in rejected["errors"]
    assert rejected["assignment_allowed"] is False

    schema = load_json(SCHEMA_PATH)
    report, validation = build_report(schema)
    assert report["trace_id"] == TRACE_ID
    assert report["service_id"] == SERVICE_ID == "browser_read_only_session"
    assert report["request_type"] == REQUEST_TYPE == "browser_research"
    assert report["policy_validation"]["path"] == str(POLICY_VALIDATION)
    assert report["adapter_contract_validation"]["path"] == str(ADAPTER_CONTRACT_VALIDATION)
    assert report["next_action"] == NEXT_ACTION
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["preflight_verdict"] == "candidates_valid_assignment_blocked_no_signed_approval"
    assert validation["candidate_request_count"] == len(report["candidate_requests"])
    assert validation["assignment_allowed_count"] == 0
    assert validation["blocked_no_signed_approval_count"] == validation["candidate_request_count"]
    assert validation["operator_signed_approval_present"] is False
    assert validation["adapter_contract_gate"] == "present_valid_start_blocked"
    assert validation["service_requests_assigned"] == 0
    assert validation["service_requests_mutated"] == 0
    assert validation["browser_sessions_started"] == 0
    assert validation["worker_starts"] == 0
    assert validation["external_side_effects"] is False
