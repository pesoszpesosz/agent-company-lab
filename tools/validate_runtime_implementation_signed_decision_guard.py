#!/usr/bin/env python3
"""Validate signed runtime implementation decisions without applying them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from runtime_implementation_signed_decision_guard_core import (
    APPROVAL_PACKET,
    FIXTURE_DIR,
    GUARD_JSON,
    GUARD_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    build_guard_report,
    fixture_set,
    load_json,
    sha256_path,
)


def write_fixtures(packet: dict[str, Any]) -> list[dict[str, Any]]:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    written: list[dict[str, Any]] = []
    for fixture in fixture_set(packet):
        path = FIXTURE_DIR / f"{fixture['name']}.json"
        path.write_text(json.dumps(fixture["decision"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(
            {
                "name": fixture["name"],
                "expected": fixture["expected"],
                "path": str(path),
                "sha256": sha256_path(path),
            }
        )
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Runtime Implementation Signed Decision Guard v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Source approval packet: `{APPROVAL_PACKET}`",
        f"Guard report JSON: `{GUARD_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Fixture count: `{validation['fixture_count']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Decisions applied: `{validation['decisions_applied']}`",
        f"- Runtime implementation allowed: `{validation['runtime_implementation_allowed']}`",
        f"- Runtime code write allowed: `{validation['runtime_code_write_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        row = (
            f"| `{item['name']}` | `{item['expected']}` | "
            f"`{item['result']['accepted_for_later_preflight']}` | "
            f"`{item['passed']}` | {errors} |"
        )
        lines.append(row)
    lines.extend(
        [
            "",
            "## Guard Boundary",
            "",
            "- Accepted decisions are accepted for later preflight only.",
            "- This guard applies no approval, writes no approval rows, installs no dependencies, "
            "starts no runtime/server/worker, mutates no service request, opens no browser, "
            "calls no API/model, performs no public/account/wallet/payment/security/real-money "
            "action, and has no external side effects.",
            "- Browser/public, wallet/payment/real-money, and security-testing approvals are "
            "rejected here because those require separate lane-specific service gates.",
        ]
    )
    GUARD_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approval-packet", type=Path, default=APPROVAL_PACKET)
    args = parser.parse_args()

    packet = load_json(args.approval_packet)
    fixtures = write_fixtures(packet)
    report, validation = build_guard_report(packet, fixtures)
    GUARD_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
