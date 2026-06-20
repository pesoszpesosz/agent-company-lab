import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from browser_read_only_worker_policy_core import (  # noqa: E402
    NEXT_ACTION,
    POSITIVE_REQUEST_ID,
    READ_ONLY_ACTIONS,
    REQUEST_TYPE,
    SCHEMA_PATH,
    SERVICE_ID,
    TRACE_ID,
    ZERO_BOUNDARY,
    base_plan,
    build_report,
    fixture_set,
    load_json,
    request_index,
    validate_plan,
)


def test_browser_read_only_worker_policy_core_blocks_browser_and_external_actions() -> None:
    plan = base_plan("browser-read-only-policy-positive-boundary")

    assert plan["request_id"] == POSITIVE_REQUEST_ID
    assert plan["service_id"] == SERVICE_ID == "browser_read_only_session"
    assert plan["request_type"] == REQUEST_TYPE == "browser_research"
    assert plan["session_mode"] == "public_read_only_no_login"
    assert plan["navigation_scope"] == "explicit_allowlist_only"
    assert plan["allowed_domains"] == ["github.com"]
    assert plan["allowed_actions"] == READ_ONLY_ACTIONS
    assert plan["browser_session_start_allowed"] is False
    assert plan["worker_start_allowed"] is False
    assert plan["trace_id"] == TRACE_ID
    assert plan["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 29
    assert fixtures[0]["expected"] == "accepted"
    assert any(item["name"] == "negative_login_allowed" for item in fixtures)
    assert any(item["name"] == "negative_browser_started" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    requests = request_index()
    accepted = validate_plan(plan, schema, requests)
    assert accepted["accepted_for_browser_read_only_policy"] is True
    assert accepted["errors"] == []
    assert accepted["policy_verdict"] == "public_read_only_plan_valid_start_blocked"
    assert accepted["browser_session_start_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(plan)
    negative["allowed_actions"].append("login")
    rejected = validate_plan(negative, schema, requests)
    assert rejected["accepted_for_browser_read_only_policy"] is False
    assert "allowed_actions_include_prohibited_login" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["next_action"] == NEXT_ACTION
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["browser_session_start_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["external_side_effects"] is False
