#!/usr/bin/env python3
"""Validate runtime-start preflight fixtures without starting any runtime process."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from runtime_start_preflight_core import (
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
        path.write_text(json.dumps(fixture["entry"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
        "# Runtime Start Preflight v1 Validation",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Worker pool: `{WORKER_POOL_ID}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Report JSON: `{REPORT_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Runtime start verdict: `{validation['runtime_start_verdict']}`",
        f"- Runtime start allowed: `{validation['runtime_start_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- Runtime processes started: `{validation['runtime_processes_started']}`",
        f"- Command previews executed: `{validation['command_previews_executed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Activation Chain",
        "",
        f"- Path: `{report['activation_chain']['path']}`",
        f"- All checks passed: `{report['activation_chain'].get('all_checks_passed')}`",
        f"- Chain verdict: `{report['activation_chain'].get('chain_verdict')}`",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        row = (
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_runtime_start_preflight']}` | "
            f"`{item['passed']}` | {errors} |"
        )
        lines.append(row)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Passing this validator does not execute a command preview.",
            "- Passing this validator does not start any local runtime process.",
            "- Passing this validator does not assign service requests, start workers, "
            "enable MCP tools, open browsers, or use credentials.",
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
