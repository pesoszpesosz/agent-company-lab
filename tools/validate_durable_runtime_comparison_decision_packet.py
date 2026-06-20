#!/usr/bin/env python3
"""Validate durable runtime comparison decision packets without starting runtimes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from durable_runtime_comparison_decision_packet_core import (
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_PACKET,
    DEFAULT_SCHEMA,
    build_result,
    load_json,
)

def write_markdown(result: dict[str, Any], packet: dict[str, Any], path: Path) -> None:
    lines = [
        "# Durable Runtime Comparison Decision Packet v1",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Packet: `{result['packet_path']}`",
        f"Validation JSON: `{result['json_path']}`",
        f"Schema: `{result['schema_path']}`",
        "",
        "## Summary",
        "",
        f"- Source validations checked: `{result['source_validations_checked']}`",
        f"- Runtime recommendations checked: `{result['runtime_recommendations_checked']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Primary recommendation: {packet['decision_summary']['primary_recommendation']}",
        f"- External side effects: `{str(packet['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Runtime Ranking",
        "",
        "| Rank | Runtime | Decision | Score |",
        "| ---: | --- | --- | ---: |",
    ]
    for row in sorted(packet["runtime_recommendations"], key=lambda item: item["rank"]):
        lines.append(f"| {row['rank']} | `{row['runtime_id']}` | `{row['decision']}` | {row['score']} |")
    lines.extend(
        [
            "",
            "## Implementation Sequence",
            "",
            "| Step | Build | Status |",
            "| ---: | --- | --- |",
        ]
    )
    for row in packet["implementation_sequence"]:
        lines.append(f"| {row['sequence']} | `{row['build_id']}` | `{row['status']}` |")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Promote the local SQLite/outbox runner path first. Hold Temporal, "
            "Inngest, DBOS, Pydantic durable execution, Prefect, and Restate behind "
            "explicit dependency/runtime/model/API/server/cloud/database/"
            "service-worker approval gates.",
            "",
            "## Boundary",
            "",
            "- No dependency install, import, runtime start, queue enqueue, workflow start, "
            "event send, server start, database provisioning, service-request mutation, "
            "worker start, browser session, API/model call, public action, "
            "or external side effect.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")




def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    packet = load_json(args.packet)
    result = build_result(
        packet,
        packet_path=args.packet,
        schema_path=args.schema,
        json_path=args.json_out,
        markdown_path=args.md_out,
    )
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(result, packet, args.md_out)
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
