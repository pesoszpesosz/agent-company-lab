#!/usr/bin/env python3
"""Validate Restate agent-service boundary fixtures without importing Restate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from restate_agent_service_boundary_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    sends = (
        result["runtime_boundary"]["service_calls_or_sends"]
        + result["runtime_boundary"]["object_calls_or_sends"]
        + result["runtime_boundary"]["workflow_calls_or_sends"]
    )
    lines = [
        "# Restate Agent Service Boundary Fixture v1",
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
        f"- Restate imports: `{result['runtime_boundary']['restate_imports']}`",
        f"- Restate server starts: `{result['runtime_boundary']['restate_server_starts']}`",
        f"- Services registered: `{result['runtime_boundary']['services_registered']}`",
        f"- Handlers invoked: `{result['runtime_boundary']['handlers_invoked']}`",
        f"- Service/object/workflow sends: `{sends}`",
        f"- Journal writes: `{result['runtime_boundary']['journal_writes']}`",
        f"- State mutations: `{result['runtime_boundary']['state_mutations']}`",
        f"- LLM calls: `{result['runtime_boundary']['llm_calls']}`",
        f"- Tool executions: `{result['runtime_boundary']['tool_executions']}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Case Rows",
        "",
        "| Case | Message | Shape | Disposition | Validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["matches_expected"] else "fail"
        case_id = row["case_id"]
        message_id = row["source_message_id"]
        service_shape = row["service_shape"]
        disposition = row["outbox_disposition"]
        lines.append(
            f"| `{case_id}` | `{message_id}` | `{service_shape}` | "
            f"`{disposition}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "This fixture treats Restate as a future durable agent/service runtime only. "
            "It allows local preview mappings from central outbox messages to Basic Service, "
            "Virtual Object, and Workflow shapes. It rejects handler invocation, "
            "service/object/workflow calls or sends, journal writes, state mutation, "
            "LLM calls, tool execution, worker starts, browser/API/model/public actions, "
            "service-request mutation, and external side effects.",
            "",
            "## Boundary",
            "",
            "- No Restate package import.",
            "- No Restate server, service registration, handler invocation, "
            "service call/send, object call/send, or workflow call/send.",
            "- No journal write, state mutation, LLM call, or tool execution.",
            "- No service-request mutation, worker start, browser session, API/model call, "
            "public action, account/wallet/payment action, security test, real-money action, "
            "or external side effect.",
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
