import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from runtime_process_egress_signed_decision_guard_core import (  # noqa: E402
    EGRESS_VALIDATION,
    INTAKE_VALIDATION,
    NEXT_ACTION,
    RUNTIME_GUARD_VALIDATION,
    RUNTIME_PREFLIGHT_VALIDATION,
    TARGET_EGRESS_TYPE,
    TARGET_ROUTE_ID,
    ZERO_BOUNDARY,
    base_decision,
    build_report,
    fixture_set,
    load_json,
    route_summary,
    validate_decision,
)


def test_runtime_process_signed_decision_guard_core_accepts_only_report_only_preflight() -> None:
    decision = base_decision("runtime-process-egress-guard-positive-preflight-only")
    route = route_summary()["route"]
    schema = {
        "properties": {
            "decision": {"enum": ["deny", "approve_route_preflight_only"]},
            "route_id": {"const": TARGET_ROUTE_ID},
            "egress_type": {"const": TARGET_EGRESS_TYPE},
            "runtime_start_allowed": {"const": False},
            "live_egress_allowed": {"const": False},
        }
    }

    assert decision["route_id"] == TARGET_ROUTE_ID == "runtime_process_gateway"
    assert decision["egress_type"] == TARGET_EGRESS_TYPE == "runtime_start"
    assert decision["runtime_start_allowed"] is False
    assert decision["runtime_starts"] == 0
    assert decision["worker_start_allowed"] is False
    assert decision["worker_starts"] == 0
    assert decision["dependency_installs"] == 0
    assert decision["queue_mutations"] == 0
    assert decision["mcp_tool_calls"] is False
    assert decision["model_api_calls"] is False
    assert decision["runtime_boundary"] == ZERO_BOUNDARY

    intake_validation = load_json(INTAKE_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    runtime_preflight_validation = load_json(RUNTIME_PREFLIGHT_VALIDATION)
    runtime_guard_validation = load_json(RUNTIME_GUARD_VALIDATION)
    accepted = validate_decision(
        decision,
        schema,
        route,
        intake_validation,
        egress_validation,
        runtime_preflight_validation,
        runtime_guard_validation,
    )
    assert accepted["accepted_for_apply_preflight"] is True
    assert accepted["errors"] == []

    negative = base_decision("runtime-process-egress-guard-negative-runtime-start")
    negative["runtime_starts"] = 1
    rejected = validate_decision(
        negative,
        schema,
        route,
        intake_validation,
        egress_validation,
        runtime_preflight_validation,
        runtime_guard_validation,
    )
    assert rejected["accepted_for_apply_preflight"] is False
    assert "runtime_starts_must_be_zero" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 40
    assert [item["expected"] for item in fixtures[:2]] == ["accepted", "accepted"]
    assert any(item["name"] == "negative_runtime_started" for item in fixtures)
    assert any(item["name"] == "negative_boundary_dependency_install" for item in fixtures)

    report, validation = build_report(schema, fixtures)
    assert report["target_route_id"] == TARGET_ROUTE_ID
    assert report["target_egress_type"] == TARGET_EGRESS_TYPE
    assert set(report["target_route_required_gates"]) == {
        "runtime_start_preflight_v1",
        "runtime_start_signed_decision_guard_v1",
        "runtime_start_apply_preflight_blocker_v1",
        "runtime_dependency_install_preflight_v1",
        "agent_egress_event_ledger_v1",
    }
    assert report["next_action"] == NEXT_ACTION
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 2
    assert validation["rejected_count"] == validation["fixture_count"] - 2
    assert validation["runtime_start_allowed"] is False
    assert validation["runtime_starts"] == 0
    assert validation["dependency_installs"] == 0
    assert validation["external_side_effects"] is False