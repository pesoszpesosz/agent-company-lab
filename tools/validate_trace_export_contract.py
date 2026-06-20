#!/usr/bin/env python3
"""Validate trace export contract fixtures without contacting observability backends."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trace_export_contract_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSONL_OUT,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
    write_jsonl,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Trace Export Contract v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Schema: `{result['schema_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Preview JSONL: `{result['jsonl_preview_path']}`",
        "",
        "## Summary",
        "",
        f"- Spans checked: `{result['spans_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Backend calls: `{str(result['backend_calls']).lower()}`",
        f"- External side effects: `{str(result['external_side_effects']).lower()}`",
        "",
        "## Export Rows",
        "",
        "| Event | Lane | Kind | Runtime | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if not row["failures"] else "fail"
        lines.append(
            f"| `{row['event_id']}` | `{row['lane_id']}` | `{row['span_kind']}` | `{row['runtime']}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Contract Decision",
            "",
            "This contract permits local JSONL preview exports only. Langfuse, Phoenix, "
            "OpenTelemetry, or any hosted collector remain future adapter targets and "
            "require a separate service/API/credential review before use.",
            "",
            "## Boundary",
            "",
            "- Observability backend calls: `false`",
            "- Model/API calls: `false`",
            "- Dependency installs/imports: `false`",
            "- Service requests updated: `0`",
            "- Worker starts: `0`",
            "- External side effects: `false`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")




def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    parser.add_argument("--jsonl-out", type=Path, default=DEFAULT_JSONL_OUT)
    args = parser.parse_args()

    fixture = load_json(args.fixture)
    result = build_result(
        fixture,
        fixture_path=args.fixture,
        schema_path=args.schema,
        json_path=args.json_out,
        markdown_path=args.md_out,
        jsonl_path=args.jsonl_out,
    )
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_jsonl(fixture["export_spans"], args.jsonl_out)
    write_markdown(result, args.md_out)
    print(
        json.dumps(
            {
                "ok": result["failed_count"] == 0,
                "failed_count": result["failed_count"],
                "json": str(args.json_out),
            },
            indent=2,
        )
    )
    return 0 if result["failed_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
