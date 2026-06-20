#!/usr/bin/env python3
"""Validate Inngest event naming and flow-control fixtures without using Inngest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from inngest_event_flow_control_fixture_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Inngest Event Flow-Control Fixture v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Schema: `{result['schema_path']}`",
        "",
        "## Summary",
        "",
        f"- Events checked: `{result['events_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Inngest imports: `{result['runtime_boundary']['dependency_imports']}`",
        f"- Inngest functions registered: `{result['runtime_boundary']['inngest_functions_registered']}`",
        f"- Inngest events sent: `{result['runtime_boundary']['inngest_events_sent']}`",
        f"- Service requests updated: `{result['runtime_boundary']['service_requests_updated']}`",
        f"- External side effects: `{str(result['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Event Rows",
        "",
        "| Event | Source Message | Name | Decision | Validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["matches_expected"] else "fail"
        event_id = row["event_id"]
        message_id = row["source_message_id"]
        event_name = row["event_name"]
        decision = row["expected_decision"]
        lines.append(
            f"| `{event_id}` | `{message_id}` | `{event_name}` | "
            f"`{decision}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "This is a static contract for future Inngest adapters. It defines event names, "
            "idempotency keys, concurrency keys, throttle keys, and rate-limit behavior "
            "from central outbox messages. It does not create an Inngest client, "
            "register functions, send events, start a server, call APIs, or mutate "
            "service requests.",
            "",
            "## Boundary",
            "",
            "- No Inngest package import.",
            "- No Inngest client, function registration, server, send, or step event.",
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
