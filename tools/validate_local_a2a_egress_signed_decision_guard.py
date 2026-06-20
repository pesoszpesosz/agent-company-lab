#!/usr/bin/env python3
"""Validate signed local A2A egress-route decisions without applying them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from local_a2a_egress_signed_decision_guard_core import (
    EGRESS_VALIDATION,
    FIXTURE_DIR,
    IDENTITY_VALIDATION,
    INTAKE_REPORT,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    TARGET_ROUTE_ID,
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
        path.write_text(json.dumps(fixture["decision"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append({"name": fixture["name"], "expected": fixture["expected"], "path": str(path), "sha256": sha256_path(path)})
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Local A2A Egress Signed Decision Guard v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Target route: `{TARGET_ROUTE_ID}`",
        f"Source intake contract: `{INTAKE_REPORT}`",
        f"Egress ledger validation: `{EGRESS_VALIDATION}`",
        f"Identity validation: `{IDENTITY_VALIDATION}`",
        f"Guard report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Gateway starts: `{validation['gateway_starts']}`",
        f"- Live egress events: `{validation['live_egress_events']}`",
        f"- Agent message send allowed: `{validation['agent_message_send_allowed']}`",
        f"- Agent messages sent: `{validation['agent_messages_sent']}`",
        f"- Service requests assigned: `{validation['service_requests_assigned']}`",
        f"- Service requests updated: `{validation['service_requests_updated']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
        f"- Decisions applied: `{validation['decisions_applied']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Required Gates",
        "",
    ]
    for gate in report["target_route_required_gates"]:
        lines.append(f"- `{gate}`")
    lines.extend(
        [
            "",
            "## Fixture Results",
            "",
            "| Fixture | Expected | Accepted | Passed | Primary Errors |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        lines.append(
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_apply_preflight']}` | `{item['passed']}` | {errors} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Accepted decisions are accepted only for a later apply-preflight blocker. This guard does not "
            "write approvals, mutate service requests, register gateways, send agent messages, start workers, "
            "call models, call MCP tools, open browsers, or perform live egress.",
            "",
            f"Next action: {report['next_action']}",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    schema = load_json(args.schema)
    fixtures = write_fixtures()
    report, validation = build_report(schema, fixtures)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
