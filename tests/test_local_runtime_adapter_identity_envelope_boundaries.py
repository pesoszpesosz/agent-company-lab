import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from local_runtime_adapter_pool_identity_envelope_core import (  # noqa: E402
    POOL_ID,
    RUNTIME_MODE,
    ZERO_BOUNDARY,
    base_envelope,
    build_report,
    fixture_set,
    validate_envelope,
)


def test_identity_envelope_core_blocks_runtime_registration_and_external_effects() -> None:
    envelope = base_envelope("identity-positive-boundary")

    assert envelope["worker_pool_id"] == POOL_ID == "service-worker-local-runtime-adapter-pool"
    assert envelope["allowed_runtime_modes"] == [RUNTIME_MODE]
    assert envelope["allowed_egress_types"] == []
    assert envelope["allowed_targets"] == []
    assert envelope["allowed_mcp_servers"] == []
    assert envelope["allowed_mcp_tools"] == []
    assert envelope["credential_policy"] == "deny"
    assert envelope["browser_session_policy"] == "deny"
    assert envelope["network_policy"] == "deny"
    assert envelope["runtime_boundary"] == ZERO_BOUNDARY

    fixtures = fixture_set()
    assert len(fixtures) >= 21
    assert fixtures[0]["expected"] == "accepted"
    assert any(item["name"] == "negative_external_side_effects_true" for item in fixtures)
    assert any(item["name"] == "negative_service_request_assignment_nonzero" for item in fixtures)
    assert any(item["name"] == "negative_worker_start_nonzero" for item in fixtures)

    schema = {"properties": {"worker_pool_id": {"const": POOL_ID}}}
    accepted = validate_envelope(envelope, schema)
    assert accepted["accepted_for_registration_candidate_preflight"] is True
    assert accepted["registration_allowed"] is False
    assert accepted["assignment_allowed"] is False
    assert accepted["worker_start_allowed"] is False
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = base_envelope("identity-negative-boundary-worker-start")
    negative["runtime_boundary"]["worker_starts"] = 1
    rejected = validate_envelope(negative, schema)
    assert rejected["accepted_for_registration_candidate_preflight"] is False
    assert "runtime_boundary_worker_starts_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["positive_fixture"]["expected_result"] == "pass_identity_candidate_not_registration_approval"
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["registration_allowed"] is False
    assert validation["assignment_allowed"] is False
    assert validation["worker_start_allowed"] is False
    assert validation["identity_system_installed"] is False
    assert validation["credentials_created"] is False
    assert validation["worker_pools_registered"] == 0
    assert validation["service_requests_assigned"] == 0
    assert validation["worker_starts"] == 0
    assert validation["model_api_calls"] is False
    assert validation["mcp_tool_calls"] is False
    assert validation["external_side_effects"] is False