#!/usr/bin/env python3
"""Validate browser-worker safety fixture classifications locally."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from browser_worker_safety_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Browser Worker Safety Fixture v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Schema: `{result['schema_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        "",
        "## Summary",
        "",
        f"- Cases checked: `{result['cases_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Browser sessions started: `{result['browser_sessions_started']}`",
        f"- External side effects: `{str(result['external_side_effects']).lower()}`",
        "",
        "## Cases",
        "",
        "| Case | Lane | Class | Decision | Gate | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if not row["failures"] else "fail"
        case_id = row["case_id"]
        lane_id = row["lane_id"]
        classification = row["actual_classification"]
        decision = row["actual_decision"]
        gate = row["actual_required_gate"]
        lines.append(
            f"| `{case_id}` | `{lane_id}` | `{classification}` | "
            f"`{decision}` | `{gate}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Contract Decision",
            "",
            "Use this fixture before any Browser Use, Browser Harness, in-app browser, "
            "signed-in browser, or public-action worker starts. It is a classifier "
            "and validator only; it grants no approval.",
            "",
            "## Boundary",
            "",
            "- Browser sessions started: `0`",
            "- Account actions: `false`",
            "- Wallet actions: `false`",
            "- Payment actions: `false`",
            "- Public actions: `false`",
            "- Security testing actions: `false`",
            "- Model/API calls: `false`",
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
    args = parser.parse_args()

    fixture = load_json(args.fixture)
    result = build_result(
        fixture,
        fixture_path=args.fixture,
        schema_path=args.schema,
        json_path=args.json_out,
        markdown_path=args.md_out,
    )
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
