import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from dbos_workflow_step_boundary_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_SCHEMA,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    request_ids_from_queue,
    validate_case,
)


def test_dbos_workflow_step_boundary_core_validates_without_runtime_edges() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    queue_doc = load_json(Path(fixture["source_service_worker_queue_path"]))
    known_request_ids = request_ids_from_queue(queue_doc)
    case = fixture["cases"][0]

    assert validate_case(case, fixture, known_request_ids) == []

    negative = copy.deepcopy(case)
    negative["planned_steps"][0]["executes_now"] = True
    errors = validate_case(negative, fixture, known_request_ids)
    assert "planned_step_executes_now:validate_packet" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
        known_request_ids=known_request_ids,
        source_inngest_doc={
            "next_local_test": "dbos_workflow_step_boundary_fixture_for_service_worker_request_v1"
        },
    )

    assert result["schema_version"] == "agent_company.dbos_workflow_step_boundary_fixture_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["cases_checked"] == len(fixture["cases"])
    assert result["passed_count"] == len(fixture["cases"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert all(row["matches_expected"] for row in result["rows"])
