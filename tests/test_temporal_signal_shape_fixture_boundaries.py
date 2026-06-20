import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from temporal_signal_shape_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    validate_case,
)


def test_temporal_signal_shape_core_validates_payloads_without_temporal_runtime() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    case = fixture["signal_cases"][0]

    assert validate_case(case, fixture) == []

    negative = copy.deepcopy(case)
    negative["payload"]["requested_disposition"] = "reply_publicly"
    errors = validate_case(negative, fixture)
    assert "requested_disposition_not_allowed" in errors
    assert "public_action_requires_separate_gate" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=DEFAULT_JSON_OUT,
        markdown_path=DEFAULT_MD_OUT,
        reducer_doc={
            "next_local_test": "temporal_signal_shape_fixture_against_service_worker_request_v1"
        },
    )

    assert result["schema_version"] == "agent_company.temporal_signal_shape_fixture_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["cases_checked"] == len(fixture["signal_cases"])
    assert result["passed_count"] == len(fixture["signal_cases"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert all(row["matches_expected"] for row in result["rows"])
