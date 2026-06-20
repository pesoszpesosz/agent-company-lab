import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from durable_runtime_adapter_matrix_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_SCHEMA,
    REQUIRED_RUNTIMES,
    ZERO_ACTION_FIELDS,
    build_result,
    load_json,
    validate_row,
    zero_action_failures,
)


def test_durable_runtime_adapter_matrix_core_keeps_runtime_actions_static() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    seen: set[str] = set()
    sqlite_row = next(row for row in fixture["matrix"] if row["runtime_id"] == "sqlite_control_plane")
    temporal_row = next(row for row in fixture["matrix"] if row["runtime_id"] == "temporal_python")

    assert zero_action_failures(fixture["artifact_actions"], "artifact_actions") == []
    assert validate_row(sqlite_row, seen) == []
    assert validate_row(temporal_row, seen) == []

    negative = copy.deepcopy(temporal_row)
    negative["safe_now"] = True
    negative["promotion_decision"] = "adopt_now"
    errors = validate_row(negative, set())

    assert "non-sqlite runtime must not be safe_now" in errors
    assert "non-sqlite runtime cannot be adopted now" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
    )

    assert result["schema_version"] == (
        "agent_company.durable_runtime_adapter_matrix_validation.v2"
    )
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["artifact_actions"] == ZERO_ACTION_FIELDS
    assert result["rows_checked"] == len(fixture["matrix"])
    assert result["passed_count"] == len(fixture["matrix"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert result["required_runtimes_present"] is True
    assert {row["runtime_id"] for row in result["rows"]} == REQUIRED_RUNTIMES
