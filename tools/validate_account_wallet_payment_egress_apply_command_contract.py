#!/usr/bin/env python3
"""Validate report-only account/wallet/payment egress apply-command contract fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


from account_wallet_payment_egress_apply_command_contract_core import (
    FIXTURE_DIR,
    REPORT_JSON,
    REPORT_MD,
    SCHEMA_PATH,
    TARGET_EGRESS_TYPE,
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
        path.write_text(json.dumps(fixture["command"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append({"name": fixture["name"], "expected": fixture["expected"], "path": str(path), "sha256": sha256_path(path)})
    return written


def write_markdown(report: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Account Wallet Payment Egress Apply Command Contract v1",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Target route: `{TARGET_ROUTE_ID}`",
        f"Report JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Accepted fixtures: `{validation['accepted_count']}`",
        f"- Rejected fixtures: `{validation['rejected_count']}`",
        f"- Apply command allowed: `{validation['apply_command_allowed']}`",
        f"- Account creation allowed: `{validation['account_creation_allowed']}`",
        f"- Wallet creation allowed: `{validation['wallet_creation_allowed']}`",
        f"- Payment action allowed: `{validation['payment_action_allowed']}`",
        f"- Real-money action allowed: `{validation['real_money_action_allowed']}`",
        f"- Accounts created: `{validation['accounts_created']}`",
        f"- Wallets created: `{validation['wallets_created']}`",
        f"- Funds transferred: `{validation['funds_transferred']}`",
        f"- KYC submissions: `{validation['kyc_submissions']}`",
        f"- Service requests updated: `{validation['service_requests_updated']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Expected | Accepted | Passed | Primary Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["results"]:
        errors = ", ".join(item["result"]["errors"][:4])
        lines.append(f"| `{item['name']}` | `{item['expected']}` | `{item['result']['accepted_for_contract_only']}` | `{item['passed']}` | {errors} |")
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This contract is report-only and writes no apply command.",
        "- Account/wallet/payment execution remains blocked until a real signed decision, exact approval, and immutable command preview exist.",
        "- No account creation, terms acceptance, wallet creation, private-key or seed custody, fund transfer, payment method change, KYC/tax/legal action, public payment-address publication, service-request mutation, worker start, browser start, model/MCP call, live egress, or external side effect is allowed.",
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
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
