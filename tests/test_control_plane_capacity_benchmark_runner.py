import json
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.control_plane_capacity_benchmark_runner import (  # noqa: E402
    parse_row_counts,
    run_capacity_benchmark,
)


def test_parse_row_counts_accepts_comma_or_semicolon_lists() -> None:
    assert parse_row_counts("2, 5;10,5") == (2, 5, 10)


def test_capacity_benchmark_runner_writes_non_destructive_artifacts(tmp_path: Path) -> None:
    report_path = tmp_path / "capacity.md"
    json_path = tmp_path / "capacity.json"

    result = run_capacity_benchmark(
        Namespace(
            row_counts="2,5",
            run_id="pytest",
            work_dir=str(tmp_path),
            path=str(report_path),
            json_path=str(json_path),
            overwrite=True,
        )
    )

    written = json.loads(json_path.read_text(encoding="utf-8"))

    assert result["schema_version"] == "control_plane_capacity_benchmark_runner.v1"
    assert report_path.exists()
    assert Path(result["synthetic_db_path"]).exists()
    assert written["runtime_boundary"]["production_rows_inserted_by_benchmark"] == 0
    assert written["runtime_boundary"]["external_network_calls"] is False
    assert written["runtime_boundary"]["synthetic_data_only"] is True
    assert written["index_check"]["tasks"] == ["idx_tasks_duplicate_key", "idx_tasks_lane_created", "idx_tasks_status_priority_created"]
    assert written["scenarios"][-1]["row_count"] == 5
    assert written["scenarios"][-1]["table_counts"]["tasks"] == 5
    assert written["scenarios"][-1]["slowest_query"]["label"]
    assert written["scenarios"][-1]["query_timings"]
