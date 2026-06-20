#!/usr/bin/env python3
"""Validate report-only CEO/operator event surface contract fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ceo_operator_event_surface_contract_core import (
    EVENT_TYPES,
    FIXTURE_DIR,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    build_report,
    fixture_set,
    load_json,
    sha256_path,
)


def write_fixtures() -> list[dict[str, Any]]:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for fixture in fixture_set():
        path = FIXTURE_DIR / f"{fixture['name']}.json"
        path.write_text(json.dumps(fixture["event"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append({"name": fixture["name"], "expected": fixture["expected"], "path": str(path), "sha256": sha256_path(path)})
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# CEO Operator Event Surface Contract v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Contract status: `{validation['contract_status']}`",
        f"- Event types: `{validation['event_type_count']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Event transport enabled: `{validation['event_transport_enabled']}`",
        f"- SSE enabled: `{validation['sse_enabled']}`",
        f"- WebSocket enabled: `{validation['websocket_enabled']}`",
        f"- Operator events emitted: `{validation['operator_events_emitted']}`",
        f"- Service requests updated: `{validation['service_requests_updated']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Event Types",
        "",
        "| Event Type | Producer | Consumer |",
        "| --- | --- | --- |",
    ]
    for event_type, _label, producer, consumer in EVENT_TYPES:
        lines.append(f"| `{event_type}` | `{producer}` | `{consumer}` |")
    lines.extend([
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ])
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        lines.append(
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_contract_only']}` | "
            f"`{item['passed']}` | {errors} |"
        )
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This contract defines local operator event templates only.",
        "- It does not enable SSE, WebSockets, browser sessions, workers, "
        "service-request mutation, model/API calls, MCP tool calls, public actions, "
        "account/wallet/payment actions, or external side effects.",
        "",
        f"Next action: {report['next_action']}",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()
    schema = load_json(args.schema)
    fixtures = write_fixtures()
    report, validation = build_report(schema, fixtures)
    REPORT_JSON.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    VALIDATION_JSON.write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(report, validation)
    print(
        json.dumps(
            {
                "ok": validation["all_checks_passed"],
                "failure_count": validation["failure_count"],
                "validation": str(VALIDATION_JSON),
            },
            indent=2,
        )
    )
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
