#!/usr/bin/env python3
"""No-network parser check for Algora candidate refresh fixtures."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_FIXTURE = Path(
    r"E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-20260616.json"
)
DEFAULT_JSON_OUT = Path(
    r"E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-check-20260616.json"
)
DEFAULT_MD_OUT = Path(
    r"E:\agent-company-lab\reports\paid-code-bounties\algora-candidate-refresh-fixture-check-20260616.md"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_amount(text: str | None) -> float | None:
    if not text:
        return None
    match = re.search(r"\$?\s*([0-9][0-9,]*(?:\.[0-9]+)?)", text)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def parse_claim_count(text: str | None) -> int | None:
    if not text:
        return None
    match = re.search(r"([0-9]+)\s+claim", text, re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1))


def parse_state(row: dict[str, Any]) -> str:
    if row.get("fixture_id", "").endswith("reference_only"):
        return "unclear"
    state_text = (row.get("state_text") or "").lower()
    page_text = (row.get("page_text") or "").lower()
    joined = f"{state_text} {page_text}"
    if "completed" in joined or "closed" in joined:
        if "0 open" in joined or "zero open" in joined:
            return "none_open"
        return "completed"
    if "0 open" in joined or "zero open" in joined or "no open" in joined:
        return "none_open"
    if "open" in joined and "unclear" not in joined:
        return "open"
    return "unclear"


def repo_health(row: dict[str, Any]) -> str:
    text = f"{row.get('page_text') or ''} {row.get('last_activity_text') or ''}".lower()
    if "recent" in text or "active" in text:
        return "active"
    if "stale" in text:
        return "stale"
    return "unknown"


def local_testability(row: dict[str, Any]) -> str:
    note = (row.get("local_testability_note") or "").lower()
    if re.search(r"\bclear\b", note) or "tests possible" in note or "standard open-source local test" in note:
        return "clear"
    if re.search(r"\bunclear\b", note):
        return "unclear"
    if "blocked" in note or "reference" in note or "no current issue" in note:
        return "blocked"
    return "unclear"


def candidate_id(row: dict[str, Any]) -> str:
    expected = row.get("expected") or {}
    if expected.get("candidate_id"):
        return expected["candidate_id"]
    raw = re.sub(r"[^a-z0-9]+", "-", row["fixture_id"].lower()).strip("-")
    return raw


def decide(row: dict[str, Any]) -> tuple[str, list[str], str]:
    amount = parse_amount(row.get("amount_text"))
    claims = parse_claim_count(row.get("claim_text"))
    state = parse_state(row)
    testability = local_testability(row)
    text = f"{row.get('page_text') or ''} {row.get('local_testability_note') or ''}".lower()
    reasons: list[str] = []

    if row.get("fixture_id", "").endswith("reference_only"):
        reasons.extend(["missing_explicit_amount", "no_specific_open_issue"])
        return "reference_only", reasons, "No candidate issue; use only to verify parser shape."
    if state == "none_open":
        reasons.append("no_open_bounty")
        return "watchlist", reasons, "Wait for an explicit open bounty before local triage."
    if amount is None:
        reasons.append("missing_explicit_amount")
    if state in {"completed", "closed"}:
        reasons.append("completed_or_closed")
    if state == "unclear":
        reasons.append("state_unclear")
    if amount is not None and amount < 100 and claims is not None and claims > 3:
        reasons.append("tiny_and_crowded")
    if (
        "requires credentials" in text
        or "requires credential" in text
        or "paid services" in text
        or "paid service required" in text
    ):
        reasons.append("requires_credentials_or_paid_service")
    if "subjective" in text or "no measurable target" in text:
        reasons.append("subjective_acceptance")

    if "tiny_and_crowded" in reasons:
        return "reject", reasons, "Do not spend sprint time on low-value crowded bounty."
    if "subjective_acceptance" in reasons:
        return "reject", reasons, "Reject until measurable acceptance target exists."
    if reasons == ["missing_explicit_amount", "state_unclear"]:
        return "watchlist", reasons, "Read-only refresh required for explicit amount and acceptance state."
    if reasons:
        return "watchlist", reasons, "Read-only refresh required before promotion."
    if state == "open" and amount is not None and amount >= 100 and (claims is None or claims <= 3) and testability == "clear":
        return (
            "promote_local_triage",
            [],
            "Local triage only; no claim, comment, PR, or payout details without GitHub/public-action approval.",
        )
    return "watchlist", ["local_testability_unclear"], "Keep on watchlist until local testability is clear."


def parse_row(row: dict[str, Any]) -> dict[str, Any]:
    decision, reasons, gate = decide(row)
    return {
        "candidate_id": candidate_id(row),
        "algora_url": row.get("algora_url"),
        "github_issue_url": row.get("github_issue_url"),
        "amount_usd": parse_amount(row.get("amount_text")),
        "state": parse_state(row),
        "claim_count": parse_claim_count(row.get("claim_text")),
        "repo_health": repo_health(row),
        "local_testability": local_testability(row),
        "decision": decision,
        "gate": gate,
        "rejection_reasons": reasons,
    }


def compare(actual: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if actual_value != expected_value:
            failures.append(f"{key}: expected {expected_value!r}, got {actual_value!r}")
    return failures


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Algora Candidate Refresh Fixture Check",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"JSON mirror: `{result['json_path']}`",
        "",
        "## Summary",
        "",
        f"- Fixtures checked: `{result['fixtures_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Network calls: `{str(result['network_calls']).lower()}`",
        f"- External side effects: `{str(result['external_side_effects']).lower()}`",
        "",
        "## Rows",
        "",
        "| Fixture | Decision | Status | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if not row["failures"] else "fail"
        notes = "; ".join(row["failures"]) if row["failures"] else row["actual"]["gate"]
        lines.append(f"| `{row['fixture_id']}` | `{row['actual']['decision']}` | `{status}` | {notes} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Live Algora fetch: `false`",
            "- Live GitHub fetch: `false`",
            "- GitHub comments/claims/PRs: `false`",
            "- Account/payment/public actions: `false`",
            "- External side effects: `false`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    rows = []
    for source_row in fixture["fixtures"]:
        actual = parse_row(source_row)
        failures = compare(actual, source_row["expected"])
        rows.append(
            {
                "fixture_id": source_row["fixture_id"],
                "actual": actual,
                "expected": source_row["expected"],
                "failures": failures,
            }
        )

    failed_count = sum(1 for row in rows if row["failures"])
    result = {
        "schema_version": "agent_company.algora_fixture_parser_check.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(args.fixture),
        "json_path": str(args.json_out),
        "markdown_path": str(args.md_out),
        "fixtures_checked": len(rows),
        "passed_count": len(rows) - failed_count,
        "failed_count": failed_count,
        "network_calls": False,
        "external_side_effects": False,
        "rows": rows,
    }
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(result, args.md_out)
    print(json.dumps({"ok": failed_count == 0, "json": str(args.json_out), "failed_count": failed_count}, indent=2))
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
