from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""First local evidence packet helpers and report writer."""

from .constants import (
    FIRST_LOCAL_EVIDENCE_PACKETS_JSON,
    FIRST_LOCAL_EVIDENCE_PACKETS_REPORT,
    FIRST_LOCAL_EVIDENCE_PACKETS_VALIDATION_JSON,
    FIRST_LOCAL_EVIDENCE_PACKET_DIR,
)
from .io import now_utc
from .paths import REPORTS_DIR
from .registry import upsert_evidence
from .service_workers import db_scalar


def first_local_evidence_summary(lane_id: str, spec_name: str, risk_gate: str) -> tuple[str, str]:
    summaries = {
        "ai_ml_competitions": (
            "Local first-evidence packet establishing the AI/ML competitions lane can now scout public prize registries under its source spec without account creation, gated dataset download, or submission.",
            "Create a local shortlist template from approved public sources; stop before account, terms, dataset, compute spend, or submission.",
        ),
        "content_and_social_growth": (
            "Local first-evidence packet establishing the content/social lane has a read-only Grok/X research source spec and must keep all public actions gated.",
            "Refresh the parked browser-readonly service request or create a local prompt/evidence template; no posts, replies, likes, follows, or settings changes.",
        ),
        "digital_products_templates_plugins": (
            "Local first-evidence packet establishing the digital-products lane can research marketplace demand and fees under a read-only source spec.",
            "Create a demand-scan worksheet from approved public sources; stop before account, listing, checkout, payment, or public marketplace action.",
        ),
        "lead_generation_and_sales": (
            "Local first-evidence packet establishing the lead-generation lane starts from policy and offer design, not real lead collection or outreach.",
            "Draft a local offer and source-category rubric; no scraping, CRM upload, email, DM, marketplace proposal, or contact form action.",
        ),
        "local_trading_strategy_research": (
            "Local first-evidence packet establishing the trading-research lane is paper/backtest-only and must not connect brokers or place trades.",
            "Inventory local backtest evidence standards and kill-switch fields; no broker, exchange, prediction-market, API, deposit, withdrawal, or order action.",
        ),
        "money_source_discovery": (
            "Local first-evidence packet establishing the money-source discovery lane can map public venues and gates without registration or outreach.",
            "Create a local venue-registry template with payout route, proof artifact, account gate, and first safe task; no registration, outreach, wallet, payment, or submission.",
        ),
    }
    return summaries.get(
        lane_id,
        (
            f"Local first-evidence packet for {lane_id} based on source spec {spec_name} and risk gate {risk_gate}.",
            "Create one local evidence artifact and stop before any gated external action.",
        ),
    )


def write_first_local_evidence_packets(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    packet_dir = Path(args.packet_dir) if args.packet_dir else FIRST_LOCAL_EVIDENCE_PACKET_DIR
    packet_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else FIRST_LOCAL_EVIDENCE_PACKETS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else FIRST_LOCAL_EVIDENCE_PACKETS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else FIRST_LOCAL_EVIDENCE_PACKETS_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    target_rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT l.lane_id, l.department, l.owner_agent_id, ss.spec_id, ss.name AS spec_name,
                   ss.source_type, ss.risk_gate
            FROM lanes l
            JOIN source_specs ss ON ss.lane_id = l.lane_id
            WHERE l.status = 'active'
              AND l.owner_agent_id IS NOT NULL
              AND l.lane_id NOT IN ('platform_engineering', 'submitted_bounty_payouts')
              AND l.lane_id NOT IN (SELECT lane_id FROM lane_evidence)
            ORDER BY l.lane_id
            """
        )
    ]
    zero_evidence_lane_count_before = len(target_rows)
    source_spec_gap_count_after = db_scalar(
        conn,
        """
        SELECT COUNT(*)
        FROM lanes
        WHERE status = 'active'
          AND owner_agent_id IS NOT NULL
          AND lane_id != 'submitted_bounty_payouts'
          AND lane_id NOT IN (SELECT lane_id FROM source_specs)
        """,
    )

    packet_rows: list[dict[str, Any]] = []
    for row in target_rows:
        lane_id = row["lane_id"]
        summary, next_action = first_local_evidence_summary(lane_id, row["spec_name"], row["risk_gate"])
        evidence_id = f"first-local-evidence-{lane_id}-20260615"
        packet_path = packet_dir / f"{lane_id}-first-local-evidence-20260615.json"
        md_path = packet_dir / f"{lane_id}-first-local-evidence-20260615.md"
        packet = {
            "schema_version": "agent_company.first_local_evidence_packet.v1",
            "generated_utc": generated_utc,
            "lane_id": lane_id,
            "department": row["department"],
            "owner_agent_id": row["owner_agent_id"],
            "evidence_id": evidence_id,
            "title": f"First local evidence packet for {lane_id}",
            "status": "local_seed_evidence",
            "source_spec": {
                "spec_id": row["spec_id"],
                "name": row["spec_name"],
                "source_type": row["source_type"],
                "risk_gate": row["risk_gate"],
            },
            "summary": summary,
            "next_action": next_action,
            "ownership_note": "Generated by platform_engineering as local first-evidence bootstrap; lane manager owns follow-up.",
            "local_only": True,
            "forbidden_actions": [
                "Do not browse or use signed-in sessions from this packet.",
                "Do not register accounts, accept terms, upload data, publish, submit, contact anyone, trade, touch wallets/payments, or run model/API calls.",
                "Do not mutate service requests, assign workers, or start workers from this packet.",
            ],
        }
        packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        md_lines = [
            f"# First Local Evidence Packet: {lane_id}",
            "",
            f"Generated UTC: {generated_utc}",
            f"JSON mirror: `{packet_path}`",
            "",
            "## Source Spec",
            "",
            f"- Spec: `{row['spec_id']}` - {row['spec_name']}",
            f"- Type: `{row['source_type']}`",
            f"- Risk gate: `{row['risk_gate']}`",
            "",
            "## Evidence",
            "",
            summary,
            "",
            "## Boundary",
            "",
            "This is local bootstrap evidence only. It does not browse, use accounts, accept terms, upload/download gated data, publish, submit, contact anyone, trade, touch wallets/payments, mutate service requests, assign/start workers, call APIs, or create external side effects.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        upsert_evidence(
            conn,
            {
                "evidence_id": evidence_id,
                "lane_id": lane_id,
                "source_path": str(md_path),
                "source_url": None,
                "title": packet["title"],
                "status": packet["status"],
                "summary": summary,
                "next_action": next_action,
                "ownership_note": packet["ownership_note"],
            },
        )
        packet_rows.append(
            {
                "lane_id": lane_id,
                "evidence_id": evidence_id,
                "packet_path": str(packet_path),
                "markdown_path": str(md_path),
                "source_spec_id": row["spec_id"],
                "local_only": True,
            }
        )
    conn.commit()

    zero_evidence_lane_count_after = db_scalar(
        conn,
        """
        SELECT COUNT(*)
        FROM lanes
        WHERE status = 'active'
          AND owner_agent_id IS NOT NULL
          AND lane_id NOT IN ('platform_engineering', 'submitted_bounty_payouts')
          AND lane_id NOT IN (SELECT lane_id FROM lane_evidence)
        """,
    )
    evidence_ids = [row["evidence_id"] for row in packet_rows]
    evidence_rows_present = db_scalar(
        conn,
        f"SELECT COUNT(*) FROM lane_evidence WHERE evidence_id IN ({','.join('?' for _ in evidence_ids)})"
        if evidence_ids
        else "SELECT 0",
        tuple(evidence_ids),
    )
    all_evidence_rows_present = evidence_rows_present == len(evidence_ids)
    all_target_lanes_have_evidence_after = zero_evidence_lane_count_after == 0
    all_evidence_packets_local_only = all(row["local_only"] for row in packet_rows)
    if zero_evidence_lane_count_before != 6:
        failures.append(f"expected 6 zero-evidence lanes before packet generation, got {zero_evidence_lane_count_before}")
    if len(packet_rows) != 6:
        failures.append(f"expected 6 evidence packets, got {len(packet_rows)}")
    if zero_evidence_lane_count_after != 0:
        failures.append(f"expected 0 zero-evidence lanes after packet generation, got {zero_evidence_lane_count_after}")
    if not all_evidence_rows_present:
        failures.append("not all first local evidence rows are present")
    if source_spec_gap_count_after != 0:
        failures.append(f"expected 0 source-spec gaps, got {source_spec_gap_count_after}")

    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    payload = {
        "schema_version": "agent_company.first_local_evidence_packets.v1",
        "generated_utc": generated_utc,
        "purpose": "Create local first-evidence packets and lane_evidence rows for owned non-platform lanes with no evidence rows.",
        "packet_dir": str(packet_dir),
        "evidence_packet_count": len(packet_rows),
        "evidence_rows_inserted_or_updated": len(packet_rows),
        "zero_evidence_lane_count_before": zero_evidence_lane_count_before,
        "zero_evidence_lane_count_after": zero_evidence_lane_count_after,
        "source_spec_gap_count_after": source_spec_gap_count_after,
        "all_target_lanes_have_evidence_after": all_target_lanes_have_evidence_after,
        "all_evidence_packets_local_only": all_evidence_packets_local_only,
        "all_evidence_rows_present": all_evidence_rows_present,
        "packet_rows": packet_rows,
        "runtime_boundary": runtime_boundary,
        "next_action": "Create narrow manager tasks for first approved local proof work, starting with lanes that still have parked service requests.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.first_local_evidence_packets_validation.v1",
        "generated_utc": generated_utc,
        "evidence_packets_path": str(json_output_path),
        "evidence_packet_count": len(packet_rows),
        "evidence_rows_inserted_or_updated": len(packet_rows),
        "zero_evidence_lane_count_before": zero_evidence_lane_count_before,
        "zero_evidence_lane_count_after": zero_evidence_lane_count_after,
        "all_target_lanes_have_evidence_after": all_target_lanes_have_evidence_after,
        "all_evidence_packets_local_only": all_evidence_packets_local_only,
        "all_evidence_rows_present": all_evidence_rows_present,
        "source_spec_gap_count_after": source_spec_gap_count_after,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# First Local Evidence Packets",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Zero-evidence lanes before: `{zero_evidence_lane_count_before}`",
        f"- Evidence packets generated: `{len(packet_rows)}`",
        f"- Zero-evidence lanes after: `{zero_evidence_lane_count_after}`",
        f"- Source-spec gaps after: `{source_spec_gap_count_after}`",
        "",
        "## Packets",
        "",
        "| Lane | Evidence | Source Spec | JSON | Markdown |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            f"| `{row['lane_id']}` | `{row['evidence_id']}` | `{row['source_spec_id']}` | `{row['packet_path']}` | `{row['markdown_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- These packets are local bootstrap evidence only.",
            "- They do not browse, register accounts, accept terms, upload/download gated data, publish, submit, contact anyone, trade, touch wallets/payments, mutate service requests, assign/start workers, call APIs, or create external side effects.",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "packet_dir": str(packet_dir),
                "evidence_packet_count": len(packet_rows),
                "zero_evidence_lane_count_after": zero_evidence_lane_count_after,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
