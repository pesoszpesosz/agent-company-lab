import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from inngest_event_flow_control_fixture_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_SCHEMA,
    ZERO_RUNTIME_BOUNDARY,
    build_result,
    load_json,
    validate_event,
)


def test_inngest_event_flow_control_core_rejects_event_drift() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    outbox = load_json(Path(fixture["source_outbox_path"]))
    messages = {row["message_id"]: row for row in outbox["messages"]}
    event = fixture["events"][0]

    assert validate_event(event, fixture, messages) == []

    negative = copy.deepcopy(event)
    negative["event_name"] = "agent_company/outbox.dispatch"
    negative["data"]["idempotency_key"] = "missing-message-context"
    errors = validate_event(negative, fixture, messages)

    assert "event_name_not_allowed_for_outbox_message_type" in errors
    assert "idempotency_key_missing_message_event_or_replay_status" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=Path("memory-validation.json"),
        markdown_path=Path("memory-validation.md"),
        outbox_doc=outbox,
        temporal_doc={
            "next_local_test": (
                "inngest_event_name_and_flow_control_fixture_against_central_outbox_history_v1"
            )
        },
    )

    assert result["schema_version"] == (
        "agent_company.inngest_event_flow_control_fixture_validation.v1"
    )
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["runtime_boundary"] == ZERO_RUNTIME_BOUNDARY
    assert result["events_checked"] == len(fixture["events"])
    assert result["passed_count"] == len(fixture["events"])
    assert result["failed_count"] == 0
    assert result["top_level_failures"] == []
    assert all(row["matches_expected"] for row in result["rows"])
