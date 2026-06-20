#!/usr/bin/env python3
"""Validate checkpoint interrupt contracts without resuming or applying work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from checkpoint_interrupt_contract_core import (
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
        path.write_text(json.dumps(fixture["checkpoint"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
        "# Checkpoint Interrupt Contract v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Resume allowed: `{validation['resume_allowed']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Source State",
        "",
        "| Source | Ready |",
        "| --- | --- |",
    ]
    for key, value in report["source_state"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Fixture Results",
            "",
            "| Fixture | Expected | Accepted | Passed | Errors |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        row = (
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_checkpoint_interrupt']}` | "
            f"`{item['passed']}` | {errors} |"
        )
        lines.append(row)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Checkpoint interrupts pause work; they do not resume it.",
            "- They write no apply or resume command.",
            "- They start no worker, runtime, browser, MCP tool, model call, public action, wallet action, or payment.",
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
