import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from checkpoint_interrupt_bridge_fixture_core import (  # noqa: E402
    CHECKPOINT_VALIDATION,
    RECOMMENDED_NEXT_ACTION,
    SCHEMA_PATH,
    SCORECARD_VALIDATION,
    ZERO_BOUNDARY,
    base_bridge,
    build_report,
    fixture_set,
    load_json,
    top_candidate_is_langgraph,
    validate_bridge,
    validation_ready,
)


def test_checkpoint_interrupt_bridge_fixture_core_stays_local_only() -> None:
    bridge = base_bridge("checkpoint-bridge-boundary")

    assert bridge["source_candidate"] == "langchain-ai/langgraph"
    assert bridge["source_candidate_rank"] == 1
    assert bridge["bridge_mode"] == "local_fixture_only"
    assert bridge["local_adapter_kind"] == "checkpoint_interrupt_bridge_fixture"
    assert bridge["checkpoint_contract_validation_path"] == str(CHECKPOINT_VALIDATION)
    assert bridge["scorecard_validation_path"] == str(SCORECARD_VALIDATION)
    assert bridge["maps_to_checkpoint_interrupt_contract"] is True
    assert bridge["runtime_adoption_allowed"] is False
    assert bridge["dependency_install_allowed"] is False
    assert bridge["dependency_import_allowed"] is False
    assert bridge["resume_allowed"] is False
    assert bridge["apply_allowed"] is False
    assert bridge["worker_start_allowed"] is False
    assert bridge["runtime_boundary"] == ZERO_BOUNDARY
    assert validation_ready(CHECKPOINT_VALIDATION) is True
    assert validation_ready(SCORECARD_VALIDATION) is True
    assert top_candidate_is_langgraph() is True

    fixtures = fixture_set()
    assert fixtures[0]["expected"] == "accepted"
    assert len(fixtures) >= 20
    assert any(item["name"] == "negative_external_framework_import" for item in fixtures)
    assert any(item["name"] == "negative_checkpoint_resumed" for item in fixtures)
    assert any(item["name"] == "negative_external_side_effect" for item in fixtures)

    schema = load_json(SCHEMA_PATH)
    accepted = validate_bridge(bridge, schema)
    assert accepted["accepted_for_local_bridge_fixture"] is True
    assert accepted["errors"] == []
    assert accepted["runtime_boundary"] == ZERO_BOUNDARY

    negative = copy.deepcopy(bridge)
    negative["runtime_boundary"]["external_framework_imports"] = 1
    rejected = validate_bridge(negative, schema)
    assert rejected["accepted_for_local_bridge_fixture"] is False
    assert "runtime_boundary_external_framework_imports_must_equal_0" in rejected["errors"]
    assert rejected["runtime_boundary"] == ZERO_BOUNDARY

    report, validation = build_report(schema, fixtures)
    assert report["recommended_next_action"] == RECOMMENDED_NEXT_ACTION
    assert report["source_state"]["scorecard_top_candidate_langgraph"] is True
    assert report["runtime_boundary"] == ZERO_BOUNDARY
    assert validation["all_checks_passed"] is True
    assert validation["accepted_count"] == 1
    assert validation["rejected_count"] == validation["fixture_count"] - 1
    assert validation["runtime_adoption_allowed"] is False
    assert validation["dependency_installs"] == 0
    assert validation["external_framework_imports"] == 0
    assert validation["external_side_effects"] is False
