from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .registry import evidence_id_for_source, upsert_evidence
from .utils import compact_text
from .profit_edge_source_summary import find_first_url

SUBMITTED_PAYOUT_OWNERSHIP_NOTE = (
    "Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane."
)
def normalize_profit_edge_lane(row: dict[str, Any]) -> str:
    raw_lane = str(row.get("lane", "")).lower()
    strategy = str(row.get("strategy", "")).lower()
    values = [
        raw_lane,
        strategy,
        str(row.get("event", "")),
        str(row.get("event_id", "")),
        str(row.get("opportunity", "")),
        str(row.get("result", "")),
        str(row.get("nextAction", "")),
        str(row.get("next_action", "")),
    ]
    combined = " ".join(values).lower()
    if "security_bounty" in raw_lane or "security_bounty" in strategy or "google_oss_vrp" in strategy:
        return "security_bounty_private_reports"
    if "paid_code" in raw_lane:
        if "rustchain" in combined and ("payout" in combined or "wallet" in combined or "monitor" in combined):
            return "submitted_bounty_payouts"
        return "paid_code_bounties"
    if "rustchain" in combined and ("payout" in combined or "wallet" in combined or "monitor" in combined):
        return "submitted_bounty_payouts"
    if "cashflow_monitor" in combined or "submitted_bounty_monitor" in combined:
        return "submitted_bounty_payouts"
    if "security" in combined or "vrp" in combined or "ghsa" in combined or "advisory" in combined:
        return "security_bounty_private_reports"
    if (
        "prediction" in combined
        or "kalshi" in combined
        or "polymarket" in combined
        or "cross_venue" in combined
        or "cross-venue" in combined
        or "market" in combined
    ):
        return "prediction_market_research"
    if "web3" in combined or "hackathon" in combined or "airdrop" in combined or "grant" in combined:
        return "web3_airdrops_grants_hackathons"
    if "twitter" in combined or "x.com" in combined or "traction" in combined or "content" in combined:
        return "content_and_social_growth"
    if "lead" in combined or "sales" in combined or "outreach" in combined:
        return "lead_generation_and_sales"
    if "trading" in combined or "backtest" in combined or "quant" in combined:
        return "local_trading_strategy_research"
    if "bounty" in combined or "paid_code" in combined or "github" in combined or "algora" in combined or "opire" in combined:
        return "paid_code_bounties"
    return "platform_engineering"


def import_ledger_rows(conn: sqlite3.Connection, source_root: Path, ledger_tail: int) -> list[dict[str, str | None]]:
    ledger_path = source_root / "opportunities" / "opportunity-ledger.jsonl"
    if not ledger_path.exists():
        return []
    raw_lines = [line for line in ledger_path.read_text(encoding="utf-8-sig", errors="replace").splitlines() if line.strip()]
    imported: list[dict[str, str | None]] = []
    for line in raw_lines[-ledger_tail:]:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        lane_id = normalize_profit_edge_lane(row)
        title = compact_text(str(row.get("opportunity") or row.get("event") or row.get("event_id") or "Profit Edge ledger row"), 160) or "Profit Edge ledger row"
        event_key = "|".join(
            [
                str(row.get("timestamp_utc") or row.get("timestampUtc") or ""),
                str(row.get("event_id") or ""),
                str(row.get("event") or ""),
                title,
                find_first_url(row) or "",
            ]
        )
        evidence_id = evidence_id_for_source("pe-ledger", event_key, title)
        ownership_note = SUBMITTED_PAYOUT_OWNERSHIP_NOTE if lane_id == "submitted_bounty_payouts" else "Read-only ledger import for future lane managers."
        evidence = {
            "evidence_id": evidence_id,
            "lane_id": lane_id,
            "source_path": str(ledger_path),
            "source_url": find_first_url(row),
            "title": title,
            "status": compact_text(str(row.get("decision") or row.get("event") or row.get("lane") or "imported"), 80) or "imported",
            "summary": compact_text(str(row.get("result") or row.get("decision") or ""), 900),
            "next_action": compact_text(str(row.get("nextAction") or row.get("next_action") or ""), 500),
            "ownership_note": ownership_note,
        }
        upsert_evidence(conn, evidence)
        imported.append(evidence)
    return imported
