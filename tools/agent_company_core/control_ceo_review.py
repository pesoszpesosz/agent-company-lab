from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    CEO_REVIEW_REPORT,
    COMPANY_EXPANSION_GAP_MAP_JSON,
    COMPANY_EXPANSION_GAP_MAP_REPORT,
    COMPANY_EXPANSION_GAP_MAP_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_workers import db_scalar
from .utils import md_cell

def lane_recommendation(lane_id: str, status_counts: dict[str, int], active_tasks: int, service_requests: int) -> str:
    status_text = " ".join(status_counts.keys()).lower()
    if lane_id == "submitted_bounty_payouts":
        return "Read-only visibility only. Parallel payout worker owns monitoring and GitHub follow-up."
    if lane_id == "platform_engineering":
        if active_tasks:
            return "Finish active platform task, then promote separate lane-manager launches from manager packets."
        return "Launch separate lane-manager chats from manager packets; keep real model/API execution behind the pending service request."
    if lane_id == "security_bounty_private_reports":
        if "submission_ready" in status_text or "verified_patch_candidate" in status_text or "private_report" in status_text:
            return "Launch a security manager to rank private-report drafts, rules gates, and proof gaps. No submissions without approval."
        return "Launch only rules-first source scouting and static review; keep account/testing gates explicit."
    if lane_id == "prediction_market_research":
        return "Launch a data/replay manager only. Keep Polymarket data-only and all real-money trading behind eligibility and treasury gates."
    if lane_id == "paid_code_bounties":
        if "rejected" in status_text or "parked" in status_text:
            return "Use imported rows as negative samples. Launch a fresh-source scout, not a PR worker, until a clean unclaimed bounty is found."
        return "Launch a paid-code scout with duplicate checks, then a patch worker only after claim and payout rules are clean."
    if lane_id == "web3_airdrops_grants_hackathons":
        return "Keep as gated venture lane. Launch terms/deadline scouting only; no wallet, deployment, or registration without approval."
    if lane_id == "content_and_social_growth":
        return "Use X/Grok/Radar as read-only discovery until a human-reviewed public-action workflow is assigned."
    if lane_id == "lead_generation_and_sales":
        return "Design non-spam offer and CRM rules before any email, DM, marketplace, or account action."
    if lane_id == "local_trading_strategy_research":
        return "Use only local backtests and paper evidence. Real-money execution needs broker, treasury, and kill-switch gates."
    if service_requests:
        return "Resolve service requests before assigning more workers."
    return "Create one narrow manager task with evidence requirements before launching seekers."


