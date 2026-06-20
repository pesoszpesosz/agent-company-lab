#!/usr/bin/env python3
"""Validate browser-worker adapter contracts without starting a browser runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from browser_worker_adapter_contract_core import (
    FIXTURE_DIR,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    TRACE_METADATA_JSON,
    VALIDATION_JSON,
    build_report,
    build_trace_metadata,
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
        "# Browser Worker Adapter Contract v1 Validation",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Contract verdict: `{validation['contract_verdict']}`",
        f"- Browser session start allowed: `{validation['browser_session_start_allowed']}`",
        f"- Worker start allowed: `{validation['worker_start_allowed']}`",
        f"- Fixtures: `{validation['fixture_count']}`",
        f"- Accepted: `{validation['accepted_count']}`",
        f"- Rejected: `{validation['rejected_count']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Accepted Runtime Shape",
        "",
        "The only accepted fixture is a report-only `playwright_deterministic` adapter contract "
        "tied to an existing `browser_read_only_session` service request. It allows public "
        "HTTPS navigation, visible text reading, accessibility snapshots, screenshots, and "
        "local evidence writes, but it still blocks browser and worker starts.",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        lines.append(
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_adapter_contract']}` | "
            f"`{item['passed']}` | {errors} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Passing this contract does not start Playwright, Browser Use, Stagehand, "
            "Playwright MCP, agent-browser, cloud browsers, extensions, or browser forks.",
            "- Passing this contract does not approve service requests or assign workers.",
            "- Login, form submit, account, wallet, payment, public, security testing, "
            "file transfer, model/API, credential, MCP server, and external side-effect "
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
    trace_metadata = build_trace_metadata(validation)
    REPORT_JSON.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    VALIDATION_JSON.write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    TRACE_METADATA_JSON.write_text(
        json.dumps(trace_metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
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
