import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from durable_runtime_comparison_decision_packet_core import (  # noqa: E402
    DEFAULT_PACKET,
    DEFAULT_SCHEMA,
    REQUIRED_RUNTIME_IDS,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    source_validation_ok,
)


def test_durable_runtime_comparison_core_blocks_non_sqlite_promotion() -> None:
    packet = load_json(DEFAULT_PACKET)
    first_source = Path(packet["source_validation_paths"][0])

    assert source_validation_ok(first_source) == (True, "ok")

    result = build_result(
        packet,
        packet_path=DEFAULT_PACKET,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
    )

    assert result["schema_version"] == (
        "agent_company.durable_runtime_comparison_decision_packet_validation.v1"
    )
    assert result["packet_path"] == str(DEFAULT_PACKET)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["runtime_recommendations_checked"] == len(packet["runtime_recommendations"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert {row["runtime_id"] for row in packet["runtime_recommendations"]} == REQUIRED_RUNTIME_IDS

    negative = copy.deepcopy(packet)
    temporal = next(
        row for row in negative["runtime_recommendations"] if row["runtime_id"] == "temporal_python"
    )
    temporal["decision"] = "promote_now_local_only"
    temporal["required_gates_before_execution"] = []

    negative_result = build_result(
        negative,
        packet_path=DEFAULT_PACKET,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
    )

    assert negative_result["failed_count"] == 1
    assert "temporal_python must have approval gates before execution" in negative_result["top_level_failures"]
    assert "temporal_python cannot be promoted for execution now" in negative_result["top_level_failures"]
