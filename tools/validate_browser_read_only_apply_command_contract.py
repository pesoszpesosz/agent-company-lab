#!/usr/bin/env python3
"""Validate report-only browser read-only apply-command contract fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from browser_read_only_apply_command_contract_core import (
    ADAPTER_CONTRACT_VALIDATION,
    APPLY_PREFLIGHT_VALIDATION,
    FIXTURE_DIR,
    GUARD_VALIDATION,
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
        path.write_text(json.dumps(fixture["command"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
        "# Browser Read-Only Apply Command Contract v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Apply preflight validation: `{APPLY_PREFLIGHT_VALIDATION}`",
        f"Guard validation: `{GUARD_VALIDATION}`",
        f"Adapter contract validation: `{ADAPTER_CONTRACT_VALIDATION}`",
        f"Contract report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Source apply preflight status: `{validation['source_apply_preflight_status']}`",
        f"- Source guard adapter contract gate: `{validation['source_guard_adapter_contract_gate']}`",
        f"- Apply command allowed: `{validation['apply_command_allowed']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- Assignment allowed: `{validation['assignment_allowed']}`",
        f"- Browser session start allowed: `{validation['browser_session_start_allowed']}`",
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
        row = (
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_contract_only']}` | "
            f"`{item['passed']}` | {errors} |"
        )
        lines.append(row)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This contract validates command-shaped fixtures only.",
            "- It writes no apply command and executes no command.",
            "- It assigns no service requests, starts no browser sessions, and starts no workers.",
            "- Target request IDs must remain empty until a real signed operator decision "
            "artifact and a separate apply preflight exist.",
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
