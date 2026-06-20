from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .catalog import seed
from .constants import PROFIT_EDGE_IMPORT_REPORT
from .io import now_utc
from .paths import REPORTS_DIR
from .registry import evidence_id_for_source, upsert_evidence
from .utils import md_cell
from .profit_edge_ledger_import import SUBMITTED_PAYOUT_OWNERSHIP_NOTE, import_ledger_rows
from .profit_edge_source_summary import summarize_source_file
SUBMITTED_PAYOUT_OWNERSHIP_NOTE = (
    "Read-only import. The parallel Find profitable edge worker owns payout monitoring and GitHub follow-up for this lane."
)

PROFIT_EDGE_REPORT_IMPORTS = [
    {
        "relative_path": "reports/daily-action-queue-latest.md",
        "lane_id": "platform_engineering",
        "title": "Profit Edge Daily Action Queue",
        "ownership_note": "Read-only source snapshot used for lane routing and infrastructure design.",
    },
    {
        "relative_path": "reports/submitted-bounty-monitor-latest.md",
        "lane_id": "submitted_bounty_payouts",
        "title": "Submitted Bounty Monitor",
        "ownership_note": SUBMITTED_PAYOUT_OWNERSHIP_NOTE,
    },
    {
        "relative_path": "reports/charles-submission-monitor-latest.md",
        "lane_id": "submitted_bounty_payouts",
        "title": "Charles Submission Monitor",
        "ownership_note": SUBMITTED_PAYOUT_OWNERSHIP_NOTE,
    },
    {
        "relative_path": "reports/submitted-security-advisory-monitor-latest.md",
        "lane_id": "security_bounty_private_reports",
        "title": "Submitted Security Advisory Monitor",
        "ownership_note": "Read-only security-lane evidence; no external report submission from this infrastructure thread.",
    },
    {
        "relative_path": "reports/security-bounty-source-scan-latest.md",
        "lane_id": "security_bounty_private_reports",
        "title": "Security Bounty Source Scan",
        "ownership_note": "Read-only source evidence for future security department workers.",
    },
    {
        "relative_path": "reports/google-oss-static-review-shortlist-latest.md",
        "lane_id": "security_bounty_private_reports",
        "title": "Google OSS Static Review Shortlist",
        "ownership_note": "Read-only source evidence for future security department workers.",
    },
    {
        "relative_path": "reports/issuehunt-security-program-scan-latest.md",
        "lane_id": "security_bounty_private_reports",
        "title": "IssueHunt Security Program Scan",
        "ownership_note": "Read-only source evidence for future security department workers.",
    },
    {
        "relative_path": "reports/sherlock-contest-1259-detail-latest.md",
        "lane_id": "security_bounty_private_reports",
        "title": "Sherlock Contest Detail",
        "ownership_note": "Read-only contest evidence; registration/account gates remain separate service requests.",
    },
    {
        "relative_path": "reports/prediction-market-scan-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Prediction Market Scan",
        "ownership_note": "Read-only market research; no real-money trading from this infrastructure thread.",
    },
    {
        "relative_path": "reports/cross-venue-next-team-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Cross-Venue Next-Team Scan",
        "ownership_note": "Read-only market research; no real-money trading from this infrastructure thread.",
    },
    {
        "relative_path": "reports/polymarket-tennis-edge-packet-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Polymarket Tennis Edge Packet",
        "ownership_note": "Read-only market research; Polymarket remains data-only unless eligibility is explicitly verified.",
    },
    {
        "relative_path": "reports/kalshi-btc-range-edge-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Kalshi BTC Range Edge",
        "ownership_note": "Read-only market research; no real-money trading from this infrastructure thread.",
    },
    {
        "relative_path": "reports/kalshi-btc-settlement-lag-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Kalshi BTC Settlement Lag",
        "ownership_note": "Read-only market research; no real-money trading from this infrastructure thread.",
    },
    {
        "relative_path": "reports/kalshi-crypto-settlement-lag-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Kalshi Crypto Settlement Lag",
        "ownership_note": "Read-only market research; no real-money trading from this infrastructure thread.",
    },
    {
        "relative_path": "reports/kalshi-settlement-lag-latest.md",
        "lane_id": "prediction_market_research",
        "title": "Kalshi Generic Settlement Lag",
        "ownership_note": "Read-only market research; no real-money trading from this infrastructure thread.",
    },
    {
        "relative_path": "reports/bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "Paid Code Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/github-fresh-bounty-pulse-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "Fresh GitHub Bounty Pulse",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/algora-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "Algora Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/opire-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "Opire Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/bountyhub-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "BountyHub Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/boss-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "BOSS Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/gibwork-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "Gibwork Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/gitpay-task-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "Gitpay Task Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/unitone-skill-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "UnitOne Skill Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/projectdiscovery-bounty-scan-latest.md",
        "lane_id": "paid_code_bounties",
        "title": "ProjectDiscovery Bounty Scan",
        "ownership_note": "Read-only evidence for future paid-code workers; this thread is not submitting PRs.",
    },
    {
        "relative_path": "reports/web3-public-code-target-shortlist-latest.md",
        "lane_id": "web3_airdrops_grants_hackathons",
        "title": "Web3 Public Code Target Shortlist",
        "ownership_note": "Read-only venture/security source evidence; wallet, account, and submission gates remain separate.",
    },
    {
        "relative_path": "opportunities/manual-overrides.jsonl",
        "lane_id": "platform_engineering",
        "title": "Profit Edge Manual Overrides",
        "ownership_note": "Read-only negative-sample and policy memory for future lane managers.",
    },
]

