#!/usr/bin/env python3
"""Validate service-worker signed decision intake contracts without applying decisions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from atomic_writes import write_json_atomic
from service_worker_signed_decision_intake_contract_core import (
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    build_report,
    load_json,
)


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Service Worker Signed Decision Intake Contract v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Contract status: `{validation['contract_status']}`",
        f"- Service templates: `{validation['service_template_count']}` / `{validation['service_count']}`",
        (
            f"- Current requests covered: `{validation['current_requests_covered']}` / "
            f"`{validation['current_request_count']}`"
        ),
        f"- Approval granted by contract: `{validation['approval_granted_by_contract']}`",
        f"- Apply allowed: `{validation['apply_allowed']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Templates",
        "",
        "| Service | Decisions | Bound Requests | Route |",
        "| --- | --- | --- | --- |",
    ]
    for template in report["service_templates"]:
        decisions = ", ".join(f"`{decision}`" for decision in template["allowed_decisions"])
        request_count = len(template["allowed_request_ids"])
        lines.append(
            f"| `{template['service_id']}` | {decisions} | `{request_count}` | "
            f"`{template['authority_route']}` |"
        )
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This contract defines the signed-decision intake shape only.",
        (
            "- It grants no approval, applies no decision, assigns no request, starts no "
            "worker, opens no browser, and calls no APIs."
        ),
        "- Any accepted decision still requires a separate apply preflight.",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    schema = load_json(args.schema)
    report, validation = build_report(schema)
    write_json_atomic(REPORT_JSON, report)
    write_json_atomic(VALIDATION_JSON, validation)
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
