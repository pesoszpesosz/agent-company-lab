#!/usr/bin/env python3
"""Validate DBOS workflow/step boundary fixtures without importing DBOS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from dbos_workflow_step_boundary_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# DBOS Workflow Step Boundary Fixture v1",
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
        f"- DBOS imports: `{result['runtime_boundary']['dependency_imports']}`",
        f"- DBOS launch called: `{str(result['runtime_boundary']['dbos_launch_called']).lower()}`",
        f"- Database connections: `{result['runtime_boundary']['database_connections']}`",
        f"- Queues registered: `{result['runtime_boundary']['queues_registered']}`",
        f"- Workflows started: `{result['runtime_boundary']['workflows_started']}`",
        f"- Workflows enqueued: `{result['runtime_boundary']['workflows_enqueued']}`",
        f"- Steps executed: `{result['runtime_boundary']['steps_executed']}`",
        f"- Service requests updated: `{result['runtime_boundary']['service_requests_updated']}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Case Rows",
        "",
        "| Case | Service Request | Snapshot | State | Validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["matches_expected"] else "fail"
        lines.append(
            f"| `{row['case_id']}` | `{row['service_request_id']}` | "
            f"`{row['status_snapshot']}` | `{row['expected_state']}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                "This is a static DBOS boundary contract for future service-worker orchestration. "
                "It maps service-request snapshots to workflow IDs, deduplication IDs, queue "
                "partition keys, and preview-only step boundaries without importing DBOS, "
                "launching DBOS, provisioning a database, registering queues, starting "
                "workflows, enqueueing workflows, executing steps, or mutating service requests."
            ),
            "",
            "## Boundary",
            "",
            "- No DBOS package import.",
            "- No `DBOS.launch()` call.",
            "- No Postgres or DBOS system database provisioning.",
            "- No queue registration, workflow start, workflow enqueue, or step execution.",
            (
                "- No service-request mutation, worker start, browser session, model/API call, "
                "public action, account action, wallet action, payment action, security test, "
                "real-money action, or external side effect."
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
