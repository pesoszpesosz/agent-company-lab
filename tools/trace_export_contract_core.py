#!/usr/bin/env python3
"""Validate trace export contract fixtures without contacting observability backends."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = ROOT / "reports" / "trace-export-contract-v1-20260617.json"
DEFAULT_JSON_OUT = ROOT / "reports" / "trace-export-contract-validation-20260617.json"
DEFAULT_MD_OUT = ROOT / "reports" / "trace-export-contract-v1-20260617.md"
DEFAULT_JSONL_OUT = ROOT / "reports" / "trace-export-contract-preview-20260617.jsonl"
DEFAULT_SCHEMA = ROOT / "architecture" / "trace-export-contract-v1.schema.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        out: list[str] = []
        for key, child in value.items():
            out.append(str(key))
            out.extend(flatten_values(child))
        return out
    if isinstance(value, list):
        out = []
        for child in value:
            out.extend(flatten_values(child))
        return out
    return [str(value)]


def validate_span(span: dict[str, Any], deny_keys: set[str], deny_patterns: list[str]) -> list[str]:
    failures: list[str] = []
    if span.get("external_side_effects") is not False:
        failures.append("external_side_effects must be false")
    if span.get("api_calls") is not False:
        failures.append("api_calls must be false for this preview contract")
    if not span.get("span_id"):
        failures.append("span_id is required")
    if not span.get("summary_redacted") or len(span["summary_redacted"]) > 1000:
        failures.append("summary_redacted must be present and <= 1000 chars")
    attributes = span.get("attributes") or {}
    lower_keys = {str(key).lower() for key in attributes.keys()}
    blocked_keys = sorted(lower_keys & deny_keys)
    if blocked_keys:
        failures.append(f"blocked metadata keys present: {', '.join(blocked_keys)}")
    values = flatten_values(span)
    for value in values:
        for pattern in deny_patterns:
            if blocked_pattern_present(value, pattern):
                failures.append(f"blocked value pattern present: {pattern}")
    if span.get("artifact_ref") and "E:\\agent-company-lab\\" not in span["artifact_ref"]:
        failures.append("artifact_ref must stay inside E:\\agent-company-lab for v1 preview")
    return sorted(set(failures))


def blocked_pattern_present(value: str, pattern: str) -> bool:
    token_prefixes = {
        "sk-": r"(?i)(^|[^a-z0-9])sk-[a-z0-9]",
        "xox": r"(?i)(^|[^a-z0-9])xox[a-z0-9-]",
        "ghp_": r"(?i)(^|[^a-z0-9])ghp_[a-z0-9]",
        "gho_": r"(?i)(^|[^a-z0-9])gho_[a-z0-9]",
        "AIza": r"(?i)(^|[^a-z0-9])aiza[0-9a-z_-]",
    }
    if pattern in token_prefixes:
        return re.search(token_prefixes[pattern], value) is not None
    return pattern.lower() in value.lower()


def write_jsonl(spans: list[dict[str, Any]], path: Path) -> None:
    path.write_text("\n".join(json.dumps(span, sort_keys=True) for span in spans) + "\n", encoding="utf-8")




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
    jsonl_path: Path,
) -> dict[str, Any]:
    policy = fixture["redaction_policy"]
    deny_keys = {key.lower() for key in policy["deny_metadata_keys"]}
    deny_patterns = list(policy["deny_value_patterns"])
    rows = []
    seen: set[str] = set()
    for span in fixture["export_spans"]:
        failures = validate_span(span, deny_keys, deny_patterns)
        if span["event_id"] in seen:
            failures.append("duplicate event_id")
        seen.add(span["event_id"])
        rows.append(
            {
                "event_id": span["event_id"],
                "trace_id": span["trace_id"],
                "lane_id": span["lane_id"],
                "span_kind": span["span_kind"],
                "runtime": span["runtime"],
                "failures": sorted(set(failures)),
            }
        )
    failed_count = sum(1 for row in rows if row["failures"])
    return {
        "schema_version": "agent_company.trace_export_contract_validation.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "jsonl_preview_path": str(jsonl_path),
        "spans_checked": len(rows),
        "passed_count": len(rows) - failed_count,
        "failed_count": failed_count,
        "backend_calls": False,
        "external_side_effects": False,
        "rows": rows,
    }
