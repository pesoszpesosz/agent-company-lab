import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from browser_read_only_signed_approval_guard_core import (  # noqa: E402
    ASSIGNMENT_PREFLIGHT_VALIDATION,
    NEXT_ACTION,
    ZERO_BOUNDARY,
    assignment_preflight_summary,
    base_decision,
    build_report,
    fixture_set,
    load_json,
    validate_decision,
)


def test_browser_read_only_signed_approval_guard_core_accepts_preflight_only_decisions() -> None:
    decision = base_decision("browser-read-only-approval-positive-boundary")
    preflight = assignment_preflight_summary()
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_browser_read_only_assignment_preflight_only"]}
        }
    }

    assert decision["decision"] == "approve_browser_read_only_assignment_preflight_only"
    assert decision["source_assignment_preflight_path"] == str(ASSIGNMENT_PREFLIGHT_VALIDATION)
    assert decision["source_adapter_contract_validation_path"] == preflight["adapter_contract_validation_path"]
    assert decision["allowed_scope"] == "browser_read_only_assignment_preflight_only"
    assert set(decision["allowed_candidate_request_ids"]) == set(preflight["candidate_request_ids"])
    assert decision["assignment_allowed"] is False
    assert decision["browser_session_start_allowed"] is False
    assert decision["worker_start_allowed"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    accepted = validate_decision(decision, schema, preflight)
    assert accepted["accepted_for_later_preflight"] is True
    assert accepted["errors"] == []
    assert accepted["assignment_allowed"] is False
    assert accepted["browser_session_start_allowed"] is False

    negative = base_decision("browser-read-only-approval-negative-boundary-browser-start")
    negative["runtime_boundary"]["browser_sessions_started"] = 1
    rejected = validate_decision(negative, schema, preflight)
    assert rejected["accepted_for_later_preflight"] is False
    assert "runtime_boundary_browser_sessions_started_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    deny = base_decision("browser-read-only-approval-positive-boundary-deny", "deny")
    deny_result = validate_decision(deny, schema, preflight)
    assert deny["allowed_scope"] == "none"
    assert deny_result["accepted_for_later_preflight"] is True

    fixtures = fixture_set()
    assert len(fixtures) >= 20
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_missing_candidate_ids" for item in fixtures)
    assert any(item["name"] == "negative_browser_started" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["trace_id"].startswith("trace-browser-read-only-signed-approval-guard-v1")
    assert report["source_preflight"]["adapter_contract_gate"] == "present_valid_start_blocked"
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["assignment_allowed"] is False
    assert validation["browser_session_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["decisions_applied"] == 0
    assert validation["approval_rows_written"] == 0
    assert validation["browser_sessions_started"] == 0
    assert validation["external_side_effects"] is False
