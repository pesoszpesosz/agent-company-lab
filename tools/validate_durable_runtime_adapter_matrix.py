#!/usr/bin/env python3
"""Validate the durable runtime adapter matrix without installing or starting runtimes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from durable_runtime_adapter_matrix_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Durable Runtime Adapter Matrix v2",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Schema: `{result['schema_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        "",
        "## Summary",
        "",
        f"- Runtime rows checked: `{result['rows_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Required runtimes present: `{str(result['required_runtimes_present']).lower()}`",
        f"- Dependency installs: `{str(result['artifact_actions']['dependency_installs']).lower()}`",
        f"- Dependency imports: `{str(result['artifact_actions']['dependency_imports']).lower()}`",
        f"- Runtime starts: `{result['artifact_actions']['runtime_starts']}`",
        f"- Queue enqueues: `{result['artifact_actions']['queue_enqueues']}`",
        f"- Service request mutations: `{result['artifact_actions']['service_request_mutations']}`",
        f"- API calls: `{str(result['artifact_actions']['api_calls']).lower()}`",
        f"- External side effects: `{str(result['artifact_actions']['external_side_effects']).lower()}`",
        "",
        "## Matrix",
        "",
        "| Runtime | Category | Safe Now | Score | Decision | Status |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if not row["failures"] else "fail"
        runtime_id = row["runtime_id"]
        category = row["category"]
        safe_now = str(row["safe_now"]).lower()
        score = row["score"]
        decision = row["promotion_decision"]
        lines.append(
            f"| `{runtime_id}` | `{category}` | `{safe_now}` | `{score}` | "
            f"{decision} | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Recommended Next Local Tests",
            "",
        ]
    )
    for test in result["recommended_next_local_tests"]:
        lines.append(f"- `{test}`")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            result["decision"],
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
