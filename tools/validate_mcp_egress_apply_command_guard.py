#!/usr/bin/env python3
"""Validate report-only MCP egress apply-command guard fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


from mcp_egress_apply_command_guard_core import (
    APPLY_PREFLIGHT_VALIDATION,
    EGRESS_LEDGER_VALIDATION,
    FIXTURE_DIR,
    IDENTITY_VALIDATION,
    MCP_REGISTRY_VALIDATION,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    TARGET_ROUTE_ID,
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
        path.write_text(json.dumps(fixture["command"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append({"name": fixture["name"], "expected": fixture["expected"], "path": str(path), "sha256": sha256_path(path)})
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# MCP Egress Apply Command Guard v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Target route: `{TARGET_ROUTE_ID}`",
        f"Apply preflight validation: `{APPLY_PREFLIGHT_VALIDATION}`",
        f"MCP registry validation: `{MCP_REGISTRY_VALIDATION}`",
        f"Egress ledger validation: `{EGRESS_LEDGER_VALIDATION}`",
        f"Identity validation: `{IDENTITY_VALIDATION}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Apply command allowed: `{validation['apply_command_allowed']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Gateway start allowed: `{validation['gateway_start_allowed']}`",
        f"- Live egress allowed: `{validation['live_egress_allowed']}`",
        f"- MCP server enable allowed: `{validation['mcp_server_enable_allowed']}`",
        f"- MCP tool call allowed: `{validation['mcp_tool_call_allowed']}`",
        f"- MCP servers started: `{validation['mcp_servers_started']}`",
        f"- MCP servers enabled: `{validation['mcp_servers_enabled']}`",
        f"- Credentials created: `{validation['credentials_created']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        lines.append(f"| `{item['name']}` | `{item['expected']}` | `{item['result']['accepted_for_guard_only']}` | `{item['passed']}` | {errors} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This guard validates report-only MCP command shapes. It writes no command, executes no command, registers no gateway, enables or starts no MCP server, calls no MCP tool, accesses no credentials, starts no worker, mutates no service request, and performs no live egress.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    schema = load_json(args.schema)
    fixtures = write_fixtures()
    report, validation = build_report(schema, fixtures)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
