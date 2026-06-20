#!/usr/bin/env python3
"""Validate service-worker approval authority coverage without granting authority."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from service_worker_approval_authority_coverage_core import (
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    VALIDATION_JSON,
    build_report,
    load_json,
)


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Service Worker Approval Authority Coverage v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Coverage status: `{validation['coverage_status']}`",
        f"- Services covered: `{validation['service_rows_covered']}` / `{validation['service_count']}`",
        (
            f"- Current requests covered: `{validation['current_requests_covered']}` / "
            f"`{validation['current_request_count']}`"
        ),
        f"- Missing roles: `{validation['missing_role_count']}`",
        f"- Approval granted by coverage: `{validation['approval_granted_by_coverage']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Services",
        "",
        "| Service | Risk Family | Authorities | Route | Covered |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["service_rows"]:
        authority_list = ", ".join(f"`{item}`" for item in row["approval_required_by"])
        lines.append(
            f"| `{row['service_id']}` | `{row['risk_family']}` | {authority_list} | "
            f"`{row['authority_route']}` | `{row['covered']}` |"
        )
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This report covers authority routes only.",
        "- It does not approve, reject, assign, update, start, browse, call APIs, or perform external actions.",
    ])
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
