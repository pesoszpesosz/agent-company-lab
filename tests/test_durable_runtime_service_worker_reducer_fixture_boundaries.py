import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from durable_runtime_service_worker_reducer_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    REQUIRED_RUNTIMES,
    ZERO_ACTION_FLAGS,
    ZERO_PROFILE_FIELDS,
    build_result,
    check_zero_fields,
    load_json,
    status_output,
)


def test_durable_runtime_reducer_core_expands_runtime_status_matrix_without_side_effects() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    sqlite_profile = next(
        row for row in fixture["runtime_profiles"] if row["runtime_id"] == "sqlite_control_plane"
    )
    needs_review = next(
        row for row in fixture["service_status_cases"] if row["status_snapshot"] == "needs_review"
    )

    assert check_zero_fields(sqlite_profile, ZERO_PROFILE_FIELDS, "runtime_profiles[sqlite]") == []
    mutated_profile = copy.deepcopy(sqlite_profile)
    mutated_profile["runtime_starts"] = 1
    assert check_zero_fields(mutated_profile, ZERO_PROFILE_FIELDS, "runtime_profiles[sqlite]") == [
        "runtime_profiles[sqlite].runtime_starts must be 0; got 1"
    ]
    assert status_output(needs_review) == {
        "output_state": "parked.awaiting_human_review",
        "parked": True,
        "terminal": False,
        "resume_requirements": needs_review["resume_requirements"],
    }

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=DEFAULT_JSON_OUT,
        markdown_path=DEFAULT_MD_OUT,
    )

    assert result["schema_version"] == "agent_company.durable_runtime_service_worker_reducer_fixture_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_profile_count"] == len(REQUIRED_RUNTIMES)
    assert result["status_case_count"] == 3
    assert result["expanded_check_count"] == len(REQUIRED_RUNTIMES) * 3
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert result["required_runtimes_present"] is True
    assert result["required_statuses_present"] is True
    assert result["runtime_boundary"]["runtime_starts"] == 0
    assert result["runtime_boundary"]["external_side_effects"] is False
    assert all(
        row["action_flags"] == fixture["expected_action_flags"] == ZERO_ACTION_FLAGS
        for row in result["expanded_checks"]
    )
    assert all(not row["failures"] for row in result["expanded_checks"])