def write_ceo_review(conn: sqlite3.Connection, path: str | None) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(path) if path else CEO_REVIEW_REPORT
    lanes = [dict(row) for row in conn.execute("SELECT lane_id, department, owner_agent_id, owner_thread_id, status FROM lanes ORDER BY lane_id")]
    evidence_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id")
    }
    status_counts_by_lane: dict[str, dict[str, int]] = {}
    for row in conn.execute("SELECT lane_id, status, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id, status"):
        status_counts_by_lane.setdefault(row["lane_id"], {})[row["status"]] = row["count"]
    active_task_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute(
            "SELECT lane_id, COUNT(*) AS count FROM tasks WHERE status NOT IN ('complete', 'cancelled') GROUP BY lane_id"
        )
    }
    service_request_counts = {
        row["lane_id"] or "unassigned": row["count"]
        for row in conn.execute(
            "SELECT COALESCE(lane_id, 'unassigned') AS lane_id, COUNT(*) AS count FROM service_requests WHERE status NOT IN ('complete', 'cancelled') GROUP BY COALESCE(lane_id, 'unassigned')"
        )
    }
    top_evidence = [
        dict(row)
        for row in conn.execute(
            """
            SELECT evidence_id, lane_id, status, title, source_url, source_path, next_action, ownership_note
            FROM lane_evidence
            WHERE lane_id NOT IN ('submitted_bounty_payouts', 'platform_engineering')
            ORDER BY
              CASE
                WHEN status LIKE '%submission%' THEN 1
                WHEN status LIKE '%verified%' THEN 2
                WHEN status LIKE '%promote%' THEN 3
                WHEN status LIKE '%watch%' THEN 4
                ELSE 5
              END,
              updated_at DESC
            LIMIT 20
            """
        )
    ]
    read_only_payout_evidence = [
        dict(row)
        for row in conn.execute(
            """
            SELECT evidence_id, lane_id, status, title, source_url, source_path, next_action, ownership_note
            FROM lane_evidence
            WHERE lane_id = 'submitted_bounty_payouts'
            ORDER BY updated_at DESC
            LIMIT 10
            """
        )
    ]
    service_requests = [
        dict(row)
        for row in conn.execute(
            "SELECT request_id, service_id, request_type, lane_id, status, risk_gate, requested_action, assigned_agent_id, artifact_path, decision_note FROM service_requests ORDER BY created_at DESC LIMIT 25"
        )
    ]
    service_catalog = [
        dict(row)
        for row in conn.execute(
            "SELECT service_id, request_type, owner_role_id, default_status, purpose FROM service_catalog ORDER BY request_type, service_id"
        )
    ]
    tasks = [
        dict(row)
        for row in conn.execute(
            "SELECT task_id, lane_id, status, priority, title, next_action FROM tasks ORDER BY priority DESC, created_at DESC LIMIT 50"
        )
    ]

    lines = [
        "# Agent Company CEO Review",
        "",
        f"Generated UTC: {now_utc()}",
        f"Database: `{DB_PATH}`",
        "",
        "## Executive Directives",
        "",
        "- Keep this thread on `platform_engineering` unless explicitly reassigned.",
        "- Do not duplicate the parallel payout worker. `submitted_bounty_payouts` is read-only here.",
        "- Future lane managers must claim lanes, acquire tasks, and record evidence before acting.",
        "- Account registration, wallets, public posts, PR comments, bounty submissions, payment details, KYC, billing, and real-money trades are service-request gates.",
        "",
        "## Lane Scoreboard",
        "",
        "| Lane | Department | Evidence | Open Tasks | Service Requests | Owner | Recommendation |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for lane in lanes:
        lane_id = lane["lane_id"]
        recommendation = lane_recommendation(
            lane_id,
            status_counts_by_lane.get(lane_id, {}),
            active_task_counts.get(lane_id, 0),
            service_request_counts.get(lane_id, 0),
        )
        owner = lane["owner_agent_id"] or lane["owner_thread_id"] or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{lane_id}`",
                    md_cell(lane["department"], 120),
                    str(evidence_counts.get(lane_id, 0)),
                    str(active_task_counts.get(lane_id, 0)),
                    str(service_request_counts.get(lane_id, 0)),
                    md_cell(owner, 160),
                    md_cell(recommendation, 360),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Suggested Launch Order", ""])
    launch_order = [
        ("platform_engineering", "Use manager packets to launch separate lane-manager chats; keep real model/API execution behind the pending service request."),
        ("security_bounty_private_reports", "Rank private-report drafts and rules gates; no external submission without approval."),
        ("prediction_market_research", "Build paper-only replay and source-of-truth monitors; no trades."),
        ("paid_code_bounties", "Use negative samples to improve fresh-source scouting before any PR worker."),
        ("content_and_social_growth", "Run read-only X/Grok/Radar discovery after browser state is clean; no public actions."),
        ("web3_airdrops_grants_hackathons", "Scout deadlines and terms only; no wallet/account/deployment action."),
        ("lead_generation_and_sales", "Draft compliant offer and targeting rules before outreach."),
        ("local_trading_strategy_research", "Run backtest/paper evidence only."),
    ]
    for index, (lane_id, reason) in enumerate(launch_order, start=1):
        lines.append(f"{index}. `{lane_id}` - {reason}")
    lines.extend(["", "## High-Signal Evidence", "", "| Lane | Status | Evidence | Source | Next Action |", "| --- | --- | --- | --- | --- |"])
    for item in top_evidence:
        source = item["source_url"] or item["source_path"] or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    md_cell(item["status"], 120),
                    f"`{item['evidence_id']}` - {md_cell(item['title'], 180)}",
                    md_cell(source, 180),
                    md_cell(item["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read-Only Payout Evidence",
            "",
            "These rows are visibility only. The parallel payout worker owns monitoring and GitHub follow-up.",
            "",
            "| Status | Evidence | Source | Next Action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in read_only_payout_evidence:
        source = item["source_url"] or item["source_path"] or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item["status"], 120),
                    f"`{item['evidence_id']}` - {md_cell(item['title'], 180)}",
                    md_cell(source, 180),
                    md_cell(item["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Open Service Requests", "", "| Status | Service | Type | Lane | Assigned | Gate | Requested Action | Artifact | Decision Note |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for req in service_requests:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(req["status"], 80),
                    md_cell(req["service_id"], 120),
                    md_cell(req["request_type"], 120),
                    f"`{req['lane_id'] or ''}`",
                    md_cell(req["assigned_agent_id"], 120),
                    md_cell(req["risk_gate"], 180),
                    md_cell(req["requested_action"], 320),
                    md_cell(req["artifact_path"], 180),
                    md_cell(req["decision_note"], 220),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Service Bureau Catalog", "", "Use these entries to route side-effect-adjacent needs. Catalog entries do not approve actions; they define intake and hard stops.", "", "| Status | Type | Service | Owner Role | Purpose |", "| --- | --- | --- | --- | --- |"])
    for service in service_catalog:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(service["default_status"], 80),
                    md_cell(service["request_type"], 120),
                    f"`{service['service_id']}`",
                    f"`{service['owner_role_id']}`",
                    md_cell(service["purpose"], 280),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Task Register", "", "| Priority | Status | Lane | Task | Next Action |", "| ---: | --- | --- | --- | --- |"])
    for task in tasks:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(task["priority"]),
                    md_cell(task["status"], 80),
                    f"`{task['lane_id']}`",
                    f"`{task['task_id']}` - {md_cell(task['title'], 220)}",
                    md_cell(task["next_action"], 260),
                ]
            )
            + " |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path)}, indent=2))

