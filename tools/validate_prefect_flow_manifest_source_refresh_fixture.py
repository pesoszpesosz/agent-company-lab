#!/usr/bin/env python3
"""Validate Prefect source-refresh flow manifests without importing Prefect."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from prefect_flow_manifest_source_refresh_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Prefect Source-Refresh Flow Manifest Fixture v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Schema: `{result['schema_path']}`",
        "",
        "## Summary",
        "",
        f"- Cases checked: `{result['cases_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Prefect imports: `{result['runtime_boundary']['prefect_imports']}`",
        f"- Flow runs: `{result['runtime_boundary']['flow_runs']}`",
        f"- Task runs: `{result['runtime_boundary']['task_runs']}`",
        f"- Deployments created: `{result['runtime_boundary']['deployments_created']}`",
        f"- Schedules created: `{result['runtime_boundary']['schedules_created']}`",
        f"- Workers started: `{result['runtime_boundary']['workers_started']}`",
        f"- Test harness starts: `{result['runtime_boundary']['prefect_test_harness_starts']}`",
        f"- API calls: `{str(result['runtime_boundary']['api_calls']).lower()}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Case Rows",
        "",
        "| Case | Source | Mode | Decision | Validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["matches_expected"] else "fail"
        lines.append(
            f"| `{row['case_id']}` | `{row['source_id']}` | "
            f"`{row['allowed_mode']}` | `{row['expected_decision']}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                "This manifest treats Prefect as a future flow-orchestration adapter for "
                "source refreshes, not as an active runtime. It allows only local-file, "
                "local-planning, and read-only GitHub metadata preview manifests. Browser, "
                "service-request-only, API, public-action, security, wallet, payment, "
                "model/API, deployment, schedule, work-pool, worker, server/cloud, and "
                "test-harness execution paths are rejected."
            ),
            "",
            "## Boundary",
            "",
            "- No Prefect package import.",
            "- No `@flow` or `@task` decoration.",
            (
                "- No flow run, task run, deployment, schedule, work pool, worker, test "
                "harness, server, cloud, or API call."
            ),
            (
                "- No service-request mutation, browser session, public action, account "
                "action, wallet/payment action, security test, model/API call, real-money "
                "action, or external side effect."
            ),
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
