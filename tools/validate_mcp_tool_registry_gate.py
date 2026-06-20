#!/usr/bin/env python3
"""Validate MCP tool registry gate fixtures without starting MCP servers or tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from mcp_tool_registry_gate_core import (
    EGRESS_VALIDATION,
    FIXTURE_DIR,
    IDENTITY_VALIDATION,
    PACKET,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    build_report,
    fixture_set,
    load_json,
    sha256_path,
)


def write_fixtures() -> list[dict[str, Any]]:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for fixture in fixture_set():
        path = FIXTURE_DIR / f"{fixture['name']}.json"
        path.write_text(json.dumps(fixture["entry"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append({"name": fixture["name"], "expected": fixture["expected"], "path": str(path), "sha256": sha256_path(path)})
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# MCP Tool Registry Gate v1 Validation",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Source packet: `{PACKET}`",
        f"Schema: `{SCHEMA_PATH}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Fixture directory: `{FIXTURE_DIR}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Fixture count: `{validation['fixture_count']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- MCP server enable allowed: `{validation['mcp_server_enable_allowed']}`",
        f"- MCP tool call allowed: `{validation['mcp_tool_call_allowed']}`",
        f"- MCP servers started: `{validation['mcp_servers_started']}`",
        f"- MCP tool calls: `{validation['mcp_tool_calls']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        lines.append(
            f"| `{item['name']}` | `{item['expected']}` | `{item['result']['accepted_for_local_report_only_registry']}` | `{item['passed']}` | {errors} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This validator creates local fixture/report files only.",
            "- It does not install, start, enable, publish, or call MCP servers or tools.",
            "- A passing entry is only valid as local report-only registry evidence, not as permission to call an MCP tool.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    schema = load_json(args.schema)
    identity_validation = load_json(IDENTITY_VALIDATION)
    egress_validation = load_json(EGRESS_VALIDATION)
    fixtures = write_fixtures()
    report, validation = build_report(schema, identity_validation, egress_validation, fixtures)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
