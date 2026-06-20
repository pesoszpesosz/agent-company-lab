#!/usr/bin/env python3
"""Validate central outbox/history fixtures without external side effects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from central_outbox_history_core import (
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Agent Company Central Outbox History v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Schema: `{result['schema_path']}`",
        "",
        "## Summary",
        "",
        f"- Messages checked: `{result['messages_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- External side effects: `{str(result['external_side_effects']).lower()}`",
        "",
        "## Messages",
        "",
        "| Message | Lane | Type | Approval | Replay | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if not row["failures"] else "fail"
        message_id = row["message_id"]
        lane_id = row["lane_id"]
        message_type = row["message_type"]
        approval = row["approval_posture"]
        replay = row["replay_status"]
        lines.append(
            f"| `{message_id}` | `{lane_id}` | `{message_type}` | "
            f"`{approval}` | `{replay}` | `{status}` |"
        )
    lines.extend(
        [
            "",
            "## Contract Decision",
            "",
            "Use this v1 outbox/history contract as a local replay surface for "
            "manager and service-worker communication before adding Temporal, "
            "Inngest, DBOS, LangGraph, OpenAI Agents, or A2A execution adapters.",
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
            "- Runtime starts: `0`",
            "- Service requests updated: `0`",
            "- Worker starts: `0`",
            "- External side effects: `false`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")




def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
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