def write_profit_edge_import_report(
    source_root: Path,
    imported: list[dict[str, str | None]],
    missing: list[str],
    task_id: str | None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for item in imported:
        counts[item["lane_id"] or "unknown"] = counts.get(item["lane_id"] or "unknown", 0) + 1
    lines = [
        "# Profit Edge Import Bridge",
        "",
        f"Generated UTC: {now_utc()}",
        f"Source root: `{source_root}`",
        f"Task: `{task_id or ''}`",
        "",
        "## Boundary",
        "",
        "- This is a read-only import into the agent-company control plane.",
        "- `submitted_bounty_payouts` stays owned by the parallel payout-monitoring worker.",
        "- This thread uses imported rows only for infrastructure, lane routing, launch packets, and future task assignment.",
        "",
        "## Counts By Lane",
        "",
        "| Lane | Imported Rows |",
        "| --- | ---: |",
    ]
    for lane_id, count in sorted(counts.items()):
        lines.append(f"| `{lane_id}` | {count} |")
    lines.extend(["", "## Imported Evidence", "", "| Lane | Status | Evidence | Source | Next Action |", "| --- | --- | --- | --- | --- |"])
    for item in imported:
        source = item.get("source_url") or item.get("source_path") or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    md_cell(item.get("status"), 120),
                    f"`{item['evidence_id']}` - {md_cell(item.get('title'), 180)}",
                    md_cell(source, 180),
                    md_cell(item.get("next_action"), 220),
                ]
            )
            + " |"
        )
    if missing:
        lines.extend(["", "## Missing Sources", ""])
        lines.extend([f"- `{path}`" for path in missing])
    PROFIT_EDGE_IMPORT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return PROFIT_EDGE_IMPORT_REPORT


def import_profit_edge(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    seed(conn)
    source_root = Path(args.source_root).resolve()
    imported: list[dict[str, str | None]] = []
    missing: list[str] = []
    conn.execute("DELETE FROM lane_evidence WHERE evidence_id LIKE 'pe-report-%' OR evidence_id LIKE 'pe-ledger-%'")
    for spec in PROFIT_EDGE_REPORT_IMPORTS:
        path = source_root / str(spec["relative_path"])
        if not path.exists():
            missing.append(str(path))
            continue
        summary = summarize_source_file(path, str(spec["title"]))
        source_key = str(path)
        evidence = {
            "evidence_id": evidence_id_for_source("pe-report", source_key, str(spec["title"])),
            "lane_id": str(spec["lane_id"]),
            "source_path": str(path),
            "source_url": None,
            "title": str(summary["title"] or spec["title"]),
            "status": str(summary["status"] or "imported"),
            "summary": summary.get("summary"),
            "next_action": summary.get("next_action"),
            "ownership_note": str(spec["ownership_note"]),
        }
        upsert_evidence(conn, evidence)
        imported.append(evidence)
    if args.ledger_tail > 0:
        imported.extend(import_ledger_rows(conn, source_root, args.ledger_tail))
    report_path = write_profit_edge_import_report(source_root, imported, missing, args.task_id)
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, notes, created_at)
        VALUES(?, 'platform_engineering', ?, 'profit_edge_import_report', ?, ?, ?)
        ON CONFLICT(artifact_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          kind=excluded.kind,
          path_or_url=excluded.path_or_url,
          notes=excluded.notes
        """,
        (
            "artifact-profit-edge-import-latest",
            args.task_id,
            str(report_path),
            f"Imported {len(imported)} read-only evidence row(s) from {source_root}; {len(missing)} source(s) missing.",
            ts,
        ),
    )
    conn.commit()
    print(
        json.dumps(
            {
                "ok": True,
                "source_root": str(source_root),
                "imported": len(imported),
                "missing": len(missing),
                "report": str(report_path),
            },
            indent=2,
        )
    )
