#!/usr/bin/env python3
"""Validate local checkpoint interrupt bridge fixtures without importing LangGraph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from checkpoint_interrupt_bridge_fixture_core import (
    FIXTURE_DIR,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    SCORECARD,
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
        path.write_text(json.dumps(fixture["bridge"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
        "# Checkpoint Interrupt Bridge Fixture v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Source scorecard: `{SCORECARD}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Runtime adoption allowed: `{validation['runtime_adoption_allowed']}`",
        f"- Dependency installs: `{validation['dependency_installs']}`",
        f"- External framework imports: `{validation['external_framework_imports']}`",
        f"- Runtime starts: `{validation['runtime_starts']}`",
        f"- Graph nodes executed: `{validation['graph_nodes_executed']}`",
        f"- Resume allowed: `{validation['resume_allowed']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
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
            f"`{item['result']['accepted_for_local_bridge_fixture']}` | "
            f"`{item['passed']}` | {errors} |"
        )
        lines.append(row)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This bridge is local scaffolding only.",
            "- It imports no LangGraph package and installs no dependency.",
            "- It executes no graph node, resumes no checkpoint, applies no decision, and starts no worker or runtime.",
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
