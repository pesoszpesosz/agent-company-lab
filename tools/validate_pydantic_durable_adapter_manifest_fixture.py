#!/usr/bin/env python3
"""Validate Pydantic durable adapter manifest fixtures without importing Pydantic AI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pydantic_durable_adapter_manifest_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Pydantic Durable Adapter Manifest Fixture v1",
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
        f"- Pydantic AI imports: `{result['runtime_boundary']['pydantic_ai_imports']}`",
        f"- Durable backend imports: `{result['runtime_boundary']['durable_backend_imports']}`",
        f"- Agent runs: `{result['runtime_boundary']['agent_runs']}`",
        f"- Model API calls: `{str(result['runtime_boundary']['model_api_calls']).lower()}`",
        f"- Model requests allowed: `{str(result['runtime_boundary']['model_requests_allowed']).lower()}`",
        f"- MCP servers started: `{result['runtime_boundary']['mcp_servers_started']}`",
        f"- Runtime starts: `{result['runtime_boundary']['runtime_starts']}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Case Rows",
        "",
        "| Case | Backend | Model Mode | Decision | Validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["matches_expected"] else "fail"
        case_id = row["case_id"]
        backend = row["backend"]
        model_mode = row["model_mode"]
        decision = row["expected_decision"]
        lines.append(
            f"| `{case_id}` | `{backend}` | `{model_mode}` | "
            f"`{decision}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "This manifest keeps Pydantic AI durable execution as a reference layer only. "
            "It permits TestModel and FunctionModel-shaped manifests for Temporal, "
            "DBOS, Prefect, and Restate, but blocks real providers, model requests, "
            "backend imports, runtime starts, MCP server starts, and dynamic durable "
            "toolsets without stable IDs.",
            "",
            "## Boundary",
            "",
            "- No Pydantic AI import.",
            "- No durable backend import.",
            "- No agent run, TestModel run, FunctionModel run, or model/API call.",
            "- No MCP server, runtime, browser, worker, account, wallet, payment, "
            "public, security, or real-money action.",
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
