#!/usr/bin/env python3
"""Validate durable-runtime reducer fixtures without importing or starting runtimes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from durable_runtime_service_worker_reducer_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Durable Runtime Service-Worker Reducer Fixture v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Schema: `{result['schema_path']}`",
        "",
        "## Summary",
        "",
        f"- Runtime profiles: `{result['runtime_profile_count']}`",
        f"- Service status cases: `{result['status_case_count']}`",
        f"- Expanded reducer checks: `{result['expanded_check_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Required runtimes present: `{str(result['required_runtimes_present']).lower()}`",
        f"- Required statuses present: `{str(result['required_statuses_present']).lower()}`",
        f"- Dependency installs: `{result['runtime_boundary']['dependency_installs']}`",
        f"- Dependency imports: `{result['runtime_boundary']['dependency_imports']}`",
        f"- Runtime starts: `{result['runtime_boundary']['runtime_starts']}`",
        f"- Queue enqueues: `{result['runtime_boundary']['queue_enqueues']}`",
        f"- Service request mutations: `{result['runtime_boundary']['service_request_mutations']}`",
        f"- API calls: `{str(result['runtime_boundary']['api_calls']).lower()}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Expanded Reducer Checks",
        "",
        "| Runtime | Status | Output State | Mode | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["expanded_checks"]:
        status = "pass" if not row["failures"] else "fail"
        lines.append(
            f"| `{row['runtime_id']}` | `{row['status_snapshot']}` | "
            f"`{row['output_state']}` | `{row['allowed_reducer_mode']}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                "The reducer contract permits local previews only. SQLite remains the active "
                "source of truth; external durable runtimes may consume this fixture as a "
                "contract reference only after their own dependency, runtime, service-worker, "
                "credential, and approval gates are cleared."
            ),
            "",
            "## Boundary",
            "",
            "- No dependency install was performed.",
            "- No durable runtime package was imported.",
            "- No runtime was started.",
            "- No queue event was enqueued.",
            "- No service request was mutated.",
            "- No browser session was opened.",
            "- No model/API call was made.",
            "- No external side effect was performed.",
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
