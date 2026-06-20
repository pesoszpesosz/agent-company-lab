import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from restate_agent_service_boundary_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_SCHEMA,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    validate_case,
)


def test_restate_agent_service_boundary_core_rejects_runtime_edges() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    outbox = load_json(Path(fixture["source_outbox_history_path"]))
    messages = {row["message_id"]: row for row in outbox["messages"]}
    case = fixture["agent_service_cases"][0]

    assert validate_case(case, fixture, messages) == []

    negative = copy.deepcopy(case)
    negative["restate_edges"]["service_call_or_send"] = True
    negative["side_effects"]["external_side_effect"] = True
    errors = validate_case(negative, fixture, messages)

    assert "restate_runtime_edge:service_call_or_send" in errors
    assert "external_side_effect_requested" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
        prefect_doc={
            "next_local_test": (
                "restate_agent_service_boundary_fixture_against_central_outbox_history_v1"
            ),
            "failed_count": 0,
        },
        outbox_doc=outbox,
    )

    assert result["schema_version"] == (
        "agent_company.restate_agent_service_boundary_fixture_validation.v1"
    )
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["cases_checked"] == len(fixture["agent_service_cases"])
    assert result["passed_count"] == len(fixture["agent_service_cases"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert all(row["matches_expected"] for row in result["rows"])
