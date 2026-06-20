#!/usr/bin/env python3
"""Validate agent egress event ledger fixtures without performing live egress."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agent_egress_event_ledger_core import (
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
        path.write_text(json.dumps(fixture["event"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append({"name": fixture["name"], "expected": fixture["expected"], "path": str(path), "sha256": sha256_path(path)})
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Agent Egress Event Ledger v1 Validation",
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
        f"- Live egress allowed: `{validation['live_egress_allowed']}`",
        f"- Gateway started: `{validation['gateway_started']}`",
        f"- Model API calls: `{validation['model_api_calls']}`",
        f"- MCP tool calls: `{validation['mcp_tool_calls']}`",
        f"- Browser sessions started: `{validation['browser_sessions_started']}`",
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
            f"| `{item['name']}` | `{item['expected']}` | `{item['result']['accepted_for_local_report_only_preflight']}` | `{item['passed']}` | {errors} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This validator creates local fixture/report files only.",
            "- It does not start a gateway, install a gateway, create API keys, record live egress, call model APIs, call MCP tools, open a browser, register pools, assign service requests, start workers, or perform credential/wallet/payment/public actions.",
            "- A passing event is only acceptable as local report-only preflight evidence.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    schema = load_json(args.schema)
    identity_validation = load_json(IDENTITY_VALIDATION)
    fixtures = write_fixtures()
    report, validation = build_report(schema, identity_validation, fixtures)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
