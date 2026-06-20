#!/usr/bin/env python3
"""Validate browser read-only worker policy plans without opening a browser."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from browser_read_only_worker_policy_core import (
    FIXTURE_DIR,
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
        "# Browser Read-Only Worker Policy v1 Validation",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Policy verdict: `{validation['policy_verdict']}`",
        f"- Browser session start allowed: `{validation['browser_session_start_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- Fixtures: `{validation['fixture_count']}`",
        f"- Accepted: `{validation['accepted_count']}`",
        f"- Rejected: `{validation['rejected_count']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
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
            f"`{item['result']['accepted_for_browser_read_only_policy']}` | "
            f"`{item['passed']}` | {errors} |"
        )
        lines.append(row)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Passing this validator accepts only a browser research plan shape.",
            "- Passing this validator does not open an in-app browser, Browser Use session, "
            "Playwright session, or signed-in browser.",
            "- Passing this validator does not assign or mutate service requests.",
            "- Login, form submit, account, wallet, payment, public, security testing, "
            "file transfer, MCP tool, model/API, credential, and external side-effect "
            "actions remain blocked.",
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
