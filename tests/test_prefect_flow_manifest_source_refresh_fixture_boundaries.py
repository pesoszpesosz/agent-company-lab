import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from prefect_flow_manifest_source_refresh_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_SCHEMA,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    source_lanes_from_scheduler,
    source_modes_from_scheduler,
    validate_case,
)


def test_prefect_flow_manifest_source_refresh_core_validates_without_prefect_runtime() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    scheduler = load_json(Path(fixture["source_freshness_scheduler_plan_path"]))
    source_modes = source_modes_from_scheduler(scheduler)
    source_lanes = source_lanes_from_scheduler(scheduler)
    case = fixture["flow_cases"][0]

    assert validate_case(case, fixture, source_modes, source_lanes) == []

    negative = copy.deepcopy(case)
    negative["prefect_edges"]["flow_run_requested"] = True
    errors = validate_case(negative, fixture, source_modes, source_lanes)
    assert "prefect_runtime_edge:flow_run_requested" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
        scheduler_doc=scheduler,
        pydantic_doc={
            "next_local_test": "prefect_flow_manifest_for_local_source_refresh_without_runtime_start",
            "failed_count": 0,
        },
    )

    assert result["schema_version"] == "agent_company.prefect_flow_manifest_source_refresh_fixture_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["cases_checked"] == len(fixture["flow_cases"])
    assert result["passed_count"] == len(fixture["flow_cases"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert all(row["matches_expected"] for row in result["rows"])
