import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from trace_export_contract_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_JSONL_OUT,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    blocked_pattern_present,
    build_result,
    load_json,
    validate_span,
)


def test_trace_export_core_blocks_secret_patterns_and_external_refs() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    policy = fixture["redaction_policy"]
    deny_keys = {key.lower() for key in policy["deny_metadata_keys"]}
    deny_patterns = list(policy["deny_value_patterns"])
    span = fixture["export_spans"][0]

    assert blocked_pattern_present("prefix sk-test-secret", "sk-") is True
    assert validate_span(span, deny_keys, deny_patterns) == []

    negative = copy.deepcopy(span)
    negative["attributes"]["api_key"] = "sk-test-secret"
    negative["artifact_ref"] = r"C:\outside\trace.json"
    errors = validate_span(negative, deny_keys, deny_patterns)

    assert any("blocked metadata keys present" in error for error in errors)
    assert "blocked value pattern present: sk-" in errors
    assert r"artifact_ref must stay inside E:\agent-company-lab for v1 preview" in errors

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=DEFAULT_JSON_OUT,
        markdown_path=DEFAULT_MD_OUT,
        jsonl_path=DEFAULT_JSONL_OUT,
    )

    assert result["schema_version"] == "agent_company.trace_export_contract_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["jsonl_preview_path"] == str(DEFAULT_JSONL_OUT)
    assert result["spans_checked"] == len(fixture["export_spans"])
    assert result["passed_count"] == len(fixture["export_spans"])
    assert result["failed_count"] == 0
    assert result["backend_calls"] is False
    assert result["external_side_effects"] is False
