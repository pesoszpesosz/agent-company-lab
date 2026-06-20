import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from pydantic_durable_adapter_manifest_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_SCHEMA,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    validate_case,
)


def test_pydantic_durable_manifest_core_blocks_runtime_and_model_calls() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    case = fixture["manifest_cases"][0]

    assert validate_case(case, fixture) == []

    negative = copy.deepcopy(case)
    negative["allow_model_requests"] = True
    negative["durable_backend_imported"] = True
    negative["toolsets"][0]["registration"] = "dynamic"
    negative["toolsets"][0]["uses_get_toolset"] = True
    errors = validate_case(negative, fixture)

    assert "model_requests_not_blocked" in errors
    assert "durable_backend_imported" in errors
    assert "dynamic_toolset_with_get_toolset_not_supported" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
        dbos_doc={
            "next_local_test": (
                "pydantic_durable_adapter_manifest_fixture_without_model_api_calls"
            ),
            "failed_count": 0,
        },
    )

    assert result["schema_version"] == (
        "agent_company.pydantic_durable_adapter_manifest_fixture_validation.v1"
    )
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["cases_checked"] == len(fixture["manifest_cases"])
    assert result["passed_count"] == len(fixture["manifest_cases"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert all(row["matches_expected"] for row in result["rows"])
