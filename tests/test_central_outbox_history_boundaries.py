import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from central_outbox_history_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    REQUIRED_PROHIBITIONS,
    build_result,
    load_json,
    validate_message,
)


def test_central_outbox_history_core_requires_review_prohibitions() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    message = fixture["messages"][0]

    assert validate_message(message) == []
    assert REQUIRED_PROHIBITIONS <= set(message["prohibited_actions"])

    negative = copy.deepcopy(message)
    negative["approval_posture"] = "needs_human_review"
    negative["service_request_id"] = ""
    negative["prohibited_actions"] = sorted(REQUIRED_PROHIBITIONS)
    errors = validate_message(negative)

    assert "non-local-only messages must prohibit service_request_mutation" in errors
    assert "review-gated message should reference a service_request_id" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=DEFAULT_JSON_OUT,
        markdown_path=DEFAULT_MD_OUT,
    )

    assert result["schema_version"] == "agent_company.central_outbox_history_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["messages_checked"] == len(fixture["messages"])
    assert result["passed_count"] == len(fixture["messages"])
    assert result["failed_count"] == 0
    assert result["external_side_effects"] is False
