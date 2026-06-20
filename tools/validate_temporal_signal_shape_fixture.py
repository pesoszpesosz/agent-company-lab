#!/usr/bin/env python3
"""Validate Temporal signal payload shapes without importing Temporal or sending messages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from temporal_signal_shape_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Temporal Signal Shape Fixture v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Schema: `{result['schema_path']}`",
        "",
        "## Summary",
        "",
        f"- Signal cases checked: `{result['cases_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Temporal imports: `{result['runtime_boundary']['dependency_imports']}`",
        f"- Temporal client connections: `{result['runtime_boundary']['temporal_client_connections']}`",
        f"- Temporal workflows started: `{result['runtime_boundary']['temporal_workflows_started']}`",
        f"- Temporal signals sent: `{result['runtime_boundary']['temporal_signals_sent']}`",
        f"- Service requests updated: `{result['runtime_boundary']['service_requests_updated']}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Signal Cases",
        "",
        "| Case | Signal | Request Status | Shape Valid | Disposition | Validation |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["matches_expected"] else "fail"
        shape_valid = str(row["actual_shape_valid"]).lower()
        lines.append(
            f"| `{row['case_id']}` | `{row['signal_name']}` | "
            f"`{row['status_snapshot']}` | `{shape_valid}` | "
            f"`{row['expected_disposition']}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                "Temporal remains a contract-preview target only. These payloads define what "
                "a future signal handler may accept or reject, but this artifact does not "
                "register handlers, connect a client, start a Workflow, send a Signal, "
                "execute a Query or Update, schedule an Activity, or mutate service requests."
            ),
            "",
            "## Boundary",
            "",
            "- No Temporal package import.",
            "- No Temporal client connection.",
            "- No Temporal server, Worker, Workflow, Signal, Query, Update, or Activity.",
            "- No service request mutation.",
            "- No browser, model/API, public, account, wallet, payment, security, or real-money action.",
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
