#!/usr/bin/env python3
"""Validate browser read-only service-request assignment preflight without assigning workers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from browser_read_only_assignment_preflight_core import (
    ADAPTER_CONTRACT_VALIDATION,
    POLICY_VALIDATION,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    build_report,
    load_json,
)


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Browser Read-Only Assignment Preflight v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Policy validation: `{POLICY_VALIDATION}`",
        f"Adapter contract validation: `{ADAPTER_CONTRACT_VALIDATION}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Preflight verdict: `{validation['preflight_verdict']}`",
        f"- Candidate requests: `{validation['candidate_request_count']}`",
        f"- Assignment allowed: `{validation['assignment_allowed_count']}`",
        f"- Blocked without signed approval: `{validation['blocked_no_signed_approval_count']}`",
        f"- Browser sessions started: `{validation['browser_sessions_started']}`",
        f"- Service requests assigned: `{validation['service_requests_assigned']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Candidate Requests",
        "",
        "| Request | Lane | Packet Complete | Assignment Allowed | Blocked Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["candidate_requests"]:
        lines.append(
            f"| `{row['request_id']}` | `{row['lane_id']}` | "
            f"`{row['packet_complete']}` | `{row['assignment_allowed']}` | "
            f"`{row['blocked_reason']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This preflight reads the queue and policy validation only.",
            "- It does not assign service requests, start workers, open browsers, mutate "
            "queue state, or perform external actions.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    schema = load_json(args.schema)
    report, validation = build_report(schema)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
