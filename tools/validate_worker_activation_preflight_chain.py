#!/usr/bin/env python3
"""Validate the local worker activation preflight chain without enabling workers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from worker_activation_preflight_chain_core import (
    FIXTURE_DIR,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    WORKER_POOL_ID,
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
        path.write_text(
            json.dumps(fixture["entry"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(
            {
                "name": fixture["name"],
                "expected": fixture["expected"],
                "path": str(path),
                "sha256": sha256_path(path),
            }
        )
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Worker Activation Preflight Chain v1 Validation",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Worker pool: `{WORKER_POOL_ID}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Report JSON: `{REPORT_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Chain verdict: `{validation['chain_verdict']}`",
        f"- Registration allowed: `{validation['registration_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- MCP tool call allowed: `{validation['mcp_tool_call_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Composed Validators",
        "",
        "| Validator | All Checks Passed | Accepted | Rejected |",
        "| --- | --- | ---: | ---: |",
    ]
    for name, summary in report["composed_validators"].items():
        lines.append(
            f"| `{name}` | `{summary.get('all_checks_passed')}` | "
            f"`{summary.get('accepted_count')}` | `{summary.get('rejected_count')}` |"
        )
    lines.extend(
        [
            "",
            "## Fixture Results",
            "",
            "| Fixture | Expected | Accepted | Passed | Primary Errors |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        accepted = item["result"]["accepted_for_activation_preflight"]
        lines.append(
            f"| `{item['name']}` | `{item['expected']}` | `{accepted}` | "
            f"`{item['passed']}` | {errors} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Passing this chain does not register a worker pool.",
            "- Passing this chain does not assign service requests.",
            "- Passing this chain does not start workers or enable MCP tool calls.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    print(
        json.dumps(
            {
                "ok": validation["all_checks_passed"],
                "failure_count": validation["failure_count"],
                "validation": str(VALIDATION_JSON),
            },
            indent=2,
        )
    )
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
